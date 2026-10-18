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
 report={'kind':'Focused PC/touch UI fixtures, not a full story review','checks':[]}
 async with async_playwright() as p:
  OUT.mkdir(parents=True,exist_ok=True)
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  async def shot(name):
   await page.mouse.move(1270,2);await asyncio.sleep(.4);await q.shot(name)
  async def meta():
   return await q.py('import renpy;s=renpy.store;result=dict(location=s.room13["location"],view=s.r13_field_view,pick=s.r13_field_pick,target=s.r13_field_selection(),offset=s.r13_world_offset())')
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/')
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="inn",evidence=["E01"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.persistent.r13_pan_hint_seen=True;s.r13_world_cameras={};s.r13_field_location=None;s.r13_field_view="scene";s.r13_field_pick=None;s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub');assert (await meta())['view']=='people'
   await shot('01-pc-default-people')
   buttons=(await q.state())['buttons'];assert not any(x['text'].strip() in ['식당','주방','2층 복도','여관 밖','사람과 대화','조사 지점','더보기'] for x in buttons),buttons
   before=await q.room();await q.press('주변 살피기');assert (await meta())['view']=='scene';assert await q.room()==before
   await shot('02-pc-background-investigation')
   await q.input(1105,221);await asyncio.sleep(.4);assert (await meta())['target']=='keys',await meta();assert 'r13_map' not in (await q.state())['screens']
   await shot('03-pc-selected-keys');report['checks'].append('People default; redundant controls removed; scene hides people; formerly blocked keys center now selects keys')
   before=await q.room();cam=(await meta())['offset'];await q.press('지도 · 이동');await q.wait('r13_map');await q.press('13호실');await q.press('현장으로 돌아가기');await q.wait('r13_hub');assert await q.room()==before;assert (await meta())['offset']==cam;assert (await meta())['view']=='scene'
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('13호실');await q.press('이곳으로 이동');await q.until('r13_hub');assert (await meta())['location']=='room13';assert (await meta())['view']=='people';assert (await meta())['pick'] is None
   await q.press('주변 살피기');await q.input(228,478);assert (await meta())['target']=='coat',await meta()
   await q.press('›');assert (await meta())['target'] is None;assert (await meta())['pick'] is None
   await shot('04-pc-pan-clears-hidden-selection');report['checks'].append('Actual map-only travel; destination resets to people; offscreen selection clears after pan; map cancel preserves exact story/view/camera')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   await shot('05-mobile-background-investigation')
   before=await q.room();await q.press('기록');await q.press('닫기');await q.wait('r13_hub');after=await q.room();assert {k:v for k,v in after.items() if k!='record_ui'}=={k:v for k,v in before.items() if k!='record_ui'}
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('마을');await shot('06-mobile-map-current-inn')
   assert await q.py('import renpy;result=renpy.store.room13["location"] in renpy.store.R13_INN_LOCATIONS')
   rect=await q.py('import renpy;result=renpy.store.r13_cart_name_rect("school")');x,y,w,h=rect;await q.input(x+w/2,y+h/2);await q.press('이곳으로 이동');await q.until('r13_hub');assert (await meta())['location']=='school';assert (await meta())['view']=='people'
   await shot('07-mobile-default-people')
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('여관 안');await q.press('13호실');await q.press('이곳으로 이동');await q.until('r13_hub');assert (await meta())['pick'] is None;assert (await meta())['offset']==880
   await q.press('주변 살피기');await shot('08-mobile-return-no-stale-target');report['checks'].append('Touch map room→school→room works; camera persists without stale target; records preserve story state except record read markers')
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('접수대');await q.press('이곳으로 이동');await q.until('r13_hub')
   await q.press('할머니');await q.until('r13_resident_approach');await q.press('아내 편지를 받고 찾아왔습니다.');await q.until('r13_topics');await shot('09-mobile-direct-conversation');await q.press('돌아가기');await q.until('r13_hub')
   report['checks'].append('Direct tap on the default visible resident opens real conversation questions and returns to the field')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'))
   try:report['failure_state']=await q.state()
   except:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
asyncio.run(main())
