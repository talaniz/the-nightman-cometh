import json
from pathlib import Path
import numpy as np
import pytest
from tools.audio.production import render_score, synth_effect
from tools.audio.approved import render_score as approved
from tools.audio.preview import RATE

ROOT = Path(__file__).resolve().parents[2]

@pytest.mark.parametrize('name,preview',[('proposal','proposal-v1'),('dayman','dayman-v2')])
def test_long_phrase_and_approved_prefix_preserved(name,preview):
    score = json.loads((ROOT/f'assets/audio/sources/{name}-full.json').read_text())
    pcm = render_score(score)
    assert len(pcm) == round(score['duration_seconds'] * RATE) * 2
    crop = json.loads((ROOT/f'assets/audio/previews/{preview}.json').read_text())
    # The original crop has tail padding; preserve the actual approved notes.
    frames = round(crop['parts'][0][-1]['end'] * RATE)
    assert pcm[:frames*2] == approved(crop)[:frames*2]


def test_speed_scales_duration_not_pitch():
    score={'profile':'lead-v1','duration_seconds':1,'parts':[[{'start':0,'end':1,'midi':69}]]}
    for speed in (1,1.1):
        samples=np.frombuffer(render_score(score,speed),dtype='<i2')
        assert len(samples)==round(RATE/speed)
        tone=samples[1000:20000]
        hz=np.argmax(abs(np.fft.rfft(tone)))*RATE/len(tone)
        assert abs(hz-440)<3
        assert samples[0]==samples[-1]==0


@pytest.mark.parametrize('speed',[0,True,float('inf'),3])
def test_invalid_speed_rejected(speed):
    with pytest.raises(ValueError):render_score({},speed)


def test_effect_has_defined_duration_safe_levels_and_edges():
    recipe={'duration':.15,'start_hz':220,'end_hz':880,'noise':.1,'seed':1}
    samples=np.frombuffer(synth_effect(recipe),dtype='<i2')
    assert len(samples)==round(.15*RATE)
    assert samples[0]==samples[-1]==0
    assert 0<max(abs(samples.astype(np.int32)))<=6554
    assert synth_effect(recipe)==synth_effect(recipe)


def test_ensemble_boundary_snap_ends_at_zero():
    score={'profile':'ensemble-v2','duration_seconds':.5,
           'parts':[[],[],[{'start':.48,'end':.5,'midi':60}]]}
    samples=np.frombuffer(render_score(score),dtype='<i2')
    assert samples[-1]==0


@pytest.mark.parametrize('score',[
    {'profile':[], 'duration_seconds':1,'parts':[]},
    {'profile':'lead-v1','duration_seconds':121,'parts':[[{'start':0,'end':1,'midi':69}]]},
    {'profile':'lead-v1','duration_seconds':1,'parts':[[]]},
    {'profile':'lead-v1','duration_seconds':1,'parts':[[{'start':0,'end':1,'midi':True}]]},
    {'profile':'lead-v1','duration_seconds':1,'parts':[[{'start':0,'end':2,'midi':60}]]},
    {'profile':'lead-v1','duration_seconds':1,'parts':[[{'start':0,'end':1,'midi':60}]*2001]},
])
def test_production_scores_reject_unbounded_or_invalid_data(score):
    with pytest.raises(ValueError):render_score(score)


def test_credits_master_preserves_user_approved_bytes_and_export_hashes():
    import hashlib
    manifest=json.loads((ROOT/'assets/audio/production/manifest.json').read_text())
    cue=manifest['cues']['sunny-credits']
    expected='3ae10eb062973dbd4fb25ca535d3a0ce9fbc873080274e507f6b187e9b3d3259'
    assert hashlib.sha256((ROOT/'assets/audio/sources/sunny-credits-approved.wav').read_bytes()).hexdigest()==expected
    assert hashlib.sha256((ROOT/'assets/audio/production'/cue['master']).read_bytes()).hexdigest()==expected==cue['master_sha256']
    assert hashlib.sha256((ROOT/'assets/audio/production'/cue['file']).read_bytes()).hexdigest()==cue['sha256']
    assert cue['duration']==61 and cue['loop'] is False
