import asyncio,json,time,subprocess,base64,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/b038-review');OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  for mode in os.environ.get('ABC_MODES','ABC'):
   b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
   c=await b.new_context(viewport={'width':1280,'height':720});await c.add_init_script(path='/workspace/capture_game_audio.js');page=await c.new_page();q=ReviewQA(page,OUT)
   try:
    await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
    await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E35","E09"],propositions=["C1"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.preferences.text_cps=0;s.preferences.afm_enable=False;s.persistent.room13_motion=True;s.r13_carriage_skip=False;s.r13_effect_review_enabled=True;s.r13_effect_review_mode='+repr(mode)+';result=True')
    await native_jump(q,'r13_effect_review')
    await asyncio.sleep(7)
    await q.py('import renpy;renpy.exports.hide_screen("r13_effect_review_screen");renpy.exports.restart_interaction();result=True')
    await native_jump(q,'r13_effect_review')
    capture=await page.evaluate('window.__startGameCapture()');start=time.monotonic()
    await asyncio.sleep(7)
    await page.screenshot(path=str(OUT/(mode+'-hold.png')))
    await asyncio.sleep(max(0,10.5-(time.monotonic()-start)))
    meta=await page.evaluate('window.__stopGameCapture()');raw=OUT/(mode+'.webm')
    await page.screenshot(path=str(OUT/'before-click.png'))
    await q.input(810,610);await asyncio.sleep(.5)
    await page.screenshot(path=str(OUT/'after-click.png'))
    with raw.open('wb') as f:
     for offset in range(0,meta['bytes'],500000):f.write(base64.b64decode(await page.evaluate('(n)=>window.__gameCaptureChunk(n)',offset)))
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-profile:v','baseline','-c:a','aac','-b:a','128k','-movflags','+faststart',str(OUT/(mode+'.mp4'))],check=True)
    (OUT/(mode+'.json')).write_text(json.dumps(dict(mode=mode,capture=capture,media=meta,state=await q.state(),audio='Actual WebAudio capture, council original at .65 channel gain, same fresh context per candidate; no new voice'),ensure_ascii=False,indent=2));print('COMPLETE '+mode,flush=True)
   except Exception:
    await page.screenshot(path=str(OUT/(mode+'-failure.png')));raise
   finally:await b.close()
asyncio.run(main())
