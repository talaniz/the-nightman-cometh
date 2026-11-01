# M6 — Rooftop, Nightman and complete keyboard journey

Status: user approved both implementation phases on 2026-11-01; phase 6.1 underway.

## Authority and context

On 2026-11-01 the user requested refinement of acceptance criteria, verification contracts, scope and boundaries. The subsequent user reply "Approved" authorizes both refined implementation phases, production assets and their reviews. PR #19 is merged; fetched main is 9a0d57be05ae35d2850635e15e3a975956daa483. User reported reviewing M5 before merge; do not infer physical controller or final whole-game acceptance.

Repository: https://github.com/talaniz/the-nightman-cometh. Main owns branch `codex/m6-rooftop-ending`, worktree `/home/palpatine/projects/the-nightman-cometh-m6`, based on that merge. Local main was fast-forwarded; prior worktrees preserved. One branch and one PR across both implementation phases. No M6 PR or implementation commit yet. Pre-dev-prep verified this worktree and its two main-owned planning edits. Execute both phases without repeated phase permission requests. Merge, deployment and final human acceptance remain separate.

Specification precedence: latest user decisions and planning/specification.md. Correct the older M6/music-map sentence saying Dayman credits: Dayman belongs on the ending screen; credits are silent. New credits composition remains issue #12. Preserve approved audio files and existing first/second-act content.

## Outcome and scope

Deliver a complete three-act desktop-keyboard game from title through the rooftop boss, final joke, ending and credits. Reuse pygame-ce/pygbag, existing movement/combat/health, audio and save adapters. No new service or dependency by default. Prefer a cohesive Act3 implementation over copying an entire earlier act. Keep simulation, rendering and browser adapters separated.

Content paths: `game/levels/act3.py`, narrowly needed Nightman module, `game/scenes/`, `assets/backgrounds/act3/`, `assets/scenes/act3/`, `assets/sprites/`, `assets/ui/`, focused `tests/unit/` and `tests/browser/`, `docs/evidence/M6/`, relevant controls/release notes and `planning/`.

Integration paths: `game/session.py`, `game/progress.py`, `game/render.py`, `game/art.py`, `game/main.py`, `game/audio.py`, `game/fixtures.py`, `tools/build_web.py`, `.github/workflows/m3.yml`. Changes must serve Act3 selection, rendering, cue routing, stage-safe progression, credits, diagnostics or packaging. Shared `game/world.py` changes require a recorded reproduction, narrow rationale and Act1/Act2 regression contract before editing. Do not change global physics or redesign earlier levels to ease Act3 implementation.

Out of scope: USB input/hardware (M7), mobile controls, new modes, accounts/backend/database/telemetry, new music or edits to approved audio bytes, actor voices, global art redesign, unrelated issue fixes, public hosting or release. Final packaging/release clearance and three qualifying final runs remain M8. Remaining ads belong on the new rooftop set; avoid revisiting approved earlier-act layouts unless a specific regression requires it.

## Phase 6.1 — Rooftop traversal and Nightman

User outcome: beating Frank and advancing the existing abduction leads to an actual rooftop level and a fair, winnable Nightman fight.

