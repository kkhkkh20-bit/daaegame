"""Keep the web presplash consistent with the in-game title, using exact assets."""
from pathlib import Path
import re,shutil,json
ROOT=Path(__file__).resolve().parents[1]
def update_title_loader(release,game):
 release=Path(release);game=Path(game)
 art=game/'assets/room13-title-fairytale084.webp'
 if not art.exists():return
 shutil.copy2(art,release/'loading-scene.webp')
 shutil.copy2(game/'assets/room13-title-logo.webp',release/'loading-logo.webp')
 p=release/'index.html';s=p.read_text().replace('src="loading-scene.png"','src="loading-scene.webp"')
 style='<style id="r13-title-loader">'+(ROOT/'dev/title-loader.css').read_text()+'</style>'
 if 'id="r13-title-loader"' in s:s=re.sub(r'<style id="r13-title-loader">.*?</style>',lambda m:style,s,flags=re.S)
 else:s=s.replace('</head>',style+'\n</head>',1)
 brand='<div id="loading-brand"><h1><img src="loading-logo.webp" alt="다람탐정"></h1><p class="loading-hint">마을의 문을 여는 중…</p></div>'
 s,n=re.subn(r'<div id="loading-brand">.*?</div>',lambda m:brand,s,count=1,flags=re.S);assert n==1
 p.write_text(s)
 catalog=release/'pwa_catalog.json';j=json.loads(catalog.read_text())
 for f in ('loading-scene.webp','loading-logo.webp','Galmuri11.woff2','Galmuri-OFL.txt'):
  if f not in j['files']:j['files'].append(f)
 catalog.write_text(json.dumps(j))
 # The packaging helper refreshes all manifest hashes after this call.
 manifest=release/'build-manifest.json';j=json.loads(manifest.read_text())
 for f in ('loading-scene.webp','loading-logo.webp','Galmuri11.woff2','Galmuri-OFL.txt'):j['files'].setdefault(f,{})
 manifest.write_text(json.dumps(j,indent=2))
