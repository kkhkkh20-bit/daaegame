"""Q1 v2 playthroughs. Fixtures place the father; conversations and proofs use real controls."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_q1_review import Q1QA,native_jump,URL
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/q1-arguments-browser'));OUT.mkdir(parents=True,exist_ok=True)
COUNTERS=['꺼내는 행동을 본 겁니다.','얼굴과 그 자리를 봤습니다.','수레를 도운 전후가 같습니다.','받았다는 설명이 어긋납니다.']
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720});q=Q1QA(page,OUT);seen=[];checks=[];route='boot';shots=set()
  async def py(code):return await q.py('import renpy;s=renpy.store;'+code)
  async def until(screen=None,label=None):
   for i in range(300):
    st=await q.state();say=st.get('say')
    if say and (not seen or seen[-1]['text']!=say):
     seen.append(dict(route=route,text=say))
     (OUT/'dialogue.json').write_text(json.dumps(seen,ensure_ascii=False,indent=2))
    for snippet,name in [('조각이 들려','removal-observation'),('거래 27번','trade-record'),('수리점에서 받은 게','admission'),('무단 반출','finding')]:
     tag=route+'-'+name
     if say and snippet in say and tag not in shots:await q.shot(tag);shots.add(tag)
    if (screen and screen in st['screens']) or (label and any(label in b['text'] for b in st['buttons'])):
     await asyncio.sleep(.3);return st
    if 'choice' in st['screens']:
     match=next((x for x in COUNTERS if any(x in b['text'] for b in st['buttons'])),None)
     if match:
      tag=route+'-counter-'+str(len(shots));await q.shot(tag);shots.add(tag);await q.press(match);continue
    if await py('result=s.r13_aftermath_active'):
     if any(b.get('value') in ('next',repr('next')) for b in st['buttons']):await q.value('next')
     else:await asyncio.sleep(.1)
    elif 'say' in st['screens']:await q.input(810,610)
    else:await asyncio.sleep(.1)
   raise AssertionError((route,'timeout',screen,label,st['screens'],say,[b['text'][:75] for b in st['buttons']]))
  async def fixture(evidence):
   flags=['entry_corrected','lodging','lt_dawn','lt_open','piko_dead','librarian_dead','lt_lib_dawn','lt_siluk_seen','ep4_seen','ep1_done','ep1_patrol_seen','ep1_eaves_seen']
   await py('s.r13_edit(day=4,period=0,location="square",q1_rules=2,evidence='+repr(evidence)+',flags='+repr(flags)+',propositions=[],arguments={},debate={},meeting_heard=[],meeting_votes={},records={},q1_checkpoints={},run_token='+repr('q1-v2-'+route)+',livelihood=dict(cash=7,debt=0,items=[]));s.r13_meeting_active=False;s.r13_meeting_live_active=False;result=True')
   await native_jump(q,'r13_roam');await until('r13_hub')
  async def talk(who,topics):
   await py('s.r13_target='+repr(who)+';result=True');await native_jump(q,'r13_talk_menu');await until('r13_topics')
   for key in topics:
    title=await py('result=s.ROOM13["topics"][%r]["title"]'%key)
    await q.press(title);await until('r13_topics');print('ACQUIRED',route,key,flush=True)
   await q.shot(route+'-topics-'+who)
  async def item(key,hearing=True):
   await until('r13_book');title=await py('result=s.R13_RECORD_SHORT['+repr(key)+']')
   for _ in range(20):
    st=await q.state()
    if any(title in b['text'] for b in st['buttons']):break
    direction=await py('sc=renpy.display.screen.get_screen("r13_book");entries=sc.scope["entries"];result="다음" if entries.index('+repr(key)+')//s.r13_record_page_size()>sc.scope["page"] else "이전"')
    await q.press(direction)
   await q.press(title);await q.press('이 주장에 근거로 낸다' if hearing else '에게 보여주기')
  async def enter():
   await py('s.r13_edit(location="square");result=True');await native_jump(q,'r13_roam');await until('r13_hub')
   await q.value(('offer','r13_ep1_meeting'));await until(label='회의에 들어간다');await q.press('회의에 들어간다')
   for _ in range(100):
    if await py('result=s.r13_meeting_live_active'):break
    await q.input(810,610)
   await q.press('발언 선택');await until('r13_debate_board')
  async def select(sid):
   for _ in range(20):
    if await py('result=s.r13_debate_selected=='+repr(sid)):return
    await q.press('›')
   raise AssertionError(('not visible',sid))
  async def proof(sid,key):
   await select(sid);await q.press('보여주기');await item(key);await until('r13_debate_board');print('PROOF',route,sid,key,flush=True)
  async def press(sid):
   await select(sid);await q.press('되묻기');await until('r13_debate_board')
  async def finish(success=True,conclusion="실룩이 허락 없이"):
   await q.shot(route+'-before-conclusion');await q.press('결론 정리');await until(label=conclusion);await q.press(conclusion);await until('r13_confirm');await q.press('이 결론으로 마친다')
   if success:
    await until(label='회의를 계속한다');await q.press('회의를 계속한다');await until(label='둘 다 요구한다');await q.press('둘 다 요구한다')
   await until(label='이 결과로 계속한다');await q.shot(route+'-result')
   if success:
    assert await py('result=s.r13_has("tok_cleared") and s.r13_has("lt_solved") and s.r13_has("madam_store_opened") and not s.r13_has("tok_detained")')
    assert await py('result=all(done for _,done,_ in s.r13_q1_review_rows())')
   else:assert await py('result=s.r13_has("tok_detained") and not s.r13_has("tok_cleared")')
   state=await py('result=dict(flags=s.room13["flags"],evidence=s.room13["evidence"],debate=s.room13["debate"],cash=s.r13_wallet(s.room13)["cash"])')
   (OUT/(route+'-state.json')).write_text(json.dumps(state,ensure_ascii=False,indent=2))
   checks.append(dict(route=route,success=success));print('PASS',route,flush=True)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000);await q.wait('main_menu');print('BOOT',flush=True)
   assert await py('result=s.config.version=="0.19.58"')
   await py('s.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance()
   route='physical';await fixture(['L04','L07','L06'])
   await talk('resident_lamplighter',['q1v:patrol','q1v:removal']);await enter()
   for sid,key in [('v_trace','L04'),('v_trace','L07'),('v_recent','L15')]:await proof(sid,key)
   await press('v_user');await proof('v_action','L16');await press('v_permission')
   assert not await py('result=s.r13_has("L09") or s.r13_has("L18") or s.r13_has("L19")')
   await finish()
   route='trade';await fixture([]);await talk('resident_siluk',['q1v:receipt'])
   await py('s.r13_edit(location="store");result=True');await native_jump(q,'r13_roam');await until('r13_hub')
   assert await py('result=s.r13_has("L09")')
   await talk('resident_madam',[]);await q.press('자료 보여주기');await item('L09',False);await until('r13_topics')
   assert await py('result=s.r13_has("L18")')
   await enter()
   for sid,key in [('v_origin','L09'),('v_trade','L19'),('v_trade','L18'),('v_own','L19')]:await proof(sid,key)
   assert not await py('result=s.r13_debate_ready("Q1")')
   await press('v_where');await proof('v_slip','L20');await press('v_permission')
   assert not await py('result=bool(set(s.room13["evidence"]) & {"L04","L07","L15","L16","L17"})')
   await finish()
   route='testimony';await fixture(['L06']);await talk('resident_lamplighter',['q1v:patrol','q1v:removal']);await talk('buri',['q1v:buri']);await enter()
   for sid,key in [('v_identity','L17'),('v_action','L16'),('v_link','L17'),('v_link','L16')]:await proof(sid,key)
   await press('v_permission');await finish()
   route='incomplete';await fixture(['L16']);await enter();await proof('v_action','L16');await finish(False)
   await q.press('같은 자료로 회의를 다시 한다');await until(label='회의에 들어간다')
   assert await py('result=not s.r13_has("lt_done") and not s.r13_q1_done("v_action") and s.room13["evidence"]==["L16"]')
   await q.shot('incomplete-native-restore');checks.append(dict(route='native-restore',success=True))
   # Targeted final-verdict fixture: the argument is complete, but murder intent is unsupported.
   route='overreach';await fixture(['L16','L17']);await enter()
   await py('s.r13_debate_mark("broken","Q1","v_action");s.r13_debate_mark("broken","Q1","v_identity");s.r13_debate_mark("broken","Q1","v_link");s.r13_q1_press_done("v_permission");result=True')
   assert await py('result=s.r13_debate_ready("Q1")')
   await finish(False,'실룩은 사람을 죽이려')
   over=[row['text'] for row in seen if row['route']=='overreach']
   assert any('그 결론을 뒷받침할 근거' in t for t in over)
   assert not any('결론을 듣지 못했소' in t for t in over)
   (OUT/'result.json').write_text(json.dumps(dict(passed=True,checks=checks,dialogue_pages=len(seen)),ensure_ascii=False,indent=2))
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except Exception:pass
   raise
  finally:await browser.close()
if __name__=='__main__':asyncio.run(main())
