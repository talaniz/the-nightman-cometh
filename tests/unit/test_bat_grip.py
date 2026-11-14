"""The visible handle must follow the hand, including mirrored running poses."""
from types import SimpleNamespace
import pygame
import pytest
from game.render import Renderer

class MarkerArt:
    def image(self,*args):
        return pygame.Surface((40,64),pygame.SRCALPHA)
    def asset(self,*args,**kwargs):
        bat=pygame.Surface((43,13),pygame.SRCALPHA)
        pygame.draw.rect(bat,(0,255,0),(5,5,5,5))
        return bat

@pytest.mark.parametrize('facing',[1,-1])
@pytest.mark.parametrize('grounded',[False,True])
@pytest.mark.parametrize('dayman',[False,True])
def test_idle_and_jump_handle_tracks_the_visible_hand(facing,grounded,dayman):
    screen=pygame.Surface((300,200),pygame.SRCALPHA)
    renderer=Renderer.__new__(Renderer);renderer.screen=screen;renderer.art=MarkerArt()
    p=SimpleNamespace(x=100,y=100,swing=0,moving=False,grounded=grounded,dayman=dayman,invulnerable=0,facing=facing)
    renderer.actor(p,0,0)
    # Hand locations in the trimmed/scaled cast art, relative to player origin.
    hx,hy=(27,22) if grounded else (28,-4)
    if facing<0:hx=24-hx
    assert screen.get_at((100+hx,100+hy)).g==255,'bat grip detached from hand'

@pytest.mark.parametrize('facing',[1,-1])
@pytest.mark.parametrize('dayman',[False,True])
def test_jump_bat_barrel_is_raised_above_anchored_hand(facing,dayman):
    class TipArt(MarkerArt):
        def asset(self,*args,**kwargs):
            bat=super().asset(*args,**kwargs)
            pygame.draw.rect(bat,(255,0,0),(35,5,5,5))
            return bat
    renderer=Renderer.__new__(Renderer)
    renderer.screen=pygame.Surface((300,200),pygame.SRCALPHA);renderer.art=TipArt()
    p=SimpleNamespace(x=100,y=100,swing=0,moving=True,grounded=False,dayman=dayman,invulnerable=0,facing=facing)
    renderer.actor(p,0,0)
    tip=[(x,y) for x in range(60,160) for y in range(50,120) if renderer.screen.get_at((x,y)).r==255]
    assert tip and max(y for x,y in tip)<86,'jump bat should point up, not remain horizontal'
