"""Small audio state machine shared by desktop and browser audition."""
import math


class Director:
    def __init__(self, manifest, backend):
        self.manifest = manifest
        self.backend = backend
        self.scene = 'title'
        self.remaining = 0
        self.paused = False
        self.unlocked = False
        self.error = ''
        self.elapsed = 0
        self.music_volume = .7
        self.sfx_volume = .7
        self.muted = False
        self.playing = None

    def _play(self):
        if not self.unlocked:
            return False
        cue = 'dayman-fast' if self.remaining > 0 else self.manifest['scenes'][self.scene]
        try:
            self.backend.stop()
            if cue is not None:
                self.backend.music(cue, self.manifest['cues'][cue]['loop'])
            self.playing = cue
            self.volumes()
            self.backend.pause(self.paused)
            self.error = ''
            return True
        except (OSError, RuntimeError) as exc:
            self.playing = None
            self.error = 'Audio unavailable. Press R to retry. ' + str(exc)
            return False

    def unlock(self):
        if self.unlocked:
            return not self.error
        self.unlocked = True
        return self._play()

    def set_scene(self, scene):
        if not isinstance(scene, str) or scene not in self.manifest['scenes']:
            raise ValueError('unknown scene')
        self.scene = scene
        self.elapsed = 0
        # Update the baseline even during transformation; expiry uses this scene.
        if not self.remaining:
            self._play()

    def transform(self):
        if not self.unlocked or self.paused:
            return
        self.remaining = 10
        self._play()

    def tick(self, dt):
        if type(dt) not in (int, float) or not math.isfinite(dt) or dt < 0:
            raise ValueError('invalid elapsed time')
        if self.paused or not self.unlocked:
            return
        self.backend.tick(dt)
        if self.error:
            return
        if self.remaining:
            self.remaining = max(0, self.remaining - dt)
            if not self.remaining:
                self.elapsed = 0
                self._play()
            return
        self.elapsed += dt
        cue = self.manifest['scenes'][self.scene]
        if cue and not self.manifest['cues'][cue]['loop']:
            if self.elapsed >= self.manifest['cues'][cue]['duration']:
                destination = self.manifest.get('next', {}).get(self.scene)
                if destination:
                    self.set_scene(destination)

    def pause(self, value):
        self.paused = bool(value)
        self.backend.pause(self.paused)

    def volumes(self, music=None, sfx=None, muted=None):
        for value in (music, sfx):
            if value is not None and (type(value) not in (int,float) or not math.isfinite(value) or not 0 <= value <= 1):
                raise ValueError('volume must be between zero and one')
        if music is not None:
            self.music_volume = music
        if sfx is not None:
            self.sfx_volume = sfx
        if muted is not None:
            self.muted = bool(muted)
        mix = self.manifest['mix']
        self.backend.volumes(0 if self.muted else self.music_volume * mix['music_gain_cap'],
                             0 if self.muted else self.sfx_volume * mix['sfx_gain_cap'])

    def effect(self, name):
        if name not in self.manifest['effects']:
            raise ValueError('unknown effect')
        if not self.unlocked or self.paused or self.error or self.muted or self.sfx_volume == 0:
            return False
        try:
            return self.backend.effect(name)
        except (OSError, RuntimeError) as exc:
            self.error = 'Effect unavailable. Press R to retry. ' + str(exc)
            return False

    def retry(self):
        self.remaining = 0
        self.elapsed = 0
        self.paused = False
        self.unlocked = True
        self._play()
