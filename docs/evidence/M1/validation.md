# M1 audio validation increment — 2026-10-11

This is technical tooling evidence, not musical acceptance or completed M1.

## Environment and reproduction

Pi aarch64; Python 3.11.2. Runtime uses only Python standard library.
Tests: pytest 9.1.1 in an isolated temporary venv; no system Python modifications.
Recreate: python3 -m venv /tmp/nightman-m1-tools, then /tmp/nightman-m1-tools/bin/python -m pip install pytest==9.1.1.
Run from the milestone worktree: /tmp/nightman-m1-tools/bin/python -m pytest tests/audio -q.
CLI: python3 tools/check_audio.py <WAV-file-or-directory>; optional --sample-rate 48000. Exit 0 means all inspected files meet technical checks; 1 means invalid audio/input; argparse usage errors exit 2. Output is JSON for validation runs, conventional argparse help/errors for invalid invocation.

## Observed red → green

Before implementation, tools/check_audio.py exposed AudioValidationError and inspect_wav(path, sample_rate=44100), returning {}.
Command: /tmp/nightman-m1-tools/bin/python -m pytest tests/audio -q -k 'valid_report or invalid_audio_rejected' --tb=short.
Actual: exit 1, 9 failed / 8 deselected. The valid report lacked frames; eight invalid fixtures failed DID NOT RAISE AudioValidationError. No import/environment failure.

After implementation: /tmp/nightman-m1-tools/bin/python -m pytest tests/audio -q.
Actual: 17 passed in 2.16 seconds. Covers valid mono/stereo and duration endpoints; unsupported rate/format/channels; too short/long; silence; positive/negative full-scale samples; malformed/truncated/missing files; actual CLI directory recursion, mixed success/failure, empty input directory, symlinks and explicit 48 kHz selection.
git diff --check: passed.
Refactor: kept single cohesive stdlib tool; separate collection, inspection and CLI presentation. No extra framework.

## Limits

Full-scale detection is a conservative digital-rail check; it cannot detect all distortion. Declared-frame completeness is not proof that a musical phrase finishes correctly. Nonzero samples do not prove a useful melody. No actual source or output has been listened to by this agent; there is no audio-perception tool in this session.
No audition player, synthesizer, score, melody preview or approved audio has been delivered yet. No game/browser/controller test has run.
Screenshot evidence is not applicable: no UI or game interaction changes.
Independent reviewers post their exact-head verdicts on the draft milestone PR. Review of this increment cannot approve unfinished M1.
