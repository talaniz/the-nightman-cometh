"""Regression for a browser font whose em-dash ink overlaps the previous word."""
import pygame
from game.render import Renderer

class OverhangingDashFont:
    def __init__(self):self.base=pygame.font.Font(None,25)
    def size(self,text):return self.base.size(text)
    def get_height(self):return self.base.get_height()
    def render(self,text,aa,color):
        image=self.base.render(text,aa,color)
        if '—' in text:
            prefix=text.split('—')[0]
            x=self.base.size(prefix)[0]
            pygame.draw.line(image,color,(max(0,x-20),4),(x+4,4),2)
        return image

def test_dialogue_dash_does_not_overpaint_preceding_word():
    pygame.font.init()
    screen=pygame.Surface((960,540));renderer=Renderer(screen)
    renderer.font=OverhangingDashFont()
    text='Dee—er—Waitress! Stop getting kidnapped, you bird!'
    expected=renderer.font.render('Dee',False,(15,18,32))
    image=renderer.dialogue_image(text)
    prefix=image.subsurface((0,0,expected.get_width(),expected.get_height()))
    assert pygame.mask.from_surface(prefix).to_surface().get_buffer().raw==pygame.mask.from_surface(expected).to_surface().get_buffer().raw
    assert image.get_width()>renderer.font.size(text)[0]

    assert image.get_width()==renderer.dialogue_width(text)
    # A clear gap separates the word from punctuation, independent of glyph ink.
    mask=pygame.mask.from_surface(image)
    assert all(not mask.get_at((expected.get_width()+dx,y)) for dx in range(3) for y in range(image.get_height()))
