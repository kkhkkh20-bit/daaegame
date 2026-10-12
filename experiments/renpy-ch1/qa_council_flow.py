"""Actual browser UI route: weak hearing, adverse result, save and proof retry."""
import argparse,asyncio,hashlib,json,shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial
from qa_village import map_to
ROOT=Path(__file__).resolve().parent

async def present(t,key):
 await t.wait('council');await t.click(228,547);await t.wait('evidence')
 index=(await t.state())['inventory'].index(key)
 for _ in range(index//6):await t.click(286,576)
 slot=index%6
 await t.click(199+(slot%2)*230,240+(slot//2)*110)
 await t.wait('evidence',False)
 await t.advance_until('council' if key=='C01' else 'roam')

async def run(browser,out,w,h):
 out.mkdir(parents=True,exist_ok=True)
 context=await browser.new_context(viewport=dict(width=w,height=h),has_touch=w<1000,is_mobile=w<1000)
 page=await context.new_page();t=SourceTrial(page,w,h,out)
 await page.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/')
 await page.wait_for_function("typeof renpy_exec==='function'",timeout=60000)
 await t.state();await t.click(320,425);await t.advance_until('village_place')
 await t.arrival_action('map');await map_to(t,'post');await t.arrival_action('map')
 await map_to(t,'inn');await t.arrival_action('stay')
 await t.wait('roam');assert not (await t.state())['inventory']
 await t.click(964,635);await t.advance_until('council');await t.shot('empty-hearing')
 assert (await t.state())['council_result']=='open'
 # Listening advances public opinion; no guaranteed hero's turn is inserted.
 for expected in (1,2):
  await t.click(740,547);await t.wait('council',False);await t.advance_until('council')
  assert (await t.state())['council_claim']==expected
 await t.click(740,547);await t.wait('council',False);await t.advance_until('roam')
 state=await t.state();assert state['council_result']=='adverse' and 'adverse' in state['council_history']
 assert not state['found'] and 'C04' not in state['inventory']
 await t.shot('after-adverse');await t.save();await t.load();await t.wait('roam')
 assert (await t.state())['council_result']=='adverse'
 await t.click(964,635);await t.advance_until('council')
 assert (await t.state())['council_result']=='open' and 'resumed' in (await t.state())['council_history']
 await t.click(996,547);await t.wait('council',False);await t.advance_until('roam')
 await t.interact(900,280)
 await t.click(964,635);await t.advance_until('council')
 await present(t,'C01')
 state=await t.state();assert state['council_marks']==['sealed_money'] and state['council_result']=='open'
 await t.shot('partial-material-proof');await t.click(996,547);await t.wait('council',False);await t.advance_until('roam')
 await t.save();await t.load();await t.wait('roam')
 assert (await t.state())['council_marks']==['sealed_money']
 await t.move('dining');await t.question('T_se2',True);await t.question('C12',True)
 await t.click(964,635);await t.advance_until('council')
 assert 'sealed_money' in (await t.state())['council_marks']
 await present(t,'C12');state=await t.state()
 assert state['council_result']=='resolved' and {'sealed_money','uncorroborated_count'}<=set(state['council_marks'])
 assert not state['found'] and not state['complete']
 assert not t.errors,t.errors
 await t.shot('narrow-issue-resolved-before-discovery')
 result=dict(viewport=[w,h],checks=['empty_evidence_can_enter_hearing','three_listens_reach_adverse_result',
  'no_undiscovered_small_guest_injected','adverse_saved_and_resumed','manual_adjourn_returns_to_investigation',
  'one_material_proof_is_insufficient','material_progress_survives_adjourn_and_save',
  'independent_count_completes_narrow_issue','preview_does_not_announce_innocence_or_culprit','no_browser_errors'],
  final_council_result=state['council_result'],errors=t.errors)
 await context.close();return result

async def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',default='/tmp/daram-council-native');parser.add_argument('--touch',action='store_true');args=parser.parse_args()
 digest=hashlib.sha256((ROOT.parent.parent/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest()
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader-webgl','--autoplay-policy=no-user-gesture-required'])
  w,h=(844,390) if args.touch else (1280,720)
  route=await run(browser,Path(args.output),w,h)
  report=dict(native=True,read_only_state=True,injected_progress=False,game_zip_sha256=digest,route=route)
  (Path(args.output)/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
  print(json.dumps(report,ensure_ascii=False,indent=2));await browser.close()

if __name__=='__main__':asyncio.run(main())
