"""Desktop-only storage and SDL controller boundaries."""
import os
from pathlib import Path
import sys
import tempfile


def save_path():
    if sys.platform == 'darwin':
        root = Path.home() / 'Library' / 'Application Support'
    elif sys.platform == 'win32':
        root = Path(os.environ.get('LOCALAPPDATA') or Path.home() / 'AppData' / 'Local')
    else:
        configured = Path(os.environ.get('XDG_DATA_HOME', ''))
        root = configured if configured.is_absolute() else Path.home() / '.local' / 'share'
    return root / 'NightmanCometh' / 'progress.json'


class FileStorage:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else save_path()

    def read(self):
        try:
            with self.path.open(encoding='utf-8') as handle:
                raw = handle.read(16385)
        except FileNotFoundError:
            return None
        if len(raw) > 16384:
            raise ValueError('Save exceeds size limit')
        return raw

    def write(self, value):
        if not isinstance(value, str) or len(value) > 16384:
            raise ValueError('Invalid save size')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                             dir=self.path.parent, delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(value)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


class NativePad:
    """SDL mapped controllers only; no guesses for unknown raw USB layouts."""
    def __init__(self):
        from pygame._sdl2 import controller
        self.api = controller
        self.device = None
        self.available = False
        try:
            controller.init()
            self.available = True
        except Exception:
            pass

    def read(self, focused=True):
        empty = lambda status: {'status': status, 'focused': focused}
        if not self.available:
            return empty('unavailable')
        try:
            if self.device is not None and not self.device.attached():
                self.device.quit()
                self.device = None
                return empty('absent')
            if self.device is None:
                count = min(16, self.api.get_count())
                for index in range(count):
                    if self.api.is_controller(index):
                        self.device = self.api.Controller(index)
                        break
                if self.device is None:
                    return empty('unsupported' if count else 'absent')
            # SDL standard buttons -> Web Gamepad standard slots, shared by Controls.
            mapping = {0: 0, 1: 1, 2: 2, 3: 3, 9: 4, 10: 5, 4: 8,
                       6: 9, 7: 10, 8: 11, 11: 12, 12: 13, 13: 14, 14: 15, 5: 16}
            buttons = [False] * 17
            for source, target in mapping.items():
                buttons[target] = bool(self.device.get_button(source))
            axes = []
            for index in (0, 1):
                value = self.device.get_axis(index)
                axes.append(max(-1.0, min(1.0, value / (32768 if value < 0 else 32767))))
            return {'status': 'connected', 'slot': 0, 'axes': axes,
                    'buttons': buttons, 'focused': focused}
        except Exception:
            if self.device is not None:
                try:
                    self.device.quit()
                except Exception:
                    pass
            self.device = None
            return empty('unavailable')
