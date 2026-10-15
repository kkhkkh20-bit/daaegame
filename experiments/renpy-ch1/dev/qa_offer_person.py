# Browser check (0.18.53): an event is pressed on the person doing it.
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'offer-person';OUT.mkdir(parents=True,exist_ok=True)
async def main():
 report={'checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=UIQA(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   # Walk there the ordinary way so arrival raises the offer.
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="square",life_poc=True);s.r13_flag("entry_corrected","lodging","livelihood_open","ev_g_done","ev_i_done","ev_a_done","ep1_patrol_seen");s.r13_upgrade();result=True')
   # The opening hub is the gate entry; leave it for the ordinary field loop.
   await q.py('import renpy;s=renpy.store\ndef f(**kw):renpy.ui.timer(0.2,action=[renpy.store.Hide("qa_jump"),renpy.store.Jump("r13_field")])\nrenpy.display.screen.define_screen("qa_jump",f,zorder="200")\nrenpy.exports.show_screen("qa_jump");result=True')
   await asyncio.sleep(3);await q.wait('r13_hub');await q.shot('00-square');await q.press('지도 · 이동');await q.wait('r13_map');await q.press('우체국');await q.press('이곳으로 이동');await q.advance();await q.wait('r13_hub')
   await asyncio.sleep(2);await q.shot('01-sling-marked')
   room=await q.room();assert 'r13_w1c_letters' in room.get('offers',{}),room.get('offers')
   st=await q.state();texts=[b['text'] for b in st['buttons']]
   assert not any('김에 쐬고' in t for t in texts),texts
   await q.press('슬링');await q.advance();await q.wait('choice');await q.shot('02-sling-event')
   room=await q.room();assert 'ev_l_done' in room['flags'],room['flags']
   report['checks'].append('post: no text marker, Sling nameplate starts the letters event')
   report['status']='passed'
  except Exception as e:
   report['status']='failed';report['error']=repr(e)[:600]
  await b.close()
 print(json.dumps(report,ensure_ascii=False))
asyncio.run(main())
