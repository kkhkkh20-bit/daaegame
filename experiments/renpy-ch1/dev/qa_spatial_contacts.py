"""Focused native furniture contacts and existing square residents; no new schedules."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/spatial-before'));OUT.mkdir(exist_ok=True,parents=True)
async def main():
 report={'cases':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   report['version']=await q.py('import renpy;result=renpy.store.config.version')
   for loc,day,period,case in [('room13',2,t,c) for c in ['pending','occurred'] for t in range(3)]+[('guestroom',12,t,'occurred') for t in range(3)]+[('square',2,t,'pending') for t in range(3)]:
    label=f'{loc}-{day}-{period}-{case}';print(label,flush=True);await setup(q,day,loc,flags=['ev_g_done'],period=period)
    await q.py('import renpy;s=renpy.store;s.r13_edit(case_state='+repr(case)+',trial_result="pending");s.R13_STAGE_CACHE.clear();result=True')
    await native_jump(q,'r13_field');await q.wait('r13_hub')
    data=await q.py('import renpy;s=renpy.store;result=dict(actors=s.r13_stage_people(),location_name=s.R13_PLACES[s.room13["location"]][0],offset=s.r13_world_offset(),visible=s.r13_visible_people(),home=s.r13_home_with_daram(),daram_spec={k:s.r13_acting_spec("daram",k) for k in ["neutral","action_1","action_2","inspect_floor"]})')
    await page.screenshot(path=str(OUT/(label+'.png')));report['cases'].append(dict(label=label,**data))
   report['status']='captured'
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
