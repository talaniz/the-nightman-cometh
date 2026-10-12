# M7 — Dedicated USB-controller sprint

Status: planned, not started. Dependency: M6 complete keyboard game; explicit M7 authorization; physical USB pad and operator available before sign-off.

- Branch/worktree: reserve `milestone/m7-usb-controller` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: game/input/, game/adapters/browser_gamepad*, game/ui/control*, tests/unit/input*, tests/browser/controller*, docs/controls.md, docs/evidence/M7/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 7.1 — Use controller across the browser game

**Deliverable:** Browser Gamepad API through bounded adapter into shared input actions; standard mapped USB pad first, document actual mappings; d-pad/left stick, jump/attack, pause/confirm/back and story. Deadzone, edge-trigger buttons, keyboard fallback, no double actions if both sources active. Show device and control prompts.

**Acceptance and failure/recovery contract:** PAD-SIM: injected mapping/deadzone/held-button tests, menu focus, pause/skip, disconnect clears input and pauses, reconnect requires safe resume, unsupported mapping gives guidance/fallback. No promise of all controllers.

**Verification / expected red:** Red disconnect-stuck movement, drift, double-confirm, unsupported-map crash; input unit suite and headless Gamepad injection. Mocked checks explicitly labeled supplemental.

**Evidence:** Controller controls/menu/disconnect/unsupported-map screenshots plus real browser trace. Independent E2E exercises mapping fixtures; hardware still pending.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 7.2 — Verify real USB play and recovery

**Deliverable:** Connect an actual supported pad to intended desktop browser; record model/vendor/product where available, browser/OS, mapping. Exercise all menus and act mechanics, unplug/reconnect and sustained play. Main may coordinate human operator if tooling cannot manipulate real pad.

**Acceptance and failure/recovery contract:** PAD-HW: physical d-pad/stick and buttons work without drift; replug and keyboard fallback safe; button labels accurate; full storyline navigable. Missing pad/access is blocking evidence gap, not a mock substitute.

**Verification / expected red:** Document manual hardware checklist with timestamp/video and browser gamepad diagnostics; rerun automated controller regressions only after fixes.

**Evidence:** Independent reviewer directly tests or verifies attributed human hardware evidence and exercises browser interactions. Real pad required; release notes list only tested configurations.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
