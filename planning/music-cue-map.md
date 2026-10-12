# Agreed music placements and remaining composition

The user's latest build request authorizes implementation through the milestone
plan; it does not authorize merging or production deployment. The four preview
approvals establish musical direction, not full-length cue approval.

| Scene | Cue | Acceptance status / intended character |
| --- | --- | --- |
| Title / splash | Dayman | Approved v2 motif; title arrangement pending M2 |
| Charlie opening narration | Proposal Song | Approved v1 motif; gentle narration arrangement |
| First level | Little Boy, Tiny Boy | Approved Little Baby Boy v1 motif; loop pending |
| Cricket boss | Original | Fast/frantic retro arcade boss theme |
| Frank kidnaps Waitress | Original | Short comic abduction transition |
| Underbridge level | Troll Toll | Approved v2 full ensemble direction; loop pending |
| Frank boss | Original | Heavy, punchy, urgent theme; new melody |
| Nightman kidnaps Dee | Original | Short ominous abduction transition |
| Rooftop level | Original | Tense nighttime theme |
| Nightman boss | Original | Faster/intense final-boss theme, distinct from approach |
| Final rescue / Charlie proposal | Proposal Song | Finite cue, readable stills; duck/stop for final joke |
| End / credits | Dayman | Final transition and credits arrangement pending |
| Dayman power-up | Faster Dayman variant | Slightly faster requested; 1.10x pitch-preserving audition proposed |

Original music may draw broad rhythmic/timbral inspiration from TMNT arcade and
Mega Man boss music but uses newly composed melodies. No imported game recordings.
Build variants using the approved instrumental palette, keeping lead melody clear.

## State and transition contract for M2/M3

A scene cue is the baseline. Transformation temporarily overrides it; on expiry,
resume the cue belonging to the current scene, not a stale prior scene. Boss
entry, defeat, dialogue skip, retry and credits each have an explicit destination.
Pause/blur freezes or pauses playback as appropriate; resume must not duplicate
players. Mute and audio failure do not prevent progress. Browser autoplay requires
a user gesture, so a visible Start action unlocks the title music. No promise of
automatic sound before that gesture. Short music stings must not trap dialogue.

## Approved final exchange

Charlie proposes; actual Waitress refuses. Charlie: "Well, see you tomorrow."
Dee: "I told you no one writes a musical for no reason!"
Charlie, hand low: "Dee, I'm right here right now"; hand high:
"but I'm about to go here!" End. Credits with Dayman.

## Listening gates

M1: all four preview approvals obtained; preserve exact approved WAV hashes.
M2: audition each new original cue, expanded arrangement, loop boundary, power-up
speed and SFX mix with the user. M3–M6: verify transitions in real browser gameplay.
M8: listen during all three qualifying final-candidate runs. None are inferred from
waveform checks or independent source inspection.
