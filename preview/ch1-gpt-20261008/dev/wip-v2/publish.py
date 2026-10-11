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
# Cover iframe navigation with the exact same loader as the payload, including
# the shell's portrait rotation. The child hands over as soon as its own loader
# exists; actual game readiness stays owned by the native boot routine.
wrapper = wrapper.replace('#0E1128', '#211b16')
boot_css = (SOURCE / 'boot_theme.css').read_text()
boot_markup = (SOURCE / 'boot_theme.html').read_text()
wrapper = wrapper.replace('</head>', '<style>'+boot_css+'\n#inn-boot{position:absolute;transform-origin:0 0}\n@font-face{font-family:Galmuri11;src:url(art/ui/galmuri11.woff2) format("woff2");font-display:swap}</style></head>')
wrapper = wrapper.replace('</iframe></div>', '</iframe><div id="inn-boot">'+boot_markup+'</div></div>')
wrapper = wrapper.replace("pending=0,last='';", "pending=0,last='',boot=document.getElementById('inn-boot');\n  function handoff(){if(boot){boot.remove();boot=null}}\n  window.addEventListener('message',function(e){if(e.source===frame.contentWindow&&e.origin===location.origin&&e.data&&e.data.type==='inn-v2-boot-ready')handoff()});\n  frame.addEventListener('load',function(){try{if(frame.contentDocument&&frame.contentDocument.getElementById('app'))handoff()}catch(e){}});")
wrapper = wrapper.replace("surface.dataset.rotated=rotated?'true':'false';", "if(boot){boot.style.width=frame.style.width;boot.style.height=frame.style.height;boot.style.transform=frame.style.transform}\n    surface.dataset.rotated=rotated?'true':'false';")
assert 'id="inn-boot"' in wrapper and "boot.style.transform=frame.style.transform" in wrapper
(PREVIEW / 'play_v2.html').write_bytes(payload)
(PREVIEW / 'v2.html').write_text(wrapper)
print(f'Pages files ready: https://kkhkkh20-bit.github.io/daaegame/preview/ch1-gpt-20261008/v2.html?v={version}')
