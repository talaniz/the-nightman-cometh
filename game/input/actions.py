"""Dispatch shared actions without changing world physics or authored scenes."""
from game.audio import retry_audio

PASSWORD_KEYS = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') + ('DEL', 'GO')


def perform(session, audio, controls, pressed):
    """Return one-shot gameplay actions; navigation never leaks into gameplay."""
    if 'pause' in pressed:
        if session.screen in ('training', 'pause'):
            session.back()
        return set()
    if 'back' in pressed:
        session.back()
        return set()
    if 'mute' in pressed:
        audio.volumes(muted=not audio.muted)
    if 'retry' in pressed:
        retry_audio(audio, session.world.player.dayman if audio.scene in
                    ('level1', 'cricket', 'bridge', 'frank', 'rooftop', 'nightman') else 0, audio.paused)
    if session.screen == 'training':
        return pressed & {'jump', 'bat', 'beam'}
    if session.screen == 'password' and controls.pad_mode:
        for action, delta in (('left', -1), ('right', 1), ('up', -10), ('down', 10)):
            if action in pressed:
                controls.password_index = (controls.password_index + delta) % len(PASSWORD_KEYS)
        if 'confirm' in pressed:
            key = PASSWORD_KEYS[controls.password_index]
            if key == 'GO': session.submit_password()
            elif key == 'DEL': session.password = session.password[:-1]
            elif len(session.password) < 16: session.password += key
        return set()
    if 'confirm' in pressed:
        session.activate()
        return set()
    if 'up' in pressed: session.select(-1)
    elif 'down' in pressed: session.select(1)
    if 'left' in pressed: session.adjust(-1)
    elif 'right' in pressed: session.adjust(1)
    return set()
