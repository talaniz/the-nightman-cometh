# M4 candidate verification

This is Act 1 implementation evidence, not full-game acceptance. The approved
[contract](../../../planning/milestones/M4-coffee-shop.md) and
[red/green record](red-green.md) define the boundaries. Main owns implementation
and finding triage; independent reviewers and user acceptance are separate gates.

## Candidate identity

- Branch `milestone/m4-coffee-shop`, based on merged M3 `1f97dd46a7479536d94c56567479ec73ce86fcd0`.
- Final source/art fingerprint: `674bf4acf595c3616a83fe56c49216a505e52cb2faed4148a8bdd84ecf175560`.
- Fixture build `/tmp/nightman-m4-review-fixture`; ordinary build `/tmp/nightman-m4-review-normal`.
- Both build manifests are preserved in [manifest.json](manifest.json). The normal APK excludes `game/fixtures.py` and `test-fixtures.json`; all six packaged art/provenance files were byte-compared with source. Required PNGs are decoded before packaging, and linked asset roots/files are rejected.
- No game/runtime/art changes after these builds. Tests, documentary results and captured evidence may be added to the same implementation commit. The source-tree fingerprint identifies the tested code independently of that commit's evidence files.

## Environment and reproduction

Pi4 ARM64; native Python3.11.2, pygame-ce2.5.8, pytest9.1.1; Node22,
Playwright1.64.1; Chromium139 and Playwright Firefox157. Browser WASM reports
Python3.12.12 and pygame-ce2.5.7. Python commands used the isolated existing
`/tmp/nightman-m2-tools/bin/python`; no project dependencies were upgraded.

Run browsers serially on the Pi. Each invocation sets `NIGHTMAN_PORT=8775`,
`NIGHTMAN_BUILD` to the appropriate build above, `NIGHTMAN_RESULTS` to a fresh
`/tmp/nightman-m4-review-results-<group>`, and `NIGHTMAN_EVIDENCE` to
`/tmp/nightman-m4-review-captures`. The preview server is started by Playwright.

| Check | Command | Actual result |
|---|---|---|
| Native gameplay/audio | `PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest -p no:cacheprovider tests/unit tests/audio -q` | Final source:138 passed in64.71s, exit0. |
| Loader | `npm run test:loader` | 2 passed |
| Approved audio | `python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio` | No errors. Approved audio and M2 mixer/director unchanged from M3. No new listening claim. |
| Act1 focused | `npx playwright test --project=chromium tests/browser/act1.spec.cjs --grep-invert ACT1_NORMAL` | Initial three groups passed in3.0m; focused BEAM/ad check passed in47.6s (exit0). |
| Startup | `npx playwright test --project=chromium tests/browser/game.spec.cjs --grep BOOT` | Five tests reported passed in3.2m. Parent batch later ended143 before the next group; this is not labelled a successful full-suite process exit. |
| Core/shell | `npx playwright test --project=chromium tests/browser/game.spec.cjs --grep 'CORE\|SHELL'` | 4 passed in3.5m, exit0 |
| Ordinary Chromium | `npx playwright test --project=chromium --grep 'SMOKE\|ACT1_NORMAL'` | 4 passed in6.4m, exit0. Later test-only driver strategy change awaits final-head CI/review revalidation. |
| Ordinary Firefox | `npx playwright test --project=firefox --grep 'SMOKE\|ACT1_NORMAL'` | First route failed after5 deaths. Corrected driver completed rescue with3 hearts, then post-rescue runtime reload timed out120s. No local Firefox suite pass claimed; desktop CI/review remains required. |
| Evidence | `python tools/verify_evidence.py docs/evidence/M4/manifest.json` | 57 screenshots verified against current source |

The ordinary ACT1_NORMAL journeys assert that mutation fixtures are absent and use
only keyboard controls with read-only observations. They advance every opening
still, traverse the approach, defeat Cricket, advance Frank's abduction, and reload
Continue at the safe end-of-preview screen. The recovery journey deliberately dies
at the boss, retries with3 hearts/no Dayman, reloads the pre-boss checkpoint, and
completes the same route. These are not the three qualifying full-game runs.

Focused checks cover exact story/audio routing; first/repeated flags; isolated
boss, stunned bat damage and no beam without transformation; legacy save migration;
malformed/disabled storage; QA save isolation; audio error/retry; blur and paused
timers; blocked SDK, missing package and stalled loading. Native checks additionally
exercise stomp/beam vulnerability, one-hit-per-stun, ordinary route without the meal,
30/60/120Hz equivalence, safe completion/replay and missing/corrupt/linked art.

## Evidence interpretation and limitations

[Gallery](screenshots.md) and [manifest](manifest.json) contain actual browser
captures at1280×720,1920×1080 and390×844. Each retained image is inspected before
publication. Capture records identify browser, build, test and state. Frozen pose
fixtures only establish rendering of brief animation/boss states; live collision
and ordinary-route tests establish interactions. Post-capture JSON can be later
than the displayed live frame. The narrow view checks unsupported-touch guidance.

The Firefox rerun is recorded in `logs/nightman-m4-firefox-route2.log`: it reached the complete screen with3 hearts, but restarting the runtime on the same page exceeded120s. No console error was observed in the completed trace. The cause is not established; do not treat it as a pass or claim it is fixed by a faster machine. Existing desktop Linux CI runs the same Firefox workflow, including reload, and its outcome must be assessed before readiness.

Headless Pi frame-time observations are recorded in capture JSON, not a universal
60FPS claim. Wall-clock automated route durations include IPC/screenshot overhead;
the map is4200 game units. Human desktop readability, boss feel and integrated
music/SFX acceptance remain mandatory. Browser audio state and waveform validation
do not establish what a person hears.

Earlier failures are preserved in the ledger: test-driver latency around pits and
stun captures, plus a real bug where knocked-out Cricket still damaged the player.
That contact bug was reproduced in a failing native test and corrected; stunned
and recovering contact is now safe. Further fixes preserve QA save isolation and
reject linked art roots. No earlier failing candidate is presented as final proof.

## Local human preview

The ordinary candidate is served only at Pi loopback `127.0.0.1:8767`; accepted M3
preview port8765 is preserved. HTTP200 and hashes of index/APK/package/loader/style
match the ordinary build manifest. On the desktop:

```sh
ssh -N -o ExitOnForwardFailure=yes -L 8767:127.0.0.1:8767 palpatine@deathstar
```

Keep that terminal open and visit `http://127.0.0.1:8767/`, click the startup button,
and choose Start Act1. Keyboard arrows/A,D move; Space jumps; J attacks; K fires
while Dayman; Enter advances; Escape pauses/skips; M mutes; R retries audio.
This loopback preview is not a public deployment.

## Gates still open

Final-head CI, per-commit independent code review, independent actual-browser E2E
and explicit user M4 art/play/audio acceptance. M4 merge and production deployment
are not authorized. Bridge/rooftop, physical USB and final full-game runs remain
later milestones. See [release notes](release-notes.md).
