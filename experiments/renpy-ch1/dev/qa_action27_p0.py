"""Native field QA for eight approved map actions; scheduled fixtures, no whole campaign."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
from qa_remaining_approved22 import setup
OUT=Path('/workspace/action27-p0-runtime');OUT.mkdir(exist_ok=True)
CASES=[('resident_eunho',2,0,'market'),('resident_guseul',2,1,'market'),('resident_nubi',2,1,'market'),('resident_yeoni',3,0,'market'),('resident_dalgeurak',2,0,'market'),('resident_sling',2,0,'post'),('resident_sling',3,1,'post'),('resident_sling',2,2,'post'),('resident_piko',2,1,'square'),('resident_tok',2,0,'workshop')]
async def actor(q,who):return await q.py('import renpy;result=next((a for a in renpy.store.r13_stage_people() if a["person"]=='+repr(who)+'),None)')
async def save_load(q,slot):
 await q.press('메뉴');await asyncio.sleep(.3);await q.press('저장 · 불러오기');await q.wait('save');await q.press('1쪽 '+str(slot)+'번')
 st=await q.state()
 if any(b['text'].strip()=='예' for b in st['buttons']):await q.press('예')
 await q.press('돌아가기');await q.wait('r13_hub')
 await q.press('메뉴');await asyncio.sleep(.3);await q.press('저장 · 불러오기');await q.wait('save');await q.press('불러오기로');await q.wait('load');await q.press('1쪽 '+str(slot)+'번');await q.press('예');await q.wait('r13_hub');await q.py('import renpy;renpy.exports.hide_screen("qa_meeting_jump");renpy.exports.restart_interaction();result=True');await asyncio.sleep(.2)
async def main():
 report={'cases':[],'save_restore':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');report['version']=await q.py('import renpy;result=renpy.store.config.version');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.7)
   for i,(who,day,period,loc) in enumerate(CASES):
    if os.environ.get('ROOM13_CASE_FILTER') and who not in os.environ['ROOM13_CASE_FILTER'].split(','):continue
    print('CASE',who,day,period,loc,flush=True);await setup(q,day,loc,flags=['ev_g_done'],period=period)
    a=await actor(q,who);assert a and a['pose'].startswith('map27_'),a
    width=await q.py('import renpy;result=renpy.store.r13_world_width()');offset=max(0,min(a['x']+a['width']/2-640,width-1280))
    await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,**{'+repr(loc)+':'+str(offset)+'});renpy.exports.scene();renpy.exports.show("qa_field",what=s.r13_background(s.R13_PLACES['+repr(loc)+'][1]));result=True')
    await native_jump(q,'r13_field');await q.wait('r13_hub');await asyncio.sleep(.25);name=who+'-'+str(period);await page.screenshot(path=str(OUT/(name+'.png')))
    hit=await q.py('import renpy;s=renpy.store;a=next(x for x in s.r13_stage_people() if x["person"]=='+repr(who)+');x,y,w,h=s.r13_actor_face(a,0);f=renpy.display.render.focus_at_point(int(x+w/2-s.r13_world_offset()),int(y+h/2));acts=getattr(getattr(f,"widget",None),"action",[]);acts=acts if isinstance(acts,(list,tuple)) else [acts];result=dict(face=[x,y,w,h],actions=[str(getattr(z,"value",None)) for z in acts])')
    item=dict(person=who,day=day,period=period,location=loc,actor=a,hit=hit);report['cases'].append(item);assert any(who in x for x in hit['actions']),hit
    item['hidden_foot_hit']=await q.py('import renpy;s=renpy.store;a=next(x for x in s.r13_stage_people() if x["person"]=='+repr(who)+');sp=s.R13_ACTING[a["person"]][a["pose"]];sc=a["height"]/float(sp["crop"][3]);x=a["x"]+sp["foot"][0]*sc;y=a["y"]+sp["foot"][1]*sc;f=renpy.display.render.focus_at_point(int(x-s.r13_world_offset()),int(y));acts=getattr(getattr(f,"widget",None),"action",[]);acts=acts if isinstance(acts,(list,tuple)) else [acts];result=dict(point=[x,y],actions=[str(getattr(z,"value",None)) for z in acts])')
    assert not any(who in x for x in item['hidden_foot_hit']['actions']),item
    if i in [0,6,9]:
     slot={0:1,6:2,9:3}[i];await save_load(q,slot);restored=await actor(q,who);assert restored==a,(a,restored);report['save_restore'].append(dict(person=who,period=period,actor=restored));await page.screenshot(path=str(OUT/(name+'-restored.png')))
   report['guards']=await q.py('import renpy;s=renpy.store;s.r13_flag("tok_detained");s.R13_STAGE_CACHE.clear();result=dict(tok_absent=all(a["person"]!="resident_tok" for a in s.r13_stage_people()));s.r13_edit(flags=[f for f in s.room13["flags"] if f!="tok_detained"])')
   assert report['guards']['tok_absent']
   # Real map UI round-trip, preserving time and actor placement.
   before=await actor(q,'resident_tok');clock=await q.py('import renpy;s=renpy.store;result=[s.room13["day"],s.room13["period"]]')
   for label,loc in [('우체국','post'),('수리점','workshop')]:
    await q.press('지도 · 이동');await q.wait('r13_map');st=await q.state();button=min((z for z in st['buttons'] if z['value']==loc),key=lambda z:z['rect'][2]*z['rect'][3]);x,y,w,h=button['rect'];await q.input(x+w/2,y+h/2);await asyncio.sleep(.2);await q.press('이곳으로 이동');await q.advance();await q.wait('r13_hub');assert (await q.room())['location']==loc
   after=await actor(q,'resident_tok');assert before==after,(before,after);assert await q.py('import renpy;s=renpy.store;result=[s.room13["day"],s.room13["period"]]')==clock
   report['movement']=dict(route=['workshop','post','workshop'],clock=clock,restored=after);await page.screenshot(path=str(OUT/'movement-restored.png'))
   report['status']='passed' 
  except Exception as e:report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
