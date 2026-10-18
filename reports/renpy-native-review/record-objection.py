import asyncio,json,time,subprocess,base64
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_meeting_objection',")
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/objection-review');OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=await b.new_context(viewport={'width':1280,'height':720});await c.add_init_script(path='/workspace/capture_game_audio.js');page=await c.new_page();q=ReviewQA(page,OUT)
  async def until(text=None,screen=None):
   for _ in range(50):
    st=await q.state()
    if text and text in st['say'] or screen and screen in st['screens']:return
    if 'say' in st['screens']:await q.input(810,610)
    else:await asyncio.sleep(.15)
   raise AssertionError(st)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E35","E09"],propositions=["C1"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.preferences.text_cps=0;s.preferences.afm_enable=False;s.persistent.room13_motion=True;s.r13_carriage_skip=False;result=True')
   await native_jump(q,'r13_trial');await until(screen='r13_meeting_agenda');await q.press('다람이의 방어가');await until(text='아이가 촛대로');await q.input(810,610);await q.input(810,610);await until(text='촛대는')
   await q.press('자료 보여주기');await q.wait('r13_book');label=await q.py('import renpy;s=renpy.store;result=s.R13_RECORD_SHORT.get("E35",s.r13_catalog_title("E35")[:8])');await q.press(label);await asyncio.sleep(.5)
   capture=await page.evaluate('window.__startGameCapture()');start=time.monotonic();await asyncio.sleep(1)
   await q.press('이 주장에 근거로 낸다');await asyncio.sleep(.25);await page.screenshot(path=str(OUT/'settled-hold.png'));await q.wait('say');await asyncio.sleep(1.2);await q.input(810,610)
   await asyncio.sleep(max(0,10-(time.monotonic()-start)));meta=await page.evaluate('window.__stopGameCapture()');raw=OUT/'actual.webm'
   with raw.open('wb') as f:
    for offset in range(0,meta['bytes'],500000):f.write(base64.b64decode(await page.evaluate('(n)=>window.__gameCaptureChunk(n)',offset)))
   subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-profile:v','baseline','-c:a','aac','-b:a','128k','-movflags','+faststart',str(OUT/'after.mp4')],check=True)
   (OUT/'capture.json').write_text(json.dumps(dict(capture=capture,media=meta,elapsed=time.monotonic()-start,fixture='day10/E35/E09/C1 only before recording; actual UI for objection',state=await q.state(),audio='Actual WebAudio capture, existing sfx-present.wav; no new voice'),ensure_ascii=False,indent=2));print('COMPLETE',flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:await b.close()
asyncio.run(main())
