from game.input.controls import Controls


def pad(*buttons, x=0, y=0, slot=0, status='connected'):
    return {'status': status, 'slot': slot, 'axes': [x, y],
            'buttons': [i in buttons for i in range(17)]}


def ready():
    controls = Controls()
    controls.sample(pad(), 'training')
    return controls


def test_pad_move_jump_and_held_edge():
    c = ready()
    held, pressed, lost = c.sample(pad(0, x=1), 'training')
    assert held == {'right', 'jump'}
    assert pressed == {'right', 'jump'}
    assert not lost
    assert c.sample(pad(0, x=1), 'training')[1] == set()


def test_deadzone_and_opposing_sources_are_neutral():
    c = ready()
    assert not c.sample(pad(x=.2), 'training')[0]
    c.key_down('left')
    assert not c.sample(pad(x=1), 'training')[0] & {'left', 'right'}


def test_union_prevents_duplicate_confirm_and_keeps_other_source_held():
    c = ready()
    c.key_down('confirm')
    assert c.sample(pad(0), 'title')[1] == {'confirm'}
    c.key_up('confirm')
    assert c.sample(pad(0), 'title')[1] == set()
    c.sample(pad(), 'title')
    assert c.sample(pad(0), 'title')[1] == {'confirm'}


def test_disconnect_pauses_and_clears_then_reconnect_requires_release():
    c = ready()
    c.sample(pad(x=1), 'training')
    held, pressed, lost = c.sample({'status': 'absent'}, 'training')
    assert lost and not held and not pressed
    assert c.sample(pad(9, x=1), 'pause')[:2] == (set(), set())
    c.sample(pad(), 'pause')
    assert c.sample(pad(9), 'pause')[1] == {'pause'}


def test_screen_transition_and_focus_cannot_reuse_held_buttons():
    c = ready()
    c.sample(pad(0), 'title')
    c.quarantine()
    assert not c.sample(pad(0), 'dialogue')[1]
    c.sample(pad(), 'dialogue')
    assert c.sample(pad(0), 'dialogue')[1] == {'confirm'}
    assert not c.sample(pad(x=1), 'training', focused=False)[0]
    assert not c.sample(pad(x=1), 'pause', focused=True)[0]
    c.sample(pad(), 'pause')
    assert c.sample(pad(9), 'pause')[1] == {'pause'}


def test_unsupported_pad_falls_back_to_keyboard_and_reports_status():
    c = ready()
    assert c.sample(pad(status='unsupported'), 'training')[2]
    c.key_down('right')
    assert 'right' in c.sample(pad(status='unsupported'), 'training')[0]
    assert c.status == 'unsupported'


def test_quick_keyboard_tap_is_not_lost_between_frames():
    c = ready()
    c.key_down('jump'); c.key_up('jump')
    assert 'jump' in c.sample(pad(), 'training')[1]
    assert not c.sample(pad(), 'training')[1]


def test_duplicate_keyboard_hold_does_not_repeat():
    c = ready()
    c.key_down('confirm'); c.sample(pad(), 'title')
    c.key_down('confirm')
    assert not c.sample(pad(), 'title')[1]


def test_malformed_pad_data_fails_closed():
    c = ready()
    for bad in [None, [], {'status': 'connected'}, pad(x=float('nan'))]:
        c.sample(bad, 'training')
    assert not c.sample({'status': 'unavailable'}, 'training')[0]


def test_lost_or_unsupported_pad_restores_keyboard_hints():
    for status in ('absent', 'unsupported', 'unavailable'):
        c = ready()
        c.sample(pad(2), 'training')
        assert c.pad_mode
        c.sample({'status': status}, 'training')
        assert not c.pad_mode
