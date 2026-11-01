"""Boss safety, real collision attacks and recovery behavior."""
import pytest
from game.levels.act3 import Act3
from game.world import DT

def arena():
    w=Act3();w.player.x=3220;w.enter_boss();return w

def test_entry_has_only_nightman_and_clears_attacks():
    w=Act3();w.shots=[dict(x=1,y=1,life=1)];w.beams=[dict(x=1,y=1,life=1)]
    w.enter_boss()
    assert [t.get('kind') for t in w.targets]==['nightman']
    assert not w.shots and not w.beams

def test_summons_capped_and_safe():
    w=arena()
    assert w.summon()
    assert w.summon()
    assert not w.summon()
    g=[t for t in w.targets if t.get('summoned') and t['alive']]
    assert len(g)==2 and all(abs(t['x']-w.player.x)>=96 for t in g)
    for t in g:assert any(x<=t['x'] and t['x']+30<=x+width and y==t['y']+32 for x,y,width,h in w.platforms)

def test_retry_removes_summons_and_transformation():
    w=arena();w.summon();w.meal();w.retry()
    assert not any(t.get('summoned') for t in w.targets) and not w.player.dayman

@pytest.mark.parametrize('attack',['bat','stomp','beam'])
def test_attacks_hit_nightman_once(attack):
    w=arena();b=w.targets[0];b.update(x=3380.,timer=10)
    p=w.player
    if attack=='bat':p.x=3340;p.y=386;p.facing=1;p.swing=.14
    elif attack=='stomp':p.x=3380;p.y=b['y']-44;p.vy=100;p.grounded=False
    else:w.beams=[dict(x=3370.,y=b['y']+10,dx=600.,dy=0,life=1)]
    w.step({});assert b['hp']==5
    assert not w.hit_target(b,'bat-hit') and b['hp']==5
    if attack=='stomp':assert p.vy<0

def test_victory_cleans_summons_and_paused_state_frozen():
    w=arena();w.summon();w.paused=True;before=w.snapshot();w.advance(1,{});assert w.snapshot()==before
    w.paused=False;b=w.targets[0]
    for _ in range(6):b['immune']=0;w.hit_target(b,'bat-hit')
    assert w.complete and not any(t['alive'] for t in w.targets)

def test_no_supported_spawn_position_defers():
    w=arena();w.platforms=()
    assert not w.summon()

def test_boss_warning_recovery_and_summon_spacing():
    w=arena();w.player.x=3170;seen=set();transitions=[];previous=''
    # Observe actual AI; stay away from it via ordinary movement/jumps.
    for tick in range(600):
        b=w.targets[0];state=b['state'];seen.add(state)
        if state!=previous:transitions.append((tick,state,b['timer']));previous=state
        w.step({'jump':w.player.grounded,'bat':tick%16==0})
        if w.dead:break
    assert {'windup','dash','recover','leap','summon'}<=seen
    for tick,state,timer in transitions:
        if state in ('windup','recover','summon'):assert timer>=.58

@pytest.mark.parametrize('attack',['bat','stomp','beam'])
def test_each_attack_kills_a_summoned_ghoul(attack):
    w=arena();w.summon();g=w.targets[-1];g['x']=3380.;w.targets=[g];p=w.player
    if attack=='bat':p.x=3340;p.y=386;p.facing=1;p.swing=.14
    elif attack=='stomp':p.x=3380;p.y=354;p.vy=100;p.grounded=False
    else:w.beams=[dict(x=3370.,y=410.,dx=600.,dy=0,life=1)]
    w.step({});assert not g['alive']
    if attack=='stomp':assert p.vy<0
