# M1 — Music recognition previews

Status: planned, not started. Dependency: M0 planning accepted; explicit M1 authorization.

- Branch/worktree: reserve `milestone/m1-music-previews` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: assets/audio/previews/, assets/audio/manifest.json, tools/audio/, tools/check_audio.py, tools/audition.py, tests/audio/, docs/evidence/M1/, planning/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 1.1 — Hear the reference and prove Dayman

**Deliverable:** Identify the episode Dayman performance using the official FX clip; audition actual audio, record source/cue timestamps and arrangement provenance. Choose a reproducible notation/MIDI/synthesis workflow only after confirming local ARM64 tooling and legal source access. Produce a short 15–30 second instrumental melody-led preview plus a simple chip arrangement. Do not infer notes from lyrics or generate a generic mood substitute.

**Acceptance and failure/recovery contract:** Fixture AUDIO-DAYMAN: source vs preview listening comparison. Check decodable file, consistent sample rate, no clipping and no missing end. User must identify the tune without vocals and approve direction. If audition/tooling unavailable, record blocked musical verification; no pretend pass.

**Verification / expected red:** Documentary source check first; executable audio validation tools use meaningful failing malformed/clipped fixtures. Planned commands: python -m pytest tests/audio -q; python tools/check_audio.py assets/audio/previews; python tools/audition.py --manifest assets/audio/manifest.json (establish exact supported paths in phase contract).

**Evidence:** Source log, preview files/hashes, waveform checks and actual user listening decision. Screenshot evidence N/A unless an audition UI is introduced, then capture controls/loading/error at specified viewports.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 1.2 — Approve the remaining three motifs

**Deliverable:** After Dayman approval, produce Tiny Boy, Troll Toll and I Was That Little Boy/Marry Me previews. Same instrumental palette. Record revisions and listening feedback per song. Keep tribute rerecordings separate from episode sources.

**Acceptance and failure/recovery contract:** AUDIO-TINY, AUDIO-TROLL, AUDIO-PROPOSAL: each recognizable to user, intended phrase intact and distinguishable. Reject/iterate close-but-wrong melody/rhythm. No full soundtrack expansion before each track's acceptance.

**Verification / expected red:** Same audio commands; regression-test already approved Dayman file hash unchanged unless deliberately revised. Human decisions are required, not automated similarity scores.

**Evidence:** Four named approved preview versions and source/cue references. Independent reviewer checks traceability and listens when capable; disclose unavailable playback.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
