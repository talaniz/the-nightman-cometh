# Execution context

- Repository: https://github.com/talaniz/the-nightman-cometh (public).
- Specification: specification.md. Plan: implementation-plan.md. Active milestone: M1, phase 1.1, partial technical-tooling increment.
- Authorization: user on 2026-10-11: "Unless there are any additional questions, please proceed with the plan." This authorizes planned implementation cycles and their reviews, subject to documented dependencies and human listening/hardware acceptance. Do not repeatedly ask for implementation permission.
- Merge, deployment and final human acceptance remain separately gated.
- Main owns worktree /home/palpatine/projects/the-nightman-cometh-m1 and branch milestone/m1-music-previews.
- Recorded base: 342a4e54a5cd9ec87f44dd1881f520fa58f7e08d, reviewed planning branch plan/full-game-milestones. This is a stacked branch because planning PR #1 remains unmerged and merge is not authorized. M1 PR targets that planning branch; retarget only after verified planning merge ancestry.
- M1 issue: https://github.com/talaniz/the-nightman-cometh/issues/2. Per-milestone phase trackers exist for M1–M8 (issues #2–#9), 17 phases.
- Current contract: M1-phase-1.1-contract.md. Evidence: ../docs/evidence/M1/validation.md and ../docs/evidence/M1/source-reference.md.
- Python 3.11.2 / aarch64; FFmpeg available. Isolated temporary test/reference tools under /tmp/nightman-m1-tools. Runtime validator needs no third-party dependencies.
- Technical verification: 9 meaningful red cases, then 17 tests passed; review reproduced two RIFF regressions, followed by 19 tests passing after the fix; diff check passes. Independent review status and exact SHAs live in the milestone PR comments.
- Historical status before the 2026-10-12 workflow authorization: actual source listening/transcription, 15–30 second Dayman previews and user listening approval. Source file is available locally, but this session lacks audio-listening capability. No melody/composition or audition player delivered. Do not mark M1 complete, close its issue, or make its PR ready.
- Prior resumption point (superseded below): resolve listening/transcription capability, then finish phase 1.1. Do not expand to the other three motifs before Dayman approval or later game milestones before the documented music dependency.
- No production UI screenshots apply to this command-line increment. No game tests, physical USB tests or final playthroughs have run.

## Current resumption — 2026-10-12

User approved local transcription, synthesis and human listening iteration. Source was corrected to FX Dayman highlight VCvr6tzZPTU. Local Basic Pitch/ONNX, Demucs and CREPE run on the Pi; extraction is still musically uncertain. Dayman v1 is an explicitly unapproved 16-second probe (plain sine and chip lead, score and editable MIDI). See ../docs/evidence/M1/dayman-v1.md and ../assets/audio/manifest.json. No source audio/stems are committed.

39 tests pass; actual preview WAV checks pass. Await user recognition/correction and timbre feedback, not further implementation permission. Do not expand to other songs or mark M1 complete. PR #10 remains draft; all prior code reviewers must revalidate final head, a distinct reviewer handles this commit, and separate E2E review must check actual rendering/artifacts without claiming to have listened.


## Current resumption — approved preview integration

Latest user instruction: "Let’s build this sucker" after approving all four preview
melodies and the complete music cue map/finale. This explicitly authorizes continued
implementation of documented milestones in order; merge and deployment remain gated.
Dayman v1 was rejected. Dayman v2, Proposal v1, Little Baby Boy v1 and Troll Toll v2
have explicit human listening approval. Prior "await Dayman approval" paragraphs
are historical, superseded here. M1 integration contract: M1-integration-contract.md.
Reproduction preserves approved bytes; no further tune approval needed if hashes
remain identical. M2 expanded to three phases (original gap/boss compositions now
explicit). See music-cue-map.md. Existing worktree/branch/PR reused. No game exists yet.
No new review sign-off is implied; integrate and review this head before M1 readiness.


## Current resumption — M2 original-cue auditions

M1 is accepted at `001cc40559b9e4b0e9b9a99b738a79c22a0693d1`: all four code
reviewers and separate workflow reviewer signed off, PR #10 verified non-draft.
No merge performed. M1's commit-time pending status above is superseded.
Main owns `/home/palpatine/projects/the-nightman-cometh-m2`, branch
`milestone/m2-audio-production`, based on that exact M1 head. This is an intentional
stacked successor because merge remains unauthorized. M2 PR targets M1 branch.
Latest build authorization applies; no renewed implementation permission needed.
Original-cue auditions (phase 2.2) are brought forward before full production loop
work to collect human feedback. Contract: M2-original-preview-contract.md.
Six original cues rendered; 19 observed failures, then 69 audio tests pass; actual
CLI rerender/failure/recovery and WAV checks pass. M1 assets remain unchanged.
Human approval of six new cues is pending. Next: distinct per-commit review and
private Drive audition delivery; then remaining 2.1/2.2/2.3 work and final separate
M2 E2E/browser acceptance. No UI screenshots apply to this increment.


