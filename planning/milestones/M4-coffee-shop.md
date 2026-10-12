# M4 — Opening, first level and Cricket

Status: planned, not started. Dependency: M2 and M3; explicit M4 authorization.

- Branch/worktree: reserve `milestone/m4-coffee-shop` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: game/levels/act1*, game/scenes/, assets/sprites/, assets/backgrounds/act1/, assets/ui/, tests/unit/act1*, tests/browser/act1*, docs/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 4.1 — Play the opening and Philadelphia approach

**Deliverable:** Translate approved references into clean scalable assets; create actual Charlie/Dee/Dennis opening stills and bubbles exactly per specification; title, actors cue, Cricket dumpster/kidnapping, Dennis reluctant rescue. Stage curtains only transitions. Build alley platforms with rats, green ghouls, sparse telegraphed denim chicken and pickups; mid/pre-boss flags.

**Acceptance and failure/recovery contract:** ACT1-APPROACH: full story and skip both reach same playable start; natural Charlie eyes, green Dennis, bound scene sequence correct; ads readable without covering hazards; chicken has visual cue; no softlock between flags. Cat food and combined meal distinct.

**Verification / expected red:** Red story-order/progression fixture and enemy spawn/stomp/telegraph assertions, then act1 unit/browser route tests. Run full unit suite for shared simulation changes.

**Evidence:** Opening/dialogue/skip/title, dumpster/chase, approach enemies, flags, Kitten Mittens/other distributed ads, narrow layout. Portrait readability inspected at actual render size.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 4.2 — Defeat Cricket and see Frank abduct Dee

**Deliverable:** Arena isolates Cricket, player, Dee and garbage-can props. Implement charge/dodge/collision/stun/damage/recover cycle; no normal-enemy spawn carryover. Bat/stomp/beam damage only while stunned, normal attacks suffice. Frank kidnapping stills lead to act 2.

**Acceptance and failure/recovery contract:** CRICKET: no rat/ghoul/chicken in arena; correct telegraph/can crash/stun window; attacks before stun don't damage; damage after stun ends once per attack; retries reset boss; win transitions exactly once and unlocks next act. Complete with no Dayman.

**Verification / expected red:** Red unstunned-hit, enemy-leak, double-win and retry tests; unit and headless full Act1 from title through transition, no skip cheats for E2E route.

**Evidence:** Charging/stunned/hit/victory/death/retry and Frank kidnapping screenshots; game audio with Tiny Boy and impact/can cues. M4 release notes.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
