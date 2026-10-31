import json
from pathlib import Path
from game.audio import retry_audio
from tools.audio.audition_app.director import Director

class Backend:
    def stop(self):pass
    def music(self,cue,loop):self.cue=cue
    def volumes(self,*args):pass
    def pause(self,value):self.paused=value
    def tick(self,dt):pass

def test_audio_recovery_uses_game_timer_and_preserves_pause():
    manifest=json.loads(Path('assets/audio/production/manifest.json').read_text())
    backend=Backend();audio=Director(manifest,backend);audio.unlock();audio.set_scene('level1');audio.transform()
    retry_audio(audio,remaining=4.25,paused=True)
    assert audio.remaining==4.25
    assert audio.playing=='dayman-fast' and backend.paused
    retry_audio(audio,remaining=0,paused=False)
    assert audio.playing=='little-boy' and not backend.paused

def test_kidnapping_music_never_advances_a_player_controlled_scene():
    from game.audio import gameplay_manifest
    manifest=json.loads(Path('assets/audio/production/manifest.json').read_text())
    audio=Director(gameplay_manifest(manifest),Backend());audio.unlock();audio.set_scene('nightman-kidnap')
    audio.tick(120)
    assert audio.scene=='nightman-kidnap'
    assert manifest['next']['nightman-kidnap']=='rooftop','Audition metadata stays unchanged'
