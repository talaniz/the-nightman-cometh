# M5 — Bridge approach, Frank and Nightman abduction

Status: planned, not started. Dependency: M4; explicit M5 authorization.

- Branch/worktree: reserve `milestone/m5-underbridge` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: game/levels/act2*, game/enemies/bridge*, game/bosses/frank*, game/scenes/, assets/backgrounds/act2/, assets/sprites/, tests/, docs/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 5.1 — Traverse the bridge crew and walking guns

**Deliverable:** Duncan/Z distinguishable reference-based sprites, readable patrol/attack patterns, cartoon guns walk/pause/shoot. Stomp/bat/sunbeam ordinary-enemy defeat. Platforms and flags under bridge. Include Shadynasty's, Wolf Cola, Fight Milk and distributed ads without crowding.

**Acceptance and failure/recovery contract:** ACT2-APPROACH: projectiles avoidable, enemy facing and shots consistent, platform collision stable, no invisible blockers, checkpoint and exit reliable. Preserve ordinary-enemy rules and no injected content outside scope.

**Verification / expected red:** Red walking-gun telegraph/fire cooldown/projectile collision and platform fixtures; relevant unit tests plus browser Act2 approach with QA fixture for diagnosis and real route for acceptance.

**Evidence:** Desktop/narrow gameplay, gun windup/shot/stomp/puff, crew, flags and readable signs. Audio Troll Toll loop and ordinary combat.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 5.2 — Fight Birdo-inspired Frank and continue story

**Deliverable:** Short shuffles facing Dennis with clear throwing windup; straight horizontal sandwiches, never arcs. Bat/stomp/sunbeam destroy sandwiches and damage Frank (not pause-only). Preserve pointy nose and warm costume. Arena regular-enemy-free. On defeat Nightman jumps down, exact toll line, grabs Dee/runs, Dennis watching and Dee 'Not again!' still.

**Acceptance and failure/recovery contract:** FRANK: sandwich Y remains fixed in flight, all three attacks hit both targets, short invulnerability avoids multi-hit bugs, normal bat/stomp victory possible, no lingering crew/gun bullets in boss entry, retry/win no softlock. Story played or skipped gives same act3 state.

**Verification / expected red:** Red arcing projectile, sandwich immunity, Frank pause-only immunity, enemy/projectile leakage and story-state tests; browser full Act2 route including loss/retry.

**Evidence:** Frank shuffle/windup/straight throw/stomp/bat/beam/victory plus Nightman abduction stills. Reviewer confirms final source matches motion evidence, not just static trajectories.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
