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
 OUT.mkdir(parents=True,exist_ok=True);report={'kind':'Focused inn hit conflict and touch swipe; day-2 UI fixture','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True');await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="inn",evidence=["E01"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.r13_world_cameras={};s.r13_field_view="scene";s.r13_field_spots=False;s.r13_field_pick=None;s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub')
   rect=await q.py('import renpy;s=renpy.store;x,y,w,h=s.ROOM13["objects"]["inn"]["keys"]["rect"];result=[x-s.r13_world_offset(),y,w,h]');x,y,w,h=rect
   for mobile in [False,True]:
    tag='mobile' if mobile else 'pc';q.touch=mobile;await page.set_viewport_size({'width':844 if mobile else 1280,'height':390 if mobile else 720})
    await q.py('import renpy;renpy.store.persistent.room13_large_text='+repr(mobile)+';renpy.exports.restart_interaction();result=True')
    before=await q.room();await q.input(x+w/2,y+h/2);await q.wait('r13_map');await q.shot(tag+'-keys-center-opens-map');assert await q.room()==before
    await q.press('현장으로 돌아가기');await q.wait('r13_hub');await q.input(x+w/2,y+h-20)
    picked=await q.py('import renpy;result=renpy.store.r13_field_selection()');await q.shot(tag+'-keys-lower-area-selects');assert picked=='keys',picked
    report['checks'].append({'platform':tag,'keys_rect':rect,'center_tap_result':'r13_map (outside travel button intercepts)','lower_tap_result':picked,'story_state_unchanged':await q.room()==before})
   before=await q.room();cdp=await page.context.new_cdp_session(page)
   def point(x,y):return {'x':(844-1280*(390/720))/2+x*(390/720),'y':y*(390/720)}
   await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[point(600,400)]})
   for i in range(1,11):
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[point(600+40*i,400)]});await asyncio.sleep(.025)
   await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await asyncio.sleep(.5)
   offset=await q.py('import renpy;result=renpy.store.r13_world_offset()');await q.shot('mobile-real-swipe');assert offset<640,offset;assert await q.room()==before
   report['checks'].append({'touch_swipe_offset':offset,'story_state_unchanged':True});report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
