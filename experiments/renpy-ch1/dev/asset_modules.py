"""제작자가 보는 UI/표정 납품 현황. 게임의 실제 연결 파일에서 재생성한다."""
import argparse,csv,html,json,sys,hashlib
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'game/python-packages'))
from r13_assets import Registry

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def inventory(project=PROJECT):
 game=project/'game';folder=game/'asset-toolbox'
 registry=Registry(load(folder/'catalog.json'),load(folder/'bindings.json'))
 rows=[]
 def row(module,role,person,state,path,error='',reference=None):
  exists=bool(path and (game/path).is_file());size=None
  if exists:
   try:
    with Image.open(game/path) as im:size=list(im.size)
   except Exception:pass
  digest=hashlib.sha256((game/path).read_bytes()).hexdigest() if exists else ''
  rows.append(dict(sha256=digest,module=module,role=role,person=person,state=state,status='연결됨' if exists and not error else '파일 없음' if path and not exists else '미연결',path=path or '',size=size,reference=reference or '',error=error,tags=[module,person,state]))
 for role,spec in registry.bindings['bindings'].items():
  if role.startswith('file:'):continue
  for state in spec.get('states',['basic']):
   try:resolved=registry.resolve(role,state);row('UI',role,'',state,resolved['path'])
   except Exception as e:row('UI',role,'',state,'',str(e))
 faces=load(game/'assets/room13-dialogue-b-faces.json')
 bodies=load(game/'assets/room13-fullbody-dialogue.json')
 for person in sorted(set(faces)|set(bodies['people'])):
  for module,states,images in [('대사 얼굴', ['neutral','joy','angry','anxious','surprise_talk','surprise_react'],faces.get(person,{})),('전신 표정',bodies.get('emotions',[]),bodies['people'].get(person,{}).get('images',{}))]:
   if person=='dad' and module=='대사 얼굴':continue
   reference=next((v if isinstance(v,str) else v['file'] for v in images.values()),'')
   for state in sorted(set(states)|set(images)):
    value=images.get(state);path=value if isinstance(value,str) else value.get('file') if value else ''
    row(module,f'{module}/{person}/{state}',person,state,path,reference=reference)
 return rows

def build(project=PROJECT):
 rows=inventory(project);out=project/'docs/asset-modules';out.mkdir(parents=True,exist_ok=True)
 previous=load(out/'inventory.json') if (out/'inventory.json').exists() else []
 before={r['role']+'@'+r['state']:r for r in previous}
 changes=[]
 for r in rows:
  old=before.get(r['role']+'@'+r['state'])
  if old and (old.get('path'),old.get('sha256'))!=(r['path'],r['sha256']):
   changes.append(dict(role=r['role'],state=r['state'],before=old.get('path'),after=r['path'],status=r['status']))
 if changes:(out/'latest-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
 stamp=datetime.now(timezone.utc).isoformat()
 handoff=(out/'HANDOFF.md').read_text() if (out/'HANDOFF.md').exists() else ''
 portal='<section><h2>다른 채팅에 전달할 작업 지시</h2><p>갱신 UTC: '+stamp+'</p><pre style="white-space:pre-wrap">'+html.escape(handoff)+'</pre><p><a href="latest-changes.json">최근 연결 변경</a> · <a href="deliveries.json">제작자 완료 보고 / 실제 게임 캡처</a></p><div id="deliveries"></div></section>'

 (out/'inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 fields=['module','role','person','state','status','path','size','reference','error']
 with (out/'requests.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(r for r in rows if r['status']!='연결됨')
 def esc(x):return html.escape(str(x))
 cards=[]
 for r in rows:
  preview=f'<img loading="lazy" src="../../game/{esc(r["path"])}">' if r['size'] else '<div class="empty">빈 슬롯</div>'
  cards.append(f'<article data-search="{esc(" ".join(map(str,r.values())))}" data-missing="{int(r["status"]!="연결됨")}"><b>{esc(r["role"])}</b><p>{esc(r["status"])} · {esc(r["size"] or "규격 미정")}</p>{preview}<p>파일: {esc(r["path"] or "미납품")}</p><p>참고 원본: {esc(r["reference"])}</p><p>{esc(r["error"])}</p></article>')
 missing=sum(r['status']!='연결됨' for r in rows)
 (out/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>다람탐정 에셋·표정 모듈</title><style>body{font:16px sans-serif;background:#fff5e4;color:#29364b;margin:24px}header{position:sticky;top:0;background:#fff5e4;padding:12px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}article{background:white;border:2px solid #29364b;border-radius:12px;padding:14px;overflow-wrap:anywhere}img{width:100%;height:180px;object-fit:contain;background:#ddd}input{padding:12px}.empty{height:90px;background:#f4d7d4;padding:20px}</style><header><h1>에셋·캐릭터 표정 도구함</h1>'''+f'<p>전체 {len(rows)} 슬롯 · 미연결/파일 없음 {missing}개. 미연결은 제작 승인 여부와 다릅니다. 중립 얼굴 등 의도적으로 비운 슬롯도 포함합니다.</p>'+portal+'''<p><a href="requests.csv">빈 슬롯 요청서 CSV</a> · <a href="inventory.json">전체 태그/연결 JSON</a> · <a href="HANDOFF.md">다른 채팅용 원문</a> · <a href="GUIDE.md">채우는 방법</a></p><input id="search" placeholder="캐릭터 / 표정 / 역할 검색"><label><input id="missing" type="checkbox">빈 슬롯만</label></header><main>'''+''.join(cards)+'''</main><script>function filter(){let q=document.querySelector('#search').value.toLowerCase(),m=document.querySelector('#missing').checked;document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.search.toLowerCase().includes(q)||(m&&a.dataset.missing!='1'))}fetch('deliveries.json').then(r=>r.json()).then(rows=>{const box=document.querySelector('#deliveries');rows.forEach(r=>{let p=document.createElement('p');p.textContent=[r.role,r.status,r.note].join(' · ');if(r.capture&&!r.capture.includes(':')&&!r.capture.startsWith('//')){let a=document.createElement('a');a.textContent=' 실제 게임 캡처';a.href=r.capture;p.append(a)}box.append(p)})});document.querySelector('#search').oninput=filter;document.querySelector('#missing').onchange=filter;</script>''')
 print(f'{len(rows)}개 슬롯 / 빈 슬롯 {missing}개 → {out}/index.html')
if __name__=='__main__':build()
