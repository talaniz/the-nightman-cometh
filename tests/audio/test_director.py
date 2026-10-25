import pytest
from tools.audio.audition_app.director import Director

class Backend:
    def __init__(self):self.current=None;self.starts=0;self.active=[];self.gains=(1,1);self.failed=False
    def music(self,name,loop):
        if self.failed:raise RuntimeError('asset unavailable')
        self.current=name;self.starts+=1
    def tick(self,dt):pass
    def stop(self):self.current=None;self.active=[]
    def pause(self,value):self.paused=value
    def volumes(self,music,sfx):self.gains=(music,sfx)
    def effect(self,name):
        if len(self.active)>=4:return False
        self.active.append(name);return True

@pytest.fixture
def rig():
    m={'scenes':{'title':'dayman','level1':'little-boy','bridge':'troll-toll','frank-kidnap':'sting','ending':None},
       'cues':{k:{'loop':k!='sting','duration':2} for k in ['dayman','little-boy','troll-toll','sting','dayman-fast']},
       'next':{'frank-kidnap':'bridge'},'effects':['beam'],'mix':{'music_gain_cap':.65,'sfx_gain_cap':.5,'sfx_voices':4}}
    b=Backend();return Director(m,b),b

def test_unlock_is_idempotent_and_restores_current_scene_after_transform(rig):
    d,b=rig;d.unlock();d.unlock();assert b.starts==1
    d.set_scene('level1');d.transform();assert b.current=='dayman-fast'
    d.set_scene('bridge');d.tick(10);assert b.current=='troll-toll'

def test_pause_freezes_override_and_suppresses_effects(rig):
    d,b=rig;d.unlock();d.transform();d.pause(True);d.tick(20)
    assert d.remaining==10 and not d.effect('beam')
    d.pause(False);d.tick(10);assert b.current=='dayman'

def test_muting_volumes_and_voice_limit(rig):
    d,b=rig;d.unlock();d.volumes(music=0,sfx=0);assert b.gains==(0,0)
    d.volumes(music=1,sfx=1);assert b.gains==(.65,.5)
    d.volumes(muted=True);assert b.gains==(0,0)
    d.volumes(muted=False)
    assert [d.effect('beam') for _ in range(5)]==[True,True,True,True,False]

def test_failure_keeps_navigation_and_retry_working(rig):
    d,b=rig;b.failed=True;assert d.unlock() is False;assert d.error
    d.set_scene('bridge');b.failed=False;d.retry();assert not d.error and b.current=='troll-toll'

def test_sting_advances_but_skip_and_retry_clear_transients(rig):
    d,b=rig;d.unlock();d.set_scene('frank-kidnap');d.tick(2)
    assert d.scene=='bridge' and b.current=='troll-toll'
    d.transform();d.retry();assert d.remaining==0 and b.current=='troll-toll'

@pytest.mark.parametrize('scene',['../secret','bogus'])
def test_invalid_scene_rejected(rig,scene):
    with pytest.raises(ValueError):rig[0].set_scene(scene)


def test_production_finale_plays_dayman_then_silent_credits():
    import json
    from pathlib import Path
    manifest = json.loads((Path(__file__).resolve().parents[2] / 'assets/audio/production/manifest.json').read_text())
    backend = Backend()
    director = Director(manifest, backend)
    director.unlock()
    director.set_scene('proposal')
    director.tick(manifest['cues']['proposal']['duration'])
    assert director.scene == 'ending'
    assert backend.current == 'dayman'
    director.set_scene('credits')
    assert backend.current is None
    director.retry()
    assert backend.current is None and not director.error
