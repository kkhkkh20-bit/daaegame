"""Keep the web presplash consistent with the in-game title, using exact assets."""
from pathlib import Path
import re,shutil,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
# 2026-10-27 소유자: "로딩창 이미지 바꿔줘야지 예전 다람탐정 나오잖아."
# 앞 것은 dev/make_loading_scene.py 가 메인화면(엽서+로고+포스터)과 같은 구성으로 합친 그림이고,
# 뒤 것은 그 파일이 없을 때 떨어지는 예전 타이틀이다. 둘 다 없으면 로딩창을 건드리지 않는다.
LOADING_ART=('assets/room13-loading-scene.webp','assets/room13-title-winter020.webp')
def loading_art(game):
 for rel in LOADING_ART:
  if (Path(game)/rel).exists():return Path(game)/rel
def update_title_loader(release,game):
 release=Path(release);game=Path(game)
 art=loading_art(game)
 if art is None:return
 shutil.copy2(art,release/'loading-scene.webp')
 # The approved logo is part of the cover plate, so do not double it on load.
 (release/'loading-logo.webp').unlink(missing_ok=True)
 p=release/'index.html';s=p.read_text().replace('src="loading-scene.png"','src="loading-scene.webp"')
 style='<style id="r13-title-loader">'+(ROOT/'dev/title-loader.css').read_text()+'</style>'
 if 'id="r13-title-loader"' in s:s=re.sub(r'<style id="r13-title-loader">.*?</style>',lambda m:style,s,flags=re.S)
 else:s=s.replace('</head>',style+'\n</head>',1)
 # 음악 안내 줄은 숨긴 채 넣는다. 브라우저가 자동재생을 거부했을 때만 title-loader-audio.js 가 편다 —
 # 소리가 이미 나는 재방문에서 "누르면 켜진다"고 쓰여 있으면 거짓말이 된다.
 brand=('<div id="loading-brand"><h1 class="title-accessible">다람탐정</h1><p class="loading-hint">마을의 문을 여는 중…</p>'
        '<p class="loading-audio-hint" hidden>화면을 한 번 누르면 음악이 켜집니다</p></div>')
 s,n=re.subn(r'<div id="loading-brand">.*?</div>',lambda m:brand,s,count=1,flags=re.S);assert n==1
 music_hash=hashlib.sha256((game/'assets/bgm-title.mp3').read_bytes()).hexdigest()[:12]
 audio_script='<script id="r13-loading-audio">'+(ROOT/'dev/title-loader-audio.js').read_text().replace('__MUSIC_HASH__',music_hash)+'</script>'
 s=re.sub(r'[ \t]*<script id="r13-loading-audio">.*?</script>[ \t]*\n?', '', s, flags=re.S)
 s=s.replace('<script src="renpy-pre.js',audio_script+'\n<script src="renpy-pre.js',1)
 p.write_text("\n".join(line.rstrip() for line in s.splitlines())+"\n")
 catalog=release/'pwa_catalog.json';j=json.loads(catalog.read_text())
 for f in ('loading-scene.webp','Galmuri11.woff2','Galmuri-OFL.txt'):
  if f not in j['files']:j['files'].append(f)
 catalog.write_text(json.dumps(j))
 # The packaging helper refreshes all manifest hashes after this call.
 manifest=release/'build-manifest.json';j=json.loads(manifest.read_text())
 for f in ('loading-scene.webp','Galmuri11.woff2','Galmuri-OFL.txt'):j['files'].setdefault(f,{})
 manifest.write_text(json.dumps(j,indent=2))
