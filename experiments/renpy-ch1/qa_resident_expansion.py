"""Read-only native routes for optional historical residents and public testimony."""
import argparse,asyncio,hashlib,json,shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial
from qa_village import map_to
from qa_ui import check_topic_actor
ROOT=Path(__file__).resolve().parent
PEOPLE=json.loads((ROOT/'game/village-residents.json').read_text())
ROSTER=json.loads((ROOT/'game/legacy-resident-roster.json').read_text())
class ResidentTrial(SourceTrial):
 async def state(self):
  st=await super().state()
  extra=await self.page.evaluate('renpy_exec("import renpy; result=dict(nearby=bool(renpy.exports.get_screen(\\\"village_nearby_residents\\\")),optional=renpy.store.village_optional_people(renpy.store.arrival_location),testimonies=dict(renpy.store.village_testimonies),local_memories=dict(renpy.store.village_people_memories))")')
  return dict(st,**extra)
async def nearby(t,person):
 await t.wait('village_place');before=await t.state();index=next(i for i,p in enumerate(before['optional']) if p['id']==person)
 await t.click(180,642);await t.wait('nearby');await t.shot('nearby-'+person)
 assert index<4,'Fixture should use an initially visible row'
 await t.click(620,248+80*index);await t.wait('local_questions');await check_topic_actor(t,'village_contact_questions')
 assert (await t.state())['minutes']==before['minutes'],'Opening list must not advance time'
async def topic(t,person,index,permission):
 before=await t.state();await t.click(640,169+63*index);await t.wait('local_questions',False)
 await t.advance_until('choice');await t.shot('permission-'+person)
 await t.click(600,180 if permission else 240);await t.wait('choice',False);await t.advance_until('local_questions')
 st=await t.state();spec=PEOPLE['profiles'][person]['topics'][index]['testimony'];record=st['testimonies'][spec['id']]
 assert record['speaker']==person and record['permission']==permission and not record['verified']
 assert record['heard_place'] and record['heard_minute']<=before['minutes']
 assert person in st['locals_met'];await t.shot('questions-'+person);return st
async def back(t):
 await t.click(640,295);await t.wait('village_place')
async def run(browser,out,w,h):
 loaded_sha=hashlib.sha256((ROOT.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest()
 out.mkdir(parents=True,exist_ok=True);c=await browser.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000)
 page=await c.new_page();t=ResidentTrial(page,w,h,out);await page.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/')
 await page.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(320,425);await t.advance_until('village_place')
 # Knowledge, support and permissions start empty. All new identities are optional.
 state=await t.state();assert not state['testimonies'] and not state['locals_met']
 assert len(ROSTER['entries'])==35 and len([e for e in ROSTER['entries'] if e['integration']=='optional_concept'])==28
 await nearby(t,'resident_tori');first=await topic(t,'resident_tori',1,False)
 repeated=await topic(t,'resident_tori',1,False)
 assert repeated['minutes']==first['minutes'] and repeated['locals_trust']==first['locals_trust']
 original_minute=repeated['testimonies']['T_V_TORI']['heard_minute']
 permitted=await topic(t,'resident_tori',1,True)
 assert permitted['minutes']==first['minutes'] and permitted['testimonies']['T_V_TORI']['heard_minute']==original_minute
 await back(t);await t.arrival_action('map');await map_to(t,'inn')
 await nearby(t,'resident_nubi');await topic(t,'resident_nubi',1,True);await back(t)
 await t.arrival_action('map');await map_to(t,'post')
 await nearby(t,'resident_tok');await topic(t,'resident_tok',1,True);await back(t)
 await t.arrival_action('map');saved=await t.state();await t.save();await t.load();await t.wait('village_map');loaded=await t.state()
 for key in ('testimonies','local_memories','locals_seen','locals_met','minutes'):assert saved[key]==loaded[key],key
 # Global availability is checked without changing the native story clock.
 global_data=await page.evaluate('renpy_exec("import renpy; result=dict(ids=list(renpy.store.VILLAGE_PEOPLE[\\\"profiles\\\"]),routes=list(renpy.store.VILLAGE_PEOPLE[\\\"routines\\\"]),cast=list(renpy.store.CAST))")')
 wanted={e['runtime_id'] for e in ROSTER['entries'] if e['integration']=='optional_concept'}
 assert wanted<=set(global_data['cast']) and wanted<=set(global_data['ids'])
 for person in wanted:
  routes=[r for r in global_data['routes'] if r['id']==person]
  assert len(routes)==2 and routes[0]['start']==1050 and routes[-1]['end']==1261 and routes[0]['end']==routes[1]['start']
  assert len(PEOPLE['profiles'][person]['topics'])==2
 assert not t.errors and not t.failed and not t.bad
 checks=['original_35_preserved_without_overwriting_approved_seven','28_runtime_actors_have_images_and_56_optional_topics','five_places_have_contiguous_time_based_routes','list_and_question_opening_do_not_advance_time','three_context_records_have_source_place_time_and_verification_state','private_record_needs_explicit_permission_before_public_use','asking_later_can_grant_permission_without_reward_farming','repeated_topics_preserve_original_heard_time','testimony_permissions_relationship_memories_and_met_faces_survive_save_load']
 result=dict(viewport=[w,h],loaded_game_zip_sha256=loaded_sha,checks=checks,minutes=loaded['minutes'],testimonies=loaded['testimonies'],errors=t.errors,failed_requests=t.failed,bad_responses=t.bad)
 await c.close();return result
async def main(args):
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);runs=[]
  for w,h in ([(1280,720)] if args.desktop_only else [(1280,720),(844,390)]):
   r=await run(b,out/f'{w}x{h}',w,h);runs.append(r);print(json.dumps(dict(viewport=r['viewport'],checks=r['checks']),ensure_ascii=False),flush=True)
  await b.close()
 report=dict(game_zip_sha256=hashlib.sha256((ROOT.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest(),runs=runs)
 (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--desktop-only',action='store_true');asyncio.run(main(p.parse_args()))
