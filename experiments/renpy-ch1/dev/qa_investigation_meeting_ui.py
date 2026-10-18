import asyncio,json,sys
from pathlib import Path
sys.path.insert(0,'dev')
from playwright.async_api import async_playwright
from webqa import UIQA,FLOW_PROBE
import os
OUT=Path(os.environ.get('ROOM13_UI_QA_OUT','/tmp/room13-investigation-meeting-ui'))
class Q(UIQA):
 async def py(self,code):return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)
 async def state(self):
  probe=FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_debate_board','r13_records',")
  st=await self.py('ns={};exec('+ascii(probe)+',ns);result=ns["result"]');assert '_exception'not in st['screens'],st;return st
 async def jump(self,label):
  code='\n'.join(['import renpy','def qa_jump(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 시작",clicked=s.Jump('+repr(label)+'),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_jump',qa_jump,modal='True',zorder='200')","renpy.exports.show_screen('qa_jump')","renpy.exports.restart_interaction()","result=True"])
  await self.py(code);await self.press('검토 시작');await self.py('import renpy;renpy.exports.hide_screen("qa_jump");renpy.exports.restart_interaction();result=True')
 async def until(self,name):
  for _ in range(100):
   st=await self.state()
   if name in st['screens']:await asyncio.sleep(.4);return st
   if 'say'in st['screens']:await self.input(810,610)
   else:await asyncio.sleep(.2)
  raise AssertionError((name,st))
async def main():
 report={'kind':'Scoped UI fixtures: gate investigation and day-10 C2 council, representative owned evidence; not a story playthrough','checks':[],'captures':[]}
 async with async_playwright() as p:
  OUT.mkdir(parents=True,exist_ok=True)
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  page.on('console',lambda msg: print('BROWSER',msg.text,flush=True) if msg.type=='error' else None)
  page.on('pageerror',lambda err: print('PAGEERROR',str(err),flush=True))
  async def shot(name):
   await page.mouse.move(1270,2);await q.shot(name);report['captures'].append(name)
   st=await q.state()
   footer=[x for x in st['buttons'] if x['rect'][1]>=624 and x['rect'][2]>180]
   for button in footer:
    x,y,w,h=button['rect']
    assert w==232 and h in (64,80) and y+h==704,(name,button)
   for a,bn in zip(sorted(footer,key=lambda x:x['rect'][0]),sorted(footer,key=lambda x:x['rect'][0])[1:]):
    assert a['rect'][0]+a['rect'][2]<=bn['rect'][0],(name,'footer overlap')
  try:
   await page.goto(os.environ.get('ROOM13_UI_QA_URL','http://127.0.0.1:8776/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.py('import renpy;renpy.exports.show_screen("r13_control_specimen");renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(.4);await shot('00-pc-components')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   await shot('00-mobile-components')
   await q.py('import renpy;renpy.exports.hide_screen("r13_control_specimen");renpy.store.persistent.room13_large_text=False;renpy.exports.restart_interaction();result=True')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=1,period=1,location="gate",evidence=["E01"]);s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.r13_field_location="gate";s.r13_field_view="scene";s.r13_field_spots=False;s.r13_field_pick=None;s.place=s.R13_PLACES["gate"][0];s.r13_scene_bg=s.R13_PLACES["gate"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_entry');await q.wait('r13_hub');await shot('01-pc-investigate')
   before=await q.room();await shot('02-pc-hotspots')
   await q.input(1120,420);await asyncio.sleep(.4)
   assert await q.py('import renpy;result=renpy.store.r13_field_selection()') in ['gate_documents','booth']
   assert await q.room()==before;await shot('03-pc-selected-object')
   await q.press('사람 보기');assert await q.room()==before;await shot('04-pc-people')
   assert any(x['text'].strip()=='돌목' for x in (await q.state())['buttons'])
   await q.press('주변 살피기');assert not any(x['text'].strip()=='돌목' for x in (await q.state())['buttons'])
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   await shot('05-mobile-investigate')
   await q.input(1120,420);assert await q.room()==before
   await q.press('살펴보기');await q.until('r13_hub');assert 'G1' in (await q.room())['evidence']
   report['checks'].append('PC and touch: view/marker/target selection preserve exact game state; only explicit inspect runs the real G1 discovery')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="room13");s.r13_flag("entry_corrected","lodging");s.place=s.R13_PLACES["room13"][0];s.r13_scene_bg=s.R13_PLACES["room13"][1];renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub');await shot('05b-mobile-room-controls')
   # Meeting fixture deliberately matches the canonical day, with a representative small evidence set.
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;s.r13_edit(day=s.R13_TRIAL_DAY,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E01","E02","E03","E05","E06","E07","E08","E10","E11","E12","E15"],propositions=[]);s.r13_flag("entry_corrected","lodging");result=True')
   await q.jump('r13_trial');await q.until('r13_meeting_agenda');await shot('06-pc-meeting-agenda')
   await q.press('다람이의 방어가');await q.until('say')
   for _ in range(80):
    st=await q.state()
    if any('발언 선택' in x['text'] for x in st['buttons']):break
    await q.input(810,610)
   await shot('07-pc-listening');await q.press('더보기');await shot('07b-pc-more');await page.keyboard.press('Escape');await q.wait('say')
   before=await q.room();await q.press('자료 보여주기');await q.wait('r13_book');await shot('08-pc-live-evidence')
   assert await q.py('import renpy;result=renpy.store.r13_meeting_active')
   await q.press('그만두기');await q.wait('say');assert await q.room()==before
   await q.press('발언 선택');await q.until('r13_debate_board');await shot('09-pc-review-statement')
   before=await q.room();selected=await q.py('import renpy;result=renpy.store.r13_meeting_live_target()')
   await q.press('자료 보여주기');await q.wait('r13_book');await shot('10-pc-review-evidence')
   await q.press('그만두기');await q.wait('r13_debate_board');assert await q.room()==before
   await q.press('기록');assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records") is not None')
   await shot('11-pc-meeting-records');await q.press('닫기');await q.wait('r13_debate_board');after=await q.room();assert {k:v for k,v in after.items() if k!='record_ui'}=={k:v for k,v in before.items() if k!='record_ui'};before=after
   report['checks'].append('Actual meeting dispatcher: listening -> evidence -> cancel -> listening; review -> evidence/records -> cancel -> review, story state preserved (records may mark an item read)')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   await shot('12-mobile-review')
   await q.press('자료 보여주기');await q.wait('r13_book');await shot('13-mobile-evidence');await q.press('그만두기');await q.wait('r13_debate_board');assert await q.room()==before
   await q.press('토론 듣기');await q.until('say');await shot('14-mobile-listening')
   assert not await q.py('import renpy;result=renpy.display.screen.get_screen("_exception") is not None')
   report['checks'].append('844x390 large text: touch presentation and cancellation, review/listen mode transition pass')
   report['checks'].append('All captured gameplay footers: equal 232px widths, 64/80px heights, shared baseline and no overlap')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
