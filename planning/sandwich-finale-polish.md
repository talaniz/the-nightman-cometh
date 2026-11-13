# Sandwich and finale polish

User authorized these two changes on 2026-11-11. Branch polish/sandwich-finale, worktree /home/palpatine/projects/the-nightman-cometh-final-polish, base e56bb99. Main owns implementation and review triage.

Acceptance: scored French bread; textured lettuce and meat; square yellow cheese, readable at game scale. Ingredient shots randomly choose top y366,382,398 and retain that height, speed, collision bounds and counters. Whole sandwich keeps current height; attack cadence/order unchanged. Charlie says “Well, technically I didn’t sign anything” then “So, I guess I’ll see you tomorrow?…” after refusal, before unchanged Dee/Charlie exchange and approved credits. Player-paced pages, existing instrumental only.

Scope: game/levels/act2.py, game/render.py, game/scenes/finale.py; relevant unit/browser tests and evidence. No music changes, unrelated mechanics, packaging, merge or deployment.

Verification: meaningful red for selected launch heights and exact closing dialogue; run nice -n10 /tmp/nightman-m2-tools/bin/python -m pytest tests/unit tests/audio -q. Browser checks exercise Frank attacks/counters and finale; capture actual branch at1280x720,1920x1080,390x844 and visually inspect. Remote Chromium/Firefox ordinary routes; independent per-commit code review then separate E2E. All final three-run/physical USB/audio-recording gates remain required on the new candidate; no claim of completion from unit tests. Pi guard75C/400MiB; no local heavy browser runs.

Observed red: 2 failed/8 passed, on fixed398 launch height and old dialogue. Initial broad regression found one further stale dialogue contract (256 passed/1 failed); updated it. Green:257 unit/audio tests passed in80.05s; subsequent expanded height/counter checks passed32 focused tests. JS syntax and diff whitespace checks passed. Native renderer contact sheet inspected: four distinct textured ingredients; this is not browser proof. Remote actual-browser evidence pending.

## Cat-food can addendum — authorized 2026-11-13
Replace the CAT text box with a small cylindrical metal can: visible oval lid/rim, shaded body/base and fish-skeleton label readable at gameplay scale. Shared renderer covers every act. Keep pickup positions, collection bounds, one-heart healing/cap, sound and taken-state removal unchanged. Scope game/render.py and focused browser/evidence only. This is a reversible visual edit: no artificial red pixel test; use existing food regression, actual-browser screenshots at1280x720/1920x1080/390x844 and collection check. Inspect captures then per-commit code review, prior-scope revalidation and independent E2E. Prior PR CI passed before this change; new runtime requires renewed candidate evidence.

Cat-food verification:10 existing world tests passed; guarded actual Chromium CAT_FOOD workflow passed after bounded-input driver correction. Main inspected all4 current captures and runtime fingerprint matched after capture. Full remote CI and reviewer revalidation pending.
