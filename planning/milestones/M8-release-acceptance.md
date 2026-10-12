# M8 — Release candidate and three full playthroughs

Status: planned, not started. Dependency: M1–M7 complete; explicit M8 authorization; same final build available to reviewers and physical pad operator.

- Branch/worktree: reserve `milestone/m8-release-acceptance` at authorization; record actual base/head in context/PR. One PR across these phases.
- Allowed paths: game/ and assets/ ONLY for accepted in-scope defects, tests/, tools/, docs/evidence/M8/, docs/releases/, build packaging config
- Non-goals: everything outside specification and this milestone; no merge/deployment. Fixes to shared systems need an explicit in-scope rationale and regression contract.
- Review: a distinct code-review agent PER COMMIT (including fixes), complete combined-diff context and final-head revalidation; separate independent E2E reviewer per PR AFTER code sign-off. Main triages all recommendations against AGENTS.md and records acceptance/rejection/defer rationale on PR.
- Authority: plan only today; execute after explicit milestone authorization. Record user authorization and environment capability before phase 1.

## Phase 8.1 — Prepare a reviewable final candidate

**Deliverable:** Triage visual/audio/control/performance defects against AGENTS scope. Resolve straight-projectile and latest-ad requirements, packaging and runtime dependency handling, privacy/secrets scan, third-party asset provenance/release permissions. Produce pinned build, release notes/install/recovery/rollback instructions, evidence manifest.

**Acceptance and failure/recovery contract:** RC: all required tests pass, no missing assets/console errors, cold/warm load and audio unlock/recovery work, user-approved tracks hash-linked, supported browser smoke checks and actual screenshots complete. No unresolved material finding. Production deployment still unapproved.

**Verification / expected red:** Full unit, audio, build, headless browser, evidence and diff checks from verification.md; capture actual commands/results. Fixes each get distinct code reviewer; code sign-off before final E2E.

**Evidence:** Final screenshot set, packaged artifact hash and provenance, browser traces/performance observations, known minor limitations. Verify ready conditions without declaring final acceptance yet.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Phase 8.2 — Perform three qualifying complete runs and final review

**Deliverable:** Execute all three final runs exactly as verification.md: keyboard normal, independent keyboard recovery, physical USB. All on same candidate, no cheats/skips. Main investigates every recommendation within AGENTS boundaries; independent E2E evaluates runs plus its own real workflows and all screenshots.

**Acceptance and failure/recovery contract:** All three runs reach end title with story/music/three bosses; specified failure/recovery exercised; no unresolved material user-visible defects. Any game/runtime/asset fix resets three-run requirement on new candidate. User music acceptance and real hardware evidence cannot be waived.

**Verification / expected red:** Run log command or manual record for each route with build/hash and trace/video; final evidence checker, headless regression and audio checks as relevant. Docs-only edits may preserve runs with identical build hash and documentary revalidation.

**Evidence:** Exact final-head per-commit sign-offs, independent E2E sign-off, three run logs, final screenshots, checks and release notes. Transition PR non-draft and verify; report no material defects observed, not universal bug-free. Merge/deployment/final human acceptance separately authorized.

**Execution record (pending):** exact commands and versions; observed red assertion/exit; green and regression results; refactor rationale; commit SHA; assigned independent code reviewer; findings and main triage; final-head revalidation; E2E reviewer/result; evidence URLs. None run yet. Refactor only where it clarifies this phase's responsibilities, then rerun affected checks.

## Milestone gate

Attach required evidence and release notes before final review. Test actual user workflows; unit tests/source inspection alone do not satisfy E2E. Missing environment/hardware/audio access is explicit blocked evidence. Follow planning/verification.md for screenshot dimensions, artifact fingerprints and final-candidate rules. Mark PR ready only after exact-final-head review gates; no automatic merge. Next milestone starts only with applicable authorization and dependencies satisfied.
