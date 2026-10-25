"""실제 게임 캡처를 같은 배율로 나열한 검토판. 게임 이미지는 수정하지 않는다."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import threading,sys
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'docs/reviews/ui-consistency-20261025'
version=sys.argv[2] if len(sys.argv)>2 else '0.20.40'
groups=[('01-options-meeting',[('02-settings','옵션 · 소리'),('15-settings-reading','옵션 · 읽기'),('16-settings-display','옵션 · 화면'),('17-meeting-dialogue','회의 · 대사'),('13-meeting','회의 · 자료 대조'),('12-meeting-retry','회의 재시도 · 화면 단독 표시'),('10-records','기록 / 자료')]),('02-story-ui',[('04-dialogue','대사'),('05-questions','질문 · 검토용 항목'),('06-choice','선택 · 검토용 항목'),('01-main','메인')]),('03-field-map',[('03-field','조사 · 여관'),('09-map-village','마을 지도'),('07-map-inn','여관 지도'),('08-map-forest','숲·산길 지도'),('11-forks','갈림길 · 검토용 진행 상태'),('14-meeting-touch','회의 · 터치 UI')])]
groups=[(name,[(stem,label) for stem,label in items if (root/(stem+'.png')).exists()]) for name,items in groups]
style='<meta charset="utf-8"><style>body{margin:0;background:#eee8dc;color:#29364b;font-family:sans-serif}main{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:8px}article{background:white}h3{font-size:20px;margin:0;padding:10px 14px}img{display:block;width:100%}a{color:inherit;text-decoration:none}header{font-size:24px;font-weight:bold;padding:16px}</style>'
for name,items in groups:
 body=''.join(f'<article><h3>{caption}</h3><a href="{stem}.png"><img src="{stem}.png"></a></article>' for stem,caption in items)
 (root/(name+'.html')).write_text(style+f'<header>다람탐정 {version} · 실제 UI 검토</header><main>'+body+'</main>')
(root/'index.html').write_text(style+'<header>다람탐정 · 전체 UI (이미지를 누르면 원본)</header>'+''.join('<main>'+''.join(f'<article><h3>{caption}</h3><a href="{stem}.png"><img src="{stem}.png"></a></article>' for stem,caption in items)+'</main>' for _,items in groups))
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1600,'height':1000},device_scale_factor=1)
 for name,_ in groups:
  page.goto(f'http://127.0.0.1:{server.server_port}/{name}.html')
  page.screenshot(path=str(root/(name+'.png')),full_page=True)
 b.close()
server.shutdown()
