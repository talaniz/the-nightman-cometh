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
