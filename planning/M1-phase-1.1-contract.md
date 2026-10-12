# M1 phase 1.1 execution contract

Authorization: the user's 2026-10-11 request, "please proceed with the plan", authorizes the planned implementation cycles. Human listening gates remain required; merge and deployment are not authorized.

Route: M1 implementation, starting with a bounded audio validation increment. Scope: tools/check_audio.py, tests/audio/, docs/evidence/M1/, planning/. No composition is claimed before actual reference audition. The audition player and synthesis workflow follow source availability.

## Repository preparation

Branch: milestone/m1-music-previews. Worktree: /home/palpatine/projects/the-nightman-cometh-m1. Main owns this worktree.
Base: reviewed planning head 342a4e54a5cd9ec87f44dd1881f520fa58f7e08d; planning PR #1 remains unmerged. This is a stacked milestone branch, not a standalone branch from main. PR targets plan/full-game-milestones until the separately authorized planning merge; no duplicate planning changes belong to the M1 diff. Retarget onto main after verifying the planning merge ancestry.

## Observable behavior for this increment

A command-line validator checks local instrumental-preview WAV files. It accepts uncompressed PCM16 mono/stereo, 44,100 Hz by default or explicitly selected 48,000 Hz, duration 15–30 seconds inclusive, complete declared frames, non-silent samples and no full-scale sample values. It reports deterministic JSON with path, frames, duration, channel count, peak and SHA-256. These checks do not prove a melody is right, the musical phrase ends correctly, or audio is free from audible distortion.

Explicit files or directories (recursive *.wav) are accepted. Missing input, empty directories, malformed/truncated audio, unsupported formats, rate/duration mismatch, silence and digital-rail samples produce useful JSON errors and nonzero exit. Any invalid member fails a mixed batch. Directory discovery does not follow symlinks; explicit symlinks are rejected. No audio playback, network access, file modification or UI.

## Verification contract before implementation

Synthetic PCM fixtures only; no episode audio in Git.
Run /tmp/nightman-m1-tools/bin/python -m pytest tests/audio -q.
First use a callable minimal interface and demonstrate assertions failing for valid reports and invalid audio rejection, rather than module/import failure. Then implement and rerun.
Run python3 tools/check_audio.py <fixture-path> for independent real CLI valid, mixed-invalid and empty-directory cases.
Run git diff --check. Record tool versions and actual outcomes in docs/evidence/M1/.
Screenshot evidence: not applicable, command-line tool only.
Each commit receives a distinct independent code reviewer. E2E follows code sign-off and can validate this increment, but M1 acceptance stays pending until actual source audition, previews and user listening approval.

## Musical acceptance still required

Dayman 15–30 second melody-led and chip previews after verified source listening; then user approval before the other three motifs. Waveform validity is never musical recognition acceptance. Missing source/playback capability is an explicit gap.


## 2026-10-12 — authorized local transcription and listening iteration

User accepted the recommended approach: automatic local note extraction, deterministic synthesis, then user listening correction/approval. This supersedes the requirement that the implementing agent personally hear the reference before producing an explicitly unapproved candidate. Do not claim automated extraction establishes musical accuracy.

New increment paths: tools/audio/, tests/audio/, assets/audio/previews/, assets/audio/manifest.json, docs/evidence/M1/, planning/. Reuse M1 branch and PR #10.
Source correction: prior FX scene ends before Dayman; locate actual FX Dayman highlight and record timestamps/hash. Keep source recordings/captions temporary, not in Git.
Install Basic Pitch with ONNX in isolated venv; record ARM64 inference capability and package versions, without adding ML runtime to the game.
Select candidate melody notes from actual inference events, preserve source-timing provenance and edits, label uncertain extraction. Export editable MIDI and note JSON; render 15–30 second PCM16 mono 44.1 kHz sine melody and chip variation. No vocals/source samples in generated files.
Verification: selection fixture chooses strongest eligible active note, preserves rests and excludes bass; known A4 synth has 440 Hz zero crossings, correct duration, no rail samples and silent tail. Reject invalid time ranges, overlaps, pitch, style, empty score and non-finite values before allocation. Observe stub behavior failures first, then run full tests and actual generated-WAV validator.
Human gate: user listens to both candidates against linked source. No inferred approval. Musical fidelity, source phrase completeness and preferred timbre remain pending.
Screenshots N/A for this CLI/artifact-only increment. Per-commit code review and independent E2E remain mandatory; earlier reviewers revalidate final head.
