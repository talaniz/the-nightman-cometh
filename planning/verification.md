# Verification contracts and evidence

## Current planning checks

For M0 inspect all new files, compare against conversation decisions, verify relative Markdown links and parse prompt JSON. Run git diff --check and confirm all published images were visually inspected. No app exists, so headless GAME inspection, actual game screenshots, audio fidelity, USB hardware and playthroughs are NOT RUN / not applicable to this docs-only PR. Independent reviewer must exercise document navigation/requirements traceability, not mislabel it gameplay E2E.

## Future command contract (NOT AVAILABLE OR RUN YET)

M3 phase 3.1 delivers and documents these interfaces. M1/M2 deliver audio tools when appropriate. Dependency versions and exact entrypoints must be verified and pinned before use. Failing because a command is missing is not a behavior-test red.

- python -m pytest tests/unit -q : simulation, collisions, timing, checkpoint/health, save/input adapters.
- python tools/build_web.py --output build/web : pinned pygbag build and manifest hashes.
- python tools/serve_preview.py --root build/web --host 127.0.0.1 --port 8765 : local static preview, never production server.
- npm ci && npx playwright install chromium : pinned browser tools (install once as needed).
- npx playwright test --project=chromium : real build workflows, traces/console/network failures and screenshot captures; tests launch/stop local preview.
- python tools/check_audio.py assets/audio : decode, duration/format, peaks/clipping, loop boundary reports. NOT musical-fidelity proof.
- python tools/audition.py --manifest assets/audio/manifest.json : human audition with per-track version decisions, desktop and browser audition required for delivery.
- python tools/verify_evidence.py docs/evidence/<milestone>/manifest.json : existence, source revision/fingerprint and hash checks.
- git diff --check : every commit candidate.

Per-phase contracts list fixture IDs and scenarios. Add red command/assertion, actual result, green result, tool versions and skipped checks before requesting review. Headless browser screenshots must be opened and visually inspected. If Pi Chromium/WASM support fails, diagnose authorized environment or use a documented supported environment; do not mark skipped checks passed.

## Fixture contract

Deterministic test seed; synthetic saves; distinct approach and boss entry scenes for QA only; no personal information. Fixture definitions reproduce initial health, flag state, Dayman timer, spawn counts, player position, controller state and audio state. Release builds must not depend on debug fixtures. Test skipped intro/replay, held-key blur, pause/resume, resized window, blocked audio unlock, asset failure, invalid password, corrupt or unavailable local storage, death after flag, flag recrossing, Dayman expiration, boss progression, controller unplug and reconnect.

Capture desktop 1280x720 and 1920x1080. Capture 390x844 for layout/no-touch guidance, not a claim of supported mobile input. Changed UI states: title/loading/error/settings/password; dialogue/skip; approach and boss; checkpoint first/repeat; meal/expiration; cat food/full health; damage/death/retry; paused/blur; ending/credits; controller connected/disconnected and menu focus. Scope each PR to affected states; final release covers all.

## Evidence publication

Use docs/evidence/<milestone>/ with manifest containing source commit or exact tested tree fingerprint, final reviewed head, build hash, browser/device, viewport, fixture/state, reproducible command, result and screenshot/audio/video paths. Capture source before evidence-only commit, then verify final head changes no tested game source/assets. If game source changes, recapture affected evidence. Embed durable GitHub image URLs in PR body or linked evidence comment. Caption each state. Reviewers inspect every supplied screenshot. Concept mockups are labeled as such, never claimed as captures.

For music include source performance reference, manually verified cue/timestamp range, arrangement version/hash, audio previews, listening decision and browser playback evidence. Source filenames/MIDI assertions do not demonstrate recognition. Do not claim listening if tools only expose metadata. Obtain source audio access legitimately; document any permission/distribution limitation before release. Do not commit downloaded third-party episode recordings by default.

## Three final qualifying playthroughs

All on SAME final candidate build. No skip codes, invincibility, scene teleporting or reduced boss health. Ordinary saves start clean. Pause is permitted and recorded. A run completes opening → three full approaches/bosses → proposal/rejection/Dee/Charlie ending → end title. Require actual browser play, not source inspection or unit-test substitute.

| Run | Operator and route | Required observations |
| --- | --- | --- |
| 1 | Main acceptance operator, desktop keyboard, normal progression | Controls, platform readability, three bosses, all story, music/SFX, completion |
| 2 | Independent E2E reviewer, keyboard, deliberate failure/recovery | Die/retry after flag; repeat flag no farm; meal timeout; pause/blur; all acts completed without cheats |
| 3 | Physical USB pad operator, independent reviewer observes/verifies evidence | Menus/story/gameplay end-to-end, unplug/reconnect at safe point, analog/d-pad/deadzone, final credits |

A human hardware operator may supply recorded physical-controller evidence if agent cannot directly operate hardware; mark identity and independent reviewer verification. Automated Gamepad injection is supplemental only. Each run logs timestamp, head/build hash, browser/platform/device/controller, route, elapsed time, defects, screenshot/video references and explicit completed/not-completed status. Audio must be auditioned at least once through the actual browser route; headless muted runs cannot establish sound quality.

Any material issue blocks full sign-off: crash/softlock, broken progression, missed/stuck controls, unreadable UI, unfair unavoidable attack, lost checkpoint, false healing, broken music/loops, failed controller reconnect, or material story/art divergence. Accepted fixes require per-commit review, relevant regressions, updated evidence and renewed three runs after ANY game/runtime/asset modification. Docs-only changes may use documentary revalidation with identical build hashes. Report residual minor issues explicitly; no universal bug-free guarantee.

## Release operational checks

Check cold-load and warm-load, missing runtime/assets, supported desktop browsers (Chromium mandatory, Firefox smoke; declare untested browsers), initial loading feedback, CPU/frame-time on intended desktop plus measured Pi where available, key-repeat and game-speed independence, scaling/legibility, audio mix and volume persistence, no secrets/network telemetry, pinned dependencies and third-party notices. Performance targets: responsive 60Hz simulation, report measured rendering frame times rather than claim unmeasured universal performance. Validate downloadable static package, install/build instructions and rollback to prior artifact; no production deployment in this gate.

## Delivered M3 candidate verification

The executable M3 commands, environment and actual results are recorded in [M3 execution evidence](../docs/evidence/M3/execution.md); [README](../README.md) documents reproduction. Earlier milestone command lists remain contracts, not claims of execution. Full gameplay/USB and three qualifying final runs remain later gates.
