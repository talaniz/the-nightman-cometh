# M4 observed red/green record

Environment: Pi ARM64, Python3.11.2, pygame-ce2.5.8, pytest9.1.1 in
`/tmp/nightman-m2-tools`. Prefix all commands below with `PYTHONDONTWRITEBYTECODE=1`.
Use `python -m pytest -p no:cacheprovider` from the M4 worktree. The checked-in
[logs](logs/) retain actual assertion output from each observed red; all reds exited1. Trailing whitespace is normalized in the published logs; assertions and outcomes are unchanged.
Missing imports/syntax errors were not counted as meaningful behavior failures.

| Contract | Test command suffix | Observed red | Green verification |
|---|---|---|---|
| Opening/Act1 entry/art fingerprint | `tests/unit/test_act1_contract.py -q` |3fail: rehearsal dialogue, rehearsal world, unchanged art fingerprint |Same tests then13pass with world regression |
| Enemies/boss/retry | same |3fail: no creature types, no boss isolation, no boss reset |17pass with world regression |
| Save migration/completion | same |2fail: rehearsal coordinate retained, completion lost |13targeted/progress tests pass |
| Replay completed act | same |1fail: destructive new-run confirmation instead of replay |Full unit31pass |
| Missing/corrupt art | `tests/unit/test_act1_contract.py -k 'required_art or corrupt_art' -q` |2fail: no rejection |Full unit35pass |
| Chicken warning contact | `tests/unit/test_act1_contract.py -k chicken_warning -q` |Health2 before swoop |17Act1 tests pass |
| QA completion replay | `tests/unit/test_act1_contract.py -k qa_completion -q` |Ordinary replay menu from QA |Full unit37pass |
| Stunned Cricket contact | `tests/unit/test_act1_contract.py -k knocked_out -q` |Health2 touching knocked-out Cricket |Full unit38pass |
| Future-QA Title/Continue | `tests/unit/test_act1_contract.py -k title_from_future -q` |QA world not restored |Full unit39pass |
| Asset-root boundary | `tests/unit/test_act1_contract.py -k linked_art_root -q` |Symlink allowed outside-content packaging |Full unit42pass |

Additional direct collision and fixed-step checks cover actual stomp/beam windows,
one damage per stun cycle, safe retry, checkpoint healing, and30/60/120renderHz
simulation equivalence. A deterministic normal-input route finishes with bat/stomp
while avoiding the combined meal. These are simulation checks, not browser/human
acceptance. Real browser results, including failures and reruns, are recorded in
[execution](execution.md) and [the milestone ledger](../../../planning/M4-execution.md).
