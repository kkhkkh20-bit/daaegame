"""Play the public schedule and observed-notebook UI without revealing hidden state."""
import argparse,asyncio,json,shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial
from qa_ui import check_resident_scroll

async def main(args):
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  c=await b.new_context(viewport={'width':1280,'height':720});pg=await c.new_page();t=SourceTrial(pg,1280,720,out)
  await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await pg.wait_for_timeout(650);await t.click(320,425)
  await t.advance_until('village_place');await t.arrival_action('talk');await t.arrival_action('map')
  saved=await t.state();assert any(o['person']=='neoul' for o in saved['observations'])
  assert not any(o['person']=='doto' for o in saved['observations'])
  await t.click(1038,45);await t.wait('evidence');await t.click(1005,145)
  assert await pg.evaluate('renpy_exec("import renpy; result=bool(renpy.exports.get_screen(\\\"village_timetable\\\"))")')
  await check_resident_scroll(t)
  await t.shot('observed-notebook');await t.click(1020,588);await t.click(374,576);await t.wait('evidence',False)
  await t.save();await t.load();await t.wait('village_map');state=await t.state();assert state['minutes']==saved['minutes'] and state['trust']==saved['trust'] and state['observations']==saved['observations']
  await t.arrival_move('gate')
  # Revisiting routes consumes travel time, not conversation points.
  while (await t.state())['minutes']<1110:
   await t.arrival_action('map');await t.arrival_move('fountain');await t.arrival_action('map');await t.arrival_move('gate')
  absent=await pg.evaluate('renpy_exec("import renpy; result=renpy.store.village_arrival_resident(\\\"gate\\\")")');assert absent is None
  state=await t.state();before=len(state['lines']);await t.click(825,365);state=await t.state();assert not state['village_questions'] and len(state['lines'])==before
  assert state['trust']==saved['trust'];await t.shot('gate-after-duty')
  assert not t.errors and not t.failed and not t.bad
  result=dict(observed_notebook_opens_and_closes=True,unmet_resident_not_revealed=True,memory_time_trust_saved=True,scheduled_resident_leaves=True,travel_cannot_farm_trust=True,errors=t.errors,failed_requests=t.failed,bad_responses=t.bad)
  (out/'report.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));await b.close()

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);asyncio.run(main(a.parse_args()))
