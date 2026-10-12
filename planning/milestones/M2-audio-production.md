# M2 — Soundtrack arrangements and separate SFX phase

Status: planned, not started. Dependency: M1 previews individually approved; explicit M2 authorization.

- Branch/worktree: reserve `milestone/m2-audio-production` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: assets/audio/, tools/audio/, tools/audition.py, tools/check_audio.py, tests/audio/, docs/evidence/M2/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 2.1 — Turn approved motifs into game cues

**Deliverable:** Build Tiny Boy/bridge loops and Dayman transformation/victory/title variants as needed; proposal is a finite ending cue. Establish loop points, transitions, relative mix levels and versioned source notation. No voice cloning or episode recording ripped into build.

**Acceptance and failure/recovery contract:** AUDIO-LOOPS: repeated loop has no click/gap or unintended silence, recognizable lead remains clear, fades do not click, proposal reaches complete cadence. Audition in desktop and minimal actual browser playback harness after user gesture. Audio-unavailable behavior remains visible/recoverable.

**Verification / expected red:** python tools/check_audio.py assets/audio; python tools/audition.py --manifest assets/audio/manifest.json; audio unit tests. Loop boundary numeric checks supplement listening and never establish musical acceptance.

**Evidence:** User listening acceptance of final arrangements; source files plus distributable exports with provenance. If browser harness UI added, capture initial/unlocked/muted/failure states.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 2.2 — Create distinct gameplay sound effects

**Deliverable:** Separate phase for original NES-style jump, springy DuckTales-informed stomp, bat swing/hit, damage, cat food, Dayman meal/beam, checkpoint, hoagie, boss defeat and menu sounds. Actually audition reference before claiming match. Tune sounds against music and simultaneous combat.

**Acceptance and failure/recovery contract:** SFX-MIX: stomp sounds at impact, damage distinct from transformation, repeated shots do not clip, mute/volume settings independent, no ear-piercing spikes. Sounds short and identifiable in blind listening comparison.

**Verification / expected red:** Audio checks plus authored cue map. Executable mixer logic red: simultaneous voices exceeding cap, zero-volume leakage, repeated unlock rejection; green checks in audio harness.

**Evidence:** Per-effect inventory, preview reel and listening report. Browser playback inspected; no claim that file generation equals verified sound.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
