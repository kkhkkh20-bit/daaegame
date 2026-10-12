"""Short native UI check of release cleanup and the two new full-body sprites."""
import asyncio,hashlib,json,shutil,argparse
from pathlib import Path
from playwright.async_api import async_playwright
from qa_resident_expansion import ResidentTrial,nearby,back
from qa_village import map_to
ROOT=Path(__file__).resolve().parent
async def main(out):
 out.mkdir(parents=True,exist_ok=True)
 sha=hashlib.sha256((ROOT.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest()
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  c=await b.new_context(viewport={'width':1280,'height':720});pg=await c.new_page();t=ResidentTrial(pg,1280,720,out)
  await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000)
  await t.state();await t.click(320,425)
  await t.advance_until('village_place')
  await nearby(t,'resident_teacher');await t.shot('teacher-fullbody');await back(t)
  await t.arrival_action('map');await map_to(t,'post');await nearby(t,'resident_librarian');await t.shot('librarian-fullbody');await back(t)
  metadata=await pg.evaluate('renpy_exec("import renpy; result=all(\\\"permission_note\\\" not in q.get(\\\"testimony\\\",{}) for p in renpy.store.VILLAGE_PEOPLE[\\\"profiles\\\"].values() for q in p[\\\"topics\\\"]) ")')
  assert metadata
  await t.arrival_action('map');await map_to(t,'inn')
  await t.arrival_action('stay')
  await t.click(964,635);await t.advance_until('council')
  caption=await pg.evaluate('renpy_exec("import renpy; result=renpy.store.clock_text")')
  assert caption.endswith(' · 논의'),caption
  assert not (await t.state())['found'];await t.shot('release-hearing-caption')
  assert not t.errors and not t.failed and not t.bad
  r={'game_zip_sha256':sha,'checks':['new_teacher_fullbody_and_question_face','new_librarian_fullbody_and_question_face','permission_provenance_has_no_false_granted_note','hearing_hud_uses_discussion_caption','no_undiscovered_guest','no_browser_errors_or_missing_files'],'errors':t.errors,'injected_progress':False,'normal_player_skip_used':False}
  (out/'report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False));await b.close()
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);asyncio.run(main(Path(parser.parse_args().output)))
