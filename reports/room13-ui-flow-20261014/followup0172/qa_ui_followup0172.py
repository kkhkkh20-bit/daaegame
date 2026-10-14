"""Additional natural map/resident/mobile review of the published 0.17.2 archive."""
import asyncio,json,shutil
from pathlib import Path
from playwright.async_api import async_playwright
from pixel_qa_ui0156 import UIQA
OUT=Path('/workspace/room13-review/followup0172');OUT.mkdir(exist_ok=True)
URL='http://127.0.0.1:8094/room13-dev/'
async def main():
 report={'kind':'natural map and local navigation; no story injection','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=UIQA(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   await q.press('지도 · 이동');await q.wait('r13_map');before=await q.room();await q.shot('01-village-known-pins');await q.press('여관 접수대');await q.shot('02-village-inn-selected');assert await q.room()==before
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True;await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await q.shot('03-map-mobile-large')
   await q.press('여관 내부 보기');await q.shot('04-inn-interior-preview');assert await q.room()==before;await q.press('이곳으로 이동');await q.advance();await q.wait('r13_hub');assert (await q.room())['location']=='inn';await q.shot('05-inn-mobile-local-exits')
   await q.press('할머니');await q.advance();await q.wait('r13_hub');assert 'lodging' in (await q.room())['flags'];await q.shot('06-inn-checkin-local-exits')
   await q.press('2층 복도');await q.advance();await q.wait('r13_hub');assert (await q.room())['location']=='hall';await q.shot('07-hall-mobile');await q.press('13호실');await q.advance();await q.wait('r13_hub');assert (await q.room())['location']=='room13';await q.shot('08-room-mobile');report['checks'].append('Natural village selection and interior preview leave state/time unchanged; actual entry, check-in, visible local hallway and room buttons work on mobile')
   await q.press('복도로');await q.advance();await q.wait('r13_hub');await q.press('1층 접수대');await q.advance();await q.wait('r13_hub');await q.press('여관 밖으로');await q.wait('r13_map');await q.shot('09-back-to-village');await q.press('광장');await q.press('이곳으로 이동');await q.advance();await q.wait('r13_hub');await q.shot('10-square-mobile')
   people=await q.py('import renpy;result=renpy.store.r13_people()');report['square_people']=people
   if 'resident_piko' in people:
    await q.value(('person','resident_piko'));await q.advance();await q.wait('r13_resident_approach');await q.shot('11-resident-approach-mobile');before=await q.room();await q.press('지금은 말을');await q.wait('r13_hub');assert await q.room()==before
    await q.value(('person','resident_piko'));await q.advance();await q.wait('r13_resident_approach');await q.value(True);await q.advance();await q.wait('r13_topics');await q.shot('12-resident-topics-mobile');await q.press('돌아가기');await q.wait('r13_hub');report['checks'].append('Natural Piko approach observation, decline preserving state, accept conversation and return work on mobile')
   else:report['not_executed']=['Piko approach unavailable in this natural day-1 square state']
   report['status']='passed-pending-visual-review'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
