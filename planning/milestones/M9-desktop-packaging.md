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
Merged-head broad run43653641924 and recording run43654287539 passed at the baseline.
They are historical evidence, not current-candidate qualification. Recording used
candidate artifact from run43487934311,
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

PR25 remains draft. Runtime head add35aa1af49fcb47c4cd1dedb36b974d247c8a6 has four
per-commit code-review sign-offs. Corrected native package run43657884551 passed all
three targets, including missing/corrupt resource probes; inspected target captures
and archive SHA256 checks passed. Local private candidates are preserved under
ignored `build/desktop-candidates/add35aa`, served through the existing SSH preview
at `/desktop-add35aa/`. They are unsigned test candidates, not a release.

Current full browser run43657884482 passed319 unit/audio tests,36 focused browser
checks and normal/recovery full routes in Chromium and Firefox. Independent current
run43659758840 also passed;44 fresh captures inspected by the independent reviewer.
Current ordinary artifact fingerprint and every file hash were verified locally.
Frozen private browser preview: `/browser-add35aa/`. Prior e7cfee7 run43655723059 passed
318 unit/audio tests,36 focused browser checks and four ordinary full keyboard routes
(normal/recovery in Chromium/Firefox). Independent browser run43657609032 passed,
but credits contrast correction invalidates those as current-candidate qualification.
Independent native credits interactions and current six package captures were rechecked.

Baseline recording43654287539 is282.2seconds with video/stereo audio; samples across
its full duration were visually inspected and audio measured non-silent. It is historical,
not the requested final post-acceptance recording. Physical USB, target-machine GUI/
listening, final same-artifact qualifying runs and final recording remain open. No USB
controller attached on the Pi; user participation requested, no response yet. Do not
claim three qualifying runs, full listening acceptance or readiness to merge.

Next: publish inspected evidence in one documentation-only commit,
obtain its distinct code review and all final-head revalidations. Final source/asset
changes require renewed qualifying runs. Keep PR draft while hardware/final evidence
is missing. No merge or public release authorization applies to PR25.

## Inspection addendum

Native options capture exposed low-contrast keyboard hints over bright footlights.
In-scope correction: opaque dark backing under existing menu hint, preserving wording,
controls, artwork and panel layout. Regression: render menu over bright background and
require an opaque dark hint backing; capture actual options/pause at current source.
Packaging failure contract also requires intentionally missing/corrupt audio to fail
installation verification rather than silently succeed. Runner probes restore the bytes
before archiving. No successful-package or listening claim follows from negative probes.

Current browser capture `normal-complete.png` also exposed the same low-contrast hint
on credits, whose rendering uses a separate path. Extend the same dark backing to
credits only; preserve all text, music and layout. Regression parameterizes bright
background checks for options and credits. Observed credits pixel `(255,240,190)`
instead of INK `(15,18,32)` before fix. Renew packages and ordinary browser candidate
because this changes the runtime fingerprint; prior runs remain historical evidence.
