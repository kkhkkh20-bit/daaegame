"""Compiled release renderer only: explicit scene fixtures, no source/data overlays."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
from qa_design_restore import FIELD
OUT=Path('/workspace/work/ms14/design74-browser');OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  pg=await b.new_page(viewport={'width':1280,'height':720});q=UIQA(pg,OUT);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8766/preview/room13-dev/'),wait_until='domcontentloaded',timeout=180000)
  await pg.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await asyncio.sleep(12);await q.input(1100,600);await q.wait('main_menu')
  report={'kind':'Rebuilt release; state fixtures only, no Python/data overlays. Actual dispatcher inputs separately covered by native tests.'}
  for name,state in [('inn',dict(day=2,period=0,location='inn',life_poc=True)),('piko',dict(day=2,period=0,location='square',life_poc=True,offers={'r13_w1c_portrait':dict(day=2,period=0,location='square')}))]:
   rows=await q.py('state='+repr(state)+'\n'+FIELD.replace('s.r13_world_cameras={}',"s.r13_world_cameras={state['location']:0}"))
   for _ in range(50):
    busy=await q.py('import renpy;result=len(renpy.webloader.queue)')
    if not busy:break
    await asyncio.sleep(.2)
   await asyncio.sleep(1);await q.shot(name+'-release')
   if name=='piko':assert any(r['person']=='resident_piko' for r in rows),rows
   report[name]=rows
  assert not errors,errors;report.update(status='passed',page_errors=errors)
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
asyncio.run(main())
