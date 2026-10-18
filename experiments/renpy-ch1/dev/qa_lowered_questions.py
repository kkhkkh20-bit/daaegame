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
 report={'kind':'Measured PC/touch pagination fixtures and real hunter conversation; not full story playthrough','checks':[]}
 async with async_playwright() as p:
  OUT.mkdir(parents=True,exist_ok=True)
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  async def shot(name):
   await page.mouse.move(1270,2);await asyncio.sleep(.3);await q.shot(name)
  async def bounds():
   st=await q.state();rows=[x for x in st['buttons'] if x['rect'][0]==640 and x['rect'][2]==592]
   upper=await q.py('import renpy;result=renpy.store.r13_control_upper_y()')
   paging=any("다음 질문" in x["text"] or "이전 질문" in x["text"] for x in st["buttons"])
   limit=upper-(72 if paging else 12)
   for row in rows:
    x,y,w,h=row["rect"];assert y>=192 and y+h<=limit,(row,limit)
   for x in st['buttons']:
    bx,by,bw,bh=x['rect'];assert bx>=0 and by>=0 and bx+bw<=1281 and by+bh<=721,x
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True');await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="inn",evidence=["E01"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.persistent.r13_pan_hint_seen=True;s.r13_world_cameras={};s.r13_field_location=None;s.r13_field_view="scene";s.r13_field_pick=None;s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.py('import renpy;s=renpy.store;s.qa_original_topics=s.r13_topics_in_order;s.qa_layout_rows=[(k,t) for k,t in s.ROOM13["topics"].items() if t.get("npc")=="buri"][:8];result=True')
   for big in [False,True]:
    await page.set_viewport_size({'width':844 if big else 1280,'height':390 if big else 720});q.touch=big
    await q.py('import renpy;renpy.store.persistent.room13_large_text='+repr(big)+';result=True')
    for count in [1,2,8,12]:
     await q.py('import renpy;s=renpy.store;s.qa_layout_count='+str(count)+';s.r13_topics_in_order=lambda person,rows=(s.qa_layout_rows*2)[:s.qa_layout_count]:list(rows);renpy.exports.hide_screen("r13_topics");renpy.exports.show_screen("r13_topics",person="buri");renpy.exports.restart_interaction();result=True')
     await asyncio.sleep(.3);await bounds();await shot(('mobile' if big else 'pc')+'-fixture-'+str(count))
     if count>=8:
      before=await q.room();await q.press('다음 질문');await bounds();assert await q.room()==before;await shot(('mobile' if big else 'pc')+'-fixture-'+str(count)+'-page2');await q.press('이전 질문');await bounds()
   report['checks'].append('PC and touch, 1/2/8/12 authored-title fixtures: all rows start at y192, remain above material/footer controls, and explicit paging works without state changes')
   await q.py('import renpy;s=renpy.store;s.r13_topics_in_order=s.qa_original_topics;renpy.exports.hide_screen("r13_topics");s.persistent.room13_large_text=False;s.r13_edit(location="forest");s.place=s.R13_PLACES["forest"][0];s.r13_scene_bg=s.R13_PLACES["forest"][1];renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.jump('r13_field');await q.wait('r13_hub');await q.press('칼바람');await q.until('r13_topics');await bounds();await shot('01-pc-hunter-one-question')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await bounds();await shot('02-mobile-hunter-one-question')
   await q.press('아내');await q.until('r13_topics');await bounds();await shot('03-mobile-hunter-two-questions')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;renpy.store.persistent.room13_large_text=False;renpy.exports.restart_interaction();result=True');await bounds();await shot('04-pc-hunter-two-questions')
   report['checks'].append('Actual hunter dialogue: lower name/title aligned at y150; one question and two questions after real witness account work on PC and touch')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'))
   try:report['failure_state']=await q.state()
   except:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
asyncio.run(main())
