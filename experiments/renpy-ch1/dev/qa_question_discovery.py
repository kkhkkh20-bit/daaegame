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
  probe=FLOW_PROBE.replace('names=[',"names=['r13_resident_approach','r13_meeting_agenda','r13_debate_board','r13_records',")
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
 report={'kind':'Focused causal-question and empty-contact PC/touch fixtures; not a complete story playthrough','checks':[]}
 async with async_playwright() as p:
  OUT.mkdir(parents=True,exist_ok=True)
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  async def shot(name):
   await page.mouse.move(1270,2);await asyncio.sleep(.3);await q.shot(name)
  async def keys():return await q.py('import renpy;result=[k for k,t in renpy.store.r13_topics("granny")]')
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="inn",evidence=["E01"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.persistent.r13_pan_hint_seen=True;s.r13_world_cameras={};s.r13_field_location=None;s.r13_field_view="scene";s.r13_field_pick=None;s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub');initial=await keys();report['initial_keys']=initial
   assert 'granny_letter' in initial and not any(k in initial for k in ['granny_rules','life:granny:work','alibi:night1:granny']),initial
   before=await q.room();await shot('01-pc-field-before-conversation');assert await q.room()==before
   await q.press('할머니');await q.until('r13_resident_approach');await q.press('아내 편지를 받고 찾아왔습니다.');await q.until('r13_topics');await shot('02-pc-wife-question-only')
   assert 'life:granny:work' not in await keys()
   await q.press('아내가 가족을 불렀는지');await q.until('r13_topics');await shot('03-pc-followup-after-actual-subject')
   assert 'life:granny:work' in await keys();assert 'alibi:night1:granny' not in await keys();assert 'granny_rules' not in await keys()
   report['learned_sources']=await q.py('import renpy;result=renpy.store.room13.get("question_cues",{})')
   assert 'life:granny:work' in report['learned_sources'];report['checks'].append('Day-2 initial questions contain wife lead, not guests/locks/first-night; actual wife/date dialogue mentions guests and only then adds that follow-up')
   await q.press('돌아가기');await q.until('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(read_topics=list(dict.fromkeys(s.room13.get("read_topics",[])+[k for k,t in s.r13_topics("granny")])),resident_knowledge={"granny":["E01:anonymous"]});renpy.exports.restart_interaction();result=True')
   assert not await q.py('import renpy;result=renpy.store.r13_contact_has_content("granny")')
   before=await q.room();await q.press('할머니');await asyncio.sleep(.2);assert 'r13_hub' in (await q.state())['screens'];st=await q.state();assert not any(n in st['screens'] for n in ['r13_topics','r13_resident_approach','say']);assert await q.room()==before;await shot('04-pc-empty-contact-stays-in-field')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   before=await q.room();await q.press('할머니');await asyncio.sleep(.2);assert 'r13_hub' in (await q.state())['screens'];assert await q.room()==before;await shot('05-mobile-empty-contact-stays-in-field')
   report['checks'].append('PC and touch: when questions are read and relevant record already shown, clicking the real resident keeps field/camera and exact game state; a short notification replaces portrait/empty questions')
   await q.py('import renpy;s=renpy.store;s.r13_edit(resident_knowledge={});renpy.exports.restart_interaction();result=True')
   before=await q.room();assert await q.py('import renpy;result=renpy.store.r13_contact_has_content("granny")');assert await q.room()==before
   report['checks'].append('An unshown owned relevant record keeps contact available; eligibility checks award no flags, meetings, evidence or knowledge')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;s.r13_edit(location="forest");s.place=s.R13_PLACES["forest"][0];s.r13_scene_bg=s.R13_PLACES["forest"][1];renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub');await q.press('칼바람');await q.until('r13_topics');assert await q.py('import renpy;result="kalbaram:edge" not in [k for k,t in renpy.store.r13_topics("resident_kalbaram")]');await shot('06-pc-hunter-mother-question')
   await q.press('아내');await q.until('r13_topics');await shot('07-pc-hunter-after-witness-account')
   assert 'alibi:night1:granny' in await keys()
   assert await q.py('import renpy;s=renpy.store;result=s.r13_has("alibi:night1:resident_kalbaram") and "alibi:night1:resident_kalbaram" not in [k for k,t in s.r13_topics("resident_kalbaram")]')
   report['checks'].append('Actual mother-search question to hunter delivers the existing first-night witness account, unlocks checking that night with Granny, and avoids a duplicate hunter question')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'))
   try:report['failure_state']=await q.state()
   except:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
asyncio.run(main())
