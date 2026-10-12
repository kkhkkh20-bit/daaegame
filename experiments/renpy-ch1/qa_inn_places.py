"""Actual inn entry, layered counter, local room navigation and lodging regression."""
import asyncio,json,hashlib,shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial
from qa_village import map_to
from qa_ui import check_topic_actor
ROOT=Path(__file__).resolve().parent
async def run(b,w,h):
 out=Path('/tmp/daram-inn-qa-final')/str(w);out.mkdir(parents=True,exist_ok=True)
 c=await b.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000);pg=await c.new_page();t=SourceTrial(pg,w,h,out)
 await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(320,425);await t.advance_until('village_place')
 await t.arrival_action('map');await map_to(t,'inn');before=await t.state();await t.click(960,638);await t.wait('village_inn');st=await t.state()
 assert st['inn_room']=='reception' and len(st['lines'])==len(before['lines']) and not st['post_closed']
 widgets=await pg.evaluate('renpy_exec("import renpy; result={k:renpy.exports.get_widget(\\\"arrival_interior\\\",k) is not None for k in (\\\"inn_host_activity\\\",\\\"inn_counter_foreground\\\")}")')
 assert all(widgets.values());await t.shot('reception-counter')
 await t.click(680,330);await t.wait('village_questions');await check_topic_actor(t,'arrival_questions');await t.shot('host-interview')
 await t.arrival_topic('room');assert not (await t.state())['roam']
 await t.click(640,295);await t.wait('village_inn')
 before=await t.state();await t.click(1050,350);await t.wait('inn_room','lounge');await t.wait('village_inn');st=await t.state()
 assert st['background']=='inn-lounge' and st['minutes']==before['minutes'] and st['music']=='assets/town-bright.mp3'
 assert set(st['interior_seen'])=={'inn:reception','inn:lounge'};await t.shot('lounge-sewing')
 await t.click(930,380);await t.advance_until('local_questions');await check_topic_actor(t,'village_contact_questions');await t.shot('guest-interview')
 await t.click(640,169);await t.wait('local_questions',False);await t.advance_until('local_questions');await t.click(640,295);await t.wait('village_inn')
 st=await t.state();assert 'resident_nubi' in st['greeted'] and 'resident_nubi' in st['locals_met'] and st['inn_room']=='lounge'
 await t.save();saved=await t.state();await t.click(125,640);await t.wait('inn_room','reception');await t.wait('village_inn');await t.load();await t.wait('village_inn');st=await t.state()
 assert st['inn_room']=='lounge' and st['interior_seen']==saved['interior_seen'] and st['minutes']==saved['minutes'] and st['locals_met']==saved['locals_met']
 await t.click(815,640);await t.wait('village_place');assert (await t.state())['village_location']=='inn'
 await t.click(180,642);await t.wait('nearby_picker')
 st=await t.state();index=next(i for i,e in enumerate(st['nearby_people']) if e['id']=='resident_nubi')
 await t.click(620,248+80*index);await t.advance_until('local_questions');assert (await t.state())['inn_room']=='lounge' and (await t.state())['background']=='inn-lounge'
 await t.click(640,295);await t.wait('village_inn');await t.click(815,640);await t.wait('village_place')
 await t.arrival_action('map');await t.shot('map-with-inn-rooms');await map_to(t,'post');assert (await t.state())['post_closed']
 await t.arrival_action('map');await map_to(t,'inn');await t.click(960,638);await t.wait('village_inn');assert (await t.state())['inn_room']=='reception'
 await t.click(680,330);await t.wait('village_questions');await t.arrival_topic('room');await t.wait('roam');assert (await t.state())['location']=='bed13';await t.shot('case-after-lodging')
 assert not t.errors and not t.failed and not t.bad,(t.errors,t.failed,t.bad)
 await c.close();return dict(viewport=[w,h],checks=['inn_entry_is_quiet','host_behind_counter_foreground','host_click_opens_separate_interview','lodging_requires_closed_post','public_rooms_connected_without_time_farming','dusk_lounge_and_correct_music','scheduled_sewing_guest_can_be_interviewed','guest_question_and_memory_return_to_same_room','save_load_restores_local_room_and_memory','return_to_town_and_map','nearby_list_routes_to_guests_actual_room','reentry_starts_at_reception','lodging_still_leads_to_existing_case','no_browser_native_or_asset_errors'],injected_progress=False)
async def main():
 sha=hashlib.sha256((ROOT.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest()
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);results=[]
  for w,h in [(1280,720),(844,390)]:
   results.append(await run(b,w,h));print(json.dumps(results[-1]),flush=True)
  await b.close()
 (ROOT/'INN_PLACES_QA_REPORT.json').write_text(json.dumps(dict(game_zip_sha256=sha,routes=results),ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
