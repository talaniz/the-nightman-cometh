# M4 approval contract — Opening, coffee-shop act and Cricket

Status: approved by the user on 2026-10-25; implementation in progress. Verified main baseline: `1f97dd46a7479536d94c56567479ec73ce86fcd0` (M3 PR13 merged, issue4 closed). This contract refines the existing M4 milestone; latest user decisions override older planning boilerplate. M1/M2 music and M3 foundation are accepted; final art and complete game acceptance are not implied.

## Outcome and authority

Deliver one complete first act with production-intent pixel art, full opening stills/speech bubbles, playable staged Philadelphia route, Cricket boss, and Frank abduction. One branch/worktree `milestone/m4-coffee-shop` / `the-nightman-cometh-m4`, one PR across phases, created after approval. Preserve M3 worktrees and user files. Approval of this contract authorizes bounded M4 implementation, evidence, commits/pushes and reviews; not merge, public deployment, M5 or final-game sign-off.

## Scope and boundaries

- New Act1 level/enemy/boss definitions under `game/levels/`, still/dialogue definitions under `game/scenes/`, assets under `assets/sprites/`, `assets/backgrounds/act1/`, `assets/ui/`, `assets/scenes/act1/` and corresponding provenance records.
- Necessary integration in existing `game/world.py`, `session.py`, `render.py`, `main.py`, `progress.py`, `audio.py`, `fixtures.py`: configurable Act1 geometry/entities, scene progression, safe save migration, asset loading, approved-cue routing and isolated QA. Keep simulation separate from rendering/browser APIs. Extract small cohesive helpers within `game/` only where needed; no framework rewrite or speculative engine.
- `tools/build_web.py` and `tools/verify_evidence.py`: explicitly package approved artwork and include all shipped image/font/data bytes in source/build fingerprints. Missing required assets fail clearly; paths are bounded to known asset roots. Existing loopback preview retained. Browser loader changes only for demonstrated Act1 asset-load failure, with BOOT regression evidence.
- `tests/unit/`, `tests/browser/`, synthetic fixtures, existing test/build config and CI only as needed for Act1 checks. Include issue14 elapsed-aware timing observation where relevant, retaining exact simulation-duration assertions and real browser expiry checks.
- `planning/`, README, `docs/evidence/M4/`, release notes: approved contract, execution, provenance and evidence. Reconcile stale M3 status text when recording the new baseline, without rewriting earlier evidence.
- No bridge/rooftop gameplay, Frank combat, Nightman, full ending/credits, USB, touch, new audio compositions, modified approved recordings, backend/services, accounts, telemetry, hosting or unrelated cleanup. Do not use approved audio/source assets as evidence of distribution rights.

## Phase 4.1 — Finished opening and a playable Philadelphia approach

### Acceptance

ART-1: Replace representative art on M4 surfaces with aligned pixel-art sprites, animations, scenery and stills inspired by the supplied title and latest corrected concepts. Dennis wears green/dark pants; Dayman white/gold; director Charlie has gray suit/top hat and natural eyes; Dee has apron/blue skirt; dog Cricket has visible face paint. Green imp-like ghouls, ground rats and denim-shorts chicken remain visually distinct. HUD has a detailed RAT BAT portrait; held bat animates through idle/run/jump/swing. Scene colors and silhouettes remain readable at actual game size. Full portrait/art polish for later acts is deferred, except Frank's abduction cameo (warm skin, hooked nose, brown/moss robe).

STORY-1: Entry menu uses approved Dayman. Start plays Charlie/Dee introduction with approved Proposal music, in-story title card with Dayman, actors line and dumpster/kidnap/chase with Little Boy, then the approach. Initial menu and scripted title card are separate states; no return-to-menu loop. Use specification opening lines1–10 verbatim, including “For ye see”, emphasized “and words”, Dee's spoken “Sherwin William”, and Dennis's whispered “If I have to…”. Storefront reads Sherwin-Williams. Story stills show Cricket grabbing Dee and carrying her away, and Dennis watching them flee. No voice synthesis.

STORY-2: Enter advances, Escape skips the current story sequence to its correct destination, replay returns to its caller without changing progression. Held/repeated inputs do not duplicate scene entry or skip required state updates. Dialogue fits inside readable bubbles, with enough room for the longest line. Curtains open at stage start and close at stage end; they do not border active gameplay.

