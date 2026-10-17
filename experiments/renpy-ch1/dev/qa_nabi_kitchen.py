"""Native five kitchen actions and 14-day/three-period state matrix (no campaign playthrough)."""
import asyncio,csv,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
from qa_action27_p0 import actor,save_load
OUT=Path('/workspace/nabi-kitchen-runtime');OUT.mkdir(exist_ok=True)
MATRIX='''import renpy
def _qa_map31_matrix(day):
 import renpy
 s=renpy.store
 people=sorted(set(r['person'] for r in s.R13_MAP_ACTION27['rows']))
 locations=sorted(set(r['location'] for r in s.R13_MAP_ACTION27['rows']))
 poses=set(r['pose'] for r in s.R13_MAP_ACTION27['rows'])
 records=[];errors=[]
 for scenario in ['routine','offers','losses','shelter','case_prevented']:
  for period in range(3):
   s.room13=s.r13_new();s.r13_upgrade()
   flags=['entry_corrected','lodging']+([] if scenario=='offers' else ['ev_g_done'])
   if scenario=='losses':flags+=list(s.R13_DEATH_FLAGS.values())+['chorong_dead','ttadak_dead','musoe_gone','tok_detained']
   if scenario=='shelter':flags+=['shelter_ready','nubi_protected','bami_protected','patient_transport','mom_reunited']
   s.r13_flag(*flags)
   case='prevented' if scenario=='case_prevented' else 'occurred' if day>s.R13_CASE_DAY or (day==s.R13_CASE_DAY and period==2) else 'pending'
   s.r13_edit(day=day,period=period,location='kitchen',case_state=case,granny_state='detained' if scenario=='losses' else 'trusted',victim_state='dead' if scenario=='losses' else 'alive',daram_state='with_dad')
   expected={who:s.r13_where(who) for who in people};found={who:[] for who in people};s.R13_STAGE_CACHE.clear()
   for loc in locations:
    s.r13_edit(location=loc);width=s.r13_world_width();daylight=s.r13_daylight()
    for a in s.r13_stage_people():
     who=a['person']
     if who not in found:continue
     offer=bool(s.r13_offer_for_person(who));found[who].append(dict(location=loc,pose=a['pose'],world_width=width,rect=a['rect'],height=a['height'],contact=a['contact'],offer=offer))
     if a['pose'] in poses:
      row=next((r for r in s.R13_MAP_ACTION27['rows'] if r['person']==who and r['pose']==a['pose'] and r['location']==loc),None)
      if row is None:errors.append([day,period,scenario,who,'stale location pose',loc]);continue
      test=dict(a,pose=row['replace_poses'][0]);v=s.r13_map27_variant(row,test,s.room13,daylight,width,offer)
      if v is None:errors.append([day,period,scenario,who,'pose bypassed date/period/story/width guard',loc])
      if not s.renpy.loadable(row['spec']['file']):errors.append([day,period,scenario,who,'missing artwork'])
   for who in people:
    actual=found[who]
    if len(actual)>1:errors.append([day,period,scenario,who,'duplicate locations',actual])
    if any(a['location']!=expected[who] for a in actual):errors.append([day,period,scenario,who,'schedule mismatch',expected[who],actual])
    if expected[who] in locations and not actual:errors.append([day,period,scenario,who,'scheduled actor missing',expected[who]])
    if expected[who] is None and actual:errors.append([day,period,scenario,who,'absent actor resurrected'])
    records.append(dict(day=day,period=period,scenario=scenario,person=who,scheduled=expected[who],appearances=actual))
 return dict(day=day,records=records,errors=errors)
renpy.store._qa_map31_matrix=_qa_map31_matrix
result=True'''
async def main():
 report={'cases':[],'saves':[],'matrix':[],'errors':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');report['version']=await q.py('import renpy;result=renpy.store.config.version');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.5)
   for day in [2,3,4,5,6]:
    print('KITCHEN DAY',day,flush=True);await setup(q,day,'kitchen',flags=['ev_g_done']);a=await actor(q,'nabi');assert a and a['pose'].startswith(('map27_ki_1','map31_nabi_')),a
    width=await q.py('import renpy;result=renpy.store.r13_world_width()');offset=max(0,min(a['x']+a['width']/2-640,width-1280));await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,kitchen='+str(offset)+');result=True');await native_jump(q,'r13_field');await q.wait('r13_hub');await asyncio.sleep(.2);await page.screenshot(path=str(OUT/('kitchen-day'+str(day)+'.png')))
    hit=await q.py('import renpy;s=renpy.store;a=next(a for a in s.r13_stage_people() if a["person"]=="nabi");x,y,w,h=s.r13_actor_face(a,0);f=renpy.display.render.focus_at_point(int(x+w/2-s.r13_world_offset()),int(y+h/2));acts=getattr(getattr(f,"widget",None),"action",[]);acts=acts if isinstance(acts,(list,tuple)) else [acts];result=[str(getattr(z,"value",None)) for z in acts]');assert any('nabi' in x for x in hit),hit
    report['cases'].append(dict(day=day,person='nabi',period=0,location='kitchen',actor=a,hit=hit))
    if day in [2,3]:await save_load(q,day-1);assert await actor(q,'nabi')==a;report['saves'].append(dict(day=day,restored=a))
   # Existing serving and week2 priority scenes: one person, no kitchen pose leakage.
   for day,period,loc,flags,granny in [(2,1,'dining',[],'trusted'),(12,0,'school',['shelter_ready'],'trusted'),(12,0,'inn',['shelter_ready'],'detained')]:
    await setup(q,day,loc,flags=['ev_g_done']+flags,period=period);await q.py('import renpy;s=renpy.store;s.r13_edit(granny_state='+repr(granny)+');result=True');a=await actor(q,'nabi');assert a and not a['pose'].startswith(('map27_ki','map31_')),a;await native_jump(q,'r13_field');await q.wait('r13_hub');await page.screenshot(path=str(OUT/('nabi-'+loc+'-'+str(day)+'.png')));report['cases'].append(dict(day=day,period=period,location=loc,actor=a))
   if not os.environ.get('ROOM13_SKIP_MATRIX'):
    await q.py(MATRIX)
    for day in range(1,15):
     print('MATRIX DAY',day,flush=True);r=await q.py('import renpy;result=renpy.store._qa_map31_matrix('+str(day)+')');report['matrix']+=r['records'];report['errors']+=r['errors']
    assert not report['errors'],report['errors'][:10]
   report['status']='passed'
  except Exception as e:report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
   with (OUT/'schedule.csv').open('w',newline='') as f:
    w=csv.writer(f,lineterminator="\n");w.writerow(['scenario','day','period','person','scheduled','actual_location','pose','world_width','rect','offer'])
    for r in report['matrix']:
     a=r['appearances'][0] if r['appearances'] else {};w.writerow([r['scenario'],r['day'],r['period'],r['person'],r['scheduled'],a.get('location'),a.get('pose'),a.get('world_width'),a.get('rect'),a.get('offer')])
   await b.close()
if __name__=='__main__':asyncio.run(main())
