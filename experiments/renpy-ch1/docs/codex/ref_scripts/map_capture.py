import asyncio,sys
sys.path.insert(0,'/home/claude/daaegame/experiments/renpy-ch1/dev')
from webqa import QA
from pathlib import Path
from playwright.async_api import async_playwright
URL='http://localhost:8766/'
OUT=Path('/tmp/claude-0/-home-claude/a6c0a1f6-b7da-5023-bdb2-55e6e15573c0/scratchpad/mapqa/out');OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  pg=await (await b.new_context(viewport={'width':1280,'height':720})).new_page();q=QA(pg,OUT)
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
  print('ver',await q.py('import renpy;result=renpy.config.version'))
  await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
  await q.press('처음부터')
  for i in range(400):
   st=await q.state()
   if 'r13_hub' in st['screens']:break
   if 'choice' in st['screens'] and any('편지를 접는다' in x['text'] for x in st['buttons']):
    await q.press('편지를 접는다');continue
   await q.input(640,300);await asyncio.sleep(.2)
  await asyncio.sleep(1.5)
  st=await q.state();lab=[x['text'] for x in st['buttons'] if '지도' in x['text']];print('btn',lab)
  await q.press(lab[0]);await q.wait('r13_map');await asyncio.sleep(1.2)
  await pg.screenshot(path=str(OUT/'01-open.png'))
  places=await q.py('import renpy;result=sorted(renpy.store.r13_places())');print('places',places)
  key='gate'
  x,y=await q.py('import renpy;result=renpy.store.r13_cart_point("village",%r)'%key)
  sc=await q.py('import renpy;v=renpy.exports.get_widget("r13_map","r13_map_view");result=[v.xadjustment.value,v.yadjustment.value] if v else None');print('view',sc,'pt',key,x,y)
  if sc:x,y=x-sc[0]+16,y-sc[1]
  await pg.mouse.move(x,y);await asyncio.sleep(.6);await pg.screenshot(path=str(OUT/'02-hover.png'))
  await pg.mouse.click(x,y);await asyncio.sleep(.6);await pg.screenshot(path=str(OUT/'03-picked.png'))
  print('scope',await q.py('import renpy;s=renpy.display.screen.get_screen("r13_map");result=None if not s else str(s.scope.get("selected"))'))
  await pg.mouse.move(1200,700);await asyncio.sleep(.5)
  # 캡처용: 모든 마을 장소를 열린 것으로 보고 솜이네를 고른 상태
  await q.py('import renpy;s=renpy.store;_o=s.r13_map_nodes;s.r13_map_nodes=lambda region,_o=_o,_n=s.R13_MAP_NODES:list(_n[region].items()) if region=="village" else _o(region);allp=set(s.R13_MAP_NODES["village"])|set(s.r13_places());renpy.exports.restart_interaction();s.r13_places=lambda *a,_p=allp,**k:_p;renpy.exports.restart_interaction();result=True')
  await asyncio.sleep(.8)
  await pg.mouse.move(1000,560);await pg.mouse.down();await pg.mouse.move(300,40,steps=25);await pg.mouse.up();await asyncio.sleep(.8)
  await pg.screenshot(path=str(OUT/'04-dragged.png'))
  for k,name in (('laundry','05-laundry-hover'),('somi','06-somi-picked')):
   sc=await q.py('import renpy;v=renpy.exports.get_widget("r13_map","r13_map_view");result=[v.xadjustment.value,v.yadjustment.value]')
   x,y=await q.py('import renpy;result=renpy.store.r13_cart_point("village",%r)'%k)
   x,y=x-sc[0]+16,y-sc[1];print(k,sc,x,y)
   await pg.mouse.move(x,y);await asyncio.sleep(.6)
   if k=='somi':await pg.mouse.click(x,y);await asyncio.sleep(.6)
   await pg.screenshot(path=str(OUT/(name+'.png')))
  print('scope',await q.py('import renpy;s=renpy.display.screen.get_screen("r13_map");result=str(s.scope.get("selected"))'))
  print('errs',errs)
  await b.close()
asyncio.run(main())
