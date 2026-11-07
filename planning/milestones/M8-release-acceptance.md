# M8 — Final polish and release-candidate acceptance

Status: execution authorized by user after consolidated plan, including Cricket direction changes and realistic dumpsters. Base 43032c4c3253b49b97beac41da7997ae670e9914; branch milestone/m8-release-acceptance; worktree /home/palpatine/projects/the-nightman-cometh-m8. One PR. No merge or deployment authorization.

## Scope and acceptance

- Title: user-provided Nightman artwork, remove Reddit frame/margins, preserve composition; functional menus without duplicate labels.
- Animation: bat follows running hand and facing; nailed bat only; slightly larger animated rats with fair hitboxes; Cricket running poses, readable crash/stun/recovery; Shadynasty signs integrated into scenery.
- Approaches: target 25–35% longer, moderately harder, no empty padding/unreachable platforms/unavoidable damage. Bridge crew throw eggs; more telegraphed denim chickens; walking guns recoil and fire alcohol shots.
- Cricket: occasional mid-charge direction changes with a visible braking tell, bounded reversals so a dumpster crash and punish window always follow. No instant reversal into unavoidable contact. Realistic industrial dumpsters replace cylindrical crash cans; visible impact faces match crash coordinates. Preserve stun-only damage, pause/retry and no ordinary boss enemies.
- Frank: straight whole sandwiches then rapid four-piece meat/cheese/bread/lettuce burst; jump/bat/beam interception; clear tells and recovery.
- Nightman: hardest boss, back-and-forth running and karate, charged three-crucifix or two-chimichanga bursts; fair openings, capped existing ghoul summons. All bosses beatable without Dayman.
- First rescue Dee: “Don’t you ever leave me with that looney—I mean, my hero…I guess…”; Nightman abduction Dee: “I hate this storyyyy!!!!”.
- Finale: Dennis “I was a boy, now I am…”; same Superman pose/position/background in two stills. White flash + short sound, fade to original outfit, slow color washes for three seconds + single onset sound, second white flash + short sound, fade to Dayman outfit; “The Dayman!”. No continuously repeating effect sound.
- Charlie in suit before sunburst, all supplied proposal lyrics verbatim in manually advanced bubbles, approved instrumental only; then kneeling before skeptical Waitress. Waitress: “You said if I came to the show, you’d leave me alone. So, no….” Charlie thinks, shrugs: “So…see you tomorrow…?” Retain Dee “I told you no one writes a musical for no reason!” and Charlie hand-low “Dee, I’m right here right now…” / hand-high “…but I’m about to go here!”. Direct credits with approved Sunny theme; no extra end screen. Keyboard/controller and pointer story advance, no double advance.

## Phases and verification contracts

1. Story/presentation: game/scenes, session, render/art, input/main, relevant assets and tests. Exact dialogue/order, manual advance, replay/skip/completed-save, automatic effect timing and one-shot sound; screenshots all revised states and effect recording with audio. Red: finale order/credits route and new dialogue fail old behavior.
2. Animation/environment: game/render, art, relevant sprites/backgrounds/UI, collision if required. Fixed-position distinct poses, paused stability, facing/hand alignment; actual motion clips and screenshots. Red: missing motion/size/sign evidence; never substitute image existence for visual acceptance.
3. Encounters/difficulty: game/levels, world, relevant rendering/assets/tests. Telegraphed and bounded attacks, exact burst counts/directions/interception, route reachability, unpowered victories and retry reset. Red: Cricket currently never brakes/reverses mid-charge; later features get their own observed behavioral red before implementation.
4. Frozen candidate: build/package fingerprint, native/audio checks, actual Chromium/Firefox, cold/warm loading, focus/audio recovery, keyboard/controller regression. Three complete ordinary runs: keyboard normal, keyboard failure/recovery, physical USB. No skips/invincibility. Any runtime/game/asset fix resets all three runs.
5. Recorded handoff: additional complete final run with audible game music/SFX, inspect full video and sync; durable PR recording, screenshots, manifests, release notes. Exact-head per-commit code reviewers then separate independent E2E reviewer exercises implementation and inspects evidence. Main triages findings against AGENTS. Ready only with all final-head sign-offs/checks and verified non-draft state.

Baseline commands (existing tools, not claimed passes):
```
npm run test:loader
node --test tests/browser/gamepad.test.cjs
SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=dummy python -m pytest tests/unit tests/audio -q
python tools/build_web.py --output build/web --test-fixtures
npx playwright test --project=chromium --grep CONTROLLER
npx playwright test --project=chromium --grep-invert 'ACT1_NORMAL|CONTROLLER'
python tools/build_web.py --output build/normal
NIGHTMAN_BUILD=build/normal npx playwright test --project=chromium --grep ACT1_NORMAL
NIGHTMAN_BUILD=build/normal npx playwright test --project=firefox --grep 'SMOKE|ACT1_NORMAL'
```
Browser executables/environment follow existing CI. Extend focused assertions/routes as mechanics change, not to suppress product failures. Record exact commands, expected/observed red, green/regression outcomes and fixture details in docs/evidence/M8/execution.md before each phase. Screenshots: 1280x720, 1920x1080, 390x844 (scaling/unsupported device only); revision, viewport, state, command and source fingerprint recorded. Unit/dummy audio/mock pad checks are not browser/listening/physical evidence.

## Bounds and resources

Allowed: scoped game/assets changes above; tests/tools; planning spec/context/contracts; docs/evidence/M8; docs/releases; necessary build packaging/evidence configuration. No new songs/vocals, levels/story arcs, services, telemetry, databases, mobile touch, framework migration, unrelated rewrites or deployment. Preserve existing approved audio bytes and health/checkpoint/power-up behavior.

Heavy browser jobs remote where possible. Pi checks sequential/low priority; inspect temperature, RAM/swap/load before/during heavy work. Stop heavy jobs at 75C, observed throttling or sustained memory pressure. Missing sensors are evidence gaps. Full swap alone is a caution, not proof of current thrashing.

Physical USB full-run participation and actual listening remain mandatory; previous M7 responsiveness approval does not cover changed M8 content. Report no material defects observed with limitations, never universal zero defects. No final sign-off until qualifying evidence is complete.
