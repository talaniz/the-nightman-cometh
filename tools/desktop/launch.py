"""Desktop entrypoint; no local server and no runtime network dependencies."""
import asyncio
import sys
from pathlib import Path

# Source execution and the PyInstaller bundle share this package layout.
if not getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def verify_progress(storage):
    from game.session import Session
    from game.desktop import FileStorage
    session = Session(storage)
    if not session.progress.save(session.world):
        raise RuntimeError('Save write failed')
    restored = Session(FileStorage(storage.path))
    if not restored.progress.saved or restored.progress.saved != session.progress.saved:
        raise RuntimeError('Save did not survive restart')
    return session


def verify_install(destination):
    """Explicit installation diagnostic, never a gameplay/physical-audio acceptance."""
    import json
    import platform
    import tempfile
    import pygame
    from game.main import initialize_display
    from game.render import Renderer
    from game.session import Session
    from game.desktop import FileStorage
    from game.audio import gameplay_manifest
    from tools.audio.audition_app.backend import Mixer
    from tools.audio.audition_app.director import Director
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    screen = initialize_display()
    renderer = Renderer(screen)
    root = renderer.art.root / 'audio' / 'production'
    manifest = json.loads((root / 'manifest.json').read_text())
    mixer = Mixer(manifest, root)
    audio = Director(gameplay_manifest(manifest), mixer)
    audio.unlock()
    for cue in manifest['cues']:
        mixer._sound(cue)
    with tempfile.TemporaryDirectory(prefix='nightman-install-') as directory:
        storage = FileStorage(Path(directory) / 'progress.json')
        session = verify_progress(storage)
        renderer.draw(session, audio)
        pygame.image.save(screen, str(destination / 'title.png'))
        session.enter_screen('options')
        renderer.draw(session, audio)
        pygame.image.save(screen, str(destination / 'options.png'))
    (destination / 'installation.json').write_text(json.dumps({
        'platform': sys.platform, 'architecture': platform.machine(),
        'python': platform.python_version(), 'pygame': pygame.version.ver,
        'decoded_cues': len(manifest['cues']), 'save_restart': True,
        'limits': 'Installation diagnostic only; no full route, physical audio or USB test.'
    }, indent=2))
    pygame.quit()


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--verify-install':
        try:
            verify_install(sys.argv[2])
        except Exception as error:
            if sys.stderr is not None:
                print('Installation verification failed: ' + str(error), file=sys.stderr)
            raise SystemExit(1)
    elif len(sys.argv) == 1:
        from game.main import main
        try:
            asyncio.run(main())
        finally:
            import pygame
            pygame.quit()
    else:
        raise SystemExit('Usage: NightmanCometh [--verify-install OUTPUT_DIRECTORY]')
