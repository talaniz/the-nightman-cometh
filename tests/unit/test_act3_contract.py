"""Rooftop progression and checkpoint boundary contracts."""
import json
import pytest
from game.session import Session
from game.levels.act2 import Act2
from game.levels.act3 import Act3
from game.scenes.opening import NIGHTMAN
from test_progress import Memory

@pytest.mark.parametrize('skip',[False,True])
def test_abduction_enters_actual_rooftop(skip):
    s=Session(Memory());s.world=Act2();s.world.complete=True;s.enter_screen('training');s.update(0,{})
    assert s.sequence is NIGHTMAN
    if skip:s.next_dialogue(skip=True)
    else:
        for _ in NIGHTMAN:s.next_dialogue()
    assert s.world.act=='act3' and s.screen=='training'

def test_completed_act2_continue_and_rooftop_save():
    storage=Memory();s=Session(storage);w=Act2();w.complete=True;s.progress.save(w)
    s=Session(storage);s.selection=s.menu().index('Continue Act 2');s.activate()
    assert s.sequence is NIGHTMAN and s.screen=='dialogue'
    s.next_dialogue(skip=True);s.world.flag('mid',s.world.flag_positions['mid']);s.progress.save(s.world)
    resumed=Session(storage)
    assert resumed.world.act=='act3' and resumed.world.flags=={'mid'}
    bad=json.loads(storage.raw);bad['checkpoint']=1500;storage.raw=json.dumps(bad)
    assert Session(storage).progress.saved is None

def test_nightman_password_real_level_isolates_progress():
    store=Memory();s=Session(store);s.start();saved=store.raw
    s.password='NIGHTMAN';s.submit_password()
    assert s.world.act=='act3' and s.qa
    s.world.complete=True;s.update(0,{})
    assert store.raw==saved
    s.exit_qa();assert s.world.act=='act1' and not s.qa

def test_rooftop_flags_and_retry():
    w=Act3();assert w.flag_positions=={'mid':1600,'preboss':3000}
    w.player.hearts=1;w.flag('mid',1600);assert w.player.hearts==2
    w.player.hearts=1;w.flag('mid',1600);assert w.player.hearts==1
    w.meal();w.retry();assert w.player.hearts==3 and w.player.dayman==0 and w.flags=={'mid'}

@pytest.mark.parametrize('index',range(3,7))
def test_rooftop_raised_platforms_reachable(index):
    w=Act3();w.targets=[];w.pickups=[];p=w.player;target=w.platforms[index]
    if index in (4,6):
        lower=w.platforms[index-1];p.x=lower[0]+lower[2]-25;p.y=lower[1]-44
    else:p.x=target[0]+30
    for tick in range(60):
        w.step({'jump':tick==0,'right':index in (4,6) and p.x<target[0]+20})
        if tick>0 and p.grounded and p.y+44==target[1]:break
    assert p.grounded and p.y+44==target[1]

def test_leaving_gameplay_removes_summons_and_attacks():
    s=Session(Memory());s.world=Act3();s.world.enter_boss();s.world.summon()
    s.enter_screen('title')
    assert not any(t.get('summoned') and t['alive'] for t in s.world.targets)

def test_unpowered_rooftop_route_wins_without_cheats():
    w=Act3()
    for tick in range(16000):
        p=w.player
        assert not w.dead,('death',p.x,w.checkpoint)
        if w.complete:break
        keys={'bat':tick%16==0}
        if not w.boss_active:
            keys['right']=True
            keys['jump']=p.grounded and (any(0<edge-p.x<65 for edge in (1100,2350,1660)) or any(t['alive'] and 0<t['x']-p.x<90 and abs(t['y']-p.y)<65 for t in w.targets))
        else:
            b=w.targets[0];dx=b['x']-p.x
            keys.update(right=dx>42,left=dx<-42,jump=p.grounded and abs(dx)<170)
            if abs(dx)<42 and (p.facing>0)!=(dx>0):keys['right']=dx>0;keys['left']=dx<0
        w.step(keys)
        assert p.dayman==0 and not w.beams and not w.invincible
    assert w.complete and w.flags=={'mid','preboss'}

def test_v2_rehearsal_save_keeps_working_continue_label():
    store=Memory();store.raw=json.dumps(dict(v=2,stage='rehearsal',checkpoint=80,flags=[],complete=False,settings={'music':.4,'effects':.5}))
    s=Session(store)
    assert 'Continue Act 1' in s.menu()
    s.selection=s.menu().index('Continue Act 1');s.activate()
    assert s.screen=='training' and s.world.act=='act1'