| ID | Acceptance criterion |
| --- | --- |
| R1 | Played or skipped Nightman abduction enters Act3 exactly once. Existing completed Act2 saves can Continue into Act3. Existing Act1/Act2 saves and settings remain valid; stage-specific checkpoints cannot be mixed. NIGHTMAN loads actual Act3 with a visible QA label and cannot overwrite ordinary progress. |
| R2 | Philadelphia rooftops/fire escapes read as stage scenery: brick flats, skyline, visible set supports/lighting, curtains at act boundaries. Every intended platform is reachable with unchanged jump physics and visually agrees with its collision surface. Decorations cannot resemble required footholds. Camera and arena bounds never trap Dennis. |
| R3 | Approach uses established rats, green imp-like ghouls and occasional visibly telegraphed denim-chicken swoops. Preserve real animation and the nails-only Rat Bat attached through run/jump/swing, including left-facing and Dayman poses. No bridge crew or walking guns introduced here. |
| R4 | Three hearts. Cat food restores one. One plate of milksteak WITH jellybeans gives the existing 10-second Dayman transformation; one straight horizontal beam per shot. Midpoint and pre-boss flags heal one heart once, capped at three. Retry restores three hearts, clears Dayman/transient attacks, resets enemies and retains activated flags. Recrossing cannot farm healing. |
| R5 | Add physically mounted The Shotgun Shot ad and Dennis campaign poster with readable exact copy: REYNOLDS FOR COMPTROLLER / SOUTH PHILLY / ZONE 2 / DISTRICT 37. No invented campaign claims, plain text cards, obscured enemy telegraphs or blocked platforms. |
| N1 | Mac as Nightman has black costume/eye makeup and distinct idle, windup, dash/leap, recovery, summon and hit poses. Boss entry removes all ordinary approach enemies and projectiles. Only Nightman and his summoned green ghouls can remain hostile. |
| N2 | Dash/leap attacks have visible warning and recovery; no instantaneous teleport-contact attack or unavoidable arrival hit. Provisional starting tuning: six boss hits, at least 0.6 seconds attack warning and 0.6 seconds recovery, 0.75 seconds post-hit immunity. Record any tuning changes and observed reason; do not alter shared movement. |
| N3 | At most TWO summoned ghouls alive at once. Proposed summon spacing: at least six seconds; visible 0.6-second summon warning. Spawn only on supported ground at least 96 logical pixels from Dennis; defer if no safe position exists. Never spawn inside Dennis or a pit. No overlap of an active dash/leap with a summon windup. |
| N4 | Bat, descending stomp and a single beam damage Nightman; each kills summoned ghouls. Stomps bounce safely and one contact cannot consume multiple boss hits. Boss is beatable without Dayman; prove an ordinary unpowered keyboard victory. Transformation expiry cannot strand combat or leave beams firing while unpowered. |
| N5 | Summons and other transient attacks clean up on death, retry, leaving gameplay and victory. No carry-over damage in dialogue. Boss defeat happens once, records completion safely and hands off to the finale. Pause/blur freezes AI, cooldowns and transformation; blur releases held input. |
| N6 | Use approved rooftop and Nightman-boss cues. Dayman expiry restores the CURRENT scene cue, including boss entry. Pause/retry/mute/audio failure and recovery cannot duplicate players or block progress. |

Tuning values are proposed M6 defaults, not pre-existing user decisions. Small speed/cadence adjustments are allowed after approval within the safety bounds above; changing summon cap, attacks, health rules or scope requires an explicit contract revision. Measure overall play length against the provisional 10–15-minute target; do not pad or shorten prior acts merely to hit it.

Fixtures and expected behavior failures before implementation: missing Act3 interfaces may be scaffolded, but import errors alone do not count as red. Observe existing completed Act2 Continue still ending at the preview, NIGHTMAN still selecting rehearsal, Act3 checkpoint rejection, a third summon incorrectly allowed, unsafe spawn accepted, transient ghouls surviving retry, invalid attack damage/bounce, and missing victory-to-finale transition. Record actual assertion/command/exit, not hypothetical results.

## Phase 6.2 — Finale, credits and complete progression

User outcome: rescue Dee, watch the exact final joke, hear Dayman at the ending and reach silent credits with reliable replay/return controls.

