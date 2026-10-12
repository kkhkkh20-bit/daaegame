import asyncio,sys,shutil,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from qa_winter_web import WinterTrial
from playwright.async_api import async_playwright
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  pg=await b.new_page(viewport={'width':1280,'height':720});out=Path('/tmp/winter-qa/topic-save');out.mkdir(exist_ok=True)
  t=WinterTrial(pg,1280,720,out)
  await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(300,423);await t.advance()
  await t.click(820,660);await pg.wait_for_timeout(300);st=await t.state();assert not st['confirm'],'Cannot sleep without getting a room';await t.advance()
  await t.open_person('granny');before=await t.state()
  await t.click(1125,43);await t.wait('saving');await t.click(760,245);await t.click(265,590);await t.wait('topics')
  await t.close_topics();await t.move('gate');await t.open_person('guard');await t.shot('guard-questions');await t.close_topics()
  await t.click(1212,43);await t.wait('menu');await t.click(780,243);await t.wait('loading');await t.click(760,245);await t.wait('topics')
  after=await t.state();assert after['state']==before['state'] and after['target_id']=='granny' and after['actor']=='granny'
  await t.shot('restored-questions');await t.close_topics()
  assert not t.errors and not t.bad and not t.failed
  report={'registration_required_for_sleep':True,'guard_click_dialogue':True,'save_from_questions_restores_actor_place_state':True,'runtime_errors':t.errors,'injected_progress':False}
  (out/'result.json').write_text(json.dumps(report));print(json.dumps(report));await b.close()
asyncio.run(main())
