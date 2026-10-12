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
