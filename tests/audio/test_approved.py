"""Approval preservation checks use the WAVs the user actually heard."""
import json
from pathlib import Path
import wave
import pytest
from tools.audio.approved import render_score

ROOT = Path(__file__).resolve().parents[2]
PREVIEWS = ROOT / 'assets/audio/previews'
IDS = ['dayman-v2', 'proposal-v1', 'little-boy-v1', 'troll-toll-v2']

@pytest.mark.parametrize('name', IDS)
def test_reproduces_approved_pcm(name):
    score = json.loads((PREVIEWS / (name + '.json')).read_text())
    with wave.open(str(PREVIEWS / (name + '.wav')), 'rb') as f:
        approved = f.readframes(f.getnframes())
    assert render_score(score) == approved

@pytest.mark.parametrize('change', ['profile', 'duration', 'pitch', 'end', 'empty', 'too_many', 'third_voice'])
def test_rejects_invalid_scores(change):
    score = {'profile':'lead-v1', 'duration_seconds':15,
             'parts':[[{'start':0, 'end':1, 'midi':69}]]}
    if change == 'profile': score['profile'] = '__import__'
    if change == 'duration': score['duration_seconds'] = float('inf')
    if change == 'pitch': score['parts'][0][0]['midi'] = True
    if change == 'end': score['parts'][0][0]['end'] = 16
    if change == 'empty': score['parts'] = [[]]
    if change == 'too_many': score['parts'][0] *= 1001
    if change == 'third_voice':
        score['profile'] = 'duet-v1'
        score['parts'][0] *= 3
    with pytest.raises(ValueError): render_score(score)
