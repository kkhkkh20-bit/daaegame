"""Place-based native visual review, existing schedules; screenshots are not generated art."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/place-balance'));OUT.mkdir(exist_ok=True,parents=True)
async def main():
 report={'kind':'Native investigation fixtures; unique person/pose/place coverage, no campaign playthrough','shots':[],'observed':[]};seen=set()
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   report['version']=await q.py('import renpy;result=renpy.store.config.version')
   places=await q.py('import renpy;result=list(renpy.store.R13_PLACES)')
   for day,period,scenario in [(d,t,'routine') for d in (2,12) for t in range(3)]+[(12,0,'shelter')]:
    for loc in places:
     await setup(q,day,loc,flags=['ev_g_done']+(['shelter_ready','nubi_protected','bami_protected','patient_transport'] if scenario=='shelter' else []),period=period)
     await q.py('import renpy;s=renpy.store;s.r13_edit(case_state="pending" if s.room13["day"]==2 else "occurred",trial_result="pending");s.R13_STAGE_CACHE.clear();result=True')
     data=await q.py('import renpy;s=renpy.store;result=dict(actors=s.r13_stage_people(),width=s.r13_world_width(),place=s.R13_PLACES[s.room13["location"]][0],names={a["person"]:s.R13_NAMES.get(a["person"],a["person"]) for a in s.r13_stage_people()})')
     actors=data['actors'];fresh=[a for a in actors if (a['person'],a['pose'],loc) not in seen]
     if not fresh:continue
     for focus in fresh:
      key=(focus['person'],focus['pose'],loc)
      if key in seen:continue
      offset=max(0,min(focus['x']+focus['width']/2-640,data['width']-1280))
      await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,**{'+repr(loc)+':'+str(offset)+'});result=True');await native_jump(q,'r13_field');await q.wait('r13_hub');await page.mouse.move(1278,718);await asyncio.sleep(.2)
      actual=await q.py('import renpy;result=renpy.store.r13_world_offset()')
      visible=[a for a in actors if a['x']>=actual and a['x']+a['width']<=actual+1280]
      label=f'{len(report["shots"])+1:03d}-{loc}-d{day}-p{period}-{scenario}'
      await page.screenshot(path=str(OUT/(label+'.png')))
      report['shots'].append(dict(file=label+'.png',day=day,period=period,scenario=scenario,location=loc,location_name=data['place'],camera=actual,actors=visible,names=data['names']))
      for a in visible:seen.add((a['person'],a['pose'],loc))
      # A large/offscreen actor remains explicitly unreviewed if no complete screenshot fits.
      if key not in seen:seen.add(key);report['observed'].append(dict(key=key,status='partially visible; manual review required'))
      (OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(label,flush=True)
   report['status']='captured_for_visual_review';report['covered_combinations']=len(seen)
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
