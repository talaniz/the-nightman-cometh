# M3 execution evidence

Approved contract: planning/milestones/M3-browser-foundation.md, GitHub issue #4.
Base: 65a05abec308e9d7b263a713c14daafa3cc8ee68. Main owns the M3 worktree/branch.
One milestone PR covers three coherent implementation phases; no merge/deployment.

## Observed red and corrections

- Shared JavaScript BootState: two failed assertions for timeout/error/retry and
  idempotent readiness, then both passed. An initial Python-only prototype was
  discarded before use: loader recovery must work before Python is available.
- CORE: five failed assertions for repeat checkpoint healing, paused Dayman timer,
  repeated contact damage, spread beams and side contact mistaken for stomp.
  Corrected deterministic simulation passed these and additional physics tests.
- Training projectile regression failed because no projectile was emitted; after
  adding a controlled rehearsal launcher, bat interception passes without damage.
- Progress: four failed tests for corrupt/unavailable storage, QA contamination,
  settings persistence and invalid version/schema, then all passed.
- Actual browser startup failed when a nested pygame import escaped pygbag's
  dependency scan. Explicit pygame import in the generated entrypoint fixed startup.
  This integration failure is distinct from the meaningful behavior reds above.
- Visual inspection found a square, distorted canvas and gray side background.
  Explicit 16:9 viewport sizing and background precedence corrected it; browser
  bounding-box assertions now protect aspect ratio.
- Combined pytest collection exposed duplicate test_preview module names; the new
  preview-server test was renamed. This collection error is not counted as a red.
- Concurrent Chromium/Firefox runs collided in Playwright's output directory;
  isolated output roots were added. Chromium on this Pi also attempted unavailable
  GPU access; software rendering is explicit. Invalid runs are not passes.

## Verification record

Final commands/results, source/build hashes and screenshots are recorded in the
manifest and PR once complete. Native tools currently use Python3.11.2,
pygame-ce2.5.8, pygbag0.9.3, NumPy1.26.4, pytest9.1.1, Node22.23.2 and
Playwright1.64.1. Runtime Python/pygame and browser versions are captured from
actual browser state. SDK startup requires Internet. No audio asset bytes changed.

All screenshots are synthetic gameplay/menus, never personal desktop photos.
Foundation artwork is code-native representative pixel art. No final act/boss or
controller acceptance is claimed. Integrated human browser hearing and feel remain
an explicit M3 gate; headless output cannot establish them.

### Candidate verification, 2026-10-25

- Native regression: `PYTHONDONTWRITEBYTECODE=1 SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit tests/audio -q`: **114 passed, 78.85s**.
- `npm run test:loader`: **2 passed**.
- Ordinary and fixture builds completed with `/tmp/nightman-m2-tools/bin/python tools/build_web.py --output <new-dir>` (add `--test-fixtures` for targeted fixtures). Both source fingerprints match manifest. Archive inspection confirmed the ordinary build has neither fixture marker nor mutation module.
- `NIGHTMAN_PORT=8776 NIGHTMAN_RESULTS=<isolated-results> NIGHTMAN_BUILD=<fixture-build> NIGHTMAN_EVIDENCE=<captures> npx playwright test --project=chromium`: **8 workflow groups passed, 6.9 minutes**. This run preceded the extra AUDIO SMOKE test; its separate result is below.
- Ordinary Chromium AUDIO SMOKE: **passed**, including mute, movement, restoration to little-boy. An ordinary Chromium cold smoke and Firefox audio smoke timed out during simultaneous browser runs. Firefox ordinary cold/menu/movement smoke passed. These failures are recorded; isolated reruns are pending, not claimed green.
- `python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio`: **no errors**. Approved recordings remain byte-identical to main.
- Preview lifecycle at temporary loopback port 8780: background readiness succeeded, a second root on the occupied port was rejected, and explicit stop succeeded. Ordinary candidate runs independently at port 8765 for human audition. No public binding or system boot service.
- `python tools/verify_evidence.py docs/evidence/M3/manifest.json` and `git diff --check`: passed for current source and captures.
- Browser runtime captured: Python 3.12.12, pygame-ce 2.5.7; native build versions differ as documented. Chromium 139.0.7258.66 and Playwright Firefox 157 are headless on Linux ARM64. Pi headless timing is not desktop performance/feel acceptance.

