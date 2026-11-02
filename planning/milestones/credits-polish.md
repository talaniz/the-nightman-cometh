# Focused credits and journey polish

Authorized: user approved the recommended focused polish phase after approving the 61-second Sunny credits audition. Base main 6b507797820a9893cb9f412438073f01dcaea0e2 (merged PR20). Main owns branch codex/credits-polish and worktree /home/palpatine/projects/the-nightman-cometh-credits-polish. One PR. This phase precedes M7 and does not implement USB or claim M8 final acceptance.

## Acceptance criteria and boundaries

1. Credits plays the exact approved 61-second master (SHA256 3ae10eb062973dbd4fb25ca535d3a0ce9fbc873080274e507f6b187e9b3d3259), exported to browser Ogg. Once per visit, finite ending; no forced wait to navigate. No new arrangement or change to existing approved music.
2. Proposal remains under its two stills; rejection and the closing spoken joke remain silent via an explicit dialogue-silence scene. Dayman remains on the ending screen. Credits track starts only on credits, including completed-save Continue. Replay/title navigation replaces the old cue cleanly.
3. Mute/unmute, music volume, pause/blur, audio failure/retry and replay preserve responsiveness and one active music player after transitions. Natural 61-second completion leaves the credits menu usable and stops playback; R intentionally restarts the current cue. No audition chaining in gameplay.
4. Add readable music attribution to credits. Preserve exact story wording, art, physics, health/checkpoints and enemy behavior. Inspect the complete three-act browser journey and actual screenshots; address only concrete reproducible in-scope regressions. No speculative redesign.
5. Preserve source provenance/approval and reproduce the approved bytes. Keep current documentation and contracts consistent with music replacing silence. Old evidence remains historical, not evidence for this new runtime.

Paths: assets/audio/sources and production (new credits files/manifest only), tools/audio/production.py, game/scenes/finale.py, game/render.py, affected tests/audio/unit/browser, README and relevant planning/evidence. Narrow additional integration changes require a reproduced defect and documented rationale. No backend/dependency changes, public deployment, merge, controller work, new compositions or final-game acceptance.

## Verification contract before implementation

Expected red: production credits currently resolves to None, and final spoken stills currently share that scene; require sunny-credits on credits but None for every rejection/joke still. Observe assertion failures in tests/audio/test_director.py and tests/unit/test_finale_contract.py before changing runtime. Verify the pinned master hash and finite loop metadata after asset integration. Tests for missing assets use existing audio-error fixture; no real missing production files.

Commands (Python is /tmp/nightman-m2-tools/bin/python, pinned requirements.lock):
- PYTHONDONTWRITEBYTECODE=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python -m pytest -p no:cacheprovider tests/audio/test_director.py tests/unit/test_finale_contract.py -q (red then green).
- Full tests/unit tests/audio; npm run test:loader; tools/check_audio.py --min-duration .02 --max-duration 120 assets/audio; node --check affected browser drivers; git diff --check.
- Fresh tools/build_web.py fixture and ordinary builds. Remote CI Chromium focused suite, two ordinary full-three-act keyboard routes and Firefox smoke/full routes. Existing workflow is used because Pi browser resource constraints persist.
- FINALE focused browser checks: actual decoder/mixer active, silence during joke, Dayman ending, credits track, failure/retry, mute, finite stop after 61 seconds, replay and completed-save reload. Keep strict no-cheat ordinary routes.
- Actual branch captures: finale/rejection, ending, credits at 1280x720/1920x1080, narrow 390x844 guidance; credits audio error/recovery/mute/finished/replay. Inspect full-journey screenshots for concrete polish defects. Commit selected screenshots with revision/source fingerprint, states, commands and hashes before review. Screenshots do not prove hearing.

Distinct independent reviewer per commit, final-head revalidation from all; separate independent E2E reviewer after code sign-off. Both post exact SHA on PR. E2E exercises actual browser workflows (reviewer-initiated remote run allowed), opens all attached screenshots, and distinguishes user-approved composition from pending integrated hearing. Mark non-draft only after checks/reviews/evidence; no merge. Human integrated hearing remains a separate handoff, not an invented listening pass. M7 physical USB and M8 three same-artifact runs remain future milestones.
