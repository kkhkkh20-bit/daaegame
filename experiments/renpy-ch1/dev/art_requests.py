"""현재 파일·연결 근거를 포함한 미납품 그림 요청 포털을 재생성한다.

python3 dev/art_requests.py [--check]
편집 원본: docs/art-requests/manifest.json. 외부 전송이나 이미지 생성 없음.
"""
import argparse,csv,io,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/art-requests'
def reference(path):
 p=ROOT/path
 if not p.is_file():raise ValueError('참조 파일 없음: '+path)
 result={'path':path,'exists':True}
 try:
  with Image.open(p) as im:
   result.update(width=im.width,height=im.height,mode=im.mode,alpha_channel='A' in im.getbands())
   if 'A' in im.getbands():result['has_transparent_pixels']=im.getchannel('A').getextrema()[0]<255
 except (OSError,ValueError):pass
 return result

def request_md(r,statuses):
 link=lambda p:'['+p+'](../../'+p+')'
 lines=['# '+r['id']+' — '+r['title'],'','상태: '+statuses[r['status']]+' / 우선순위: '+r['priority'],'',r['description'],'','승인 범위: '+r['approved_scope'],'','용도·장면: '+', '.join(r['scenes']),'분기: '+', '.join(r['branches']),'','## 보여 줄 것','']
 lines+=['- '+s for s in r['required']]+['','## 피할 것','']+['- '+s for s in r['avoid']]
 lines+=['','## 납품 계약','',r['contract']['size_rule'],'','- 투명 배경: '+('필요' if r['contract']['transparent'] else '배경 전체 그림은 불투명') ,'- 상태: '+', '.join(r['contract']['states']),'- 납품: '+', '.join(r['contract']['delivery']),'','### 현행 레퍼런스 실측','']
 for ref in r['reference_details']:
  size=(' — '+str(ref['width'])+'×'+str(ref['height'])+' / '+ref['mode']+(' / 투명 픽셀 있음' if ref.get('has_transparent_pixels') else '')) if 'width' in ref else ''
  lines.append('- '+link(ref['path'])+size)
 lines+=['','## 인수 확인','']+['- [ ] '+s for s in r['acceptance']]+['','## 근거','']+['- '+link(p) for p in r['sources']]
 return '\n'.join(lines)+'\n'

def build():
 data=json.loads((OUT/'manifest.json').read_text());ids=set()
 for r in data['requests']:
  if r['id'] in ids:raise ValueError('중복 ID: '+r['id'])
  ids.add(r['id']);r['reference_details']=[reference(p) for p in r['references']]
  for p in r['sources']:reference(p)
  r['markdown']=request_md(r,data['statuses'])
 for e in data['excluded']:reference(e['source'])
 data['summary']={k:sum(r['status']==k for r in data['requests']) for k in data['statuses']}
 intro=['# 그림 제작 요청서','',data['as_of']+' 현재 파일·등록 코드 대조. 이 문서를 외부에 전달하거나 그림을 생성하지 않았다.','',data['scope'],'','## 중복 요청 방지','']+['- '+p for p in data['policies']]
 intro+=['','## 현황','']+['- '+data['statuses'][k]+': '+str(n)+'건' for k,n in data['summary'].items()]
 intro+=['','기본 제작 검토 목록은 전용 그림 미납품과 납품·제작 필요 확인 항목이다. 납품된 배경/자료/인물은 아래 대조 이력에 남기며 새 제작 요청에서 제외한다.','']
 md='\n'.join(intro)+'\n\n'+'\n\n---\n\n'.join(r['markdown'] for r in data['requests'])+'\n\n## 그림 요청에서 제외한 과거 화면 작업\n\n'+'\n'.join('- '+e['id']+': '+e['reason'] for e in data['excluded'])+'\n'
 data['all_markdown']=md
 sio=io.StringIO(newline='');w=csv.writer(sio,lineterminator="\n");w.writerow(['id','priority','status','title','kind','scenes','branches','states','transparent','size_rule','references','sources','required','avoid','acceptance'])
 for r in data['requests']:w.writerow([r['id'],r['priority'],data['statuses'][r['status']],r['title'],r['kind'],' / '.join(r['scenes']),' / '.join(r['branches']),' / '.join(r['contract']['states']),r['contract']['transparent'],r['contract']['size_rule'],' / '.join(r['references']),' / '.join(r['sources']),' / '.join(r['required']),' / '.join(r['avoid']),' / '.join(r['acceptance'])])
 html=(OUT/'portal.template.html').read_text().replace('__ART_REQUESTS_DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
 return {'requests.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n','requests.csv':sio.getvalue(),'그림_제작_요청서.md':md,'index.html':html}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();files=build();stale=[]
 for name,content in files.items():
  p=OUT/name
  if args.check:
   if not p.exists() or p.read_text()!=content:stale.append(name)
  else:p.write_text(content)
 if stale:raise SystemExit('다시 생성 필요: '+', '.join(stale))
 print('그림 요청 포털 '+('검사 통과' if args.check else '생성 완료')+': '+str(len(files))+'개 파일')
if __name__=='__main__':main()
