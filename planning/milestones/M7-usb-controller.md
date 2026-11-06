# M7 — Dedicated USB-controller sprint

Status: authorized; phase 7.1 in progress. Dependency: M6 complete keyboard game; explicit M7 authorization; physical USB pad and operator available before sign-off.

- Branch/worktree: reserve `milestone/m7-usb-controller` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: game/input/, game/adapters/browser_gamepad*, game/ui/control*, tests/unit/input*, tests/browser/controller*, docs/controls.md, docs/evidence/M7/
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: user approved the refined M7 contract and Pi resource limits, then explicitly requested implementation. Record user authorization and environment capability before phase 1.

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

## Approved refinement and execution contract (2026-11-06)

Base 96924a51474379180283745e73950203bdb19c36 (merged PR21). One branch milestone/m7-usb-controller and worktree /home/palpatine/projects/the-nightman-cometh-m7. Main owns implementation. Physical pad/desktop/browser details requested; hardware validation cannot be replaced by simulation.

Acceptance: standard-mapped USB pad, d-pad/left-stick movement, bottom face jump/confirm, left face bat, top face beam, right face back/skip, Start pause/resume. Shoulder buttons provide mute/retry audio. Menus/options/death/retry/finale/credits and controller character selection for QA passwords work; keyboard typing retained. No stick drift, duplicate actions, held-button dialogue skipping, transition input leakage or involuntary reconnect resume. Opposing directions neutral. Active-pad loss or tab blur clears input and pauses gameplay. Release controls before rearming. Unsupported/missing/blocked API leaves keyboard usable with guidance. Initial browser click/keyboard audio unlock may be required and clearly explained. No raw device identifiers stored or sent.

Refined integration paths: game/input/, game/web/gamepad.js, game/main.py, game/session.py, game/render.py, game/web/loader.js and style.css, tools/build_web.py (bridge/footer wiring), tests/unit/test_input*, tests/browser/controller*, tests/browser/gamepad*.test.cjs, package.json and existing CI workflow only for focused checks; planning/context.md, this contract, docs/controls.md and docs/evidence/M7. No physics/level/story/audio asset changes, dependencies, backend, telemetry, multiplayer, remapping, rumble, mobile/Bluetooth/native packaging, merge or deployment.

Before implementation, executable Controls interface returns neutral; tests must fail on observable movement/edge/disconnect behavior, not imports. Command: PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit/test_input_controls.py -q. Retain red, same green, full tests/unit tests/audio, npm run test:loader, node --test tests/browser/gamepad.test.cjs. Browser fixture build via python tools/build_web.py --output build/web --test-fixtures, npx playwright test --project=chromium --grep CONTROLLER. Ordinary build --output build/normal with existing ACT1_NORMAL Chromium and SMOKE|ACT1_NORMAL Firefox regressions. Tests/commands added here are planned until results recorded.

Browser contract: actual pygbag loop samples synthetic Gamepad API fixtures for drift/held/duplicate/malformed/unsupported/disconnect/reconnect/blur, navigation, password editing, options/audio recovery and all gameplay actions. Capture 1280x720 and1920x1080 plus390x844 guidance; contextual prompts, title/dialogue/pause/options/password/death/retry/ending/credits, connected/release/disconnected/unsupported states. Durable manifest records revision/fingerprint/viewport/state/hashes; main and E2E open every required screenshot. Tests are simulated-pad checks, not hardware proof.

Hardware contract: identified USB pad on recorded desktop OS/browser/version, exact build hash, timestamped attributable checklist/video demonstrating all menus, three acts/bosses, move/jump/bat/beam, death/retry, pause/blur/unplug/replug, keyboard fallback, story/ending/credits. Only tested configurations listed verified. Physical run required before M7 readiness. M8 still requires three final-candidate no-cheat runs.

Pi protection: check temperature, throttling availability, memory/swap pressure and load before heavy work. Sequential local tests/builds, no overlapping intensive agents; heavy browser suites in remote CI. Monitor local commands; stop at75C, current throttling, or sustained memory pressure threatening responsiveness; resume only after recovery. Record pauses/skipped checks as gaps. Initial44.3C, ~2113MiB available, swap167/199MiB occupied but vmstat showed no churn; firmware throttling query unavailable (/dev/vcio missing). Do not alter kernel devices to work around this. No heavy local browser.

Execution: next observe Controls red, implement bounded bridge/shared actions and targeted tests. Required independent per-commit code review precedes distinct E2E; final-head signoffs plus hardware evidence before non-draft transition. Missing hardware remains an explicit gate, not a pass.

Browser finding refinement: first actual run passed25existing focused checks but3controller boots failed because synthetic Gamepad lacked SDL-required id/index/value fields. Make fixtures faithful, and isolate display/font initialization from unused SDL joystick subsystem so unavailable/denied Gamepad API at startup cannot bypass our keyboard fallback. Meaningful native startup red observed (joystick incorrectly initialized). Add real-browser denied-at-startup test. Run controller fixtures first in CI to expose failures before unrelated regression routes; same full suite remains required.

Focus/error refinement: next remote run passed3controller workflows (menus/password/audio/credits, three-act attacks/retries/mixed input, denied-API startup) but opening another headless tab did not produce the expected pause. Do not claim an OS-focus pass. Automated integration now injects explicit browser focus signals and document focus state; physical tab switching stays mandatory. Add a latched blur/visibility interruption so a brief loss between game samples cannot disappear before polling. Node red observed missing interruption latch. Screenshot inspection found stale password error after edits; native red observed and require clearing it for both input methods. Capture password at both desktop sizes and wait for footer status before snapshots.

#### Recovery hint correction
On absent, unsupported or unavailable pad status, keyboard fallback hints must immediately replace controller hints. Scope: Controls.sample, native input regression and controller recovery browser evidence. Reproduce with test_lost_or_unsupported_pad_restores_keyboard_hints (expected false pad_mode, currently true), then run input/action/startup tests and remote browser recovery captures. No gameplay or mapping change.

#### Batched menu input regression
Remote ACT3_SAVE revealed that a quick Down then Enter within one pygame frame discarded navigation and activated Start Act1 instead of Continue. Scope: shared action dispatch and native action regression. Menu navigation/adjustment must precede confirmation within the same sampled frame; pause/back remain dominant and at most one activation occurs. Expected red: saved-game title with Down+confirm should enter training, currently enters confirm. Retain the existing actual-browser saved-game test unchanged and rerun all browser routes.
