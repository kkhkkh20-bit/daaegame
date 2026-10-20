"""Exercise early audio with the engine held back, including gesture-only browsers."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
OUT=Path('/workspace/work/update75');OUT.mkdir(exist_ok=True)
async def run(p,autoplay):
 b=await p.chromium.launch(executable_path='/usr/bin/chromium',ignore_default_args=['--mute-audio'],args=['--no-sandbox','--autoplay-policy='+('no-user-gesture-required' if autoplay else 'document-user-activation-required')])
 c=await b.new_context();await c.add_init_script('window.qaAudio=[];const A=window.Audio;window.Audio=function(...args){const a=new A(...args);window.qaAudio.push(a);return a;};')
 pg=await c.new_page();errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
 await pg.route('**/renpy.js',lambda route:route.abort())
 await pg.goto('http://localhost:8766/preview/room13-dev/',wait_until='domcontentloaded')
 await asyncio.sleep(1)
 before=await pg.evaluate('()=>({paused:qaAudio[0].paused,time:qaAudio[0].currentTime})')
 if not autoplay:
  assert before['paused'],before
  await pg.mouse.click(640,400)
 await pg.wait_for_function('qaAudio[0].currentTime>0 && !qaAudio[0].paused')
 active=await pg.evaluate('()=>({paused:qaAudio[0].paused,time:qaAudio[0].currentTime,src:qaAudio[0].src})')
 await pg.evaluate('document.getElementById("presplash").remove()');await asyncio.sleep(.15)
 assert await pg.evaluate('qaAudio[0].paused && !qaAudio[0].getAttribute("src")')
 assert not errors,errors
 await b.close();return dict(before=before,active=active,handover_stopped=True,page_errors=errors)
async def main():
 async with async_playwright() as p:
  r=dict(autoplay=await run(p,True),gesture=await run(p,False),status='passed');(OUT/'loading-audio.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
asyncio.run(main())
