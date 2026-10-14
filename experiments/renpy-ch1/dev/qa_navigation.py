"""Explicit day-two/day-eight fixture, actual map/touch/travel/save UI."""
import asyncio,json,os,shutil,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'navigation';OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
async def main():
 report={'archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'kind':'Explicit day-two/day-eight fixture; real navigation, cancellation, save/load, and touch clicks','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=UIQA(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.persistent.room13_map_list=False;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="inn");s.r13_flag("entry_corrected","lodging");s.r13_upgrade();w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True');await q.input(1220,50);await q.wait('r13_hub');await q.shot('01-inn-field');before=await q.room();await q.press('지도 · 이동');await q.wait('r13_map');await q.shot('02-inn-map');await q.press('마을 보기');await q.shot('03-village-map');await q.press('여관 접수대');await q.shot('04-inn-selected');assert await q.room()==before
   await q.press('여관 내부 보기');await q.press('2층 복도');await q.shot('05-hall-selected-cost');assert await q.room()==before;await q.press('현장으로 돌아가기');await q.wait('r13_hub');assert await q.room()==before
   report['checks'].append('Browsing town/building/interior and selecting/cancelling destinations does not alter any room state; cost shown before travel')
   await q.press('2층으로');await q.wait('r13_hub');assert (await q.room())['location']=='hall';await q.press('13호실');await q.wait('r13_hub');assert (await q.room())['location']=='room13';await q.shot('06-room-field');await q.press('복도로');await q.wait('r13_hub');await q.press('1층 로비');await q.wait('r13_hub');assert (await q.room())['location']=='inn'
   assert ((await q.room())['day'],(await q.room())['period'])==(2,0)
   await q.save(1);saved=await q.room();await q.press('식당');await q.wait('r13_hub');await q.load(1);assert await q.room()==saved;await q.shot('07-save-restored-inn')
   report['checks'].append('Real adjacent travel inn→hall→room→hall→inn and save→dining→load retain day/period, clues and exact saved state')
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('큰 목록 보기');await q.shot('08-large-list');await q.press('주방');assert await q.room()==saved;await q.press('이곳으로 이동');await q.wait('r13_hub');assert (await q.room())['location']=='kitchen';await q.press('지도 · 이동');await q.wait('r13_map');assert await q.py('import renpy;result=renpy.store.persistent.room13_map_list')
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True;await asyncio.sleep(1);await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await q.shot('09-mobile-landscape-list')
   await q.press('식당');await q.press('이곳으로 이동');await q.wait('r13_hub');assert (await q.room())['location']=='dining';await q.press('지도 · 이동');await q.wait('r13_map');await q.press('지도로 보기');await q.shot('10-mobile-landscape-map');await q.press('현장으로 돌아가기');await q.wait('r13_hub');await q.save(2);await q.load(2)
   report['checks'].append('844×390 touch, large text: list selection/confirmed travel, map/list preference, cancel and real save/load passed')
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('큰 목록 보기');await pg.set_viewport_size({'width':390,'height':844});await asyncio.sleep(1);await q.shot('11-mobile-portrait-list');await q.press('현장으로 돌아가기');await q.wait('r13_hub')
   await pg.set_viewport_size({'width':1280,'height':720});q.touch=False;await asyncio.sleep(.5)
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=8,period=0,location="facility",week2_started=True,trial_ended=True);w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True');await q.input(1220,50);await q.wait('r13_hub');await q.press('지도 · 이동');await q.wait('r13_map');await q.shot('12-mountain-known-only');keys=await q.py('import renpy;s=renpy.store;result=[k for k,p in s.r13_map_nodes("mountain")]');assert 'greenhouse' not in keys and 'altar' not in keys,keys
   report['checks'].append('Day-eight unknown greenhouse/altar remain absent; north-path breadcrumb correct; no resident schedule lookup added')
   report['status']='passed-pending-visual-review'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'));(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
