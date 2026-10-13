"""Musical timing, bounded inputs and preservation of the frozen palette."""
import numpy as np
import pytest
from tools.audio.arrangement import compile_score, render_score
from tools.audio.approved import render_ensemble
from tools.audio.preview import RATE


def fixture():
    return {"schema": "ensemble-beats-v1", "bpm": 120, "beats": 4,
            "parts": [[{"start": 0, "end": 2, "midi": 69}], [], []]}


def test_beat_timing_and_frozen_palette():
    score = fixture()
    duration, parts = compile_score(score)
    assert duration == 2
    assert parts[0] == [{"start": 0, "end": 1, "midi": 69}]
    assert render_score(score) == render_ensemble(parts, duration)


def test_tempo_changes_timing_without_transposing():
    score = fixture()
    for bpm in (120, 180):
        score['bpm'] = bpm
        pcm = np.frombuffer(render_score(score), dtype='<i2')
        assert len(pcm) == round(4 * 60 / bpm * RATE)
        tone = pcm[1000:20000]
        dominant = np.argmax(abs(np.fft.rfft(tone))) * RATE / len(tone)
        assert abs(dominant - 440) < 3
        assert pcm[0] == pcm[-1] == 0
        assert 0 < np.max(abs(pcm.astype(np.int32))) < 32767


@pytest.mark.parametrize('field,value', [
    ('schema', 'unknown'), ('bpm', True), ('bpm', float('nan')),
    ('bpm', 0), ('bpm', 241), ('beats', 0), ('beats', 129),
    ('parts', [[], [], []]), ('parts', 'bad'), ('parts', [[], []]),
])
def test_invalid_score_rejected(field, value):
    score = fixture()
    score[field] = value
    with pytest.raises(ValueError):
        render_score(score)


@pytest.mark.parametrize('change', [
    {'start': -1}, {'end': 5}, {'end': .001}, {'midi': True},
    {'midi': 128}, {'end': float('inf')},
])
def test_invalid_notes_rejected(change):
    score = fixture()
    score['parts'][0][0].update(change)
    with pytest.raises(ValueError):
        render_score(score)


def test_event_count_time_order_and_duration_limits():
    score = fixture()
    score['parts'][0] *= 1001
    with pytest.raises(ValueError):
        render_score(score)
    score = fixture()
    score['parts'][0] = [{'start': 1, 'end': 2, 'midi': 60},
                         {'start': 0, 'end': 1, 'midi': 60}]
    with pytest.raises(ValueError):
        render_score(score)
    score = fixture()
    score.update(bpm=40, beats=128)
    with pytest.raises(ValueError):
        render_score(score)


def test_noise_snap_at_cue_end_has_safe_zero_endpoint():
    score = fixture()
    score['beats'] = 1
    score['parts'] = [[], [], [{'start': .96, 'end': 1, 'midi': 60}]]
    pcm = np.frombuffer(render_score(score), dtype='<i2')
    assert np.max(abs(pcm.astype(np.int32))) > 0
    assert pcm[-1] == 0
