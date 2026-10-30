# The Nightman Cometh

A Python/pygame browser platformer inspired by Charlie's musical: Philadelphia
painted as stage scenery, the Rat Bat, Dayman and three planned story acts.

M1–M3 are accepted and merged. The M4 candidate adds the full coffee-shop act:
Charlie's illustrated opening, staged Philadelphia approach, Cricket boss and
Frank's abduction. It ends explicitly before the bridge. M4 visual/play/audio
acceptance and independent review are still pending. Bridge/rooftop acts, USB
controllers and the final three full-game playthroughs remain later milestones.

## Build and preview

Use Python 3.11 and Node 22. Native dependencies are pinned in requirements.lock;
Node/browser tooling in package-lock.json. The browser SDK uses its own recorded
Python/pygame versions, not necessarily the host versions.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock
npm ci
python tools/build_web.py --output build/web
python tools/serve_preview.py --root build/web --port 8765 --background
```

Open **http://127.0.0.1:8765**, click **Enter the theatre**, then use the title menu.
Internet is required for the versioned pygame-web runtime. A localhost URL is
redirected to numeric loopback before runtime startup to avoid upstream developer
package routing. No backend, account or telemetry is used. This is a local preview,
not production hosting; no system boot service is installed.

From another computer, keep an SSH tunnel open:

```sh
ssh -N -o ExitOnForwardFailure=yes -L 8765:127.0.0.1:8765 palpatine@deathstar
```

Open the same numeric-loopback URL on that computer. Its browser plays the audio.
If an old preview is cached or the local port is already occupied, use a fresh local
port, for example `-L 8766:127.0.0.1:8765`, and open `http://127.0.0.1:8766`.
Stop the Pi preview with:

```sh
python tools/serve_preview.py --root build/web --port 8765 --stop
```

Build output must be a **new directory**; use a new versioned directory for a new
candidate and stop/start the preview with its matching root. Existing builds are
never silently overwritten. Use the prior directory to roll back a local preview.
The background preview reports readiness and an occupied port clearly.

## Controls

- Arrows or A/D: move. Space: jump. J: Rat Bat. K: sunbeam while Dayman.
- Enter: choose/advance. Escape: back, pause, or skip dialogue. M: mute.
- Options: arrows adjust separate music/effect volume. R: retry unavailable audio.
- PAINTDOG enters actual Act1 in QA. TROLLTOLL and NIGHTMAN enter clearly labelled
  rehearsal destinations for future acts. Pause provides QA controls and Exit QA.
  QA does not write ordinary progress. Mobile touch and controllers are not included.

Three hearts; cat food heals one. Milksteak with jellybeans transforms for ten
seconds. Flags heal once and set checkpoints. Death retries at the last flag with
three hearts; flag healing cannot be farmed. Progress/settings are stored only in
this browser origin. Storage failure permits in-memory play. Clear browser data
or use Start Act1 to begin fresh; New Game confirms before discarding a save.
Legacy rehearsal saves keep volumes and reset to the Act1 start with an explanation.
Completed Act1 can be replayed without erasing completion; Continue returns to the
safe end-of-preview screen until the next act is implemented.

## Verification

```sh
npm run test:loader
python -m pytest tests/unit tests/audio -q
python tools/build_web.py --output build/test-web --test-fixtures
NIGHTMAN_BUILD=build/test-web npx playwright test --project=chromium --grep-invert ACT1_NORMAL
python tools/build_web.py --output build/normal-web
NIGHTMAN_BUILD=build/normal-web npx playwright test --project=chromium --grep ACT1_NORMAL
NIGHTMAN_BUILD=build/normal-web npx playwright test --project=firefox --grep 'SMOKE|ACT1_NORMAL'
python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio
python tools/verify_evidence.py docs/evidence/M4/manifest.json
```

Chromium defaults to /usr/bin/chromium on the Pi. Override CHROMIUM_PATH for a
Playwright-installed browser; `npx playwright install chromium firefox` installs
the supported test versions. NIGHTMAN_PORT and NIGHTMAN_RESULTS isolate concurrent
runs. Use one browser worker on this Pi. Regular builds omit synthetic fixture
mutation support; the full CORE suite requires --test-fixtures. Screenshots must
identify that test build, and ordinary-build smoke coverage remains mandatory.

- [Specification](planning/specification.md)
- [Approved M4 contract](planning/milestones/M4-coffee-shop.md)
- [Milestones](planning/implementation-plan.md)
- [Verification and final playthroughs](planning/verification.md)
- [Concept references](planning/mockups/README.md)
- [Execution context](planning/context.md)
- [Review boundaries](AGENTS.md)

M4 remains subject to exact-head independent reviews and integrated human visual,
listening and gameplay acceptance. Passing automation alone is not final acceptance.
Merge and deployment require separate authorization.
