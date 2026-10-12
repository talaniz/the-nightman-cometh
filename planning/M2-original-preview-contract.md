# M2 original-cue audition increment

Authorization: latest user request to build the game and explicitly compose six
original gap/boss cues; no merge/deployment. M1 readiness is required before
implementation. This increment brings phase 2.2 auditions forward to collect
human feedback before production looping in 2.1; all remain on one M2 PR.

## Ownership and bounds

Main owns branch `milestone/m2-audio-production`, worktree
`/home/palpatine/projects/the-nightman-cometh-m2`, stacked on exact M1 dependency
`001cc40559b9e4b0e9b9a99b738a79c22a0693d1` (PR #10). Remote main was fetched and
remains `502f5803ea2d4912658bdc6388b46961d986b866`; no merge is authorized.
Original planning/M1 worktrees remain untouched, including untracked caches.

In-scope paths: tools/audio/arrangement.py, tests/audio/test_arrangement.py,
assets/audio/originals/, docs/evidence/M2/, planning/. No game/UI changes yet.
Reuse existing ensemble synthesis palette, with bounded beat-based scores for
three boss themes, rooftop approach, and two finite kidnapping stings. Preserve
all approved M1 assets byte-for-byte. No audio copied from NES/arcade games.
Original melodies, source notation, tempos, scene assignments and WAV hashes are
reviewable. These are audition candidates, never implied listening approvals.

## Acceptance and verification

- Beat score accepts 40–240 BPM, 1–128 beats, at most 60 seconds, exactly three
  parts (lead, accompaniment, snaps), at most 1000 notes, finite ordered times,
  integer MIDI pitches 0–127 and no events beyond the declared cue duration.
- Render pitch-preserving tempo change by converting beat positions to seconds;
  reuse frozen ensemble timbre. PCM16 mono/44100 Hz, non-silent, below full scale,
  deterministic output with zero end samples for safe joins. Numeric boundaries
  supplement listening; they do not prove musical phrasing/seamlessness.
- CLI reads at most 1 MiB JSON; reject malformed/oversized inputs, unknown schema,
  existing paths and dangling symlinks. Failure emits JSON/nonzero, no overwrite.
  Corrected input must recover successfully. Exclusive output creation.
- Short finite stings end without forcing 15-second preview padding; no runtime
  skip/retry behavior implemented in this increment.

Commands: `PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m1-tools/bin/python -m pytest
 tests/audio/test_arrangement.py -q -p no:cacheprovider`, then full `tests/audio`;
actual `python -m tools.audio.arrangement SCORE OUTPUT.wav` for all six scores;
independent WAV frame/duration/peak/endpoints/hash inspection and rerender equality;
malformed-input/recovery/overwrite/symlink CLI probes; `git diff --check`.
Use an executable stub returning empty PCM for meaningful initial failures:
expected nonempty samples and invalid-input rejection, not import errors.

## Delivery and review

One commit for this coherent audition increment, then its own independent code
review agent. Keep M2 PR draft: human approval, full approved-motif arrangements,
production loops, SFX and actual browser audition are outstanding. Final separate
E2E review follows all milestone code sign-offs. No UI changes: screenshots N/A.
User authorized future music preview delivery through their connected Drive;
private Drive URLs must not be published to the public repository/PR.
