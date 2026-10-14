"""Fresh browser natural interactions, then explicitly injected meeting/save fixtures."""
import asyncio,json,shutil,sys
from pathlib import Path
from playwright.async_api import async_playwright
from pixel_qa_ui0156 import UIQA
from pixel_qa_flow0150 import FLOW_PROBE
OUT=Path('/workspace/room13-review/meeting0178');OUT.mkdir(exist_ok=True)
URL='http://127.0.0.1:8094/room13-dev/'
class Q(UIQA):
 async def state(self):
  probe=FLOW_PROBE.replace('names=[',"names=['r13_records','r13_backlog','r13_debate_board','r13_save_cleanup','r13_save_review',")
  s=await self.py('ns={};exec('+ascii(probe)+',ns);result=ns["result"]');assert '_exception' not in s['screens'],s;return s
 async def advance(self):
  for _ in range(220):
   s=await self.state()
   if 'r13_arrival_card' in s['screens']:await self.input(800,400);continue
   if 'r13_cinematic_view' in s['screens']:await self.press('계속');continue
   if any(k in s['screens'] for k in ('r13_debate_board','choice','r13_hub','r13_book','r13_confirm','r13_topics','r13_entry_topics','r13_entry_karo_topics','r13_object_context','r13_map')):return s
   if 'say' in s['screens']:await self.input(810,610)
   else:await asyncio.sleep(.15)
  raise AssertionError(s)
async def main():
 report={'checks':[],'kind':'Explicit meeting fixtures; all proof submissions and conclusion choices use real UI'}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=Q(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   for claim,keys in [('C3',['E12','E05'])]:
    await q.py('import renpy;s=renpy.store;s.r13_edit(day='+('14' if claim=='F1' else '7')+',period=1,case_state="occurred",location="dining");s.r13_grant('+repr(keys)+',"QA fixture");renpy.exports.hide_screen("r13_evidence_found");result=True')
    code="import renpy\ns=renpy.store\ndef enter(renpy=renpy):\n renpy.exports.call_in_new_context('r13_debate_run',"+repr(claim)+")\nw=renpy.exports.get_widget('r13_hub','r13_options_gear')\nw.action=s.Function(enter)\nw.clicked=w.action\nresult=True"
    await q.py(code);await q.input(1220,50);await q.wait('r13_debate_board');await q.shot(claim+'-seating-desktop')
    await q.press('자료로 반박');await q.wait('r13_book');await q.press('그만두기');await q.wait('r13_debate_board');assert await q.py('import renpy;result=renpy.store.r13_debate_selected')=='s2'
    await pg.set_viewport_size({'width':844,'height':390});q.touch=True;await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await q.shot(claim+'-mobile-large')
    await pg.set_viewport_size({'width':1280,'height':720});q.touch=False;await asyncio.sleep(1)
    await pg.mouse.move(700,500);await pg.mouse.wheel(0,700);await asyncio.sleep(.8)
    offset=await q.py('import renpy;result=renpy.store.r13_meeting_scrolls.get('+repr(claim)+',0)');assert offset>0 if claim!='F1' else offset>=0
    await q.press('자료로 반박');await q.wait('r13_book');await q.press('그만두기');await q.wait('r13_debate_board');assert await q.py('import renpy;result=renpy.store.r13_meeting_scrolls.get('+repr(claim)+',0)')==offset
    await q.shot(claim+'-scrolled-cancel-preserved')
    for index,key in enumerate(keys):
     assert await q.py('import renpy;result=renpy.store.r13_debate_selected')=='s'+str(index+2)
     await q.press('자료로 반박');await q.wait('r13_book');category=await q.py('import renpy;result=renpy.store.r13_record_category('+repr(key)+')');await q.press('들은 말' if category=='testimony' else '증거')
     await q.press(await q.py('import renpy;result=renpy.store.R13_RECORD_SHORT.get('+repr(key)+',renpy.store.ROOM13["evidence"]['+repr(key)+']["name"])'));await q.press('이 주장에 근거로');await q.advance();await q.wait('r13_debate_board')
    assert await q.py('import renpy;result=renpy.store.r13_debate_ready('+repr(claim)+')');await q.shot(claim+'-proof-ready');await q.press('결론을 말한다');await q.wait('choice')
    correct=await q.py('import renpy;result=next(t for k,t in renpy.store.R13_DEBATE['+repr(claim)+']["conclusion"]["options"] if k=="correct")');await q.press(correct);await q.advance();await q.wait('r13_hub');assert claim in (await q.room())['propositions']
    report['checks'].append(claim+': desktop and mobile large text seats, evidence cancel retains selection and scroll, actual evidence rebuttals and correct conclusion preserve proof engine')
   report['status']='passed'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
