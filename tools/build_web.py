"""Build the static pygame game into a new directory; never overwrite a build."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

ART_ROOTS=('sprites','backgrounds','ui','scenes')

def art_files():
    paths=[]
    for name in ART_ROOTS:
        root=ROOT/'assets'/name
        if root.is_symlink():raise ValueError('Linked production art is not allowed')
        if root.exists():
            for path in sorted(root.rglob('*')):
                if path.is_symlink():raise ValueError('Linked production art is not allowed')
                if path.is_file() and path.suffix.lower() in ('.png','.json','.ttf','.otf'):
                    paths.append(path)
    return paths

def validate_art():
    import pygame
    files=art_files()
    required=('sprites/cast.png','scenes/act1/opening.png',
              'scenes/act1/kidnapping.png','backgrounds/act1/street.png','ui/kitten-mittens.png',
              'ui/kitten-billboard.png','ui/wolf-billboard.png','ui/sherwin-sign.png',
              'sprites/enemy-walk.png','sprites/nail-bat.png','sprites/bat-attack.png',
              'sprites/bridge.png','backgrounds/act2/bridge.png','scenes/act2/story.png','ui/bridge-ads.png')
    for relative in required:
        path=ROOT/'assets'/relative
        if path not in files:raise ValueError('Missing required art: '+relative)
        try:
            image=pygame.image.load(str(path))
            if image.get_width()<64 or image.get_height()<64:raise ValueError('image too small')
            if relative.startswith('sprites/') and not image.get_masks()[3]:raise ValueError('sprite atlas lacks alpha')
        except (pygame.error,OSError,ValueError) as exc:
            raise ValueError('Invalid art: '+relative) from exc
    return files

def fingerprint():
    paths=sorted([*art_files(),*ROOT.joinpath('game').rglob('*.py'),*ROOT.joinpath('game/web').glob('*'),
                  ROOT/'tools/build_web.py',ROOT/'pyproject.toml',ROOT/'requirements.lock',ROOT/'assets/audio/production/manifest.json',
                  ROOT/'tools/audio/audition_app/backend.py',ROOT/'tools/audio/audition_app/director.py'])
    return hashlib.sha256(''.join(str(p.relative_to(ROOT))+hashlib.sha256(p.read_bytes()).hexdigest() for p in paths).encode()).hexdigest()

def build(output,test_fixtures=False):
    if output.exists() or output.is_symlink():raise ValueError('Choose a new output directory')
    validated_art=validate_art()
    with tempfile.TemporaryDirectory(prefix='nightman-build-') as temp:
        app=Path(temp)/'nightman';app.mkdir()
        shutil.copytree(ROOT/'game',app/'game',ignore=shutil.ignore_patterns('__pycache__'))
        if not test_fixtures:(app/'game/fixtures.py').unlink(missing_ok=True)
        else:(app/'test-fixtures.json').write_text('{}')
        (app/'main.py').write_text('import asyncio\nimport pygame  # pygbag dependency scanner needs top-level imports\nfrom game.main import main\nasyncio.run(main())\n')
        for asset in validated_art:
            target=app/asset.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(asset,target)
        # Reuse the reviewed M2 mixer/director verbatim; no parallel mixer fork.
        dest=app/'tools/audio/audition_app';dest.mkdir(parents=True)
        for name in ['backend.py','director.py']:shutil.copyfile(ROOT/'tools/audio/audition_app'/name,dest/name)
        from tools.audition import stage
        audio_stage=Path(temp)/'audio-stage';stage(ROOT/'assets/audio/production/manifest.json',audio_stage)
        shutil.copytree(audio_stage/'audio',app/'audio')
        subprocess.run([sys.executable,'-m','pygbag','--build','--no_opt','--title','The Nightman Cometh',str(app)],check=True)
        web=app/'build/web'
        with urllib.request.urlopen('https://pygame-web.github.io/archives/0.7/browserfs.min.js',timeout=30) as response:browserfs=response.read(300000)
        if hashlib.sha256(browserfs).hexdigest()!='ba01fda78db31a7ba579afe74b8b56cf4636381ca1b6c54ffba20467756a627f':raise ValueError('BrowserFS hash mismatch')
        (web/'browserfs.min.js').write_bytes(browserfs)
        shutil.copyfile(ROOT/'tools/audio/browserfs-LICENSE.txt',web/'browserfs-LICENSE.txt')
        for p in (ROOT/'game/web').iterdir():shutil.copyfile(p,web/p.name)
        html=(web/'index.html').read_text()
        early='''<script>if(location.hostname==='localhost'){const u=new URL(location.href);u.hostname='127.0.0.1';location.replace(u.href);}</script><script src="boot-state.js"></script><script src="loader.js"></script>'''
        html=html.replace('<script src=',early+'<script src=',1)
        html=html.replace('</head>','<link rel="stylesheet" href="style.css"></head>')
        html=html.replace('<body>','''<body><section id="loader" aria-live="polite"><h1>The Nightman Cometh</h1><p id="boot-status">Loading the stage…</p><button id="boot-action" disabled>Loading runtime…</button><p>Desktop keyboard · Internet required for runtime</p></section><aside id="narrow"><h1>The Nightman Cometh</h1><p>Use a desktop browser and keyboard to play. Touch controls are not available.</p></aside><p id="controls">Arrows / A,D move · Space jump · J bat · K sunbeam · Enter confirm · Esc pause</p>''')
        html=html.replace('https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js','browserfs.min.js')
        html=html.replace('src="https://pygame-web.github.io/cdn/0.9.3/empty.html"','src="about:blank"')
        import re
        html=re.sub(r'allow="autoplay;[^"]*"','allow="autoplay"',html)
        (web/'index.html').write_text(html)
        manifest={'source_fingerprint':fingerprint(),'python':sys.version,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(web.iterdir()) if p.is_file()}}
        (web/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        shutil.copytree(web,output)
    return manifest

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--test-fixtures',action='store_true')
    args=ap.parse_args()
    try:build(args.output,args.test_fixtures)
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:ap.exit(1,str(exc)+'\n')
    print('Built '+str(args.output))
