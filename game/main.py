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
from game.input.controls import Controls
from game.input.actions import perform
from game.audio import retry_audio, gameplay_manifest
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

def initialize_display():
    # Browser Gamepad access belongs to our guarded adapter, not SDL joystick.
    pygame.display.init()
    pygame.font.init()
    return pygame.display.set_mode((960,540))

async def main():
    screen=initialize_display();pygame.display.set_caption('The Nightman Cometh')
    renderer=Renderer(screen);session=Session(Storage());held=set();pending=set();inputs=Controls();session.input_state=inputs.snapshot()
    root=Path('audio') if Path('audio/manifest.json').is_file() else Path(__file__).resolve().parents[1]/'assets/audio/production'
    manifest=json.loads((root/'manifest.json').read_text());mixer=Mixer(manifest,root);audio=Director(gameplay_manifest(manifest),mixer)
    audio.volumes(music=session.progress.settings['music'],sfx=session.progress.settings['effects']);audio.unlock()
    previous=time.monotonic();previous_screen='title';frames=[];frame_count=0
    fixture_path=Path('test-fixtures.json');test_mode=fixture_path.is_file();fixture_id=None
    while True:
        now=time.monotonic();dt=min(.1,now-previous);previous=now;frames.append(dt*1000);frames=frames[-120:]
        context=(session.screen,session.dialogue)
        keymap={pygame.K_LEFT:'left',pygame.K_a:'left',pygame.K_RIGHT:'right',pygame.K_d:'right',
                pygame.K_UP:'up',pygame.K_DOWN:'down',pygame.K_RETURN:'confirm',pygame.K_ESCAPE:'back',
                pygame.K_SPACE:'jump',pygame.K_j:'bat',pygame.K_k:'beam',pygame.K_m:'mute',pygame.K_r:'retry'}
        for event in pygame.event.get():
            if event.type==pygame.QUIT:return
            if event.type==pygame.WINDOWFOCUSLOST:
                held.clear();pending.clear();inputs.keys.clear();inputs.blocked_keys.clear();inputs.quarantine();session.blur()
            if event.type==pygame.KEYUP:
                held.discard(event.key)
                action=keymap.get(event.key)
                if action and not any(keymap.get(k)==action for k in held):inputs.key_up(action)
            if event.type!=pygame.KEYDOWN or event.key in held:continue
            key=event.key;held.add(key)
            if session.screen=='password' and key not in (pygame.K_ESCAPE,pygame.K_RETURN,pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT):
                inputs.pad_mode=False
                if key==pygame.K_BACKSPACE:session.password=session.password[:-1]
                elif getattr(event,'unicode','').isascii() and event.unicode.isalnum() and len(session.password)<16:session.password+=event.unicode.upper()
                continue
            action=keymap.get(key)
            if action:inputs.key_down(action)
        pad=json.loads(str(window.nightmanReadPad())) if WEB else {'status':'absent'}
        focused=pad.get('focused',True)
        directions,pressed,lost=inputs.sample(pad,session.screen,focused)
        if lost or not focused:
            held.clear();inputs.keys.clear();inputs.blocked_keys.clear();pending.clear();session.blur()
        else:
            pending.update(perform(session,audio,inputs,pressed))
        if context!=(session.screen,session.dialogue):
            inputs.quarantine();pending.clear();directions=set()
        session.input_state=inputs.snapshot()
        # Test fixture mutation is absent from regular builds. QA passwords are separate.
        if test_mode and WEB:
            raw=str(window.__nightmanFixture or '')
            if raw:
                window.__nightmanFixture=''
                from game.fixtures import apply
                request=json.loads(raw)
                if request.get('name')=='audio-error':
                    mixer.fail_next=True
                    retry_audio(audio,session.world.player.dayman if audio.scene in ('level1','cricket','bridge','frank','rooftop','nightman') else 0,audio.paused)
                else:
                    apply(session,request);previous_screen='fixture'
                fixture_id=request.get('id')
                held.clear();inputs.keys.clear();inputs.quarantine();pending.clear();directions=set()
        before=session.world.steps
        controls={'left':'left' in directions,'right':'right' in directions,**{k:True for k in pending}}
        before_screen=session.screen
        session.update(dt,controls)
        if session.screen!=before_screen:inputs.quarantine();pending.clear()
        if session.world.steps!=before:pending.clear()
        desired=session.music_scene() or audio.scene
        if desired!=audio.scene or session.screen!=previous_screen and session.screen=='training':
            audio.remaining=session.world.player.dayman if session.screen=='training' else 0
            audio.set_scene(desired)
            if audio.remaining:audio._play()
        previous_screen=session.screen
        audio.pause(session.screen in ('pause','dead','options','confirm','password'))
        audio.volumes(music=session.progress.settings['music'],sfx=session.progress.settings['effects'])
        for event in session.world.events:
            if event=='meal':audio.transform()
            audio.effect('boss-defeat' if event=='defeat' else event) if event!='boss-start' else None
        session.world.events.clear()
        audio.tick((session.world.steps-before)*DT if session.screen=='training' else dt)
        renderer.draw(session,audio);frame_count+=1
        if WEB:
            state={'input':inputs.snapshot(),'password':session.password,'screen':session.screen,'selection':session.selection,'menu':session.menu(),'qa':session.qa,'qa_label':session.qa_label,
                   'message':session.message or session.progress.message,'settings':session.progress.settings,'dialogue':session.dialogue,
                   'story':{'count':len(session.sequence),'speaker':session.sequence[min(session.dialogue,len(session.sequence)-1)].speaker,'text':session.sequence[min(session.dialogue,len(session.sequence)-1)].text},'world':session.world.snapshot(),'audio':{'playing':audio.playing,'muted':audio.muted,'error':audio.error,**mixer.state()},
                   'fixture_id':fixture_id,'loops':1,'frames':frame_count,'frame_ms_mean':sum(frames)/len(frames),'test_build':test_mode,
                   'python':sys.version,'pygame':pygame.version.ver}
            window.__nightmanGame=json.dumps(state)
        await asyncio.sleep(0)

if __name__=='__main__':asyncio.run(main())
