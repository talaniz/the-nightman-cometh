# Historical native package verification — e7cfee7

Runtime source: e7cfee7e7c3f5d5e8797f68a8cc9e5dc8af4560a. Build/run:
[43655723064](https://github.com/talaniz/the-nightman-cometh/actions/runs/43655723064).
Each platform built on its own runner, launched its bundled executable from an unrelated
working directory using `--verify-install`, decoded all24 production cues, and restored
progress in a new Session. Missing and corrupt proposal audio were rejected; original
bytes were restored and a fresh successful check preceded archiving. These are isolated
installation diagnostics using SDL dummy drivers, not full packaged gameplay or listening.

CI checks out the PR synthetic merge commit; manifest records that actual source SHA.
`runtime_head` identifies the reviewed branch source. Source fingerprints are host-dependent
(the existing function includes native path separators); do not compare Windows and POSIX
fingerprints as if identical. macOS runtime fingerprint matches the Linux reviewed tree.
All three archive SHA256 checks passed locally; Windows archive member hashes match its
build manifest. No source WAV audio or QA fixtures were staged. Packages are unsigned test
candidates, not Developer ID notarized or publicly released.

Screenshots are actual960x540 native renders. Main and independent E2E reviewer visually
inspected all6; no private data observed. Menu hint backing is readable. These supplement
actual native input-loop review; they do not replace target-machine GUI/hardware checks.
Reproduction: workflow desktop.yml at this source, build then `NightmanCometh
--verify-install OUTPUT` with dummy SDL. Archive hashes and image hashes: manifest.json.

| Target | Title | Options | Diagnostic |
|---|---|---|---|
| Windows x64 | [Title](windows/title.png) | [Options](windows/options.png) | [Result](windows/installation.json) |
| Mac Apple Silicon | [Title](mac-arm/title.png) | [Options](mac-arm/options.png) | [Result](mac-arm/installation.json) |
| Mac Intel | [Title](mac-intel/title.png) | [Options](mac-intel/options.png) | [Result](mac-intel/installation.json) |

These packages were superseded by the credits contrast correction add35aa. They are
historical installation evidence, not the final candidate. Physical USB, target GUI,
listening and final qualifying run/video acceptance remain open.
