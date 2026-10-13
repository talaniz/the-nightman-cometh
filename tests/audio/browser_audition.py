"""Actual Chromium/pygbag audition workflow; no claim of human hearing."""
import argparse
import functools
import hashlib
import http.server
import json
from pathlib import Path
import threading
import time
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True)
    args=ap.parse_args();args.evidence.mkdir(parents=True,exist_ok=True)
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(args.build)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    errors=[];captures=[];checks=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':1280,'height':720})
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('requestfailed',lambda r:errors.append(r.url+' '+str(r.failure)))
            page.on('console',lambda m:errors.append(m.text) if m.type=='error' and 'MEDIA USER ACTION REQUIRED' not in m.text else None)
            page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='domcontentloaded')
            deadline=time.monotonic()+150
            while not page.evaluate('Boolean(window.__nightmanAudio)'):
                assert time.monotonic()<deadline,'pygbag startup timed out'
                page.wait_for_timeout(1000);page.mouse.click(480,330)
            page.locator('#canvas').focus()
            def state():return json.loads(page.evaluate('window.__nightmanAudio'))
            def key(k,wait=180):page.keyboard.press(k);page.wait_for_timeout(wait)
            def capture(name):
                page.screenshot(path=str(args.evidence/(name+'.png')))
                captures.append({'file':name+'.png','viewport':page.viewport_size,'state':state()})
            assert not state()['unlocked'] and state()['music_busy']==0
            capture('locked-1280')
            key('Enter',600)
            assert state()['unlocked'] and state()['music_busy']==1
            assert state()['gains'][0]>.2,'unlocked music channel is silent'
            capture('playing-1280');checks.append('gesture unlock and nonzero mixer gain')
            page.evaluate("window.dispatchEvent(new Event('blur'))");page.wait_for_timeout(180)
            assert state()['paused'],'browser blur did not pause'
            page.evaluate("window.dispatchEvent(new Event('focus'))");key('p')
            checks.append('browser blur event pauses; explicit resume')
            key('d');assert state()['playing']=='dayman-fast'
            key('p');remaining=state()['remaining'];page.wait_for_timeout(500)
            assert state()['paused'] and abs(state()['remaining']-remaining)<.05
            capture('paused-1280')
            key('p');key('m');assert state()['muted'] and state()['gains']==[0.0,0.0]
            capture('muted-1280');key('m')
            # Changing scene during transformation must restore the new scene.
            for _ in range(5):key('ArrowDown',30)
            key('Enter');assert state()['scene']=='bridge'
            page.wait_for_timeout(11000)
            assert state()['remaining']==0 and state()['playing']=='troll-toll'
            checks.append('pause freezes override; mute independent; expiry restores current bridge')
            key('x');assert state()['error'] and state()['playing'] is None
            capture('asset-error-1280');key('r',400)
            assert not state()['error'] and state()['playing']=='troll-toll' and state()['music_busy']==1
            capture('recovered-1280');checks.append('actual missing Ogg load and retry recovery')
            # Abduction sting has a finite destination and can be skipped.
            key('ArrowUp');key('Enter');assert state()['scene']=='frank-kidnap'
            page.wait_for_timeout(3700);assert state()['scene']=='bridge'
            key('ArrowDown');key('Enter');assert state()['scene']=='bridge'
            checks.append('finite sting advances, manual scene selection remains usable')
            # Space repeatedly exercises actual SDL voices, not an injected mixer.
            for _ in range(8):key('Space',5)
            assert state()['sfx_busy']<=4
            for _ in range(7):key('1',20);key('3',20)
            assert state()['gains']==[0.0,0.0]
            checks.append('actual effect voice cap and independent zero music/effect volumes')
            page.set_viewport_size({'width':1920,'height':1080});page.wait_for_timeout(300);capture('desktop-1920')
            page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(300)
            assert page.locator('#narrow').is_visible()
            assert 'desktop browser and keyboard' in page.locator('#narrow').inner_text()
            capture('narrow-390');checks.append('desktop and narrow-device guidance')
            assert not errors,errors
            version=browser.version;browser.close()
        files=sorted([ROOT/'tools/audition.py',*(ROOT/'tools/audio/audition_app').glob('*.py'),ROOT/'assets/audio/production/manifest.json'])
        fingerprint=hashlib.sha256(''.join(str(f.relative_to(ROOT))+hashlib.sha256(f.read_bytes()).hexdigest() for f in files).encode()).hexdigest()
        (args.evidence/'manifest.json').write_text(json.dumps({'source_tree_sha256':fingerprint,'browser':version,
            'build_files':{str(f.relative_to(args.build)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(args.build.rglob('*')) if f.is_file()},
            'captures':captures,'checks':checks,'errors':errors,'hearing':'not established by headless checks'},indent=2)+'\n')
        print(json.dumps({'ok':True,'checks':checks,'captures':len(captures)}))
    finally:server.shutdown();server.server_close()

if __name__=='__main__':main()
