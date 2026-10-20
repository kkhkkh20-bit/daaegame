"""First-use shared sound, with music/ambience paused and no remote placeholder."""
import asyncio,ast,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path('/workspace/work/ms14/shared-sfx74');OUT.mkdir(exist_ok=True)
source=ast.parse((Path(__file__).parent/'qa_startup74.py').read_text());AUDIO=next(ast.literal_eval(n.value) for n in source.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='AUDIO' for t in n.targets))
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',ignore_default_args=['--mute-audio'],args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
  c=await b.new_context(viewport={'width':1280,'height':720});await c.add_init_script(AUDIO);pg=await c.new_page();q=UIQA(pg,OUT)
  await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8766/preview/room13-dev/'),wait_until='domcontentloaded',timeout=180000)
  await pg.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await asyncio.sleep(12);await q.input(1100,600);await q.wait('main_menu');await q.press('처음부터');await q.wait('say')
  size=await pg.evaluate("FS.stat('/game/assets/sfx-page.wav').size");assert size>1000,size
  await q.py('import renpy\nfor ch in ("music","ambience","carriage_ride"):renpy.audio.music.set_pause(True,channel=ch)\nresult=True')
  await asyncio.sleep(.25);await q.py('import renpy;renpy.store.source_fx("page");result=True')
  peaks=[]
  for _ in range(8):
   peaks.append(await pg.evaluate('''()=>Math.max(0,...window.r13Analysers.map(a=>{let v=new Float32Array(a.fftSize);a.getFloatTimeDomainData(v);return Math.sqrt(v.reduce((s,x)=>s+x*x,0)/v.length)}))'''));await asyncio.sleep(.03)
  assert max(peaks)>0,peaks
  report=dict(status='passed',first_page_sound_bytes=size,first_play_output_rms=peaks,music_and_ambience_paused=True)
  (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True);await b.close()
asyncio.run(main())
