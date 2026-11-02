# Credits polish execution and release notes

Base: merged M6, 6b507797820a9893cb9f412438073f01dcaea0e2. User approved both standalone auditions, selected the 61-second credits version, then approved this polish phase. Contract: planning/milestones/credits-polish.md.

## Implemented outcome

The approved 61-second master plays once on credits, including completed-save Continue. Dayman remains on the ending screen. Rejection and the final spoken joke use a separate silent cue so the credits track does not start early. Replay, Title and skip remain immediately available. Small credits attribution added; no other art, physics or story changes. Existing approved music bytes are unchanged. This is a derived arrangement from the user's score, not an original composition or show recording.

Source master SHA256: 3ae10eb062973dbd4fb25ca535d3a0ce9fbc873080274e507f6b187e9b3d3259. Production export preserves that exact WAV hash; Ogg hash is in production/manifest.json. Source score/provenance accompanies the master. Production exporter reads and verifies approved bytes rather than resynthesizing an approximation. User hearing approval applies to the standalone audition; browser mix/transition listening remains separate.

## Observed native verification

Pi Python3.11.2, pygame-ce2.5.8, pinned existing environment /tmp/nightman-m2-tools. PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy used for pytest with -p no:cacheprovider.

- Meaningful red: 3 failed / 9 passed for missing credits cue and incorrect shared silent-dialogue scene (logs/routing-red.txt).
- Same routing/finale suite green: 12 passed (logs/routing-green.txt).
- Full tests/unit tests/audio: 209 passed (logs/native.txt).
- node --test tests/browser/boot-state.test.cjs passed; tools/check_audio.py --min-duration .02 --max-duration 120 assets/audio passed. Raw results in logs/.
- node --check affected browser scripts and git diff --check passed.
- Full audio production export completed in a fresh temporary directory. Only new credits files and corresponding cue metadata were copied into production; earlier assets were preserved.

## Pending browser/evidence gates

Remote CI will execute real pygbag Chromium/Firefox full journeys and focused recovery checks. FINALE additionally waits for the actual 61-second music channel to stop, exercises missing-audio recovery/mute and captures changed credits states in three viewports. Screenshot/gallery evidence, independent per-commit reviews and separate E2E must complete before readiness. No final human acceptance, M7 USB, M8 qualifying runs, merge or deployment claimed.
