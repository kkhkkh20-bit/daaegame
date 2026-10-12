"""Native village life pass: click activity sprites, first greetings, map, persistence."""
import asyncio,json,hashlib,shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial
from qa_village import map_to
from qa_ui import check_topic_actor
ROOT=Path(__file__).resolve().parent
async def meet(t,person):
 before=await t.state();entry=next(e for e in before['outdoor_people'] if e['id']==person)
 assert entry['activity_pose'] and entry['activity']
 await t.click(entry['x']+entry['width']/2,entry['y']+entry['height']/2)
 await t.advance_until('local_questions');await check_topic_actor(t,'village_contact_questions')
 st=await t.state();assert person in st['greeted'] and st['minutes']==before['minutes'] and st['locals_trust']==before['locals_trust']
 assert len([l for l in st['lines'] if l['id'].startswith('V_GREETING_'+person)])==2
 await t.shot(person+'-questions');await t.click(640,295);await t.wait('village_place')
 entry=next(e for e in (await t.state())['outdoor_people'] if e['id']==person)
 await t.click(entry['x']+entry['width']/2,entry['y']+entry['height']/2);await t.wait('local_questions')
 assert len([l for l in (await t.state())['lines'] if l['id'].startswith('V_GREETING_'+person)])==2
 await t.click(640,295);await t.wait('village_place')
async def run(browser,w,h):
 out=Path('/tmp/daram-life-qa')/str(w);out.mkdir(parents=True,exist_ok=True)
 c=await browser.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000);pg=await c.new_page();t=SourceTrial(pg,w,h,out)
 await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(320,425);await t.advance_until('village_place')
 await t.shot('gate-life');await meet(t,'resident_tori')
 await t.arrival_action('map');await t.shot('map');await map_to(t,'fountain');await t.shot('square-life')
 await meet(t,'resident_piko');await meet(t,'resident_momo')
 before=await t.state();await t.click(450,642);await t.wait('village_place',False);await t.advance_until('village_place');after=await t.state()
 assert after['minutes']==before['minutes'] and after['inventory']==before['inventory'] and not after['stone']
 await t.arrival_action('map');await map_to(t,'post');await t.shot('post-life');await meet(t,'resident_tok')
 await t.click(180,642);await t.wait('nearby_picker');await t.shot('resident-activities');await t.click(1000,590);await t.wait('village_place')
 await t.arrival_action('map');await map_to(t,'lane');await t.shot('lane');await t.arrival_action('map');await map_to(t,'inn');await t.shot('inn')
 before=await t.state();await t.save();await t.arrival_action('map');await map_to(t,'gate');await t.load();await t.wait('village_place');after=await t.state()
 assert after['greeted']==before['greeted'] and after['minutes']==before['minutes'] and after['village_location']=='inn'
 data=await pg.evaluate('renpy_exec("import renpy; result=dict(profiles=all(p.get(\\\"personality\\\") and p.get(\\\"activity\\\") and len(p.get(\\\"greeting\\\",[]))==2 for p in renpy.store.VILLAGE_PEOPLE[\\\"profiles\\\"].values()),count=len(renpy.store.VILLAGE_PEOPLE[\\\"profiles\\\"]),poses=all(renpy.store.CAST[k][\\\"activity\\\"]!=renpy.store.CAST[k][\\\"interview_neutral\\\"] for k in renpy.store.VILLAGE_ACTIVITY_ACTORS))")')
 assert data==dict(profiles=True,count=31,poses=True),data
 assert not t.errors and not t.failed and not t.bad,(t.errors,t.failed,t.bad)
 await c.close();return dict(viewport=[w,h],checks=['four_activity_actors_clickable','activity_and_interview_art_distinct','first_greeting_once_per_person','no_greeting_time_or_trust_farming','map_all_five_destinations','observation_does_not_grant_evidence','resident_activity_list_closes','greetings_time_location_save_load','31_personality_activity_greetings','no_native_browser_asset_errors'],injected_progress=False)
async def main():
 sha=hashlib.sha256((ROOT.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest()
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);results=[]
  for w,h in [(1280,720),(844,390)]:
   results.append(await run(b,w,h));print(json.dumps(results[-1]),flush=True)
  await b.close()
 (ROOT/'VILLAGE_LIFE_QA_REPORT.json').write_text(json.dumps(dict(game_zip_sha256=sha,routes=results),ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
