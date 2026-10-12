# M6 — Rooftop battle, ending and full keyboard journey

Status: planned, not started. Dependency: M5; explicit M6 authorization.

- Branch/worktree: reserve `milestone/m6-rooftop-ending` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: game/levels/act3*, game/bosses/nightman*, game/scenes/, assets/backgrounds/act3/, assets/sprites/, assets/story/, tests/, docs/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 6.1 — Reach and defeat Nightman

**Deliverable:** Roof/fire-escape platform route with visible landing zones, flags and approach enemies. Boss telegraphed dash/leap/recovery, capped ghoul summons as sole boss-enemy exception; no rats/chickens/crew/walking guns. Dayman single horizontal shots; keyboard bat/stomp-only route possible.

**Acceptance and failure/recovery contract:** NIGHTMAN: summon cap enforced, spawned ghouls cleaned on death/win, no unavoidable spawn on player, no arena escape softlock, boss beatable unpowered, transformation timeout during fight safe. Tune provisional summon frequency/duration with observed play.

**Verification / expected red:** Red unlimited summon/no-safe-space, retained summon after retry, multiple-beam/spread and progression assertions; relevant unit suite and real-browser Act3 workflows.

**Evidence:** Approach, telegraphs, ghoul spawn, bat/stomp, single beam, timeout, damage/retry/win; screenshot differences from older concept recorded.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 6.2 — Finish complete narrative and progression

**Deliverable:** Implement Charlie proposal cue and stills, ACTUAL Waitress rejection, Dee callback, Charlie low/high hand rant, hard cut ending/title with Dayman music. All three acts chain correctly; credits/replay return clear; narrative timing supports readable bubbles and full song cue. Resolve campaign-ad typography and visual consistency across game.

**Acceptance and failure/recovery contract:** FULL-KEYBOARD: title to credits all acts, no duplicate transition or trapped dialogue, skip/replay coherent, ending differentiates Dee vs actual Waitress, clocks paused during scene transitions, save/restart choices clear. User checks tune/context and story fidelity.

**Verification / expected red:** Red finale order, wrong speaker identity, skip transitions, save resume at act boundaries; full browser route plus core regressions. Record an exploratory full run, explicitly NOT one of final M8 three.

**Evidence:** Full ending stills, menu/replay and all new states; listen to full cue transitions. Documentation/install/control notes, known issues and release notes. No claim final release before M7/M8.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
