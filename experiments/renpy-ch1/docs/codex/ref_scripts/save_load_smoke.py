import asyncio,sys,json
sys.path.insert(0,'/home/claude/daaegame/experiments/renpy-ch1/dev')
from webqa import QA
from pathlib import Path
from playwright.async_api import async_playwright
URL='http://localhost:8766/'
OUT=Path('/tmp/claude-0/-home-claude/a6c0a1f6-b7da-5023-bdb2-55e6e15573c0/scratchpad/smoke/out');OUT.mkdir(exist_ok=True)
async def run(mobile):
 tag='m' if mobile else 'd'
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  if mobile:ctx=await b.new_context(viewport={'width':844,'height':390},device_scale_factor=2,is_mobile=True,has_touch=True)
  else:ctx=await b.new_context(viewport={'width':1280,'height':720})
  pg=await ctx.new_page();q=QA(pg,OUT);q.touch=mobile
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
  ver=await q.py('import renpy;result=renpy.config.version')
  await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
  await q.press('처음부터')
  for i in range(400):
   st=await q.state()
   if 'r13_hub' in st['screens']:break
   if 'choice' in st['screens'] and any('편지를 접는다' in x['text'] for x in st['buttons']):
    await q.press('편지를 접는다');continue
   await q.input(640,300);await asyncio.sleep(.2)
  await asyncio.sleep(1.5);await pg.screenshot(path=str(OUT/f'{tag}-field.png'))
  before=await q.py('import renpy;s=renpy.store;result=dict(day=s.room13["day"],loc=s.room13["location"],scene=s.room13["v111"].get("scene"),ev=sorted(s.room13["evidence"]))')
  await q.press('보리');await asyncio.sleep(1.5)
  await q.press('더보기');await asyncio.sleep(1.2)
  await pg.screenshot(path=str(OUT/f'{tag}-more.png'))
  await q.press('저장 · 불러오기')
  await q.wait('save')
  await q.press('1쪽 1번');await asyncio.sleep(1.5)
  st=await q.state()
  if 'confirm' in st['screens']:await q.press('예');await asyncio.sleep(1)
  await pg.screenshot(path=str(OUT/f'{tag}-saved.png'))
  ok=await q.py('import renpy;result=renpy.exports.can_load("1-1")')
  await asyncio.sleep(3)
  await pg.reload();await pg.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
  await q.press('불러오기');await q.wait('load')
  await q.press('1쪽 1번');await asyncio.sleep(1)
  st=await q.state()
  if 'confirm' in st['screens']:await q.press('예')
  for _ in range(60):
   st=await q.state()
   if 'say' in st['screens'] or 'r13_hub' in st['screens']:break
   await asyncio.sleep(1)
  print(tag,'loaded screens',st['screens'])
  await asyncio.sleep(2)
  after=await q.py('import renpy;s=renpy.store;result=dict(day=s.room13["day"],loc=s.room13["location"],scene=s.room13["v111"].get("scene"),ev=sorted(s.room13["evidence"]))')
  await pg.screenshot(path=str(OUT/f'{tag}-loaded.png'))
  print(tag,'version',ver,'saved',ok,'same',before==after,before,'errors',errs[:3])
  await b.close()
async def main():
 for m in (False,True):await run(m)
asyncio.run(main())
