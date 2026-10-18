import asyncio,json,sys
from pathlib import Path
sys.path.insert(0,'dev')
from playwright.async_api import async_playwright
from webqa import UIQA,FLOW_PROBE
import os
OUT=Path(os.environ.get('ROOM13_UI_QA_OUT','/tmp/room13-direct-investigation'))
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
 report={'kind':'Scoped real object-discovery/presentation and pan fixtures; not a whole-story playthrough','checks':[]}
 async with async_playwright() as p:
  OUT.mkdir(parents=True,exist_ok=True)
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/')
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   for touch in (False,True):
    await page.set_viewport_size({'width':844,'height':390} if touch else {'width':1280,'height':720});q.touch=touch
    await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=1,period=1,location="gate",evidence=["E01"]);s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.r13_field_location="gate";s.r13_field_view="people";s.r13_world_cameras={};s.r13_field_pick=None;s.place=s.R13_PLACES["gate"][0];s.r13_scene_bg=s.R13_PLACES["gate"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
    await q.jump('r13_entry');await q.wait('r13_hub');await q.shot(('mobile' if touch else 'pc')+'-background-no-markers')
    assert not any(x['text'].strip() in ('살펴보기','주변 살피기','사람 보기') for x in (await q.state())['buttons'])
    assert 'G1' not in (await q.room())['evidence']
    await q.input(1120,420);await q.until('r13_hub');assert 'G1' in (await q.room())['evidence']
    await q.shot(('mobile' if touch else 'pc')+'-discovery')
    await q.press('돌목');await q.until('r13_entry_topics')
    report['topics_state']=await q.state()
    await q.press('자료');await q.until('r13_book')
    await q.shot(('mobile' if touch else 'pc')+'-owned-record')
    report['book_state']=await q.state()
    # Select the actual newly obtained record in the presentation book.
    await q.press('예약');await q.press('돌목에게 보여주기');await q.until('r13_hub')
    assert 'entry_corrected' in (await q.room())['flags']
    await q.shot(('mobile' if touch else 'pc')+'-after-presentation')
    report['checks'].append(('Touch' if touch else 'PC')+': object tap runs real G1 discovery, owned record can be presented to guard')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="inn");s.r13_flag("entry_corrected","lodging");s.r13_field_location="inn";s.r13_field_view="people";s.r13_world_cameras={};s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub')
   for key in ('keys','register'):
    rect=await q.py('import renpy;s=renpy.store;result=s.ROOM13["objects"]["inn"]['+repr(key)+']["rect"]')
    offset=await q.py('import renpy;result=renpy.store.r13_world_offset()')
    x,y,w,h=rect;await q.input(x+w/2-offset,y+h/2);await q.advance()
    assert await q.py('import renpy;result=renpy.store.r13_has('+repr('observed:inn:'+key)+')')
    st=await q.state()
    if 'r13_object_context' in st['screens']:
     await q.press('그만 살펴본다');await q.advance()
    await q.wait('r13_hub')
   report['checks'].append('Two inn objects directly run observation instead of target selection')
   before=await q.room();cdp=await page.context.new_cdp_session(page)
   def point(x,y):return {'x':(844-1280*(390/720))/2+x*(390/720),'y':y*(390/720)}
   # Confirm real camera movement, rather than a swipe against the camera limit.
   await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[point(600,400)]})
   for i in range(1,11):
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[point(600+40*i,400)]});await asyncio.sleep(.025)
   await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await asyncio.sleep(.5)
   assert 'r13_hub' in (await q.state())['screens'];assert await q.room()==before
   offset=await q.py('import renpy;result=renpy.store.r13_world_offset()');assert offset<640,offset
   report['touch_pan_offset']=offset
   await q.shot('mobile-pan-no-inspection')
   report['checks'].append('Real touchscreen swipe over background does not inspect or change story state')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));report['failure_state']=await q.state();raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
