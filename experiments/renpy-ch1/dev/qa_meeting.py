"""Actual web meeting flow with explicit day-7/day-14 scene fixtures; not a full playthrough."""
import asyncio,json,os,time
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
  recording_started=time.monotonic()
  video_options={'record_video_dir':str(OUT/'video'),'record_video_size':{'width':1280,'height':720}} if os.environ.get('ROOM13_MEETING_RHYTHM') or os.environ.get('ROOM13_MEETING_ALTAR') else {}
  page=await browser.new_page(viewport={'width':1280,'height':720},**video_options);q=UIQA(page,OUT)
  async def shot(name):
   await asyncio.sleep(.35)  # Let the speaker pan settle before comparing framing.
   await q.shot(name)
  async def until(screen=None,say=None):
   for i in range(100):
    st=await q.state()
    if screen and screen in st['screens'] or say and 'say' in st['screens'] and say in st['say']:
     await asyncio.sleep(.4);return st
    if screen=='r13_debate_board' and not os.environ.get('ROOM13_MEETING_LOOP') and await q.py('import renpy;s=renpy.store;result=s.r13_meeting_live_active and not s.r13_meeting_interrupting and s.r13_read_id.startswith("meeting:live:")'):await q.press('발언 고르기')
    elif 'say' in st['screens']:await q.input(800,610)
    elif 'r13_cinematic_view' in st['screens']:await q.press('계속')
    elif any(s in st['screens'] for s in ('choice','r13_debate_board','r13_meeting_ballot','r13_meeting_agenda','r13_crisis')):
     raise AssertionError(('unexpected stop',screen,say,st['screens'],st['say'],[b['text'][:70] for b in st['buttons']]))
    else:await asyncio.sleep(.15)
   raise AssertionError(('timeout',screen,say))
  async def select_statement(sid):
   for _ in range(8):
    if await q.py('import renpy;result=renpy.store.r13_debate_selected=='+repr(sid)):return
    await q.press('›')
   raise AssertionError(('statement not found',sid))
  async def select_record(key):
   await q.wait('r13_book')
   title=await q.py('import renpy;s=renpy.store;result=s.R13_RECORD_SHORT.get('+repr(key)+',s.r13_catalog_title('+repr(key)+')[:8])')
   for i in range(20):
    st=await q.state()
    if any(title in b['text'] for b in st['buttons']):break
    # The book now restores its previous page. Navigate in either direction
    # through real buttons rather than assuming each opening starts at zero.
    direction=await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_book");s=renpy.store;entries=sc.scope["entries"];result="다음" if entries.index('+repr(key)+')//s.r13_record_page_size()>sc.scope["page"] else "이전"')
    await q.press(direction)
   await q.press(title);await q.press('이 주장에 근거로 낸다')
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await asyncio.sleep(.7)
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance()
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=7,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=list(s.ROOM13["evidence"]),propositions=[]);s.r13_flag("entry_corrected","lodging");s.r13_upgrade();result=True')
   await native_jump(q,'r13_trial');await q.wait('say');await shot('01-opening-focused')
   if os.environ.get('ROOM13_MEETING_LOGIC'):
    async def fixture(keys,flags=(),props=(),observations=None):
     args=dict(day=14,period=2,location='altar',finale_started=True,mom_state='reunited',daram_state='with_dad',evidence=list(keys),flags=list(flags),propositions=list(props),observations=observations or {},debate={},arguments={})
     await q.py('import renpy;s=renpy.store;s.r13_edit(**'+repr(args)+');s.r13_meeting_active=False;s.r13_meeting_intro=False;s.r13_meeting_live_active=False;result=True')
     await native_jump(q,'r13_final_hub');await q.wait('r13_crisis')
    async def open_claim(claim):
     title=await q.py('import renpy;result=renpy.store.R13_CLAIMS['+repr(claim)+']["assertion"]');await q.press(title);await until('r13_debate_board')
    async def present(sid,key):
     await select_statement(sid);await q.press('보여주기');await select_record(key);await until('r13_debate_board')
    async def conclusion(claim,kind):
     await q.press('결론을 말한다');await until('choice')
     text=await q.py('import renpy;result=dict(renpy.store.R13_DEBATE['+repr(claim)+']["conclusion"]["options"])['+repr(kind)+']')
     await q.press(text)
    observations=dict(first=dict(time=30,load='day_low',operator='buri',recorder='resident_seori'),second=dict(time=32,load='evening_high',operator='buri',recorder='resident_seori'))
    await fixture(['E21','E23']);await open_claim('F2');await select_statement('s1');await q.press('되묻기');await until('r13_debate_board')
    await present('s2','E21');await present('s3','E23')
    assert await q.py('import renpy;s=renpy.store;result=not s.r13_debate_ready("F2") and "F2" not in s.room13["propositions"]')
    await shot('50-first-test-insufficient')
    await q.py('import renpy;s=renpy.store;s.r13_edit(evidence=["E21","E23","E24"]);result=True')
    await present('s4','E24');assert await q.py('import renpy;result=not renpy.store.r13_debate_is_broken("F2","s4")')
    await shot('51-paper-without-observation')
    await q.py('import renpy;renpy.store.r13_edit(observations='+repr(observations)+');result=True')
    await present('s4','E24');assert await q.py('import renpy;result=renpy.store.r13_debate_ready("F2")'),await q.py('import renpy;s=renpy.store;result={"debate":s.r13_debate_state(),"obs":s.room13["observations"],"valid":s.r13_debate_observations_ready(),"held":s.room13["evidence"]}')
    await conclusion('F2','over');await until('r13_meeting_ballot')
    assert await q.py('import renpy;result="F2" not in renpy.store.room13["propositions"]')
    await q.press('회의를 계속한다');await until('r13_debate_board');await conclusion('F2','correct');await until('r13_meeting_ballot')
    assert await q.py('import renpy;s=renpy.store;result="F2" in s.room13["propositions"] and s.r13_resolve_ending()=="E4"')
    await shot('52-energy-proved-with-limits')
    await fixture(['E25','E26'])
    assert await q.py('import renpy;result=not renpy.store.r13_debate_open("F3")')
    await shot('53-papers-not-preparations')
    await q.py('import renpy;renpy.store.r13_flag("shelter_ready");renpy.exports.restart_interaction();result=True')
    await open_claim('F3');await present('s1','E25');await present('s2','E26')
    assert await q.py('import renpy;result=not renpy.store.r13_debate_is_broken("F3","s2")')
    await select_statement('s3');await q.press('되묻기');await until('r13_debate_board')
    assert await q.py('import renpy;s=renpy.store;result=not s.r13_debate_is_pressed("F3","s3") and not s.r13_has("operators_ready") and not s.r13_has("patient_transport")')
    await shot('54-missing-manpower-not-confirmed')
    await q.py('import renpy;renpy.store.r13_flag("supplies_ready","operators_ready","patient_transport");result=True')
    await present('s2','E26');await select_statement('s3');await q.press('되묻기');await until('r13_debate_board')
    assert await q.py('import renpy;result=renpy.store.r13_debate_ready("F3")')
    await conclusion('F3','correct');await until('r13_meeting_ballot');await shot('55-actual-preparations-confirmed')
    await fixture(['E01','E16','E17']);await open_claim('F4');await present('s1','E17')
    assert await q.py('import renpy;result=not renpy.store.r13_debate_is_broken("F4","s1")')
    await shot('56-meeting-is-not-warning')
    await q.py('import renpy;renpy.store.r13_edit(evidence=["E01","E16","E17","E18"]);result=True')
    await present('s1','E18');await present('s2','E16');await conclusion('F4','correct');await until('r13_meeting_ballot')
    assert await q.py('import renpy;result="F4" in renpy.store.room13["propositions"]')
    await shot('57-warning-and-separation-proved')
    (OUT/'result.json').write_text(json.dumps({'passed':True,'checks':['F2 first test alone insufficient','E24 paper without independent observations insufficient','actual evening observation completes F2','infinite-energy conclusion rejected','F2 alone resolves to E4 without preparations','F3 papers do not prepare shelter or supplies','missing manpower press does not mark confirmation','F3 actual preparations and question allow conclusion','F4 meeting record does not prove warning','actual warning and separation record allow F4']},ensure_ascii=False,indent=2))
    print('PASS F2 independent observation, F3 real preparations, F4 scope and wrong conclusions',flush=True);return
   if os.environ.get('ROOM13_MEETING_ALTAR'):
    await q.py('import renpy;s=renpy.store;s.r13_edit(day=14,period=2,location="altar",finale_started=True,mom_state="reunited",daram_state="with_dad");s.r13_meeting_active=False;s.r13_meeting_intro=False;result=True')
    await native_jump(q,'r13_final_hub');await q.wait('r13_crisis')
    title=await q.py('import renpy;result=renpy.store.R13_CLAIMS["F1"]["assertion"]');await q.press(title)
    await until(say='가족도 못 알아봅니다');await shot('40-standing-speaker')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_meeting_live_active and s.r13_meeting_claim=="F1" and s.r13_meeting_edge(640,"final")==432 and s.r13_meeting_edge(0,"final")==500 and "dad" not in dict(s.r13_meeting_cast("F1",s.r13_debate_session("F1")))')
    clip={'start':time.monotonic()-recording_started}
    await q.input(800,610);await q.wait('say');await shot('41-standing-peer')
    assert await q.py('import renpy;result=renpy.store.dialogue_speaker=="nabi"')
    await q.input(800,610);await q.wait('say');await shot('42-standing-next-statement')
    assert await q.py('import renpy;result=renpy.store.r13_meeting_live_sid=="s2"')
    clip['end']=time.monotonic()-recording_started
    await page.set_viewport_size({'width':844,'height':390});await shot('43-standing-mobile')
    await q.press('보여주기');await q.wait('r13_book');await q.press('그만두기');await q.wait('say')
    assert await q.py('import renpy;result=renpy.store.r13_meeting_live_sid=="s2"')
    await page.set_viewport_size({'width':1280,'height':720});await q.press('발언 고르기');await until('r13_debate_board')
    await select_statement('s1');await q.press('보여주기');await select_record('E20');await until('r13_debate_board')
    await select_statement('s2');await q.press('보여주기');await select_record('E31');await until('r13_debate_board')
    assert await q.py('import renpy;result=renpy.store.r13_debate_ready("F1")')
    await shot('44-standing-proven')
    await q.press('결론을 말한다');await until('choice')
    correct=await q.py('import renpy;result=next(text for kind,text in renpy.store.R13_DEBATE["F1"]["conclusion"]["options"] if kind=="correct")')
    await q.press(correct);await until('r13_meeting_ballot');await shot('45-standing-whole-council')
    assert await q.py('import renpy;s=renpy.store;result="F1" in s.room13["propositions"] and not s.r13_has("operators_ready") and not s.r13_has("patient_transport")')
    (OUT/'clip.json').write_text(json.dumps(clip,indent=2))
    (OUT/'result.json').write_text(json.dumps({'passed':True,'checks':['actual day14 altar standing stone slab','standing centre and two standing neighbors','same horizontal speaker camera','waist-high stone foreground rim at 432/500','no dad sprite','mobile presentation cancel retains utterance','actual F1 evidence and conclusion','whole council and public opinions around stone','preparation gates unchanged']},ensure_ascii=False,indent=2))
    print('PASS standing altar, speaker movement, mobile, actual proof and whole council',flush=True);return
   if os.environ.get('ROOM13_MEETING_LOOP'):
    async def live_at(sid):
     for _ in range(50):
      if await q.py('import renpy;s=renpy.store;result=s.r13_meeting_live_active and s.r13_meeting_live_sid=='+repr(sid)+' and s.r13_read_id.startswith("meeting:live:") and s.r13_index==0'):return
      await q.input(800,610)
     raise AssertionError(('missing live statement',sid))
    async def cursor():
     return await q.py('import renpy;s=renpy.store;result={"id":s.r13_read_id,"index":s.r13_index,"page":s.r13_page_i,"sid":s.r13_meeting_live_sid,"lap":s.r13_meeting_live_lap,"proofs":s.room13["propositions"],"evidence":s.room13["evidence"]}')
    await until('r13_meeting_agenda');await q.press('다람이의 방어가');await live_at('s1')
    assert '{color=' not in (await q.state())['say']
    await shot('30-live-first-pass')
    for lap in range(2):
     for sid in ('s2','s3','s1'):
      await q.input(800,610);await live_at(sid)
     assert await q.py('import renpy;result=renpy.store.r13_meeting_live_lap=='+str(lap+1))
    assert await q.py('import renpy;s=renpy.store;result=s.r13_meeting_heard("C2","s1") and s.r13_meeting_heard("C2","s2") and s.r13_meeting_heard("C2","s3") and not s.r13_debate_ready("C2") and not s.r13_debate_is_pressed("C2","s1")')
    await shot('31-two-loops')
    await q.press('더보기');await q.wait('r13_more_tools')
    assert not any(b['text'].strip() in ('읽은 것만','전부') for b in (await q.state())['buttons'])
    await q.press('토론 멈추기');await until('r13_debate_board');await q.press('토론 듣기');await live_at('s1')
    await q.py('import renpy;renpy.store.r13_fast_all=True;result=True');await q.input(800,610)
    assert await q.py('import renpy;s=renpy.store;result=not s.r13_fast_all and not s.r13_fast_read and s.r13_meeting_live_active')
    await live_at('s1')
    await q.press('‹');await live_at('s3');await q.press('›');await live_at('s1')
    before=await cursor();before_say=(await q.state())['say']
    await q.press('보여주기');await q.wait('r13_book');await q.py('import renpy;renpy.exports.save("qa-meeting-loop");result=True')
    await native_load(q,'qa-meeting-loop');await q.wait('say');assert await cursor()==before
    await q.press('보여주기');await q.wait('r13_book');await q.press('그만두기');assert await cursor()==before
    await q.press('되묻기');await until(say='말한 그대로입니다');await live_at('s1')
    assert await q.py('import renpy;result=renpy.store.r13_debate_is_pressed("C2","s1")')
    await q.press('›');await live_at('s2');before=await cursor()
    await q.press('보여주기');await select_record('E01');await until(say='촛대는')
    assert await cursor()==before
    assert await q.py('import renpy;result=not renpy.store.r13_debate_is_broken("C2","s2")')
    await shot('32-wrong-record-returns')
    await q.press('보여주기');await select_record('E35');await until(say='촛대는')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_debate_is_broken("C2","s2") and s.r13_meeting_live_target()=="s2"')
    await q.press('›');await live_at('s3');await q.press('‹');await live_at('s1')
    await q.press('발언 고르기');await until('r13_debate_board');await shot('33-heard-review')
    await q.press('발언 기록');await shot('34-heard-history');await q.press('닫기')
    await page.set_viewport_size({'width':844,'height':390});await q.press('토론 듣기');await live_at('s1');await shot('35-mobile-loop')
    await q.press('‹');await live_at('s3');await q.press('발언 고르기');await until('r13_debate_board')
    await page.set_viewport_size({'width':1280,'height':720})
    # The actual last required rebuttal exits listening and enables conclusion.
    await q.press('토론 듣기');await live_at('s3');await q.press('보여주기');await select_record('E09');await live_at('s1')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_debate_is_broken("C2","s3") and not s.r13_debate_ready("C2")')
    await q.press('보여주기');await select_record('E06');await until('r13_debate_board')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_debate_ready("C2") and not s.r13_meeting_live_active and s.room13["propositions"]==[]')
    await shot('36-ready-after-proof')
    # A true statement loops alone until a real question reveals the second one.
    await q.py('import renpy;s=renpy.store;s.r13_claim="C1";s.r13_meeting_claim="C1";s.r13_meeting_live_active=False;result=True')
    await q.py('import renpy;s=renpy.store;s.r13_debate_selected="s1";s.r13_debate_action=("round","s1");result=True');await native_jump(q,'r13_debate_dispatch');await live_at('s1')
    await q.input(800,610);await q.input(800,610);await live_at('s1')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_meeting_live_ids("C1","s1")==["s1"] and s.r13_meeting_live_lap>=1')
    await q.press('되묻기');await live_at('s2');await shot('37-question-reveals-statement')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_debate_visible("C1",s.r13_debate_statement("C1","s2")) and not s.r13_meeting_heard("C1","s2")')
    assert '{color=' not in (await q.state())['say']
    (OUT/'result.json').write_text(json.dumps({'passed':True,'checks':['two full automatic loops without proof or pressed flags','fast skip disabled during cyclic listening and more-menu stop works','previous and next wrap during dialogue','save/load and cancel restore repeated utterance and lap','press resumes own statement','wrong material returns exact utterance','successful rebuttal removed from loop','heard statements remain selectable','mobile loop and controls','last required proof exits to conclusion','hidden statement appears only after actual question','no automatic contradiction highlight']},ensure_ascii=False,indent=2))
    print('PASS loop, seek, heard status, press, material return, save/load, hidden reveal, completion and mobile',flush=True);return
   if os.environ.get('ROOM13_MEETING_RHYTHM'):
    await until('r13_meeting_agenda');await q.press('다람이의 방어가');await until(say='아이가 촛대로')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_meeting_live_active and s.r13_meeting_live_sid=="s1"')
    before_say=(await q.state())['say']
    before=await q.py('import renpy;s=renpy.store;result={"id":s.r13_read_id,"index":s.r13_index,"page":s.r13_page_i,"sid":s.r13_meeting_live_sid,"proofs":s.room13["propositions"],"evidence":s.room13["evidence"]}')
    await q.press('보여주기');await q.wait('r13_book');await q.py('import renpy;renpy.exports.save("qa-meeting-rhythm");result=True')
    await native_load(q,'qa-meeting-rhythm');await q.wait('say');assert (await q.state())['say']==before_say
    await q.press('보여주기');await q.wait('r13_book');await q.press('그만두기');assert (await q.state())['say']==before_say
    after=await q.py('import renpy;s=renpy.store;result={"id":s.r13_read_id,"index":s.r13_index,"page":s.r13_page_i,"sid":s.r13_meeting_live_sid,"proofs":s.room13["propositions"],"evidence":s.room13["evidence"]}')
    assert before==after
    await q.press('되묻기');await until(say='말한 그대로입니다');assert await q.py('import renpy;result=renpy.store.r13_read_id.startswith("debate:press:C2:s1")')
    await until(say='아이가 촛대로');assert await q.py('import renpy;s=renpy.store;result=s.r13_meeting_live_active and s.r13_debate_is_pressed("C2","s1")')
    await shot('20-live-round')
    clip={'start':time.monotonic()-recording_started}
    await q.input(800,610);await q.wait('say');assert await q.py('import renpy;result=renpy.store.dialogue_speaker=="buri"');await shot('21-peer-response')
    await q.input(800,610);await q.wait('say');assert await q.py('import renpy;s=renpy.store;result=s.dialogue_speaker=="resident_ppul" and s.r13_meeting_live_sid=="s2"');await shot('22-next-speaker')
    clip['pan_end']=time.monotonic()-recording_started
    await q.press('보여주기');await select_record('E35');await q.wait('say');await shot('23-live-rebuttal');await until(say='촛대는')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_meeting_live_active and s.r13_meeting_live_sid=="s2" and s.r13_debate_is_broken("C2","s2") and s.r13_meeting_live_target()=="s2"')
    await q.input(800,610);await q.wait('say');await q.input(800,610);await q.wait('say');await q.press('발언 고르기');await until('r13_debate_board');await shot('24-return-to-review')
    clip['end']=time.monotonic()-recording_started
    await q.py('import renpy;renpy.store.persistent.room13_motion=False;result=True');await q.press('‹')
    assert await q.py('import renpy;s=renpy.store;t=type("CameraProbe",(),{})();s.r13_meeting_pan_tick(t,0,0);a=(t.xoffset,t.alpha);s.r13_meeting_pan_tick(t,0,0,True);result=a==(0,1.0) and t.alpha==0.0')
    await shot('25-reduced-motion');await q.py('import renpy;renpy.store.persistent.room13_motion=True;result=True')
    await page.set_viewport_size({'width':844,'height':390});await select_statement('s3');await q.press('토론 듣기');await q.wait('say');await shot('26-mobile-live');await q.press('발언 고르기');await until('r13_debate_board')
    assert await q.py('import renpy;s=renpy.store;result=s.room13["propositions"]==[] and not s.r13_has("operators_ready") and not s.r13_has("patient_transport")')
    (OUT/'clip.json').write_text(json.dumps(clip,indent=2))
    (OUT/'result.json').write_text(json.dumps({'passed':True,'checks':['live round and peer response','interrupt to canonical press and resume listening','live material cancel and nested save/load','successful live rebuttal remains pinned to spoken claim','stop listening to review without closing claim','camera cuts and reduced motion','mobile live controls','no automatic proofs or preparation flags']},ensure_ascii=False,indent=2))
    print('PASS live round, press interruption, rebuttal, camera, mobile and save/load',flush=True);return
   if os.environ.get('ROOM13_MEETING_OPINIONS_ONLY'):
    await q.py('import renpy;s=renpy.store;s.r13_meeting_active=True;s.r13_meeting_intro=False;s.r13_claim="C1";s.r13_meeting_claim="C1";s.r13_debate_selected="s2";s.r13_meeting_begin_opinions("C1");s.r13_edit(propositions=["C1"]);s.r13_debate_mark("pressed","C1","s1");s.r13_debate_mark("broken","C1","s2");result=True')
    await native_jump(q,'r13_debate_loop');await until('r13_debate_board');await shot('19-completed-controls');await q.press('결론을 말한다');await until('choice')
    correct=await q.py('import renpy;result=next(text for kind,text in renpy.store.R13_DEBATE["C1"]["conclusion"]["options"] if kind=="correct")')
    await q.press(correct);await until(say='동의하지 않아요');await shot('17-changed-resident-reaction')
    assert await q.py('import renpy;s=renpy.store;result=s.r13_read_id.startswith("meeting:opinions:C1") and s.dialogue_speaker in [row["person"] for row in s.r13_meeting_vote["changed"]]')
    await until('r13_meeting_ballot');await shot('18-opinions-after-reactions')
    print('PASS changed residents speak before public opinion tally',flush=True);return
   if os.environ.get('ROOM13_MEETING_FRAME_ONLY'):
    assert await q.py('import renpy;s=renpy.store;t=type("CameraProbe",(),{})();s.r13_meeting_pan_tick(t,0,0);result=t.xoffset==0')
    await page.set_viewport_size({'width':844,'height':390});await shot('07-mobile-interview');await page.set_viewport_size({'width':1280,'height':720})
    await q.py('import renpy;s=renpy.store;s.r13_edit(day=14,period=2,location="altar",finale_started=True,mom_state="reunited",daram_state="with_dad");s.r13_meeting_active=False;s.r13_meeting_intro=False;result=True')
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
   await q.press('다람이의 방어가');await until('r13_debate_board');await select_statement('s3');await q.press('보여주기');await select_record('E09');await until('choice');await shot('11-opponent-counter-choice')
   await q.press('그 통로는 할머니만 썼다');await until('r13_debate_board');assert await q.py('import renpy;result=not renpy.store.r13_debate_is_broken("C2","s3")')
   await q.press('보여주기');await select_record('E09');await until('choice');await q.press('통로는 주방 레버로만 열린다');await until('r13_debate_board');assert await q.py('import renpy;result=renpy.store.r13_debate_is_broken("C2","s3")')
   await q.press('회의 중단');await q.wait('r13_confirm');await q.press('더 찾아본다');await until('r13_debate_board');assert await q.py('import renpy;result=not renpy.store.r13_debate_closed("C2")')
   # Explicit finale fixture: preserve canonical preparations; test only the relevant interaction.
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=14,period=2,location="altar",finale_started=True,mom_state="reunited",daram_state="with_dad");s.r13_meeting_active=False;s.r13_meeting_intro=False;result=True')
   await native_jump(q,'r13_final_hub');await q.wait('r13_crisis');await shot('12-stone-altar-agenda')
   title=await q.py('import renpy;result=renpy.store.R13_CLAIMS["F1"]["assertion"]');await q.press(title);await until('r13_debate_board');await shot('13-stone-altar-statements');await q.press('되묻기');await q.wait('say');await shot('14-stone-altar-focused')
   await until('r13_debate_board')
   await q.py('import renpy;renpy.store.r13_meeting_active=False;result=True');await native_jump(q,'r13_final_hub');await q.wait('r13_crisis')
   title=await q.py('import renpy;result=renpy.store.R13_CLAIMS["F3"]["assertion"]');await q.press(title);await until('r13_debate_board');await select_statement('s3');await q.press('보여주기');await select_record('E21');await until('r13_debate_board')
   assert await q.py('import renpy;s=renpy.store;result=not s.r13_debate_is_broken("F3","s3") and not s.r13_has("operators_ready") and not s.r13_has("patient_transport")')
   (OUT/'result.json').write_text(json.dumps({'passed':True,'checks':['actual day7 opening and roundtable','live cancel preserves proof and dialogue','live hidden claim rebuttal resumes outer dialogue','completed replay preserves proof and hidden gates','previous/next statements','fixed presentation-button position','record history','mobile and large text','wrong conclusion no proof','correct conclusion and public opinions','wrong and correct counter','leave cancellation','actual day14 stone altar','no item bypass for actual preparations']},ensure_ascii=False,indent=2))
   print('PASS live meeting, camera, counter, ballots, stone altar, mobile',flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:
   video=page.video
   await browser.close()
   if video:
    Path(await video.path()).rename(OUT/'meeting-recording.webm')
asyncio.run(main())
