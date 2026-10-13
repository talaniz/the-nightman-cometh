# M2 original-cue auditions — technical evidence

Contract: [original-preview contract](../../../planning/M2-original-preview-contract.md).
Predecessor M1 head `001cc40559b9e4b0e9b9a99b738a79c22a0693d1` passed all four
per-commit reviewers and separate workflow acceptance; PR #10 is verified non-draft.
It remains unmerged; this increment is stacked, not a merge/deployment.

## Observed red / green

On Python 3.11.2, NumPy 1.26.4, pytest 9.1.1 (Pi/aarch64):

`PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m1-tools/bin/python -m pytest tests/audio/test_arrangement.py -q -p no:cacheprovider`

Initial callable stub produced **19 meaningful failures**: expected duration 2
versus 0, expected 88200 PCM samples versus 0, and invalid score/note/count/order/
duration inputs not raising ValueError. No import/syntax/environment failures.
Implemented bounded beat conversion and reused frozen ensemble rendering rather
than introducing another oscillator/mixer. No additional abstraction was useful.

`PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m1-tools/bin/python -m pytest tests/audio -q -p no:cacheprovider`

**69 passed (21.79 seconds)**, including exact preservation of all four approved M1
PCM exports. Tempo test measures a 440 Hz lead at two tempos with duration changes
and unchanged dominant pitch. Numeric frequency checks are not musical hearing.

## Actual CLI and export checks

Ran `python -m tools.audio.arrangement SCORE OUTPUT.wav` for every one of the six
scores, then rerendered into new temporary paths. Complete WAV bytes match each
committed artifact. Repeated output invocation fails without altering its hash.
Malformed JSON emits error JSON/nonzero and creates no output; corrected input
successfully renders. Oversized input and dangling output symlink fail safely.
No symlink target is created. These were actual subprocess/CLI workflows.

For every WAV independently read PCM with Python wave/NumPy: mono PCM16/44100Hz,
frame count equals declared beats/BPM, nonzero peak below full-scale, first/last
samples zero. Detailed durations, peaks, note counts and SHA-256 values are in
[manifest](../../../assets/audio/originals/manifest.json). Zero endpoints avoid a
sample-step discontinuity but do not prove absence of a perceived rhythmic gap.

## Gates still open

All six compositions await human listening acceptance. No source recording was
imported, and no agent hearing is claimed. Full approved-song arrangements,
production loops/fades, faster Dayman audition, SFX and actual browser playback
remain M2 work. No executable game or UI changed, so screenshots are N/A.
Per-commit review follows publication; milestone E2E happens after complete code
review. PR remains draft even if this increment receives scoped code sign-off.


## Accepted review finding: boundary-ending percussion

Independent reviewer /root/review_m2_3273338 identified that a noise snap at the
exact end of the cue could violate the promised zero endpoint. Main accepted it
as a valid in-scope correctness issue; no extra features or M1 timbre changes.
Reproduction: 120 BPM, one beat, only a snap from beat 0.96 to 1.0. New regression
`test_noise_snap_at_cue_end_has_safe_zero_endpoint` failed with `130 == 0` before
the fix (1 observed failure). The M2-only render wrapper now applies a 5 ms end
ramp; the frozen approved M1 synthesis function is untouched.

The full audio suite then passed **70 tests (22.80 seconds)**. Actual CLI rerender
of all six audition scores preserved every complete WAV SHA-256, so the existing
Drive auditions remain current. No new user audition needed for this technical
fix because those bytes did not change. Original composition approval remains
pending. A distinct fix-commit reviewer and original-reviewer final-head
revalidation are required before scoped workflow review.


## Later listening decision
The user approved all six original compositions: "those all sound fine". Prior
pending-listening text above is historical. Production loop/codec and whole-game
acceptance remain separate. No approved original WAV bytes changed.
