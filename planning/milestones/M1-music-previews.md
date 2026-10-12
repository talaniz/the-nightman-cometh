# M1 — Music recognition previews

Status: all four musical previews approved by the user; preservation/integration and independent reviews in progress. See ../M1-integration-contract.md and ../context.md.

- Branch/worktree: `milestone/m1-music-previews`; actual worktree/base recorded in context. One PR across these phases.
- Allowed paths: assets/audio/previews/, assets/audio/manifest.json, tools/audio/, tools/check_audio.py, tools/audition.py, tests/audio/, docs/evidence/M1/, planning/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: user authorized proceeding with the plan on 2026-10-11. Environment and remaining listening gap are recorded in context.

## Phase 1.1 — Hear the reference and prove Dayman

**Deliverable:** Identify the episode Dayman performance using the official FX clip; audition actual audio, record source/cue timestamps and arrangement provenance. Choose a reproducible notation/MIDI/synthesis workflow only after confirming local ARM64 tooling and legal source access. Produce a short 15–30 second instrumental melody-led preview plus a simple chip arrangement. Do not infer notes from lyrics or generate a generic mood substitute.

**Acceptance and failure/recovery contract:** Fixture AUDIO-DAYMAN: source vs preview listening comparison. Check decodable file, consistent sample rate, no clipping and no missing end. User must identify the tune without vocals and approve direction. If audition/tooling unavailable, record blocked musical verification; no pretend pass.

**Verification / expected red:** Documentary source check first; executable audio validation tools use meaningful failing malformed/clipped fixtures. Planned commands: python -m pytest tests/audio -q; python tools/check_audio.py assets/audio/previews; python tools/audition.py --manifest assets/audio/manifest.json (establish exact supported paths in phase contract).

**Evidence:** Source log, preview files/hashes, waveform checks and actual user listening decision. Screenshot evidence N/A unless an audition UI is introduced, then capture controls/loading/error at specified viewports.

**Execution record:** See ../../docs/evidence/M1/approved-previews.md for actual approvals, preservation tests and limits. Exact-head independent reviews are recorded in PR #10; they remain required before readiness.

## Phase 1.2 — Approve the remaining three motifs

**Deliverable:** After Dayman approval, produce Tiny Boy, Troll Toll and I Was That Little Boy/Marry Me previews. Same instrumental palette. Record revisions and listening feedback per song. Keep tribute rerecordings separate from episode sources.

**Acceptance and failure/recovery contract:** AUDIO-TINY, AUDIO-TROLL, AUDIO-PROPOSAL: each recognizable to user, intended phrase intact and distinguishable. Reject/iterate close-but-wrong melody/rhythm. No full soundtrack expansion before each track's acceptance.

**Verification / expected red:** Same audio commands; regression-test already approved Dayman file hash unchanged unless deliberately revised. Human decisions are required, not automated similarity scores.

**Evidence:** Four named approved preview versions and source/cue references. Independent reviewer checks traceability and listens when capable; disclose unavailable playback.

**Execution record:** See ../../docs/evidence/M1/approved-previews.md for actual approvals, preservation tests and limits. Exact-head independent reviews are recorded in PR #10; they remain required before readiness.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
