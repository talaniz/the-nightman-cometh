"""Frank and projectile contracts, including direct collision-path attack matrix."""
import pytest
from game.levels.act2 import Act2
from game.world import DT

def boss():
    w=Act2();w.player.x=3100;w.enter_boss();return w

def test_arena_entry_cleans_ordinary_projectiles():
    w=Act2();w.shots=[dict(x=3000,y=410,life=2)];w.beams=[dict(x=2900,y=400,life=2)]
    w.player.x=2950;w.step({})
    assert w.boss_active and all(t['kind']=='frank' for t in w.targets)
    assert w.shots==[] and w.beams==[]

def test_frank_active_damage_has_short_immunity_and_requires_multiple_hits():
    w=boss();b=w.targets[0]
    assert w.hit_target(b,'bat-hit') and b['hp']==4 and b['alive']
    assert not w.hit_target(b,'bat-hit') and b['hp']==4

def test_frank_throws_horizontal_sandwich_after_windup():
    w=boss();seen=set()
    for _ in range(240):
        w.step({});seen.add(w.targets[0]['state'])
        if len(w.targets)>1:break
    assert 'windup' in seen
    sandwich=next(t for t in w.targets if t['kind']=='sandwich')
    y=sandwich['y'];x=sandwich['x']
    for _ in range(10):w.step({})
    assert sandwich['y']==y and sandwich['x']<x

@pytest.mark.parametrize('kind',['frank','sandwich'])
@pytest.mark.parametrize('attack',['bat','stomp','beam'])
def test_attack_matrix_uses_world_collision(kind,attack):
    w=boss();t=w.targets[0]
    if kind=='sandwich':
        t=dict(id=101,kind='sandwich',x=3200.,y=398.,alive=True,direction=-1,state='flight',timer=3.,animation_step=0)
        w.targets=[t]
    t['x']=3200;t['timer']=10
    p=w.player
    if attack=='bat':p.x=3160;p.y=386;p.facing=1;p.swing=.14
    elif attack=='stomp':p.x=3200;p.y=t['y']-44;p.vy=100;p.grounded=False
    else:w.beams=[dict(x=3190.,y=t['y']+10,dx=600.,dy=0,life=1)]
    w.step({})
    assert (t.get('hp')==4) if kind=='frank' else not t['alive']
    if attack=='stomp':assert p.vy<0

def test_unpowered_boss_victory_and_cleanup():
    w=boss();b=w.targets[0]
    for _ in range(5):
        b['immune']=0;w.hit_target(b,'stomp')
    assert w.complete and not b['alive'] and w.shots==[]
    w.retry();assert not w.complete and not w.boss_active and w.player.dayman==0
