from types import SimpleNamespace
import pygame
from game.render import Renderer, INK
from game.session import Session
from test_progress import Memory


def test_menu_controls_have_opaque_backing_over_bright_stage(monkeypatch):
    monkeypatch.setattr(pygame.display, "flip", lambda: None)
    pygame.font.init()
    renderer = Renderer(pygame.Surface((960, 540)))
    class BrightStage:
        def image(self, *args):
            surface = pygame.Surface((960, 540))
            surface.fill((255, 240, 190))
            return surface
    renderer.art = BrightStage()
    session = Session(Memory())
    session.enter_screen('options')
    renderer.draw(session, SimpleNamespace(error='', muted=False))
    assert tuple(renderer.screen.get_at((230, 477)))[:3] == INK
