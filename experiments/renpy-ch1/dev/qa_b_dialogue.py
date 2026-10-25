"""B dialogue and map surfaces on a disposable browser profile; no save writes."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/r13-b-browser'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True)
  q=UIQA(page,OUT);errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  try:
   await page.goto(URL)
   await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=150000)
   await q.wait('main_menu');await q.press('처음부터');await q.wait('say')
   await q.py('''import renpy
s=renpy.store
s.r13_edit(day=2,period=0,location="inn",flags=["lodging","entry_corrected"])
s.r13_black_card=False
s.r13_thought_active=False
s.r13_camera="stage"
s.place="여관 · 접수대"
s.preferences.text_cps=0
s.r13_packet=("granny","잘 왔구나. 여기 앉아서 천천히 이야기하자.")
s.r13_directed_pose="joy"
s.r13_expression="expressive"
renpy.exports.scene()
renpy.exports.show("qa_background",what=s.r13_background(s.R13_PLACES["inn"][1]))
s.r13_speaker("granny","expressive","joy")
renpy.exports.show_screen("say",who=s.R13_NAMES["granny"],what=s.r13_packet[1])
renpy.exports.restart_interaction()
result=True''')
   levels=await q.py('import renpy;s=renpy.store;old=s.persistent.room13_window_alpha;values=[]\nfor value in ("99","d4","f5"):\n s.persistent.room13_window_alpha=value;values.append(s.r13_night_shade_alpha())\ns.persistent.room13_window_alpha=old;result=values')
   assert levels[0]<levels[1]<levels[2],levels
   await asyncio.sleep(2)
   assert await q.py('result=renpy.store.r13_bdialogue_face("granny","joy") is not None')
   await q.shot('dialogue-desktop')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('renpy.store.r13_set_text_size("large");renpy.exports.restart_interaction();result=True')
   await q.shot('dialogue-mobile-large')
   await q.press('더보기');await q.press('설정');await q.wait('pause_menu');await q.shot('dialogue-settings')
   await q.press('읽기');await q.shot('settings-reading-mobile-large')
   tab=next(b for b in (await q.state())['buttons'] if b['text'].strip()=='화면')
   x,y,w,h=tab['rect'];await q.input(x+w/2,y+h/2);await q.shot('settings-display-mobile-large')
   await q.press('닫기');await q.wait('say')
   await q.py('renpy.store.room13.pop("v111",None);renpy.exports.hide_screen("r13_more_tools");renpy.exports.show_screen("r13_map",initial_region="inn");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_map');await q.shot('map-inn-mobile')
   assert await q.py('result="passage" not in dict(renpy.store.r13_bmap_places("inn"))')
   await q.press('숲·산길');await q.shot('map-forest-mobile')
   assert await q.py('result=all(k not in dict(renpy.store.r13_bmap_places("mountain")) for k in ("altar","greenhouse"))')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.press('마을');await q.shot('map-village-desktop')
   assert not errors,errors
   info={'passed':True,'version':(await q.info())['version'],'checks':['B dialogue body and matching face','large touch dialogue','more/settings/return','inn and forest mobile maps','hidden destinations absent','village map preserved'],'pageerrors':errors}
   (OUT/'result.json').write_text(json.dumps(info,ensure_ascii=False,indent=2));print('PASS',info,flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:await browser.close()
if __name__=='__main__':asyncio.run(main())
