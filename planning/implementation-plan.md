# Full implementation plan

Status: authorized planning, not implementation. All milestones below are pending. One branch/worktree and draft PR per milestone, phases committed separately when each provides a coherent reviewable result. EACH commit receives a distinct code reviewer; each PR receives a separate E2E reviewer after code sign-off. Do not merge automatically.

| Milestone | User-visible result | Build phases | Dependencies |
| --- | --- | --- | --- |
| M0 — Planning baseline | Agreed scope, phase contracts, repository and review gates | Specification; milestone plans; independent documentary reviews | Current task |
| [M1 — Music recognition previews](milestones/M1-music-previews.md) | Four recognizable short chiptune previews, Dayman first | 1.1 reference and Dayman proof; 1.2 other three previews and listening decisions | Approved M0 and explicit M1 authorization |
| [M2 — Music and sound production](milestones/M2-audio-production.md) | Approved loops/cues and coherent original effects | 2.1 soundtrack arrangements; 2.2 SFX and browser audio audition | User-approved M1 |
| [M3 — Browser foundation](milestones/M3-browser-foundation.md) | Playable keyboard training slice and complete shell | 3.1 reproducible build/real-browser harness; 3.2 movement/combat/health/flags; 3.3 menus/dialogue/audio/save/QA | M1 accepted; M2 artifacts before 3.3 audio sign-off |
| [M4 — Coffee-shop act](milestones/M4-coffee-shop.md) | Full first act, intro and Cricket | 4.1 production art + opening + approach; 4.2 boss and Frank transition | M2, M3 |
| [M5 — Underbridge act](milestones/M5-underbridge.md) | Crew, walking guns, Frank and Nightman abduction | 5.1 approach; 5.2 Frank battle and transition | M4 |
| [M6 — Rooftop and ending](milestones/M6-rooftop-ending.md) | Complete three-act keyboard game | 6.1 rooftop/summons/boss; 6.2 finale, full progression and credits | M5 |
| [M7 — USB controller sprint](milestones/M7-usb-controller.md) | Whole game works on physical USB pad | 7.1 Gamepad input and menus; 7.2 physical compatibility/recovery | M6 |
| [M8 — Release acceptance](milestones/M8-release-acceptance.md) | Reviewed release candidate with three completed runs | 8.1 polish/packaging/preflight; 8.2 final three playthroughs and independent acceptance | M1–M7 gates complete |

## Skill route and authority

Current: ideate → build-author → pr-author → independent documentary review.
Future authorized milestone: pre-dev-prep → tdd per executable phase → pr-author → per-commit code reviews → independent E2E → merge-manager readiness coordination. close-milestone only after explicit completion on main. Skills are workflow guidance, not blanket implementation/merge/deployment permission. Main evaluates reviewer recommendations against AGENTS.md and scope before acting.

Milestones proceed in order. M1 intentionally blocks substantial game production until the user recognizes the musical direction. M7 is a dedicated controller effort; no mobile substitution. Do not split UI and behavior across unrelated PRs. If a milestone becomes too large, revise the plan with reasons rather than silently fragmenting its recorded PR.

## Architecture direction

Keep simulation independent of rendering/audio and browser APIs: fixed-step deterministic game state, input actions, collisions/combat, scene/level definitions; pygame presentation; audio adapter; browser storage/Gamepad adapter. Pin tested pygame-ce/pygbag/tooling versions after an ARM64/Pi and browser spike. Avoid network at gameplay time beyond loading packaged runtime/assets; record runtime/CDN dependencies and supply failure/retry feedback. No assumption of offline support until tested.

Planned folders: game/ (main.py, state/input/combat/checkpoints/scenes/adapters), assets/ (sprites/backgrounds/UI/music/SFX and provenance), tests/unit/, tests/browser/, tools/ (build/evidence/audition), docs/evidence/, docs/releases/, planning/. These are boundaries and future artifacts, not existing implementation.

## Commit and review scheduling

Define the phase contract before code. Observe meaningful red → green. Attach required screenshot/audio artifacts before review. Prefer one phase commit; if extra fixes are needed each gets a new independent code reviewer. With four agent slots, queue reviewers sequentially as necessary; do not lower independence requirements to fit concurrency. E2E starts only when all required code-review verdicts agree on the final head. Main posts acceptance/rejection rationale and evidence for every finding. Only final-head sign-offs permit non-draft transition.

## Definition of full completion

M1 music approved by user; all phases implemented and checked; all required PR review gates satisfied; physical USB controller verified; three final full playthroughs complete; no unresolved material defects; final source/build and evidence hashes recorded. A docs PR or passing headless suite alone cannot meet this definition. Production deployment and merge still require separate instructions.
