# M7 physical USB checklist — NOT YET RUN

Status: pending actual hardware. Synthetic Gamepad tests do not satisfy this gate.
User intends an SNES-style USB pad (such as iBuffalo). Exact model, desktop OS and browser are not yet supplied. No compatibility result is claimed.

Record before testing:
- Operator and timestamp:
- Controller make/model and wired mode:
- Desktop OS and browser/version:
- Build source SHA and source fingerprint:
- Browser connection status (standard / unsupported / unavailable):
- Attributable screen recording or timestamped result evidence:

For each item record pass/fail, actual result and evidence/time marker:
1. Click Enter the theatre once; press and release a controller button. Connection guidance and controls readable; music audible after startup (or clearly explained mute/retry).
2. Title/Continue/new-game confirmation, Options volume, Back and dialogue replay usable without keyboard after startup.
3. D-pad movement; jump, bat and single Dayman beam; no drift or repeated actions on hold. Verify in all three acts and bosses. SNES pads without a stick do not need stick hardware checks.
4. Pause/resume, loss of focus, unplug while moving, reconnect with a button held: world remains paused, no stuck movement, release then explicit resume. Keyboard fallback also works.
5. Password picker: enter a bad code and correct it with DEL; submit each QA code; return to ordinary play without overwriting normal progress. QA is supplemental M7 coverage, not M8 qualifying play.
6. Damage/death/checkpoint retry, opening and all inter-act dialogue, final sequence, Dayman ending, musical credits, replay and return to title are usable.
7. Left shoulder mute/unmute and right shoulder audio retry work; music/effects volume adjustments remain available. Existing composition approval is separate from this integrated listening check.
8. Sustained play completes without controller dropouts, accidental skips or duplicate button actions. Record any defects and tested configuration limits.

If mapping is unsupported, stop hardware acceptance and report the exact model/browser/mode. Do not guess a mapping, certify the pad, or count keyboard completion as a USB pass. A device-specific addition would need its own bounded mapping evidence and review.

Independent E2E must inspect this completed evidence and perform its own browser workflow review. Missing fields/results block M7 readiness. M8 requires three later no-cheat complete runs on the same final candidate.

## Current ordinary preview candidate

Source: 60158d05ac9e5cc2f9e28c2a685230fa26d3a6b6
Source fingerprint: 62492865698748481014c549026982863ccf0abb31537809752d2b7030979450
Local build: /tmp/nightman-m7-normal-v4; loopback port8799. This is a development preview, not a deployment or accepted release. Refresh these identifiers after any runtime/asset change before recording hardware results.

From the desktop terminal:
```sh
ssh -N -o ExitOnForwardFailure=yes -L 8799:127.0.0.1:8799 palpatine@deathstar
```
Keep the terminal open and visit http://127.0.0.1:8799/ on that desktop. Connect the pad to the desktop, click Enter the theatre, then press/release a pad button. Browser status must report controller connected before testing. Record the exact OS/browser version and pad model; shell shape alone is insufficient.
