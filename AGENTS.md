# Repository instructions

## Scope and authority

This repository is a planning-stage game. The current request authorizes a full implementation plan, GitHub repository setup/reuse, planning commits and a planning PR with independent reviews. It does NOT authorize implementing the game, composing audio, merging, deploying, or claiming final human acceptance. Later explicit milestone authorization covers its documented phases and reviews; do not repeatedly ask for already-granted authority.

Use the user's latest decisions and planning/specification.md. Conflicts must be surfaced rather than silently broadening scope. Recommendations are proposals until accepted by main within the authorized boundaries. Keep new unrelated ideas in deferred work.

Prioritize security, clean cohesive code, practical deployment readiness, and complete user experience. Prefer Python, pygame-ce and pygbag. Static browser build, no database or backend, no accounts, telemetry, real payments or online leaderboard. Desktop keyboard is initial scope; USB controller support is a dedicated milestone. Mobile touch is deferred. Do not introduce a framework migration, new services or unrelated features.

## Workflow and ownership

Use Spec Driven Development: ideate and build-author for planning; pre-dev-prep before authorized implementation; tdd for executable behavior; pr-author for draft PRs; merge-manager for coordinating acceptance (merge only if explicitly authorized); close-milestone only for explicitly completed milestone records.

Each named milestone uses one recorded branch/worktree and one PR across its build phases. Main owns implementation, scope, test evidence, reviewer finding triage and completion. No self-review sign-off. Preserve user files, prior mockups, Git history and unrelated work. Never force push or commit secrets. Use synthetic screenshots and fixtures.

Before each executable phase, record behavior, in-scope paths, failure cases, fixtures, exact commands, expected failing assertion and required screenshot/audio evidence in the milestone/PR. Observe meaningful failures before implementing, then run relevant green/regression checks. Documentation changes need documentary checks, not invented failing tests. Planned commands in planning/verification.md are future contracts until the corresponding tooling is delivered.

## Per-commit code review and per-PR independent E2E review

1. After creating the draft PR, assign a DISTINCT independent code-review agent to EACH new commit, including documentation and fix commits. Each inspects its assigned commit and the combined PR diff as context, checking correctness, regression risk, security, maintainability and scope. Record identity, assigned SHA, inspected final head and actionable findings or explicit sign-off in a GitHub PR comment.
2. Every new commit needs its own agent. Earlier reviewers revalidate effects on their reviewed work at the final head; each must explicitly record final-head sign-off. A distinct final integrator may inspect the combined diff but cannot substitute for per-commit agents or sign off on their behalf. Reviewer availability gaps block readiness. Reviewers inherit the session model policy; no model override is mandated.
3. Main assesses EACH recommendation against this file, the agreed specification and the milestone's path/behavior boundaries. Accept valid in-scope findings with reproductions, fixes and evidence. Explain invalid/out-of-scope decisions on the PR. Track legitimate deferred work without automatically implementing it. Blocking disagreements remain visible.
4. Only after code-review sign-off, assign a SEPARATE independent E2E reviewer for EACH PR, distinct from main and all its code reviewers. It must exercise actual workflows and relevant failure/recovery paths, inspect every required screenshot, and report exact head, commands, outcomes and limitations on the PR. Docs-only PRs use an explicitly labeled independent documentary acceptance review; they cannot claim game E2E.
5. Fixes during E2E return to code review with a new per-commit reviewer, followed by E2E revalidation. Any later commit invalidates previous final-head approvals until revalidated appropriately.
6. Reviews are comments unless an actual formal GitHub review exists. If a reviewer cannot post, main may relay its report verbatim with identity and exact SHA. Posting these task-related review comments/replies is authorized.
7. Resolve review threads only after fix evidence and reviewer confirmation. Missing tools, audio playback, browser access or USB hardware are gaps, never passes.
8. Mark draft PR ready only after all per-commit and E2E reviewers explicitly sign off on the exact final head, required checks pass, screenshots/audio evidence and release notes are complete. Perform the GitHub non-draft transition and verify isDraft=false before notification. Readiness never authorizes merge or deployment.

## UI evidence and headless inspection

For EVERY PR changing appearance or interaction, before review attach actual-branch screenshots to the PR or clearly linked evidence comment using durable reviewer-accessible URLs. Concept images are design references and NEVER implementation proof. Visually inspect all captures before publication; no private conversations, credentials or personal desktop content.

Capture desktop 1280x720 and 1920x1080, and a 390x844 narrow viewport for readable scaling/unsupported-device messaging, not mobile-playability acceptance. Include affected title/settings/password screens, dialogue, each changed level approach and boss, power-ups, checkpoint, damage/death/retry, loading/error and controller states as applicable. Record code revision, viewport, fixture, state and reproduction command in an evidence manifest. If only adding evidence in the same final commit, record the tested source-tree fingerprint and verify no game-source change after capture. E2E must visually inspect all attached captures and exercise interactions. Refresh changed states after fixes.

Use headless Chromium against the actual pygbag build for browser flow, console errors, asset failures, screenshots and recorded input. SDL dummy tests and unit tests do not replace browser execution. Mock Gamepad API tests do not replace real USB controller testing. Listening acceptance does not follow from waveform checks.

## Final acceptance

Before full game sign-off complete THREE start-to-finish playthroughs of the final candidate: keyboard normal route; keyboard failure/recovery route; physical USB controller route. No level-skip cheats or invincibility in qualifying runs. Record build/hash, device/browser, all three levels/bosses, opening/ending, music/SFX, deaths/checkpoints and findings. Same artifact across runs. Material user-visible bugs block acceptance. Fix then renew review and relevant checks; any game/runtime/asset change after the three runs requires all three qualifying runs on the new candidate.

Do not claim zero defects universally: report no material defects observed in the documented runs and list limitations. Main owns release sign-off; independent E2E reviewer must verify the run evidence and perform its own workflow review. Human music approval and actual USB evidence remain mandatory.

## Publication

Existing remote is https://github.com/talaniz/the-nightman-cometh (public). Do not change audience or settings without authorization. Only inspected, task-related artifacts are authorized for this planning PR. Deployment target, production hosting, third-party asset distribution permissions and final release approval must be resolved before public game deployment; do not claim the source repo grants any third-party rights.
