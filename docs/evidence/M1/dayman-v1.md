# Dayman v1 — unapproved transcription probe (2026-10-12)

The user approved a local transcription → synthesis → human listening workflow on 2026-10-12. This permits a clearly labeled machine-derived candidate without claiming the implementing agent heard or verified it.

## Source correction and provenance

Actual source: [FX Networks' Season 4 episode 13 Dayman highlight](https://www.youtube.com/watch?v=VCvr6tzZPTU), channel ID UC2dIDJBf9W88PxGm-uHZPaQ. Metadata and English captions place the first chorus at the beginning. The earlier 210sYMGeeY0 scene ends before Dayman; its old access log is not evidence for this melody.

Source container SHA-256: cad7812e2af5b5d1f356831056c8395457fe4a2d949a1e377a632bd90308757f.
Requested source crop: 0.00–15.22 seconds. 22,050 Hz mono crop hash: 3cfc7aa3864a16f1909acf141374a53a8a0788167794b71ab2bfae956f27d890.
Basic Pitch ONNX model SHA-256: 2c3c1d144bfa61ad236e92e169c13535c880469a12a047d4e73451f2c059a0ec.

No source recording, captions, separated vocals or model weights are committed. Previews contain synthesized tones only. Source/arrangement rights for public game deployment remain a separate gate; no ownership of the underlying song is claimed.

## What was tried and what is delivered

1. Basic Pitch 0.4.0 ONNX on the full mix produced 118 note events in 59.14 seconds, including accompaniment. The retained raw events are dayman-v1-events.json.
2. A lightweight librosa foreground mask produced 86 events; a pYIN cross-check yielded only three sustained candidates under the chosen thresholds. This did not establish a usable isolated melody.
3. Demucs 4.0.1 htdemucs ran successfully on CPU in 4:55, with four-second segments, no shifts and one job. Its vocal stem yielded 27 sparse Basic Pitch events. Weight hash: 8726e21a993978c7ba086d3872e7608d7d5bfca646ca4aca459ffda844faa8b4. Stem hash: 6065e0878b0eeda1c7369d0f0836bb08d65e92b513216b361a35e2684bca23b5.
4. CREPE tiny 0.0.24 on that stem produced 1,522 frames in 37.50 seconds; a 0.21 periodicity cutoff and 100 ms note grouping yielded 22 short events. This did not resolve the sparse melody.
5. The delivered v1 probe uses the fuller original Basic Pitch extraction, NOT the separated-vocal experiments. select_melody keeps the strongest active C4–C6 note, activation >=0.2, input and output segments >=100 ms. It yields 34 notes, about 8.08 seconds sounding within a 16-second file. No manual musical correction, tempo grid, inserted notes or fabricated source listening.

This is an explicit experiment for user feedback. Piano/harmony may be mistaken for melody, gaps may be missing notes, and octave jumps may be wrong. Neither technical success nor this selection implies recognition. Do not approve it automatically. A rejection means the extraction needs correction or musician input, not that the user should accept inaccurate music.

## Reproduction

Runtime rendering needs Python 3.11 only; source analysis uses the isolated environment whose versions are in inference-environment.txt. Basic Pitch's metadata requires TensorFlow on Python 3.11 even though ONNX inference worked; TensorFlow was deliberately omitted. pip check is not claimed to pass.

Source commands (temporary files only):

```sh
/tmp/nightman-m1-tools/bin/yt-dlp --no-playlist --js-runtimes node -f bestaudio -o '/tmp/nightman-dayman-source.%(ext)s' 'https://www.youtube.com/watch?v=VCvr6tzZPTU'
ffmpeg -v error -nostdin -i /tmp/nightman-dayman-source.webm -t 15.22 -ac 1 -ar 22050 /tmp/nightman-dayman-crop.wav
```

Inference used basic_pitch.inference.predict on that crop, with default thresholds and the installed ONNX model. Each returned event was saved as [float(start), float(end), int(MIDI pitch), float(activation)] in the checked-in raw-event JSON. The local helper select_melody(events, 15.22) supplies the score's notes; source timing is retained. MIDI was exported via pretty_midi 0.2.11.post0, program 80, velocity 90. Its 120 BPM header is only a seconds-to-ticks encoding reference, not a claim about the performance's tempo.

Regenerate the listening files to NEW paths:

```sh
python3 tools/audio/preview.py assets/audio/previews/dayman-v1.json /tmp/dayman-v1-melody.wav
python3 tools/audio/preview.py assets/audio/previews/dayman-v1.json /tmp/dayman-v1-chip.wav --style chip
python3 tools/check_audio.py /tmp/dayman-v1-melody.wav /tmp/dayman-v1-chip.wav
```

Both renderings contain the same notes/timing. Chip mode adds odd harmonics to the lead; there is no rhythm section yet. Approval remains pending in the score and manifest.

## Observed verification

Before implementation, stub select_melody returned [] and render returned empty bytes. Twelve tests failed on expected selection, actual sample length, distinct timbre and rejection of invalid inputs. No import failure was counted as red.
An additional oversized JSON integer regression failed with OverflowError, then passed after numeric validation was fixed.
Final suite: 39 passed, including the previous 19 validator tests, score selection, A4 frequency/sample count, rest preservation, malformed events/scores and real CLI success/failure/no-overwrite.
Actual generated WAVs pass tools/check_audio.py: PCM16 mono, 44,100 Hz, 705,600 frames (16 seconds), no digital-rail samples, both non-silent. Exact hashes and peaks are in dayman-v1-validation.json and assets/audio/manifest.json.
No UI changed: screenshots N/A. No game, browser, USB or final-playthrough acceptance is claimed.
Independent exact-head code and workflow review results live in PR #10. Musical recognition/listening approval is outstanding.

## Listening decision (pending)

Listen to the plain melody first against the beginning of the linked source, then assess chip timbre. Record recognizable/not recognizable, wrong passage timestamps and requested corrections. Do not proceed to the other songs until Dayman direction is approved.

Primary tool references: [Basic Pitch](https://github.com/spotify/basic-pitch), [Demucs](https://github.com/facebookresearch/demucs), [CREPE implementation](https://github.com/maxrmorrison/torchcrepe), [librosa foreground experiment](https://librosa.org/doc/0.10.2/auto_examples/plot_vocal_separation.html).