| ID | Acceptance criterion |
| --- | --- |
| F1 | Final stills show rescued Dee/Dennis, then actual director Charlie interrupting to propose. Actual Waitress is visibly distinct from Dee playing her. Preserve gray suit/top hat/scruffy beard and natural eyes for Charlie; no added eyeliner. |
| F2 | Exact exchange order: actual Waitress, "I'm not going to marry you, Charlie." Charlie, "Well, see you tomorrow." Dee, "I told you no one writes a musical for no reason!" Charlie with hand low, "Dee, I'm right here right now"; next still/pose, hand high, "but I'm about to go here!" End. Do not omit, reorder or paraphrase these beats. |
| F3 | Use approved proposal cue during proposal; stop it when advancing to the rejection exchange, then Dayman on the ending screen, then silence upon entering credits. No automatic audition-track chaining. Proposal cue can finish if the player waits; dialogue remains player-advanced and can skip safely without waiting for music. Existing credits-music issue stays deferred. |
| F4 | Speech bubbles, speaker labels and punctuation fit at target sizes; no em-dash overlap, clipped lines or premature advance from a held confirm key. Curtains close at act end without covering readable final dialogue. |
| F5 | Completed-save Continue offers ending replay or a clear completed-game menu. Credits offer Title and Replay ending; new-game action retains the existing confirmation before resetting progress. Replay preserves saved progress and returns to its caller. Played/skipped finale converges to the same completed state. Reload after boss defeat cannot lose completion or softlock. |
| F6 | Title → all three approaches/bosses → finale → ending → credits → Title works on keyboard with no cheats or level skips. Mid-level death/retry, checkpoint reload, completed-save reload, pause/blur and dialogue replay work. QA completion remains isolated and clearly labeled; leaving QA restores ordinary progress. |
| F7 | Existing approved compositions remain byte-identical. Credits stay silent even after mute/unmute, audio retry, replay or reload. User checks actual in-game mix and transitions; cue-state assertions are not a listening pass. |

Failures to reproduce: wrong speaker identity/order, omitted see-you-tomorrow beat, Dayman continuing under credits, skip/replay awarding completion incorrectly, old completed Act2 saves stranded, completed Act3 save invalidated, stale scene cue after Dayman, and duplicate transition on held input.

## Verification contract

All new test filenames/selectors below are future deliverables, not current passing checks. Implement assertions before behavior, observe meaningful red, implement, then run focused green and justified regressions. Documentation-only planning uses document checks, not invented failing tests. Record exact Python/pygame/browser versions, command/exit, test names/counts, source/build hash, defects and fixes in `docs/evidence/M6/execution.md`.

Native commands (existing temporary environment must be revalidated before reuse):

```sh
PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit/test_act3_contract.py tests/unit/test_nightman_contract.py tests/unit/test_progress.py tests/unit/test_session.py -q
PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit/test_finale_contract.py tests/unit/test_dialogue_layout.py -q
PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy /tmp/nightman-m2-tools/bin/python -m pytest -p no:cacheprovider tests/unit tests/audio -q
npm run test:loader
/tmp/nightman-m2-tools/bin/python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio
git diff --exit-code 9a0d57be05ae35d2850635e15e3a975956daa483 -- assets/audio
git diff --check
```

Build with pinned requirements/package locks; no dependency upgrades by default. Use fresh output paths per round, never overwrite a candidate:

```sh
/tmp/nightman-m2-tools/bin/python tools/build_web.py --output /tmp/nightman-m6-fixture-r1 --test-fixtures
/tmp/nightman-m2-tools/bin/python tools/build_web.py --output /tmp/nightman-m6-normal-r1
NIGHTMAN_PORT=8796 NIGHTMAN_BUILD=/tmp/nightman-m6-fixture-r1 NIGHTMAN_RESULTS=/tmp/nightman-m6-focused-r1 NIGHTMAN_EVIDENCE=/tmp/nightman-m6-captures-r1 npx playwright test --project=chromium --trace off --grep 'ACT3_APPROACH|NIGHTMAN_BOSS|ACT3_SAVE|FINALE|ACT3_MOTION'
NIGHTMAN_PORT=8796 NIGHTMAN_BUILD=/tmp/nightman-m6-normal-r1 NIGHTMAN_RESULTS=/tmp/nightman-m6-normal-results-r1 NIGHTMAN_EVIDENCE=/tmp/nightman-m6-normal-captures-r1 npx playwright test --project=chromium --grep FULL_KEYBOARD
NIGHTMAN_PORT=8796 NIGHTMAN_BUILD=/tmp/nightman-m6-normal-r1 NIGHTMAN_RESULTS=/tmp/nightman-m6-firefox-results-r1 npx playwright test --project=firefox --grep 'SMOKE|FULL_KEYBOARD'
/tmp/nightman-m2-tools/bin/python tools/verify_evidence.py docs/evidence/M6/manifest.json
```

