"""웹 빌드에서 제거한 히트음 경로와 실제 하차 상태를 확인한다."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_novel_adaptation import until

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/retired-hit-web'))
OUT.mkdir(parents=True,exist_ok=True)

async def run(q,code):
 return await q.py('ns={};exec('+repr(code)+',ns);result=ns["result"]')

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  q=SayQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
   await q.wait('main_menu')
   paths=await run(q,'''import renpy
import renpy.audio.music as music
s=renpy.store
calls=[]
original=music.play
try:
 music.play=lambda *a,**kw:calls.append([a,kw])
 for key in ('impact','cut9','present'):
  s.source_fx(key)
 s.r13_impact('jolt')
 retired=list(calls)
 s.source_fx('right')
 s.source_fx('wrong')
finally:
 music.play=original
data=renpy.exports.file('assets/sfx-present.wav').read()
result=dict(version=s.config.version,retired=retired,remaining=calls,silent_wav=data[:4]==b'RIFF' and data[8:12]==b'WAVE' and not any(data[44:]),maps={k:s.r13_fx_path(k) for k in ('impact','cut9','present')})''')
   assert paths['retired']==[],paths
   assert paths['silent_wav'] and all(v is None for v in paths['maps'].values()),paths
   assert [c[0][0] for c in paths['remaining']]==['assets/sfx-right.wav','assets/sfx-wrong.wav'],paths
   print('웹 효과음 연결 확인',flush=True)
   await run(q,'import renpy;renpy.store.preferences.text_cps=0;result=True')
   await q.press('처음부터')
   await until(q,text='일곱 개에서')
   await q.press('건너뛰기')
   await until(q,text='혼자 내려갈')
   channels=await run(q,'import renpy.audio.music as music;result={c:music.get_playing(channel=c) for c in ("carriage_ride","carriage_hooves","scene_fx","sound")}')
   assert all(v is None for v in channels.values()),channels
   await page.screenshot(path=str(OUT/'하차_PC.png'))
   await page.set_viewport_size({'width':844,'height':390})
   await page.screenshot(path=str(OUT/'하차_휴대폰.png'))
   assert not errors,errors
   report=dict(status='통과',paths=paths,channels=channels,pageerrors=errors)
   (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
   print(json.dumps(report,ensure_ascii=False),flush=True)
  finally:
   await browser.close()

if __name__=='__main__':asyncio.run(main())
