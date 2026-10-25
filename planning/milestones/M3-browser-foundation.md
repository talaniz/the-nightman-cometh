# M3 — Browser foundation and playable keyboard slice

Status: approved by the user on 2026-10-25; implementation and verification in progress. This contract replaces the earlier high-level M3 issue text. Completion still requires the recorded review and human acceptance gates.

## Baseline, authority and outcome

Verified remote main: `65a05abec308e9d7b263a713c14daafa3cc8ee68`, containing merged PRs #1, #10 and #11. M2 audio and browser listening are approved. Ending uses Dayman; credits are silent; new credits composition remains deferred in #12.

The user approved the printed plan before execution. Approval covers the bounded phases below, tests, scoped commits/pushes, one draft PR and the mandated independent reviews. It does not authorize merging that PR, public deployment or final game acceptance.

Deliverable: a locally previewable static pygame-ce/pygbag browser build with a playable training room, representative Dennis/Dayman/Rat Bat visuals, core mechanics, menus, dialogue navigation, local progress and integrated approved audio. This is a foundation slice, not any completed story act.

After approval, pre-dev-prep verifies current main and creates one `milestone/m3-browser-foundation` branch/worktree and one PR across all phases. Main records actual base/head, commands, versions, evidence and review decisions in existing planning records. If main changes substantively before execution, reconcile the plan before touching affected behavior.

## Scope and path boundaries

In scope:
- `game/`: deterministic simulation, pygame presentation, input, scenes, progress and audio adapters; minimal training scene and fixture destinations.
- `tests/unit/`, `tests/browser/`, `tests/fixtures/`: behavior/failure fixtures and real-build browser verification. Existing audio tests remain regression coverage.
- `tools/build_web.py`, `tools/serve_preview.py`, `tools/verify_evidence.py`: build, bounded local preview lifecycle, evidence manifests.
- `pyproject.toml`, applicable dependency locks, `package.json`, `package-lock.json`, Playwright configuration, `.github/workflows/`: pinned tools and test/build CI only.
- `assets/test/`: representative foundation sprites, training scenery, target props and temporary dialogue panels. Do not portray these as final act art. Runtime code may reuse approved production audio read-only; copied/reused audio state logic must retain provenance and tests rather than create an incompatible second mixer.
- `planning/` milestone/context/verification records, `docs/`, and relevant README setup instructions. This explicitly adds planning/README to the older M3 path list so execution records stay in scope.

Out of scope: coffee-shop/bridge/rooftop level layouts and actual boss AI; full storyboards and final act art; final ad placements; new compositions or changed approved audio; USB controller support; mobile touch; multiplayer; backend/database/accounts/telemetry/online saves; production hosting; unrelated rewrites; final three qualifying playthroughs.

Fixes outside these paths need an explicit in-scope rationale and regression contract. A change to product scope or an approved recording requires a new decision, not silent expansion.

## Phase 3.1 — Reliable boot and playable training room

Deliverable: pinned Python/pygame-ce/pygbag build, async browser loop, small staged-Philadelphia training room, preliminary horizontal movement, loader and local preview tool. Native and browser runtime versions must be recorded separately; reuse M2 findings without assuming versions are identical. Minimal pixel art should communicate the stage setting and Dennis silhouette; no strict NES hardware emulation.

Acceptance:
- BOOT-1: clean and warm desktop Chromium launches reach a usable training scene; user action starts the session. Loading is visible before WASM is ready.
- BOOT-2: missing game asset/runtime, rejected network request and a stalled startup show an actionable error with Retry. A 60-second no-progress timeout exposes recovery; successful recovery starts exactly one game loop.
- BOOT-3: `localhost` preview URLs are canonicalized to numeric loopback before SDK startup; both entry URLs reach the same working preview. No dependency request to localhost:8000 or an unintended development package index. CDN dependence is documented; offline startup is not promised.
- BOOT-4: preview tool binds loopback by default, reports its URL/readiness, rejects occupied ports clearly and provides an explicit start/stop lifecycle independent of a chat tool session. No system boot service or public binding is introduced.
- BOOT-5: build records source fingerprint, dependency/runtime versions and artifact hashes. No game-source or asset changes after capture without renewed affected evidence. CI runs real commands and never reports unavailable browser checks as passed.

Fixtures: BOOT-clean, BOOT-missing-asset, BOOT-runtime-blocked, BOOT-stalled, BOOT-retry, BOOT-host-alias, BOOT-port-busy. Expected meaningful red: stalled/missing-resource startup remains blank or lacks retry; retry duplicates update loop; localhost fetches wrong origin. Missing scripts/imports are not accepted as behavior-test failures.

