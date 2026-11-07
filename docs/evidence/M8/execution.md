# M8 execution

Base 43032c4; isolated worktree; no prior edits changed. All results below pending unless explicitly recorded.

First behavioral increment (phase 8.3 Cricket brought forward to verify latest request): tests/unit/test_m8_cricket.py, game/levels/act1.py; deterministic first-cycle brake/reversal, subsequent crash within bounded time, safe stationary telegraph, pause/retry reset. Test command: SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest tests/unit/test_m8_cricket.py -q. Expected red: no brake state/mid-charge reversal exists. No art or visual acceptance implied by this increment. Phase 8.1 follows.

## Observed behavior and regression results

- Cricket red: 2 failures, absent brake/reversal. Green: 25 new+Act1 checks.
- Story red: 3 failures, old dialogue/extra ending. Effect red: manual advance skipped transformation. Green: 7 story/finale checks.
- Combat red: 4 failures, missing ingredients/eggs/chickens/Nightman bursts. Green: 26 new+Frank+Nightman contracts.
- Route red: 3 failures, unchanged pre-boss positions. Extended approaches by 900/750/850 pixels with one additional pit and two raised platforms per act. Migrated known legacy pre-boss saves. Ordinary native bat/stomp routes pass after updating drivers for the added pits.
- Latest complete native+audio run: 240 passed in 66.06s. Node boot-state/gamepad files passed. This predates final visual refinements; renew affected checks before commit.
- Rendering checks are supplemental, not browser acceptance. Generated original and edited assets use built-in image_gen; exact prompts in art-prompts.json. Inspected source images; actual-browser screenshots and motion still pending.
- Initial local telemetry: 44.8C, available RAM ~1514MB, full 199MB swap. Subsequent samples under 50C, vmstat observed no active swap-in/out. No parallel local browser suites run.
- No independent reviewer sign-off, physical controller playthrough, final video/audio capture or release readiness yet.

Final local increment checks: 142 unit tests passed in 3.63s after composing both Dennis costumes over one shared backdrop and using one fixed atlas anchor. JavaScript syntax checks and git diff --check passed. Prior complete 240 native/audio tests include the same approved audio bytes; no audio production source/assets changed. Node boot-state and gamepad checks passed. Native title, Cricket/dumpsters and revised finale frames inspected under /tmp/nightman-m8-render; these are explicitly not browser evidence.

Browser next: push the single coherent implementation commit, create draft PR, run remote CI and inspect actual screenshots. Capture changed states missing from existing browser suites before requesting independent code review. Hardware/listening and recorded full-run gates remain open.

## Browser/recording verification increment

PR23 https://github.com/talaniz/the-nightman-cometh/pull/23 is draft at first implementation commit 5e1929a47f900fb10bc7effa688d934f55e0ffbc. Remote CI 42424915146 exercises actual browser workflows; results pending.

Added focused actual-browser tests for Cricket's stationary tell/reversal/dumpster crash and automatic Dayman reveal/pointer lyric advance, with screenshots. Added opt-in remote Xvfb/PulseAudio/FFmpeg recording of the ordinary keyboard route, with readable story pacing, full credits and separate video/audio stream validation. Syntax checks pass; recording execution is pending. An uploaded CI recording is staging evidence only: inspect and publish a durable PR link before acceptance. It is not a substitute for the physical USB run.

Packaging contract: every new required M8 image must be validated before building. Observed six failures when each new image was omitted from the asset inventory, then six passes after adding the required paths. No game/audio bytes changed in this increment. Any final evidence must still identify the build fingerprint.

## In-scope balance and browser findings

Initial real browser CI 42424915146: four controller groups passed; focused Chromium 23 passed / 2 failed, so ordinary full runs did not start. Failures were retained, not waived:
- Act 1 sign screenshot driver walked left from the relocated pre-boss flag through new enemies with one heart. Replace that obsolete positioning route with a dedicated sign camera fixture; ordinary combat routes still cover those enemies.
- Rooftop pre-boss fixture took immediate contact damage from the new nearby ghoul before accepting input. Native reproduction failed (screen dead instead of training). Move that ghoul farther from the checkpoint; retain the one-heart flag test.
- Ordinary native Nightman diagnostic finished in 7.27 seconds without charge/fire. A new ordinary-input regression failed. Move charged bursts earlier, raise health from six to eight with 0.85-second hit immunity, and fit all health markers on screen. Focused Nightman/Act3 checks: 29 passed, including unpowered completion with charge/fire observed.

These accepted findings are within the approved difficulty/recovery boundaries. The changed game candidate invalidates earlier qualifying runs; no such runs are claimed. Latest full unit suite result is recorded with this commit. Independent reviews and final E2E remain pending actual final-candidate browser evidence.

Latest unit result: 150 passed in 15.45s.

Visual follow-up: extending the bridge left the captive and Troll Crossing label at their old world positions. A rendered-scene test failed because Dee appeared behind Frank. Shift both with the arena; require the captive to be beyond Frank and inside the visible arena. This is a game-rendering change, so prior candidate runs are not qualifying final runs. Title scaling and extended-route captures have also been added without changing route inputs.
