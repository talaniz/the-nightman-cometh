"""Check preview PCM WAV structure; this cannot establish musical acceptance."""
import argparse
import array
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import wave


class AudioValidationError(ValueError):
    """A preview does not meet the documented PCM contract."""


def inspect_wav(path: Path, sample_rate: int = 44100, min_duration: float = 15, max_duration: float = 30) -> dict:
    """Inspect bounded PCM16 audio; default remains the M1 15–30 second window."""
    if (type(min_duration) not in (int, float) or type(max_duration) not in (int, float)
            or not math.isfinite(min_duration) or not math.isfinite(max_duration)
            or not .02 <= min_duration <= max_duration <= 120):
        raise AudioValidationError("invalid duration bounds (0.02–120 seconds)")
    path = Path(path)
    if path.is_symlink():
        raise AudioValidationError("symlink inputs are not supported")
    if sample_rate not in (44100, 48000):
        raise AudioValidationError("sample rate must be 44100 or 48000")
    if not path.is_file():
        raise AudioValidationError("input is not a regular file")
    try:
        with path.open("rb") as stream:
            # Bound file size, including ancillary chunks, before parsing or hashing.
            if os.fstat(stream.fileno()).st_size > max(8 * 1024 * 1024, max_duration * sample_rate * 4 + 1024 * 1024):
                raise AudioValidationError("file exceeds bounded PCM size limit")
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
            stream.seek(0)
            with wave.open(stream, "rb") as reader:
                channels = reader.getnchannels()
                rate = reader.getframerate()
                frames = reader.getnframes()
                if reader.getsampwidth() != 2 or reader.getcomptype() != "NONE":
                    raise AudioValidationError("expected uncompressed PCM16")
                if channels not in (1, 2):
                    raise AudioValidationError("expected mono or stereo")
                if rate != sample_rate:
                    raise AudioValidationError(f"sample rate {rate}; expected {sample_rate}")
                if not min_duration * rate <= frames <= max_duration * rate:
                    raise AudioValidationError(f"duration must be {min_duration:g}–{max_duration:g} seconds")
                peak = 0
                consumed = 0
                while consumed < frames:
                    count = min(8192, frames - consumed)
                    raw = reader.readframes(count)
                    if len(raw) != count * channels * 2:
                        raise AudioValidationError("truncated PCM frame data")
                    samples = array.array("h", raw)
                    if sys.byteorder != "little":
                        samples.byteswap()
                    low, high = min(samples), max(samples)
                    if low == -32768 or high == 32767:
                        raise AudioValidationError("full-scale sample detected")
                    peak = max(peak, abs(low), abs(high))
                    consumed += count
                if not peak:
                    raise AudioValidationError("silent preview")
    except RuntimeError as exc:
        # Python wave raises RuntimeError for RIFF chunks that seek past a boundary.
        raise AudioValidationError("cannot read WAV: invalid RIFF chunk boundary") from exc
    except (OSError, EOFError, wave.Error) as exc:
        raise AudioValidationError(f"cannot read WAV: {exc}") from exc
    return {
        "path": str(path), "sample_rate": rate, "channels": channels,
        "frames": frames, "duration_seconds": frames / rate,
        "peak": peak, "sha256": digest,
    }


def collect_files(inputs):
    """Discover files deterministically, without following directory symlinks."""
    files = set()
    errors = []
    for item in inputs:
        path = Path(item)
        if path.is_symlink():
            errors.append({"path": str(path), "error": "symlink inputs are not supported"})
        elif path.is_dir():
            found = []
            def on_error(exc):
                errors.append({"path": str(exc.filename), "error": str(exc)})
            for root, directories, names in os.walk(path, onerror=on_error, followlinks=False):
                directories[:] = sorted(d for d in directories if not (Path(root) / d).is_symlink())
                found.extend(Path(root) / name for name in sorted(names)
                             if Path(name).suffix.lower() == ".wav")
            if not found:
                errors.append({"path": str(path), "error": "no WAV files found"})
            files.update(found)
        else:
            files.add(path)
    return sorted(files), errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-rate", type=int, choices=(44100, 48000), default=44100)
    parser.add_argument("--min-duration", type=float, default=15)
    parser.add_argument("--max-duration", type=float, default=30)
    parser.add_argument("paths", nargs="+", help="WAV files or directories to inspect")
    args = parser.parse_args(argv)
    files, errors = collect_files(args.paths)
    reports = []
    for path in files:
        try:
            reports.append(inspect_wav(path, args.sample_rate, args.min_duration, args.max_duration))
        except AudioValidationError as exc:
            errors.append({"path": str(path), "error": str(exc)})
    print(json.dumps({"ok": not errors, "files": reports, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
