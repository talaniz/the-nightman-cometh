"""Loopback-only static preview; foreground, --background and --stop modes."""
import argparse
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

class Handler(SimpleHTTPRequestHandler):
    def list_directory(self,path):self.send_error(403,'Directory listing disabled')
    def do_GET(self):
        if any(p.startswith('.') for p in urllib.parse.unquote(self.path.split('?')[0]).split('/') if p):
            self.send_error(404);return
        super().do_GET()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True);ap.add_argument('--host',choices=['127.0.0.1','localhost'],default='127.0.0.1')
    ap.add_argument('--port',type=int,default=8765)
    group=ap.add_mutually_exclusive_group();group.add_argument('--background',action='store_true');group.add_argument('--stop',action='store_true')
    args=ap.parse_args();root=args.root.resolve()
    if not 1024<=args.port<=65535:ap.error('Use an unprivileged port 1024..65535')
    key=hashlib.sha256((str(root)+str(args.port)).encode()).hexdigest()[:16]
    record=Path(tempfile.gettempdir())/('nightman-preview-'+key+'.json')
    url=f'http://127.0.0.1:{args.port}/'
    if args.stop:
        if not record.exists():ap.exit(1,'No recorded preview for this root and port\n')
        data=json.loads(record.read_text());pid=data['pid']
        try:cmd=Path(f'/proc/{pid}/cmdline').read_bytes().decode().split('\0')
        except FileNotFoundError:record.unlink();return
        if str(Path(__file__).resolve()) not in cmd or str(root) not in cmd:ap.exit(1,'Recorded PID no longer belongs to this preview\n')
        os.kill(pid,signal.SIGTERM);record.unlink();print('Stopped '+url);return
    if not (root/'index.html').is_file():ap.error('Build directory must contain index.html')
    if args.background:
        if record.exists():ap.exit(1,'Preview record exists; stop it before starting another')
        # Probe bind before spawning; child still handles the race independently.
        import socket
        with socket.socket() as probe:
            try:probe.bind(('127.0.0.1',args.port))
            except OSError:ap.exit(1,'Preview port is already in use\n')
        log=record.with_suffix('.log')
        with log.open('ab') as stream:
            process=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--root',str(root),'--port',str(args.port)],stdin=subprocess.DEVNULL,stdout=stream,stderr=stream,start_new_session=True)
        for _ in range(50):
            if process.poll() is not None:ap.exit(1,'Preview failed; see '+str(log)+'\n')
            try:
                with urllib.request.urlopen(url,timeout=.3) as response:
                    if response.status==200:break
            except OSError:time.sleep(.1)
        else:
            process.terminate();ap.exit(1,'Preview readiness timed out\n')
        record.write_text(json.dumps({'pid':process.pid,'root':str(root),'port':args.port}))
        print(url+' ready; stop with --stop using the same root/port');return
    try:server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(root)))
    except OSError:ap.exit(1,'Preview port is already in use\n')
    print(url,flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=='__main__':main()
