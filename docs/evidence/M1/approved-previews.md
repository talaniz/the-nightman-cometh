# Approved musical previews — integration evidence

All four short candidates have explicit user listening approval. No agent claims
to have heard the source or output. This evidence records the user's decisions and
preservation checks, not an automated musical-fidelity assessment.

| ID | Duration | Source / conversion | Human decision |
| --- | --- | --- | --- |
| dayman-v2 | 15 s | User-supplied musical MIDI, Soprano track 0, from 409.29476345 s; 37 unchanged notes | User called it perfect after receiving chip/plain candidates |
| proposal-v1 | 27 s | Same MIDI, Soprano track 4, from 455.20257745 s; 66 unchanged notes | User said Proposal and Little Baby Boy were spot on |
| little-boy-v1 | 15 s | [EEknuF's Little Baby Boy sequence](https://onlinesequencer.net/5515500), Lucent Choir instrument 59, grid 98–194 at 105 BPM; 48 notes, two simultaneous voices | Source first approved; rendered version subsequently approved |
| troll-toll-v2 | 29 s | [MB's Songsterr Troll Toll score](https://www.songsterr.com/a/wsa/its-always-sunny-in-philadelphia-troll-toll-tab-s3135536t1), revision 8538834, bars 7–14, 70 BPM; vocals, piano and snaps | User called revised full arrangement perfect |

Hashes and normalized short-score paths are in ../../../assets/audio/manifest.json.
The WAV files are the original approved local artifacts copied without re-encoding.
User audition links were MP3 encodings of these WAVs (Dayman also provided plain WAV).
The four committed candidates preserve the approved synthesis exactly. Rejected
Dayman v1 remains identifiable as rejected; do not load it as production music.

Source MIDI SHA-256: b78fb281a2a5a4909ec1ffaceb4646d6da1f700de7a3b405901239bc400489fc.
Original uploaded MIDI/MP3, full downloaded score data, private Drive URLs and
model weights are not published. Short normalized note excerpts are sufficient to
reproduce these previews. A source repository is not evidence of third-party rights;
public game distribution remains the existing release gate.

## Reproduction and checks

From repository root, use Python 3.11 and the pinned development dependencies in
`tools/audio/requirements-preview.txt`. The verified Pi environment uses NumPy 1.26.4.

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m1-tools/bin/python -m pytest tests/audio -q -p no:cacheprovider
python3 tools/check_audio.py assets/audio/previews
/tmp/nightman-m1-tools/bin/python -m tools.audio.approved assets/audio/previews/dayman-v2.json /tmp/dayman-approved-new.wav
git diff --check
```

Use a fresh output filename for each of the four score IDs. Existing output is
intentionally refused. The paths above describe the verified local environment;
another machine should create a venv and install the pinned requirements, then use
that venv's Python. No network/source-file access occurs during rendering.

Observed red: executable `render_score` stub returned empty bytes; four approved-PCM
comparisons failed and seven invalid-score rejection assertions failed (11 failures,
exit 1). Implemented bounded recipes; full audio suite: **50 passed**. This includes
previous malformed RIFF regressions and all four exact approved-PCM comparisons.
Actual CLI: all four outputs byte-identical including WAV headers; existing-output
rejection preserves the file; malformed JSON rejected with no output, corrected
input succeeds; dangling output symlink refused. See approved-cli-validation.json.
All six WAVs (four approved plus two rejected historical probes) pass format/range
checks; validity does not make rejected probes musically acceptable.

No game/UI/browser implementation changed: screenshots N/A. Exact-head independent
per-commit review and subsequent workflow acceptance are recorded in PR #10. These
checks are main's evidence, not independent sign-off. No merge or deployment.

## Rendering limits and future work

Lead uses the accepted pulse-like odd-harmonic recipe with 10/20 ms edge ramps.
Little Boy preserves overlapping voices at equal lane gain. Troll Toll uses fixed
part gains, sine bass, chip vocal/chord timbres and seeded noise snaps. Sixteenth
swing is interpreted 2:1; explicit tuplets retain their subdivisions. Ties are joined;
piano let-ring is approximated by finite written lengths/decay. Source dynamics and
human vocal inflections are not reproduced exactly. Those limitations were present
in the accepted sample; this integration does not silently alter them.

Exact NumPy PCM rounding may vary across numerical builds/hardware. The shipped
WAVs and hashes are authoritative; never silently accept a changed regeneration.
These are short previews, not finished loops or the complete game soundtrack.
M2 must implement and audition the cue map, original compositions, full arrangements,
SFX, loop transitions and actual browser audio behavior. M1 approval is not M2/M8
acceptance. Latest ending and cue map are in planning/specification.md and
planning/music-cue-map.md.
