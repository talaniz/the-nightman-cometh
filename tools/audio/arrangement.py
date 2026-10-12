"""Render original, beat-based audition scores with the frozen ensemble palette.

Development only: python -m tools.audio.arrangement SCORE OUTPUT.wav
"""
import argparse
import json
from pathlib import Path
import wave

from .approved import render_ensemble
from .preview import RATE, number


def compile_score(score):
    """Validate bounded musical timing and translate beats to seconds."""
    if not isinstance(score, dict) or score.get('schema') != 'ensemble-beats-v1':
        raise ValueError('expected ensemble-beats-v1 score')
    bpm, beats, parts = (score.get(k) for k in ('bpm', 'beats', 'parts'))
    if not number(bpm) or not 40 <= bpm <= 240:
        raise ValueError('tempo must be 40–240 BPM')
    if not number(beats) or not 1 <= beats <= 128:
        raise ValueError('cue must span 1–128 beats')
    seconds_per_beat = 60 / bpm
    duration = beats * seconds_per_beat
    if duration > 60:
        raise ValueError('cue exceeds 60 seconds')
    if (not isinstance(parts, list) or len(parts) != 3
            or any(not isinstance(part, list) for part in parts)
            or not 1 <= sum(map(len, parts)) <= 1000):
        raise ValueError('expected three parts and 1–1000 notes')
    compiled = []
    for part in parts:
        notes, last = [], -1
        for note in part:
            if not isinstance(note, dict):
                raise ValueError('note must be an object')
            start, end, midi = (note.get(k) for k in ('start', 'end', 'midi'))
            if (not number(start) or not number(end)
                    or not 0 <= start < end <= beats or start < last
                    or (end - start) * seconds_per_beat < .01
                    or type(midi) is not int or not 0 <= midi <= 127):
                raise ValueError('invalid note pitch/time/order')
            notes.append({'start': start * seconds_per_beat,
                          'end': end * seconds_per_beat, 'midi': midi})
            last = start
        compiled.append(notes)
    return duration, compiled


def render_score(score):
    duration, parts = compile_score(score)
    return render_ensemble(parts, duration)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('score', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.output.exists() or args.output.is_symlink():
            raise ValueError('output already exists')
        with args.score.open('rb') as stream:
            content = stream.read(1024 * 1024 + 1)
        if len(content) > 1024 * 1024:
            raise ValueError('score exceeds 1 MiB')
        pcm = render_score(json.loads(content))
        with args.output.open('xb') as stream:
            with wave.open(stream, 'wb') as writer:
                writer.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
                writer.writeframes(pcm)
    except (OSError, ValueError, UnicodeError, ImportError, RecursionError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}))
        return 1
    print(json.dumps({'ok': True, 'path': str(args.output), 'approval': 'pending'}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
