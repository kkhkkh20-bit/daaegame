"""Cold web boot, actual audio channels/position, rendered motion and mobile footer."""
import asyncio,json,os,time,io
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path('/workspace/work/ms14/startup75-browser');OUT.mkdir(exist_ok=True)
AUDIO="""(()=>{window.r13Analysers=[];const connect=AudioNode.prototype.connect;AudioNode.prototype.connect=function(dest,...args){if(dest instanceof AudioDestinationNode){const a=this.context.createAnalyser();a.fftSize=2048;connect.call(a,dest);window.r13Analysers.push(a);return connect.call(this,a,...args);}return connect.call(this,dest,...args);};})()"""
SNAP='''import renpy
s=renpy.store;t=renpy.game.context().scene_lists.layer_transform.get("master")
result=dict(version=s.config.version,music=renpy.audio.music.get_playing(),position=renpy.audio.music.get_pos(),pulse=renpy.audio.music.get_playing(channel="pulse"),ride=renpy.audio.music.get_playing(channel="carriage_ride"),fx=renpy.audio.music.get_playing(channel="scene_fx"),ambience=renpy.audio.music.get_playing(channel="ambience"),typing=renpy.audio.music.get_playing(channel="typing"),typing_allowed=s.typing_allowed,motion=s.persistent.room13_motion,offset=[t.xoffset,t.yoffset] if t else None)
'''
async def run(browser,mobile):
 ctx=await browser.new_context(viewport={'width':390,'height':844} if mobile else {'width':1280,'height':720},has_touch=mobile,is_mobile=mobile,device_scale_factor=1)
 await ctx.add_init_script(AUDIO);pg=await ctx.new_page();q=UIQA(pg,OUT);q.touch=mobile;errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
 started=time.monotonic();await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8766/preview/room13-dev/'),wait_until='domcontentloaded',timeout=180000)
 await pg.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await asyncio.sleep(12);await q.input(1100,600);await q.wait('main_menu');ready=time.monotonic()-started
 await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.wait('say');await asyncio.sleep(2)
 samples=[];frames=[]
 for i in range(4):
  samples.append(await q.py(SNAP));frames.append(Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'));await asyncio.sleep(.23)
 assert all(s['music']=='assets/bgm-travel.mp3' and s['pulse'] is None and s['ride']=='assets/ms14-audio/cart-roll-light.mp3' and s['typing'] is None and not s['typing_allowed'] for s in samples),samples
 assert samples[-1]['position']>samples[0]['position'],samples
 assert all(s['offset'] is None for s in samples),samples
 vp=pg.viewport_size;scale=min(vp['width']/1280,vp['height']/720);top=(vp['height']-720*scale)/2;left=(vp['width']-1280*scale)/2
 box=tuple(round(v) for v in (left+420*scale,top+70*scale,left+880*scale,top+150*scale))
 differences=[sum(ImageStat.Stat(ImageChops.difference(frames[0].crop(box),f.crop(box))).mean) for f in frames[1:]]
 assert max(differences)<.1,('Unwanted continuous carriage motion',differences)
 peak=await pg.evaluate('''()=>Math.max(0,...window.r13Analysers.map(a=>{let v=new Float32Array(a.fftSize);a.getFloatTimeDomainData(v);return Math.sqrt(v.reduce((s,x)=>s+x*x,0)/v.length)}))''')
 assert peak>0,peak
 name='mobile' if mobile else 'desktop';await q.shot(name+'-carriage')
 # Sample the real master transform throughout the one authored bump.
 await pg.mouse.click(left+900*scale,top+600*scale) if not mobile else await pg.touchscreen.tap(left+900*scale,top+600*scale)
 bump=[]
 for _ in range(10):
  bump.append(await q.py(SNAP));await asyncio.sleep(.035)
 assert any(x['offset'] and any(abs(v)>2 for v in x['offset']) for x in bump),bump
 await asyncio.sleep(.7)
 assert (await q.py(SNAP))['offset'] is None
 assert '아빠는 안 잡아 줘?' in (await q.state())['say']
 await q.shot(name+'-dad-after-bump')
 st=await q.state();buttons=st['buttons'];skip=next(b for b in buttons if b['text'].strip()=='건너뛰기');more=next(b for b in buttons if b['text'].strip()=='더보기');assert skip['rect'][1:]==more['rect'][1:]
 await q.press('건너뛰기');await q.advance();await q.wait('r13_hub')
 end=await q.py(SNAP);assert end['ride'] is None and end['pulse'] is None and end['offset'] is None,end
 await q.shot(name+'-gate')
 # Instrument actual renderer frames; story state and input routes stay natural.
 await q.py("""import renpy
s=renpy.store
s.qa_pan_frames=[]
def sample(st,at,s=s):
 s.qa_pan_frames.append([st,s.r13_world_offset()])
 return s.Null(),0
renpy.exports.show('qa_pan_sample',what=s.DynamicDisplayable(sample),layer='screens')
result=True
""")
 st=await q.state()
 arrow=next(x for x in st['buttons'] if x['text'].strip() in ('‹','›'))
 await q.input(arrow['rect'][0]+arrow['rect'][2]/2,arrow['rect'][1]+arrow['rect'][3]/2)
 await asyncio.sleep(.7)
 pan=await q.py('import renpy;result=list(renpy.store.qa_pan_frames)')
 moved=[x for i,x in enumerate(pan) if i and x[1]!=pan[i-1][1]]
 # Software-rendered CI cannot guarantee a hardware refresh rate. Verify
 # real intermediate positions, monotonic motion and a stable final position.
 assert len(moved)>=3,('Pan jumped or stalled',pan)
 direction=1 if moved[-1][1]>pan[0][1] else -1
 assert all((b[1]-a[1])*direction>=0 for a,b in zip(pan,pan[1:])),pan
 assert pan[-1][1]==pan[-2][1],pan
 assert abs(moved[-1][1]-pan[0][1])>100,pan
 await q.py("import renpy;renpy.exports.hide('qa_pan_sample',layer='screens');result=True")
 await q.shot(name+'-gate-panned')
 assert not errors,errors
 result=dict(pan_frames=pan,bump=bump,menu_observed_seconds_including_12s_settle=ready,samples=samples,rendered_pixel_difference=differences,output_rms=peak,after_skip=end,page_errors=errors)
 await ctx.close();return result
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',ignore_default_args=['--mute-audio'],args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
  report={'desktop':await run(b,False),'mobile':await run(b,True),'status':'passed'}
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
asyncio.run(main())
