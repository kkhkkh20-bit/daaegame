import asyncio,json,time,subprocess,base64,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/actor-trail-review');OUT.mkdir(exist_ok=True)
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
    route=await q.py('import renpy;s=renpy.store;w=renpy.display.screen.get_displayable("r13_effect_review_screen","effect_review");result=[dict(arrival=e.arrival,passing=e.passing) for e in w.effects[1:]]')
    await q.py('import renpy;s=renpy.store;s.r13_effect_review_manual=True;s.r13_effect_review_phase=0;s.r13_effect_review_started=renpy.display.core.get_time();renpy.exports.restart_interaction();result=True')
    click_start=time.monotonic();await page.mouse.click(810,610);await asyncio.sleep(.08);await page.mouse.click(810,610);click_interval=time.monotonic()-click_start;await asyncio.sleep(.10)
    rapid=await q.py('import renpy;s=renpy.store;result=dict(phase=s.r13_effect_review_phase,elapsed=renpy.display.core.get_time()-s.r13_effect_review_started)')
    assert rapid['phase']==2,rapid
    await asyncio.sleep(.5);await page.screenshot(path=str(OUT/'rapid-settled.png'))
    await q.py('import renpy;s=renpy.store;s.persistent.room13_motion=False;s.r13_effect_review_phase=1;s.r13_effect_review_started=renpy.display.core.get_time();renpy.exports.restart_interaction();result=True')
    await page.screenshot(path=str(OUT/'motion-off.png'))
    await q.py('import renpy;s=renpy.store;s.persistent.room13_motion=True;s.r13_effect_review_started=renpy.display.core.get_time()-1;renpy.exports.restart_interaction();result=True')
    await page.screenshot(path=str(OUT/'motion-on-settled.png'))
    (OUT/'checks.json').write_text(json.dumps(dict(route=route,rapid=rapid,click_pair_wall_seconds=click_interval),ensure_ascii=False,indent=2))
    print('CHECKS COMPLETE',flush=True)
   except Exception:
    await page.screenshot(path=str(OUT/(mode+'-failure.png')));raise
   finally:await b.close()
asyncio.run(main())
