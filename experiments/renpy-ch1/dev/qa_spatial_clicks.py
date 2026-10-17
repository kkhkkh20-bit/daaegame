"""Actual final actor hit targets, plus bounded runtime preservation matrix."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/spatial-clicks');OUT.mkdir(exist_ok=True)
MATRIX='''import renpy
def _qa_contacts():
 import renpy,json
 s=renpy.store;rows=[];errors=[]
 for day in (2,7,12):
  for period in range(3):
   for scenario in ('routine','offers','absent'):
    s.room13=s.r13_new();s.r13_upgrade();s.r13_flag('entry_corrected','lodging')
    if scenario!='offers':s.r13_flag('ev_g_done')
    if scenario=='absent':s.r13_flag(*list(s.R13_DEATH_FLAGS.values()))
    s.r13_edit(day=day,period=period,case_state='pending' if day==2 else 'occurred',trial_result='pending',daram_state='missing' if scenario=='absent' else 'with_dad')
    for loc in ('room13','guestroom','square','clinic','school','dining','workshop','post'):
     s.r13_edit(location=loc);s.R13_STAGE_CACHE.clear()
     before=s._r13_contact_stage();snapshot=json.dumps(before,sort_keys=True);after=s.r13_stage_people()
     if json.dumps(before,sort_keys=True)!=snapshot:errors.append([day,period,loc,'mutated prior stage'])
     old={a['person']:a for a in before};new={a['person']:a for a in after}
     if set(old)!=set(new):errors.append([day,period,loc,'changed presence'])
     for who,a in new.items():
      changed=a!=old[who]
      if changed and not ((loc in ('room13','guestroom') and who=='daram') or (loc=='square' and who in s.R13_SQUARE_LEVELS) or (loc=='clinic' and who=='resident_seori')):errors.append([day,period,loc,who,'unrelated actor changed'])
      if changed and s.r13_offer_for_person(who):errors.append([day,period,loc,who,'event moved'])
      rows.append(dict(day=day,period=period,scenario=scenario,location=loc,person=who,pose=a['pose'],changed=changed,contact=a.get('contact')))
 return dict(rows=rows,errors=errors)
renpy.store._qa_contacts=_qa_contacts
result=True'''
async def main():
 report={'clicks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   for loc,period,case,trial,person in [('room13',0,'pending','pending','daram'),('room13',1,'occurred','pending','daram'),('guestroom',0,'occurred','acquitted','daram'),('square',1,'pending','pending','resident_sling'),('square',0,'pending','pending','resident_seol'),('clinic',0,'occurred','pending','resident_seori'),('clinic',1,'occurred','pending','resident_seori'),('clinic',2,'occurred','pending','resident_seori')]:
    await setup(q,12 if loc=='clinic' else 2,loc,flags=['ev_g_done'],period=period);await q.py('import renpy;s=renpy.store;s.r13_edit(case_state='+repr(case)+',trial_result='+repr(trial)+');s.R13_STAGE_CACHE.clear();result=True')
    if person=='resident_seori':
     scheduled=await q.py('import renpy;result=renpy.store.r13_where("resident_seori")')
     if scheduled!=loc:
      loc=scheduled
      await q.py('import renpy;s=renpy.store;s.r13_edit(location='+repr(loc)+');s.R13_STAGE_CACHE.clear();s.place=s.R13_PLACES['+repr(loc)+'][0];result=True')
    offset=await q.py('import renpy;s=renpy.store;a=next(a for a in s.r13_stage_people() if a["person"]=='+repr(person)+');result=max(0,min(a["x"]+a["width"]/2-640,s.r13_world_width()-1280))')
    await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,**{'+repr(loc)+':'+str(offset)+'});result=True');await native_jump(q,'r13_field');await q.wait('r13_hub')
    probe=await q.py('import renpy;s=renpy.store;a=next(a for a in s.r13_stage_people() if a["person"]=='+repr(person)+');x,y,w,h=s.r13_actor_face(a,0);px=int(x+w/2-s.r13_world_offset());py=int(y+h/2);f=renpy.display.render.focus_at_point(px,py);acts=getattr(getattr(f,"widget",None),"action",[]);acts=acts if isinstance(acts,(list,tuple)) else [acts];result=dict(actor=a,point=[px,py],actions=[str(getattr(z,"value",None)) for z in acts])')
    assert any(person in v for v in probe['actions']),probe
    label=f'{loc}-{period}-{case}-{person}';await page.screenshot(path=str(OUT/(label+'.png')))
    await q.input(*probe['point']);await asyncio.sleep(.4)
    target=await q.py('import renpy;result=renpy.store.r13_target');assert target==person,(target,person)
    report['clicks'].append(dict(label=label,person=person,target=target,**probe));print('CLICK',label,flush=True)
   await q.py(MATRIX);report['matrix']=await q.py('import renpy;result=renpy.store._qa_contacts()');assert not report['matrix']['errors'];report['status']='passed'
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
