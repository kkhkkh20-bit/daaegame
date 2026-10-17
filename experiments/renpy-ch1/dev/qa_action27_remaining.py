"""Focused native field fixtures for approved action27 remaining sources."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
from qa_remaining_approved22 import setup
from qa_action27_p0 import actor,save_load
OUT=Path('/workspace/action27-rest-runtime');OUT.mkdir(exist_ok=True)
CASES=[('MK-1','resident_solbang',2,1,'market'),('MK-7','resident_mungchi',2,0,'market'),('MK-8','resident_hyeoni',2,1,'market'),('MK-8','resident_hyeoni',2,0,'square'),('MK-8','resident_hyeoni',2,2,'dining'),('PO-2','resident_librarian',2,0,'post'),('PO-2','resident_librarian',2,1,'post'),('PO-3','resident_jongjong',2,0,'post'),('PO-3','resident_jongjong',2,1,'post'),('IN-1','resident_nubi',2,0,'inn'),('IN-1','resident_nubi',12,0,'facility'),('IN-1','resident_nubi',12,2,'school'),('ST-1','resident_mungchi',2,1,'store'),('ST-2','resident_siluk',2,1,'store'),('SQ-1','resident_dalgeurak',2,1,'square'),('GA-1','neoul',2,0,'gate'),('CL-1','resident_piko',12,0,'clinic'),('CL-1','resident_piko',12,1,'clinic'),('CL-1','resident_piko',12,2,'clinic'),('SC-1','resident_teacher',2,0,'school'),('FA-1','neoul',12,0,'facility'),('DI-1a','resident_tok',2,2,'dining'),('DI-1b','resident_dalgeurak',2,2,'dining'),('RI-1','resident_kkwak',2,1,'river'),('RI-2','resident_mulgyeol',2,0,'river'),('FO-1','resident_kalbaram',2,0,'forest')]
async def main():
 report={'cases':[],'issues':[],'save_restore':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await browser.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');report['version']=await q.py('import renpy;result=renpy.store.config.version');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.7)
   for key,who,day,period,loc in CASES:
    if os.environ.get('ROOM13_CASE_FILTER') and key not in os.environ['ROOM13_CASE_FILTER'].split(','):continue
    print('CASE',key,loc,period,flush=True);await setup(q,day,loc,flags=['ev_g_done'],period=period)
    a=await actor(q,who);expected='map27_'+key.lower().replace('-','_')
    if not a or a['pose']!=expected:
     report['issues'].append(dict(key=key,person=who,location=loc,period=period,actor=a,all_actors=await q.py('import renpy;result=renpy.store.r13_stage_people()')));print('UNRESOLVED',key,a,flush=True);continue
    width=await q.py('import renpy;result=renpy.store.r13_world_width()');offset=max(0,min(a['x']+a['width']/2-640,width-1280))
    await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,**{'+repr(loc)+':'+str(offset)+'});renpy.exports.scene();renpy.exports.show("qa_field",what=s.r13_background(s.R13_PLACES['+repr(loc)+'][1]));result=True');await native_jump(q,'r13_field');await q.wait('r13_hub');await asyncio.sleep(.2)
    name=key+'-'+loc+'-'+str(period);await page.screenshot(path=str(OUT/(name+'.png')))
    hit=await q.py('import renpy;s=renpy.store;a=next(x for x in s.r13_stage_people() if x["person"]=='+repr(who)+');x,y,w,h=s.r13_actor_face(a,0);f=renpy.display.render.focus_at_point(int(x+w/2-s.r13_world_offset()),int(y+h/2));acts=getattr(getattr(f,"widget",None),"action",[]);acts=acts if isinstance(acts,(list,tuple)) else [acts];result=dict(face=[x,y,w,h],actions=[str(getattr(z,"value",None)) for z in acts])')
    item=dict(key=key,person=who,day=day,period=period,location=loc,actor=a,hit=hit,all_actors=await q.py('import renpy;result=renpy.store.r13_stage_people()'));report['cases'].append(item)
    if not any(who in x for x in hit['actions']):report['issues'].append(dict(key=key,location=loc,period=period,hit=hit))
    if key in ['CL-1','FA-1','DI-1a'] and period==({'CL-1':1,'FA-1':0,'DI-1a':2}[key]):
     await save_load(q,{'CL-1':1,'FA-1':2,'DI-1a':3}[key]);restored=await actor(q,who);assert restored==a,(a,restored);report['save_restore'].append(dict(key=key,actor=restored))
   report['nabi']=await q.py('import renpy;s=renpy.store;r=next(r for r in s.R13_MAP_ACTION27["rows"] if r["request_id"]=="KI-1");result=dict(registered=r["pose"] in s.R13_ACTING["nabi"],periods=r["periods"],file=r["spec"]["file"])');assert report['nabi']['registered'] and report['nabi']['periods']==[]
   if os.environ.get('ROOM13_CHECK_PREVIEW'):
    await setup(q,2,'kitchen',flags=['ev_g_done']);await native_jump(q,'r13_field');await q.wait('r13_hub')
    report['nabi']['scheduled_in_kitchen']=await q.py('import renpy;result=any(a["person"]=="nabi" for a in renpy.store.r13_stage_people())');assert not report['nabi']['scheduled_in_kitchen']
    preview_code='\n'.join(['import renpy','def _qa_map27_preview(**kwargs):',' import renpy',' s=renpy.store',' r=next(r for r in s.R13_MAP_ACTION27["rows"] if r["request_id"]=="KI-1")',' a=s.r13_map27_geometry(dict(person="nabi",pose=r["pose"],occlusion=[]),r["spec"],r["variants"]["morning"],2160)',' renpy.ui.add(s.Transform(s.r13_staged_visible_art(a,True),xpos=a["x"]-s.r13_world_offset(),ypos=a["y"]))',' renpy.ui.text("KI-1 PREVIEW ONLY - no kitchen schedule",size=25,color="#fff",outlines=[(2,"#000",0,0)],xpos=40,ypos=80)',"renpy.exports.define_screen('qa_map27_preview',_qa_map27_preview,zorder='300')","renpy.exports.show_screen('qa_map27_preview')","renpy.exports.restart_interaction()","result=True"])
    await q.py(preview_code);await asyncio.sleep(.3);await page.screenshot(path=str(OUT/'KI-1-preview-only.png'))
    report['nabi']['preview_screen_visible']=await q.py('import renpy;result=bool(renpy.display.screen.get_screen("qa_map27_preview"))');assert report['nabi']['preview_screen_visible']
    await q.py('import renpy;renpy.exports.hide_screen("qa_map27_preview");renpy.exports.restart_interaction();result=True')
    report['absence_guards']=[]
    for who,loc,day,period,flag in [('resident_piko','clinic',12,0,'piko_dead'),('resident_teacher','school',2,0,'teacher_dead'),('resident_librarian','post',2,0,'librarian_dead'),('resident_siluk','store',2,1,'siluk_dead'),('resident_tok','dining',2,2,'tok_detained')]:
     await setup(q,day,loc,flags=['ev_g_done',flag],period=period);absent=await q.py('import renpy;result=all(a["person"]!='+repr(who)+' for a in renpy.store.r13_stage_people())');assert absent,(who,flag);report['absence_guards'].append(dict(person=who,flag=flag,absent=absent))
   report['status']='passed' if not report['issues'] else 'needs_review'
  except Exception as e:report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await browser.close()
if __name__=='__main__':asyncio.run(main())
