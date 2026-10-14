"""Natural gate interactions plus explicit daylight/crowd layout fixtures."""
import asyncio,json,os,shutil,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
from webqa import FLOW_PROBE
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'save-slots';OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
class Q(UIQA):
 async def state(self):
  probe=FLOW_PROBE.replace('names=[',"names=['r13_gate_document_inspection','r13_gate_document_read','r13_records',")
  s=await self.py('ns={};exec('+ascii(probe)+',ns);result=ns["result"]');assert '_exception' not in s['screens'],s;return s
 async def object(self,key):
  rect=await self.py('import renpy;s=renpy.store;result=s.ROOM13["objects"][s.room13["location"]]['+repr(key)+']["rect"]')
  offset=(await self.camera())['offset'];x,y,w,h=rect;assert 0<=x+w/2-offset<=1280,(key,rect,offset);await self.input(x+w/2-offset,y+h/2)
 async def pan(self,start,end):
  # Real drag on open snow, not a direct camera-state write.
  await self.p.mouse.move(start,650);await self.p.mouse.down();await self.p.mouse.move(end,650,steps=18);await self.p.mouse.up();await asyncio.sleep(.5)
async def main():
 report={'archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True);pg=await c.new_page();q=Q(pg,OUT)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   await q.press('옵션');await q.wait('pause_menu');await q.press('저장');await q.wait('save')
   for page in (1,2,3):
    await q.press(str(page)+'쪽');state=await q.state();slots=[b for b in state['buttons'] if str(page)+'쪽 ' in b['text']];assert len(slots)==6,slots
    await q.shot('save-page-'+str(page))
   await q.press('3쪽 6번');await q.press('3쪽 6번');await q.wait('confirm');await q.shot('overwrite-confirm');await q.press('아니요');await q.wait('save');await q.press('돌아가기');await q.wait('r13_hub')
   report['checks'].append('Actual save screen: three pages, six slots each; slot 3-6 saves, repeat opens overwrite confirmation; cancel returns safely')
   report['status']='passed-pending-visual-review'
  except Exception as e:
   report.update(status='failed',error=repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']=='failed':raise SystemExit(1)
asyncio.run(main())
