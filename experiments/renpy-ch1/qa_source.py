"""Native mouse/touch route and spoken-line parity for the captured v2 chapter."""
import argparse
import asyncio
import json
import shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_web import Trial, AUDIO_PROBE

ROOT=Path(__file__).resolve().parent
EP=json.loads((ROOT/'game/chapter-source.json').read_text())['episode']

class SourceTrial(Trial):
 async def state(self):
  result=await self.page.evaluate('renpy_exec("import renpy; result=dict(renpy.store.trial_state(), **renpy.store.source_state())")')
  if result.get('exception'):
   await self.shot('exception');raise AssertionError('Native RenPy exception; see exception.png')
  return result
 async def advance_until(self,key,value=True,limit=1200):
  for _ in range(limit):
   st=await self.state()
   if st.get(key)==value:
    await self.page.wait_for_timeout(550);return st
   if self.errors:raise AssertionError(self.errors)
   if _ % 150 == 149:print('ADVANCE',self.width,key,st.get('line'),st.get('text'),flush=True)
   if st['inspect']:await self.click(225,535)
   else:await self.click(830,665)
  await self.shot('failure');raise AssertionError((key,value,{k:v for k,v in (await self.state()).items() if k not in ('lines','effects')}))
 async def move(self,key):
  await self.click(842,635);await self.wait('map')
  pos={'plaza':(160,390),'front':(425,310),'kitchen':(660,430),'hall':(700,175),'dotoroom':(950,210),'bed13':(960,410),'dining':(425,535)}
  x,y=pos[key];await self.click(x+112,y+45);await self.wait('roam');assert (await self.state())['location']==key
 async def interact(self,x,y):
  await self.wait('roam')
  await self.click(x,y);await self.wait('roam',False);await self.advance_until('roam')
 async def question(self,key,second=False):
  await self.click(1005 if second else 785,220 if (await self.state())['location']=='hall' else 370);await self.wait('questions')
  person=next(k for k,v in EP['TALK'].items() if any(q['id']==key for q in v))
  st=await self.state();qs=[q for q in EP['TALK'][person] if (not q.get('need') or q['need'] in st['inventory']) and (not q.get('after') or q['after'] in st['seen'])]
  index=next(i for i,q in enumerate(qs) if q['id']==key)
  await self.click(360,209+index*63);await self.wait('questions',False);await self.advance_until('questions')
  st=await self.state();qs=[q for q in EP['TALK'][person] if (not q.get('need') or q['need'] in st['inventory']) and (not q.get('after') or q['after'] in st['seen'])]
  await self.click(140,206+len(qs)*63);await self.wait('roam')
 async def evidence(self,key,duel=False):
  await self.click(227,485);await self.wait('evidence')
  index=(await self.state())['inventory'].index(key)
  for _ in range(index//6):await self.click(286,576)
  slot=index%6;await self.click(199+(slot%2)*230,240+(slot//2)*110);await self.wait('evidence',False)
 async def proof(self,phase,row,keys):
  st=await self.advance_until('debate');assert st['phase']==phase,(phase,st)
  await self.click(350,220+row*87);await self.wait('debate');assert (await self.state())['statement']==row
  for key in keys:
   await self.evidence(key)
   if key==keys[-1]:break
   await self.advance_until('debate')

async def run(browser,out,w,h,discovery_only=False):
 c=await browser.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000);await c.add_init_script(AUDIO_PROBE);pg=await c.new_page();t=SourceTrial(pg,w,h,out)
 await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.shot('title');await t.click(320,425);await t.advance_until('roam');st=await t.state();await t.shot('investigation')
 expected=[(p[0],p[1]) for sc in EP['PRO'] for p in sc['items'] if isinstance(p,list) and p[0] not in ('narr','@dir','@grant','@inspect')]
 actual=[(p['w'],p['t']) for p in st['lines'] if p['id'].split(':')[0] in [s['sid'] for s in EP['PRO']] and p['w']!='narr']
 assert actual==expected,(len(actual),len(expected));assert {'knock','steps','doorOpen','door','bell10','slam','heartbeat'}<=set(st['effects']);assert st['pulse'] is None
 checks=['opening_spoken_lines_match_shipped_v2','opening_sound_cues_and_no_pulse_leak'];print('OPENING',w,flush=True)
 await t.interact(600,545);assert not (await t.state())['found'];checks.append('original_late_discovery_gate')
 await t.interact(800,275);await t.interact(610,365);await t.move('kitchen');await t.question('C03');await t.move('front');await t.interact(340,495);await t.move('dining');await t.question('T_se2',True);await t.question('C12',True);await t.move('bed13')
 await t.click(600,545);await t.wait('roam',False)
 pulse_seen=False; pulse_heard=False
 for _ in range(400):
  st=await t.state()
  if st['roam']:break
  if st['pulse']:
   pulse_seen=True;assert st['music'] is None;assert st['typing'] is None
   if st['fx'] is None:pulse_heard |= any(a['rms']>1e-5 for a in await pg.evaluate('__probeAudio()'))
   if not (out/'discovery.png').exists():await t.shot('discovery')
  if st.get('camera')=='held' and not (out/'held.png').exists():
   await pg.wait_for_timeout(650)
   assert not await pg.evaluate("(code)=>renpy_exec(code)", 'import renpy; result=renpy.exports.showing("visitor")'), 'Old actor remains over CG'
   await t.shot('held')
  await t.click(830,665)
 assert pulse_seen and pulse_heard and st['found'];assert st['pulse'] is None;checks.append('discovery_silence_heartbeat_and_crowd');print('FOUND',w,flush=True)
 if discovery_only:
  assert (out/'held.png').exists();assert not t.errors and not t.failed and not t.bad
  result=dict(viewport=[w,h],touch=w<1000,checks=checks+['held_cg_from_black'],errors=t.errors,failed_requests=t.failed,bad_responses=t.bad,stage=st['stage'])
  await c.close();return result
 await t.interact(740,190);await t.click(730,450);await t.advance_until('code');await t.click(260,550);assert (await t.state())['code_error']
 for x,count in [(424,1),(568,1),(712,0),(856,2)]:
  for _ in range(count):await t.click(x,294)
 await t.click(260,550);await t.wait('code',False);await t.advance_until('roam');assert 'C11' in (await t.state())['inventory'];await t.interact(295,530)
 await t.save();saved=(await t.state())['inventory'];await pg.reload();await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(320,500);await t.wait('loading');await t.click(760,245);await t.wait('roam');assert (await t.state())['inventory']==saved;checks.append('source_save_survives_refresh')
 await t.move('hall');await t.interact(430,170);await t.question('C07');await t.question('C13');await t.move('dotoroom');await t.interact(340,495);await t.move('plaza');await t.question('T_ka2');await t.move('bed13');await t.click(964,635);await t.advance_until('debate');await t.shot('meeting');assert (await t.state())['phase']==1
 # A wrong record cannot solve the breathing question, and pressing is required.
 await t.evidence('C01');await t.wait('debate');assert (await t.state())['phase']==1
 await t.click(110,485);await t.advance_until('debate');assert (await t.state())['pressed'];await t.evidence('C04');await t.advance_until('choice');await t.shot('breathing-choice');await t.click(600,180);await t.advance_until('debate');assert (await t.state())['phase']==3;checks.append('life_check_requires_question_and_evidence')
 await t.proof(3,1,['C02','C03']);await t.advance_until('debate');assert (await t.state())['phase']==7
 await t.click(350,307);await t.wait('debate');await t.evidence('C06');await t.advance_until('debate');await t.save();await t.evidence('C07');await t.advance_until('debate');await t.load();await t.wait('debate');assert (await t.state())['step']==1;checks.append('original_comparison_save_restores');await t.evidence('C07');await t.advance_until('debate');await t.evidence('C08');await t.advance_until('debate');assert (await t.state())['phase']==8
 await t.proof(8,2,['C04','C10']);await t.advance_until('choice');await t.shot('vote');await t.click(600,272);await t.advance_until('debate');assert (await t.state())['group']=='final';await t.shot('final')
 await t.proof(0,0,['C05','C01']);await t.advance_until('debate');await t.proof(1,0,['C13','C01']);await t.advance_until('debate');await t.proof(3,0,['C10','C12','C14']);await t.advance_until('complete_screen');await t.shot('complete');st=await t.state();assert st['complete'] and st['pulse'] is None;assert not t.errors and not t.failed and not t.bad
 checks.extend(['original_four_meeting_rounds','original_three_final_rounds_and_vote','source_after_story_to_end'])
 # Every spoken line executed is directly present in the captured source.
 allowed=set()
 def collect(value):
  if isinstance(value,dict):
   if 'w'in value and 't'in value:allowed.add((value['w'],value['t']))
   for v in value.values():collect(v)
  elif isinstance(value,list):
   if len(value)>1 and isinstance(value[0],str) and isinstance(value[1],str):allowed.add((value[0],value[1]))
   else:
    for v in value:collect(v)
 collect(EP)
 assert all((p['w'],p['t']) in allowed for p in st['lines'] if p['w']!='narr');checks.append('all_executed_spoken_lines_are_source_text')
 result=dict(viewport=[w,h],touch=w<1000,checks=checks,spoken_lines=sum(p['w']!='narr' for p in st['lines']),effects=sorted(set(st['effects'])),final=st,errors=t.errors,failed_requests=t.failed,bad_responses=t.bad)
 await c.close();return result

async def main(args):
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);runs=[]
  for w,h in ([(1280,720)] if args.desktop_only else [(844,390)] if args.mobile_only else [(1280,720),(844,390)]):
   folder=out/f'{w}x{h}';folder.mkdir(exist_ok=True);r=await run(b,folder,w,h,args.discovery_only);runs.append(r);print(json.dumps({k:v for k,v in r.items() if k!='final'},ensure_ascii=False),flush=True)
  await b.close()
 (out/'report.json').write_text(json.dumps(runs,ensure_ascii=False,indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',default='/tmp/daram-source-qa');a.add_argument('--desktop-only',action='store_true');a.add_argument('--discovery-only',action='store_true');a.add_argument('--mobile-only',action='store_true');asyncio.run(main(a.parse_args()))
