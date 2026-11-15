# Corrected desktop package verification — add35aa

Runtime source: `add35aa1af49fcb47c4cd1dedb36b974d247c8a6`.
[Remote build and diagnostic run43657884551](https://github.com/talaniz/the-nightman-cometh/actions/runs/43657884551)
passed Windows x64, macOS arm64 and macOS Intel. Each launched the bundled executable from
an unrelated working directory with SDL dummy drivers, decoded24 production cues, restored
saved progress in a fresh Session, rejected missing/corrupt audio, restored the bytes and
passed a fresh diagnostic before ZIP creation. These are installation checks, not full
packaged playthroughs, physical audio/controller or Finder/Explorer launch acceptance.

All three downloaded archive SHA256 values were verified locally. All177 Windows manifest
members also matched. Mac fingerprints match the reviewed POSIX runtime; the existing
fingerprint includes platform path separators, so Windows/POSIX values are not directly
comparable. CI manifests record the actual PR merge checkout SHA; manifest.json identifies
the reviewed branch head separately. No source WAV/QA fixtures were staged.

Main and independent E2E reviewer visually inspected all six960x540 actual-package title
and options captures. No private data or visual defects observed. Reproduce via desktop.yml
at this runtime source, invoking the built executable with `--verify-install OUTPUT`.

| Target | Title | Options | Diagnostic |
|---|---|---|---|
| Windows x64 | [Title](windows-x64-test-package/title.png) | [Options](windows-x64-test-package/options.png) | [Result](windows-x64-test-package/installation.json) |
| Mac Apple Silicon | [Title](macos-arm64-test-package/title.png) | [Options](macos-arm64-test-package/options.png) | [Result](macos-arm64-test-package/installation.json) |
| Mac Intel | [Title](macos-x86_64-test-package/title.png) | [Options](macos-x86_64-test-package/options.png) | [Result](macos-x86_64-test-package/installation.json) |

Unsigned test candidates only. Retention-limited CI artifacts were copied to ignored
`build/desktop-candidates/add35aa` for durable local handoff through the existing private
SSH preview. No public release, signing purchase or merge. Physical USB and target-machine
GUI/listening remain mandatory open gates. The final qualifying run/video sequence is not
claimed complete by these installation results.
