import subprocess
import sys
from pathlib import Path

def test_preview_rejects_missing_root_and_public_bind(tmp_path):
    script=Path(__file__).resolve().parents[2]/'tools/serve_preview.py'
    result=subprocess.run([sys.executable,str(script),'--root',str(tmp_path)],capture_output=True,text=True)
    assert result.returncode==2 and 'index.html' in result.stderr
    result=subprocess.run([sys.executable,str(script),'--root',str(tmp_path),'--host','0.0.0.0'],capture_output=True,text=True)
    assert result.returncode==2 and 'invalid choice' in result.stderr
