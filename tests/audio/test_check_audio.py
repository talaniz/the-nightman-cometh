"""Synthetic fixtures for the M1 preview contract; no copyrighted source audio."""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import wave

import pytest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "check_audio.py"
SPEC = importlib.util.spec_from_file_location("check_audio", TOOL)
audio = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audio)


def write_wav(path, *, rate=44100, seconds=15, channels=1, width=2, value=1000):
    with wave.open(str(path), "wb") as output:
        output.setparams((channels, width, rate, 0, "NONE", "not compressed"))
        sample = struct.pack("<h", value) if width == 2 else bytes([128])
        output.writeframes(sample * (int(rate * seconds) * channels))
    return path


def test_valid_report(tmp_path):
    path = write_wav(tmp_path / "preview.wav")
    report = audio.inspect_wav(path)
    assert report["frames"] == 661500
    assert report["duration_seconds"] == 15
    assert report["channels"] == 1
    assert report["sample_rate"] == 44100
    assert report["peak"] == 1000
    import hashlib
    assert report["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()


def test_stereo_48000_upper_duration(tmp_path):
    path = write_wav(tmp_path / "stereo.wav", rate=48000, seconds=30, channels=2)
    assert audio.inspect_wav(path, 48000)["frames"] == 1440000


@pytest.mark.parametrize("kwargs,reason", [
    ({"rate":48000}, "sample rate"),
    ({"seconds":14.99}, "duration"),
    ({"seconds":30.01}, "duration"),
    ({"width":1}, "PCM16"),
    ({"channels":3}, "mono or stereo"),
    ({"value":0}, "silent"),
    ({"value":32767}, "full-scale"),
    ({"value":-32768}, "full-scale"),
])
def test_invalid_audio_rejected(tmp_path, kwargs, reason):
    path = write_wav(tmp_path / "invalid.wav", **kwargs)
    with pytest.raises(audio.AudioValidationError, match=reason):
        audio.inspect_wav(path)


@pytest.mark.parametrize("kind", ["truncated", "malformed", "missing"])
def test_unreadable_audio_rejected(tmp_path, kind):
    path = tmp_path / "broken.wav"
    if kind == "truncated":
        write_wav(path)
        path.write_bytes(path.read_bytes()[:-10])
    elif kind == "malformed":
        path.write_bytes(b"not a WAV")
    with pytest.raises(audio.AudioValidationError):
        audio.inspect_wav(path)


def run_cli(*args):
    result = subprocess.run([sys.executable, str(TOOL), *map(str, args)],
                            text=True, capture_output=True)
    return result, json.loads(result.stdout)


def test_cli_valid_directory_and_mixed_failure(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    write_wav(nested / "valid.wav")
    result, report = run_cli(tmp_path)
    assert result.returncode == 0
    assert report["ok"] is True and len(report["files"]) == 1
    (tmp_path / "broken.wav").write_bytes(b"broken")
    result, report = run_cli(tmp_path)
    assert result.returncode == 1
    assert report["ok"] is False
    assert len(report["errors"]) == 1 and len(report["files"]) == 1


def test_cli_empty_missing_and_symlink(tmp_path):
    for path in [tmp_path, tmp_path / "missing"]:
        result, report = run_cli(path)
        assert result.returncode == 1 and report["errors"]
    target = write_wav(tmp_path / "valid.wav")
    link = tmp_path / "alias.wav"
    link.symlink_to(target)
    with pytest.raises(audio.AudioValidationError, match="symlink"):
        audio.inspect_wav(link)


def test_cli_does_not_follow_directory_symlinks(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    write_wav(outside / "other.wav")
    (source / "linked").symlink_to(outside, target_is_directory=True)
    result, report = run_cli(source)
    assert result.returncode == 1 and not report["files"]


def test_cli_selected_sample_rate(tmp_path):
    path = write_wav(tmp_path / "48000.wav", rate=48000)
    result, report = run_cli("--sample-rate", "48000", path)
    assert result.returncode == 0 and report["ok"]
