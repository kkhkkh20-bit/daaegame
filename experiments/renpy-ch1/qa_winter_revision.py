"""Real mouse/touch play of the revised arrival, investigation and fourteen-day endings."""
import asyncio,json,shutil,hashlib,sys
from pathlib import Path
from playwright.async_api import async_playwright
from qa_winter_web import WinterTrial,D,W,R
from qa_web import AUDIO_PROBE
class RevisionTrial(WinterTrial):
 async def advance(self,until='hub',limit=450):
  for _ in range(limit):
   s=await self.state()
   if s.get(until):await self.page.wait_for_timeout(450);return s
   if self.errors:raise AssertionError(self.errors)
   if s['choice']:await self.click(410,245)
   else:await self.click(750,690)
  await self.shot('stalled');raise AssertionError(await self.state())
 async def close_topics(self):
  await self.page.wait_for_timeout(500)
  await self.click(1040,664);await self.wait('hub')
 async def move(self,loc):
  await self.page.wait_for_timeout(500)
  return await super().move(loc)
 async def rest(self):
  await self.page.wait_for_timeout(500)
  return await super().rest()
 async def choose_pair(self,keys):
  s=await self.state();inv=s['state']['evidence'];page=s['evidence_page']
  for k in keys:
   index=inv.index(k);wanted=index//8
   while page<wanted:await self.click(225,633);page+=1;await self.wait('evidence_page',page)
   while page>wanted:await self.click(88,633);page-=1;await self.wait('evidence_page',page)
   slot=index%8;await self.click(180+(slot%2)*360,175+(slot//2)*106)
   assert k in (await self.state())['evidence_selected']
  await self.click(415,633)
 async def select_topic(self,key):
  s=await self.state();tab='activity' if D['actions'][key]['cost'] else 'talk'
  if s['topic_tab']!=tab:
   await self.click(1140 if tab=='activity' else 940,270);await self.page.wait_for_timeout(400);s=await self.state()
  i=s['topic_options'].index(key)+(s['target_kind']=='person' and tab=='talk')
  count=len(s['topic_options'])+(s['target_kind']=='person' and tab=='talk')+(s['target_kind']=='person' and s['target_id']!='mom' and tab=='talk')
  offset=0
  if i>=4:
   scale=min(self.width/1280,self.height/720);left=(self.width-1280*scale)/2;top=(self.height-720*scale)/2
   if self.width<1000:
    cdp=await self.page.context.new_cdp_session(self.page)
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':left+1040*scale,'y':top+596*scale}]})
    for y in (550,500,450,400,340):await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':left+1040*scale,'y':top+y*scale}]})
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await cdp.detach()
   else:
    await self.page.mouse.move(left+1040*scale,top+475*scale);await self.page.mouse.wheel(0,1400)
   await self.page.wait_for_timeout(500);offset=max(0,count*69-9-322)
  await self.click(1040,335+i*69-offset)
 async def act(self,key):
  print(self.width,'ACTION',key,flush=True)
  destination=D['actions'][key]['place'];owner=W['owners'].get(key)
  if owner and owner!='mom':destination=(await self.state())['whereabouts'][owner];assert destination,(key,'absent')
  await self.move(destination)
  if owner:await self.open_person(owner)
  else:
   obj=next(v for v in W['places'][destination]['objects'].values() if key in v['actions']);x,y,w,h=obj['rect']
   await self.click(x+w/2,y+h/2);await self.advance('topics')
  before=(await self.state())['state'];await self.select_topic(key)
  if D['actions'][key]['cost']:
   await self.wait('confirm');await self.shot('activity-confirm');await self.click(365,396)
  for _ in range(250):
   st=await self.state()
   if st['topics'] or st['hub']:break
   if st['choice']:await self.click(410,245)
   else:await self.click(750,690)
  st=await self.state();assert key in st['state']['done'],(key,st)
  assert st['state']['period']-before['period']==D['actions'][key]['cost']
  if st['topics']:await self.close_topics()
 async def save(self,until='hub'):
  await self.click(1100,113);await self.wait('saving');await self.click(760,245);await self.click(265,590);await self.wait(until)
 async def load(self,until='hub'):
  await self.click(1200,113);await self.wait('menu');await self.click(780,243);await self.wait('loading');await self.click(760,245);await self.wait(until)
 async def hearing(self,winning=True):
  await self.advance('board')
  while (await self.state())['board']:
   s=await self.state();c=D['claims'][s['hearing']]['claims'][s['claim_index']]
   paths=[p for p in c['paths'] if set(p)<=set(s['state']['evidence'])]
   await self.shot('hearing-'+c['id'])
   if winning and paths:
    await self.click(410,615);await self.wait('evidence');await self.choose_pair(list(reversed(paths[0])))
   else:await self.click(775,615)
   for _ in range(200):
    await self.click(750,690);s=await self.state()
    if s['board'] or s['hub'] or s['ending']:break
   await self.page.wait_for_timeout(500)
   if s['hub'] or s['ending']:return s
  return await self.state()
async def run(browser,width,height,full):
 out=Path('/tmp/winter-revision')/str(width);out.mkdir(parents=True,exist_ok=True)
 c=await browser.new_context(viewport={'width':width,'height':height},has_touch=width<1000,is_mobile=width<1000)
 await c.add_init_script(AUDIO_PROBE)
 p=await c.new_page();t=RevisionTrial(p,width,height,out)
 await p.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/')
 await p.wait_for_function("typeof renpy_exec==='function'",timeout=60000)
 await t.state();await t.click(300,423);await p.wait_for_timeout(1200)
 st=await t.state();assert st['presentation']['bg']=='winter_carriage',st
 await t.shot('carriage');assert st['music']=='assets/travel.mp3'
 audio=await p.evaluate('__probeAudio()')
 assert any(a['state']=='running' and a['rms']>1e-5 for a in audio),'No browser audio output'
 typing=False
 for _ in range(6):
  await t.click(750,690);typing |= bool((await t.state())['typing'])
 assert typing,'No typing sound during carriage dialogue'
 await t.click(900,113);await t.wait('calendar');await t.shot('calendar-first-day');await t.click(1140,650)
 await t.advance('entry');await t.shot('gate-investigation')
 for x in (177,459,741):
  await t.click(x,650);await t.advance('entry')
 before=(await t.state())['state'];assert before['period']==0
 await t.save('entry');await t.click(1023,650);await t.wait('evidence');await t.choose_pair(['invitation','entry_copy']);await t.advance('entry')
 assert not 'entry_corrected' in (await t.state())['state']['facts']
 await t.load('entry');assert (await t.state())['state']==before
 await t.click(1023,650);await t.wait('evidence');await t.choose_pair(['entry_copy','entry_permit']);await t.advance('choice');await t.shot('entry-inference')
 await t.click(450,330);await t.advance();assert 'entry_corrected' in (await t.state())['state']['facts']
 await t.open_person('granny');await t.shot('centered-questions');await t.close_topics()
 for key in ('granny','post','karo','karo_sighting','doto_sighting'):await t.act(key)
 assert 'sightings' in (await t.state())['state']['evidence']
 before=(await t.state())['state'];await t.save();await t.move('room');await t.load();assert (await t.state())['state']==before
 await p.reload();await p.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(300,498);await t.wait('loading');await t.click(760,245);await t.wait('hub');assert (await t.state())['state']==before
 route=[['appointment','receipt','bed'],['ritual','meter','witness'],['protect','surveillance','timing'],['hidden','mother','symptoms'],['repair','fuel','escape'],['ledger','order','death'],[],[],[],[],[],[]]
 for day in range(1,14):
  await t.rest()
  if day in (3,6,13):await t.hearing(full)
  else:await t.advance()
  st=await t.state();print(width,'DAY',st['state']['day'],st['state']['ending'],flush=True)
  if day<13:
   assert st['state']['day']==day+1
   if full:
    for key in route[day-1]:await t.act(key)
    if day==1:
     await t.move((await t.state())['whereabouts']['doto']);await t.open_person('doto');assert 'doto_recanted' in (await t.state())['state']['facts'];await t.shot('recanted');await t.close_topics()
     await t.act('doto_fear');await t.click(650,665);await t.wait('confirm');await t.click(365,396);await t.wait('hub');await t.act('warm_home');assert 'doto_supported' in (await t.state())['state']['facts']
    if day==2:assert st['state']['day']==3
   elif day==1:
    # No map, appointment or replay unlock: discover by place and world time.
    await t.move('post');await t.click(450,337);await t.advance()
    assert 'service_hint' in (await t.state())['state']['facts']
    for _ in range(2):
     await p.wait_for_timeout(500);await t.click(650,665);await t.wait('confirm');await t.click(365,396);await t.wait('hub')
    await t.move('square');await t.click(1150,480);await t.advance('choice');await t.shot('timed-cart-choice')
    await t.click(450,330);await t.advance()
    st=await t.state();assert 'transfer_seal' in st['state']['evidence'] and not st['state']['marks']
    before=st['state'];await t.save();await t.move('inn');await t.load();assert (await t.state())['state']==before
    await p.wait_for_timeout(500);await t.click(1150,480);await t.advance()
    assert (await t.state())['state']['evidence'].count('transfer_seal')==1
    await t.move('post');await t.click(450,337);await t.advance()
    st=await t.state();assert st['state']['location']=='passage' and 'passage_known' in st['state']['facts'] and 'map' not in st['state']['evidence']
    await t.shot('first-run-secret-passage')
 expected='truth' if full else 'separated';st=await t.state();assert st['ending'] and st['state']['ending']==expected,st
 await t.shot(expected+'-ending')
 assert not t.errors and not t.bad and not t.failed,(t.errors,t.bad,t.failed)
 await c.close()
 return {'viewport':[width,height],'ending':expected,'entry_wrong_proof_rejected':True,'calendar_from_carriage':True,'two_witnesses_verified':True,'save_reload':True,'actual_audio_output':True,'typing_sound':typing,'first_run_timed_route':not full,'real_input_only':True,'errors':t.errors}
async def main():
 artifact=R.parents[1]/'preview/renpy-ch1-test/game.zip'
 tested_hash=hashlib.sha256(artifact.read_bytes()).hexdigest()
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  results=await asyncio.gather(run(b,1280,720,True),run(b,844,390,False))
  await b.close()
 assert hashlib.sha256(artifact.read_bytes()).hexdigest()==tested_hash,'Build changed during browser verification'
 report={'game_zip_sha256':tested_hash,'routes':results}
 (R/'WINTER_REVISION_QA_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':asyncio.run(main())
