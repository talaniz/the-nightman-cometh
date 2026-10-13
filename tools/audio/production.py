"""Reproducible production masters and browser Ogg exports; no source recordings."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import wave

import numpy as np
from .approved import lanes_for, render_ensemble
from .preview import RATE, number, synthesize_lead

ROOT = Path(__file__).resolve().parents[2]
AUDIO = ROOT / 'assets/audio'


def render_score(score, speed=1):
    if not number(speed) or not .5 <= speed <= 2:
        raise ValueError('speed must be 0.5–2')
    if not isinstance(score, dict):
        raise ValueError('score must be an object')
    profile, duration, parts = (score.get(k) for k in ('profile', 'duration_seconds', 'parts'))
    counts = {'lead-v1': 1, 'duet-v1': 1, 'ensemble-v2': 3}
    if not isinstance(profile, str) or profile not in counts:
        raise ValueError('invalid synthesis profile')
    if not number(duration) or not .02 <= duration <= 120 or not .02 <= duration / speed <= 120:
        raise ValueError('duration must be bounded to 120 seconds')
    if (not isinstance(parts, list) or len(parts) != counts[profile]
            or any(not isinstance(p, list) for p in parts)
            or not 1 <= sum(map(len, parts)) <= 2000):
        raise ValueError('invalid parts or note count')
    converted = []
    for part in parts:
        notes, previous = [], -1
        for n in part:
            if not isinstance(n, dict):
                raise ValueError('note must be an object')
            start, end, pitch = (n.get(k) for k in ('start', 'end', 'midi'))
            if (not number(start) or not number(end) or not 0 <= start < end <= duration
                    or start < previous or (end-start)/speed < .01
                    or type(pitch) is not int or not 0 <= pitch <= 127):
                raise ValueError('invalid note time/order/pitch')
            notes.append({'start':start/speed, 'end':end/speed, 'midi':pitch})
            previous = start
        converted.append(notes)
    if profile == 'ensemble-v2':
        pcm = render_ensemble(converted, duration/speed)
    else:
        lanes = lanes_for(converted[0], counts[profile] if profile == 'lead-v1' else 2)
        tracks = [np.frombuffer(synthesize_lead(p, duration/speed), dtype='<i2').astype(np.float64)
                  for p in lanes]
        pcm = np.rint(sum(tracks)/len(tracks)).astype('<i2').tobytes()
    samples = np.frombuffer(pcm, dtype='<i2').copy()
    count = min(len(samples), round(.005 * RATE))
    samples[-count:] = np.rint(samples[-count:] * np.linspace(1, 0, count))
    return samples.tobytes()


def synth_effect(recipe):
    """Original pitch sweep + seeded noise with soft edges, peak <= 0.20."""
    if not isinstance(recipe, dict):
        raise ValueError('effect must be an object')
    duration, low, high, noise = (recipe.get(k) for k in ('duration','start_hz','end_hz','noise'))
    seed = recipe.get('seed')
    if (not all(number(v) for v in (duration,low,high,noise)) or not .02 <= duration <= 2
            or not 40 <= low <= 4000 or not 40 <= high <= 4000 or not 0 <= noise <= 1
            or type(seed) is not int or not 0 <= seed < 2**32):
        raise ValueError('invalid effect recipe')
    count = round(duration*RATE)
    hz = np.geomspace(low, high, count)
    phase = 2*np.pi*np.cumsum(hz)/RATE
    signal = (np.sin(phase)+np.sin(phase*3)/3)/1.334
    signal = signal*(1-noise) + np.random.default_rng(seed).uniform(-1,1,count)*noise
    edge = np.minimum(1,np.minimum(np.arange(count)/(.004*RATE),
                                    (count-1-np.arange(count))/(.018*RATE)))
    envelope = edge*np.exp(-np.linspace(0,2,count))
    return np.rint(signal*envelope*.20*32767).astype('<i2').tobytes()


def write_wav(path, pcm):
    with path.open('xb') as stream:
        with wave.open(stream,'wb') as out:
            out.setparams((1,2,RATE,0,'NONE','not compressed'))
            out.writeframes(pcm)


def export(output):
    output = Path(output)
    # Exclusive new directory protects prior masters and user files.
    output.mkdir()
    sources = AUDIO/'sources'
    recipe = json.loads((sources/'effects.json').read_text())
    cues = {}
    def add(name, pcm, loop, approval, source):
        wav = output/(name+'.wav'); ogg = output/(name+'.ogg')
        write_wav(wav, pcm)
        subprocess.run(['ffmpeg','-v','error','-nostdin','-n','-i',str(wav),
                        '-map_metadata','-1','-fflags','+bitexact','-flags:a','+bitexact',
                        '-c:a','libvorbis','-q:a','6',str(ogg)],check=True)
        samples = np.frombuffer(pcm,dtype='<i2').astype(np.int32)
        cues[name]={'file':ogg.name,'master':wav.name,'duration':len(samples)/RATE,'loop':loop,
                    'approval':approval,'source':source,'sha256':hashlib.sha256(ogg.read_bytes()).hexdigest(),
                    'master_sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),
                    'peak':int(max(abs(samples))), 'endpoints':[int(samples[0]),int(samples[-1])]}
    for name in ('dayman','proposal'):
        p=sources/(name+'-full.json'); score=json.loads(p.read_text())
        add(name,render_score(score),name=='dayman','extended phrase awaiting listening',
            'sources/'+p.name)
    score=json.loads((AUDIO/'previews/dayman-v2.json').read_text())
    # Full approved motif sped up 10%; runtime overrides only for the 10 s power-up.
    add('dayman-fast',render_score(score,1.1),True,'speed variant awaiting listening','previews/dayman-v2.json at 1.10x tempo')
    for name,source,duration in [('little-boy','little-boy-v1',24*60/105),('troll-toll','troll-toll-v2',32*60/70)]:
        score=json.loads((AUDIO/f'previews/{source}.json').read_text());score['duration_seconds']=duration
        add(name,render_score(score),True,'loop boundary awaiting listening','previews/'+source+'.json')
    originals=json.loads((AUDIO/'originals/manifest.json').read_text())
    for cue in originals['cues']:
        path=AUDIO/'originals'/cue['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==cue['sha256']
        with wave.open(str(path),'rb') as wav:pcm=wav.readframes(wav.getnframes())
        name=cue['scene']
        add(name,pcm,'kidnap' not in name,'composition approved; runtime loop/codec audition pending','originals/'+cue['file'])
    for name,r in recipe.items():add(name,synth_effect(r),False,'effect awaiting listening','sources/effects.json#'+name)
    # One clearly ordered effects audition with a 350 ms gap between events.
    reel=b''
    for name in recipe:
        with wave.open(str(output/(name+'.wav')),'rb') as w:reel+=w.readframes(w.getnframes())
        reel+=b'\0\0'*round(.35*RATE)
    write_wav(output/'effects-reel.wav',reel)
    manifest={'schema':1,'cues':cues,'effects':list(recipe), 'scenes':{
        'title':'dayman','narration':'proposal','level1':'little-boy','cricket':'cricket-boss',
        'frank-kidnap':'frank-kidnap','bridge':'troll-toll','frank':'frank-boss',
        'nightman-kidnap':'nightman-kidnap','rooftop':'rooftop','nightman':'nightman-boss',
        'proposal':'proposal','ending':None,'credits':'dayman'},
        'next':{'frank-kidnap':'bridge','nightman-kidnap':'rooftop','proposal':'ending'},
        'mix':{'music_gain_cap':.65,'sfx_gain_cap':.5,'sfx_voices':4},
        'approval':'New arrangements/effects and browser hearing pending; original six compositions approved'}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args(argv)
    try:manifest=export(args.output)
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:
        print(json.dumps({'ok':False,'error':str(exc)}));return 1
    print(json.dumps({'ok':True,'cues':len(manifest['cues']),'output':str(args.output)}));return 0

if __name__=='__main__':raise SystemExit(main())
