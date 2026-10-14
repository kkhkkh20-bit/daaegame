"""Explicit layout fixtures for five scenes; no claims of natural campaign completion."""
import asyncio,json,shutil,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from pixel_qa_ui0156 import UIQA
OUT=Path('/workspace/room13-review/world0178');OUT.mkdir(exist_ok=True)
URL='http://127.0.0.1:8094/room13-dev/'
PLACES=['clinic','store','greenhouse','facility','altar']
class Q(UIQA):
 async def pan(self,right):
  await self.p.mouse.move(1100 if right else 220,650);await self.p.mouse.down();await self.p.mouse.move(220 if right else 1100,650,steps=20);await self.p.mouse.up();await asyncio.sleep(.7)
 async def object(self,key):
  print('CLICK',key,flush=True);rect=await self.py('import renpy;s=renpy.store;result=s.ROOM13["objects"][s.room13["location"]]['+repr(key)+']["rect"]');x,y,w,h=rect
  offset=(await self.camera())['offset']
  if x+w/2-offset<80:await self.pan(False)
  elif x+w/2-offset>1190:await self.pan(True)
  offset=(await self.camera())['offset'];assert 0<x+w/2-offset<1280,(key,rect,offset);print('COORD',key,rect,offset,flush=True);await self.input(x+w/2-offset,y+h/2);await self.advance()
  if 'r13_object_context' in (await self.state())['screens']:await self.press('그만 살펴본다');await self.advance()
  await self.wait('r13_hub')
async def main():
 report={'kind':'Explicit calendar/branch geometry and crowded-scene fixtures','archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'checks':[],'matrices':{}}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=Q(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   for loc in PLACES:
    code="""import renpy,copy
s=renpy.store;original=copy.deepcopy(s.room13);rows=[];bad=[]
try:
 for day in range(1,15):
  for period in range(3):
   for case in (["pending"] if day<=4 else ["occurred","prevented"]):
    s.r13_edit(location=LOCATION,day=day,period=period,case_state=case,flags=list(original["flags"])+(["mom_reunited"] if day>=8 else []),mom_state="reunited" if day>=8 else "hidden",trial_ended=day>=8,week2_started=day>=8,victim_state="dead" if case=="occurred" else "protected" if case=="prevented" else "alive")
    actors=s.r13_stage_people();row=dict(day=day,period=period,case=case,count=len(actors));rows.append(row)
    for a in actors:
     if a['x']<0 or a['y']<0 or a['x']+a['width']>1920 or a['y']+a['height']>720:bad.append(dict(state=row,actor=a))
finally:
 s.room13=original;s.R13_STAGE_CACHE.clear()
result=dict(rows=rows,bad=bad)""".replace('LOCATION',repr(loc))
    matrix=await q.py(code);report['matrices'][loc]=matrix;assert not matrix['bad'],matrix['bad'][:3];dense=max(matrix['rows'],key=lambda r:r['count']);print('MATRIX',loc,'max residents',dense['count'],flush=True)
    code='import renpy;s=renpy.store;s.r13_edit(location='+repr(loc)+',day='+str(dense['day'])+',period='+str(dense['period'])+',case_state='+repr(dense['case'])+');s.r13_upgrade();s.place=s.R13_PLACES[s.room13["location"]][0];renpy.exports.scene();renpy.exports.show("qa_world_bg",what=s.r13_background(s.R13_PLACES[s.room13["location"]][1]));w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True'
    await q.py('import renpy;s=renpy.store;s.r13_flag(\"mom_reunited\");s.r13_edit(mom_state=\"reunited\",trial_ended=True,week2_started=True);result=True') if dense['day']>=8 else None
    await q.py(code);await q.input(1220,50);await q.wait('r13_hub');before=await q.room();await q.pan(False);await q.shot(loc+'-dense-left');await q.pan(True);await q.shot(loc+'-dense-right');assert await q.room()==before
    if loc=='greenhouse':
     for key in ['cloth','signal','pots','tools','watercan']:
      await q.object(key)
     await q.py('import renpy;s=renpy.store;s.r13_edit(period=2);renpy.exports.restart_interaction();result=True');await q.shot('greenhouse-reunion-evening')
    report['checks'].append(loc+': all calendar/branch sprite bounds fit; busiest fixture '+str(dense))
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True;await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await q.shot('mobile-altar-large');report['status']='passed-pending-visual-review'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='matrices'},ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
