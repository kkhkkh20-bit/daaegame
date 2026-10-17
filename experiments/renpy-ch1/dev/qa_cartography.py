"""Actual mouse/touch map selection, secret image gating and travel on web build."""
import asyncio,json,os,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/map6-browser'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True);q=UIQA(page,OUT);checks=[]
  async def scope():return await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_map");result=[sc.scope["region"],sc.scope["selected"]]')
  async def point(region,key):return await q.py('import renpy;result=renpy.store.r13_cart_point('+repr(region)+','+repr(key)+')')
  async def opened(region):
   await q.press('지도 · 이동');await q.wait('r13_map')
   if (await scope())[0]!=region:
    await q.press({'village':'마을','inn':'여관 안','mountain':'숲·산길'}[region])
  async def close():
   await q.press('현장으로 돌아가기');await asyncio.sleep(.7)
   assert not await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map") is not None')
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say');await q.press('대사 건너뛰기');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=3,period=0,location="square",flags=["entry_corrected","lodging"]);s.r13_upgrade()\ndef f(**kw):renpy.ui.timer(.2,action=[renpy.store.Hide("qa_jump"),renpy.store.Jump("r13_field")])\nrenpy.display.screen.define_screen("qa_jump",f,zorder="200")\nrenpy.exports.show_screen("qa_jump");renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(2);await q.wait('r13_hub');await q.press('지도 · 이동');await q.wait('r13_map');before=await q.room()
   keys=await q.py('import renpy;result=[k for k,p in renpy.store.r13_map_nodes("village")]');assert len(keys)==11,keys
   for key in keys:
    x,y=await point('village',key);await q.input(x,y);assert (await scope())==['village',key],(key,await scope());assert await q.room()==before
   for key in keys:
    x,y=await q.py('import renpy;result=renpy.store.r13_cart_label_point('+repr(key)+')')
    await q.input(x,y);assert (await scope())==['village',key];assert await q.room()==before
   x,y=await point('village','inn');await q.input(x,y)
   checks.append('All 11 handwritten name targets select their own destination without travel')
   await q.shot('01-village');checks.append('All 11 building/terrain polygons select exact place without state/time changes')
   # Empty corner of the inn rectangle must not steal a neighbouring click.
   x,y=await point('village','post');await q.input(x,y);await q.input(47,240);assert (await scope())[1]=='post'
   x,y=await q.py('import renpy;result=renpy.store.r13_cart_label_point("school")');await page.mouse.move(x,y);await asyncio.sleep(.4)
   assert (await scope())[1]=='post'
   assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["map_hover"]')=='school'
   await q.shot('02-village-hover');checks.append('Hovering a handwritten name changes only focus, retaining selected destination')
   await q.press('여관 안');assert (await scope())[0]=='inn';await q.shot('03-inn-text')
   assert not await q.py('import renpy;result=any(k in dict(renpy.store.r13_map_nodes("inn")) for k in ("passage","ancient","guestroom"))')
   await q.press('숲·산길');await q.shot('04-mountain-hidden');assert not await q.py('import renpy;result=renpy.store.r13_cart_cover_visible("altar") or renpy.store.r13_cart_cover_visible("greenhouse")')
   assert await q.room()==before;await close();checks.append('Inn text list excludes unknown rooms; no floor plan; unknown greenhouse and altar images absent')
   # Mobile touch selects every building, including repeated taps, without travel.
   await page.set_viewport_size({'width':844,'height':390});q.touch=True;await opened('village');before=await q.room()
   for key in keys:
    x,y=await point('village',key);await q.input(x,y);await q.input(x,y);assert (await scope())[1]==key;assert await q.room()==before
   x,y=await point('village','inn');await q.input(x,y)
   await q.shot('05-village-mobile');await q.press('여관 안');await q.shot('06-inn-mobile');await close();checks.append('844x390 real touch: all 11 targets, repeated tap never travels, cancel preserves full state')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="inn");renpy.exports.show_screen("r13_inn_guide");renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(.8)
   assert await q.py('import renpy;result=renpy.exports.get_widget("r13_inn_guide","map_room_inn") is not None')
   await page.keyboard.press('Escape');await asyncio.sleep(.6)
   assert not await q.py('import renpy;result=renpy.display.screen.get_screen("r13_inn_guide") is not None')
   checks.append('Legacy inn guide opens shared gated text list and Escape dismisses it')
   # Authored discovery gates remain in charge, including restored stale location.
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=9,period=0,location="ancient",week2_started=True,passage_open=True,case_state="occurred");s.r13_flag("ancient_found");renpy.exports.restart_interaction();result=True')
   await opened('inn');assert (await scope())==['inn','ancient'];await q.shot('07-underground');await close()
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=14,period=0,location="altar",finale_started=True,evidence=["E19"],week2_started=True);renpy.exports.restart_interaction();result=True')
   await opened('mountain');assert await q.py('import renpy;result=renpy.store.r13_cart_cover_visible("altar") and renpy.store.r13_cart_cover_visible("greenhouse")');before=await q.room()
   for key in ('forest','facility','greenhouse','altar'):
    x,y=await point('mountain',key);await q.input(x,y);assert (await scope())[1]==key,(key,await scope());assert await q.room()==before
   await q.shot('08-mountain-discovered');await close();checks.append('Existing gates reveal greenhouse/altar artwork and targets; ancient remains under inn')
   # Confirm actual Return destination through the field's map dispatcher.
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=3,period=0,location="square",finale_started=False);renpy.exports.restart_interaction();result=True')
   await q.press('지도 · 이동');await q.wait('r13_map');x,y=await point('village','post');await q.input(x,y);await q.press('이곳으로 이동');await asyncio.sleep(1)
   assert (await q.room())['location']=='post';checks.append('Explicit footer confirmation dispatches actual travel to post office')
   transport=json.load(urllib.request.urlopen(URL+'game-transport.json'));result={'passed':True,'checks':checks,'archive_sha256':transport['archive_sha256'],'transport_parts':len(transport['parts'])};(OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('PASS',result,flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await browser.close()
if __name__ == "__main__":asyncio.run(main())