Verification: deliver `python tools/build_web.py --output build/web`, `python tools/serve_preview.py --root build/web --host 127.0.0.1 --port 8765`, `python -m pytest tests/unit -q`, and `npx playwright test --project=chromium --grep BOOT`. Fixture network failures are explicitly asserted; all other console/page/network failures fail the run.

## Phase 3.2 — Combat, pickups, checkpoints and recovery

Deliverable: fixed 60 Hz simulation with rendering separated; bat/stomp/beam combat against controlled training targets, hearts, pickups, checkpoints, death/retry and pause. Training targets exercise enemy contact/projectiles without implementing future story enemies or bosses.

Acceptance:
- CORE-1: equivalent timed input produces matching simulation outcomes at 30/60/120 render Hz; no speed dependence, ordinary collision tunneling or catch-up damage after tab return. Long stalls have a documented bounded catch-up policy.
- CORE-2: Dennis moves/jumps; Rat Bat stays attached through idle/run/jump/swing, with a visible HUD bat portrait labelled RAT BAT. Swing damages targets only during its active hit window; one swing does not repeatedly damage the same target.
- CORE-3: a descending foot contact kills an ordinary target and bounces Dennis; side contact costs one heart. A one-second initial invulnerability window prevents repeated contact damage. Grounding/jump assistance are tunable constants, not new abilities.
- CORE-4: maximum three hearts. Cat food restores one heart capped at three. One combined milksteak-and-jellybeans plate transforms immediately for 10 seconds. Damage does not cancel it. Dayman emits one straight horizontal beam per attack; no spread. Expiry restores normal appearance/attack and the current scene cue. Ordinary bat/stomp combat remains viable without a meal.
- CORE-5: midpoint and pre-boss-style flags each set the respawn location and grant +1 heart only on their first activation, capped at three. Recrossing, death/retry and save/reload cannot repeat the heal. Flags grant no meal, stat upgrade or level-up.
- CORE-6: death offers unlimited retries at the last flag, or the room entrance if none. Respawn restores three hearts, clears Dayman/projectiles/transient attacks, resets encounter targets and retains activated flag IDs for that run. New Game begins a fresh run.
- CORE-7: pause freezes physics, timers and appropriate audio; losing focus clears held inputs and pauses. Resume requires deliberate input and cannot leave a stuck direction/attack.

Fixtures: CORE-render-rates, CORE-bat-window, CORE-stomp-vs-side, CORE-contact-invulnerability, CORE-meal-expiry, CORE-full-health-food, CORE-first-repeat-flags, CORE-death-after-flag, CORE-paused-transform, CORE-held-key-blur. Expected red: side contact treated as stomp; repeated swing damage; flag heals again; transformation advances while paused; multiple/spread beams or stale music returns.

Verification: `python -m pytest tests/unit -q`, `npx playwright test --project=chromium --grep CORE`, relevant existing audio regressions. Actual browser replay uses the built game, verifies visible state plus deterministic fixture observations, and records frame-time measurements on named hardware rather than claiming universal 60 FPS.

## Phase 3.3 — Menus, story framework, saves, QA and approved audio

Deliverable: Start/Options/Password title menu, pause menu, keyboard-only navigation and settings, representative still-dialogue advance/skip/replay, browser-local progress and approved soundtrack/SFX integration. Full opening/cutscene artwork and acts remain M4–M6.

Proposed initial keys: arrows or A/D move; Space jumps; J swings the bat; K fires while transformed; Enter confirms/advances; Escape backs out or pauses. Menus show controls and a visible selection/focus state. Final controller mappings are M7.

