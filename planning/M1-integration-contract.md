# M1 approved-preview integration contract

User authorized the full build after explicitly approving Dayman v2, Proposal v1,
Little Baby Boy v1 and Troll Toll v2. This increment preserves the exact listened
WAV bytes and normalized short note scores. Full uploaded MIDI/MP3, private Drive
identifiers, complete third-party score files and temporary models stay outside Git.

Reuse milestone/m1-music-previews, PR #10 and its recorded worktree/base. In-scope:
assets/audio/, tools/audio/, tests/audio/, docs/evidence/M1/, planning/. No game
implementation, M2 production soundtrack, merge or deployment in this increment.

Before executable changes: implement a bounded renderer for these approved recipe
profiles with a callable stub. Demonstrate failure of exact-approved-WAV PCM
comparisons and invalid-score rejection, then implement. Preserve existing renderer.
Profiles: lead-v1, duet-v1 and ensemble-v2. Input at most 1 MiB; 15–30 seconds;
1,000 total notes maximum; finite valid note times and integer MIDI pitches. Duet
supports at most two simultaneous lanes. Known profile determines gains/timbres;
no arbitrary execution or paths inside score. Reject existing output and malformed
scores. No backend or game runtime dependency on these development tools.

Checks: PYTHONDONTWRITEBYTECODE=1 /tmp/nightman-m1-tools/bin/python -m pytest
 tests/audio -q -p no:cacheprovider; python3 tools/check_audio.py assets/audio/previews;
 actual renderer CLI reproduces four approved WAV hashes in a new temporary folder;
 existing output unchanged on failure; malformed input rejection/recovery;
 git diff --check. Test failure evidence is recorded before implementing.

User listening decisions already establish recognition for these specific bytes;
code tests prove preservation, not hearing. NumPy 1.26.4 is the frozen ensemble
render dependency; the static game will consume exports rather than this tooling.
No UI introduced: screenshot evidence N/A. New commit needs its own independent
code reviewer, all prior reviewers revalidate final head, followed by separate
independent workflow/acceptance review. Mark ready only when all final-head gates
pass. Future M2 work adds original cues and updated placements under the latest
user direction; record that specification without composing them in this commit.
