import pytest
from game.session import Session
from game.levels.act1 import Act1
from game.levels.act2 import Act2
from game.levels.act3 import Act3
from game.scenes.opening import FRANK,NIGHTMAN
from game.scenes.finale import FINALE
from test_progress import Memory

@pytest.mark.parametrize('level,story',[(Act1,FRANK),(Act2,NIGHTMAN),(Act3,FINALE)])
def test_final_hit_holds_boss_then_transitions_once_and_pause_freezes(level,story):
    store=Memory();s=Session(store);s.world=level();s.world.enter_boss();s.enter_screen('training')
    boss=s.world.targets[0];boss['hp']=1;boss['state']='stunned';boss['immune']=0
    assert s.world.hit_target(boss,'bat-hit')
    s.update(.1,{})
    assert s.screen=='training','final hit must show boss defeat before the story'
    assert s.world.complete and not boss['alive']
    pos=(s.world.player.x,s.world.player.y);hp=s.world.player.hearts
    for _ in range(10):s.update(.1,{'right':True,'jump':True,'bat':True})
    assert (s.world.player.x,s.world.player.y)==pos and s.world.player.hearts==hp
    s.blur();assert s.screen=='pause'
    for _ in range(100):s.update(.1,{})
    s.activate();assert s.screen=='training'
    for _ in range(18):s.update(.1,{})
    assert s.screen=='training'
    s.update(.1,{})
    assert s.screen=='dialogue' and s.sequence is story
    writes=store.writes
    for _ in range(10):s.update(.1,{})
    assert s.dialogue==0 and store.writes==writes