Full Chromium failure/recovery fixtures deliberately reject runtime/package requests, stall startup, disable storage and inject an actual missing audio load. Their asserted expected errors are not unexpected-error passes. Cold/normal/core/menu flows collect console, page and failed-request errors; only SDK pre-gesture MEDIA USER ACTION REQUIRED messages are excluded.

Independent code and E2E review, CI and human integrated hearing/feel are pending. The source fingerprint records tested game inputs before the evidence-only additions; screenshots are inspected synthetic content. No M3 completion, full-game acceptance, merge or deployment is claimed.

### Independent review corrections

Reviewer `/root/review_m3_f7aa558` found audio retry cleared Dayman music early while
world transformation remained active (PR review comment6403863316). Main accepted
this against CORE/SHELL boundaries. A regression requested remaining4.25/pausedTrue
and observed remaining0 before correction; the game recovery adapter now restores
world-owned transformation and pause state. M2 director/recordings remain unchanged.
Browser CORE now injects an audio failure while transformed and checks R recovery
to dayman-fast, followed by ordinary expiry to little-boy.

Main's visual check found the duplicate browser controls clipped beneath the canvas.
A real-build bounding-box regression failed with canvas bottom704 > controls top690.
Top anchoring corrects that overlap; no artwork or scope redesign. The regression
trace archive had an independent write error after the assertion; the assertion and
original screenshot establish the defect, not trace availability.

Initial ordinary browser startup/audio reruns subsequently passed in isolation:
Chromium BOOT smoke41.6s and Firefox AUDIO smoke48.2s. Combined browser launches
are avoided on this Pi; initial concurrent timeouts are retained above, not hidden.
These results apply to the first candidate. Updated-source verification follows.

### Corrected candidate results

- Native regression: **115 passed in70.92s**, same command/environment above.
- Updated Chromium capture run passed its first eight groups, including Dayman
  failure/retry and corrected footer bounds. The runner ended with SIGTERM143
  during the ninth AUDIO smoke; this is an **interrupted run, not a full-suite pass**.
  The stale owned test server was stopped. The eight completed groups and their
  captures remain valid observations; separate ordinary smoke results follow.
- Source fingerprint: `d4ceb84c6995d5a576bf12b7fc9ae958bc8d94ef4527fa5717471c5d16bd2576`.
  Test-fixture and ordinary builds were rebuilt and match it. All affected captures
  are refreshed. Runtime/audio source files are frozen after this build.
- First-commit GitHub CI completed successfully (run40237587893). This does not
  substitute for the new head's required CI run.

- Corrected ordinary build, Chromium `--grep SMOKE`: **2 passed in1.0minute**.
  Includes explicit airborne-jump assertion, menu/pause/scaling and mute/restoration.
- Corrected ordinary build, Firefox `--grep SMOKE`: **2 passed** (cold test37.9s,
  audio test32.2s). Browsers were serialized, with separate ports/results.
- `tools/verify_evidence.py docs/evidence/M3/manifest.json`: **33 refreshed captures
  verified**, including new Dayman retry state and ordinary jump/mute. Main visually
  inspected each capture; `git diff --check` passed. Approved audio/director diff
  against baseline remains empty.
- Reproduction: build with/without `--test-fixtures`; set `NIGHTMAN_BUILD` to the
  relevant output, `NIGHTMAN_RESULTS` to a fresh result directory and `NIGHTMAN_PORT`
  to an unused loopback port, then run commands above. Full CI and independent
  final-head review outcomes are recorded in PR13 after this fix commit. Human
  integrated hearing/feel remains pending; no milestone completion claimed.
