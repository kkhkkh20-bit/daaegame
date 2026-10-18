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
 report={'checks':[]}
 async with async_playwright() as p:
  OUT.mkdir(parents=True,exist_ok=True)
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/')
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="inn",evidence=["E01"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.persistent.r13_pan_hint_seen=True;s.r13_world_cameras={};s.r13_field_location=None;s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub');await q.shot('01-pc-field')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True;await asyncio.sleep(.5)
   report['touch_geometry']=await q.py('import renpy;s=renpy.store;result={"physical":renpy.exports.get_physical_size(),"touch":s.r13_touch_ui(),"height":s.r13_control_height(),"large_text":s.persistent.room13_large_text}')
   assert report['touch_geometry']['touch'] and report['touch_geometry']['height']==80 and not report['touch_geometry']['large_text'],report
   await q.shot('02-mobile-field')
   before=await q.room();await q.press('지도');await q.wait('r13_map');await q.shot('03-mobile-map')
   st=await q.state();foot=[v for v in st['buttons'] if v['text'].strip() in ('이곳으로 이동','현장으로')]
   # Disabled current-place confirm is omitted from the enabled-button probe.
   assert any(v['text'].strip()=='현장으로' and v['rect'][2:]==[232,80] for v in foot),foot
   await q.press('식당');assert await q.room()==before;await q.shot('04-mobile-map-selected')
   st=await q.state();foot=[v for v in st['buttons'] if v['text'].strip() in ('이곳으로 이동','현장으로')];assert len(foot)==2 and all(v['rect'][2:]==[232,80] for v in foot),foot
   await q.press('마을');rect=await q.py('import renpy;result=renpy.store.r13_cart_name_rect("workshop")');x,y,w,h=rect;await q.input(x+w/2,y+h/2);await q.shot('05-mobile-village-map');assert await q.room()==before
   await q.press('현장으로');await q.wait('r13_hub');await q.press('기록');await asyncio.sleep(.4);await q.shot('06-mobile-records-folded')
   filters=[v for v in (await q.state())['buttons'] if 280<=v['rect'][0]<800 and 90<=v['rect'][1]<190]
   assert all(v['rect'][2]>=80 and v['rect'][3]>=80 for v in filters),filters
   assert len(filters)==2,filters
   await q.press('초대 편지');await q.press('출처');await q.shot('07-mobile-records-origin-open');await q.press('출처 접기');await q.press('닫기');await q.wait('r13_hub')
   await q.press('주변 살피기');await asyncio.sleep(3.3);assert await q.py('import renpy;result="inn" in renpy.store.r13_scene_hint_seen');await q.shot('08-mobile-investigation-clean')
   before=await q.room()
   # Select clear upper wall: pure background, away from HUD and authored props.
   await page.touchscreen.tap((844-1280*(390/720))/2+600*(390/720),100*(390/720))
   feedback=await q.py('import renpy;result=renpy.exports.get_screen("r13_empty_tap") is not None')
   assert feedback,'Empty tap feedback did not appear'
   await asyncio.sleep(.6);assert await q.room()==before;assert 'r13_hub' in (await q.state())['screens']
   # Dense current-run inventory fixture: page geometry must remain separate from filters.
   await q.py('import renpy;s=renpy.store;s.r13_edit(evidence=list(s.ROOM13["evidence"]));s.r13_records_view={};result=True')
   await q.press('기록');await asyncio.sleep(.4);await q.shot('09-mobile-dense-records')
   st=await q.state();filters=[v for v in st['buttons'] if 280<=v['rect'][0]<800 and 90<=v['rect'][1]<190]
   assert all(v['rect'][0]+v['rect'][2]<=800 and v['rect'][1]+v['rect'][3]<=190 for v in filters),filters
   await q.press('다음');await q.shot('10-mobile-records-page2');await q.press('닫기');await q.wait('r13_hub')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;s=renpy.store;s.config.variants=[v for v in s.config.variants if v!="touch"];renpy.exports.restart_interaction();result=True')
   assert await q.py('import renpy;result=renpy.store.r13_control_height()')==64
   await q.shot('11-pc-mouse-field')
   report['checks']=['Mobile controls grow independently of large text','Map select/cancel preserve exact story state; confirm/back share 232x80 geometry','Sparse owned collection shows two relevant filters with 80px touch targets','Record source opens and folds through real controls','Scene hint folds; empty tap gives feedback without story, evidence or clock changes']
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'))
   try:report['failure_state']=await q.state()
   except:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='failure_state'},ensure_ascii=False),flush=True);await b.close()
asyncio.run(main())
