"""Bounded attacks for the approved harder encounters."""
from game.levels.act2 import Act2
from game.levels.act3 import Act3
from game.world import DT


def test_frank_follows_whole_sandwich_with_four_ordered_ingredients():
    w=Act2();w.player.x=3000;w.enter_boss();b=w.targets[0]
    emitted=[];seen=set()
    for _ in range(300):
        b['timer']-=DT;w.update_frank(b)
        for t in w.targets[1:]:
            if t['id'] not in seen:
                seen.add(t['id']);emitted.append(t.get('ingredient','whole'))
        if b['state']=='recover':break
    assert emitted==['whole','meat','cheese','bread','lettuce']
    assert all(t['direction']==-1 for t in w.targets[1:])
    assert b['timer']>=.6


def test_bridge_crew_throw_eggs_after_warning():
    w=Act2();t=next(t for t in w.targets if t['kind']=='duncan')
    w.targets=[t];w.player.x=t['x']-160
    for _ in range(150):
        w.step({})
        if w.shots:break
    assert w.shots and w.shots[0].get('kind')=='egg'


def test_bridge_guns_shoot_alcohol_and_multiple_chickens_wait_in_approach():
    w=Act2();assert sum(t['kind']=='chicken' for t in w.targets)>=3
    t=next(t for t in w.targets if t['kind']=='gun');w.targets=[t]
    w.player.x=t['x']-200
    for _ in range(160):
        w.step({})
        if w.shots:break
    assert w.shots[0].get('kind')=='alcohol'
    assert t['state']=='recover'


def test_nightman_charges_then_fires_bounded_alternating_bursts():
    w=Act3();w.player.x=3200;w.enter_boss();b=w.targets[0]
    bursts=[];current=[];seen=set()
    for _ in range(3000):
        previous=b['state'];w.update_boss(b);seen.add(b['state'])
        current.extend(shot.get('kind') for shot in w.shots);w.shots=[]
        if previous=='fire' and b['state']=='recover':
            bursts.append(current);current=[]
            if len(bursts)==2:break
    assert 'charge' in seen and 'karate' in seen
    assert bursts==[['crucifix']*3,['chimichanga']*2]
