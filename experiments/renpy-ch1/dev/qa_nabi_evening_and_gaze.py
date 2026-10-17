"""Existing kitchen story, native travel, and inspector identity/gaze evidence."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
from qa_action27_p0 import actor
OUT=Path('/workspace/nabi-evening-gaze');OUT.mkdir(exist_ok=True)
async def main():
 report={}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.5)
   await setup(q,2,'kitchen',flags=['ev_g_done']);await native_jump(q,'r13_field');await q.wait('r13_hub');before=await actor(q,'nabi');assert before['pose']=='map27_ki_1';report['movement']=[]
   for loc in ['dining','kitchen']:
    await q.press('지도 · 이동');await q.wait('r13_map');st=await q.state();button=min((z for z in st['buttons'] if z['value']==loc),key=lambda z:z['rect'][2]*z['rect'][3]);x,y,w,h=button['rect'];await q.input(x+w/2,y+h/2);await asyncio.sleep(.2);await q.press('이곳으로 이동');await q.advance();await q.wait('r13_hub');room=await q.room();a=await actor(q,'nabi');assert room['location']==loc and [room['day'],room['period']]==[2,0]
    assert a is None if loc=='dining' else a==before;report['movement'].append(dict(location=loc,actor=a,day=room['day'],period=room['period']))
   await setup(q,2,'dining',flags=['ev_g_done','evening_brief:2'],period=2);await q.py('import renpy;renpy.store.r13_edit(case_state="pending");result=True');await native_jump(q,'r13_field');await q.wait('r13_hub')
   await q.press('지도 · 이동');await q.wait('r13_map');st=await q.state();button=min((z for z in st['buttons'] if z['value']=='kitchen'),key=lambda z:z['rect'][2]*z['rect'][3]);x,y,w,h=button['rect'];await q.input(x+w/2,y+h/2);await asyncio.sleep(.2);await q.press('이곳으로 이동');picked=False;captured=False
   for step in range(90):
    st=await q.state();room=await q.room()
    if 'W2' in room.get('evidence',[]) and 'kids_known' in room.get('flags',[]):break
    if 'choice' in st['screens']:
     await page.screenshot(path=str(OUT/'existing-evening-choices.png'));await q.press('음식 짐을 같이 날라 준다');picked=True
    elif 'say' in st['screens']:
     snap=await q.py('import renpy;s=renpy.store;p=s.r13_dialogue_source_profile("nabi",s.r13_current_pose,840);result=dict(person=s.r13_motion_person,pose=s.r13_current_pose,packet=s.r13_packet,file=p["frames"]["neutral"]["file"] if p else None)')
     if snap['person']=='nabi' and not captured:report['evening_dialogue']=snap;await page.screenshot(path=str(OUT/'existing-evening-nabi.png'));captured=True
     await q.input(900,615)
    elif any('계속' in x['text'] for x in st['buttons']):await q.press('계속')
    else:await asyncio.sleep(.1)
   room=await q.room();assert picked and captured and 'W2' in room['evidence'] and all(f in room['flags'] for f in ['ep2_seen','kids_known','nabi_secret','know_nabi_debt']),room
   assert [room['day'],room['period']]==[2,2],room
   report['evening_result']=dict(day=room['day'],period=room['period'],flags=[f for f in room['flags'] if f in ['ep2_seen','kids_known','nabi_secret','know_nabi_debt']],evidence=['W2']);assert not report['evening_dialogue']['pose'].startswith(('map27','map31'))
   await setup(q,12,'clinic',flags=['ev_g_done']);a=await actor(q,'resident_seori');assert a
   width=await q.py('import renpy;result=renpy.store.r13_world_width()');offset=max(0,min(a['x']+a['width']/2-640,width-1280));await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,clinic='+str(offset)+');result=True');await native_jump(q,'r13_field');await q.wait('r13_hub');await page.screenshot(path=str(OUT/'seori-clinic-existing-gaze.png'))
   report['inspector']=await q.py('import renpy;s=renpy.store;a=next(a for a in s.r13_stage_people() if a["person"]=="resident_seori");result=dict(person="resident_seori",actor=a,spec=s.R13_ACTING["resident_seori"][a["pose"]],other_character="resident_seol")')
   report['status']='passed'
  except Exception as e:report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
