"""Explicit layout fixtures for five scenes; no claims of natural campaign completion."""
import asyncio,json,shutil,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from pixel_qa_ui0156 import UIQA
OUT=Path('/workspace/room13-review/world0177');OUT.mkdir(exist_ok=True)
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
 report={'kind':'Explicit location/daylight layout fixtures, physical pan and object center clicks; no natural campaign claim','archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=Q(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   # End the entry-only screen through a context-local visual fixture, not by proving story facts.
   await q.py("import renpy;s=renpy.store;w=renpy.exports.get_widget('r13_hub','r13_options_gear');w.action=s.Jump('r13_field');w.clicked=w.action;result=True");await q.input(1220,50);await q.wait('r13_hub')
   for loc in PLACES:
    for period in (0,1,2):
     await q.py('import renpy;s=renpy.store;s.r13_edit(day=3,period='+str(period)+',location='+repr(loc)+');s.r13_upgrade();s.place=s.R13_PLACES[s.room13[\"location\"]][0];renpy.exports.scene();renpy.exports.show(\"qa_world_bg\",what=s.r13_background(s.R13_PLACES[s.room13[\"location\"]][1]));w=renpy.exports.get_widget(\"r13_hub\",\"r13_options_gear\");w.action=s.Jump(\"r13_field\");w.clicked=w.action;result=True');await q.input(1220,50);await q.wait('r13_hub');assert (await q.camera())['width']==1920
     before=await q.room();await q.pan(False);await q.shot(loc+'-'+str(period)+'-left');await q.pan(True);await q.shot(loc+'-'+str(period)+'-right');assert await q.room()==before
     if period==1:
      keys=await q.py('import renpy;s=renpy.store;result=list(s.ROOM13["objects"][s.room13["location"]])')
      for key in keys:
       clock=[(await q.room())[k] for k in ['day','period']];await q.object(key);assert clock==[(await q.room())[k] for k in ['day','period']]
      await q.shot(loc+'-clicked-objects');report['checks'].append(loc+': every original object key physically clicked; no time cost')
    report['checks'].append(loc+': morning/afternoon/evening and both camera edges, pan preserves state')
   # Geometry matrix reads actual schedules on all days and periods; resets full state afterwards.
   matrix=await q.py('''import renpy,copy
s=renpy.store;original=copy.deepcopy(s.room13);rows=[];bad=[]
for loc in ['clinic','store','greenhouse','facility','altar']:
 for day in range(1,15):
  for period in range(3):
   s.r13_edit(location=loc,day=day,period=period)
   actors=s.r13_stage_people()
   for a in actors:
    if a['x']<0 or a['y']<0 or a['x']+a['width']>1920 or a['y']+a['height']>720:bad.append(dict(location=loc,day=day,period=period,actor=a))
   rows.append(dict(location=loc,day=day,period=period,count=len(actors)))
s.room13=original;s.R13_STAGE_CACHE.clear();renpy.exports.restart_interaction();result=dict(rows=rows,bad=bad)''')
   (OUT/'geometry-matrix.json').write_text(json.dumps(matrix,ensure_ascii=False,indent=2));assert not matrix['bad'],matrix['bad'][:3]
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True;await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await q.shot('mobile-altar-large');report['checks'].append('210 real schedule/period layout combinations have no clipped sprite bounds; mobile large text capture')
   report['status']='passed-pending-visual-review'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
