"""Play the real Ren'Py WASM chapter using mouse/touch. State access is read-only."""
import argparse, asyncio, json, shutil, time
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
# Observe real browser audio signals without changing the game's output path.
AUDIO_PROBE='''(() => {window.__audioProbe=[];const orig=AudioNode.prototype.connect;
AudioNode.prototype.connect=function(dest,...args){const r=orig.call(this,dest,...args);
if(dest===this.context.destination){const a=this.context.createAnalyser();a.fftSize=2048;orig.call(this,a);window.__audioProbe.push({a,ctx:this.context});}return r;};
window.__probeAudio=()=>window.__audioProbe.map(({a,ctx})=>{const d=new Float32Array(a.fftSize);a.getFloatTimeDomainData(d);return {state:ctx.state,rms:Math.sqrt(d.reduce((s,v)=>s+v*v,0)/d.length)};});})();'''
class Trial:
 def __init__(self,page,width,height,output):
  self.page,self.width,self.height,self.output=page,width,height,output
  self.errors=[];self.failed=[];self.bad=[];self.checks=[]
  page.on('pageerror',lambda e:self.errors.append(str(e)))
  page.on('console',lambda m:self.errors.append(m.text) if m.type=='error' and 'favicon' not in m.text else None)
  page.on('requestfailed',lambda r:self.failed.append({'url':r.url,'error':r.failure}))
  page.on('response',lambda r:self.bad.append({'url':r.url,'status':r.status}) if r.status>=400 and 'favicon' not in r.url else None)
 async def state(self):return await self.page.evaluate('renpy_exec("import renpy; result=renpy.store.trial_state()")')
 async def click(self,x,y):
  s=min(self.width/1280,self.height/720);px=(self.width-1280*s)/2+x*s;py=(self.height-720*s)/2+y*s
  if self.width<1000:await self.page.touchscreen.tap(px,py)
  else:await self.page.mouse.click(px,py)
  await self.page.wait_for_timeout(150)
 async def wait(self,key,value=True):
  for _ in range(65):
   st=await self.state()
   if st.get(key)==value:
    await self.page.wait_for_timeout(650);return st
   await self.page.wait_for_timeout(150)
  await self.shot('failure');raise AssertionError((key,value,await self.state()))
 async def advance_until(self,key,value=True,limit=180):
  for _ in range(limit):
   st=await self.state()
   if st.get(key)==value:
    await self.page.wait_for_timeout(500);return st
   if self.errors:raise AssertionError(self.errors)
   await self.click(830,665)
  await self.shot('failure');raise AssertionError((key,value,await self.state()))
 async def shot(self,name):await self.page.screenshot(path=str(self.output/(name+'.png')))
 async def interact(self,x,y):
  await self.click(x,y);await self.wait('explore',False);await self.advance_until('explore')
 async def talk(self):await self.interact(963,640)
 async def move(self,key):
  pos={'plaza':(160,390),'front':(425,310),'kitchen':(660,430),'hall':(700,175),'doto':(950,210),'room':(960,410)}
  await self.click(882,640);await self.wait('map')
  if (await self.state())['stage']=='investigation' and not (self.output/'map.png').exists():await self.shot('map')
  x,y=pos[key];await self.click(x+112,y+45);await self.wait('explore');assert (await self.state())['location']==key
 async def evidence(self,key,duel=False):
  await self.click(320 if duel else 220,420 if duel else 414);await self.wait('evidence')
  st=await self.state();index=st['inventory'].index(key)
  for _ in range(index//6):
   await self.click(286,576)
  slot=index%6
  await self.click(199+(slot%2)*230,240+(slot//2)*110)
  await self.wait('evidence',False)
 async def save(self):
  await self.click(1105,45);await self.wait('saving');await self.shot('save');await self.click(760,245);await self.page.wait_for_timeout(400);assert (await self.state())['saved_slots'];await self.click(265,590);await self.wait('saving',False)
 async def load(self):
  await self.click(1174,45);await self.wait('menu');await self.click(780,243);await self.wait('loading');await self.click(760,245);await self.wait('loading',False)
 async def select_speaker(self,key):
  idx=['granny','nabi','buri','bami','doto','karo','neoul','seryeon'].index(key)
  await self.click(97+153*idx,595);await self.wait('council');assert (await self.state())['speaker']==key

async def run_one(browser,args,w,h,reverse,out):
 c=await browser.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000);await c.add_init_script(AUDIO_PROBE);pg=await c.new_page();t=Trial(pg,w,h,out)
 start=time.monotonic();await pg.goto(args.url);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();startup=round(time.monotonic()-start,2)
 await t.shot('title');await t.click(320,425);await pg.wait_for_timeout(650)
 st=await t.state();assert st['music']=='assets/travel.mp3' and st['music_volume']>.3 and not st['music_mute']
 signal=False;type_active=bool(st['typing'])
 for _ in range(5):
  a=await pg.evaluate('__probeAudio()');signal |= any(x['state']=='running' and x['rms']>1e-5 for x in a);type_active |= bool((await t.state())['typing']);await pg.wait_for_timeout(200)
 assert signal,'No actual browser audio signal';assert type_active,'No typing during text';t.checks.append('music_output_and_typing')
 # Click over the eventual pillow during intro: no evidence may be acquired.
 await t.click(800,275);assert not (await t.state())['inventory'];t.checks.append('early_click_does_not_investigate')
 await t.advance_until('explore');await t.talk();assert 'granny_arrival' in (await t.state())['inspected']
 await t.move('kitchen');await t.talk();await t.shot('kitchen');await t.move('plaza');await t.talk();await t.move('front');await t.shot('arrival')
 await t.click(1090,637);await t.advance_until('explore');assert (await t.state())['stage']=='investigation'
 await t.shot('investigation');await t.interact(600,545);assert not (await t.state())['found'];t.checks.append('discovery_waits_for_reason_and_lamp')
 await t.click(1012,640);await t.wait('explore',False);await t.advance_until('explore');assert (await t.state())['stage']=='investigation';t.checks.append('incomplete_council_blocked')
 # Move first on the reverse route; evidence gathering works in either order.
 if reverse:
  await t.move('hall');await t.interact(455,210);await t.talk();await t.move('doto');await t.talk();await t.move('room')
 if not reverse:
  await t.interact(800,275);await t.interact(610,365)
  inv=(await t.state())['inventory'];await t.interact(800,275);assert (await t.state())['inventory']==inv;t.checks.append('duplicate_evidence_prevented')
 await t.move('kitchen');await t.talk();await t.move('front');await t.talk();assert (await t.state())['permission'];await t.move('room');await t.interact(740,190)
 await t.click(730,450);await t.wait('code');await t.shot('lock');await t.click(260,550);assert (await t.state())['code_error'];t.checks.append('wrong_lock_code_stays_locked');print('LOCK',w,flush=True)
 for x,count in [(424,1),(568,1),(712,0),(856,2)]:
  for _ in range(count):await t.click(x,294)
 assert (await t.state())['digits']==[1,1,0,2], await t.state()
 await t.click(260,550);await t.wait('code',False);await t.advance_until('explore');assert (await t.state())['archive'] and 'registry' in (await t.state())['inventory']
 await t.save();saved=await t.state();await pg.reload();await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(320,500);await t.wait('loading');await t.click(760,245);await t.wait('explore');assert (await t.state())['archive'];assert (await t.state())['inventory']==saved['inventory'];t.checks.append('reload_restores_investigation_and_lock');print('RELOAD',w,flush=True)
 await t.interact(600,545);assert (await t.state())['found'];await t.shot('discovery_return')
 if reverse:
  assert 'pouch' not in (await t.state())['inventory'] and 'flour' not in (await t.state())['inventory'];t.checks.append('discovery_without_fixed_primary_evidence_order')
  await t.interact(800,275);await t.interact(610,365)
  inv=(await t.state())['inventory'];await t.interact(800,275);assert (await t.state())['inventory']==inv;t.checks.append('duplicate_evidence_prevented')
 if not reverse:
  await t.move('hall');await t.interact(455,210);await t.talk();await t.move('doto');await t.talk()
 await t.move('plaza');await t.talk();await t.move('room');await t.click(1010,640);await t.advance_until('choice');await t.click(620,278);await t.advance_until('council');await t.shot('council');print('COUNCIL',w,flush=True)
 # All eight residents can be selected; none changes evidence or forces a vote.
 for key in ['granny','nabi','buri','bami','doto','karo','neoul','seryeon']:await t.select_speaker(key)
 t.checks.append('eight_residents_selectable')
 await t.evidence('flour');await t.advance_until('council');assert (await t.state())['wrong']==1
 contact=('fur','pouch') if reverse else ('pouch','fur')
 await t.evidence(contact[0]);await t.advance_until('council');assert (await t.state())['first']==contact[0]
 await t.save();await t.evidence(contact[1]);await t.advance_until('choice');await t.load();await t.wait('council');assert (await t.state())['first']==contact[0] and 'contact' not in (await t.state())['resolved'];t.checks.append('mid_comparison_save_restores')
 await t.evidence(contact[1]);await t.advance_until('choice');await t.click(620,365);await t.advance_until('council');assert (await t.state())['conclusion_attempts']==1;t.checks.append('overclaim_does_not_solve_case');await t.evidence(contact[1]);await t.advance_until('choice');await t.click(620,270);await t.advance_until('council');assert 'contact' in (await t.state())['resolved'];t.checks.append('contact_evidence_both_orders')
 await t.select_speaker('bami');clock=('snow','clock') if reverse else ('clock','snow')
 await t.evidence(clock[0]);await t.advance_until('council');await t.evidence(clock[1]);await t.advance_until('clock_demo');await t.shot('clock');await t.click(700,345);await t.shot('clock-rotated');await t.click(700,410);await t.advance_until('choice');await t.click(620,270);await t.advance_until('council');assert 'clock' in (await t.state())['resolved'];t.checks.append('clock_viewpoint_reasoning');print('CLOCK',w,flush=True)
 corrected=await pg.evaluate("code => renpy_exec(code)", 'import renpy; result=renpy.store.evidence_text("bami")')
 assert '정정된 목격 시각: 자정' in corrected;t.checks.append('corrected_witness_updates_notebook')
 await t.select_speaker('nabi');await t.evidence('flour');await t.advance_until('council');assert 'quilt' in (await t.state())['resolved']
 await t.click(1130,690);await t.advance_until('duel');await t.shot('duel')
 await t.evidence('karo',True);await t.advance_until('duel');assert (await t.state())['showdown']=='place';t.checks.append('gambling_is_not_proof_of_amount')
 await t.evidence('record',True);await t.advance_until('duel');assert (await t.state())['showdown']=='movement'
 movement=('fur','bami') if reverse else ('bami','fur')
 await t.evidence(movement[0],True);await t.advance_until('duel');await t.evidence(movement[1],True);await t.advance_until('duel');assert (await t.state())['showdown']=='money'
 await t.evidence('pouch' if reverse else 'seal',True);await t.advance_until('choice');await t.shot('conclusion');await t.click(620,270);await t.advance_until('case_resolved');assert (await t.state())['stage']=='showdown';await t.advance_until('explore');assert (await t.state())['case_resolved'] and (await t.state())['stage']=='aftermath';t.checks.append('complete_case_before_confession');print('VERDICT',w,flush=True)
 await t.move('kitchen');await t.talk();await t.move('hall');await t.talk();await t.move('front');await t.talk();assert (await t.state())['mother'];await t.shot('aftermath');await t.click(1090,640);await t.advance_until('completion');await t.shot('complete');final=await t.state();assert final['complete'];assert not final['typing'];assert not t.errors,t.errors;assert not t.bad,t.bad;assert not t.failed,t.failed
 result={'viewport':[w,h],'touch':w<1000,'reverse_evidence':reverse,'startup_seconds_local':startup,'checks':t.checks,'final':final,'errors':t.errors,'failed_requests':t.failed,'bad_responses':t.bad};await c.close();return result
async def main(args):
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);results=[]
  for w,h,reverse in [(1280,720,False),(844,390,True)]:
   folder=out/f'{w}x{h}';folder.mkdir(exist_ok=True)
   result=await run_one(b,args,w,h,reverse,folder);results.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
  await b.close()
 (out/'report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8093/preview/renpy-ch1-test/');parser.add_argument('--output',default=str(ROOT/'qa-output'));asyncio.run(main(parser.parse_args()))
