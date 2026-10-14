"""Web build: episode 4 (Tok accused), town events bundle 1 (thief chase → give herbs to Musoe; overnight lock)."""
import asyncio,json,os,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'town-events';OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
ENTER=('w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_roam");w.clicked=w.action;result=True')
async def main():
 report={'archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=UIQA(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=3,period=0,location="workshop",life_poc=True);s.r13_flag("entry_corrected","lodging","livelihood_open",*["evening_brief:%d"%d for d in range(1,14)]);s.r13_upgrade();'+ENTER)
   await q.input(1220,50);await q.advance();await q.wait('choice');await q.shot('00-tok-accused')
   await q.press('톡에게 등의 돌 조각이 무엇인지 묻는다');await q.advance();await q.wait('choice')
   await q.press('톡의 편을 든다');await q.advance();await q.wait('r13_hub')
   room=await q.room();assert 'W5' in room['evidence'] and 'ep4_open' in room['flags'] and 'tok_detained' not in room['flags'],room
   report['checks'].append('Episode 4: Tok accused at workshop → ask about sliver (W5) → defend Tok')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=3,period=1,location="store",life_poc=True);s.r13_flag("entry_corrected","lodging","livelihood_open",*["evening_brief:%d"%d for d in range(1,14)]);s.r13_upgrade();'+ENTER)
   await q.input(1220,50);await q.advance();await q.wait('choice');await q.shot('01-store-theft')
   await q.press('수리점 쪽 골목으로 돌아가 앞질러 간다');await q.advance();await q.wait('choice');await q.shot('02-caught')
   await q.press('무쇠 할아버지에게 직접 가져다준다');await q.advance();await q.wait('r13_hub')
   room=await q.room();assert 'H5' in room['evidence'] and 'musoe_recovering' in room['flags'],room
   report['checks'].append('Day 3 store theft → alley chase → herbs to Musoe: mine map H5, recovery flag')
   await q.py('import renpy;s=renpy.store;s.r13_edit(period=2,location="inn");'+ENTER)
   await q.input(1220,50);await q.advance();await q.wait('choice');await q.shot('03-madam-offer')
   await q.press('받아들인다');await q.advance();await q.wait('r13_hub');await q.shot('04-after-lock')
   room=await q.room();assert (room['day'],room['period'])==(4,1) and 'room_searched' in room['flags'],room
   report['checks'].append('Day 3 evening job accepted → locked overnight: day 4 afternoon, room searched')
   report['status']='passed'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
