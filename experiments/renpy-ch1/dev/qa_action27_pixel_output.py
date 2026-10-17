"""Observe existing output sampling at native and fractional viewport sizes; no renderer changes."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/action27-pixel-output');OUT.mkdir(exist_ok=True)
async def main():
 report={}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720},device_scale_factor=1);q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5);await setup(q,2,'market',flags=['ev_g_done'])
   await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,market=700);result=True');await native_jump(q,'r13_field');await q.wait('r13_hub')
   report['source']=await q.py('import renpy;s=renpy.store;a=next(a for a in s.r13_stage_people() if a["person"]=="resident_eunho");sp=s.R13_ACTING[a["person"]][a["pose"]];result=dict(actor=a,face=s.r13_actor_face(a,0),crop=sp["crop"],source_to_actor_y=a["height"]/float(sp["crop"][3]),native_detail=sp.get("native_detail",False),grid=s.R13_WORLD_PIXEL_GRID,version=s.config.version)')
   report['captures']=[]
   for label,w,h,offset in [('native',1280,720,700),('native-pan',1280,720,702),('fractional',1024,576,700)]:
    await page.set_viewport_size({'width':w,'height':h});await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,market='+str(offset)+');renpy.exports.restart_interaction();result=True');await native_jump(q,'r13_field');await q.wait('r13_hub');await asyncio.sleep(.3)
    # Native camera output is snapped by its existing getter, not a new test renderer.
    actual=await q.py('import renpy;result=renpy.store.r13_world_offset()')
    canvas=await page.locator('canvas').evaluate_all('(els)=>els.map(e=>({width:e.width,height:e.height,rect:{x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height},imageRendering:getComputedStyle(e).imageRendering}))')
    await page.screenshot(path=str(OUT/(label+'.png')));report['captures'].append(dict(label=label,viewport=[w,h],offset=actual,canvas=canvas))
   report['status']='observed';(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  finally:await b.close()
if __name__=='__main__':asyncio.run(main())
