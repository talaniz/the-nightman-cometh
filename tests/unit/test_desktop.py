"""Native boundary contracts; browser storage remains separate."""
from game.main import Storage


def test_native_save_survives_new_storage_instance(tmp_path, monkeypatch):
    monkeypatch.setenv('XDG_DATA_HOME', str(tmp_path))
    first = Storage()
    first.write('{"v":2}')
    assert Storage().read() == '{"v":2}'

from game.desktop import FileStorage, NativePad
from types import SimpleNamespace
import pytest


def test_oversized_save_is_bounded(tmp_path):
    path = tmp_path / 'save.json'
    path.write_text('x' * 17000)
    with pytest.raises(ValueError):
        FileStorage(path).read()


def test_failed_atomic_replace_preserves_old_save(tmp_path, monkeypatch):
    import game.desktop as desktop
    storage = FileStorage(tmp_path / 'save.json')
    storage.write('old')
    def fail(*args):
        raise OSError('read only')
    monkeypatch.setattr(desktop.os, 'replace', fail)
    with pytest.raises(OSError):
        storage.write('new')
    assert storage.read() == 'old'
    assert len(list(tmp_path.iterdir())) == 1


def mapped_device():
    # Constrain doubles to the real pinned pygame API, including Cython methods.
    from pygame._sdl2.controller import Controller
    from unittest.mock import Mock
    device = Mock(spec_set=Controller)
    device.attached.return_value = True
    device.get_axis.side_effect = lambda index: -32768 if index == 0 else 32767
    device.get_button.side_effect = lambda index: index in (0, 6, 11)
    return device


def native_pad():
    pad = NativePad.__new__(NativePad)
    pad.device = None
    pad.available = True
    pad.api = SimpleNamespace(get_count=lambda: 1, is_controller=lambda i: True,
                              Controller=lambda i: mapped_device())
    return pad


def test_native_standard_pad_maps_to_shared_actions():
    result = native_pad().read()
    assert result['status'] == 'connected'
    assert result['axes'] == [-1, 1]
    assert len(result['buttons']) == 17
    assert result['buttons'][0] and result['buttons'][9] and result['buttons'][12]


def test_disconnect_reported_before_replacement():
    pad = native_pad()
    pad.read()
    pad.device.attached.return_value = False
    assert pad.read()['status'] == 'absent'
    assert pad.read()['status'] == 'connected'


def test_unknown_pad_is_not_guessed():
    pad = native_pad()
    pad.api.is_controller = lambda i: False
    assert pad.read()['status'] == 'unsupported'


def test_focus_carried_through_snapshot():
    assert native_pad().read(False)['focused'] is False


def test_native_snapshot_uses_shared_disconnect_release_barrier():
    from game.input.controls import Controls
    controls = Controls()
    pad = native_pad()
    connected = pad.read()
    neutral = {**connected, 'axes': [0, 0], 'buttons': [False] * 17}
    controls.sample(neutral, 'training')
    held, pressed, lost = controls.sample(connected, 'training')
    assert 'jump' in pressed and not lost
    assert controls.sample({'status': 'absent'}, 'training')[2]
    assert controls.sample(connected, 'training')[0] == set()
    controls.sample(neutral, 'training')
    assert 'jump' in controls.sample(connected, 'training')[1]


@pytest.mark.parametrize('platform,folder', [('darwin', 'Library/Application Support'), ('win32', 'Local')])
def test_platform_save_directory(tmp_path, monkeypatch, platform, folder):
    import game.desktop as desktop
    monkeypatch.setattr(desktop.sys, 'platform', platform)
    monkeypatch.setattr(desktop.Path, 'home', lambda: tmp_path)
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path / 'Local'))
    assert desktop.save_path() == tmp_path / folder / 'NightmanCometh/progress.json'


def test_native_pad_remains_connected_across_frames():
    pad = native_pad()
    assert pad.read()['status'] == 'connected'
    device = pad.device
    for _ in range(4):
        assert pad.read()['status'] == 'connected'
        assert pad.device is device
    device.quit.assert_not_called()


def test_installation_check_rejects_failed_save(tmp_path, monkeypatch):
    from tools.desktop.launch import verify_progress
    def fail(self, value):
        raise OSError('write denied')
    monkeypatch.setattr(FileStorage, 'write', fail)
    with pytest.raises(RuntimeError, match='Save'):
        verify_progress(FileStorage(tmp_path / 'progress.json'))
