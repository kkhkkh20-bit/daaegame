"""Focused native object-scale review; injection is preview-only."""
import asyncio,json,os,textwrap
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/balance-preview'));OUT.mkdir(exist_ok=True,parents=True)
CASES=[('school',12,0,False,0),('school',12,2,False,0),('school',12,0,True,0),('school',12,0,True,520),('post',2,0,False,880),('post',12,1,False,0),('clinic',12,0,False,550),('clinic',12,1,False,550),('room13',2,0,False,520),('guestroom',12,0,False,0),('square',2,1,False,640)]+[(loc,2 if loc=='room13' else 12,t,False,520 if loc=='room13' else 0) for loc in ('room13','guestroom') for t in (1,2)]+[('room13',12,0,False,520)]
async def main():
 report={'kind':'injected preview' if os.environ.get('ROOM13_BALANCE_INJECT') else 'native SDK release','archive_sha256':json.loads((ROOT.parents[1]/'preview/room13-dev/game-transport.json').read_text())['archive_sha256'],'cases':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   if os.environ.get('ROOM13_BALANCE_INJECT'):
    source=textwrap.dedent((ROOT/'game/systems/room13_investigation_balance.rpy').read_text().split('init 180 python:\n')[1]);rows=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())
    await q.py('import renpy;exec('+repr(source)+',renpy.store.__dict__);renpy.store.R13_MAP_ACTION27='+repr(rows)+';result=True')
   report['version']=await q.py('import renpy;result=renpy.store.config.version')
   for loc,day,period,shelter,camera in CASES:
    if os.environ.get('ROOM13_BALANCE_LOCATIONS') and loc not in os.environ['ROOM13_BALANCE_LOCATIONS'].split(','):continue
    await setup(q,day,loc,flags=['ev_g_done']+(['shelter_ready','nubi_protected','bami_protected','patient_transport'] if shelter else []),period=period)
    await q.py('import renpy;s=renpy.store;s.r13_edit(case_state="pending" if s.room13["day"]==2 else "occurred",trial_result="acquitted" if s.room13["location"]=="guestroom" else "pending");s.r13_world_cameras=s.dict(s.r13_world_cameras,**{'+repr(loc)+':'+str(camera)+'});s.R13_STAGE_CACHE.clear();result=True')
    await native_jump(q,'r13_field');await q.wait('r13_hub');await page.mouse.move(1278,718)
    label=f'{loc}-{day}-{period}-{shelter}-{camera}';await page.screenshot(path=str(OUT/(label+'.png')))
    data=await q.py('''import renpy
s=renpy.store
actors=s.r13_stage_people();offset=s.r13_world_offset();hits=[]
for a in actors:
 x,y,w,h=s.r13_actor_face(a,0);px=int(x+w/2-offset);py=int(y+h/2)
 if 20<px<1260 and 105<py<620:
  f=renpy.display.render.focus_at_point(px,py);acts=getattr(getattr(f,'widget',None),'action',[]);acts=acts if isinstance(acts,(list,tuple)) else [acts]
  hits.append(dict(person=a['person'],point=[px,py],actions=[str(getattr(z,'value',None)) for z in acts]))
result=dict(actors=actors,offset=offset,hits=hits,specs={a['person']:s.r13_acting_spec(a['person'],a['pose']) for a in actors},room={k:s.room13[k] for k in ('day','period','location')})''')
    if not os.environ.get('ROOM13_BALANCE_INJECT'):
     who={'school':'resident_teacher','post':'resident_sling','clinic':'resident_piko','room13':'daram','guestroom':'daram','square':'resident_sling'}[loc]
     hit=next((h for h in data['hits'] if h['person']==who),None)
     if hit:
      assert any(who in a for a in hit['actions']),hit
      await q.py('import renpy;renpy.store.r13_target=None;result=True');await q.input(*hit['point']);await asyncio.sleep(.3)
      data['clicked']=await q.py('import renpy;result=renpy.store.r13_target');assert data['clicked']==who
    report['cases'].append(dict(label=label,**data));print(label,[(h['person'],h['actions']) for h in data['hits'] if not any(h['person'] in a for a in h['actions'])],flush=True)
   if not os.environ.get('ROOM13_BALANCE_INJECT'):
    report['matrix']=await q.py("""import renpy,json
s=renpy.store;rows=[];errors=[]
for day in (2,7,12):
 for period in range(3):
  for scenario in ('routine','offers','absent'):
   s.room13=s.r13_new();s.r13_upgrade();s.r13_flag('entry_corrected','lodging')
   if scenario!='offers':s.r13_flag('ev_g_done')
   if scenario=='absent':s.r13_flag(*list(s.R13_DEATH_FLAGS.values()))
   s.r13_edit(day=day,period=period,case_state='pending' if day==2 else 'occurred',trial_result='pending')
   for loc in ('school','post','clinic','room13','guestroom','square'):
    s.r13_edit(location=loc);s.R13_STAGE_CACHE.clear()
    before=s._r13_balance_stage();snapshot=json.dumps(before,sort_keys=True);state=json.dumps(s.room13,sort_keys=True);after=s.r13_stage_people()
    if snapshot!=json.dumps(before,sort_keys=True):errors.append([day,period,scenario,loc,'mutated prior actors'])
    if state!=json.dumps(s.room13,sort_keys=True):errors.append([day,period,scenario,loc,'mutated state'])
    old={a['person']:a for a in before};new={a['person']:a for a in after}
    if set(old)!=set(new):errors.append([day,period,scenario,loc,'changed presence'])
    for who,a in new.items():
     changed=a!=old[who]
     if a['pose']!=old[who]['pose']:errors.append([day,period,scenario,loc,who,'changed pose'])
     if changed and s.r13_offer_for_person(who):errors.append([day,period,scenario,loc,who,'moved event'])
     rows.append(dict(day=day,period=period,scenario=scenario,location=loc,person=who,changed=changed))
result=dict(rows=rows,errors=errors)""")
    assert not report['matrix']['errors'],report['matrix']['errors']
   report['status']='passed' if not os.environ.get('ROOM13_BALANCE_INJECT') else 'preview_captured' 
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
