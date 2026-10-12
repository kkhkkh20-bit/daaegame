"""Native village map, future residents, knowledge and schedule regression route."""
import argparse,asyncio,json,shutil,hashlib
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial
from qa_ui import check_topic_actor,check_resident_scroll
ROOT=Path(__file__).resolve().parent
PEOPLE=json.loads((ROOT/'game/village-residents.json').read_text())

async def map_to(t,place):
 await t.wait('village_map')
 point={'gate':(165,415),'fountain':(440,275),'post':(750,195),'lane':(690,435),'inn':(1000,310)}[place]
 await t.click(*point);await t.wait('village_map',False);await t.advance_until('village_place')
 assert (await t.state())['village_location']==place

async def topic(t,person,key,opened=False):
 t.contact_test_person=person
 if not opened:
  state=await t.state();resident=next(r for r in state['outdoor_people'] if r['id']==person)
  await t.shot('world-'+person)
  await t.click(resident['x']+resident['width']/2,resident['y']+resident['height']/2)
  await t.advance_until('local_questions')
  await check_topic_actor(t,'village_contact_questions');await t.shot('questions-'+person)
 state=await t.state()
 available=[q for q in PEOPLE['profiles'][person]['topics'] if q.get('requires')!='stone' or state['stone']]
 index=next(i for i,q in enumerate(available) if q['id']==key)
 await t.click(640,169+63*index);await t.wait('local_questions',False)
 captured=False
 for _ in range(240):
  state=await t.state()
  if state['local_questions'] or state['village_place']:break
  if state['lines'] and state['lines'][-1]['w']==person and not captured:
   await t.shot('dialogue-'+person);captured=True
  await t.click(830,665)
 else:raise AssertionError('Encounter did not finish')
 await t.page.wait_for_timeout(600)
 state=await t.state();assert key in state['locals_seen'] and person in state['locals_met']
 return state

async def back(t):
 state=await t.state()
 if state['local_questions']:
  person=t.contact_test_person
  n=sum(q.get('requires')!='stone' or state['stone'] for q in PEOPLE['profiles'][person]['topics'])
  await t.click(640,169+63*n);await t.wait('local_questions',False);await t.wait('village_place')

async def run(browser,out,w,h):
 out.mkdir(parents=True,exist_ok=True)
 c=await browser.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000)
 pg=await c.new_page();t=SourceTrial(pg,w,h,out)
 await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000)
 await t.state();await t.click(320,425);await t.advance_until('village_place')
 state=await t.state();assert state['village_location']=='gate' and 'elder' in [p['id'] for p in state['outdoor_people']]
 await topic(t,'elder','elder_evening');before=await topic(t,'elder','elder_inn',opened=True)
 after=await topic(t,'elder','elder_inn',opened=True)
 assert after['minutes']==before['minutes'] and after['locals_trust']==before['locals_trust'];await back(t)
 await t.arrival_action('map');await t.shot('village-map');await map_to(t,'lane')
 await topic(t,'bodum','bodum_intro');await topic(t,'bodum','bodum_basket',opened=True);await topic(t,'bodum','bodum_night',opened=True);await back(t)
 await t.arrival_action('map');await map_to(t,'post')
 assert (await t.state())['post_closed'];await t.shot('post-with-resident')
 await topic(t,'workshop','workshop_lantern');await topic(t,'workshop','workshop_post',opened=True);await back(t)
 await t.arrival_action('map');saved=await t.state();await t.shot('known-residents-map');await t.save();await t.load();await t.wait('village_map')
 loaded=await t.state()
 for key in ('locals_met','locals_seen','locals_trust','locals_revisions','village_places_seen','minutes'):assert loaded[key]==saved[key],key
 await map_to(t,'fountain')
 before=await t.state();after=await topic(t,'elder','elder_inn')
 assert after['locals_revisions']['elder_inn']=='post_closed'
 assert after['locals_trust']==before['locals_trust'] and after['minutes']==before['minutes']
 await back(t);await t.arrival_action('stone');assert (await t.state())['stone']
 await topic(t,'elder','elder_lights');await back(t)
 await t.click(1038,45);await t.wait('evidence');await t.click(1005,145);await check_resident_scroll(t);await t.shot('resident-notebook')
 await t.click(1020,588);await t.click(374,576);await t.wait('evidence',False)
 # Travel through real UI until the workshop owner relocates from the post office.
 while (await t.state())['minutes']<1120:
  await t.arrival_action('map');await map_to(t,'gate');await t.arrival_action('map');await map_to(t,'fountain')
 state=await t.state();assert 'workshop' in [p['id'] for p in state['outdoor_people']]
 await t.shot('changed-residents');await topic(t,'workshop','workshop_stone');await back(t)
 trust=(await t.state())['locals_trust']
 await t.arrival_action('map');await map_to(t,'post');state=await t.state()
 assert 'workshop' not in [p['id'] for p in state['outdoor_people']]
 assert state['locals_trust']==trust and {'gate','lane','post','fountain'}<=set(state['village_places_seen'])
 assert not t.errors and not t.failed and not t.bad
 result=dict(viewport=[w,h],checks=['actual_buildings_are_map_hotspots','map_and_street_have_state_based_residents','three_future_cast_encounters_are_optional','world_and_interview_are_separate_complete_poses','question_faces_visible','repeat_topic_cannot_farm_time_or_familiarity','new_post_knowledge_revises_old_answers_without_reward_farming','stone_question_requires_prior_observation','future_cast_and_visited_places_survive_save_load','resident_notebook_scrolls_with_extended_cast','resident_relocates_by_absolute_time','closed_post_keeps_player_on_street'],final=state,errors=t.errors,failed_requests=t.failed,bad_responses=t.bad)
 await c.close();return result

async def main(args):
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  runs=[]
  for w,h in ([(844,390)] if args.mobile_only else [(1280,720),(844,390)]):
   result=await run(b,out/f'{w}x{h}',w,h);runs.append(result);print(json.dumps({k:v for k,v in result.items() if k!='final'},ensure_ascii=False),flush=True)
  await b.close()
 report=dict(game_zip_sha256=hashlib.sha256((ROOT.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest(),runs=runs)
 (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mobile-only',action='store_true');asyncio.run(main(p.parse_args()))
