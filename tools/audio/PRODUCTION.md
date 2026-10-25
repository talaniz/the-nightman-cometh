# M2 production and sound-check workflow

Install the isolated tools from requirements-audition.txt; FFmpeg with libvorbis
and Chromium are also required. Tested host: Python 3.11.2, pygame-ce 2.5.8,
NumPy 1.26.4, pytest 9.1.1, pygbag 0.9.3, Playwright 1.63.0, FFmpeg 5.1.6 and
Chromium 139.0.7258.66 on Debian/Pi ARM64. The actual browser SDK loads Python
3.12 and pygame-ce 2.5.7; full version strings are in browser evidence captures.
This version difference is explicit, not an assertion that native tests cover WASM.

```sh
python -m tools.audio.production --output /tmp/nightman-new-production
python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio
python tools/audition.py --manifest assets/audio/production/manifest.json
python tools/audition.py --manifest assets/audio/production/manifest.json --build /tmp/nightman-new-audition
python -m http.server 8765 --bind 127.0.0.1 --directory /tmp/nightman-new-audition
```

Open http://127.0.0.1:8765 in a desktop browser. The browser runtime may first request
a click; Enter inside the app enables music. Up/down selects scenes and Enter
plays; D starts the 10-second Dayman override; P pauses/resumes; M mutes. Left/right
selects an effect, Space plays it. 1/2 changes music volume, 3/4 effects volume.
X deliberately attempts a missing Ogg load; R retries. These controls belong to
the audition tool, not the game's final input mapping. New output directories are
required; existing masters/builds are never overwritten. If export/build fails,
inspect the failure and choose a new output directory after correcting the cause.

```sh
python -m pytest tests/audio -q -p no:cacheprovider
python tests/audio/browser_audition.py --build /tmp/nightman-new-audition --evidence /tmp/nightman-new-evidence
```

Browser verification runs the actual pygbag artifact, not a mock page. It checks
user gesture, mixer activity/gain, blur/pause, mute, current-scene restoration,
finite sting destination, missing-file recovery, capped effects and volume zero.
It captures 1280x720, 1920x1080 and 390x844. Narrow screens receive readable
keyboard/desktop guidance. SDL dummy decoding tests are supplemental; headless
playback never proves human hearing or musical quality.

## Source and arrangement decisions

- dayman/proposal: full single-lead phrases from the user-provided MIDI. Global
  tempo events are merged across tracks. Exact approved prefix notation retained;
  source hash, track and timestamp are recorded in assets/audio/sources/.
  Proposal includes the final sustained note instead of ending at the old crop.
- dayman-fast: approved motif with all note times divided by 1.10, pitches intact.
  Export retains the full motif for audition; gameplay override is ten seconds.
- little-boy: approved duet, 24 beats at 105 BPM; trimmed only after its musical
  phrase/rest to make a 13.714-second loop.
- troll-toll: approved ensemble, 32 beats at 70 BPM, 27.429-second loop, 5 ms
  export end ramp. Its old 29-second preview/master is untouched.
- six originals: approved WAV master bytes copied exactly; Ogg compression and
  runtime loop joins remain part of listening acceptance.
- all browser music uses Ogg; PCM masters remain authoritative for reproduction.
  Full exports reproduce byte-for-byte with the recorded FFmpeg options/version.

Music and effects have separate gains, capped at 0.65 and 0.50 respectively.
Two music channels crossfade over 80 ms with summed weights no greater than one;
four effect channels enforce a fixed cap. Music masters peak <=0.70 and effects
<=0.20, leaving nominal simultaneous PCM headroom. Ogg decoding is lossy; measured
playback and human combat-mix hearing remain acceptance evidence, not inferred.
Effects are original pitch/noise designs. No DuckTales recording was imported or
heard by the agent, so no acoustic matching claim is made.

Effects reel order: jump, stomp, bat swing, bat hit, hurt, cat food, meal,
sunbeam, checkpoint, hoagie, boss defeat, menu. A 350 ms gap separates effects.

## Browser dependency workaround and limits

The [pygbag 0.9.3 BrowserFS omission](https://github.com/pygame-web/pygbag/issues/227)
was reproduced as a failed script request and runtime error. The builder fetches
the official archived BrowserFS copy, verifies SHA-256
`ba01fda78db31a7ba579afe74b8b56cf4636381ca1b6c54ffba20467756a627f`, serves it locally
and includes its license. It removes unused iframe permissions and hides the SDK
console. It does not suppress browser errors; the documented SDK user-gesture
notice is the sole expected console-error exclusion in the test.

The SDK still fetches its versioned runtime from pygame-web's CDN; offline startup
is not supported or claimed. Build hashes identify the tested artifact; SDK build
timestamps mean whole archives are not asserted byte-identical across builds.
M3 owns the game's loader/recovery, deployment packaging and integrated controls.
This sound-check app is not game content, a deployment or final acceptance.
Use the numeric loopback address: upstream runtime treats the literal localhost
hostname as development mode and can request dependencies from the wrong port.
