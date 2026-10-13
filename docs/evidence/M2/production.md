# M2 production and browser evidence

Contract: [production contract](../../../planning/M2-production-contract.md).
Reproduction instructions: [production workflow](../../../tools/audio/PRODUCTION.md).
Prior six original compositions were explicitly approved by the user. New full
phrases, fast variant, loop boundaries, SFX and human browser hearing remain open.
This is technical audition delivery, not full milestone/game sign-off.

## Observed failures and fixes

- New production renderer: 7 semantic red tests (empty full output, missing
  duration/pitch behavior and invalid-speed rejection), then green.
- New director: 7 semantic red tests (unlock, stale scene restoration, pause,
  mute/voice cap, failure recovery, sting transition and invalid identifiers),
  then green.
- Validator duration window: short valid effect failed the old 15–30s constraint;
  explicit 0.02–120s opt-in passes, M1 defaults unchanged.
- Production boundary regression: final snap sample 130 rather than zero;
  a 5 ms export end ramp fixes it. Only new Troll production tail bytes changed;
  all approved M1/original masters are unchanged.
- Actual Chromium regression: after Enter, a music channel was busy but gain was
  zero. Test failed `unlocked music channel is silent`. SDL's fade behavior was
  replaced with explicit bounded channel-weight ramps; mute stays authoritative.
- Actual browser network/error check exposed the upstream missing BrowserFS
  script. A hash-verified official archived copy is served locally, with license.
  No runtime errors are hidden to manufacture a pass.

## Final checks

`PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m2-tools/bin/python -m pytest tests/audio -q -p no:cacheprovider`

**95 passed, 61.97 seconds**. Includes both full phrases' approved-prefix PCM,
existing M1 hash/PCM regressions, invalid/bounded scores, original effects,
real native SDL decoding of every Ogg, mute during fades and four effect voices.
Native SDL uses dummy audio; it is not counted as browser or hearing acceptance.

Actual CLI `python -m tools.audio.production --output /tmp/nightman-production-check`
reproduced all current WAV/Ogg bytes and manifest. A repeated export refused the
existing directory and preserved the manifest hash. All six original production
WAVs match their approved hashes exactly. `python tools/check_audio.py
--min-duration 0.02 --max-duration 120 assets/audio` passed for **36 WAV files**;
see [numeric report](production-validation.json). `git diff --check` passed.

Actual pygbag 0.9.3 build and Chromium 139.0.7258.66 run:

```
python tools/audition.py --build /tmp/nightman-audition-final
python tests/audio/browser_audition.py --build /tmp/nightman-audition-final --evidence docs/evidence/M2/browser
```

Seven browser workflow groups passed: user gesture/nonzero mixer gain; browser
blur and explicit resume; paused timer/mute/current-scene restoration; actual
missing Ogg file/retry; finite sting destination/manual skip; effect cap and both
volume-zero controls; desktop/narrow guidance. No unexpected console/page/network
errors. The SDK's explicit user-gesture-required notice is expected and excluded
by exact-purpose matching; no failed asset is excluded.

[Browser manifest](browser/manifest.json) records the tested app-source
fingerprint, build file hashes, browser/native runtime version strings, viewport
and state for each capture. All eight screenshots were opened and visually
inspected by main: clear controls/state feedback, no credentials/private content.
They show the actual pygame sound-check app, not concepts or the future game.

## Screenshots

- [Locked / 1280x720](browser/locked-1280.png)
- [Playing / 1280x720](browser/playing-1280.png)
- [Paused Dayman / 1280x720](browser/paused-1280.png)
- [Muted / 1280x720](browser/muted-1280.png)
- [Missing-file error / 1280x720](browser/asset-error-1280.png)
- [Recovered / 1280x720](browser/recovered-1280.png)
- [Desktop volume-zero / 1920x1080](browser/desktop-1920.png)
- [Readable desktop guidance / 390x844](browser/narrow-390.png)

## Limits and outstanding gates

No human hearing by the agent; runtime mixer observations and decoding do not
establish audible quality. No DuckTales reference audition/match claim. SDK CDN
connectivity remains needed. No gameplay, physical USB test, final playthrough,
merge or deployment. New per-commit review, prior final-head revalidation and
separate E2E review must cover this commit. M2 stays draft pending remaining
human listening/browser-hearing evidence. Final whole-game sign-off is reserved
by the user after the remaining milestones and three qualifying playthroughs.
