import asyncio,sys
sys.path.insert(0,'/home/claude/daaegame/experiments/renpy-ch1/dev')
from webqa import QA
from pathlib import Path
from playwright.async_api import async_playwright
URL='http://localhost:8766/'
OUT=Path(__file__).parent/'out';OUT.mkdir(exist_ok=True)
async def run(mobile):
 tag='m' if mobile else 'd'
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  ctx=await (b.new_context(viewport={'width':844,'height':390},device_scale_factor=2,is_mobile=True,has_touch=True) if mobile else b.new_context(viewport={'width':1280,'height':720}))
  pg=await ctx.new_page();q=QA(pg,OUT);q.touch=mobile
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
  await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
  await q.press('처음부터')
  for i in range(400):
   st=await q.state()
   if 'r13_hub' in st['screens']:break
   if 'choice' in st['screens'] and any('편지를 접는다' in x['text'] for x in st['buttons']):
    await q.press('편지를 접는다');continue
   await q.input(640,300);await asyncio.sleep(.2)
  await asyncio.sleep(1)
  n=await q.py('import renpy\ns=renpy.store\nev=list(s.room13["evidence"])\nfor k in list(s.ROOM13["evidence"]):\n if k.startswith("V111:") and k not in ev:ev.append(k)\ns.r13_edit(evidence=ev)\nrenpy.exports.show_screen("r13_book")\nrenpy.exports.restart_interaction()\nresult=len(ev)')
  print(tag,'자료',n);await asyncio.sleep(1.5)
  await pg.screenshot(path=str(OUT/f'{tag}-book1.png'))
  # 이름이 가장 긴 자료 몇 개
  names=await q.py('import renpy\nst=renpy.store\nrows=[]\nfor k in st.room13["evidence"]:\n t=st.R13_RECORD_SHORT.get(k,"")\n rows.append((len(t),t))\nrows.sort(reverse=True)\nresult=rows[:8]')
  print(names)
  await q.py('import renpy\nrenpy.exports.hide_screen("r13_book")\nrenpy.exports.restart_interaction()\nresult=True');await asyncio.sleep(.8)
  for loc,per,name in (('v111_woodshed',1,'woodshed'),('v111_woodshed',2,'woodshed-eve'),('facility',1,'facility')):
   await q.py('import renpy\nrenpy.store.r13_edit(location=%r,period=%d)\nrenpy.exports.restart_interaction()\nresult=True'%(loc,per));await asyncio.sleep(1.5)
   await pg.screenshot(path=str(OUT/f'{tag}-{name}.png'))
  print(tag,'errs',errs)
  await b.close()
async def main():
 await run(False)
asyncio.run(main())
