# Act 1 polish verification

Contract: [M4-polish](../../../planning/milestones/M4-polish.md). Scope: issue17's seven observations only. Base main `5e982162e2a68969cd0434a821e8417d80389e3d`. Source/build fingerprints and individual capture states are recorded in manifest.json.

## Observed red and green

- Native red: four meaningful failures (two unreachable first ledges; rat and ghoul poses identical at successive simulation times), one existing reachable ledge passed. See [red log](logs/red.txt).
- Native regressions: 152 tests passed after implementation, before the final sprite-padding and test-fixture refinement. See [native log](logs/native.txt).
- Final complete native regressions: **152 passed** in68.43s, including final fixtures/art/renderer. See [final native log](logs/native-final.txt).
- Final sprite-focused tests: 14 passed after correcting cross-cell weapon fragments. See [focused log](logs/final-focused.txt). Final-head CI checks the full suite.
- Two loader tests passed; loader source is unchanged.
- Final ordinary and fixture builds: `/tmp/nightman-polish-normal-v4` and `/tmp/nightman-polish-fixture-v4`. Fixture selectors are omitted from the ordinary package.

Final focused browser result: **2 passed** (all five raised ledges, both directional transfers, ads/sign/HUD, bat input, pause, 1280/1920/narrow states). See [browser log](logs/browser-polish.txt) and [gallery](gallery.md).

## Browser evidence and test boundaries

Browser runs use actual pygbag code under Chromium on the Pi, one browser at a time. Landings are verified from actual keyboard jumps and player foot/top coordinates. Dedicated platform fixtures remove enemies and position only the initial floor starting point; they do not place Dennis on a platform or alter physics. Normal-route regressions exercise combat/checkpoints/Cricket separately.

Early platform-driver attempts landed on the first ledge but failed the subsequent transfer/travel. Those failed runs are not acceptance evidence. Trace inspection identified a delayed key release walking the driver off the launch platform. Direction and jump are now dispatched together, launch footing is re-established, and geometry is isolated from combat. Live screenshot IPC often completes after the 220ms swing ends, so a clearly labeled paused-pose fixture captures the browser strike; supplemental actual-renderer sheets show every directional Dennis/Dayman pose and all four rat/ghoul frames. They are implementation renders, not concept mockups. Pause is verified through unchanged simulation snapshots.

## Reproduction

```sh
PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit tests/audio -q
npm run test:loader
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python tools/build_web.py --output /tmp/NEW-polish-fixture --test-fixtures
NIGHTMAN_BUILD=/tmp/NEW-polish-fixture NIGHTMAN_PORT=8778 NIGHTMAN_RESULTS=/tmp/NEW-results NIGHTMAN_EVIDENCE=/tmp/NEW-captures npx playwright test --project=chromium --grep POLISH
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python tools/capture_polish_frames.py /tmp/NEW-motion
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python tools/build_web.py --output /tmp/NEW-polish-normal
NIGHTMAN_BUILD=/tmp/NEW-polish-normal NIGHTMAN_PORT=8778 npx playwright test --project=chromium --grep ACT1_NORMAL
```

Use new output directories for builds. `NIGHTMAN_VIDEO=1` optionally records live browser video; screenshot and pose labels must not be mistaken for live animation timing. Existing CI also executes focused Chromium and ordinary Firefox workflows. Exact final-head results and independent review comments are on the linked PR, not inferred from this document.

## Release notes and boundaries

Lowered unreachable first ledges while preserving jump physics; moved their resident ghouls onto the new surfaces. Installed mounted Kitten Mittens/Wolf Cola artwork and painted Sherwin-Williams fascia. Replaced animal-covered bat art with wood and nails; added windup/strike/recovery poses and four-frame rats/ghouls tied to simulation time. Audio assets, combat damage, checkpoints, save semantics, story and Cricket encounter logic are unchanged.

Human visual acceptance remains outstanding. No new music approval, physical controller verification, full-game three-run acceptance, merge or deployment is claimed. This is Act1 polish, not delivery of the remaining two acts. Generated asset provenance and final prompt briefs are in [asset-prompts.md](asset-prompts.md) and assets/ui/polish-provenance.json. Provenance is not third-party distribution permission.
