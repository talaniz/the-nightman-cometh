# M5 — Bridge approach, Frank and Nightman abduction

Status: authorized for both implementation phases, including the additional Frank kidnapping still.
Dependency verified 2026-10-31: polish PR #18 merged as d27ca3e643dcacf7c511ceeb6ce50c9c10282f87.
Tracker: https://github.com/talaniz/the-nightman-cometh/issues/6

## Ownership and authorization

User said "let's proceed" in response to preparing M5's plan for implementation sign-off. User subsequently approved the contract with the additional Frank kidnapping screen. This authorizes both implementation phases, production assets and their reviews without repeated phase permission requests. Merge, deployment and final human acceptance remain separate.

Main owns branch codex/m5-underbridge and worktree /home/palpatine/projects/the-nightman-cometh-m5, based on the merge above. This replaces the earlier reserved branch name milestone/m5-underbridge. One branch/worktree and one draft PR across both phases. Prior worktrees remain untouched. Draft PR #19 contains both phases; issue #6 records the contract and user approval before implementation.

## Outcome and boundaries

A complete second act, naturally reached after Cricket and Frank's kidnapping scene, with underbridge traversal, Duncan/Z, walking guns, Frank's boss fight and Nightman's abduction. Retain the polished Act 1 art, reachable platforms, attached nailed bat and multi-frame animation standard.

Allowed content paths: game/levels/act2.py, cohesive bridge enemy/Frank modules if needed, game/scenes/, assets/backgrounds/act2/, assets/scenes/act2/, assets/sprites/, assets/ui/, relevant tests/, docs/evidence/M5/, planning/.
Necessary integration paths: game/session.py, game/progress.py, game/render.py, game/art.py, game/audio.py, game/main.py and game/fixtures.py only to select/render Act 2, route existing cues, save/restore stages and supply test-only diagnostic fixtures. tools/build_web.py and .github/workflows/m3.yml may package/require Act 2 assets and run its checks.
Shared world changes require a specific reproduction, narrow rationale and Act 1 regression contract recorded before the edit; no broad physics/combat rewrite. Keep modules cohesive instead of copying the whole Act 1 implementation.

No rooftop gameplay or Nightman boss, final proposal/credits implementation, USB support, mobile controls, new music composition, public hosting, backend/database, unrelated issue #16 fixes or global visual redesign. Preserve approved audio bytes. Existing documents saying "Dayman credits" are stale: latest user decision is Dayman ending and silent credits, deferred issue #12; M5 does not implement the finale.

## Phase 5.1 — Playable bridge approach and progression

User outcome: finish Act 1 or continue an existing completed Act 1 save, enter the bridge, fight through the crew/guns, and reach the pre-boss flag.

Acceptance:
- A1: Append a NEW still to Frank's kidnapping sequence: Frank runs off carrying Dee while Dennis shouts “Dee—er—Waitress! Stop getting kidnapped, you bird!” Keep this exact line and the earlier stills. Act 1 completion, kidnapping dialogue completion and skip all enter Act 2 exactly once. Replay dialogue returns to its caller without advancing progress. Existing completed Act 1 saves offer progression into Act 2, not a permanent old preview-end screen.
- A2: Underbridge scenery reads as theatrical Philadelphia: bridge structure, river/brick flats, stage details and curtains at act boundaries. Clear foreground footing and collision surfaces; every intended ledge reachable with existing jump physics. No sign or background silhouette mistaken for a usable platform.
- A3: Duncan and Z have distinct silhouettes and actual idle/movement/attack/hit poses. Walking guns visibly step, stop, telegraph and shoot in their facing direction with bounded cadence. Projectiles are avoidable, expire and clean up; no unavoidable spawn on Dennis.
- A4: Ordinary enemies die to descending stomp with bounce, bat or a single straight Dayman beam. Side contact damages Dennis under existing immunity rules. Frame animation does not alter combat timing; enemies cannot slide around as unchanged pictures.
- A5: Three hearts; cat food restores one. One milksteak-and-jellybeans plate triggers existing timed Dayman. Mid/pre-boss flags each restore one heart once, capped at three. Retry restores three hearts, clears transient attacks/Dayman and resets the encounter while retaining activated flags. No healing farm by recrossing.
- A6: Shadynasty's, Wolf Cola and Fight Milk appear as designed, physically mounted signs. Fight Milk features Mac/Charlie and "THE ONLY DRINK BY BODYGUARDS FOR BODYGUARDS". Distribute rather than crowd; preserve remaining ads for their planned locations. No random text cards, obscured enemies or platform blockage.
- A7: Troll Toll plays on approach; temporary Dayman returns to the correct current scene cue. Mute, audio failure, pause, blur and resume preserve playability and do not duplicate playback.
- A8: TROLLTOLL enters the actual Act 2 as visibly labeled QA, without overwriting ordinary saves. Ordinary Continue restores the correct act/checkpoint/settings. Validate save version, stage, flag IDs and coordinate combinations; malformed/unknown saves fail safely with feedback. Existing v1/v2 settings and valid Act 1 progress are preserved through migration.

