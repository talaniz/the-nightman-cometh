"""Select candidate melody notes and render unapproved listening previews.

Runtime synthesis uses only stdlib. Automatic selection is a heuristic, not a
musical-accuracy verdict. Source transcription dependencies stay outside the game.
"""
import argparse
import array
import json
import math
from pathlib import Path
import sys
import wave

RATE = 44100


def number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def select_melody(events, duration):
    """Keep strongest active C4–C6 note; omit events below 0.2 activation."""
    if not number(duration) or not 0 < duration <= 30:
        raise ValueError("invalid source duration")
    if not isinstance(events, list) or len(events) > 2000:
        raise ValueError("expected at most 2000 note events")
    candidates = []
    for event in events:
        if not isinstance(event, list) or len(event) != 4:
            raise ValueError("expected [start, end, MIDI pitch, activation]")
        start, end, pitch, strength = event
        if (not all(number(v) for v in event) or not 0 <= start < end <= duration
                or type(pitch) is not int or not 0 <= pitch <= 127
                or not 0 <= strength <= 1):
            raise ValueError("invalid transcription event")
        if 60 <= pitch <= 84 and strength >= 0.2 and end - start >= 0.1:
            candidates.append(event)
    boundaries = sorted({v for event in candidates for v in event[:2]})
    notes = []
    for start, end in zip(boundaries, boundaries[1:]):
        middle = (start + end) / 2
        active = [e for e in candidates if e[0] <= middle < e[1]]
        if not active:
            continue
        winner = max(active, key=lambda e: (e[3], e[2]))
        if notes and notes[-1]["midi"] == winner[2] and notes[-1]["end"] == start:
            notes[-1]["end"] = end
            notes[-1]["activation"] = max(notes[-1]["activation"], winner[3])
        else:
            notes.append({"start":start, "end":end, "midi":winner[2], "activation":winner[3]})
    return [n for n in notes if n["end"] - n["start"] >= 0.1]


def validate_score(notes, duration, style):
    if not number(duration) or not 15 <= duration <= 30:
        raise ValueError("preview duration must be 15–30 seconds")
    if style not in ("sine", "chip"):
        raise ValueError("style must be sine or chip")
    if not isinstance(notes, list) or not 1 <= len(notes) <= 1000:
        raise ValueError("score must contain 1–1000 notes")
    previous_end = 0
    for note in notes:
        if not isinstance(note, dict):
            raise ValueError("each note must be an object")
        start, end, pitch = (note.get(k) for k in ("start", "end", "midi"))
        if (not number(start) or not number(end) or not previous_end <= start < end <= duration
                or end - start < 0.01 or type(pitch) is not int or not 0 <= pitch <= 127):
            raise ValueError("invalid or overlapping note time/pitch")
        previous_end = end


def render(notes, duration, style="sine"):
    """Return deterministic little-endian PCM16 mono with 10/20ms edge ramps."""
    validate_score(notes, duration, style)
    samples = array.array("h", [0]) * round(duration * RATE)
    for note in notes:
        start, stop = round(note["start"] * RATE), round(note["end"] * RATE)
        frequency = 440 * 2 ** ((note["midi"] - 69) / 12)
        harmonics = [1] if style == "sine" else [h for h in (1, 3, 5, 7) if h * frequency < RATE / 2]
        scale = sum(1 / h for h in harmonics)
        for i in range(stop - start):
            phase = 2 * math.pi * frequency * i / RATE
            signal = sum(math.sin(h * phase) / h for h in harmonics) / scale
            envelope = min(1, i / (0.01 * RATE), (stop - start - 1 - i) / (0.02 * RATE))
            samples[start + i] = round(10000 * envelope * signal)
    if sys.byteorder != "little":
        samples.byteswap()
    return samples.tobytes()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("score", type=Path, help="JSON with duration_seconds and notes")
    parser.add_argument("output", type=Path, help="new WAV path; existing files are never overwritten")
    parser.add_argument("--style", choices=("sine", "chip"), default="sine")
    args = parser.parse_args(argv)
    try:
        with args.score.open("rb") as stream:
            content = stream.read(1024 * 1024 + 1)
        if len(content) > 1024 * 1024:
            raise ValueError("score exceeds 1 MiB")
        score = json.loads(content)
        if not isinstance(score, dict):
            raise ValueError("score must be a JSON object")
        pcm = render(score.get("notes"), score.get("duration_seconds"), args.style)
        with args.output.open("xb") as output:
            with wave.open(output, "wb") as writer:
                writer.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
                writer.writeframes(pcm)
    except (OSError, ValueError, UnicodeError) as exc:
        print(json.dumps({"ok":False, "error":str(exc)}))
        return 1
    print(json.dumps({"ok":True, "path":str(args.output), "style":args.style, "approval":"pending"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
