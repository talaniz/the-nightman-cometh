# The Nightman Cometh — desktop test packages

Private test candidate for the four invited testers. Not a signed/public release.

- Windows x64: extract the whole ZIP, keep the accompanying folders together, then
  open `NightmanCometh/NightmanCometh.exe`. Do not run the executable inside the ZIP.
- Apple Silicon Mac: use the arm64 package. Intel Mac: use x86_64. Extract and open
  `NightmanCometh.app`. The packages are not Developer ID signed or notarized.
  macOS may require explicit per-app approval in Privacy & Security after an attempted
  launch. Do not disable system-wide protections. Report any security warning before
  trying workarounds. No administrator privileges are needed by the game itself.
- No Python, browser, server or network connection is needed to play.

Keyboard: arrows/A,D move; Space jumps; J swings the bat; K fires a Dayman sunbeam;
Enter confirms; Escape pauses/backs out; M mutes; R retries audio. Story also advances
on a mouse click. Standard SDL-mapped USB controllers use the existing action layout.
Unknown layouts remain unsupported, with keyboard available. Unplugging an active pad
or switching away pauses the game. Release controls before resuming.

Saves and settings live outside the application:
- macOS: `~/Library/Application Support/NightmanCometh/progress.json`
- Windows: `%LOCALAPPDATA%\NightmanCometh\progress.json`

Keep the package build-manifest with feedback. Record OS/processor, controller model,
build SHA, steps to reproduce, expected versus actual result and screenshot/video.

Final acceptance checklist: ordinary start-to-credits run, all three levels/bosses,
opening/ending dialogue, music/effects, damage/death/checkpoint/retry and reconnect/focus.
No level-skip passwords or invincibility in qualifying runs. The physical controller
run is a separate mandatory gate; automated controller tests cannot replace it.

These instructions describe the intended package behavior. Successful CI installation
checks do not by themselves prove clean-machine GUI launch, listening or USB compatibility.
