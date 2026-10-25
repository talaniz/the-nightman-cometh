"""Verify the game source fingerprint and all committed M3 evidence hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.build_web import fingerprint

def verify(path):
    manifest=json.loads(path.read_text())
    if manifest['source_fingerprint']!=fingerprint():raise ValueError('Evidence source fingerprint is stale')
    root=path.parent.resolve()
    if not manifest['captures']:raise ValueError('No screenshots')
    for item in manifest['captures']:
        relative=Path(item['file'])
        if relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsafe evidence path')
        p=root/relative
        if p.is_symlink() or not p.is_file():raise ValueError('Missing or linked evidence')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Evidence hash mismatch')
    if manifest['unexpected_errors']:raise ValueError('Unresolved browser errors')
    return len(manifest['captures'])

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('manifest',type=Path);args=ap.parse_args()
    try:print(str(verify(args.manifest))+' screenshots verified against current source')
    except (OSError,ValueError,KeyError) as exc:ap.exit(1,str(exc)+'\n')
