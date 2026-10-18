"""Verify one shared settings edit propagates to actual rendered controls."""
import asyncio,json,os,sys
from pathlib import Path
sys.path.insert(0,'dev')
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-control-tokens'))
class Q(UIQA):
 async def py(self,code):return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)
async def main():
 OUT.mkdir(parents=True,exist_ok=True);report={'checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720});q=Q(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://localhost:8776/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000);await q.wait('main_menu')
   await q.py('import renpy;s=renpy.store;s._qa_control_before=dict(s.R13_CONTROL);s.persistent.room13_large_text=False;renpy.exports.show_screen("r13_control_specimen");renpy.exports.restart_interaction();result=True')
   async def check(name,width,gap,height):
    await asyncio.sleep(.5);st=await q.state();buttons=sorted([x for x in st['buttons'] if x['rect'][1]>=600],key=lambda x:x['rect'][0]);assert len(buttons)==5,buttons
    for i,bt in enumerate(buttons):assert bt['rect']==[28+i*(width+gap),704-height,width,height],bt
    await q.shot(name);report['checks'].append({'name':name,'rects':[bt['rect'] for bt in buttons]})
   await check('default',232,16,64)
   await q.py('import renpy;renpy.store.R13_CONTROL.update(width=224,gap=20,height=70,large_height=96,padding=20);renpy.exports.restart_interaction();result=True')
   await check('single-settings-edit',224,20,70)
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   await check('large-text-settings',224,20,96)
   await q.py('import renpy;s=renpy.store;s.R13_CONTROL.clear();s.R13_CONTROL.update(s._qa_control_before);s.persistent.room13_large_text=False;renpy.exports.restart_interaction();result=True')
   await check('restored',232,16,64);report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
