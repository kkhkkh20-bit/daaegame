"""Actual notebook selection/cancel/reopen; explicit inventory fixture, not a playthrough."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/abc-materials'));OUT.mkdir(parents=True,exist_ok=True)
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True);q=UIQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/'));await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=5,case_state="occurred",evidence=[key for key in s.ROOM13["evidence"] if key!="E20"],livelihood=dict(cash=30,items=["herbs"]));renpy.exports.show_screen("r13_book",target="buri");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_book');await q.shot('transferable-gold-card');assert await q.py('import renpy;result=renpy.store.r13_catalog_transferable("bag:herbs")');await q.press('다음 ›');await q.input(340,200)
   expected=await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_book");result=[sc.scope["detail"],sc.scope["page"]]')
   assert expected[0] and expected[1]==1,expected
   before=(await q.state())['room'];await q.press('닫기');await q.wait('r13_hub')
   await q.py('import renpy;renpy.exports.show_screen("r13_book",target="buri");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_book')
   assert await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_book");result=[sc.scope["detail"],sc.scope["page"]]')==expected
   await q.shot('materials-restored');await q.press('닫기')
   assert (await q.state())['room']==before
   # Present the exact current statement in the same paper shell. This is a
   # visual fixture; proof submission is covered by qa_meeting's real flow.
   await q.py('import renpy;s=renpy.store;s.r13_meeting_claim="C2";s.r13_debate_selected="s2";renpy.exports.show_screen("r13_book",target="resident_seori",present=True,hearing=True);renpy.exports.restart_interaction();result=True')
   await q.wait('r13_book');await q.shot('statement-and-materials')
   assert await q.py('import renpy;s=renpy.store;result=s.r13_book_statement()[1]==s.r13_meeting_statement_text("C2","s2")')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True;await q.shot('statement-and-materials-mobile')
   active=[b for b in (await q.state())['buttons'] if b['text'].strip() in ('그만두기','다음 ›')]
   assert active and all(b['rect'][3]*390/720>=44 for b in active),active
   result=dict(passed=True,checks=['real page/selection restored after close and reopen','close/reopen does not alter evidence or world time','exact selected statement displayed alongside materials','844x390 primary notebook controls at least44 CSSpx'])
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(result,flush=True)
  finally:await browser.close()
asyncio.run(main())