Failures to cover: unknown stage, Act 1 coordinates supplied as Act 2 checkpoint, corrupt/oversized save, unavailable storage, retry after Dayman, repeated flag crossing, pause during gun windup, held input on blur, projectile cleanup, platform edge landings.

Expected meaningful red before implementation: advancing the existing Frank scene still selects complete instead of Act 2; Act 2 saves are rejected; TROLLTOLL loads rehearsal; new gun telegraph/cadence and reachable-platform assertions fail because behavior is absent. Missing modules are scaffolding failures, not sufficient behavioral red evidence: create minimal interfaces then observe the requested behavior fail.

## Phase 5.2 — Frank, abduction and a safe M5 endpoint

User outcome: beat Frank without needing a power-up, see Nightman steal Dee, and reach a clear resumable end of the current two-act build.

Acceptance:
- B1: Frank is squat/hunched with a pointed hooked nose, warm skin and brown/moss costume. Short forward/back shuffles while facing Dennis, visible throw windup and recovery inspired by Birdo. Distinct motion poses, not a sliding still.
- B2: Sandwiches/hoagies travel straight horizontally from release height; no arc or homing. Throw rhythm and spacing provide reaction time.
- B3: Bat, descending stomp and sunbeam each damage Frank and each destroy sandwiches. Frank is hittable during ordinary active combat, not only a pause/stun window. Brief hit immunity prevents accidental repeated damage from one contact. Stomping gives predictable bounce and cannot lock Dennis into repeated unavoidable damage.
- B4: Normal bat/stomp victory is possible without Dayman. Transformation expiry mid-fight is safe. Boss entry removes all crew, walking guns and their bullets; only Frank and his sandwiches remain hostile. Death/retry/win clears stale projectiles and restores a coherent fight.
- B5: Defeat triggers a player-advanced still sequence: Nightman jumps down, "Confound your lousy toll, troll", grabs Dee and runs; Dennis watches and Dee screams "Not again!" Preserve cast identity and speech bubbles. Played/skipped versions produce the same progression state; replay never duplicates rewards or advances progress.
- B6: Existing Frank boss cue and Nightman kidnapping cue switch correctly, including pause/retry/Dayman expiry. No audio composition changes.
- B7: M5 stops at an explicit end-of-current-preview screen with Title/Replay controls and saved Act 2 completion. It records a future rooftop handoff but does not launch a fake rooftop rehearsal, claim the full game is complete or trap the player. M6 will replace this bounded endpoint with the rooftop act.

Failures to cover: diagonal sandwich drift, damaged/destroyed object hit twice, sandwich surviving a valid attack, leaking bridge enemies/bullets, restart during a throw, dying during transformation, duplicate scene transition, skip/replay changing completion, reload after Act 2 completion.

Expected meaningful red: constant-Y projectile test fails under any gravity path; attack matrix (three attacks x Frank/sandwich) fails where collision handling is missing; arena-cleanup and transition equivalence assertions fail before integration.

## Verification contract

Commands below are future execution contracts, not results. New test files/selectors must be delivered before these commands can pass. Record exact interpreter/browser versions and commands in docs/evidence/M5/execution.md. Use the pinned requirements.lock and package-lock.json; verify temporary tool environments before reuse.

Phase 5.1 focused tests:
- PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit/test_act2_contract.py tests/unit/test_progress.py tests/unit/test_session.py -q
- Add cases for A1–A8; record the failing assertion, exit status and later green result.

Phase 5.2 focused tests:
- PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit/test_frank_contract.py tests/unit/test_act2_contract.py tests/unit/test_progress.py tests/unit/test_session.py -q

Regression and packaging:
- PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit tests/audio -q
- npm run test:loader
- /tmp/nightman-m2-tools/bin/python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio
- /tmp/nightman-m2-tools/bin/python tools/build_web.py --output /tmp/nightman-m5-fixture --test-fixtures
- /tmp/nightman-m2-tools/bin/python tools/build_web.py --output /tmp/nightman-m5-normal
- git diff --exit-code d27ca3e643dcacf7c511ceeb6ce50c9c10282f87 -- assets/audio
- git diff --check

