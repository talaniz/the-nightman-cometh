"""Build a host-native portable bundle with reviewed production assets only."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def stage_assets(destination):
    from tools.build_web import validate_art
    from tools.audition import stage
    for source in validate_art():
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    with tempfile.TemporaryDirectory(prefix='nightman-audio-') as temporary:
        staged = Path(temporary) / 'stage'
        stage(ROOT / 'assets/audio/production/manifest.json', staged)
        shutil.copytree(staged / 'audio', destination / 'assets/audio/production')


def build(output):
    if sys.platform not in ('darwin', 'win32'):
        raise ValueError('Build on macOS or Windows; cross-compilation is not supported')
    if output.exists():
        raise ValueError('Choose a new output directory')
    output.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix='nightman-desktop-') as temporary:
        work = Path(temporary)
        stage_assets(work)
        command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
                   '--onedir', '--windowed', '--name', 'NightmanCometh',
                   '--paths', str(ROOT), '--distpath', str(output),
                   '--workpath', str(work / 'build'), '--specpath', str(work),
                   '--add-data', str(work / 'assets') + ':assets',
                   '--hidden-import', 'pygame._sdl2.controller',
                   '--exclude-module', 'game.fixtures']
        if sys.platform == 'darwin':
            command += ['--osx-bundle-identifier', 'local.nightmancometh.game',
                        '--target-architecture', platform.machine()]
        subprocess.run(command + [str(ROOT / 'tools/desktop/launch.py')], check=True)
    if sys.platform == 'darwin':
        shutil.rmtree(output / 'NightmanCometh')
    from tools.build_web import fingerprint
    files = {str(path.relative_to(output)): hashlib.sha256(path.read_bytes()).hexdigest()
             for path in sorted(output.rglob('*')) if path.is_file()}
    (output / 'build-manifest.json').write_text(json.dumps({
        'source_sha': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'source_fingerprint': fingerprint(), 'platform': sys.platform,
        'architecture': platform.machine(), 'files': files,
        'signed_for_distribution': False,
    }, indent=2))
    shutil.copyfile(ROOT / 'docs/desktop-testing.md', output / 'READ-ME.md')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    build(parser.parse_args().output.resolve())
