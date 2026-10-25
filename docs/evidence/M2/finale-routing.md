# M2 approved finale routing

User approved actual browser listening, with ending Dayman and silent credits.
Future original Sunny-style credits music is [deferred in issue #12](https://github.com/talaniz/the-nightman-cometh/issues/12).
This supersedes earlier pending-listening notes and the prior ending/credits map.
No recording, synthesis, gain, timing or game-story dialogue changed.

## Verification

- New real-manifest Director regression failed `None == 'dayman'` before the map
  correction; now all 8 director tests pass. Full audio suite: 96 passed (76.23s).
- Full production CLI export to a new directory reproduced every current master,
  Ogg and manifest byte. The only production asset difference from prior head is
  the ending/credits scene mapping; original approved audio is unchanged.
- Actual browser harness follows the full proposal, observes ending Dayman,
  selects credits, observes no busy music channel, retries and remains silent.
  Initial harness reload triggered a browser beforeunload warning; removed that
  unnecessary reload and used ordinary scene navigation, without filtering errors.
- Refreshed browser captures and manifest identify the tested build and source
  fingerprint. Includes ending and credits plus all prior affected audition states.
- Use http://127.0.0.1:8765 for listening. The literal localhost hostname triggers
  upstream pygbag development dependency routing; this is a documented restriction.

Source build: `/tmp/nightman-audition-ending-v2`. Commands:

```
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python -m pytest tests/audio -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python -m tools.audio.production --output /tmp/nightman-ending-export-v2
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python tools/audition.py --build /tmp/nightman-audition-ending-v2
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python tests/audio/browser_audition.py --build /tmp/nightman-audition-ending-v2 --evidence /tmp/nightman-ending-evidence-v3
```

Independent exact-head review must cover this change before readiness. No merge,
deployment, gameplay, physical USB or final-game acceptance is claimed.

Final browser rerun: eight workflow groups passed, ten screenshots captured and
visually inspected by main; no unexpected console/page/network errors. Captures
cover 1280x720, 1920x1080 and 390x844. No private content. Runtime source and asset
manifest were unchanged after capture; source fingerprint is in browser/manifest.json.
