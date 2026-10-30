"""Acceptance regressions for issue17; test real motion, not configuration values."""
import pygame
import pytest
from game.levels.act1 import Act1
from game.render import Renderer

@pytest.mark.parametrize('x', [720,2080,2860])
def test_standing_jump_lands_on_each_first_step(x):
    w=Act1(); w.targets=[]; w.player.x=x
    ledge=next(p for p in w.platforms if p[0]<=x<p[0]+p[2] and p[1]<430)
    w.step({'jump':True})
    landed=False
    for _ in range(70):
        w.step()
        if w.player.grounded and w.player.y+44==ledge[1]:landed=True
    assert landed, 'ordinary jump must reach the visible raised platform'

@pytest.mark.parametrize('kind', ['rat','ghoul'])
def test_enemy_pose_changes_without_sliding(kind):
    pygame.init();pygame.display.set_mode((960,540))
    r=Renderer(pygame.Surface((960,540)));w=Act1()
    target=next(t for t in w.targets if t['kind']==kind)
    frames=[]
    for step in (0,8,16,24):
        r.screen.fill((0,0,0));r.enemy(target,0)
        frames.append(pygame.image.tobytes(r.screen,'RGB'))
        # Enemy pose must use simulation time, independently from world translation.
        target['animation_step']=step+8
    assert len(set(frames))==4, 'four different limb poses required at a fixed world position'

@pytest.mark.parametrize('source,target', [(3,4),(4,3),(5,6),(6,5)])
def test_jump_between_adjacent_raised_platforms(source,target):
    w=Act1();w.targets=[];a=w.platforms[source];b=w.platforms[target]
    right=b[0]>a[0]
    w.player.x=a[0]+a[2]-36 if right else a[0]+12
    w.player.y=a[1]-44
    destination=b[0]+18 if right else b[0]+b[2]-42
    landed=False
    for tick in range(90):
        moving=w.player.x<destination if right else w.player.x>destination
        w.step({'jump':tick==0,'right':right and moving,'left':not right and moving})
        if w.player.grounded and w.player.y+44==b[1] and b[0]-24<w.player.x<b[0]+b[2]:landed=True
    assert landed, 'adjacent platform must be reachable with an ordinary directional jump'


def test_enemy_animation_freezes_with_pause():
    w=Act1()
    for _ in range(12):w.step()
    before=w.snapshot();w.paused=True
    for _ in range(20):w.step()
    after=w.snapshot();before['paused']=True
    assert before==after

@pytest.mark.parametrize('facing', [-1,1])
@pytest.mark.parametrize('dayman', [0,10])
def test_bat_windup_strike_recovery_are_distinct_and_pause_stable(facing,dayman):
    pygame.init();pygame.display.set_mode((960,540));r=Renderer(pygame.Surface((960,540)))
    w=Act1();p=w.player;p.x=350;p.facing=facing;p.dayman=dayman
    frames=[]
    for remaining in (.21,.12,.02):
        p.swing=remaining;r.screen.fill((0,0,0));r.actor(p,0,0)
        frame=pygame.image.tobytes(r.screen,'RGB');frames.append(frame)
        r.screen.fill((0,0,0));r.actor(p,0,0)
        assert frame==pygame.image.tobytes(r.screen,'RGB')
    assert len(set(frames))==3
