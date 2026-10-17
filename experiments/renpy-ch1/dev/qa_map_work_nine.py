"""Focused actual field rendering, with scheduled states rather than a full campaign."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/map-work-nine-runtime');OUT.mkdir(exist_ok=True)
CASES=[('resident_teacher',2,0,'school'),('resident_kkwak',2,1,'river'),('resident_nubi',2,0,'inn'),('resident_mungchi',2,1,'store'),('resident_mulgyeol',2,0,'river'),('resident_dalgeurak',2,0,'market'),('resident_jongjong',2,0,'post'),('resident_guldol',2,0,'workshop'),('resident_piko',11,0,'clinic')]
async def main():
 report={'cases':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8887/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(1)
   report['version']=await q.py('import renpy;result=renpy.store.config.version')
   for who,day,period,location in CASES:
    await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_flag("entry_corrected","lodging");s.r13_edit(day='+str(day)+',period='+str(period)+',location='+repr(location)+');s.room13_mode=True;s.r13_camera="stage";s.r13_meeting_active=False;s.r13_cg_active=False;s.r13_thought_active=False;s.place=s.R13_PLACES['+repr(location)+'][0];s.r13_scene_bg=s.R13_PLACES['+repr(location)+'][1];s.R13_STAGE_CACHE.clear();result=True')
    data=await q.py('import renpy;s=renpy.store;actors=s.r13_stage_people();wanted='+repr(who)+';a=next((x for x in actors if x["person"]=='+repr(who)+'),None);result=dict(actor=a,all=[(x["person"],x["pose"]) for x in actors])')
    report['cases'].append(dict(person=who,day=day,period=period,location=location,**data));assert data['actor'] and data['actor']['pose'].startswith('map9_'),data
    a=data['actor'];offset=max(0,min(a['x']+a['width']/2-640,await q.py('import renpy;result=renpy.store.r13_world_width()-1280')))
    await q.py('import renpy;s=renpy.store;s.r13_world_cameras=dict(s.r13_world_cameras,**{'+repr(location)+':'+str(offset)+'});result=True')
    await native_jump(q,'r13_field');await q.wait('r13_hub');await asyncio.sleep(.4);await page.screenshot(path=str(OUT/(who+'.png')))
    report['cases'][-1]['hit']=await q.py('import renpy;s=renpy.store;a=next(x for x in s.r13_stage_people() if x["person"]=='+repr(who)+');x,y,w,h=s.r13_actor_face(a,0);f=renpy.display.render.focus_at_point(int(x+w/2-s.r13_world_offset()),int(y+h/2));actions=getattr(getattr(f,"widget",None),"action",[]);actions=actions if isinstance(actions,(list,tuple)) else [actions];result=dict(face=[x,y,w,h],offset=s.r13_world_offset(),actions=[str(getattr(a,"value",None)) for a in actions])')
    assert any(who in value for value in report['cases'][-1]['hit']['actions']),report['cases'][-1]['hit']
    if who=='resident_piko':
     report['blanket_hit']=await q.py('import renpy;s=renpy.store;f=renpy.display.render.focus_at_point(int(1200-s.r13_world_offset()),410);actions=getattr(getattr(f,"widget",None),"action",[]);actions=actions if isinstance(actions,(list,tuple)) else [actions];result=[str(getattr(a,"value",None)) for a in actions]')
     assert not any('resident_piko' in value for value in report['blanket_hit'])
   report['status']='passed' 
  except Exception as e:report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
