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
