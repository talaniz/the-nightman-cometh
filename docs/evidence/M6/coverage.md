# M6 acceptance evidence map

This map locates planned/implemented checks; it is not a pass report. Results and limitations belong in execution.md and the PR. Screenshots alone do not prove interaction or motion.

| Contract | Evidence source |
| --- | --- |
| R1 progression/save/QA | test_act3_contract.py; test_progress.py; ACT3_SAVE; ordinary FULL_KEYBOARD routes |
| R2 reachable platforms/stage | native four-platform test; ACT3_APPROACH real keyboard landings; rooftop entrance/lower/upper captures |
| R3 approach animation/weapon | reused Act1 animation contracts; ACT3_APPROACH and full-route traversal; inspect rooftop enemy/weapon states |
| R4 health/meal/flags/retry | test_rooftop_flags_and_retry; existing world contracts; ACT3_APPROACH; FULL_KEYBOARD recovery |
| R5 mounted ads | rooftop entrance/poster desktop and narrow captures; visual exact-copy inspection |
| N1 poses/arena cleanup | test_entry_has_only_nightman_and_clears_attacks; NIGHTMAN_BOSS; live ACT3_MOTION frames |
| N2 warnings/recovery | test_boss_warning_recovery_and_summon_spacing; ACT3_MOTION; ordinary unpowered victory |
| N3 cap/safe spawn | test_summons_capped_and_safe; test_no_supported_spawn_position_defers; ACT3_MOTION live cap observation |
| N4 attacks/unpowered win | parametrized native boss/ghoul collision tests; NIGHTMAN_BOSS; native unpowered route; ordinary FULL_KEYBOARD |
| N5 cleanup/pause/defeat | native retry/victory/leave-scene tests; ACT3_APPROACH pause; FULL_KEYBOARD death/checkpoint route |
| N6 cue transitions | NIGHTMAN_BOSS expiry; approach/boss cue assertions; existing audio error/retry regression; human listening pending |
| F1/F2 exact finale | test_finale_contract.py; FINALE text assertions; all seven still captures and visual character/hand inspection |
| F3/F7 ending/music | FINALE proposal/rejection/ending/credits assertions; mute/retry/replay; unchanged audio hashes; human listening pending |
| F4 dialogue layout | existing layout unit tests; finale desktop/narrow captures; real Enter/Escape progression |
| F5 save/replay | native completed-save replay; FINALE; ordinary completed-save reload |
| F6 full journey | ordinary Chromium normal/recovery and Firefox FULL_KEYBOARD; no fixture mutation, password or invincibility |

Independent reviewers must identify gaps rather than equate a listed test with complete acceptance. M6 runs are exploratory; physical USB and all three final-candidate qualifying runs remain M7/M8.
