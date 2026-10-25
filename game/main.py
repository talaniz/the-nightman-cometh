"""Async pygame game entrypoint and boundary adapters."""
import asyncio
import json
from pathlib import Path
import sys
import time
import pygame
from game.session import Session
from game.render import Renderer
from game.world import DT
from game.audio import retry_audio
from tools.audio.audition_app.backend import Mixer
from tools.audio.audition_app.director import Director

WEB=sys.platform=='emscripten'
if WEB:from platform import window

class Storage:
    def __init__(self):self.raw=None
    def read(self):return window.localStorage.getItem('nightman.progress.v1') if WEB else self.raw
    def write(self,value):
        if WEB:window.localStorage.setItem('nightman.progress.v1',value)
        else:self.raw=value

async def main():
    pygame.init();screen=pygame.display.set_mode((960,540));pygame.display.set_caption('The Nightman Cometh')
    renderer=Renderer(screen);session=Session(Storage());held=set();pending=set()
    root=Path('audio') if Path('audio/manifest.json').is_file() else Path(__file__).resolve().parents[1]/'assets/audio/production'
    manifest=json.loads((root/'manifest.json').read_text());mixer=Mixer(manifest,root);audio=Director(manifest,mixer)
    audio.volumes(music=session.progress.settings['music'],sfx=session.progress.settings['effects']);audio.unlock()
    previous=time.monotonic();previous_screen='title';frames=[];frame_count=0
    fixture_path=Path('test-fixtures.json');test_mode=fixture_path.is_file()
    while True:
        now=time.monotonic();dt=min(.1,now-previous);previous=now;frames.append(dt*1000);frames=frames[-120:]
        for event in pygame.event.get():
            if event.type==pygame.QUIT:return
            if event.type==pygame.WINDOWFOCUSLOST:
                held.clear();pending.clear();session.blur()
            if event.type==pygame.KEYUP:held.discard(event.key)
            if event.type!=pygame.KEYDOWN:continue
            key=event.key
            if key in held:continue
            held.add(key)
            if session.screen=='password':
                if key==pygame.K_ESCAPE:session.back()
                elif key==pygame.K_RETURN:session.activate()
                elif key==pygame.K_BACKSPACE:session.password=session.password[:-1]
                elif getattr(event,'unicode','').isascii() and event.unicode.isalnum() and len(session.password)<16:session.password+=event.unicode.upper()
                continue
            if key==pygame.K_ESCAPE:session.back();held.clear();pending.clear()
            elif key==pygame.K_RETURN:session.activate()
            elif key==pygame.K_m:audio.volumes(muted=not audio.muted)
            elif key==pygame.K_r:retry_audio(audio,session.world.player.dayman if audio.scene=='level1' else 0,audio.paused)
            elif session.screen=='training':
                if key==pygame.K_SPACE:pending.add('jump')
                if key==pygame.K_j:pending.add('bat')
                if key==pygame.K_k:pending.add('beam')
            elif key in (pygame.K_UP,pygame.K_DOWN):session.select(-1 if key==pygame.K_UP else 1)
            elif key in (pygame.K_LEFT,pygame.K_RIGHT):session.adjust(-1 if key==pygame.K_LEFT else 1)
        # Test fixture mutation is absent from regular builds. QA passwords are separate.
        if test_mode and WEB:
            raw=str(window.__nightmanFixture or '')
            if raw:
                window.__nightmanFixture=''
                from game.fixtures import apply
                request=json.loads(raw)
                if request.get('name')=='audio-error':
                    mixer.fail_next=True
                    retry_audio(audio,session.world.player.dayman if audio.scene=='level1' else 0,audio.paused)
                else:apply(session,request)
                held.clear();pending.clear()
        before=session.world.steps
        controls={'left':bool(held & {pygame.K_LEFT,pygame.K_a}),'right':bool(held & {pygame.K_RIGHT,pygame.K_d}),**{k:True for k in pending}}
        session.update(dt,controls)
        if session.world.steps!=before:pending.clear()
        if session.screen!=previous_screen:
            if session.screen=='training':
                # Leaving death/pause also clears any prior audio transformation state.
                audio.remaining=session.world.player.dayman
                audio.set_scene('level1');audio._play()
            elif session.screen=='dialogue':audio.remaining=0;audio.set_scene('narration')
            elif session.screen=='title':audio.remaining=0;audio.set_scene('title')
            previous_screen=session.screen
        audio.pause(session.screen in ('pause','dead','options','confirm','password'))
        audio.volumes(music=session.progress.settings['music'],sfx=session.progress.settings['effects'])
        for event in session.world.events:
            if event=='meal':audio.transform()
            audio.effect(event)
        session.world.events.clear()
        audio.tick((session.world.steps-before)*DT if session.screen=='training' else dt)
        renderer.draw(session,audio);frame_count+=1
        if WEB:
            state={'screen':session.screen,'selection':session.selection,'menu':session.menu(),'qa':session.qa,'qa_label':session.qa_label,
                   'message':session.message or session.progress.message,'settings':session.progress.settings,'dialogue':session.dialogue,
                   'world':session.world.snapshot(),'audio':{'playing':audio.playing,'muted':audio.muted,'error':audio.error,**mixer.state()},
                   'loops':1,'frames':frame_count,'frame_ms_mean':sum(frames)/len(frames),'test_build':test_mode,
                   'python':sys.version,'pygame':pygame.version.ver}
            window.__nightmanGame=json.dumps(state)
        await asyncio.sleep(0)

if __name__=='__main__':asyncio.run(main())