Check port availability first; serialize browser runs on Pi. Honor existing Playwright timeout defaults and declare any route-specific timeout before execution. Use state-based input waits and fixture acknowledgements, not arbitrary sleeps. New test-only fixtures: each platform/edge, midpoint/pre-boss, meal expiry, each boss attack and summon cap/safe spawn, boss retry/win, old-save migration, each finale frame and credits. Ordinary build must contain no fixture mutator; read-only diagnostics may observe it. FULL_KEYBOARD runs send real keyboard input and never inject completion/health or use passwords/invincibility.

Require fixture Chromium workflows and two ordinary full-game routes (normal and deliberate death/checkpoint-reload recovery), plus Firefox smoke/full-route coverage. Assert no unexpected console/page/asset errors; cover unavailable/corrupt/oversized/unknown-stage storage, audio unlock/failure/retry, pause/blur and completed-save recovery. Keep Act1/Act2 regression assertions; update their intentional endpoint expectations only. Ordinary routes must include unpowered Nightman victory. M6 full runs are exploratory regression evidence, NOT the three final M8 runs.

M5 exposed unreliable local Pi Chromium startup. Prefer a supported remote CI runner for full browser suites when needed; record that environment explicitly. Independent E2E may initiate its own remote run and inspect logs/artifacts, as in M5, but merely reading main's passing CI is insufficient. A failed local launch remains a limitation, not a pass; no indefinite retry loop or weakened assertions. Native dummy-video tests never substitute for real pygbag browser execution.

## Visual, audio and review evidence

Capture actual branch at 1280x720 and 1920x1080; 390x844 proves readable scaling/unsupported-touch guidance only. Gallery must cover rooftop entrance and every platform route, ads, enemy/Denim Chicken telegraphs, normal/Dayman swings, pickups/flags, damage/death/retry, all boss poses and live summon sequence, cap/safe positions, each attack contact, victory, every ending still, Dayman ending, silent credits, save/replay/menu and failure states affected by integration. Use live multi-frame sequences/video for motion and straight beam flight; held fixtures alone cannot prove animation. Inspect every image for correctness and private data before publishing durable exact-revision links with viewport/state/command metadata and hashes. Refresh after runtime/asset changes.

User hearing check: rooftop → boss; Dayman entry/expiry in each; pause/retry; proposal → rejection exchange → Dayman ending → silent credits. Preserve approved waveform bytes; no need to reapprove compositions. Record actual listening result separately from technical cue checks.

Main owns implementation, evidence and triage. After draft PR exists assign a DISTINCT independent code reviewer to EACH commit, including plan/fixes; each inspects assigned commit and combined context and explicitly revalidates final head. Only after all code sign-offs, a SEPARATE independent E2E reviewer exercises actual success/failure workflows and visually inspects every required screenshot. Reviewer requires real browser execution (local or independently invoked remote), access to final build/evidence and GitHub posting or attributed relay. No model override required. Main accepts findings only within AGENTS/spec/path boundaries; explain rejected/deferred findings on PR and track legitimate deferred work. Code fixes require new per-commit reviewer and renewed E2E. Missing capabilities are gaps, not passes.

Technical readiness: exact-head code/E2E sign-offs, all required checks, current screenshots/audio-routing evidence and release notes; then mark PR non-draft and verify. M6 completion additionally needs user visual/listening acceptance. Neither means final release: real USB remains M7; three same-artifact no-cheat full playthroughs remain M8. Do not claim bug-free, merged or deployed.

## Resumption

Both phases authorized and implemented locally. Native red/green evidence and release notes are in docs/evidence/M6/execution.md. Draft PR publication and actual-browser CI are next; screenshots and independent reviews remain pending. No merge or deployment authorized.
