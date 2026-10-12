import importlib.util
import math
from pathlib import Path
import array

import pytest

spec = importlib.util.spec_from_file_location("preview", Path(__file__).resolve().parents[2] / "tools/audio/preview.py")
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


def test_selection_uses_strongest_active_note_and_preserves_rests():
    events = [
        [0.2, 0.8, 69, 0.8], [0.2, 0.6, 72, 0.4],
        [1.0, 1.5, 71, 0.9], [1.0, 1.5, 40, 0.95],
    ]
    notes = preview.select_melody(events, 15)
    assert [(n["start"], n["end"], n["midi"]) for n in notes] == [(0.2, 0.8, 69), (1.0, 1.5, 71)]


def test_render_a4_has_expected_frequency_and_silent_tail():
    raw = preview.render([{"start":0.0, "end":1.0, "midi":69}], 15)
    samples = array.array("h", raw)
    assert len(samples) == 15 * 44100
    assert max(abs(v) for v in samples) < 32767
    crossings = sum(a <= 0 < b for a, b in zip(samples[:44100], samples[1:44100]))
    assert abs(crossings - 440) <= 1
    assert all(v == 0 for v in samples[44100:])


def test_chip_changes_timbre_but_not_length():
    notes = [{"start":0.1,"end":1.0,"midi":69}]
    sine = preview.render(notes, 15)
    chip = preview.render(notes, 15, "chip")
    assert chip != sine and len(chip) == len(sine)


@pytest.mark.parametrize("notes,duration,style", [
    ([],15,"sine"),
    ([{"start":0,"end":1,"midi":69}],14,"sine"),
    ([{"start":0,"end":1,"midi":69}],31,"sine"),
    ([{"start":-1,"end":1,"midi":69}],15,"sine"),
    ([{"start":0,"end":16,"midi":69}],15,"sine"),
    ([{"start":0,"end":1,"midi":200}],15,"sine"),
    ([{"start":0,"end":1,"midi":69}],15,"noise"),
    ([{"start":0,"end":math.nan,"midi":69}],15,"sine"),
    ([{"start":0,"end":1,"midi":69}, {"start":0.5,"end":2,"midi":71}],15,"sine"),
])
def test_render_rejects_invalid_score(notes, duration, style):
    with pytest.raises(ValueError):
        preview.render(notes,duration,style)


@pytest.mark.parametrize("events", [
    [[0, 1, 69, float("nan")]],
    [[-1, 1, 69, 0.5]],
    [[0, 16, 69, 0.5]],
    [[0, 1, True, 0.5]],
    [[0, 1, 69, 2]],
    [[0, 1, 69]],
])
def test_selection_rejects_invalid_event_data(events):
    with pytest.raises(ValueError):
        preview.select_melody(events,15)


def test_cli_output_is_valid_and_never_overwrites(tmp_path):
    import json
    import subprocess
    import sys
    import wave
    score = tmp_path / "score.json"
    output = tmp_path / "preview.wav"
    score.write_text(json.dumps({"duration_seconds":15, "notes":[{"start":0.1,"end":0.5,"midi":69}]}))
    command = [sys.executable, str(Path(preview.__file__)), str(score), str(output)]
    first = subprocess.run(command, capture_output=True, text=True)
    assert first.returncode == 0 and json.loads(first.stdout)["approval"] == "pending"
    original = output.read_bytes()
    with wave.open(str(output)) as reader:
        assert reader.getnframes() == 15 * 44100 and reader.getnchannels() == 1
    again = subprocess.run(command, capture_output=True, text=True)
    assert again.returncode == 1 and output.read_bytes() == original
    score.write_text("not JSON")
    failure = subprocess.run(command[:-1] + [str(tmp_path / "bad.wav")], capture_output=True, text=True)
    assert failure.returncode == 1 and json.loads(failure.stdout)["ok"] is False
    assert not (tmp_path / "bad.wav").exists()

def test_huge_json_integer_is_a_validation_error():
    with pytest.raises(ValueError):
        preview.render([{"start":0, "end":1, "midi":69}], 10**400)
