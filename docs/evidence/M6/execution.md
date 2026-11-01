# M6 execution record

Authorized: both phases of planning/milestones/M6-rooftop-ending.md, confirmed by user approval. Base 9a0d57be05ae35d2850635e15e3a975956daa483; branch codex/m6-rooftop-ending; worktree /home/palpatine/projects/the-nightman-cometh-m6. Tracker issue #7 contains the approved contract (comment 6563491505).

## Implemented scope

Rooftop traversal, mounted ads, Nightman with telegraphed dash/leap and bounded summons, ordinary three-act progression/save recovery, exact proposal/rejection finale, Dayman ending and silent credits. Existing audio waveforms unchanged. New synthetic art provenance is in assets.json. No controller implementation, dependency upgrade, backend, deployment or merge.

## Observed verification

Pi: Python 3.11.2, pygame-ce 2.5.8, Node 22.23.2. Native commands used PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider.

- Initial progression/boss contracts: 11 failed, 1 passed; first green 12 passed. Initial missing-fixture KeyErrors are scaffolding errors, not behavior proof.
- Finale contracts: 3 failed before implementation; combined green 15 passed.
- Safe-spawn/scene-cleanup contracts: 2 failed, 23 passed before fixes.
- Full regression first exposed an editing indentation error (fixed), then two obsolete preview endpoint assertions (updated to real Act3 handoff): 2 failed, 203 passed. Focused green: 65 passed.
- Full tests/unit tests/audio: 206 passed in 319.46 seconds, before the final legacy menu-label fix.
- Legacy rehearsal save menu reproduced as 1 failed, 11 deselected. After fix: tests/unit/test_act3_contract.py tests/unit/test_finale_contract.py tests/unit/test_nightman_contract.py tests/unit/test_session.py tests/unit/test_progress.py: 34 passed in 2.73 seconds.
- npm run test:loader passed; audio validator reported no errors; assets/audio diff against base empty. JavaScript syntax checks and git diff --check passed.
- Fixture browser package built at /tmp/nightman-m6-fixture-r1 before final legacy-label/render alignment corrections; this build is NOT the final candidate.

Raw native red/green logs are in logs/. Native render previews were visually inspected locally but are NOT browser acceptance evidence. Actual Chromium/Firefox execution, final-source screenshots, independent per-commit code reviews and E2E review remain pending. CI will rebuild from the committed source; do not claim browser success from native tests.

## Release notes

Completes the playable rooftop act and Nightman encounter, followed by the user-authored finale. Existing completed bridge saves can continue to Act3. Completed rooftop saves reopen silent credits and allow ending replay. QA passwords remain isolated from normal saves. All six boss hits can be delivered without Dayman; spawned ghouls are capped at two and cleared on retry, victory and leaving gameplay.

## Gates at initial publication (superseded by results below)

Browser workflow evidence and visual inspection; durable screenshot manifest/gallery; exact-head independent reviews; user visual/listening acceptance. Real USB support remains M7 and the three same-artifact qualifying runs remain M8. No full-game or human acceptance claimed.

## Verified browser candidate, 2026-11-01

CI run 41349928401 at 7efc4bb0aae7d7af7df23a18ea0dd09ed3fedbc1 passed: 207 native tests (15.16s), loader/build checks, 25 focused Chromium tests (6.0m), two ordinary three-act Chromium keyboard routes (5.0m), four Firefox smoke/full-route checks (5.7m). Routes cover all three bosses, unpowered Nightman victory, deliberate death/checkpoint reload and completed-save credits. Aggregate automated timings include loading and test probes; they are not a measured human 10–15-minute play-length assessment.

Downloaded actual branch captures and inspected every image selected for gallery.md. Manifest records source fingerprint 52699acdd686ddac1d1bd21800ceae2c1c9d6f8dca958a1855d3e4c678c06618 and image hashes. No game/runtime/asset changes followed capture. Native previews were not published as browser evidence. CI environment is Ubuntu24.04/Python3.11.17 with pinned browser dependencies. Pi resource constraints are why browser acceptance uses CI; no local browser pass is claimed.

Independent exact-head code and E2E reviews and human visual/listening acceptance remain outstanding. This is not final-game release acceptance.
