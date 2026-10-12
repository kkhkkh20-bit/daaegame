"""First-scene pilot: actual inputs, read-only state, PC and touch save restoration."""
import asyncio,json,hashlib,shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_source import SourceTrial
from qa_village import map_to
ROOT=Path(__file__).resolve().parent
async def presentation(t):
 return await t.page.evaluate('renpy_exec("import renpy; result=dict(speaker=renpy.store.dialogue_speaker,expression=renpy.store.dialogue_expression,execution=renpy.store.scene_execution,portrait=renpy.exports.get_widget(\\\"say\\\",\\\"dialogue_portrait\\\") is not None,log=list(renpy.store.scene_execution_log))")')
async def run(b,w,h):
 out=Path('/tmp/daram-scene-qa')/str(w);out.mkdir(parents=True,exist_ok=True)
 c=await b.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000)
 pg=await c.new_page();t=SourceTrial(pg,w,h,out)
 await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000)
 await t.state();await t.click(320,425)
 await t.advance_until('line','V_CARRIAGE:0')
 before=await t.state();p=await presentation(t)
 assert p['speaker']=='daram' and p['portrait'] and before['camera']=='carriage' and before['music'] and not before['pulse']
 await t.shot('carriage-portrait');await t.save()
 await t.advance_until('line','V_CARRIAGE:1');assert (await presentation(t))['speaker']=='dad'
 await t.shot('dad-portrait');await t.load()
 await t.wait("line",before["line"])
 restored=await t.state();print('RESTORE',[(k,before.get(k),restored.get(k)) for k in ('line','camera','music')],flush=True);assert restored['line']==before['line'] and restored['camera']==before['camera'] and restored['music']==before['music']
 assert (await presentation(t))['speaker']=='daram'
 await t.advance_until('village_place');st=await t.state();p=await presentation(t)
 assert st['village_location']=='gate' and st['music']=='assets/town-bright.mp3' and not st['pulse'] and not st['typing']
 assert not any(x['id'].startswith('COLD_') for x in st['lines'])
 assert p['speaker'] is None and [x['camera'] for x in p['log']][:2]==['carriage','approach']
 await t.shot('arrival');await t.arrival_action('map');await map_to(t,'fountain')
 await t.save();saved=await t.state();await t.arrival_action('map');await map_to(t,'lane');await t.load();await t.wait('village_place')
 restored=await t.state();assert restored['village_location']=='fountain' and restored['minutes']==saved['minutes'] and restored['background']==saved['background']
 await pg.reload();await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(320,500);await t.wait('loading');await t.click(760,245);await t.wait('village_place')
 assert (await t.state())['village_location']=='fountain'
 assert not t.errors and not t.failed and not t.bad,(t.errors,t.failed,t.bad)
 await t.shot('restored-location');await c.close()
 return dict(viewport=[w,h],checks=['dialogue_faces','mid_line_save_load','carriage_camera_order','music_and_pulse_cleanup','no_default_crime_opening','location_movement','location_save_load','browser_refresh_load','no_browser_or_asset_errors'],injected_progress=False)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  results=[]
  for w,h in [(1280,720),(844,390)]:
   results.append(await run(b,w,h));print(json.dumps(results[-1]),flush=True)
  await b.close()
 report=dict(game_zip_sha256=hashlib.sha256((ROOT.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest(),routes=results)
 (ROOT/'SCENE_QA_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
