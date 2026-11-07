# Desktop controls

Open the game in a desktop browser through the local preview/tunnel. Click **Enter the theatre** once to allow browser startup/audio, then press and release a controller button while the game has focus. The connection message appears below the game. Keyboard play remains available.

## USB controller (M7 hardware validation pending)

An SNES-style USB pad is the user's intended shape. The first implementation supports browsers reporting the **standard** mapping; an exact iBuffalo model/OS/browser has not yet been verified. A familiar shell does not guarantee a standard browser mapping. An unsupported device receives guidance and cannot send guessed controls. If the pad has a mode switch, select its documented standard-compatible mode; otherwise use keyboard and provide its model for scoped follow-up. Do not claim universal compatibility.

| Control | Gameplay | Menus/dialogue |
|---|---|---|
| D-pad / left stick | Move (30% stick deadzone) | Choose / adjust |
| Bottom face | Jump | Confirm / next |
| Left face | Rat Bat | — |
| Top face | Single sunbeam while Dayman | — |
| Right face | Pause | Back / skip dialogue |
| Start/Menu | Pause/resume | Resume only from pause |
| Left shoulder | Mute/unmute | Mute/unmute |
| Right shoulder | Retry audio | Retry audio |

Buttons use positional labels, not Xbox/SNES letters. Only one controller is selected at a time; the active slot remains stable. On disconnect or loss of focus, gameplay pauses and held actions are cleared. Reconnect, release all controls, then explicitly resume with Start or the menu. Keyboard Escape can resume without a pad. New scenes also require held controls to be released, avoiding accidental jumps/skips. Holding a menu direction does not auto-repeat; press again to advance.

Password: D-pad chooses a character, Bottom adds it. DEL removes the last character; GO submits. Keyboard typing, Backspace, Enter and Escape still work. Codes PAINTDOG/TROLLTOLL/NIGHTMAN remain explicit QA routes, separate from ordinary progress.

## Keyboard

Arrows or A/D move; Space jumps; J uses the bat; K fires a sunbeam; Enter confirms; Escape pauses/backs/skips dialogue. Arrows navigate menus; left/right adjusts volume. M mutes; R retries audio. Simultaneous opposite movement directions cancel. No repeat attacks or duplicate menu activation from holding a button.

## Compatibility and verification

No physical configuration is certified yet. Automated standard-pad snapshots are simulated tests, not proof of a USB device. Browser Gamepad exposure can require a controller gesture; see [MDN Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API). No device names or hardware identifiers are saved or transmitted by this adapter.

M7 physical checklist: record exact build fingerprint, pad model, OS/browser version, date/operator; demonstrate all menus/password/settings, movement/jump/bat/beam in three acts and bosses, death/checkpoint retry, pause/focus loss/unplug/replug, keyboard fallback, story/ending/credits and audio interaction. Attach attributable screen recording or timestamped results to the PR. Physical evidence is mandatory before readiness. M8's three final-candidate runs are a separate gate.
