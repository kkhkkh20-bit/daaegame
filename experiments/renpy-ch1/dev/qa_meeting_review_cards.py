"""Requested native meeting screenshots, actual flow after an explicit day-7 fixture."""
import asyncio,json,subprocess
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/meeting-review-01936');OUT.mkdir(exist_ok=True)
async def main():
 report=dict(kind='Native WASM; day7 evening fixture then real meeting UI flow; no composite or art changes',base_sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),build_note='0.19.36 working build includes map-only contact adjustments above base; meeting sources match committed 0.19.35',shots=[])
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  async def until(screen):
   for _ in range(70):
    if await q.py('import renpy;result=bool(renpy.display.screen.get_screen('+repr(screen)+'))'):return
    await q.input(810,640)
   raise AssertionError('missing '+screen)
  async def shot(name):
   await asyncio.sleep(.6);await page.screenshot(path=str(OUT/(name+'.png')))
   report['shots'].append(dict(file=name+'.png',runtime=await q.py('import renpy;s=renpy.store;result=dict(day=s.room13["day"],period=s.room13["period"],location=s.room13["location"],claim=s.r13_meeting_claim,focus=s.r13_meeting_focus,packet=s.r13_packet)')));(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(name,flush=True)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');report['version']=await q.py('import renpy;result=renpy.store.config.version');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.5)
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.room13_mode=True;s.r13_edit(day=7,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=list(s.ROOM13["evidence"]),propositions=[]);s.r13_flag("entry_corrected","lodging");result=True')
   await native_jump(q,'r13_trial');await until('r13_meeting_agenda');await shot('01-whole-meeting-agenda')
   await q.press('다람이의 방어가');await until('say')
   for _ in range(30):
    if any('발언 고르기' in b['text'] for b in (await q.state())['buttons']):break
    await q.input(810,640)
   await shot('02-focused-speaker')
   await q.press('발언 고르기');await until('r13_debate_board');await shot('03-statement-selection')
   await q.press('보여주기');await until('r13_book');await shot('04-evidence-presentation')
   report['status']='captured'
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
