# M2 production/audio-browser increment

Latest user approved all six original cues ("those all sound fine") and said
"Let's do it" after the remaining M2 phases were explained. This authorizes
arrangements, effects, browser audition and reviews; no merge/deployment or final
game acceptance. Record original-cue approval without changing approved WAVs.
Reuse milestone/m2-audio-production and PR #11, base/current 82fbfd8. Main owns
implementation; distinct reviewer for each new commit; prior reviewers revalidate
final head, separate E2E after code sign-offs. M2 remains draft until human hearing
acceptance of materially new audio and browser checks are complete.

## Paths and approach

Within existing M2 bounds: tools/audio/, tools/audition.py, tools/check_audio.py,
tests/audio/, assets/audio/, docs/evidence/M2/, planning/. No game/ framework or
backend. The sound-check harness uses pygame-ce/pygbag, not a separate production
JavaScript audio engine. Synthesis is development-only; runtime decodes exported
Ogg/WAV. Browser build/output/dependency caches live in /tmp, never source control.

1. Production sources/export: preserve M1 samples, extend Dayman/proposal using
same user-provided MIDI tracks/global timing; retain Little Boy duet and Troll
ensemble palette. Document cut/loop boundaries, source hashes, 1.10x Dayman tempo
without transposition. Original six retain exact approved WAV bytes; all have
explicit playback assignments. Export compressed browser audio and deterministic
PCM masters. Finite proposal includes source ending, never inferred completed
from its old 27-second crop.
2. Original short SFX: jump, springy stomp, swing, hit, hurt, cat food, meal,
beam, checkpoint, hoagie, defeat and menu. No copied game sound. Without direct
reference hearing, never claim DuckTales acoustic match. Produce a labeled reel
and individual files; human audition remains required.
3. Audio director and sound-check app: gesture unlock, one scene baseline,
temporary 10s Dayman override, current-scene restoration, finite abduction stings,
finite proposal and credits destinations. Pause/blur freezes timer/voices; retry
clears transient state; separate music/SFX volume and mute; cap SFX voices to four;
failed/missing asset leaves visible retry feedback and navigation usable.
4. Actual desktop and pygbag browser workflow checks; branch screenshots at
1280x720,1920x1080,390x844 (readable desktop-control guidance, not touch support).
Capture locked/playing/paused/muted/error/recovered states. No gameplay proof.

## Red/green and verification contract

Before new behavior, callable stubs must fail semantic tests: long score output
empty/wrong duration, speed moves pitch, override resumes stale prior scene,
paused timer expires, volume zero leaks, fifth simultaneous effect exceeds cap.
Do not manufacture import failures. Existing 70 tests preserve all approved bytes.
Production validation: finite bounded score inputs, deterministic PCM, correct
frames/rate/channels, nonzero below-full-scale peaks, ramped boundaries, bounded
runtime identifiers/paths. CLI output directory must be new and source within
repo; do not overwrite existing exports. Reproduce exports in temporary output.

Commands (interfaces delivered in this increment):
`python -m pytest tests/audio -q -p no:cacheprovider`;
`python -m tools.audio.production --output /tmp/nightman-production-check`;
`python tools/audition.py --manifest assets/audio/production/manifest.json --build /tmp/nightman-audition`;
`python tests/audio/browser_audition.py --build /tmp/nightman-audition --evidence docs/evidence/M2/browser`;
`python tools/check_audio.py --min-duration 0.02 --max-duration 120 assets/audio`;
`git diff --check`.
Pin verified environment versions; Python screenshot/evidence runner uses installed
Chromium. Record actual failing assertions, commands/results, source fingerprint,
asset hashes and capture dimensions. No screenshot or listening claim from unit
checks. Browser audio analyser/mixer state checks are technical playback evidence,
not human hearing. Human musical acceptance stays separate from full-game sign-off.
