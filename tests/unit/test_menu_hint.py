from types import SimpleNamespace
import pygame
import pytest
from game.render import Renderer, INK
from game.session import Session
from test_progress import Memory


@pytest.mark.parametrize("screen,y", [("options",477),("credits",487)])
def test_menu_controls_have_opaque_backing_over_bright_stage(monkeypatch,screen,y):
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
    session.enter_screen(screen)
    renderer.draw(session, SimpleNamespace(error='', muted=False))
    assert tuple(renderer.screen.get_at((230, y)))[:3] == INK
