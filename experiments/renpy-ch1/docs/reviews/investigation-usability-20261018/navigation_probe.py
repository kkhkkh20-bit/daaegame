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
 OUT.mkdir(parents=True,exist_ok=True)
 report={'baseline':'0.19.47 ec6acca9','kind':'Focused day-2 UI fixtures, actual map/local-travel clicks; no full story playthrough','checks':[],'observations':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  async def shot(name):
   await page.mouse.move(1270,2);await q.shot(name)
  async def meta():
   return await q.py('import renpy;s=renpy.store;result=dict(location=s.room13["location"],mode=s.r13_field_view,pick=s.r13_field_pick,selection=s.r13_field_selection(),spots=s.r13_field_spots,offset=s.r13_world_offset(),width=s.r13_world_width(),objects=[dict(key=k,name=s.r13_object_name(k),rect=v["rect"]) for k,v in s.ROOM13["objects"].get(s.room13["location"],{}).items() if s.r13_object_visible(v)])')
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="inn",evidence=["E01"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.r13_world_cameras={};s.r13_field_view="scene";s.r13_field_spots=False;s.r13_field_pick=None;s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub');await shot('01-inn-initial');report['observations'].append({'initial':await meta()})
   before=await q.room();camera=(await meta())['offset'];await q.press('지도 · 이동');await q.wait('r13_map');await shot('02-inn-map');await q.press('13호실');await shot('03-map-selected-room');assert await q.room()==before
   await q.press('현장으로 돌아가기');await q.wait('r13_hub');assert await q.room()==before;assert (await meta())['offset']==camera
   report['checks'].append('Map destination selection and cancel preserve exact game state and camera')
   await q.press('사람과 대화');await q.press('2층 복도');await q.until('r13_hub');await shot('04-hall-after-people-mode');report['observations'].append({'arrive_hall':await meta()})
   await q.press('13호실');await q.until('r13_hub');await shot('05-room-inherited-mode');report['observations'].append({'arrive_room':await meta()})
   await q.press('주변 살피기');await shot('06-room-scene-no-markers')
   m=await meta();coat=next(o for o in m['objects'] if o['key']=='coat');x,y,w,h=coat['rect'];await q.input(x+w/2-m['offset'],y+h/2)
   await shot('07-selected-coat');report['observations'].append({'select_coat':await meta()})
   await q.press('›');await shot('08-selection-after-pan');report['observations'].append({'after_pan':await meta()})
   await q.press('조사 지점');await shot('09-room-markers');report['observations'].append({'markers':await meta()})
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await shot('10-mobile-room-markers')
   before=await q.room();await q.press('지도 · 이동');await q.wait('r13_map');await shot('11-mobile-inn-map');await q.press('마을');await shot('12-mobile-village-from-room')
   rect=await q.py('import renpy;result=renpy.store.r13_cart_name_rect("school")');x,y,w,h=rect;await q.input(x+w/2,y+h/2);await shot('13-mobile-map-selected-school');assert await q.room()==before
   await q.press('이곳으로 이동');await q.until('r13_hub');await shot('14-mobile-arrive-school');report['observations'].append({'arrive_school':await meta()})
   assert (await q.room())['location']=='school'
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('여관 안');await q.press('13호실');await q.press('이곳으로 이동');await q.until('r13_hub');await shot('15-mobile-return-room');report['observations'].append({'return_room':await meta()})
   assert (await q.room())['location']=='room13';report['checks'].append('Actual inn→hall→room and mobile map room→school→room completed; inspect observations for retained mode/selection/camera')
   before=await q.room();await q.press('기록');await q.press('닫기');await q.wait('r13_hub');after=await q.room();assert {k:v for k,v in after.items() if k!='record_ui'}=={k:v for k,v in before.items() if k!='record_ui'}
   await shot('16-after-record-return');report['checks'].append('Records return preserves story state and exploration view')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'))
   try:report['failure_state']=await q.state()
   except:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
