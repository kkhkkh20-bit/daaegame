"""Web build: carriage opening (empty interior, Daram pops in and stays), skip reaches the gate."""
import asyncio,json,os,shutil,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
from webqa import FLOW_PROBE
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'carriage';OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
class IntroQA(UIQA):
 async def state(self):
  probe=FLOW_PROBE.replace('names=[',"names=['r13_entry_daram_topics','r13_gate_document_inspection','r13_gate_document_read','r13_resident_approach','r13_desk_inspection','r13_record_compare','r13_records','r13_book','r13_backlog',")
  st=await self.py('ns={};exec('+ascii(probe)+',ns);result=ns["result"]');assert '_exception' not in st['screens'],st;return st
 async def advance_to(self,name):
  for _ in range(150):
   st=await self.state()
   if name in st['screens']:await asyncio.sleep(.4);return st
   if 'say' in st['screens']:await self.input(810,610)
   elif 'r13_cinematic_view' in st['screens']:await self.press('계속')
   else:await asyncio.sleep(.2)
  raise AssertionError((name,st))
 async def talk(self,label):
  await self.press(label);await self.advance()
  if 'r13_resident_approach' in (await self.state())['screens']:
   await self.value(True)
  await self.advance_to('r13_topics')
 async def value(self,value):
  for attempt in range(10):
   try:return await super().value(value)
   except AssertionError:
    if attempt==9:raise
    await asyncio.sleep(.3)
 async def present(self,label):
  await self.press('보여주기');await self.wait('r13_book');await self.press('들은 말' if label=='초롱의 목격담' else '증거');await self.press(label);await self.press('보여주기');await self.wait('r13_confirm');await self.press('보여준다');await self.advance_to('r13_topics')
async def main():
 report={'archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  context=await b.new_context(viewport={'width':1280,'height':720},has_touch=True,service_workers='allow');pg=await context.new_page();q=IntroQA(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터')
   for _ in range(100):
    st=await q.state()
    if 'say' in st['screens']:break
    await asyncio.sleep(.2)
   await asyncio.sleep(1);await q.shot('c0-carriage-narration')
   await q.input(810,610);await asyncio.sleep(1.5)
   info=await q.py('import renpy;s=renpy.store;result=dict(place=s.place,who=s.r13_motion_person,tags=sorted(renpy.exports.get_showing_tags()))')
   assert info['place']=='마차 안' and info['who']=='daram' and 'r13_visitor' in info['tags'],info
   await q.shot('c1-daram-pop')
   await q.input(810,610);await asyncio.sleep(1.2)
   info2=await q.py('import renpy;s=renpy.store;result=dict(who=s.r13_motion_person,tags=sorted(renpy.exports.get_showing_tags()))')
   assert info2['who']=='daram' and 'r13_visitor' in info2['tags'],info2
   await q.shot('c2-dad-line')
   await q.press('건너뛰기');await q.advance_to('r13_hub');room=await q.room()
   assert room['location']=='gate' and room['day']==1,room
   await q.shot('c3-gate')
   report['checks'].append('Web build: carriage opens on empty interior, Daram pops in and stays during Dad line, skip reaches gate day 1')
   report['status']='passed'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
   try:
    details=await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_resident_approach");result={k:repr(sc.scope.get(k)) for k in ("ready","choices","person","target","_scope","_use_scope")} if sc else {}')
    (OUT/"failure-scope.json").write_text(json.dumps(details,ensure_ascii=False,indent=2))
   except:pass
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
