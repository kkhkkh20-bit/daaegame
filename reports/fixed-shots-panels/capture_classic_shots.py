import asyncio,json,time,subprocess,base64
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/daaegame-reactions/reports/fixed-shots-panels');OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  c=await b.new_context(viewport={'width':1280,'height':720});await c.add_init_script(path='/workspace/capture_game_audio.js');page=await c.new_page();q=ReviewQA(page,OUT)
  await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
  await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E35","E09"],propositions=["C1"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.preferences.text_cps=0;s.preferences.afm_enable=False;s.persistent.room13_motion=True;s.r13_carriage_skip=False;s.r13_shot_review_enabled=True;s.r13_shot_review_mode="A";s.r13_shot_review_manual_phase=0;result=True')
  for mode in ('1','2','3'):
   phase=1 if mode=='2' else 2
   await q.py('import renpy;s=renpy.store;s.r13_shot_review_mode='+repr(mode)+';s.r13_shot_review_manual_phase='+str(phase)+';renpy.exports.hide_screen("r13_shot_review_screen");result=True');await native_jump(q,'r13_shot_review');await asyncio.sleep(1);await q.state();await page.screenshot(path=str(OUT/(mode+'.png')))
   await q.py('import renpy;renpy.store.r13_shot_review_manual_phase=None;renpy.exports.hide_screen("r13_shot_review_screen");result=True');await native_jump(q,'r13_shot_review')
   cap=await page.evaluate('window.__startGameCapture()');await asyncio.sleep(15.0);meta=await page.evaluate('window.__stopGameCapture()');state=await q.state();raw=Path('/workspace')/('fixed-'+mode+'.webm')
   with raw.open('wb') as f:
    for offset in range(0,meta['bytes'],500000):f.write(base64.b64decode(await page.evaluate('(n)=>window.__gameCaptureChunk(n)',offset)))
   subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-profile:v','baseline','-c:a','aac','-b:a','128k','-movflags','+faststart',str(OUT/(mode+'.mp4'))],check=True)
   (OUT/(mode+'.json')).write_text(json.dumps(dict(capture=cap,media=meta,state=state),ensure_ascii=False,indent=2));print('VIDEO '+mode,flush=True)
  await b.close()
asyncio.run(main())
