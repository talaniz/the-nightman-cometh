"""M5 progression contracts: ordinary input, existing save compatibility and exact story."""
import json
import pytest
from game.session import Session
from game.scenes.opening import FRANK
from test_progress import Memory

LINE='Dee—er—Waitress! Stop getting kidnapped, you bird!'

def test_added_frank_escape_still():
    assert len(FRANK)==4
    assert FRANK[-1].speaker=='DENNIS' and FRANK[-1].text==LINE
    assert FRANK[-1].atlas=='bridge-story'

def test_frank_sequence_enters_act2_once():
    s=Session(Memory());s.start();s.next_dialogue(skip=True)
    s.world.complete=True;s.update(0,{})
    assert s.sequence is FRANK
    s.next_dialogue(skip=True)
    assert s.world.act=='act2' and s.screen=='training'
    world=s.world;s.update(0,{})
    assert s.world is world

def test_troll_password_uses_real_bridge_and_preserves_save():
    store=Memory();s=Session(store);s.start();saved=store.raw
    s.password='TROLLTOLL';s.submit_password()
    assert s.world.act=='act2' and s.qa
    assert store.raw==saved

def test_completed_act1_save_continues_toward_bridge():
    store=Memory();s=Session(store);s.start();s.world.complete=True;s.progress.save(s.world)
    resumed=Session(store);resumed.selection=resumed.menu().index('Continue Act 1');resumed.activate()
    assert resumed.screen=='dialogue' and resumed.sequence is FRANK
    resumed.next_dialogue(skip=True)
    assert resumed.world.act=='act2'

from game.levels.act2 import Act2
from game.world import DT

def test_bridge_crew_and_walk_gun_telegraph_before_fire():
    w=Act2();assert {'duncan','z','gun'}<=set(t.get('kind') for t in w.targets)
    gun=next(t for t in w.targets if t['kind']=='gun')
    w.player.x=gun['x']-180;seen=set()
    for _ in range(180):
        w.step({});seen.add(gun['state'])
        if w.shots:break
    assert 'windup' in seen and w.shots
    assert w.shots[0]['dx']<0

def test_act2_save_roundtrip_and_invalid_checkpoint():
    store=Memory();s=Session(store);w=Act2();w.flag('mid',1500);s.progress.save(w)
    resumed=Session(store)
    assert resumed.world.act=='act2' and resumed.world.checkpoint==1500
    bad=json.loads(store.raw);bad['checkpoint']=3350;store.raw=json.dumps(bad)
    assert Session(store).progress.saved is None

def test_bridge_flags_are_one_shot_and_retry_clears_dayman():
    w=Act2();w.player.hearts=1;w.flag('mid',1500);assert w.player.hearts==2
    w.player.hearts=1;w.flag('mid',1500);assert w.player.hearts==1
    w.meal();w.retry();assert w.player.hearts==3 and w.player.dayman==0
    assert w.checkpoint==1500 and w.flags=={'mid'}

def test_directional_projectile_preserves_release_height():
    w=Act2();w.targets=[];w.shots=[dict(x=700.,y=410.,dx=180.,life=2.)]
    w.step({})
    assert w.shots[0]['x']>700 and w.shots[0]['y']==410

from game.scenes.opening import NIGHTMAN

def test_abduction_play_skip_and_completed_reload_agree():
    for skip in (True,False):
        store=Memory();s=Session(store);s.world=Act2();s.world.complete=True;s.enter_screen('training');s.update(0,{})
        assert s.sequence is NIGHTMAN
        if skip:s.next_dialogue(skip=True)
        else:
            for _ in NIGHTMAN:s.next_dialogue()
        assert s.screen=='training' and s.world.act=='act3'
        q=Session(store);q.selection=q.menu().index('Continue Act 3');q.activate()
        assert q.screen=='training' and q.world.act=='act3' and not q.world.complete

@pytest.mark.parametrize('index,x',[(3,590),(4,790),(5,1770),(6,1970)])
def test_all_bridge_raised_platforms_have_reachable_launch(index,x):
    w=Act2();w.targets=[];w.pickups=[]
    # Upper ledges launch from adjacent lower ledges; ordinary jump physics only.
    p=w.player
    if index in (4,6):
        lower=w.platforms[index-1];p.x=lower[0]+lower[2]-25;p.y=lower[1]-44
    else:p.x=x
    target=w.platforms[index]
    for tick in range(60):
        w.step({'jump':tick==0,'right':index in (4,6) and p.x<target[0]+20})
        if tick>0 and p.grounded and abs(p.y+44-target[1])<.01:break
    assert p.grounded and p.y+44==target[1]

def test_unpowered_ordinary_bridge_route_can_win():
    w=Act2();last_bat=-100
    for frame in range(16000):
        assert not w.dead,('death',w.player.x,w.checkpoint)
        if w.complete:break
        p=w.player;keys={}
        if not w.boss_active:
            keys['right']=True
            gap=any(0<edge-p.x<55 for edge in (1000,2200))
            enemy=any(t['alive'] and 0<t['x']-p.x<85 and abs(t['y']-p.y)<60 for t in w.targets)
            keys['jump']=p.grounded and (gap or enemy or 0<1560-p.x<65)
        else:
            boss=w.targets[0];dx=boss['x']-p.x
            keys.update(right=dx>53,left=dx<40)
            # Face the troll at attack range, dodge low sandwiches by jumping.
            if dx>=40 and p.facing<0:keys['right']=True
            incoming=any(t['kind']=='sandwich' and 0<t['x']-p.x<100 for t in w.targets)
            keys['jump']=p.grounded and incoming
        keys['bat']=frame-last_bat>15
        if keys['bat']:last_bat=frame
        w.advance(DT,keys)
        assert not w.beams and p.dayman==0
    assert w.complete and w.flags=={'mid','preboss'}

def test_bridge_dialogue_replay_preserves_progress_and_returns_to_pause():
    store=Memory();s=Session(store);s.world=Act2();s.progress.save(s.world);saved=store.raw
    s.enter_screen('pause');s.selection=s.menu().index('Replay dialogue');s.activate()
    assert s.sequence is FRANK
    s.next_dialogue(skip=True)
    assert s.screen=='pause' and s.world.act=='act2' and store.raw==saved

def test_paused_gun_and_frank_timers_do_not_advance():
    for boss in (False,True):
        w=Act2()
        if boss:w.enter_boss()
        w.paused=True;before=w.snapshot();w.advance(1,{'bat':True});assert w.snapshot()==before
