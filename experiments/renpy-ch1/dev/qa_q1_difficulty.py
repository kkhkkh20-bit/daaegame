"""Q1 rules-3 playthroughs and three-error native restart. Fixtures place the father; conversations and proofs use real controls."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_q1_review import Q1QA,native_jump,URL
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/q1-hard-browser'));OUT.mkdir(parents=True,exist_ok=True)
THESES={'physical':'남은 끈의 주인부터 따지겠습니다.','trade':'팔린 조각의 행방부터 따지겠습니다.','testimony':'두 사람이 본 작업부터 맞춰보겠습니다.'}
COUNTERS=['뜯긴 끝의 모양이 맞습니다.','첫 순찰의 내부 확인 뒤입니다.','내부 확인과 잔열은 다릅니다.',
'조각은 봤지만 얼굴은 못 봤습니다.','도움받고 작업한 사람이 실룩입니다.','부리가 수레를 도운 직후입니다.',
'내려올 때까지 작업자가 같았습니다.','3번 등의 조각이 창고에 있습니다.','날짜·번호·품목·대금이 같습니다.',
'자기 소유 조각을 판다는 조건입니다.','판매는 확인됐고 취득 경위는 남습니다.',
'수리점에서 받았나, 등에서 꺼냈나입니다.','덮개 수리와 조각 처분은 별개입니다.','반출은 입증했습니다. 허락도 확인하죠.']
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720});q=Q1QA(page,OUT);seen=[];checks=[];route='boot';shots=set();answer_override=None;cancel_commit=False
  async def py(code):return await q.py('import renpy;s=renpy.store;'+code)
  async def until(screen=None,label=None):
   nonlocal cancel_commit
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
    if 'r13_confirm' in st['screens'] and any('이 논증으로 반박한다' in b['text'] for b in st['buttons']):
     await q.shot(route+'-commit-'+str(len(shots)));shots.add(route+'-commit-'+str(len(shots)))
     await q.press('자료를 더 검토한다' if cancel_commit else '이 논증으로 반박한다');cancel_commit=False;continue
    if 'choice' in st['screens']:
     match=next((x for x in ([answer_override] if answer_override else COUNTERS) if any(x in b['text'] for b in st['buttons'])),None)
     if match:
      tag=route+'-counter-'+str(len(shots));await q.shot(tag);shots.add(tag)
      if route=='physical' and 'mobile-large' not in shots:
       await page.set_viewport_size({'width':844,'height':390});await py('s.r13_set_text_size("large");result=True');await q.shot('physical-mobile-large-counter');shots.add('mobile-large')
       await page.set_viewport_size({'width':1280,'height':720});await py('s.r13_set_text_size("normal");result=True')
      await q.press(match);continue
    if await py('result=s.r13_aftermath_active'):
     if any(b.get('value') in ('next',repr('next')) for b in st['buttons']):await q.value('next')
     else:await asyncio.sleep(.1)
    elif 'say' in st['screens']:await q.input(810,610)
    else:await asyncio.sleep(.1)
   raise AssertionError((route,'timeout',screen,label,st['screens'],say,[b['text'][:75] for b in st['buttons']]))
  async def fixture(evidence):
   flags=['entry_corrected','lodging','lt_dawn','lt_open','piko_dead','librarian_dead','lt_lib_dawn','lt_siluk_seen','ep4_seen','ep1_done','ep1_patrol_seen','ep1_eaves_seen']
   await py('renpy.exports.hide_screen("r13_debate_board");s.r13_edit(day=4,period=0,location="square",q1_rules=3,q1_thesis=None,q1_formal_errors=[],q1_argument_pending={},q1_argument_proofs={},evidence='+repr(evidence)+',flags='+repr(flags)+',propositions=[],arguments={},debate={},meeting_heard=[],meeting_votes={},records={},q1_checkpoints={},run_token='+repr('q1-hard-'+route)+',livelihood=dict(cash=7,debt=0,items=[]));s.r13_meeting_active=False;s.r13_meeting_live_active=False;result=True')
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
  async def thesis(key):
   await until(label=THESES[key])
   if route=='physical':
    await q.press('자료를 다시 살펴보겠습니다.');await until('r13_records');await q.shot('physical-before-commit-records');await q.press('닫기');await until(label=THESES[key])
    assert await py('result=not s.r13_q1_thesis() and s.r13_q1_formal_errors()==0')
   await q.shot(route+'-thesis-options');await q.press(THESES[key])
   await until('r13_confirm');await q.shot(route+'-thesis-commit');await q.press('이 논증으로 끝까지 간다')
   for _ in range(100):
    if await py('result=s.r13_meeting_live_active'):break
    await q.input(810,610)
   assert await py('result=s.r13_q1_thesis()=='+repr(key))
  async def enter():
   await py('s.r13_edit(location="square");result=True');await native_jump(q,'r13_roam');await until('r13_hub')
   await q.value(('offer','r13_ep1_meeting'));await until(label='회의에 들어간다');await q.press('회의에 들어간다')
   await thesis(route if route in THESES else 'testimony')
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
  async def authority():
   await press('h_work');await q.shot(route+'-work-order')
   await proof('h_scope','L21');await proof('h_scope','L22');await press('v_permission')
  async def finish(success=True,conclusion="실룩이 허락 없이"):
   await q.shot(route+'-before-conclusion');await q.press('결론 정리');await until(label=conclusion);await q.press(conclusion);await until('r13_confirm');await q.press('이 결론으로 마친다')
   if success:
    await until(label='회의를 계속한다');await q.press('회의를 계속한다');await until(label='둘 다 요구한다');await q.press('둘 다 요구한다')
   await until(label='이 결과로 계속한다');await q.shot(route+'-result')
   if success:
    assert await py('result=s.r13_has("tok_cleared") and s.r13_has("lt_solved") and s.r13_has("madam_store_opened") and not s.r13_has("tok_detained")')
    assert await py('result=all(done for _,done,_ in s.r13_q1_review_rows())')
   else:assert await py('result=s.r13_has("tok_detained") and not s.r13_has("tok_cleared")')
   state=await py('result=dict(flags=s.room13["flags"],evidence=s.room13["evidence"],debate=s.room13["debate"],cash=s.r13_wallet(s.room13)["cash"],thesis=s.r13_q1_thesis(),proofs=s.room13.get("q1_argument_proofs",{}),errors=s.r13_q1_formal_errors())')
   (OUT/(route+'-state.json')).write_text(json.dumps(state,ensure_ascii=False,indent=2))
   checks.append(dict(route=route,success=success));print('PASS',route,flush=True)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000);await q.wait('main_menu');print('BOOT',flush=True)
   assert await py('result=s.config.version=="0.19.60"')
   await py('s.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기')
   # The real new-game initialization has run; route fixtures safely jump past the unrelated entry conversation.
   focus=os.environ.get('ROOM13_QA_FOCUS','all')
   if focus in ('all','physical'):
    route='physical';await fixture(['L04','L07','L06'])
    await talk('resident_lamplighter',['q1v:patrol','q1v:removal']);await enter()
    for sid,key in [('v_trace','L04'),('v_trace','L07'),('v_recent','L15')]:await proof(sid,key)
    await press('v_user');await proof('v_action','L16');await authority()
    assert not await py('result=s.r13_has("L09") or s.r13_has("L18") or s.r13_has("L19")')
    await finish()
   if focus in ('all','trade'):
    route='trade';await fixture([]);await talk('resident_siluk',['q1v:receipt'])
    await py('s.r13_edit(location="store");result=True');await native_jump(q,'r13_roam');await until('r13_hub')
    assert await py('result=s.r13_has("L09")')
    await talk('resident_madam',[]);await q.press('자료 보여주기');await item('L09',False);await until('r13_topics')
    assert await py('result=s.r13_has("L18")')
    await enter()
    for sid,key in [('v_origin','L09'),('v_trade','L19'),('v_trade','L18'),('v_own','L19')]:await proof(sid,key)
    assert not await py('result=s.r13_debate_ready("Q1")')
    await press('v_where');await proof('v_slip','L20');await authority()
    assert not await py('result=bool(set(s.room13["evidence"]) & {"L04","L07","L15","L16","L17"})')
    await finish()
   if focus in ('all','testimony'):
    route='testimony';await fixture(['L06']);await talk('resident_lamplighter',['q1v:patrol','q1v:removal']);await talk('buri',['q1v:buri']);await enter()
    for sid,key in [('v_identity','L17'),('v_action','L16'),('v_link','L17'),('v_link','L16')]:await proof(sid,key)
    await authority();await finish()
   if focus not in ('all','errors'):
    (OUT/'result.json').write_text(json.dumps(dict(passed=True,checks=checks,dialogue_pages=len(seen)),ensure_ascii=False,indent=2))
    return
   route='premature-conclusion';await fixture(['L16','L17','L06']);await enter()
   await q.press('결론 정리');await until(label='실룩이 허락 없이');await q.press('실룩이 허락 없이');await until('r13_confirm');await q.press('이 결론으로 마친다');await until('r13_debate_board')
   assert await py('result=s.r13_q1_formal_errors()==1 and not s.r13_debate_closed("Q1") and not s.r13_q1_removal_proved()')
   await q.shot('premature-conclusion-one-error');checks.append(dict(route='premature-conclusion',success=True))
   route='three-errors';await fixture(['L16','L17','L06']);await enter()
   answer_override='아직 주장하지 않고 자료를 다시 본다'
   await proof('v_identity','L17')
   assert await py('result=s.r13_q1_formal_errors()==0 and not s.r13_q1_done("v_identity")')
   answer_override=None;cancel_commit=True;await proof('v_identity','L17')
   assert await py('result=s.r13_q1_formal_errors()==0 and not s.r13_q1_done("v_identity")')
   # Wrong evidence consumes the same budget as a formally committed interpretation.
   await proof('v_identity','L06')
   assert await py('result=s.r13_q1_formal_errors()==1')
   answer_override='실룩이 조각을 들고 내려왔습니다.'
   await proof('v_identity','L17')
   assert await py('result=s.r13_q1_formal_errors()==2 and not s.r13_q1_done("v_identity")')
   await select('v_identity');await q.press('보여주기');await item('L17');await until(label='이 결과로 계속한다')
   assert await py('result=s.r13_q1_formal_errors()==3 and s.r13_debate_closed("Q1") and s.r13_has("tok_detained")')
   await q.shot('three-errors-result');checks.append(dict(route='three-errors',success=True))
   await q.press('같은 자료로 회의를 다시 한다');await until(label='회의에 들어간다')
   assert await py('result=s.r13_q1_formal_errors()==0 and not s.r13_q1_thesis() and not s.room13.get("q1_argument_proofs") and not s.room13.get("q1_argument_pending") and not s.r13_q1_done("v_identity") and not s.r13_has("lt_done") and s.room13["evidence"]==["L16","L17","L06"] and s.r13_wallet(s.room13)["cash"]==7')
   await q.shot('native-meeting-restart');checks.append(dict(route='native-restart',success=True))
   route='live-errors';await q.press('회의에 들어간다');await thesis('physical')
   assert await py('result=s.r13_q1_thesis()=="physical" and not s.r13_debate_visible("Q1",s.r13_debate_statement("Q1","v_identity"))')
   checks.append(dict(route='restart-can-choose-another-thesis',success=True))
   # This attempt committed to the rope argument. Witness material cannot replace its missing links.
   for _ in range(100):
    if await py('result=s.r13_meeting_live_active and s.r13_meeting_live_sid=="v_accused"'):break
    await q.input(810,610)
   for attempt in range(3):
    await q.press('자료 보여주기');await item('L17')
    if attempt==2:await until(label='이 결과로 계속한다')
    else:
     for _ in range(150):
      st=await q.state()
      if await py('result=s.r13_meeting_live_active and not s.r13_meeting_interrupting and s.r13_q1_formal_errors()=='+str(attempt+1)):break
      await q.input(810,610)
    assert await py('result=s.r13_q1_formal_errors()=='+str(attempt+1))
   assert await py('result=s.r13_q1_thesis()=="physical" and not s.r13_q1_removal_proved()')
   await q.shot('live-third-error-result');checks.append(dict(route='live-third-error',success=True))
   (OUT/'result.json').write_text(json.dumps(dict(passed=True,checks=checks,dialogue_pages=len(seen)),ensure_ascii=False,indent=2))
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except Exception:pass
   raise
  finally:await browser.close()
if __name__=='__main__':asyncio.run(main())
