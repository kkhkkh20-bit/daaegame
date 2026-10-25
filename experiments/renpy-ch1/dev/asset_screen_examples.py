"""현재 소스로 실제 게임 화면을 캡처해 제작자용 공개 예시를 생성한다."""
import argparse,hashlib,html,json,re,shutil,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
from asset_modules import PROJECT
from asset_toolbox_preview import _fingerprint
SCREENS=[('01-main','메인'),('04-dialogue','대사'),('05-questions','질문'),('06-choice','선택'),('03-field','조사'),('09-map-village','마을 지도'),('07-map-inn','여관 지도'),('08-map-forest','숲 지도'),('02-settings','옵션 소리'),('15-settings-reading','옵션 읽기'),('16-settings-display','옵션 화면'),('17-meeting-dialogue','회의 대사'),('13-meeting','회의 자료'),('10-records','기록'),('11-forks','갈림길')]
BASE='https://kkhkkh20-bit.github.io/daaegame/experiments/renpy-ch1/docs/asset-modules/screens/'
def capture(project=PROJECT):
 import review_ui_consistency as first
 import review_ui_meeting as second
 from asset_toolbox_preview import _fingerprint
 before=_fingerprint(project/'game')
 # Importing fixtures mutates the common runner, so choose each fixture explicitly.
 with tempfile.TemporaryDirectory(prefix='daram-screen-examples-') as tmp:
  tmp=Path(tmp)
  import importlib
  first=importlib.reload(first);first.runner.capture(project,tmp/'main')
  second=importlib.reload(second);second.r.capture(project,tmp/'meeting')
  if before!=_fingerprint(project/'game'):raise RuntimeError('캡처 중 게임 소스가 바뀌었습니다. 다시 실행하세요.')
  out=project/'docs/asset-modules/screens';out.mkdir(parents=True,exist_ok=True)
  if (out/'manifest.json').exists():
   previous=out/'previous';previous.mkdir(exist_ok=True)
   for old in list(out.glob('*.png'))+[out/'manifest.json']:shutil.copy2(old,previous/old.name)
  for folder in ('main','meeting'):
   for image in (tmp/folder).glob('*.png'):shutil.copy2(image,out/image.name)
  version=re.search(r'config.version\s*=\s*["\']([^"\']+)',(project/'game/options.rpy').read_text()).group(1)
  commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=project,text=True).strip()
  dirty=bool(subprocess.check_output(['git','diff','--','game'],cwd=project,text=True))
  entries=[]
  for stem,label in SCREENS:
   path=out/(stem+'.png')
   if not path.exists():raise RuntimeError('필수 캡처 누락: '+str(path))
   sha=hashlib.sha256(path.read_bytes()).hexdigest()
   entries.append(dict(id=stem,label=label,file=path.name,image_url=BASE+path.name+'?v='+sha[:12],sha256=sha,width=1280,height=720))
  manifest=dict(kind='actual-game-capture',version=version,commit=commit,local_game_changes=dirty,captured_at=datetime.now(timezone.utc).isoformat(),source_fingerprint=before,note='격리된 실제 게임 렌더입니다. QA 진행 상태/질문·선택 예시 문구를 사용하며 자연 플레이 검증은 아닙니다. 공개 게임과 로컬 변경 여부를 확인하세요.',screens=entries)
  (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  intro=f'실제 게임 캡처 · {html.escape(version)} · '+('로컬 UI 수정 포함' if dirty else '커밋 소스')+' · '+manifest['captured_at']
  cards=''.join(f'<article><h2>{html.escape(e["label"])}</h2><a href="{e["file"]}"><img loading="lazy" src="{e["file"]}"></a><p><a href="{e["image_url"]}">이미지 직접 주소</a></p></article>' for e in entries)
  comparisons=''.join('<article><h2>'+html.escape(label)+' · 이전 / 현재</h2><div style="display:flex"><img style="width:50%" src="previous/'+stem+'.png"><img style="width:50%" src="'+stem+'.png"></div></article>' for stem,label in SCREENS) if (out/'previous/manifest.json').exists() else '<p>첫 캡처입니다. 다음 캡처부터 이전/현재 비교가 표시됩니다.</p>'
  cards=comparisons+cards
  (out/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>실제 게임 화면 예시</title><style>body{font:16px sans-serif;background:#eef1f6;color:#243249;margin:16px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,480px),1fr));gap:16px}article{background:white;padding:12px}img{width:100%}p{overflow-wrap:anywhere}</style><a href="../">에셋 도구함</a><h1>실제 적용 화면</h1><p>'+intro+'</p><p>'+html.escape(manifest['note'])+'</p><a href="manifest.json">다른 채팅용 화면 목록 JSON · 버전/해시/직접 이미지 주소</a><main>'+cards+'</main>')
  (out/'README.md').write_text('# 실제 게임 화면 예시\n\n'+intro+'\n\n'+manifest['note']+'\n\n'+ '\n\n'.join('## '+e['label']+'\n\n![화면]('+e['file']+')\n\n'+e['image_url'] for e in entries))
  print('실제 화면 '+str(len(entries))+'개 캡처/메타데이터 생성 완료')
if __name__=='__main__':capture()
