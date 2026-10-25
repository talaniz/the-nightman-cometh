"""Stage and build the actual pygame/pygbag sound-check app; loopback hosting only."""
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


def stage(manifest_path, app):
    manifest_path=manifest_path.resolve()
    manifest=json.loads(manifest_path.read_text())
    app.mkdir()
    for name in ('main.py','director.py','backend.py'):
        shutil.copyfile(ROOT/'tools/audio/audition_app'/name,app/name)
    audio=app/'audio';audio.mkdir()
    for cue in manifest['cues'].values():
        name=cue['file']
        if not isinstance(name,str) or Path(name).name!=name or not name.endswith('.ogg'):
            raise ValueError('invalid asset filename')
        path=manifest_path.parent/name
        if path.is_symlink() or not path.is_file():raise ValueError('missing/linked asset')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=cue['sha256']:raise ValueError('asset hash mismatch')
        shutil.copyfile(path,audio/name)
    shutil.copyfile(manifest_path,audio/'manifest.json')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=ROOT/'assets/audio/production/manifest.json')
    parser.add_argument('--build',type=Path)
    args=parser.parse_args(argv)
    if args.build and (args.build.exists() or args.build.is_symlink()):
        parser.error('build output already exists; choose a new directory')
    with tempfile.TemporaryDirectory(prefix='nightman-audition-stage-') as temp:
        app=Path(temp)/'soundcheck';stage(args.manifest,app)
        if args.build:
            subprocess.run([sys.executable,'-m','pygbag','--build','--no_opt','--title','Nightman Sound Check',str(app)],check=True)
            shutil.copytree(app/'build/web',args.build)
            html=args.build/'index.html'
            style = """<style>body{background:#0f1320!important;color:#e5dec3;font:18px system-ui;margin:0}#narrow{display:none;padding:24px}canvas{max-width:100%;height:auto}#pyconsole,#crt{display:none!important} @media(max-width:600px){canvas,.emscripten_border,#transfer,#infobox{display:none!important}#narrow{display:block}}</style>"""
            narrow = '<aside id="narrow"><h1>Nightman sound check</h1><p>Use a desktop browser and keyboard to audition the soundtrack. Touch controls are not available.</p></aside>'
            content = html.read_text().replace('</head>',style+'</head>').replace('<body>','<body>'+narrow)
            # 0.9.3 CDN omits BrowserFS entirely (upstream issue #227).
            # Fetch the official archived copy, verify bytes, serve locally.
            with urllib.request.urlopen('https://pygame-web.github.io/archives/0.7/browserfs.min.js', timeout=30) as response:
                browserfs = response.read(300000)
            if hashlib.sha256(browserfs).hexdigest() != 'ba01fda78db31a7ba579afe74b8b56cf4636381ca1b6c54ffba20467756a627f':
                raise ValueError('upstream BrowserFS hash changed')
            (args.build/'browserfs.min.js').write_bytes(browserfs)
            shutil.copyfile(ROOT/'tools/audio/browserfs-LICENSE.txt',args.build/'browserfs-LICENSE.txt')
            content = content.replace('https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js','browserfs.min.js')
            content = content.replace('allow="autoplay; fullscreen *; geolocation; microphone; camera; midi; monetization; xr-spatial-tracking; gamepad; gyroscope; accelerometer; xr; cross-origin-isolated"','allow="autoplay"')
            content = content.replace('src="https://pygame-web.github.io/cdn/0.9.3/empty.html"','src="about:blank"')
            html.write_text(content)
            print(json.dumps({'ok':True,'build':str(args.build),'serve':'python -m http.server --bind 127.0.0.1 --directory '+str(args.build)}))
        else:
            subprocess.run([sys.executable,'main.py'],cwd=app,check=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
