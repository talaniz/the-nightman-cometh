"""Real SDL decoding/channel checks; supplemental to actual browser execution."""
import json
from pathlib import Path
import pytest
import pygame
from tools.audio.audition_app.backend import Mixer

ROOT=Path(__file__).resolve().parents[2]/'assets/audio/production'

@pytest.fixture
def mixer(monkeypatch):
    monkeypatch.setenv('SDL_AUDIODRIVER','dummy')
    pygame.mixer.quit()
    m=Mixer(json.loads((ROOT/'manifest.json').read_text()),ROOT)
    yield m
    pygame.mixer.quit()


def test_all_production_ogg_decode_to_expected_durations(mixer):
    for name,cue in mixer.manifest['cues'].items():
        assert abs(mixer._sound(name).get_length()-cue['duration'])<.002


def test_music_ramp_mute_and_four_effect_voices(mixer):
    mixer.volumes(.455,.35)
    mixer.music('dayman',True);mixer.tick(.04)
    assert mixer.state()['gains'][0]>.1
    mixer.volumes(0,0);mixer.tick(.04)
    assert mixer.state()['gains']==[0.0,0.0]
    mixer.volumes(.455,.35)
    for _ in range(4):assert mixer.effect('boss-defeat')
    assert not mixer.effect('boss-defeat')
    for name in ['troll-toll','little-boy','dayman-fast','dayman']:
        mixer.stop();mixer.music(name,True);mixer.tick(.02)
        assert sum(mixer.weights)<=1.00001
    mixer.tick(.1);assert mixer.state()['music_busy']==1
    mixer.stop();mixer.tick(.1);assert mixer.state()['music_busy']==0