ACT1-1: A continuous alley/street-to-coffee-shop route with painted brick flats, Philadelphia skyline and visible stage construction. All platforms are reachable using existing movement. Ground rats, green ghouls and occasional denim chickens provide readable encounters; chicken entry is visibly telegraphed before a swoop and is sparse (one active chicken at a time). Enemy contact/foot-stomp/bat/beam rules preserve M3 behavior. No surprise off-camera contact or unavoidable damage at spawn/checkpoints. Stage route remains beatable with bat/stomp, without collecting Dayman.

ACT1-2: Three hearts, distinct cat-food +1 health and single combined milksteak/jellybeans pickup; Dayman initially remains10 seconds and fires single horizontal beams. Mid-route and pre-boss flags heal exactly one heart once, capped at3. Retry restores3 hearts, clears attacks/Dayman, resets encounter enemies and retains activated flags. Reload/retry cannot farm flag heals. Pause/blur freezes simulation and clears held controls. Measure route length rather than claiming the entire game's provisional10–15 minutes is achieved.

ADS-1: Place Kitten Mittens with actual Charlie and mittened cat, Wolf Cola and Shadynasty's on the Act1 route, readable without masking hazards or resembling pickups. Fight Milk, The Shotgun Shot and Reynolds campaign poster remain required later-act placements, not dropped. No invented Shadynasty's subtitle.

SAVE-1: Versioned, bounded Act1 saves validate known stage/checkpoint/flags/settings. Existing M3 rehearsal saves preserve valid volume settings but reset rehearsal-only progress to Act1 start with a one-time explanation; never interpret rehearsal coordinates as story progress. Malformed/unsupported/unavailable saves retain graceful in-memory play. Continue, new-game confirmation and replay behave predictably. PAINTDOG loads actual Act1 in explicitly labelled QA, with ordinary health/bat. Other passwords remain clearly labelled unavailable-act rehearsal destinations until their milestones. QA never changes ordinary stored progress, including Act1 completion.

### Expected red and checks

Before implementation observe meaningful failing assertions for opening order/skip equivalence; sprite/package missing-asset handling; rat/ghoul/chicken contacts and telegraph; map reachability and checkpoint lifecycle; M3-to-Act1 migration and QA save isolation. Missing imports/tooling alone are not a red. Preserve fixed-step30/60/120 equivalence tests for shared simulation changes. Visual mismatches require actual rendered captures and main/user inspection; unit tests cannot establish art quality.

## Phase 4.2 — Cricket battle and Frank's abduction

### Acceptance

CRICKET-1: Entering the coffee-shop boss arena removes approach rats/ghouls/chickens, their projectiles and spawn schedules. Arena contains player, Dee, Cricket and props only. No ordinary-enemy spawn resumes during battle or retry.

CRICKET-2: Cricket visibly telegraphs, charges back and forth, crashes into a garbage can, becomes stunned, accepts damage, then recovers. Dodge/jump timing must permit avoiding each charge. Bat, descending foot-stomp and Dayman beam damage him only during the stun window; repeated overlap of a single attack cannot consume multiple health units. Bat/stomp alone can finish the boss. Baseline tuning proposal:3 successful stun-window hits, at least0.5s charge telegraph and1.5s stun; adjust within this encounter only after measured playability, documenting changes. No compulsory timed Dayman collection.

CRICKET-3: Death/retry resets boss/props and transient attacks at the pre-boss flag; pause/blur and audio failure do not freeze progression permanently. Defeat triggers exactly one rescue/transition, never duplicate rewards or scenes. Skip and replay do not skip victory requirements or rewrite ordinary completion.

TRANSITION-1: Frank kidnaps Dee in stills, using the approved Frank transition cue. Proposed short original dialogue: Dee: “Finally. Can we leave?” Frank, grabbing Dee: “Not so fast. You gotta pay the troll toll.” Dennis, watching them go: “Seriously? We just did this.” This short script is a proposal in this approval contract, not previously approved dialogue. End on an explicit “Act 1 complete — Under the bridge comes next” preview screen with replay/title options. Persist Act1 completion/next-act unlock without attempting to load unfinished Act2 or falsely claiming it exists. Continue after completion returns to this safe endpoint; replay Act1 is available without erasing completion unintentionally.

AUDIO-1: Reuse approved Little Boy approach, original Cricket boss cue and Frank abduction cue with correct scene transitions, no duplicate playback and independent music/SFX levels. Jump/stomp/bat/damage/pickup/flag/beam/can impact/defeat use existing approved effects as applicable. Do not silently substitute generic music. Audio failure remains recoverable while gameplay continues. Ending Dayman/silent credits policy remains unchanged and outside this act.

