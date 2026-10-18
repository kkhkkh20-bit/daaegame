"""First-case browser regression with explicit investigation/meeting fixtures, real UI and native save loads."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_q1_checkpoint_wait','r13_mystery_notebook','r13_episode_aftermath_view','r13_debate_board','r13_meeting_ballot','r13_meeting_agenda',")
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/q1-browser'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8770/preview/room13-dev/')

async def native_jump(q,label):
 code='\n'.join(['import renpy','def _qa_meeting_jump(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 계속",clicked=s.Jump('+repr(label)+'),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_meeting_jump',_qa_meeting_jump,modal='True',zorder='200')","renpy.exports.show_screen('qa_meeting_jump')","renpy.exports.restart_interaction()","result=True"])
 await q.py(code);await q.press('검토 계속');await q.py('import renpy;renpy.exports.hide_screen("qa_meeting_jump");renpy.exports.restart_interaction();result=True')

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720});q=UIQA(page,OUT)
  seen=[];checks=[]
  async def until(screen=None,label=None):
   for i in range(240):
    st=await q.state()
    if st.get('say') and (not seen or seen[-1]!=st['say']):seen.append(st['say'])
    if screen and screen in st['screens'] or label and any(label in b['text'] for b in st['buttons']):
     await asyncio.sleep(.5)
     return await q.state()
    if await q.py('import renpy;result=renpy.store.r13_aftermath_active'):
     if any(b.get('value') in ('next',repr('next')) for b in st['buttons']):await q.value('next')
     else:await asyncio.sleep(.15)
    elif 'say' in st['screens']:await q.input(810,610)
    else:await asyncio.sleep(.15)
   raise AssertionError(('timeout',screen,label,st['screens'],st['say'],[b['text'][:80] for b in st['buttons']]))
  async def py(code):return await q.py('import renpy;s=renpy.store;'+code)
  async def enter():
   await until(label='회의에 들어간다');await q.press('회의에 들어간다')
   for i in range(100):
    if await py('result=s.r13_meeting_live_active'):break
    await q.input(810,610)
   await q.press('발언 선택');await until('r13_debate_board')
  async def select(sid):
   for i in range(8):
    if await py('result=s.r13_debate_selected=='+repr(sid)):return
    await q.press('›')
   raise AssertionError(sid)
  async def record(key):
   await q.press('보여주기');await until('r13_book')
   title=await py('result=s.R13_RECORD_SHORT['+repr(key)+']')
   for i in range(20):
    st=await q.state()
    if any(title in b['text'] for b in st['buttons']):break
    direction=await py('sc=renpy.display.screen.get_screen("r13_book");entries=sc.scope["entries"];result="다음" if entries.index('+repr(key)+')//s.r13_record_page_size()>sc.scope["page"] else "이전"')
    await q.press(direction)
   await q.press(title);await q.press('이 주장에 근거로 낸다');await until('r13_debate_board')
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000);await q.wait('main_menu');print('BOOT',flush=True)
   await py('s.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance()
   # Inject only the starting fixture, then execute the authored dawn and meeting.
   await py('s.r13_edit(day=4,period=0,location="square",evidence=["L03","L04","L06"],flags=["entry_corrected","lodging","lt_dawn","lt_open","piko_dead","ep4_seen","ep1_done","ep1_patrol_seen","ep1_eaves_seen"],propositions=[],debate={},run_token="browser-q1-review",livelihood=dict(cash=7,debt=0,items=[]));result=True')
   await native_jump(q,'r13_roam');await until('r13_hub')
   await py('result=s.r13_q1_can_restore("investigation")')
   assert await py('result=s.r13_q1_can_restore("investigation")')
   await q.press('기록');await until('r13_records');await q.press('메모');await q.shot('01-investigation-questions')
   await q.press('막혔다면 생각 정리');await q.shot('01b-notebook-expanded')
   await py('s.r13_set_text_size("large");result=True')
   await page.set_viewport_size({'width':844,'height':390});await q.shot('01c-notebook-mobile-large')
   await q.input(670,500);await page.mouse.wheel(0,600);await asyncio.sleep(.4);await q.shot('01d-notebook-mobile-scroll')
   await q.press('닫기');await until('r13_hub')
   await page.set_viewport_size({'width':1280,'height':720});await py('s.r13_set_text_size("normal");result=True')
   await q.py('import renpy;renpy.exports.show_screen("r13_mystery_notebook");renpy.exports.restart_interaction();result=True');await q.shot('01e-legacy-notebook-shared');await q.press('닫기');await until('r13_hub')
   checks.append('Records > Memo real entry, optional thinking, large text scroll and close; legacy entry shares the same parchment')
   if os.environ.get('ROOM13_NOTEBOOK_ONLY'):
    (OUT/'notebook-result.json').write_text(json.dumps(dict(passed=True,checks=checks),ensure_ascii=False,indent=2));return
   await q.value(('offer','r13_ep1_meeting'));await until(label='회의에 들어간다');await q.shot('02-enter-with-incomplete-evidence')
   await q.press('조사를 더 한다');await until('r13_hub')
   assert not await py('result=s.r13_has("lt_done")');checks.append('incomplete entry can cancel without time, proof or outcome')
   await q.value(('offer','r13_ep1_meeting'));await enter()
   for sid,key in [('s1','L03'),('s2','L06'),('s4','L10')]:await select(sid);await record(key)
   assert await py('result=s.r13_debate_progress("Q1")== (3,5)')
   await select('s5');await record('L04');await q.shot('03-rope-needs-connection')
   assert any('뜯긴 자리' in t for t in seen)
   await q.press('회의 중단');await until('r13_confirm');await q.shot('04-partial-exit');await q.press('여기까지 정리한다')
   await until(label='이 결과로 계속한다');await q.shot('05-failure-review')
   assert await py('result=s.r13_has("tok_detained") and not s.r13_has("tok_cleared")')
   assert not any('다시 넣었다' in t for t in seen)
   failure=await py('result=s.r13_q1_checkpoint_slot("result")');assert failure
   checks.append('3/5 rebuttals retained; detained Tok never repairs lamp; result saved')
   await q.press('남은 논점을 생각한다');await until(label='노끈의 주인');await q.press('노끈의 주인');await until(label='구체적인 조사 방향');await q.shot('06-optional-hint');await q.press('구체적인 조사 방향');await until(label='이 결과로 계속한다')
   await page.set_viewport_size({'width':844,'height':390});await q.shot('07-mobile-review');await page.set_viewport_size({'width':1280,'height':720})
   await q.press('같은 자료로 회의를 다시 한다');await until(label='회의에 들어간다');await q.shot('08-meeting-restored')
   assert await py('result=not s.r13_has("lt_done") and s.r13_debate_progress("Q1")== (0,5) and s.r13_wallet(s.room13)["cash"]==7')
   assert await py('result=s.r13_q1_previous_result()=='+repr(failure))
   checks.append('native meeting restore resets outcome and debate, preserves 7 coins');print('RESTORE meeting PASS',flush=True)
   await q.press('보관한 이전 결과를 본다');await until(label='이 결과로 계속한다')
   assert await py('result=s.r13_has("tok_detained") and s.r13_debate_progress("Q1")== (3,5)')
   await q.press('조사를 다시 살펴본다');await until('r13_hub');await q.shot('09-investigation-restored')
   assert await py('result=s.room13["day"]==4 and s.room13["period"]==0 and not s.r13_has("lt_done") and s.r13_wallet(s.room13)["cash"]==7')
   checks.append('native investigation restore returns after dawn without replaying death scene; prior failure remains loadable');print('RESTORE result/investigation PASS',flush=True)
   # Complete the investigation using actual episode labels and their options.
   await py('s.r13_edit(location="gate");result=True');await native_jump(q,'r13_roam');await until(label='노끈을 본다');await q.press('노끈을 본다');await until(label='그만 간다');await q.press('그만 간다');await until('r13_hub')
   await py('s.r13_edit(location="store");result=True');await native_jump(q,'r13_roam');await until('r13_hub')
   await py('s.r13_edit(location="square");result=True');await native_jump(q,'r13_roam');await until('r13_hub');await q.value(('offer','r13_ep1_meeting'));await enter()
   for sid,key in [('s1','L03'),('s2','L06'),('s3','L09'),('s4','L10'),('s5','L07')]:await select(sid);await record(key)
   await q.press('결론 정리');await until('choice');await q.press('실룩');await until('r13_book')
   # Decisive evidence selection (book already open).
   await q.press('실룩의 짐 끈');await q.press('이 주장에 근거로 낸다');await until(label='회의를 계속한다');await q.press('회의를 계속한다');await until(label='둘 다 요구한다');await q.press('둘 다 요구한다')
   await until(label='이 결과로 계속한다');await q.shot('10-success-review')
   assert await py('result=s.r13_has("tok_cleared") and s.r13_has("madam_store_opened") and s.r13_wallet(s.room13)["cash"]==15')
   checks.append('completed investigation wins; lamp returned only after warehouse decision; reward exactly once')
   await q.press('이 결과로 계속한다');await until('r13_hub');await q.shot('11-continue-success')
   (OUT/'result.json').write_text(json.dumps(dict(passed=True,checks=checks,dialogue=seen),ensure_ascii=False,indent=2));print('PASS',checks,flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'))
   (OUT/'failure.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   raise
  finally:await browser.close()
if __name__=='__main__':asyncio.run(main())
