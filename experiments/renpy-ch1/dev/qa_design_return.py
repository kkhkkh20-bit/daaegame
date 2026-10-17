"""Real scroll/cancel/reopen and read-only three-place visual contrast fixtures."""
import asyncio,base64,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-design-return'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=UIQA(page,OUT)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(evidence=list(s.ROOM13["evidence"]));s.persistent.room13_large_text=True;renpy.exports.show_screen("r13_book",target="buri");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_book')
   key=await q.py('import renpy;s=renpy.store;result=max((len(ev["establishes"]),key) for key,ev in s.ROOM13["evidence"].items())[1]')
   async def select(key):
    await q.py('import renpy;s=renpy.store;sc=renpy.display.screen.get_screen("r13_book");entries=sc.scope["entries"];renpy.exports.set_screen_variable("page",entries.index('+repr(key)+')//s.r13_record_page_size(),screen="r13_book");renpy.exports.set_screen_variable("detail",'+repr(key)+',screen="r13_book");renpy.exports.restart_interaction();result=True');await asyncio.sleep(1)
   async def offset():return await q.py('import renpy;w=renpy.exports.get_widget("r13_book","r13_material_scroll");result={"value":w.yadjustment.value,"range":w.yadjustment.range}')
   await select(key);await page.mouse.move(1000,400);await page.mouse.wheel(0,500);await asyncio.sleep(.7)
   scrolled=await offset();assert scrolled['value']>0,scrolled
   before=(await q.state())['room'];await q.shot('01-reading-position')
   other=await q.py('import renpy;result=next(k for k in renpy.store.room13["evidence"] if k!='+repr(key)+')')
   await select(other);assert (await offset())['value']==0
   await select(key);assert abs((await offset())['value']-scrolled['value'])<=1, {'actual':await offset(),'expected':scrolled,'memory':await q.py('import renpy;result=repr(renpy.store.r13_record_scrolls)'),'detail':await q.py('import renpy;result=renpy.display.screen.get_screen("r13_book").scope["detail"]')}
   await q.press('닫기');await q.wait('r13_hub')
   await q.py('import renpy;renpy.exports.show_screen("r13_book",target="buri");renpy.exports.restart_interaction();result=True');await q.wait('r13_book')
   assert abs((await offset())['value']-scrolled['value'])<=1, {'actual':await offset(),'expected':scrolled,'memory':await q.py('import renpy;result=repr(renpy.store.r13_record_scrolls)'),'detail':await q.py('import renpy;result=renpy.display.screen.get_screen("r13_book").scope["detail"]')}
   await q.shot('02-reading-restored')
   # The newly selected other record may be marked seen. Scrolling/closing
   # must not change evidence, clock, or other story state.
   after=(await q.state())['room'];assert {k:v for k,v in before.items() if k!='record_ui'}=={k:v for k,v in after.items() if k!='record_ui'}
   await q.press('닫기')
   await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;renpy.exports.show_screen("r13_records");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_records');await q.press('다음 ›');await q.input(340,200)
   record_view=await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result=[sc.scope[k] for k in ("tab","detail","page")]')
   await q.press('닫기');await q.py('import renpy;renpy.exports.show_screen("r13_records");renpy.exports.restart_interaction();result=True');await q.wait('r13_records')
   assert await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result=[sc.scope[k] for k in ("tab","detail","page")]')==record_view
   await q.press('닫기')
   # These are explicit scene fixtures. No campaign gates are exercised here.
   setup='\n'.join(['import renpy','def _qa_contrast(**kwargs):',' s=renpy.store',' renpy.ui.add(s.Crop((s.r13_world_offset(),0,1280,720),s.r13_world_background(s.room13["location"],"afternoon")))',"renpy.exports.define_screen('qa_contrast',_qa_contrast,modal='True',zorder='250')","result=True"])
   await q.py(setup)
   for location in ('inn','hall','room13'):
    for case in ('pending','occurred'):
     await q.py('import renpy;s=renpy.store;s.r13_edit(location='+repr(location)+',case_state='+repr(case)+',period=1);s.persistent.room13_motion=False;renpy.exports.show_screen("qa_contrast");renpy.exports.restart_interaction();result=True')
     await asyncio.sleep(.6);await q.shot(location+'-'+case)
     original=(await q.state())['room']
     await q.py('import renpy;s=renpy.store;s.r13_world_background('+repr(location)+',"afternoon");s.r13_world_background('+repr(location)+',"afternoon");result=True')
     assert (await q.state())['room']==original
   # A contact sheet of actual renderer captures, without repainting the art.
   board=await b.new_page(viewport={'width':1280,'height':1185},device_scale_factor=1)
   cards=[]
   for loc,label in [('inn','여관 접수대'),('hall','2층 복도'),('room13','13호실')]:
    for case,caption in [('pending','사건 전'),('occurred','사건 후')]:
     data=base64.b64encode((OUT/(loc+'-'+case+'.png')).read_bytes()).decode()
     cards.append('<figure><figcaption>'+label+' · '+caption+'</figcaption><img src="data:image/png;base64,'+data+'"></figure>')
   await board.set_content('<html><meta charset="utf-8"><style>body{margin:0;padding:20px;background:#18202c;color:#eee5d3;font:20px sans-serif}h1{font-size:24px;margin:0 0 14px}main{display:grid;grid-template-columns:1fr 1fr;gap:14px}figure{margin:0}figcaption{margin-bottom:6px}img{width:100%;display:block}</style><h1>장면 대비 · 실제 게임 렌더 비교</h1><main>'+''.join(cards)+'</main></html>')
   await board.screenshot(path=str(OUT/'contrast-board.png'),full_page=True);await board.close()
   result=dict(passed=True,record=key,scroll=scrolled,checks=['real wheel scroll restored after record switch and close/reopen','separate offsets per material','record tab/selection/page restored','no evidence clock or story state changed by UI','three authored interiors before/after render','reduced motion keeps static contrast'])
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('PASS',result,flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await b.close()
asyncio.run(main())
