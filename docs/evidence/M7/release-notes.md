# M7 development notes

Adds standard-mapped USB controller controls for desktop browser gameplay, menus, password entry and audio controls. Keyboard remains available. Disconnect/focus loss pauses safely; held buttons must be released before resuming or advancing a new scene. Unsupported/denied API gives keyboard fallback guidance. Fixes fast same-frame menu selection/confirmation.

No tested physical controller configuration yet. SNES-style/iBuffalo intent is not certification. Real USB, desktop/browser identification, OS focus and integrated listening evidence remain required; see [hardware checklist](hardware-checklist.md). Browser startup still needs one click. Touch input, remapping and rumble remain out of scope. No level, physics, story or audio asset changes. No merge, deployment or final-game acceptance.