### Expected red and checks

Observe failures for unstunned damage, attack multi-hit, approach enemies leaking into arena, lost retry reset, double defeat/transition and unfinished-act loading. Exercise each boss state and all three attack methods in focused fixtures; complete one ordinary start-to-Frank keyboard route without skips/QA/invincibility and a separate death/checkpoint/reload recovery route. These are Act1 acceptance runs, not any of the three final full-game runs.

## Verification contract across phases

The following new Act1 tests are planned tooling, not already passing results. Record exact commands, fixture IDs, failing assertion/exit and green outcomes per phase. Use fresh build/results paths; preserve the currently accepted preview until a new candidate is verified.

- `PYTHONDONTWRITEBYTECODE=1 SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=dummy python -m pytest -p no:cacheprovider tests/unit tests/audio -q`
- `npm run test:loader`
- `python tools/build_web.py --output /tmp/nightman-m4-fixture-<revision> --test-fixtures`
- `NIGHTMAN_BUILD=/tmp/nightman-m4-fixture-<revision> NIGHTMAN_RESULTS=/tmp/nightman-m4-chromium-<revision> npx playwright test --project=chromium` — existing BOOT/CORE/SHELL plus new ACT1/STORY/CRICKET/SAVE groups. Slow-Pi runs may be serialized into documented groups; do not label an interrupted full run passed.
- `python tools/build_web.py --output /tmp/nightman-m4-normal-<revision>`
- Ordinary-build Chromium and Firefox: set corresponding NIGHTMAN_BUILD and fresh NIGHTMAN_RESULTS, run `npx playwright test --project=chromium --grep ACT1_NORMAL` and `npx playwright test --project=firefox --grep 'SMOKE|ACT1_NORMAL'`. ACT1_NORMAL uses actual keyboard inputs and read-only observations, no mutation fixtures, passwords, invincibility or level skips. Run one browser at a time on the Pi.
- `python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio`; compare approved audio bytes against merged M3 baseline.
- `python tools/verify_evidence.py docs/evidence/M4/manifest.json`; `git diff --check`.
- Include missing/corrupt image data, rejected runtime/package requests, long loading, malformed/migrated/disabled storage, held inputs on blur, dialogue/replay, death during encounters, failed audio/retry and continued normal-save isolation. Deliberate failures must be distinguished from unexpected console/page/network errors.
- Evidence captures at1280x720 and1920x1080 plus390x844 narrow guidance: title/opening/long bubble/skip/replay, dumpster/grab/chase, approach/platforms/enemies/chicken cue, ads, bat/Dayman/food, first/repeated flags, boss telegraph/charge/can crash/stun/hit/defeat, damage/death/retry, Frank abduction/end-of-preview, loading/error and save migration/failure feedback. Every capture has viewport/state/fixture/reproduction and tested source/art/build fingerprint. Human-inspected durable URLs on PR before review; concept mockups are not implementation evidence.
- Record actual headless performance on the Pi and do a user desktop visual/readability, boss-feel and integrated music/SFX check before M4 completion. No claim of universal60FPS or hearing acceptance from automated state checks.

## Review and sign-off protocol

Main owns implementation and acceptance. Distinct independent reviewer for EACH commit, including art/docs/fixes; each inspects assigned commit and combined diff and signs the exact final head. Main accepts/rejects/defers each recommendation against AGENTS.md and this contract with reasons/evidence. After all code sign-offs, a separate E2E reviewer exercises actual browser normal/failure routes and visually opens all required screenshots. New fixes require new per-commit review and final-head revalidation before renewed E2E sign-off. Missing environment or evidence remains a gap, not a pass.

Ready only with passing final-head CI, all final-head independent sign-offs, asset/evidence provenance, release notes and explicit user art/play/audio acceptance. Verify GitHub non-draft state. Merge requires a separate user instruction. USB and the three final full-game playthroughs remain M7/M8.

## Approved decision

The user approved M4 phases4.1–4.2 with these expanded integration paths, safe rehearsal-save migration, menu versus scripted-title sequence, production-intent Act1 art, proposed short Frank transition, tunable Cricket defaults and explicit end-of-preview boundary. Execution: record this contract in `planning/milestones/M4-coffee-shop.md`, prepare the single M4 branch/worktree from verified main and begin phase4.1. Implementation is underway; see planning/M4-execution.md.