Acceptance:
- SHELL-1: all menus/settings/dialogue work by keyboard, including Back and recovery states. Start enters the foundation scene; continuing resumes the saved checkpoint when available. Starting a fresh run asks before discarding an existing run. Pixel scaling remains readable; 390x844 shows clear desktop-keyboard guidance, not touch-play claims.
- SHELL-2: bounded, versioned local save stores only progression/checkpoint/activated flags and settings; no personal data. Valid reload resumes correctly. Malformed, unsupported or unavailable storage produces useful feedback and a usable in-memory session, without crash, bogus progress or repeated flag healing. Ordinary settings persist when storage works.
- SHELL-3: still-dialogue fixtures advance, skip and replay without duplicated stage transitions or skipping required state. Replay does not mutate ordinary progress. Final full scripts are not considered implemented by these fixtures.
- SHELL-4: PAINTDOG/TROLLTOLL/NIGHTMAN are recognized QA destinations with ordinary health/bat; during M3 they enter clearly labelled training fixtures for the corresponding future act, not fabricated completed levels. Invalid codes give useful feedback. QA Dayman/invincibility/checkpoint controls visibly mark QA mode and cannot write ordinary progress. Reset/exit QA restores normal mode predictably.
- SHELL-5: Start unlocks approved music; music/SFX have independent volumes and mute. Jump/stomp/hit/damage/pickup/beam/checkpoint sounds fire at their gameplay event. Dayman temporarily overrides music and returns to the current scene on expiry. Pause/blur/skip/retry do not overlap duplicate players. Audio failure remains visible/recoverable and cannot prevent play.
- SHELL-6: preserve all approved source audio bytes and final placement rules, including ending Dayman and silent credits. Demo scenes may exercise those destinations without implying an implemented finale. User performs a short integrated browser listening/feel check; numerical tests are not hearing acceptance.

Fixtures: SHELL-keyboard-menus, SHELL-invalid-password, SHELL-QA-isolation, SHELL-corrupt-save, SHELL-storage-throws, SHELL-reload-checkpoint, SHELL-new-game, SHELL-dialogue-skip-replay, SHELL-audio-reject, SHELL-audio-current-scene. Expected red: storage exception crashes Start; QA contaminates ordinary save; skip duplicates a scene transition; audio failure blocks gameplay; stale music returns after transformation.

Verification: `python -m pytest tests/unit -q`, `python -m pytest tests/audio -q`, `npx playwright test --project=chromium --grep SHELL`, `python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio`, plus user integrated browser listening/feel check.

## Exact milestone command contract

Commands are future deliverables until implemented; none are reported run for M3 today.
- Resolve and pin dependencies; document isolated Python install and `npm ci` once Node tooling is delivered. Use supported Chromium on the Pi; record executable/version explicitly. Do not require reinstall on every test.
- `python -m pytest tests/unit tests/audio -q`
- `python tools/build_web.py --output build/web`
- `npx playwright test --project=chromium` (all BOOT/CORE/SHELL groups)
- `npx playwright test --project=firefox --grep SMOKE` (boot, Start, movement, pause, menus; unavailable environment is a reported gap, not a pass)
- `python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio`
- `python tools/verify_evidence.py docs/evidence/M3/manifest.json`
- `git diff --check`

Use isolated output directories; prevent accidental overwrite of unrelated artifacts. Build timestamps may differ: reproducibility means pinned inputs, traceable source and verified hashes, not an unsupported byte-identical archive claim.

## Screenshot, review and completion gates

Actual-branch screenshots at 1280x720 and 1920x1080 plus 390x844 guidance: loading/error/retry, title/options/password/invalid code, dialogue/skip/replay, training approach/target, bat states, stomp/damage, meal/Dayman/expiry, cat food/full health, first/repeat flag, death/retry, pause/blur, QA and save/audio failure feedback. Capture representative affected states at desktop sizes and narrow guidance; do not claim game-final visuals from concepts. Inspect every published image. Manifest includes source fingerprint/build hash, fixture/state, viewport/browser, exact command and result. Durable screenshot URLs must be attached to the PR before review.

Main implements and triages every recommendation against this plan and AGENTS.md. After a draft PR exists, a distinct independent code reviewer is assigned to EACH commit, including fixes/docs; all explicitly revalidate the final head. Only then does a separate E2E reviewer exercise actual browser workflows and inspect all attached screenshots, including relevant failure/recovery cases. Code fixes during E2E return through the required review cycle. Review gaps block readiness; no self-signoff. Screenshots supplement interaction testing.

M3 is complete only when acceptance criteria pass, build/CI and evidence checks pass, required browser/platform limitations are declared, integrated listening/feel approval is recorded, all reviewers sign off on the exact final head, and the PR is verified non-draft. Merge/deployment still need separate authorization. Three full-game playthroughs and physical USB acceptance remain M8/M7, respectively.

## Sign-off requested

Approve M3 phases 3.1–3.3 as this bounded foundation slice, including the proposed keys/default timings, labelled QA fixtures and explicit path additions. After approval, main records this contract in the existing M3 milestone file and execution context and begins phase 3.1. Current resumption point: awaiting user decision; no implementation underway.