Browser commands (one browser at a time on Pi; use fresh output paths per round):
- NIGHTMAN_BUILD=/tmp/nightman-m5-fixture NIGHTMAN_RESULTS=/tmp/nightman-m5-focused-results NIGHTMAN_EVIDENCE=/tmp/nightman-m5-captures npx playwright test --project=chromium --grep 'ACT2_APPROACH|FRANK|ACT2_STORY|ACT2_SAVE'
- NIGHTMAN_BUILD=/tmp/nightman-m5-normal NIGHTMAN_RESULTS=/tmp/nightman-m5-normal-results npx playwright test --project=chromium --grep 'ACT2_NORMAL'
- NIGHTMAN_BUILD=/tmp/nightman-m5-normal NIGHTMAN_RESULTS=/tmp/nightman-m5-firefox-results npx playwright test --project=firefox --grep 'SMOKE|ACT2_NORMAL'
- Existing fixture Chromium suite and ordinary ACT1_NORMAL Chromium/Firefox regressions stay in CI. Update old preview-ending expectations to the intentional Act 2 transition; do not weaken boss, save, error or ordinary-route assertions.

ACT2_NORMAL must cover (1) a new-game keyboard journey through both acts and Frank without QA, and (2) ordinary Act 2 checkpoint death/retry/reload and completed-save reload. Test Frank's unpowered route explicitly. Diagnostic fixtures may set starting positions/isolate actors for attack and motion checks, but must be absent from the ordinary build and cannot count as full-route acceptance.

On Pi, separate short screenshot capture runs from ordinary traversal to reduce browser load. Record trace settings and wall-clock allowances before execution. Timing failures remain failures with evidence; do not relabel them as environmental without diagnosis or remove outcome assertions to obtain a pass. Faster CI complements independent local review. No perpetual retry-until-green loop.

## Visual/audio evidence and review

Retain actual-branch screenshots at 1280x720 and 1920x1080, plus 390x844 scaling/unsupported-touch guidance. Cover bridge entrance, crew/gun poses, every platform route, signs, combined meal, Dayman shot, flags, damage/death/retry, pause, Frank windup/throw/all attack types/defeat, abduction stills, Continue/save recovery and end-of-preview controls; include affected loader/error/menu states.

Motion evidence must include live browser pose sequences or video: crew/gun movement, Dennis/Dayman directional swings, Frank shuffle/throw, straight sandwich flight and attack contacts. Static mockups or held-pose fixtures alone do not prove motion. Preserve nails-only HUD/held bat and hand attachment during running/jumping/swinging.

Inspect all captures for visual correctness and sensitive data before publication. Store images, viewport/state/reproduction metadata, build hashes and source fingerprint in docs/evidence/M5/, link durable exact-commit URLs from the PR. Verify using:
- /tmp/nightman-m2-tools/bin/python tools/verify_evidence.py docs/evidence/M5/manifest.json

User browser listening checks Troll Toll, Frank boss, Nightman abduction and Dayman return transitions; automated cue-state/WAV checks are not listening acceptance. No reapproval of unchanged compositions is needed, but actual in-game mix/transition defects must be addressed.

Distinct independent code-review agent per new commit, including plan/fixes; all revalidate final head. Only then a separate independent E2E reviewer exercises actual browser flows and all required screenshots. Main triages each finding against this scope/AGENTS, records fixes or justified deferrals on the PR. Missing tools/hardware/listening capabilities are gaps, not passes. CI, per-commit reviews, E2E, release notes/evidence and applicable user acceptance gates precede completion; verify non-draft state before reporting ready. No automatic merge.

## Current evidence / resumption

Both phases implemented in draft PR #19. CI run 41250831919 passed 179 native tests, 20 focused Chromium tests, two ordinary Chromium routes and four Firefox checks. See docs/evidence/M5/execution.md and manifest.json for actual results, screenshots and Pi limitations. Independent reviews and user in-game acceptance remain pending. USB hardware and three final full-game runs remain M7/M8.

### Accepted narrow shared change
Bridge guns must shoot toward either facing direction; World previously forced every shot left at 120px/s. projectile-red.txt reproduces x698 instead of x>700 for a rightward shot. Permit optional dx with legacy -120 default, keeping vertical position and all legacy collision/damage semantics. Run world/Act1 and full native/browser regressions.

Frank/sandwich collision rationale: the inherited 30x32 target rectangle does not match a 38x48 troll or a 30x16 sandwich. Add a target_rect hook with unchanged legacy default, overridden only by Act 2. The attack matrix exercises actual world collision paths; Act 1 regression coverage remains required. Initial matrix scaffolding KeyErrors are recorded but not counted as behavioral red proof; the arena, HP/immunity, throw and completion assertion failures establish meaningful boss red.
