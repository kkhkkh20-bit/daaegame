"""844×390 실제 웹 터치에서 조사 공간과 상단 도구를 확인한다."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_carriage import IntroQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/field-clear-web'));OUT.mkdir(parents=True,exist_ok=True)
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':844,'height':390},has_touch=True)
  q=IntroQA(page,OUT);q.touch=True;errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await page.goto(os.environ['ROOM13_URL']);await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=150000)
   await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.wait('say');await q.press('건너뛰기');await q.advance_to('r13_hub');await q.shot('field-mobile')
   await q.press('기록');await q.wait('r13_records');await q.py('renpy.hide_screen("r13_records");renpy.restart_interaction();result=True')
   await q.press('생각');assert await q.py('result=renpy.store.r13_goal_open');await q.shot('thought-mobile');await q.press('접기')
   assert not await q.py('result=renpy.store.r13_goal_open')
   await q.press('돌목');assert 'r13_hub' not in (await q.state())['screens'];await q.shot('person-mobile')
   assert not errors,errors
   (OUT/'result.json').write_text(json.dumps(dict(passed=True,version=(await q.info())['version'],checks=['actual newgame gate','records touch','thought open/close','guard interaction'],pageerrors=errors),ensure_ascii=False,indent=2))
   print('PASS',flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:await browser.close()
if __name__=='__main__':asyncio.run(main())
