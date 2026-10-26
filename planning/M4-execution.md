# M4 execution record

User approved issue5 contract on2026-10-25. Branch milestone/m4-coffee-shop; worktree /home/palpatine/projects/the-nightman-cometh-m4; base1f97dd46a7479536d94c56567479ec73ce86fcd0. Main owns implementation. One PR pending; no merge/deployment authority. Prior M3 preview preserved.

Phase4.1 begins with exact opening sequence, asset packaging/fingerprinting, and safe progression integration. Meaningful reds and results recorded below as observed. Artwork generation uses the imagegen skill; generated story illustration contains no dialogue, which the renderer supplies verbatim.

## Observed red/green cycles

- Initial story/entry/art fingerprint:3 expected assertion failures (`/tmp/nightman-m4-first-red.log`), then13 tests green with existing simulation regression.
- Act1 enemy/boss isolation/retry:3 expected behavior failures (`/tmp/nightman-m4-world-red.log`), then17 tests green.
- Legacy rehearsal migration and completion persistence:2 expected failures (`/tmp/nightman-m4-save-red.log`), then13 targeted/save tests green.
- Completed-act replay incorrectly opened destructive-new-run confirmation:1 expected failure (`/tmp/nightman-m4-replay-red.log`); fixed replay to preserve completion. Full unit suite31passed.
- First browser probe built at `/tmp/nightman-m4-probe1`; actual BOOT smoke pending. Native render inspections are visual development probes, not browser evidence.

Issue14 observation hardening: account for measured wall time since meal-fixture request when checking initial remaining timer, retain0<remaining<=10 and exact simulation-duration tests. No gameplay duration changed. M3 shell test now checks settings reload; actual Act1 checkpoint route belongs in ACT1_NORMAL rather than assuming old rehearsal coordinates.

- Production-art build validation:2 expected failures for missing/corrupt required images (`/tmp/nightman-m4-assets-red.log`); implemented PNG decoding, required paths and sprite alpha checks; full unit suite35passed.
- Chicken warning collision: observed health2 before swoop (`/tmp/nightman-m4-chicken-red.log`), then corrected waiting/warning states to be noncollidable.17 Act1 tests pass.
- Actual browser STORY ACT1 passed on probe2. Boss fixture assertion expected health2 but observed3 after taking a screenshot during its1.5s stun; reset the same fixture after capture before the attack assertion, rather than extending gameplay stun for test latency. Rerun required. Full ordinary browser route remains running.
- First-act pits narrowed to72px during input-route tuning; existing jump physics unchanged. Deterministic ordinary-input route completed using bat/stomp and avoiding the meal; no beams/transformation. This does not substitute for real browser runs or user boss-feel acceptance.

- Probe2 results: STORY and SAVE passed; boss-fixture hit and full normal route failed (2pass/2fail,4.6m). Trace shows all5 deaths at first pit; successive read-only observations jumped from x952–978 to x1062–1077 while right remained held, with roughly400ms+ driver round trips. Updated normal-input test stops before pits for stationary readback and keyboard pulses; no state mutations or gameplay slowdown. Rerun pending.
- QA completion replay red: end menu offered ordinary replay, risking ordinary-save reset. Added dedicated QA replay/exit path retaining isolated QA world; full unit regression rerun below.
- Entrypoint indentation typo from an edit was caught by source parsing and corrected before any new build; not counted as a meaningful red.

- Probe2 route retry progressed to Cricket but still failed after5 deaths (2pit,3boss). Trace isolated unfair damage at x4027 while Cricket at4050 remained stunned. Native regression reproduced losing a heart on knocked-out contact; fixed stunned/recover contact to be safe while retaining charge/standing contact and stun-only boss damage. Full unit38passed; probe3 ordinary keyboard rerun underway. No claim that all earlier deaths were test latency.
- Added neutral player damage flash and short comic impact feedback; refined per-pose Rat Bat anchors and actual Kitten Mittens art. Current screenshots must be refreshed after these changes.

## Current candidate verification

- Source/art fingerprint: `e7d459bcb938d4eee88011f6788729e16e075b553068c53d3be4da873cd8edaa`.
- Fixture build `/tmp/nightman-m4-probe3`; ordinary build `/tmp/nightman-m4-normal1`.
- Full native gameplay/audio:134passed in64.87s, using `PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit tests/audio -q`.
- Shared JavaScript loader:2passed (`npm run test:loader`).
- Audio audit: no errors; `assets/audio` and approved M2 director/backend diff against merged baseline is empty.
- Probe3 actual Chromium full ordinary-input route: passed1.5m (1.6m invocation), keyboard-only opening through Cricket and Frank, no passwords/invincibility/mutation fixture use. This invocation used the fixture-capable package; ordinary-package routes and explicit recovery/reload coverage remain required and pending.
- Final actual-browser screenshot/regression batches now running serially. No review or final acceptance yet.

