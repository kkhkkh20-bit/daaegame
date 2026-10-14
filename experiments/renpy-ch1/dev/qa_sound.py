"""Web build: title music, per-place music and ambience, remote-click button sound (0.18.5)."""
import asyncio,json,os,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'sound';OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
AUDIO=('bgm-','sfx-','amb-')
async def main():
 report={'archive_sha256':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'checks':[],'requests':{}}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
  context=await b.new_context(viewport={'width':1280,'height':720},has_touch=True,service_workers='allow');pg=await context.new_page();q=UIQA(pg,OUT)
  errors=[]
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  def seen(r):
   name=r.url.split('?')[0].rsplit('/',1)[-1]
   if name.startswith(AUDIO):report['requests'][name]=r.status
  pg.on('response',seen)
  playing=lambda ch='music':q.py('import renpy;result=renpy.audio.music.get_playing(channel=%r)'%ch)
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   assert await q.py('import renpy;result=renpy.store.config.main_menu_music')=='assets/bgm-title.mp3'
   assert await q.py('import renpy;result=renpy.store.style.button.activate_sound')=='assets/sfx-click.wav'
   await q.shot('s0-title')
   await q.press('설정');await q.wait('pause_menu');await q.press('소리');await q.shot('s0-options-sound')
   await q.press('보기');await asyncio.sleep(.8)
   assert await q.py('import renpy;result=bool(renpy.exports.get_screen("r13_music_credits"))')
   await q.shot('s0-music-credits');await q.press('닫기');await asyncio.sleep(.5);await q.press('돌아가기');await q.wait('main_menu')
   report['checks'].append('Options > sound > music credits opens and closes')
   await q.press('처음부터')
   for _ in range(100):
    st=await q.state()
    if 'say' in st['screens']:break
    await asyncio.sleep(.2)
   await asyncio.sleep(1.5)
   m=await playing();assert m=='assets/bgm-travel.mp3',m
   report['checks'].append('Carriage scene plays bgm-travel (Snowfall)')
   await q.press('건너뛰기');await q.advance()
   for _ in range(60):
    if 'r13_hub' in (await q.state())['screens']:break
    await q.advance()
   room=await q.room();assert room['location']=='gate',room
   await asyncio.sleep(1.5)
   m,a=await playing(),await playing('ambience')
   assert m=='assets/bgm-snow.mp3' and a=='assets/amb-wind.mp3',(m,a)
   report['checks'].append('Gate (day 1, calm) plays bgm-snow (First Snow) with wind ambience')
   await q.shot('s1-gate')
   # Inn at day 2 (same fixture as qa_navigation), then walk the inn with the real buttons.
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="inn");s.r13_flag("entry_corrected","lodging");s.r13_upgrade();w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True');await q.input(1220,50);await q.wait('r13_hub')
   walk=[]
   for label,loc,want_m,want_a in (('2층 복도','hall','assets/bgm-inn.mp3',None),('13호실','room13','assets/bgm-night.mp3',None),('복도로','hall','assets/bgm-inn.mp3',None),('1층 접수대','inn','assets/bgm-inn.mp3','assets/amb-fire.mp3')):
    await q.press(label);await q.wait('r13_hub');assert (await q.room())['location']==loc
    await asyncio.sleep(1.2);m,a=await playing(),await playing('ambience');walk.append((loc,m,a))
    assert m==want_m and a==want_a,(label,m,a)
   await q.shot('s2-inn-front')
   report['walk']=walk
   report['checks'].append('Inn walk with real buttons: hall=Midvinter, room13=Measured Paces, reception=Midvinter + fire ambience')
   for name in ('bgm-title.mp3','bgm-travel.mp3','bgm-snow.mp3','bgm-inn.mp3','bgm-night.mp3','amb-wind.mp3','amb-fire.mp3','sfx-click.wav'):
    st=report['requests'].get(name)
    assert st in (200,206,304) or name=='sfx-click.wav',(name,st)
   bad=[e for e in errors if any(k in e.lower() for k in ('audio','decode','mp3','wav'))]
   assert not bad,bad
   report['console_errors']=errors[:20]
   report['status']='passed'
  except Exception as e:
   report['status']='failed';report['error']=repr(e)[:2000]
   try:await q.shot('s-fail')
   except Exception:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
 print(json.dumps(report,ensure_ascii=False,indent=1))
asyncio.run(main())
