"""The enlarged rat's visible body remains a fair stomp target."""
import pytest
from game.world import World


def rat_encounter():
    world=World();world.launcher=False;world.pickups=[]
    world.targets=[dict(id=42,kind='rat',x=300.,y=398.,alive=True)]
    return world,world.targets[0]


@pytest.mark.parametrize('speed',[100,200,350])
def test_clean_descent_onto_rat_bounces_without_damage(speed):
    world,rat=rat_encounter();p=world.player
    p.x=300;p.y=354;p.vy=speed;p.grounded=False
    for _ in range(12):
        world.step({})
        if 'stomp' in world.events or 'hurt' in world.events:break
    assert 'stomp' in world.events and 'hurt' not in world.events
    assert not rat['alive'] and p.hearts==3 and p.vy<0
    assert p.y+44==world.target_rect(rat)[1]


@pytest.mark.parametrize('x,y,vy',[(280,386,0),(325,386,0),(300,366,-100)])
def test_side_or_ascending_contact_still_hurts(x,y,vy):
    world,rat=rat_encounter();p=world.player
    p.x=x;p.y=y;p.vy=vy;p.grounded=False
    world.step({})
    assert 'hurt' in world.events and 'stomp' not in world.events
    assert rat['alive'] and p.hearts==2
