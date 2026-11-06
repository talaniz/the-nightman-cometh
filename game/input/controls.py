"""Bounded keyboard/gamepad input with shared edges and release barriers."""
import math

DEADZONE = .3
BUTTONS = {0: 'primary', 1: 'back', 2: 'bat', 3: 'beam',
           4: 'mute', 5: 'retry', 9: 'pause',
           12: 'up', 13: 'down', 14: 'left', 15: 'right'}


def pad_actions(snapshot, screen):
    """Fail closed at the browser boundary; device names never enter game state."""
    if not isinstance(snapshot, dict):
        return 'unavailable', None, set()
    status = snapshot.get('status')
    if status != 'connected':
        return status if status in ('absent', 'unsupported', 'unavailable') else 'unavailable', None, set()
    axes, buttons, slot = snapshot.get('axes'), snapshot.get('buttons'), snapshot.get('slot')
    if (type(slot) is not int or not 0 <= slot < 16 or not isinstance(axes, list)
            or len(axes) != 2 or not isinstance(buttons, list) or len(buttons) != 17
            or not all(type(b) is bool for b in buttons)
            or not all(type(a) in (int, float) and math.isfinite(a) and -1 <= a <= 1 for a in axes)):
        return 'unavailable', None, set()
    actions = {action for index, action in BUTTONS.items() if buttons[index]}
    for value, negative, positive in ((axes[0], 'left', 'right'), (axes[1], 'up', 'down')):
        if value < -DEADZONE: actions.add(negative)
        if value > DEADZONE: actions.add(positive)
    if 'primary' in actions:
        actions.remove('primary')
        actions.add('jump' if screen == 'training' else 'confirm')
    return 'connected', slot, actions


class Controls:
    def __init__(self):
        self.status = 'absent'
        self.connected = False
        self.release_required = True
        self.slot = None
        self.keys = set()
        self.key_presses = set()
        self.blocked_keys = set()
        self.previous = set()
        self.focused = True
        self.password_index = 0
        self.pad_mode = False

    def key_down(self, action):
        if action not in self.keys:
            self.keys.add(action)
            if action not in self.blocked_keys:
                self.key_presses.add(action)
                self.pad_mode = False

    def key_up(self, action):
        self.keys.discard(action)
        self.blocked_keys.discard(action)

    def quarantine(self):
        """Require release after a context change; never replay a held action."""
        self.blocked_keys.update(self.keys)
        self.key_presses.clear()
        self.previous.clear()
        self.release_required = True

    def sample(self, pad, screen, focused=True):
        status, slot, actions = pad_actions(pad, screen)
        lost = self.connected and (status != 'connected' or slot != self.slot)
        changed = slot != self.slot
        if lost or changed or not focused or not self.focused:
            self.quarantine()
        self.focused = focused
        self.status, self.slot, self.connected = status, slot, status == 'connected'
        if self.release_required:
            if not actions and focused:
                self.release_required = False
            actions = set()
        if not focused or lost:
            self.key_presses.clear()
            return set(), set(), lost
        if actions:
            self.pad_mode = True
        held = actions | (self.keys - self.blocked_keys)
        for negative, positive in (('left', 'right'), ('up', 'down')):
            if negative in held and positive in held:
                held.difference_update((negative, positive))
        pressed = (held | self.key_presses) - self.previous
        # Opposing held directions must not move menu selection either.
        for action in ('left', 'right', 'up', 'down'):
            if action not in held and action in self.keys | actions:
                pressed.discard(action)
        self.key_presses.clear()
        self.previous = held
        return held, pressed, lost

    def snapshot(self):
        return {'status': self.status, 'connected': self.connected,
                'release_required': self.release_required, 'pad_mode': self.pad_mode,
                'password_index': self.password_index}
