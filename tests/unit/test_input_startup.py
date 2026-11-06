import pygame
from game.main import initialize_display


def test_keyboard_startup_does_not_require_native_joystick_subsystem():
    pygame.quit()
    try:
        screen = initialize_display()
        assert screen.get_size() == (960, 540)
        assert pygame.font.get_init()
        # The browser adapter owns Gamepad access and catches denial/errors.
        # SDL's second reader must not run first and bypass that fallback.
        assert not pygame.joystick.get_init()
    finally:
        pygame.quit()
