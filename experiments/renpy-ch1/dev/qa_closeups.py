"""0.18.22: click-to-open close-ups load their (progressively downloaded) backgrounds in the web build."""
import asyncio,json,os,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'closeups';OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
JUMP='w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=[s.Function(renpy.exports.call_in_new_context,"%s"),s.Jump("r13_field")];w.clicked=w.action;result=True'
async def main():
 report={'archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720});pg=await c.new_page();q=UIQA(pg,OUT)
  errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   for name,state,shot in (("r13_life_door",'day=2,period=0,location="inn"','01-door'),("r13_gm_scale",'day=3,period=0,location="store"','02-scale')):
    await q.py('import renpy;s=renpy.store;s.r13_edit(%s);s.r13_flag("entry_corrected","lodging","livelihood_open");s.r13_upgrade();'%state+JUMP%name);await q.input(1220,50);await asyncio.sleep(8);await q.shot(shot)
    await q.press('돌아간다');await q.wait('r13_hub')
   report['checks'].append('door and scale close-ups open from the web build and return to the field');report['errors']=errors
   report['status']='passed-pending-visual-review' if not errors else 'errors'
  except Exception as e:
   report['status']='failed';report['error']=repr(e);await q.shot('99-failure')
  finally:
   await b.close()
 (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=1));print(json.dumps(report,ensure_ascii=False))
asyncio.run(main())
