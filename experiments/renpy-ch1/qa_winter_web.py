"""Real browser input through the fourteen-day scenario. State observations are read-only."""
import asyncio,json,shutil,hashlib,argparse
from pathlib import Path
from playwright.async_api import async_playwright
from qa_web import Trial
R=Path(__file__).resolve().parent
D=json.loads((R/'game/winter-story.json').read_text())
W=json.loads((R/'game/winter-world.json').read_text())
class WinterTrial(Trial):
 async def state(self):return await asyncio.wait_for(self.page.evaluate('renpy_exec("import renpy; result=renpy.store.winter_observe()")'),30)
 async def advance(self,until='hub',limit=300):
  for _ in range(limit):
   s=await self.state()
   if s.get('actor')=='guard' and s.get('portrait')=='guard' and not getattr(self,'guard_shot',False):
    await self.shot('guard-dialogue');self.guard_shot=True
   if s.get(until):await self.page.wait_for_timeout(450);return s
   if s['choice']:
    await self.click(410,245)
   else:await self.click(1050,685)
  await self.shot('stalled');raise AssertionError(await self.state())
 async def move(self,loc):
  pos={'gate':(190,330),'square':(550,310),'post':(930,310),'inn':(220,470),'workshop':(580,470),'room':(930,470),'passage':(930,590)}
  if (await self.state())['state']['location']==loc:return
  await self.click(458,660);await self.wait('map');await self.click(*pos[loc]);await self.wait('hub')
  assert (await self.state())['state']['location']==loc
 async def open_person(self,who):
  s=await self.state()
  if who=='mom':await self.click(620,265)
  else:
   row=next(r for r in s['people'] if r[0]==who);_,x,y,w,h,pose=row
   await self.click(x+w/2,y+h*.4)
  await self.advance('topics')
 async def close_topics(self):
  await self.click(300,565);await self.wait('hub')
 async def act(self,key):
  destination=D['actions'][key]['place']
  owner=W['owners'].get(key)
  if owner and owner!='mom':
   destination=(await self.state())['whereabouts'][owner]
   assert destination,(key,'owner unavailable')
  await self.move(destination)
  if key in W['owners']:await self.open_person(W['owners'][key])
  else:
   obj=next(v for v in W['places'][D['actions'][key]['place']]['objects'].values() if key in v['actions'])
   x,y,w,h=obj['rect'];await self.click(x+w/2,y+h/2);await self.advance('topics')
  s=await self.state();i=s['topic_options'].index(key)+(s['target_kind']=='person')
  # Four rows fit above the fold. Scroll with actual mouse wheel (desktop)
  # or swipe (touch) for a later interview topic.
  offset=0
  if i>=4:
   scale=min(self.width/1280,self.height/720);left=(self.width-1280*scale)/2;top=(self.height-720*scale)/2
   if self.width<1000:
    cdp=await self.page.context.new_cdp_session(self.page)
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':left+350*scale,'y':top+490*scale}]})
    for y in (460,420,380,340,300):await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':left+350*scale,'y':top+y*scale}]})
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});await cdp.detach()
   else:
    await self.page.mouse.move(left+350*scale,top+430*scale);await self.page.mouse.wheel(0,800)
   await self.page.wait_for_timeout(500)
   count=len(s['topic_options'])+(s['target_kind']=='person')+(s['target_kind']=='person' and s['target_id']!='mom');offset=count*68-10-310
  await self.click(300,253+i*68-offset)
  if D['actions'][key]['cost']:
   await self.wait('confirm');await self.click(365,396)
  for _ in range(200):
   st=await self.state()
   if st['topics'] or st['hub']:break
   if st['choice']:await self.click(410,245)
   else:await self.click(1050,685)
  await self.page.wait_for_timeout(450)
  assert key in (await self.state())['state']['done'],(key,await self.state())
  if key in ('granny','bed','mother'):await self.shot('topic-'+key)
  if (await self.state())['topics']:await self.close_topics()
 async def rest(self):
  await self.click(820,660);await self.wait('confirm');await self.click(365,360)
 async def hearing(self,winning=True):
  await self.advance('board')
  while (await self.state())['board']:
   s=await self.state();c=D['claims'][s['hearing']]['claims'][s['claim_index']]
   paths=[p for p in c['paths'] if set(p)<=set(s['state']['evidence'])]
   if winning and paths:
    await self.click(410,615);await self.wait('evidence')
    inv=s['state']['evidence'];page=0
    for k in reversed(paths[0]):
     index=inv.index(k);wanted=index//8
     while page<wanted:
      await self.click(225,633);page+=1;await self.wait('evidence_page',page)
     while page>wanted:
      await self.click(88,633);page-=1;await self.wait('evidence_page',page)
     slot=index%8;await self.click(180+(slot%2)*360,175+(slot//2)*106)
     await self.page.wait_for_timeout(350)
     selected=(await self.state())['evidence_selected'];assert k in selected,(k,selected,await self.state())
    await self.shot('proof-'+c['id']);await self.click(415,633)
   else:await self.click(775,615)
   # Stop when next board, hub, or ending becomes visible.
   for _ in range(150):
    await self.click(1060,685);s=await self.state()
    if s['board'] or s['hub'] or s['ending']:break
   await self.page.wait_for_timeout(500)
   if s['hub'] or s['ending']:return s
  return await self.state()
 async def save(self):
  await self.click(1125,43);await self.wait('saving');await self.click(760,245);await self.click(265,590);await self.wait('hub')
 async def load(self):
  await self.click(1212,43);await self.wait('menu');await self.click(780,243);await self.wait('loading');await self.click(760,245);await self.wait('hub')
async def run(browser,width,height,full,out):
 c=await browser.new_context(viewport={'width':width,'height':height},has_touch=width<1000,is_mobile=width<1000)
 p=await c.new_page();t=WinterTrial(p,width,height,out);out.mkdir(parents=True,exist_ok=True)
 await p.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/')
 await p.wait_for_function("typeof renpy_exec==='function'",timeout=60000)
 await t.state();await t.click(300,423)
 await t.advance('choice');await t.shot('checkpoint')
 await t.click(420,245);await t.advance();await t.shot('inn')
 s=await t.state();assert s['state']['day']==1 and not s['pulse'];assert s['music']
 # The reception dialogue is initiated by clicking Granny, never auto-played.
 await t.open_person('granny');assert 'inn_registered' in (await t.state())['state']['facts']
 await t.shot('questions');await t.close_topics()
 # Object inspection and empty clicks persist independently of paid actions.
 await t.move('room');before_free=(await t.state())['state']
 await t.click(460,200);await t.advance();await t.click(390,570);await t.advance()
 inspected=(await t.state())['state'];assert inspected['period']==before_free['period'] and len(inspected['checks'])==2
 await t.shot('room-checks');await t.move('gate');await t.move('room');assert (await t.state())['state']['checks']==inspected['checks']
 await t.act('karo');await t.act('post');await t.act('granny')
 # Read again at zero AP; no evidence, facts or time may be duplicated.
 await t.open_person('granny');free_before=(await t.state())['state']
 await t.click(300,321);await t.advance('topics');assert (await t.state())['state']==free_before
 await t.close_topics()
 await t.act('letter')
 assert (await t.state())['state']['period']==0
 await t.move('gate');await t.open_person('guard')
 await t.click(300,321);await t.advance('topics')
 assert 'routine:guard' in (await t.state())['state']['seen']
 await t.close_topics()
 await t.click(650,665);await t.wait('confirm');await t.click(365,396);await t.wait('hub')
 assert (await t.state())['state']['period']==1
 await t.click(458,660);await t.wait('map');await t.shot('known-routine-map');await t.click(190,330);await t.wait('hub')
 before=(await t.state())['state'];await t.save();await t.move('gate');await t.load()
 assert (await t.state())['state']==before,'save/load did not restore all state'
 await p.reload();await p.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(300,498);await t.wait('loading');await t.click(760,245);await t.wait('hub')
 assert (await t.state())['state']==before,'browser refresh persistence'
 if full:
  route=[['appointment','receipt','bed'],['ritual','meter','witness'],['protect','surveillance','timing'],['hidden','mother','symptoms'],['repair','fuel','escape'],['ledger','order','death'],[],[],[],[],[],[]]
  for day in range(1,14):
   await t.rest()
   if day in (3,6,13):await t.hearing()
   else:await t.advance()
   s=await t.state();print('DAY',day,'NEXT',s['state']['day'],s['state']['ending'],flush=True)
   if day<13:
    assert s['state']['day']==day+1
    for action in route[day-1]:await t.act(action)
    if day in (1,4,6):await t.shot('day'+str(day+1))
    if day==7:
     await t.open_person('granny')
     assert 'hello:granny:week2:protected' in (await t.state())['state']['seen']
     await t.shot('week2-granny');await t.close_topics()
    if day==8:
     await t.move('square');await t.open_person('resident_tori')
     assert 'hello:resident_tori:week2' in (await t.state())['state']['seen']
     before_repeat=(await t.state())['state']
     # Read an old appointment again: no new map, cost or duplicate memory.
     await t.click(300,321);await t.advance('topics')
     assert (await t.state())['state']==before_repeat
     await t.shot('week2-tori');await t.close_topics()
  s=await t.state();assert s['ending'] and s['state']['ending']=='truth',s
  await t.shot('true-ending')
 else:
  for day in range(1,14):
   await t.rest()
   if day in (3,6,13):await t.hearing(False)
   else:await t.advance()
   s=await t.state();assert s['state']['day']==day+1
   if day==1:
    await t.move('square');await t.act('appointment');await t.shot('touch-investigation')
  assert s['ending'] and s['state']['ending']=='separated',s
  await t.shot('touch-ending')
 assert not t.errors and not t.bad and not t.failed,(t.errors,t.bad,t.failed)
 await c.close();return dict(viewport=[width,height],full_route=True,strategy='prepared' if full else 'insufficient',ending='truth' if full else 'separated',errors=t.errors,injected_progress=False)
async def main():
 a=argparse.ArgumentParser();a.add_argument('--desktop-only',action='store_true');args=a.parse_args()
 results=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  tasks=[run(b,1280,720,True,Path('/tmp/winter-qa/pc'))]
  if not args.desktop_only:tasks.append(run(b,844,390,False,Path('/tmp/winter-qa/touch')))
  results=await asyncio.gather(*tasks)
  await b.close()
 report=dict(game_zip_sha256=hashlib.sha256((R.parents[1]/'preview/renpy-ch1-test/game.zip').read_bytes()).hexdigest(),routes=results)
 (R/'WINTER_QA_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report),flush=True)
if __name__=='__main__':asyncio.run(main())
