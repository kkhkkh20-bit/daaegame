"""U01/U02/U03/U07/U11 실제 입력 회귀. 첫 현장 이후 자료·진입은 명시적 검수 fixture."""
import asyncio, json, os, re
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa/play-review-proof'))
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/')
OUT.mkdir(parents=True,exist_ok=True)
CLAIM='v111:함께 들어갈 근거를 고른다'

class ProofQA(UIQA):
 async def py(self,code):
  wrapped='ns={};exec('+ascii(code)+",ns);result=ns.get('result')"
  return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(wrapped)+')'),90)
 async def texts(self,name):
  return await self.py('import renpy\nsc=renpy.display.screen.get_screen('+repr(name)+')\nseen=set();texts=[]\ndef walk(w):\n if id(w) in seen:return\n seen.add(id(w))\n if isinstance(w,renpy.text.text.Text):texts.append("".join(str(x) for x in w.text))\n for c in w.visit():walk(c)\nwalk(sc)\nresult=texts')
 async def jump(self,label):
  await self.py('import renpy\ndef qa_review_jump(**kw):\n renpy.ui.textbutton("검토 계속",clicked=renpy.store.Jump('+repr(label)+'),xpos=500,ypos=300,xsize=280,ysize=88)\nrenpy.exports.define_screen("qa_review_jump",qa_review_jump,modal="True",zorder="200")\nrenpy.exports.show_screen("qa_review_jump");renpy.exports.restart_interaction();result=True')
  await self.press('검토 계속')
  await self.py('import renpy;renpy.exports.hide_screen("qa_review_jump");renpy.exports.restart_interaction();result=True')
 async def until(self,screen=None,predicate=None):
  for _ in range(350):
   st=await self.state()
   if (screen and screen in st['screens']) or (predicate and predicate(st)):
    await asyncio.sleep(.4);return await self.state()
   if 'choice' in st['screens']:
    if not st['buttons']:
     await asyncio.sleep(.4);continue
    matches=[b for b in st['buttons'] if '편지를 접는다' in b['text']]
    if matches:await self.press('편지를 접는다');continue
    raise AssertionError(('unexpected choice',st))
   if 'r13_cinematic_view' in st['screens']:await self.press('계속')
   elif 'r13_arrival_card' in st['screens']:await self.input(800,400)
   elif 'say' in st['screens']:await self.input(810,610)
   else:await asyncio.sleep(.15)
  raise AssertionError(('timeout',screen,st))
 async def pick(self,key):
  title=await self.py('import renpy;result=renpy.store.r13_catalog_title('+repr(key)+')')
  wanted=re.sub(r'\s+','',title)
  for _ in range(20):
   st=await self.state()
   matches=[b for b in st['buttons'] if wanted in re.sub(r'\s+','',b['text']) and b['rect'][0]<330]
   if matches:
    b=matches[0];x,y,w,h=b['rect'];await self.input(x+w/2,y+h/2);return
   await self.press('›')
  raise AssertionError(('missing record',key,title))
 async def add(self,key):
  await self.pick(key);await self.press('에 추가');await self.wait('r13_book')
 async def chosen(self):
  return (await self.state())['room']['arguments'].get(CLAIM,[])
 async def tries(self):
  return (await self.state())['room']['v111']['values'].get('tries:gate',0)

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True)
  q=ProofQA(page,OUT);errors=[];checks=[];measure=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000)
   await q.wait('main_menu');print('진입 타이틀',flush=True);await q.press('처음부터');await q.until('r13_hub')
   first_text='\n'.join(await q.texts('r13_hub'))
   assert '놓인 물건·붙은 글' in first_text,first_text
   await q.shot('01-first-field')
   # The opening has now been played. Controlled inventory and proof entry follow.
   await q.py('import renpy;s=renpy.store;s.r13_v111_commit("MS14_D01_S03_L0002");s.r13_v111_commit("MS14_D01_S03_L0007");s.r13_grant(["V111:E01","V111:E02","V111:E03","V111:E04","V111:E06"],"qa:proof-review");s.r13_v111_talk_person=None;result=True')
   await q.jump('r13_v111_gate_proof');await q.wait('r13_crisis_proof')
   assert '잘못된 제출은 기회를 1회' in '\n'.join(await q.texts('r13_crisis_proof'))
   await q.press('자료 고르기');await q.wait('r13_book')
   assert any('선택 마치기 · 0개' in b['text'] for b in (await q.state())['buttons'])
   await q.press('선택 마치기');await q.wait('r13_crisis_proof');assert await q.chosen()==[] and await q.tries()==0
   await q.press('자료 고르기');await q.add('V111:E02');await q.press('선택 마치기');await q.wait('r13_crisis_proof')
   assert await q.chosen()==['V111:E02'] and await q.tries()==0
   await q.press('자료 고르기');await q.add('V111:E03');await q.input(1202,58);await q.wait('r13_crisis_proof')
   assert await q.chosen()==['V111:E02','V111:E03'] and await q.tries()==0
   checks.append('0/1/여러 자료 선택 완료 및 X 복귀: 선택 유지, 기회 소비 없음')
   await q.press('자료 고르기');await q.pick('V111:E03');await q.press('출처 펼치기')
   texts='\n'.join(await q.texts('r13_book'))
   place_name=await q.py('import renpy;result=renpy.store.R13_PLACES["gate"][0]')
   assert ('얻은 곳: '+place_name) in texts and 'MS14_D01_S03_L0002' not in texts,texts
   assert '건넬지' not in texts and '아직 제출되지 않습니다' in texts,texts
   await q.shot('02-proof-source')
   await q.press('근거에서 빼기');await q.wait('r13_book');await q.press('선택 마치기');await q.wait('r13_crisis_proof')
   assert await q.chosen()==['V111:E02'] and await q.tries()==0
   checks.append('자료 빼기 무료, 내부 출처 ID 비노출, 근거 문맥 안내')
   for width,height,large,name in ((1280,720,False,'pc'),(844,390,True,'mobile-large'),(740,360,True,'small-mobile-large')):
    await page.set_viewport_size({'width':width,'height':height});q.touch=width<1000
    await q.py('import renpy;renpy.store.persistent.room13_large_text='+str(large)+';renpy.exports.restart_interaction();result=True')
    await q.shot(name+'-proof')
    controls=[b for b in (await q.state())['buttons'] if b['text'].strip() in ('자료 고르기','되묻는다','선택한 근거 제출','자료 다시 보기','빼기')]
    scale=min(width/1280,height/720)
    assert all(b['rect'][1]+b['rect'][3]<=664 for b in controls),controls
    if q.touch:assert all(b['rect'][3]*scale>=44 for b in controls),controls
    measure.append({'mode':name,'controls':controls,'scale':scale})
    await q.press('자료 고르기');await q.wait('r13_book');await q.shot(name+'-book');await q.press('선택 마치기');await q.wait('r13_crisis_proof')
   await q.press('선택한 근거 제출');await q.until('r13_hub')
   assert await q.tries()==1 and await q.chosen()==['V111:E02']
   await q.shot('03-wrong-one-chance')
   checks.append('실제 불충분한 제출로 기회 1회 감소, 기존의 맞는 자료 유지 규칙 보존')
   await q.jump('r13_v111_gate_proof');await q.wait('r13_crisis_proof');await q.press('자료 고르기')
   await q.add('V111:E03');await q.add('V111:E04');await q.press('선택 마치기');await q.wait('r13_crisis_proof')
   await q.press('선택한 근거 제출')
   await q.until(predicate=lambda st:st['room'].get('v111',{}).get('values',{}).get('meeting:gate')=='win')
   assert await q.tries()==1
   checks.append('실제 세 자료 제출 성공: 정답·기회 규칙 보존')
   # Presentation context fixtures use the same production book, without invoking gift logic.
   for purpose,target,label in (('compare','dad','자료 비교'),(None,'guard','보여주기')):
    await q.py('import renpy;renpy.exports.show_screen("r13_book",target='+repr(target)+',present=True,purpose='+repr(purpose)+',chosen=());renpy.exports.restart_interaction();result=True')
    await q.wait('r13_book');await q.pick('V111:E01');texts='\n'.join(await q.texts('r13_book'))
    assert label in texts,texts
    assert ('건넬지' in texts)==(purpose is None),texts
    await q.shot('04-'+('compare' if purpose else 'present'))
    await q.py('import renpy;renpy.exports.hide_screen("r13_book");renpy.exports.restart_interaction();result=True')
   assert not errors,errors
   result={'passed':True,'version':(await q.info())['version'],'scope':'도입 첫 현장까지 실제 진행, 이후 자료 보유·제출 진입·제시 문맥은 명시적 검수 fixture; 제출과 선택은 실제 UI 입력','checks':checks,'measurements':measure,'page_errors':errors}
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False),flush=True)
  finally:await browser.close()

if __name__=='__main__':asyncio.run(main())
