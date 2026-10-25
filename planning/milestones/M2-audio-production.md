# M2 — Soundtrack arrangements and separate SFX phase

Status: all audio samples and actual browser listening approved by user. Ending Dayman / silent credits adjustment implemented; final exact-head review pending. Future credits composition deferred to issue #12.

- Branch/worktree: `milestone/m2-audio-production` at `/home/palpatine/projects/the-nightman-cometh-m2`, stacked on the exact accepted M1 head; see context/PR. One PR across these phases.
- Allowed paths: assets/audio/, tools/audio/, tools/audition.py, tools/check_audio.py, tests/audio/, docs/evidence/M2/, planning/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: user explicitly requested the full build after approving the cue map and finale. Proceed within the documented dependencies; no repeated permission request.

## Phase 2.1 — Turn approved motifs into game cues

**Deliverable:** Build Tiny Boy/bridge loops and Dayman transformation/victory/title variants as needed; proposal accompanies the opening narration and finite ending proposal. Use ../music-cue-map.md. Dayman transformation first audition is 1.10x tempo without pitch change; user requested a slight speedup, not that exact ratio. Establish loop points, transitions, relative mix levels and versioned source notation. No voice cloning or episode recording ripped into build.

**Acceptance and failure/recovery contract:** AUDIO-LOOPS: repeated loop has no click/gap or unintended silence, recognizable lead remains clear, fades do not click, proposal reaches complete cadence. Audition in desktop and minimal actual browser playback harness after user gesture. Audio-unavailable behavior remains visible/recoverable.

**Verification / expected red:** python tools/check_audio.py assets/audio; python tools/audition.py --manifest assets/audio/manifest.json; audio unit tests. Loop boundary numeric checks supplement listening and never establish musical acceptance.

**Evidence:** User listening acceptance of final arrangements; source files plus distributable exports with provenance. If browser harness UI added, capture initial/unlocked/muted/failure states.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 2.2 — Compose original gap and boss music

**Deliverable:** Original Cricket/Frank/Nightman boss themes, rooftop level music,
Frank kidnapping sting and Nightman kidnapping sting. New melodies with energetic
retro arcade/NES instrumentation. Preserve the approved map; no additional scenes.

**Acceptance and failure/recovery contract:** Each cue identifiable by mood/scene,
boss themes faster/more urgent, clear leads at combat volume, no copied game audio.
User approves listening previews before full cue finalization. Loops are seamless;
short stings terminate safely on skip/retry. Record tempo, instrumentation, source
notation, exports, hashes and transition assignments for each.

**Verification:** Same numerical audio and loop checks as 2.1, plus human listening.
Any new synthesis/mixer behavior follows an observed red/green contract. Technical
success alone cannot approve composition. No screenshots unless an audition UI changes.

**Execution record:** first audition increment delivered; see ../M2-original-preview-contract.md and ../../docs/evidence/M2/original-auditions.md. Six original scores/WAVs, 19 observed red cases followed by 69 passing audio tests and actual CLI recovery/reproduction. This audition step is brought forward to gather feedback before production arrangements/loops. Human listening, production finalization and milestone E2E remain pending.

## Phase 2.3 — Create distinct gameplay sound effects

**Deliverable:** Separate phase for original NES-style jump, springy DuckTales-informed stomp, bat swing/hit, damage, cat food, Dayman meal/beam, checkpoint, hoagie, boss defeat and menu sounds. Actually audition reference before claiming match. Tune sounds against music and simultaneous combat.

**Acceptance and failure/recovery contract:** SFX-MIX: stomp sounds at impact, damage distinct from transformation, repeated shots do not clip, mute/volume settings independent, no ear-piercing spikes. Sounds short and identifiable in blind listening comparison.

**Verification / expected red:** Audio checks plus authored cue map. Executable mixer logic red: simultaneous voices exceeding cap, zero-volume leakage, repeated unlock rejection; green checks in audio harness.

**Evidence:** Per-effect inventory, preview reel and listening report. Browser playback inspected; no claim that file generation equals verified sound.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.


## Production increment
See ../M2-production-contract.md, ../../tools/audio/PRODUCTION.md and
../../docs/evidence/M2/production.md. Phases 2.1–2.3 have implemented audition
artifacts and runtime checks. Human approval of expanded/faster/looped audio and
SFX, plus actual human browser hearing, remain open. Do not mark M2 complete from
headless tests or the prior six-composition approval. Final whole-game sign-off
remains reserved by the user.


Latest acceptance supersedes earlier pending-listening execution notes: user approved
the actual browser audition on 2026-10-25. No musical changes requested except
ending Dayman and silent credits. See docs/evidence/M2/finale-routing.md.
