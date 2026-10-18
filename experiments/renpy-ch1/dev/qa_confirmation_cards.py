"""Approved shared confirmation card: real choices plus long/mobile specimens."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_q1_review import Q1QA,native_jump,URL
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/confirm61-browser'));OUT.mkdir(parents=True,exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720});q=Q1QA(page,OUT);checks=[]
  async def py(code):return await q.py('import renpy;s=renpy.store;'+code)
  async def until(screen=None,label=None):
   for _ in range(220):
    st=await q.state()
    if (screen and screen in st['screens']) or (label and any(label in x['text'] for x in st['buttons'])):return st
    if 'say' in st['screens']:await q.input(810,610)
    else:await asyncio.sleep(.1)
   raise AssertionError((screen,label,st))
  async def shot(name):
   st=await q.state();buttons=[x for x in st['buttons'] if x['rect'][3]>15]
   assert len(buttons)==2,buttons
   for x in buttons:
    a,c,w,h=x['rect'];assert a>=0 and c>=0 and a+w<=1280 and c+h<=720,(name,x)
    assert h>=64,(name,x)
   l,r=sorted(buttons,key=lambda x:x['rect'][0]);assert l['rect'][0]+l['rect'][2]<=r['rect'][0],buttons
   await q.shot(name);checks.append(name)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000);await q.wait('main_menu')
   assert await py('result=s.config.version=="0.19.61"')
   await py('s.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기')
   await py('s.r13_edit(day=4,period=0,location="square",q1_rules=3,q1_thesis=None,q1_formal_errors=[],evidence=["L16","L17","L06"],flags=["entry_corrected","lodging","lt_dawn","lt_open","piko_dead","librarian_dead","lt_lib_dawn","lt_siluk_seen","ep4_seen","ep1_done","ep1_patrol_seen","ep1_eaves_seen"]);result=True')
   await native_jump(q,'r13_roam');await until('r13_hub');await q.value(('offer','r13_ep1_meeting'));await until(label='회의에 들어간다');await q.press('회의에 들어간다')
   await until(label='남은 끈의 주인부터');await q.press('남은 끈의 주인부터');await until('r13_confirm');await shot('01-thesis-confirm')
   await q.press('다시 생각한다');await until(label='두 사람이 본 작업부터');assert await py('result=not s.r13_q1_thesis() and s.r13_q1_formal_errors()==0')
   await q.press('두 사람이 본 작업부터');await until('r13_confirm');await q.press('이 논증으로 끝까지 간다')
   for _ in range(100):
    if await py('result=s.r13_meeting_live_active'):break
    await q.input(810,610)
   assert await py('result=s.r13_q1_thesis()=="testimony"');checks.append('real-thesis-cancel-and-confirm')
   await q.press('발언 선택');await until('r13_debate_board');await q.press('결론 정리');await until(label='실룩이 허락 없이');await q.press('실룩이 허락 없이');await until('r13_confirm');await shot('02-conclusion-confirm');await q.press('회의에서 더 생각한다');await until('r13_debate_board')
   assert await py('result=s.r13_q1_formal_errors()==0 and not s.r13_has("lt_done")');checks.append('real-conclusion-cancel-preserves-state')
   msg='덮개 수리와 조각 처분은 별개입니다.\n반출은 입증했습니다. 허락도 확인하죠.\n\n이 반박을 확정합니다. 무너진 정식 반박이 세 번이면 회의가 끝납니다. 현재 0회.'
   for name,large,vp,period,message,yes,no in [
    ('03-rebuttal-desktop',False,(1280,720),0,msg,'이 논증으로 반박한다','자료를 더 검토한다'),
    ('04-rebuttal-mobile-large',True,(844,390),0,msg,'이 논증으로 반박한다','자료를 더 검토한다'),
    ('05-thesis-mobile-large',True,(844,390),0,'얼굴을 본 증언과 조각을 본 증언을 같은 작업으로 연결해, 누가 가져갔는지 밝히겠습니다.\n\n이번 회의에서는 이 논증을 끝까지 이어갑니다. 다른 논증은 회의를 처음부터 다시 할 때 선택할 수 있습니다.','이 논증으로 끝까지 간다','다시 생각한다'),
    ('06-sleep-night',False,(1280,720),2,'오늘 할 일을 마치고 잠자리에 듭니다.','자기','아직 할 일이 있다')]:
    await page.set_viewport_size({'width':vp[0],'height':vp[1]})
    await py('s.r13_set_text_size('+repr('large' if large else 'normal')+');s.r13_edit(period='+str(period)+');renpy.exports.show_screen("r13_confirm",message='+repr(message)+',yes='+repr(yes)+',no='+repr(no)+');renpy.exports.restart_interaction();result=True')
    await asyncio.sleep(.6);await shot(name);await py('renpy.exports.hide_screen("r13_confirm");renpy.exports.restart_interaction();result=True')
   (OUT/'result.json').write_text(json.dumps(dict(passed=True,checks=checks),ensure_ascii=False,indent=2))
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:await b.close()
if __name__=='__main__':asyncio.run(main())
