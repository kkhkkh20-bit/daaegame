"""Build approved v2 Pages files; preserve the existing public game and QA build."""
from pathlib import Path
import hashlib
import subprocess
import sys

SOURCE = Path(__file__).resolve().parent
PREVIEW = SOURCE.parent.parent
subprocess.run([sys.executable, str(SOURCE / 'build.py')], check=True)
payload = (SOURCE / 'build/play_v2.html').read_bytes()
assert b'window.__T=function' not in payload, 'QA evaluation hook must not be published'
version = hashlib.sha256(payload).hexdigest()[:12]
wrapper = (PREVIEW / 'index.html').read_text()
old = "frame.src='play.html'+(q?'?'+q:'')"
assert wrapper.count(old) == 1, 'Review the updated public wrapper before publishing v2'
wrapper = wrapper.replace(old, f"frame.src='play_v2.html?build={version}'+(q?'&'+q:'')")
wrapper = wrapper.replace('<link rel="manifest" href="manifest.webmanifest">\n', '')
wrapper = wrapper.replace('<title>다람탐정 · 1장 열세 번째 침대</title>', '<title>다람탐정 · 1장 v2 미리보기</title>')
(PREVIEW / 'play_v2.html').write_bytes(payload)
(PREVIEW / 'v2.html').write_text(wrapper)
print(f'Pages files ready: https://kkhkkh20-bit.github.io/daaegame/preview/ch1-gpt-20261008/v2.html?v={version}')