M2 PR: https://github.com/talaniz/the-nightman-cometh/pull/11 (draft). Six auditions
uploaded privately to Drive and metadata verified; human feedback requested.
First code review found a valid cue-end noise-snap boundary issue. Main accepted;
observed regression failed 130 != 0, then M2-only 5 ms end ramp fixed it. 70 audio
tests pass and all six actual CLI WAV hashes remain unchanged. New fix reviewer,
original reviewer revalidation and separate workflow review pending. Full M2
music production/browser/SFX/listening gates still outstanding.


## Current M2 production work
User approved all six original compositions and authorized the remaining M2 work.
Previous pending approval paragraphs are superseded. PR #11 remains on the same
branch/worktree; prior scoped code/workflow reviews passed at 82fbfd8. New contract:
M2-production-contract.md. Preserve approved WAV bytes; expanded phrases, faster
Dayman and SFX require new listening. Main implements; new per-commit review and
prior final-head revalidation follow. No merge/deploy authorization.


Production candidates and twelve effects now exist in assets/audio/production/.
Actual pygbag sound-check app and repeatable Chromium runner are implemented.
Native tools /tmp/nightman-m2-tools; actual browser candidate /tmp/nightman-audition-final.
New listening samples delivered privately through Drive; no private links in Git.
Current screenshots/manifest at docs/evidence/M2/browser; evidence includes source
fingerprint. Review gates must be renewed for the production commit. M2 remains
draft until new-audio human listening and browser-hearing gates are satisfied.


## M2 listening approval and finale adjustment (2026-10-25)
User approved the browser audition after using numeric loopback; earlier pending
listening statements are superseded. Ending now uses approved Dayman; credits
are silent. Original Sunny-style credits music deferred to GitHub issue #12.
No audio bytes changed. New routing regression failed before map correction.
Final exact-head reviews and refreshed browser evidence pending; no merge/deploy.

## M3 authorized execution
User approved the issue #4 foundation plan. Base main is
65a05abec308e9d7b263a713c14daafa3cc8ee68. Main owns branch
milestone/m3-browser-foundation in /home/palpatine/projects/the-nightman-cometh-m3.
All three phases authorized; one PR, independent per-commit reviews and separate
E2E required. No merge/deploy authority. No game implementation existed at start.
Phase 3.1 starts with loader/build/preview and training-room behavior tests; later
phases retain the accepted CORE/SHELL fixture contracts. Integrated human listening
and feel check remains a final M3 gate. M2 approvals and bytes are preserved.

M3 phase red evidence: actual shared JavaScript loader state failed two recovery
assertions before implementation; five CORE tests failed on repeat flags, paused
Dayman, repeated contact damage, spread beams and side/stomp confusion; four save
adapter tests failed on malformed/storage failure, QA writes, settings and schema.
The actual first pygbag boot failed: main wrapper lacked explicit pygame import,
so dependency scanning did not install pygame. Explicit entrypoint dependency fixed
it and Chromium boot/movement passed. No missing-module test counts as semantic red;
the packaging failure is separately recorded as browser integration evidence.
Node loader tests supplement, not replace, actual-browser failure tests.
.gitignore is included as necessary build hygiene for scoped generated outputs.

M3 candidate: 114 native tests and 2 loader tests pass; eight actual Chromium workflow groups pass. Ordinary build removes synthetic mutation support and serves loopback 8765. Evidence in docs/evidence/M3. Browser smoke reruns, CI, distinct per-commit review, independent E2E and integrated human hearing/feel remain pending. User was offered the existing SSH tunnel workflow. No merge/deployment authorized.

M3 delivery PR: https://github.com/talaniz/the-nightman-cometh/pull/13 (draft).
Initial commit f7aa558997e7b818b6c61afd97f4067dd49c52d2 reviewed by
/root/review_m3_f7aa558; one accepted in-scope audio retry finding, no other material
findings. Fix preserves game-owned Dayman/pause state and corrects clipped browser
controls. Native115 tests pass. Refresh/review results are recorded in
 docs/evidence/M3/execution.md and exact-head PR comments, which are the live review
ledger after this commit. Require a distinct fix-commit reviewer, original reviewer's
final-head revalidation, then separate E2E reviewer. Human hearing/feel pending.
Preview now uses /tmp/nightman-m3-fix-normal on loopback8765, explicitly stopped/
started with tools/serve_preview.py; existing SSH workflow applies. No merge or
public deployment authority; do not begin M4 from M3 approval.