Final visual inspection caught a clipped cat-food label, shop lettering sliding away
from the painted sign under parallax, and Cricket facing left while charging right.
Corrected label width, backdrop-relative sign anchors and Cricket facing. These are
in-scope visual fixes; affected images and build fingerprint must be refreshed again.
No claim of final evidence is made for earlier captures.

Evidence inspection: live bat-swing capture had already returned to idle during
screenshot latency. Added explicitly labelled test-build-only frozen visual poses
for bat/jump/damage and boss stages, rendered by the actual game. These are not
interaction proof; live attack/normal-route checks remain separate. Added actual
Act1 first/repeated flag crossing assertions/captures. Final manifest must identify
frozen poses; ordinary builds still omit all fixture code. Rebuild required because
the shared source fingerprint includes fixture source even when omitted from normal.

Final candidate identity supersedes all earlier probe fingerprints:
`674bf4acf595c3616a83fe56c49216a505e52cb2faed4148a8bdd84ecf175560`.
The fixture/ordinary review builds share that source fingerprint; ordinary APK
excludes fixture module/marker and packaged art bytes match source. Actual final
checks and screenshot provenance are maintained in docs/evidence/M4/execution.md.

Final Chromium ordinary checks passed4/4 in6.4m: full rescue, forced death/retry/
reload rescue, startup/movement/pause and mute/restore. Firefox first ordinary
route failed after5 deaths (one pit, four boss). Completed trace shows the player
reaching the far can after Cricket's stun expired (for example x4056 with stun
remaining0, then warning/contact damage). Several attempts had reduced him to1HP.
This supports an input-driver strategy problem, not changing boss vulnerability:
replace chasing across the510-unit arena with waiting beside the left can, release
movement before readback, and use bounded key presses near pits. Gameplay and
approved tuning remain unchanged. The remaining Firefox batch was interrupted130
for diagnosis; its uncompleted checks are not passes. New driver requires rerun.

A sign screenshot taken during an ordinary-route pit death was rejected during
visual inspection. A separate live-input fixture approach captures the sign safely;
the rejected death frame is excluded from the published evidence gallery.

The revised Firefox driver completed ordinary rescue with3 hearts. The post-rescue
reload then timed out waiting120s for `window.__nightmanGame`; no game mutation or
password was used, and no console error was recorded in the completed trace. This
is a failed Firefox test, not full acceptance. The second route did not run because
`--max-failures=1` stopped the batch. Required Firefox success/reload evidence remains
open for the existing desktop CI and independent review; cause is not assumed.

Final focused Dayman beam/ad capture passed in47.6s. An earlier beam assertion saw
zero projectiles because the live beam had already killed the ghoul (trace confirms
ghoul alive=false); capture moved to a clear pre-boss stretch via labelled QA Dayman.
All57 retained screenshots were opened and inspected by main; hashes/source verified.

Final native gameplay/audio regression:138passed in64.71s (exit0). Approved audio and M2 mixer/director remain byte-unchanged from M3. Draft PR next; all independent/human gates remain open.

### CI ordinary-route timing correction

Run40261162801 passed all14 fixture Chromium checks but both ordinary routes
failed their final dialogue assertion: expected dialogue, received training.
Downloaded traces show both stopped at the fixed650-observation cap with Cricket
at1HP and the player alive at1heart, with advancing simulation steps (2757 on the
full route,1809 after recovery reload). Fast-host polling exhausted the observation
budget while battle was still progressing. Firefox was not reached.

Before changing the driver, define this test-only correction: replace observation
count with a bounded180-second wall-clock route deadline; retain the actual keyboard
route, fewer-than5-deaths assertion, required rescue/Frank/completion/save/reload
assertions and prohibition on fixtures/QA/skips/invincibility. Allow420seconds for
the complete test including boot and reload. Paths: tests/browser/act1.spec.cjs,
this ledger and M4 verification evidence. No gameplay, assets or runtime changes;
the57 screenshots retain their verified source fingerprint. Re-run ordinary
Chromium/Firefox workflows via CI and independent final-head review. The original
CI failure is the observed red; a rerun must demonstrate green before acceptance.
