# Independent native interaction evidence

Runtime source: `e7cfee7e7c3f5d5e8797f68a8cc9e5dc8af4560a`.
Reviewer: `/root/desktop_e2e`; [exact-head report](https://github.com/talaniz/the-nightman-cometh/pull/25#issuecomment-6886313015).
Actual Linux native event loop, pygame-ce2.5.8, SDL dummy video/audio, synthetic keyboard
and focus events. This is not physical controller, target-OS GUI or listening acceptance.

Reviewer exercised settings persistence across fresh Session, 10 opening panels, normal
Act1 movement/jump/bat, pause on focus loss, frozen steps while paused, release/resume,
clean quit, and corrupt-save warning with recovery to a new run. Main and reviewer inspected
all four 960x540 screenshots; no private data observed. See result.json for recorded limits.

[Options](options.png) · [Act1](act1.png) · [Resumed](resumed.png) · [Corrupt save](corrupt-save.png).

At add35aa the reviewer also exercised actual native Continue Act3 from a prepared
completed save to credits, replay ending, return to credits and title. [Credits capture](credits-add35aa.png)
and [result](credits-add35aa.json). Main and reviewer inspected the capture. Prepared save
is a focused fixture, not a qualifying full walkthrough.
