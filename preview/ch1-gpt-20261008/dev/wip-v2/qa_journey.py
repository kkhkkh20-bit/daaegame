"""Native new-game journey, first-paint theme and primary-picture recovery.

Freeze the clean published bytes. Only network faults/delays are injected;
game state, scene cursors and dialogue are never injected or advanced by eval.
"""
import argparse, asyncio, hashlib, json, shutil
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin
from playwright.async_api import async_playwright

OBSERVE = r'''(()=>{
 window.__qaJourney=[];
 function seen(e){if(!e)return false;var r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility==='visible'&&s.display!=='none'&&+s.opacity>.05}
 (function frame(){
  var q=s=>document.querySelector(s),p=window.__innPresentationState&&__innPresentationState(),f=window.__innSceneFlowState&&__innSceneFlowState(),b=q('#inn-boot,#bootld'),black=q('#inn-scene-black'),label=q('.cinema-world-label text'),line=q('#dtxt,#vnbox .vtxt');
  __qaJourney.push({t:performance.now(),boot:seen(b)?{bg:getComputedStyle(b).backgroundColor,font:getComputedStyle(q('.boot-copy')).fontFamily}:null,
   sid:p&&p.sid,camera:p&&p.camera,ready:p&&p.ready,visual:p&&p.visualReady,cut:q('#inn-story-cg')?.dataset.cut,
   black:black?+getComputedStyle(black).opacity:0,line:seen(line)?line.innerText:'',label:label?{text:label.textContent,y:label.getBoundingClientRect().bottom}:null,
   panelTop:q('#vnbox .vtxt')?.getBoundingClientRect().top,old:seen(q('#vnfig')),retry:seen(q('.cinema-retry'))});
  requestAnimationFrame(frame);
 })();
})();'''

async def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--url',default='http://127.0.0.1:8000/v2.html')
 ap.add_argument('--version',required=True)
 ap.add_argument('--output',default='/tmp/journey-qa')
 args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 wrapper=urlopen(args.url).read();payload=urlopen(urljoin(args.url,'play_v2.html')).read()
 assert hashlib.sha256(payload).hexdigest()[:12]==args.version
 reports=[]
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  for case in ('slow_picture','failed_picture'):
   context=await browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce' if case=='failed_picture' else 'no-preference')
   await context.add_init_script(OBSERVE)
   await context.route('**/v2.html*',lambda r:r.fulfill(status=200,body=wrapper,content_type='text/html'))
   async def game(route):
    await asyncio.sleep(.8)
    await route.fulfill(status=200,body=payload,content_type='text/html')
   await context.route('**/play_v2.html*',game)
   frame=None;attempts=0
   async def picture(route):
    nonlocal attempts
    attempts+=1
    if attempts==1 and case=='failed_picture':
     await route.fulfill(status=503,body='intentional QA picture fault');return
    if attempts==1 and case=='slow_picture':
     while frame is None:await asyncio.sleep(.02)
     await frame.wait_for_function('__innPresentationState().camera==="postoffice"',timeout=45000)
     await asyncio.sleep(1.8)
    await route.continue_()
   await context.route('**/art/ch1/cinematics/post-office-closed-exterior.png',picture)
   page=await context.new_page();errors=[];bad=[];requests=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append([r.status,r.url]) if r.status>=400 else None)
   page.on('request',lambda r:requests.append(r.url))
   await page.goto(args.url,wait_until='domcontentloaded')
   await page.locator('#inn-boot').wait_for(state='visible')
   await page.screenshot(path=str(out/(case+'-wrapper-loader.png')))
   frame=await (await page.locator('#game').element_handle()).content_frame()
   await frame.locator('#innmain [data-m="new"]').wait_for(timeout=25000)
   await frame.locator('#bootld').wait_for(state='detached',timeout=25000)
   assert not any('/cinematics/' in u for u in requests),'Journey art competed with first menu load'
   assert await page.locator('#inn-boot').count()==0,'Wrapper did not hand over to child loader'
   await frame.locator('#innmain [data-m="new"]').click()
   recovered=False;snaps=set()
   for _ in range(350):
    if await frame.locator('.cinema-retry').count():
     assert case=='failed_picture' and not recovered
     assert await frame.evaluate('__innSceneFlowState().black')
     await page.screenshot(path=str(out/(case+'-retry.png')))
     await frame.locator('.cinema-retry').click();recovered=True
    state=await frame.evaluate('(()=>{var p=__innPresentationState();return {sid:p.sid,camera:p.camera,ready:p.ready,cue:p.cue}})()')
    if state['ready'] and state['camera'] in ('approach','postoffice','innentrance') and state['camera'] not in snaps:
     await page.screenshot(path=str(out/(case+'-'+state['camera']+'.png')));snaps.add(state['camera'])
    if state['sid']=='P3' and state['camera']=='stage' and '어서 와요' in state['cue']:break
    await page.keyboard.press('Enter');await page.wait_for_timeout(180)
   else:raise AssertionError(('Journey stalled',case,state))
   parent=await page.evaluate('__qaJourney');rows=await frame.evaluate('__qaJourney')
   for trace in (parent,rows):
    boots=[r['boot'] for r in trace if r['boot']]
    assert boots,('First-paint loader not observed',case)
    assert all(r['bg']=='rgb(33, 27, 22)' and 'Galmuri11' in r['font'] for r in boots),boots
   assert not any(r['old'] for r in rows if r['cut'] and r['black']==0),'Old actor overlaps primary picture'
   closed=[r for r in rows if r['ready'] and '우체국 문 닫혔어' in r['line']]
   assert closed and all(r['camera']=='postoffice' and r['label'] and r['label']['text']=='닫음' and r['label']['y']<r['panelTop'] for r in closed),closed[:2]
   cuts=[]
   for r in rows:
    if r['ready'] and (not cuts or cuts[-1]!=[r['sid'],r['camera']]):cuts.append([r['sid'],r['camera']])
   assert cuts==[['P1','carriage'],['P1','approach'],['P1','driver'],['P2','village'],['P2','postoffice'],['P2','village'],['P2','innentrance'],['P3','innentrance'],['P3','stage']],cuts
   held=[r for r in rows if r['camera']=='postoffice' and not r['visual']]
   assert held and all(r['black']>.99 and not r['line'] for r in held),held[:2]
   assert not errors,errors
   assert not bad if case=='slow_picture' else len(bad)==1 and bad[0][0]==503,bad
   assert recovered if case=='failed_picture' else not recovered
   report={'case':case,'frames':len(rows),'wrapperFrames':len(parent),'cameraOrder':cuts,'heldFrames':len(held),'errors':errors,'faults':bad,'recovered':recovered}
   reports.append(report);(out/(case+'-frames.json')).write_text(json.dumps(rows,ensure_ascii=False))
   print('PASS',case,report,flush=True);await context.close()
  await browser.close()
 (out/'report.json').write_text(json.dumps({'version':args.version,'cases':reports},ensure_ascii=False,indent=2))

if __name__=='__main__':asyncio.run(main())
