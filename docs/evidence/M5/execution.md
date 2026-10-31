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
