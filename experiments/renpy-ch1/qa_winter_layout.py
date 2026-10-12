"""Final layout-only check. Day-five fixture is explicitly not a gameplay test."""
import asyncio,shutil,json,hashlib
from pathlib import Path
from playwright.async_api import async_playwright
from qa_winter_web import WinterTrial,R
async def run(b,width,height):
 c=await b.new_context(viewport={'width':width,'height':height},has_touch=width<1000,is_mobile=width<1000)
 pg=await c.new_page();out=Path('/tmp/winter-qa/layout-'+str(width));out.mkdir(exist_ok=True)
 t=WinterTrial(pg,width,height,out)
 await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(300,423);await t.advance()
 await t.move('workshop');s=await t.state();assert s['people'][0][2]+s['people'][0][4]<=592;await t.shot('workshop-feet')
 await t.open_person('buri');await t.shot('workshop-questions');await t.close_topics()
 # Isolated scheduled-resident fixture; do not count this as reaching day five.
 await pg.evaluate('renpy_exec("import renpy; renpy.store.winter=dict(renpy.store.winter,day=5,period=1); result=True")')
 await t.move('post');s=await t.state();assert 'doto' in [r[0] for r in s['people']]
 assert all(row[2]+row[4]<=592 for row in s['people']);await t.shot('post-feet')
 await t.open_person('doto');await t.shot('post-questions');await t.close_topics()
 await t.move('square');s=await t.state();assert 'bami' in [r[0] for r in s['people']];await t.shot('square-hanging-bami')
 await t.open_person('bami');await t.shot('square-bami-questions');await t.close_topics()
 assert not t.errors and not t.bad and not t.failed
 await c.close();return {'viewport':[width,height],'layout_only':True,'injected_day_fixture':True,'feet_inside_play_area':True,'npc_clicks_open_questions':True,'errors':t.errors}
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  results=await asyncio.gather(run(b,1280,720),run(b,844,390));await b.close()
 report={'game_zip_sha256':hashlib.sha256((R.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest(),'layout_checks':results}
 (R/'WINTER_LAYOUT_QA_REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':asyncio.run(main())
