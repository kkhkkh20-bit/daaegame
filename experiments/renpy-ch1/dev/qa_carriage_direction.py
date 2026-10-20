"""Natural opening, original skip, active carriage direction; no story-state injection."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'carriage-direction';OUT.mkdir(parents=True,exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
  pg=await b.new_page(viewport={'width':1280,'height':720});q=UIQA(pg,OUT);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8766/preview/room13-dev/'),wait_until='domcontentloaded',timeout=180000)
  await pg.wait_for_function("typeof renpy_exec==='function'",timeout=240000)
  await asyncio.sleep(12);await pg.mouse.click(1100,600);await q.wait('main_menu')
  await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
  await q.press('처음부터');await q.wait('say');await asyncio.sleep(1)
  opening=await q.py('import renpy;s=renpy.store;result=dict(version=s.config.version,packet=s.r13_packet,music=renpy.audio.music.get_playing(),fx=renpy.audio.music.get_playing(channel="scene_fx"),master_transforms=len(renpy.game.context().scene_lists.layer_at_list["master"][1]),ms14=s.ms14)')
  assert opening['packet'][0] is None and opening['packet'][1]=='다람이 과자 봉지를 외투 안쪽으로 당긴다.',opening
  assert opening['fx'].startswith('assets/ms14-audio/SFX_cart_'),opening
  assert opening['master_transforms']==1 and opening['ms14'] is None,opening
  await q.shot('01-opening-direction')
  await q.input(900,600);await asyncio.sleep(.8)
  assert '아빠는 안 잡아 줘?' in (await q.state())['say']
  await q.shot('02-first-dialogue')
  for _ in range(24):
   packet=await q.py('import renpy;result=renpy.store.r13_packet')
   if packet[1]=='또 읽어?':break
   await q.input(900,600)
  assert packet[1]=='또 읽어?',packet
  assert await q.py('import renpy;result=bool(renpy.display.screen.get_screen("r13_evidence_card"))')
  await q.shot('03-letter-reference')
  for _ in range(24):
   packet=await q.py('import renpy;result=renpy.store.r13_packet')
   if packet[0]=='karo':break
   await q.input(900,600)
  assert packet[0]=='karo',packet
  assert not await q.py('import renpy;result=bool(renpy.display.screen.get_screen("r13_evidence_card"))')
  await q.shot('04-village-reveal')
  await q.press('씬 건너뛰기');await q.wait('say')
  for _ in range(100):
   place=await q.py('import renpy;result=renpy.store.place')
   if place=='눈에 막힌 입구':break
   await asyncio.sleep(.2)
  end=await q.py('import renpy;s=renpy.store;result=dict(place=s.place,fx=renpy.audio.music.get_playing(channel="scene_fx"),master_transforms=len(renpy.game.context().scene_lists.layer_at_list["master"][1]))')
  assert end['place']=='눈에 막힌 입구' and not end['fx'] and end['master_transforms']==0,end
  await q.advance();await q.wait('r13_hub');await q.shot('05-original-gate-after-skip')
  assert not errors,errors
  report=dict(status='passed',opening=opening,after_skip=end,page_errors=errors)
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False),flush=True)
  await b.close()
asyncio.run(main())
