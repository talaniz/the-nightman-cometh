"""pygame mixer adapter: two crossfading music channels, four effect channels."""
from pathlib import Path
import pygame


class Mixer:
    def __init__(self, manifest, root):
        self.manifest = manifest
        self.root = Path(root)
        self.ready = False
        self.sounds = {}
        self.music_index = 0
        self.music_gain = 0
        self.sfx_gain = 0
        self.fail_next = False
        self.weights = [0.0, 0.0]
        self.origins = [0.0, 0.0]
        self.targets = [0.0, 0.0]
        self.fade_elapsed = 0

    def _ready(self):
        if self.ready and pygame.mixer.get_init():
            return
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(44100, -16, 2, 1024)
            pygame.mixer.set_num_channels(6)
            self.ready = True
        except pygame.error as exc:
            raise RuntimeError('Sound device could not start') from exc

    def _sound(self, name):
        self._ready()
        if self.fail_next:
            self.fail_next = False
            filename = self.root / 'missing-audition-fixture.ogg'
        else:
            filename = self.root / self.manifest['cues'][name]['file']
        try:
            if filename not in self.sounds:
                self.sounds[filename] = pygame.mixer.Sound(str(filename))
            return self.sounds[filename]
        except (pygame.error, OSError) as exc:
            raise RuntimeError('Sound file could not load') from exc

    def music(self, name, loop):
        sound = self._sound(name)
        self.music_index = 1 - self.music_index
        channel = pygame.mixer.Channel(self.music_index)
        channel.set_volume(0)
        channel.play(sound, loops=-1 if loop else 0)
        self.weights[self.music_index] = 0
        self.origins = self.weights[:]
        self.targets = [0.0, 0.0]
        self.targets[self.music_index] = 1.0
        self.fade_elapsed = 0

    def stop(self):
        if self.ready:
            self.origins = self.weights[:]
            self.targets = [0.0, 0.0]
            self.fade_elapsed = 0
            for i in range(2, 6):
                pygame.mixer.Channel(i).stop()

    def tick(self, dt):
        if not self.ready:
            return
        # Control channel gains explicitly: SDL fade-in restores its original
        # gain, which was observed to undo a subsequent volume/mute update.
        self.fade_elapsed = min(.08, self.fade_elapsed + dt)
        fraction = self.fade_elapsed / .08
        self.weights = [a + (b-a)*fraction for a,b in zip(self.origins,self.targets)]
        for i, weight in enumerate(self.weights):
            channel = pygame.mixer.Channel(i)
            channel.set_volume(weight * self.music_gain)
            if fraction == 1 and self.targets[i] == 0:
                channel.stop()

    def pause(self, value):
        if self.ready:
            for i in range(6):
                channel = pygame.mixer.Channel(i)
                channel.pause() if value else channel.unpause()

    def volumes(self, music, sfx):
        self.music_gain, self.sfx_gain = music, sfx
        if self.ready:
            for i in range(6):
                pygame.mixer.Channel(i).set_volume(music*self.weights[i] if i < 2 else sfx)

    def effect(self, name):
        sound = self._sound(name)
        for i in range(2, 6):
            channel = pygame.mixer.Channel(i)
            if not channel.get_busy():
                channel.set_volume(self.sfx_gain)
                channel.play(sound)
                return True
        return False

    def state(self):
        if not self.ready:
            return {'music_busy':0, 'sfx_busy':0, 'gains':[0,0]}
        return {'music_busy':sum(pygame.mixer.Channel(i).get_busy() for i in range(2)),
                'sfx_busy':sum(pygame.mixer.Channel(i).get_busy() for i in range(2,6)),
                'gains':[pygame.mixer.Channel(self.music_index).get_volume(),pygame.mixer.Channel(2).get_volume()]}
