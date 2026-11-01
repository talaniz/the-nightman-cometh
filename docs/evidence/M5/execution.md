# M5 execution record — in progress

Base d27ca3e643dcacf7c511ceeb6ce50c9c10282f87 (merged polish PR #18). User authorized both phases with the added Frank escape still and exact Dennis line. See issue #6 and planning/milestones/M5-underbridge.md.

## Actual results so far

- Progression red: 4 assertion failures for missing added still, Act 2 handoff, real TROLLTOLL entry and old completed-save continuation.
- Bridge red: 6 failures / 1 pass before crew/save integration; inherited one-shot flags already passed.
- Projectile red: rightward gun shot moved left (698 instead of >700). Optional dx now preserves legacy -120 default.
- Frank red: arena cleanup, repeated damage/immunity, windup/throw and completion assertions failed. Initial collision matrix scaffolding errors are recorded but not counted as meaningful behavioral red.
- Initial focused green: 18 passed; added stage/ledge/ending cases: 23 passed.
- Cue red: audition director automatically changed Nightman kidnapping to rooftop. Game-only manifest removes audition next-map; actual scene owns progression. Audio files/production manifest unchanged.
- Native regression: 179 passed in 77.60s. Earlier integration run: 173 passed / 2 failed, both obsolete Act 1 preview-end expectations; updated to verify intentional Act 2 handoff and QA save isolation.
- Loader check passed. No audio asset diff against base; git diff --check passed.
- Built actual pygbag ordinary and fixture artifacts at /tmp/nightman-m5-normal-v2 and /tmp/nightman-m5-fixture-v2.
- Native layout inspected for bridge, Frank and added dialogue. These are not browser acceptance.
- First traced browser run interrupted under Pi memory pressure. Second untraced run reached bridge and first ledge but upper-transfer check failed: driver held Right until landing poll, allowing it to run off destination. Driver now releases movement at destination and verifies landing separately. No physics changed for this failure. Remaining tests interrupted for matching-build rerun.
- Current actual-browser pass, final screenshot manifest, independent reviews and human in-game music/visual acceptance are PENDING. No all-pass browser claim.

## Release notes

Adds underbridge Act 2 with animated Duncan/Z and walking guns; composed mounted signs; cat food, combined meal and one-shot flags; Frank's active bat/stomp/beam fight with straight sandwiches; Nightman abduction; stage-aware saves and a safe two-act preview endpoint. Appends the user-requested extra Frank kidnapping still and exact Dennis dialogue without removing earlier stills. The polished nailed bat/animations are reused in Act 2.

Rooftop gameplay, final ending/credits, physical controller testing, three full-game acceptance runs and deployment remain later milestones. Approved music files stay unchanged. No new dependencies or backend.

## Initial CI findings — run 41250071738

Native/loader/build passed; 17 focused browser tests passed and 3 failed. Act 2 approach reached the retry assertion, but the test read hearts before the Enter event was consumed. The existing polish pause test likewise compared pre-pause state with paused state. Both now wait for the requested observable state before assertions; assertions remain intact.

The Frank test reset a Dayman fixture directly into another training fixture with the same baseline cue, so the previous transformation music persisted despite the new world. Test-build fixture application now forces scene resynchronization and publishes an acknowledgement ID after rendering. The harness waits for that ID instead of a fixed sleep. Normal gameplay already resynchronizes on menu/death/scene transitions. Added fixture acknowledgement is diagnostic only and does not grant ordinary builds mutation access. Initial CI failures are retained, not counted as passes.

## Screenshot staging

Pi browser startup is resource constrained and interrupted/failed local runs are not acceptance passes. CI now retains synthetic actual-browser captures as a staging artifact. Main must download and inspect every image before selecting and publishing durable PR evidence. Native layouts are not substituted for browser screenshots.

Local final-source bridge run landed on all four raised ledges, then failed a one-heart assertion because the 230ms input pulse did not reach the flag on the busy Pi. The harness now holds movement until it observes the flag activation (or meal transformation), then releases and asserts the same health outcome. No game physics or checkpoint rules changed.

## Verified CI and evidence, 2026-10-31

Run https://github.com/talaniz/the-nightman-cometh/actions/runs/41250831919 at 659d2d8f5ef6d4397be7be2c97105d1b8c458d89 succeeded: 179 native tests (12.98s), loader checks, fixture/ordinary builds, 20 focused Chromium tests (4.7m), two ordinary two-act Chromium routes (3.1m), four Firefox smoke/ordinary-route checks (3.5m). Ordinary routes use no fixture/QA mutations and cover death/retry/checkpoint reload and completed-save reload. This is a two-act preview, not three qualifying final-game runs.

Artifact 13060999056 was downloaded and selected captures opened individually before publication. Gallery and manifest contain 51 inspected images, including 16 live Pi animation crops from a passing ACT2_MOTION test. The manifest verifies hashes and unchanged game/runtime/asset fingerprint 9029eb4ff6544158b45647224653f4a1e0b9476985e3adec7d7dbb3480d2d178. CI uses Ubuntu 24.04, Python 3.11.17, bundled Playwright browsers; Pi uses Python 3.11.2, pygame-ce 2.5.8, Node 22.23.2 and Chromium 139.0.7258.66. Exact commands and capture state metadata are in the manifest/gallery.

Local mixed browser run: motion passed, approach failed the fixed input pulse assertion, story exceeded a 5s transition wait. Subsequent focused run timed out during startup and stalled during Frank; interrupted after the CI success rather than treating retries as acceptance. Pi showed 199MiB swap fully used, ~69MiB free RAM and Chromium in I/O wait while other project work ran. Host later stalled for hours; cause of the entire stall is not established. These failures remain limitations. Outcome-based checkpoint waits and bounded 30s story transition waits now avoid the two known harness timing assumptions; final-head CI must validate this harness update. No game physics was changed to obtain a test pass.

Audio validator returned no errors; audio bytes remain unchanged against base. Approved compositions are preserved. Automated cue selection is not human listening acceptance. Independent exact-head code and E2E review are still required; PR remains draft.

## E2E readability fix

Independent reviewer found the browser font draws em-dash ink over preceding words in the new Frank still (PR comment6553030543). Main accepted this A1 defect. Exact authored story strings are unchanged. Dialogue rendering now reserves a separate punctuation cell and draws a pixel stroke, with matching line wrapping. Native font does not reproduce the web glyph fault, so a deterministic overhanging-font fixture verifies word pixels and a clear punctuation gap. Old whole-line path failed this assertion; corrected renderer plus Act2/session regression: 20 passed. An initial implementation exposed render-surface height differing from font height; fixed by sizing to actual rendered runs.

Previous 51-image source manifest is temporarily stale until refreshed captures from this renderer are attached. All four dialogue strings containing em dashes (opening0, opening8, opening9, Frank extra) require visual refresh, plus affected wrapping. All per-commit signoffs and E2E must revalidate the new head. Independent Pi browser launch failed before interactions; no E2E pass yet.
