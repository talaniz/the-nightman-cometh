# M9 — Full walkthroughs and desktop packaging

Authorized: user requested preparing the work, three complete walkthroughs, correction
of user-visible defects, then Mac and Windows packages. Main owns this milestone on
`milestone/desktop-packaging`, worktree `/home/palpatine/projects/the-nightman-cometh-desktop`,
base `4902f3357fc3234776d1366417182bfa92fa1829`. One draft PR across phases.
No merge, public release, paid signing service or production deployment authorization.

## Scope and acceptance

1. Inspect ordinary-build normal and death/checkpoint/reload routes end to end,
   opening through all three bosses and ending/credits, without fixtures, cheats or
   invincibility. Fix reproducible user-visible defects within existing mechanics.
2. Qualifying acceptance requires three runs on one frozen artifact: keyboard normal,
   keyboard recovery and physical USB controller. Remote automation is labeled as such;
   it cannot count as physical USB. No USB device is attached to the Pi. User participation
   requested. Prior controller approval does not qualify the current artifact.
3. Additional full walkthrough video contains actual game audio, readable manually
   advanced story and credits. Verify streams, duration, synchronization and inspect
   visual/audio content; publish durable PR evidence. Presence of an audio track alone
   is not listening acceptance. Fixes invalidate prior candidate qualification.
4. Build Windows x64 portable ZIP and separate macOS Apple Silicon/Intel app ZIPs.
   No Python, browser, server or SSH required on recipient machines. Include approved
   game art/audio, operating instructions, versions and SHA256 manifest; exclude source
   audio, QA fixtures, private data, credentials and development-only files.
5. Native saves survive restart in per-user application data, outside the app bundle.
   Failed/corrupt storage remains recoverable through existing user-facing messages.
   Native controller translates SDL standard controls into existing action semantics;
   disconnect/focus loss pauses and requires release before resuming. Unknown devices
   must not silently use guessed button mappings. Physical compatibility remains a gate.
6. Launch extracted packages from an unrelated working directory on target OS runners;
   verify resources, audio decoding, save restart and actual rendered title. Record
   architecture and supported OS tested. Headless checks do not prove physical audio,
   Finder/Gatekeeper or Explorer user launch acceptance.

## Phases / verification contracts

A. Baseline ordinary walkthrough inspection. Existing commands:
`NIGHTMAN_BUILD=<frozen-build> npx playwright test --project=chromium --grep FULL_KEYBOARD`.
Use existing remote workflow, frozen artifact manifest and screenshot evidence.
Merged-head broad run 43653641924 and recording run 43654287539 dispatched at base;
results pending, not passes. Recording uses candidate artifact from run43487934311,
verified against source fingerprint before playback. Record source/asset hashes.

B. Desktop boundary fixes (game/main.py, new game/desktop.py and focused tests).
Expected red: separate Storage instances lose the saved JSON; native controller
snapshot is absent regardless of input. Verify persistent save/restart, bounded reads,
atomic writes, platform data directories, failed-write preservation, SDL button mapping,
disconnection, stable device choice, focus loss and existing Controls release barriers.
Command: `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest tests/unit -q`.
No changes to approved songs, levels, story, boss balance or rendering unless an observed
walkthrough defect requires it and receives its own regression contract.

C. Reproducible packaging (tools/desktop, requirements-desktop.lock, workflow and docs).
Remote sequential Windows/macOS builds; pinned builder and runtime. Test clean launch,
asset load/audio decode, screenshot, restartable save and missing/corrupt resource failure.
One-folder bundles avoid self-extraction startup overhead. Unsigned test packages only;
Mac ad-hoc signatures are not Developer ID notarization. No global security bypass advice.
No public GitHub Release; retention-limited CI artifacts are staging, not final handoff.

D. Candidate freeze, renewed normal/recovery routes, physical USB participation, final
recording with audio, per-commit independent code reviews then separate E2E at exact head.
Capture actual implementation at1280x720,1920x1080 and390x844 browser guidance plus native
window states. Reviewers inspect captures and actual workflows. Missing hardware or OS
access is an explicit gap. No release-ready claim until all required evidence is complete.

## Boundaries and resources

No framework migration, server, database, telemetry, new songs, mobile controls or public
hosting. Native packages preserve browser functionality. Existing worktrees/previews remain
untouched. Pi runs only lightweight sequential diagnostics/tests: stop heavy work at75C,
active throttling or available RAM below400MiB; remote builds/recording preferred. Initial
reading45.3C,1230MiB available; swap full, so no local browser/build launched.

## Current state / next action

Preparation complete; baseline remote executions pending. Packaging and walkthroughs are
not complete. Physical controller run, target-machine launch/listening and final recording
inspection are open. Record actual outcomes here and on the single milestone PR.
