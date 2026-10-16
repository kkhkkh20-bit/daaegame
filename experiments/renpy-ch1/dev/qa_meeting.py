"""Actual web meeting flow with explicit day-7/day-14 scene fixtures; not a full playthrough."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_more_tools','r13_meeting_agenda','r13_debate_board','r13_meeting_ballot',")
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa/meeting'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def native_jump(q,label):
 code='\n'.join(['import renpy','def _qa_meeting_jump(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 계속",clicked=s.Jump('+repr(label)+'),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_meeting_jump',_qa_meeting_jump,modal='True',zorder='200')","renpy.exports.show_screen('qa_meeting_jump')","renpy.exports.restart_interaction()","result=True"])
 await q.py(code);await q.press('검토 계속');await q.py('import renpy;renpy.exports.hide_screen("qa_meeting_jump");renpy.exports.restart_interaction();result=True')
async def native_load(q,slot):
 code='\n'.join(['import renpy','def _qa_meeting_load(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 불러오기",clicked=s.Function(renpy.exports.load,'+repr(slot)+'),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_meeting_load',_qa_meeting_load,modal='True',zorder='200')","renpy.exports.show_screen('qa_meeting_load')","renpy.exports.restart_interaction()","result=True"])
 await q.py(code);await q.press('검토 불러오기')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720});q=UIQA(page,OUT)
  async def shot(name):
   await asyncio.sleep(.35)  # Let the speaker pan settle before comparing framing.
   await q.shot(name)
  async def until(screen=None,say=None):
   for i in range(100):
    st=await q.state()
    if screen and screen in st['screens'] or say and 'say' in st['screens'] and say in st['say']:
     await asyncio.sleep(.4);return st
    if 'say' in st['screens']:await q.input(800,610)
    elif 'r13_cinematic_view' in st['screens']:await q.press('계속')
    elif any(s in st['screens'] for s in ('choice','r13_debate_board','r13_meeting_ballot','r13_meeting_agenda','r13_crisis')):
     raise AssertionError(('unexpected stop',screen,say,st['screens'],st['say'],[b['text'][:70] for b in st['buttons']]))
    else:await asyncio.sleep(.15)
   raise AssertionError(('timeout',screen,say))
  async def select_record(key):
   await q.wait('r13_book')
   title=await q.py('import renpy;s=renpy.store;result=s.R13_RECORD_SHORT.get('+repr(key)+',s.r13_catalog_title('+repr(key)+')[:8])')
   for i in range(20):
    st=await q.state()
    if any(title in b['text'] for b in st['buttons']):break
    await q.press('다음')
   await q.press(title);await q.press('이 주장에 근거로 낸다')
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await asyncio.sleep(.7)
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance()
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=7,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=list(s.ROOM13["evidence"]),propositions=[]);s.r13_flag("entry_corrected","lodging");s.r13_upgrade();result=True')
   await native_jump(q,'r13_trial');await q.wait('say');await shot('01-opening-focused')
   if os.environ.get('ROOM13_MEETING_OPINIONS_ONLY'):
    await q.py('import renpy;s=renpy.store;s.r13_meeting_active=True;s.r13_meeting_intro=False;s.r13_claim="C1";s.r13_meeting_claim="C1";s.r13_debate_selected="s2";s.r13_meeting_begin_opinions("C1");s.r13_edit(propositions=["C1"]);s.r13_debate_mark("pressed","C1","s1");s.r13_debate_mark("broken","C1","s2");result=True')
    await native_jump(q,'r13_debate_loop');await until('r13_debate_board');await q.press('결론을 말한다');await until('choice')
    correct=await q.py('import renpy;result=next(text for kind,text in renpy.store.R13_DEBATE["C1"]["conclusion"]["options"] if kind=="correct")')
    await q.press(correct);await until(say='동의하지 않아요');await shot('17-changed-resident-reaction')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_read_id.startswith("meeting:opinions:C1") and s.dialogue_speaker in [row["person"] for row in s.r13_meeting_vote["changed"]]')
    await until('r13_meeting_ballot');await shot('18-opinions-after-reactions')
    print('PASS changed residents speak before public opinion tally',flush=True);return
   if os.environ.get('ROOM13_MEETING_FRAME_ONLY'):
    assert await q.py('import renpy;s=renpy.store;t=type("CameraProbe",(),{})();s.r13_meeting_pan_tick(t,0,0);result=t.xoffset==0')
    await page.set_viewport_size({'width':844,'height':390});await shot('07-mobile-interview');await page.set_viewport_size({'width':1280,'height':720})
    await q.py('import renpy;s=renpy.store;s.r13_edit(day=14,period=2,location="altar",finale_started=True,mom_state="reunited",daram_state="with_dad");s.r13_meeting_active=False;result=True')
    await native_jump(q,'r13_final_hub');await q.wait('r13_crisis')
    title=await q.py('import renpy;result=renpy.store.R13_CLAIMS["F1"]["assertion"]');await q.press(title);await until('r13_debate_board');await q.press('되묻기');await q.wait('say');await shot('14-stone-altar-focused')
    assert await q.py('import renpy;s=renpy.store;t=type("CameraProbe",(),{})();s.r13_meeting_pan_tick(t,0,0);result=t.xoffset==0')
    print('PASS interview framing, mobile, altar and pan settles at centre',flush=True);return
   await until('r13_meeting_agenda');await shot('02-roundtable-agenda')
   await q.press('정문이 잠겼으니');await until('r13_debate_board');await shot('03-roundtable-statements')
   if os.environ.get('ROOM13_MEETING_SMOKE'):
    await q.py('import renpy;s=renpy.store;s.r13_edit(day=14,period=2,location="altar",finale_started=True,mom_state="reunited",daram_state="with_dad",evidence=[]);s.r13_meeting_active=False;result=True')
    await native_jump(q,'r13_final_hub');await q.wait('r13_crisis');await shot('15-blocked-claim-reasons')
    print('PASS final build opening, roundtable, blocked-claim reasons',flush=True);return
   board_present=next(b['rect'] for b in (await q.state())['buttons'] if b['text'].strip()=='보여주기')
   await q.press('되묻기');await q.wait('say');await shot('04-focused-speaker-neighbors')
   line_present=next(b['rect'] for b in (await q.state())['buttons'] if b['text'].strip()=='보여주기')
   assert board_present==line_present,(board_present,line_present)
   await q.press('더보기');await q.wait('r13_more_tools');await q.press('닫기')
   # Canceling live presentation must retain the outer dialogue cursor and all proof state.
   before=await q.py('import renpy;s=renpy.store;result={"proofs":list(s.room13["propositions"]),"debate":s.r13_debate_state(),"id":s.r13_read_id,"index":s.r13_index,"page":s.r13_page_i,"focus":s.r13_meeting_focus}')
   before_say=(await q.state())['say']
   await q.press('보여주기');await q.wait('r13_book');await q.press('그만두기')
   after=await q.py('import renpy;s=renpy.store;result={"proofs":list(s.room13["propositions"]),"debate":s.r13_debate_state(),"id":s.r13_read_id,"index":s.r13_index,"page":s.r13_page_i,"focus":s.r13_meeting_focus}')
   assert before==after,(before,after)
   assert (await q.state())['say']==before_say
   # A save made with the nested picker open must load at the original utterance.
   await q.press('보여주기');await q.wait('r13_book');await q.py('import renpy;renpy.exports.save("qa-meeting-live");result=True')
   await native_load(q,'qa-meeting-live');await q.wait('say')
   assert (await q.state())['say']==before_say
   assert await q.py('import renpy;s=renpy.store;result=not s.r13_meeting_interrupting and s.r13_meeting_pending_resume is None and renpy.exports.get_screen("r13_book") is None')
   await until(say='복도 쪽 문이죠');assert await q.py('import renpy;result=renpy.store.r13_meeting_live_target()=="s2"')
   await q.press('보여주기');await select_record('E05');await q.wait('say');await shot('05-live-evidence-and-speaker');await until('r13_debate_board')
   assert await q.py('import renpy;s=renpy.store;result=s.r13_debate_is_broken("C1","s2") and s.r13_debate_is_pressed("C1","s1") and not s.r13_meeting_interrupting')
   replay_before=await q.py('import renpy;s=renpy.store;result={k:s.room13.get(k) for k in ("debate","propositions","flags","evidence")}')
   await q.press('다시 듣기');await q.wait('say');await shot('16-replay-completed');await until('r13_debate_board')
   replay_after=await q.py('import renpy;s=renpy.store;result={k:s.room13.get(k) for k in ("debate","propositions","flags","evidence")}')
   assert replay_before==replay_after
   await q.press('‹');assert await q.py('import renpy;result=renpy.store.r13_debate_selected=="s1"')
   await q.press('›');assert await q.py('import renpy;result=renpy.store.r13_debate_selected=="s2"')
   if os.environ.get('ROOM13_MEETING_RESUME_ONLY'):
    print('PASS exact live cancel, nested save/load, live proof and outer dialogue resumption',flush=True);return
   await q.press('발언 기록');await shot('06-statement-history');await q.press('닫기')
   await page.set_viewport_size({'width':844,'height':390});await shot('07-mobile-meeting');await page.set_viewport_size({'width':1280,'height':720})
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await shot('08-large-text');await q.py('import renpy;renpy.store.persistent.room13_large_text=False;renpy.exports.restart_interaction();result=True')
   await q.press('결론을 말한다');await until('choice')
   weak=await q.py('import renpy;result=next(text for kind,text in renpy.store.R13_DEBATE["C1"]["conclusion"]["options"] if kind=="weak")')
   await q.press(weak);await until('r13_meeting_ballot');assert await q.py('import renpy;result="C1" not in renpy.store.room13["propositions"]');await q.press('회의를 계속한다');await until('r13_debate_board')
   await q.press('결론을 말한다');await until('choice');await shot('09-player-conclusion-choice')
   correct=await q.py('import renpy;result=next(text for kind,text in renpy.store.R13_DEBATE["C1"]["conclusion"]["options"] if kind=="correct")')
   await q.press(correct);await until('r13_meeting_ballot');await shot('10-public-ballot')
   assert await q.py('import renpy;s=renpy.store;result="C1" in s.room13["propositions"] and s.room13["meeting_votes"]["C1"]["choice"]=="correct" and s.room13["meeting_votes"]["C1"]["tally"]==s.r13_debate_tally("trial")')
   await q.press('회의를 계속한다');await until('r13_meeting_agenda');assert await q.py('import renpy;result=not renpy.store.r13_meeting_active')
   await q.press('다람이의 방어가');await until('r13_debate_board');await q.press('›');await q.press('›');await q.press('보여주기');await select_record('E09');await until('choice');await shot('11-opponent-counter-choice')
   await q.press('그 통로는 할머니만 썼다');await until('r13_debate_board');assert await q.py('import renpy;result=not renpy.store.r13_debate_is_broken("C2","s3")')
   await q.press('보여주기');await select_record('E09');await until('choice');await q.press('통로는 주방 레버로만 열린다');await until('r13_debate_board');assert await q.py('import renpy;result=renpy.store.r13_debate_is_broken("C2","s3")')
   await q.press('회의 중단');await q.wait('r13_confirm');await q.press('더 찾아본다');await until('r13_debate_board');assert await q.py('import renpy;result=not renpy.store.r13_debate_closed("C2")')
   # Explicit finale fixture: preserve canonical preparations; test only the relevant interaction.
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=14,period=2,location="altar",finale_started=True,mom_state="reunited",daram_state="with_dad");s.r13_meeting_active=False;result=True')
   await native_jump(q,'r13_final_hub');await q.wait('r13_crisis');await shot('12-stone-altar-agenda')
   title=await q.py('import renpy;result=renpy.store.R13_CLAIMS["F1"]["assertion"]');await q.press(title);await until('r13_debate_board');await shot('13-stone-altar-statements');await q.press('되묻기');await q.wait('say');await shot('14-stone-altar-focused')
   await until('r13_debate_board')
   await q.py('import renpy;renpy.store.r13_meeting_active=False;result=True');await native_jump(q,'r13_final_hub');await q.wait('r13_crisis')
   title=await q.py('import renpy;result=renpy.store.R13_CLAIMS["F3"]["assertion"]');await q.press(title);await until('r13_debate_board');await q.press('›');await q.press('›');await q.press('보여주기');await select_record('E21');await until('r13_debate_board')
   assert await q.py('import renpy;s=renpy.store;result=not s.r13_debate_is_broken("F3","s3") and not s.r13_has("operators_ready") and not s.r13_has("patient_transport")')
   (OUT/'result.json').write_text(json.dumps({'passed':True,'checks':['actual day7 opening and roundtable','live cancel preserves proof and dialogue','live hidden claim rebuttal resumes outer dialogue','completed replay preserves proof and hidden gates','previous/next statements','fixed presentation-button position','record history','mobile and large text','wrong conclusion no proof','correct conclusion and public opinions','wrong and correct counter','leave cancellation','actual day14 stone altar','no item bypass for actual preparations']},ensure_ascii=False,indent=2))
   print('PASS live meeting, camera, counter, ballots, stone altar, mobile',flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await browser.close()
asyncio.run(main())
