# M3 — Reproducible browser foundation and keyboard slice

Status: planned, not started. Dependency: M1 accepted; M2 approved assets required for phase 3.3 sign-off; explicit M3 authorization.

- Branch/worktree: reserve `milestone/m3-browser-foundation` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: game/, tests/, tools/build_web.py, tools/serve_preview.py, tools/verify_evidence.py, pyproject.toml, lock files, package.json, playwright config, .github/workflows/, assets/test/, docs/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 3.1 — Cold-load a real browser build

**Deliverable:** Pin working pygame-ce/pygbag/Python versions after Pi/ARM64 spike, implement async browser-compatible loop and minimal playable training room. Build/serve/test commands from verification.md become real. Add CI for unit/build/headless inspection; document runtime/CDN loading and failure UI.

**Acceptance and failure/recovery contract:** BOOT: clean browser loads game, asset/runtime failure gives helpful feedback and retry, repeated load no duplicate loop. Simulated movement works in real pygbag build, console/network errors fail tests. Output artifact reproducible enough to hash/identify.

**Verification / expected red:** Red: missing asset and stalled load produce no recovery; capture assertion failure before behavior fix. python -m pytest tests/unit -q; python tools/build_web.py --output build/web; npx playwright test --project=chromium.

**Evidence:** Actual branch loading/title/training-room/error screenshots at 1280x720,1920x1080,390x844. Build log, dependency lock, browser version, trace. No dummy-SDL substitute.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 3.2 — Move, fight, heal and respawn

**Deliverable:** Implement fixed-step movement/jump, bat carried animation/hitboxes, foot stomp/bounce, side damage/invulnerability, hearts, combined meal Dayman 10 seconds with straight single beams, cat food, one-time healing flags, pause/blur and deterministic respawn. Preserve mechanics independent of renderer.

**Acceptance and failure/recovery contract:** CORE: same physics at varying render rates; no tunneling or repeated contact damage; cap hearts; one meal sufficient; timeout returns to bat; flags first +1 then +0 including after death; no boss checkpoint meal. Death returns full-health default to last flag and clears transient state. Every boss support allows normal attacks.

**Verification / expected red:** Meaningful red tests per mechanic: flag recross adds heart; timer runs while paused; spread beams emitted; side contact counted as stomp. Unit suite and headless CORE fixture replay; browser tests inspect actual state and movement.

**Evidence:** Screenshots bat idle/run/jump/hit, meal/Dayman/expiration, first/repeat flag, full-health cat food, damage/death/retry/pause. Frame-time observations.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 3.3 — Use complete menus, story navigation and QA tools

**Deliverable:** Title Start/Options/Password, music/SFX volumes, story advance/skip/replay, checkpoint progress persistence with storage-failure fallback, keyboard mappings shown onscreen. QA codes separate from normal save, explicit QA indicator and reset. Integrate approved audio unlocked by Start.

**Acceptance and failure/recovery contract:** SHELL: invalid password feedback; keyboard-only settings/back; reload valid save; malformed/unavailable storage doesn't crash; blur clears held inputs; audio blocked/muted usable; skip doesn't skip required stage state; narrow viewport explains desktop controls. No mobile touch.

**Verification / expected red:** Red fixtures corrupt-save, storage-throw, held-key-blur, invalid-password, audio-reject; python -m pytest tests/unit -q and npx playwright test --project=chromium; check audio/evidence.

**Evidence:** All menus/story/QA/pause/error states captured. Actual browser music audition plus source manifest. Screen readers/text alternatives for controls/menu labels where practical; keyboard focus visible.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
