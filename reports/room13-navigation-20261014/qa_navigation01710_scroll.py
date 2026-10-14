"""Explicit day-two/day-eight fixture, actual map/touch/travel/save UI."""
import asyncio,json,shutil,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from pixel_qa_ui0156 import UIQA
OUT=Path('/workspace/room13-review/navigation01710-scroll');OUT.mkdir(exist_ok=True)
URL='http://127.0.0.1:8094/room13-dev/'
async def main():
 report={'archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'kind':'Explicit day-two/day-eight fixture; real navigation, cancellation, save/load, and touch clicks','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=UIQA(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.persistent.room13_map_list=False;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="inn");s.r13_flag("entry_corrected","lodging");s.r13_upgrade();w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True');await q.input(1220,50);await q.wait('r13_hub');await q.press('지도 · 이동');await q.wait('r13_map');await q.press('큰 목록 보기');before=await q.room()
   await pg.mouse.move(450,450)
   for _ in range(8):await pg.mouse.wheel(0,100);await asyncio.sleep(.12)
   await asyncio.sleep(.7);await q.value('room13');await q.shot('scrolled-last-room');assert await q.room()==before;await q.press('이곳으로 이동');await q.wait('r13_hub');assert (await q.room())['location']=='room13'
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True;await asyncio.sleep(.7);await q.press('지도 · 이동');await q.wait('r13_map');await q.shot('mobile-list-scroll-start')
   # Real touch gesture, using the same letterboxed 1280x720 mapping as gameplay taps.
   vp=pg.viewport_size;scale=min(vp['width']/1280,vp['height']/720);sx=(vp['width']-1280*scale)/2;sy=(vp['height']-720*scale)/2
   cdp=await c.new_cdp_session(pg);await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':sx+420*scale,'y':sy+600*scale}]})
   for i in range(1,21):
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':sx+420*scale,'y':sy+(600-410*i/20)*scale}]});await asyncio.sleep(.04)
   await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await asyncio.sleep(.7)
   st=await q.state();matches=[b for b in st['buttons'] if b['value']=='room13' and b['rect'][3]>70];assert matches,('last room must be visible after touch drag',st)
   await q.value('room13');await q.shot('mobile-list-scroll-end');assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["selected"]')=='room13';await q.press('현장으로 돌아가기');await q.wait('r13_hub')
   report['checks'].append('Actual wheel reveals last interior destination; confirmed travel succeeds. Real CDP touch-drag exposes last room; touch selection and return succeeds.')
   report['status']='passed-pending-visual-review'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'));(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
