# Local music preview workflow

These are development tools, not game runtime dependencies. All generated music remains a candidate until the user's listening approval.

## Render or revise a candidate

The checked-in score JSON contains seconds and MIDI pitches. Edit a COPY to preserve the version under review, then render to new filenames:

```sh
python3 tools/audio/preview.py assets/audio/previews/dayman-v1.json /tmp/dayman-listen.wav
python3 tools/audio/preview.py assets/audio/previews/dayman-v1.json /tmp/dayman-chip.wav --style chip
python3 tools/check_audio.py /tmp/dayman-listen.wav /tmp/dayman-chip.wav
```

Renderer uses Python 3.11 stdlib only. Existing outputs are rejected, not overwritten. It bounds input to 1 MiB, score length to 1,000 notes and duration to 15–30 seconds. Notes must be ordered, non-overlapping and within the preview. Sine and chip modes share identical pitches/timings and use short attack/release ramps. Chip mode uses a truncated odd-harmonic lead; it is not a hardware-accurate NES emulator or a full soundtrack arrangement.

Machine-selected notes can be wrong, missing, or from a harmony voice. Model activation is not the probability of musical correctness. Ask the listener about tune/rhythm first and timbre second; record feedback against the exact file hash. Never mark approval automatically.

## Isolated source-analysis environment

Verified environment versions are in ../../docs/evidence/M1/inference-environment.txt. Source processing uses Basic Pitch 0.4.0 / ONNX, librosa 0.11.0 and Demucs 4.0.1 / CREPE 0.0.24 with CPU PyTorch 2.5.1. Models and dependencies live outside the repository; source recordings and stems are temporary.

Basic Pitch's Python 3.11 packaging requires TensorFlow even when using its supported ONNX backend. We installed Basic Pitch with --no-deps, then its needed ONNX/audio packages explicitly. pip reports the missing TensorFlow metadata dependency; do not describe pip check as passing. Actual inference, not package metadata alone, establishes capability. Renderer/tests do not import any of those packages.

The full source procedure, weights, hashes and limitations are in ../../docs/evidence/M1/dayman-v1.md. Keep the original reference and stems out of Git. Only new synthesized previews, editable notes/MIDI and technical evidence are published.

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m1-tools/bin/python -m pytest tests/audio -q -p no:cacheprovider
git diff --check
```

No UI is introduced; screenshot evidence is not applicable. Technical audio checks and independent CLI review cannot substitute for user listening acceptance.

## Approved four-track baseline

Dayman v1 is rejected historical evidence. The approved score IDs are dayman-v2,
proposal-v1, little-boy-v1 and troll-toll-v2. From the repository root:

```sh
python -m tools.audio.approved assets/audio/previews/dayman-v2.json /tmp/dayman-approved.wav
```

Use a fresh output name; existing files/symlinks are refused. Install the pinned
`tools/audio/requirements-preview.txt` in a development venv. Lead and duet use
the original standard-library renderer; Troll Toll uses the frozen NumPy recipe.
The static game consumes exported audio, not these dependencies. Different hardware
or numerical library versions may change PCM rounding; compare against the committed
approved WAV hashes before accepting regenerated output. Do not silently replace an
approved file if its bytes change. Run the four exact PCM preservation tests.

Normalized scores encode the short approved phrases after source tempo-map conversion,
ties and swing interpretation. Reproduction needs no private source files, credentials,
network or pretrained models. Provenance/limitations: ../../docs/evidence/M1/approved-previews.md.
Full game loops and original gap music are M2 work, not yet delivered.
