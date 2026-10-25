import wave
import pytest
from tools.check_audio import inspect_wav, AudioValidationError

def test_production_duration_window_accepts_short_effect_but_default_rejects(tmp_path):
    path=tmp_path/'short.wav'
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,44100,0,'NONE','not compressed'))
        w.writeframes(b'\x01\x01'*4410)
    with pytest.raises(AudioValidationError):inspect_wav(path)
    assert inspect_wav(path,min_duration=.02,max_duration=120)['duration_seconds']==.1
