"""Reproduce human-approved preview recipes; development tool, not game runtime.

Run from the repository root: python -m tools.audio.approved SCORE OUTPUT.wav
"""
import argparse
import array
import json
from pathlib import Path
import sys
import wave
from .preview import RATE, number, render

PROFILES = {'lead-v1': 1, 'duet-v1': 1, 'ensemble-v2': 3}


def validate(score):
    if not isinstance(score, dict):
        raise ValueError('score must be an object')
    profile = score.get('profile')
    if not isinstance(profile, str) or profile not in PROFILES:
        raise ValueError('unknown approved recipe profile')
    duration, parts = score.get('duration_seconds'), score.get('parts')
    if not number(duration) or not 15 <= duration <= 30:
        raise ValueError('duration must be 15–30 seconds')
    if not isinstance(parts, list) or len(parts) != PROFILES[profile]:
        raise ValueError('incorrect number of parts')
    if any(not isinstance(p, list) for p in parts) or not 1 <= sum(map(len, parts)) <= 1000:
        raise ValueError('expected 1–1000 total notes')
    for part in parts:
        last_start = -1
        for n in part:
            if not isinstance(n, dict):
                raise ValueError('note must be an object')
            start, end, pitch = (n.get(k) for k in ('start', 'end', 'midi'))
            if (not number(start) or not number(end)
                    or not 0 <= start < end <= duration or end - start < .01
                    or start < last_start or type(pitch) is not int or not 0 <= pitch <= 127):
                raise ValueError('invalid note pitch/time/order')
            last_start = start
    return profile, duration, parts


def lanes_for(notes, maximum):
    lanes = []
    for note in notes:
        for lane in lanes:
            if lane[-1]['end'] <= note['start']:
                lane.append(note)
                break
        else:
            if len(lanes) >= maximum:
                raise ValueError('too many simultaneous voices for profile')
            lanes.append([note])
    return lanes


def render_ensemble(parts, duration):
    # Frozen NumPy recipe matches the exact user-approved Troll Toll v2 bytes.
    import numpy as np
    tracks = []
    for part_index, notes in enumerate(parts):
        y = np.zeros(round(RATE * duration), dtype=np.float64)
        for n in notes:
            first, last = round(n['start'] * RATE), round(n['end'] * RATE)
            count = last - first
            t = np.arange(count) / RATE
            if part_index == 2:
                count = min(count, round(.045 * RATE))
                t = np.arange(count) / RATE
                raw = np.random.default_rng(first).uniform(-1, 1, count)
                signal = np.concatenate(([0.], np.diff(raw))) * np.exp(-t / .009) * .055
            else:
                hz = 440 * 2 ** ((n['midi'] - 69) / 12)
                phase = 2 * np.pi * hz * t
                harmonics = [h for h in (1, 3, 5, 7) if h * hz < RATE / 2]
                if part_index == 1 and n['midi'] < 55:
                    signal = np.sin(phase) * .19
                else:
                    signal = sum(np.sin(h * phase) / h for h in harmonics) / sum(1 / h for h in harmonics)
                    signal *= .40 if part_index == 0 else .105
                if part_index == 1:
                    signal *= .30 + .70 * np.exp(-t / .15)
                signal *= np.minimum(1, np.minimum(np.arange(count) / (.01 * RATE),
                                                  (count - 1 - np.arange(count)) / (.02 * RATE)))
            y[first:first + len(signal)] += signal
        tracks.append(y)
    full = sum(tracks)
    peak = np.max(np.abs(full))
    if peak == 0:
        raise ValueError('score produces silence')
    full *= min(1, .70 / peak)
    return np.round(full * 32767).astype('<i2').tobytes()


def render_score(score):
    profile, duration, parts = validate(score)
    if profile == 'ensemble-v2':
        return render_ensemble(parts, duration)
    lanes = lanes_for(parts[0], 1 if profile == 'lead-v1' else 2)
    if not lanes:
        raise ValueError('score produces silence')
    if profile == 'lead-v1':
        return render(lanes[0], duration, 'chip')
    tracks = []
    for lane in lanes:
        a = array.array('h')
        a.frombytes(render(lane, duration, 'chip'))
        if sys.byteorder != 'little':
            a.byteswap()
        tracks.append(a)
    mixed = array.array('h', (round(sum(values) / len(tracks)) for values in zip(*tracks)))
    if sys.byteorder != 'little':
        mixed.byteswap()
    return mixed.tobytes()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('score', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args(argv)
    try:
        # Check before synthesis as well as atomic exclusive creation afterwards.
        if args.output.exists() or args.output.is_symlink():
            raise ValueError('output already exists')
        with args.score.open('rb') as f:
            data = f.read(1024 * 1024 + 1)
        if len(data) > 1024 * 1024:
            raise ValueError('score exceeds 1 MiB')
        score = json.loads(data)
        pcm = render_score(score)
        with args.output.open('xb') as f:
            with wave.open(f, 'wb') as w:
                w.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
                w.writeframes(pcm)
    except (OSError, ValueError, UnicodeError, ImportError, RecursionError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}))
        return 1
    print(json.dumps({'ok': True, 'path': str(args.output)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
