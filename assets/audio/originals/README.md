# Original cue auditions, v1

Six new melodies for the approved scene map. Pulse lead, sine bass, pulse chord
stabs and short noise snaps reuse the frozen M1 ensemble palette. No TMNT/Mega Man
melodies or recordings were imported. Numerical validation does not establish
style, musical quality or listening acceptance. All six await user feedback.

| Score/WAV stem | Scene | BPM | Form |
| --- | --- | --- | --- |
| cricket-boss-v1 | Cricket fight | 172 | E-minor chase, eight-bar idea played twice |
| frank-kidnap-v1 | Frank steals Dee | 140 | Two-bar comic downward stumble |
| frank-boss-v1 | Frank fight | 152 | C-minor stomp, eight-bar idea played twice |
| nightman-kidnap-v1 | Nightman steals Dee | 128 | Two-bar diminished alarm to D minor |
| rooftop-v1 | Rooftop approach | 116 | Spacious D-minor theme, eight bars twice |
| nightman-boss-v1 | Final boss | 184 | D harmonic-minor runs, eight bars twice |

Scores use quarter-note beats, MIDI pitches and explicit note ends, with rests
represented by gaps. Parts: 0 lead, 1 bass/chords, 2 noise snaps (pitch ignored).
The JSON files are the authoritative editable notation; metadata fields describe
scene/form but do not change synthesis. `manifest.json` records export hashes and
technical checks, and is not a score. `loop_beats` identifies a candidate musical
phrase, not a verified runtime loop point. Production loop/fade listening remains
M2 work. Stings are finite, approximately 3–4 seconds, not padded to 15 seconds.

From the repository root, with `tools/audio/requirements-preview.txt` installed:

```sh
python -m tools.audio.arrangement assets/audio/originals/cricket-boss-v1.json /tmp/cricket-audition.wav
```

The output must be new; the CLI refuses existing files or symlinks. PCM16 mono,
44100 Hz, deterministic using the recorded NumPy recipe. Beat timing preserves
pitch when BPM changes. Bounds: 40–240 BPM, 1–128 beats, at most 60 seconds and
1000 events; input at most 1 MiB. Rendered note length must be at least 10 ms.
A 5 ms end ramp applies only to these new arrangements, ensuring a noise snap
cut by the cue boundary ends at zero. The frozen M1 renderer is unchanged.
M1's `tools/check_audio.py` still intentionally enforces its 15–30 second preview
contract, so it is not the validator for these short stings/longer audition reels.
Use the M2 evidence report and tests; expanded production validation is pending.

No UI or browser audio player is included in this increment. Drive delivery is
private; no private sharing links are published here.


## Later listening decision
The user approved all six original compositions: "those all sound fine". Prior
pending-listening text above is historical. Production loop/codec and whole-game
acceptance remain separate. No approved original WAV bytes changed.
