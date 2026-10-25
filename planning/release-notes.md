# Planning baseline — 2026-10-11

Established the agreed specification, eight implementation milestones with 17 build phases, per-commit code review, per-PR independent E2E, real browser screenshot contracts, user listening gates and three final complete playthroughs. Existing public repository reused without changes to history/visibility. No game code, audio implementation, production UI screenshots or executed gameplay checks are included.

# M1 work in progress — audio validation

Added a standard-library PCM WAV validator with JSON reports and synthetic tests. Retrieved the official reference to temporary local storage and documented the lack of actual listening/transcription. This increment contains no music preview or game and does not complete M1.

# M1 listening probe — 2026-10-12

Added a source-derived, unapproved 16-second Dayman note probe, plain and chip-lead WAVs, editable MIDI/JSON, deterministic renderer and local inference evidence. Automatic extractors disagree; melody fidelity is unverified and needs user correction/approval. No other songs or game implementation delivered.

# M1 approved preview integration

Preserves the four human-approved music previews and normalized short scores;
adds bounded recipe reproduction and approval-preservation tests. Dayman v1 is
retained as rejected historical evidence. Updated ending dialogue and full music
cue map, including original boss/transition/rooftop assignments, are documented
for M2–M6. No source recordings or private sharing links are included. The game,
full soundtrack, browser audition and controller support remain future milestones.


# M2 original-cue auditions

Adds six new boss/rooftop/kidnapping compositions with editable beat notation,
WAV auditions and a bounded deterministic renderer using the approved ensemble
palette. Includes pitch-preserving tempo and invalid-input checks. Approved M1
assets are unchanged. All new compositions await listening approval; full game
cues, runtime playback and SFX remain in progress. No UI changed.


# M2 production audio and actual browser audition

Records approval of all six original cues. Adds full Dayman/proposal source
phrases, two level loops, a pitch-preserving faster Dayman variant, twelve original
effects and WAV/Ogg exports. A pygame/pygbag sound-check app verifies gesture
unlock, independent volume/mute, crossfades, pause/blur, scene restoration and
missing-file retry in actual Chromium. Approved source previews and original
masters remain unchanged. New arrangements/effects await listening; this is
not a playable game or full M2/final-game acceptance.


## M2 listening approval and finale adjustment (2026-10-25)
User approved the browser audition after using numeric loopback; earlier pending
listening statements are superseded. Ending now uses approved Dayman; credits
are silent. Original Sunny-style credits music deferred to GitHub issue #12.
No audio bytes changed. New routing regression failed before map correction.
Final exact-head reviews and refreshed browser evidence pending; no merge/deploy.

# M3 browser foundation (candidate)

Adds a staged-Philadelphia rehearsal room with Dennis/Dayman, Rat Bat/stomp/beam
combat, controlled targets/projectiles, three hearts, combined meal, cat food,
one-time healing checkpoints and deterministic retry. Adds keyboard menus,
representative dialogue replay/skip, local save failure recovery, isolated QA,
approved audio integration, visible loader retry and localhost canonicalization.
Build/preview tools and actual-browser CI are delivered. Final story acts, USB,
new credits music, deployment and full-game acceptance remain outside M3.
