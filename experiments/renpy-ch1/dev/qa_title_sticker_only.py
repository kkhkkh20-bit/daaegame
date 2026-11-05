"""실제 웹 로딩·메인에서 왼쪽 지도 제거와 PC·휴대폰 메뉴를 확인한다."""
import asyncio,json,os
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
from webqa import SayQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/title-sticker-web'));OUT.mkdir(parents=True,exist_ok=True)

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  release=asyncio.Event()
  async def hold(route):
   await release.wait();await route.continue_()
  await page.route('**/renpy.wasm*',hold)
  q=SayQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'),wait_until='domcontentloaded')
   await page.wait_for_function("document.getElementById('presplash') && document.getElementById('presplash').complete && document.getElementById('presplash').naturalWidth>0")
   src=await page.locator('#presplash').get_attribute('src')
   assert 'loading-scene.webp?v=' in src,src
   await page.screenshot(path=str(OUT/'로딩_PC.png'))
   with Image.open(OUT/'로딩_PC.png') as im:
    pixel=im.convert('RGB').getpixel((300,400))
   assert max(abs(a-b) for a,b in zip(pixel,(10,34,82)))<6,pixel
   await page.set_viewport_size({'width':844,'height':390});await page.screenshot(path=str(OUT/'로딩_휴대폰.png'))
   await page.set_viewport_size({'width':1280,'height':720});release.set()
   await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
   await q.wait('main_menu');await asyncio.sleep(1)
   await page.screenshot(path=str(OUT/'메인_PC.png'))
   st=await q.state()
   assert any('처음부터' in b['text'] for b in st['buttons']),st
   await q.press('설정');await q.wait('pause_menu');await q.press('닫기');await q.wait('main_menu')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await page.screenshot(path=str(OUT/'메인_휴대폰.png'))
   await q.press('설정');await q.wait('pause_menu');await q.press('닫기');await q.wait('main_menu')
   assert not errors,errors
   version=await q.py('import renpy;result=renpy.store.config.version')
   report=dict(status='통과',version=version,loader_src=src,left_background_pixel=pixel,checks=['PC·휴대폰 실제 로딩과 메인 캡처','왼쪽 마을 제거','설정 열기·닫기와 터치 복귀'],pageerrors=errors)
   (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True)
  finally:
   release.set();await browser.close()

if __name__=='__main__':asyncio.run(main())
