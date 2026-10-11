"""Actual New Game: passive frame observations of audio lead, visuals and night.

Clean wrapper/payload bytes are frozen. Native input advances the whole intro.
Separate slow/failing music cases change only network loading, then exercise
the real recovery button. No game state, dialogue or direction is injected.
"""
import argparse, asyncio, hashlib, json, shutil
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin
from playwright.async_api import async_playwright

OBSERVER=r'''(()=>{
 if(!/play_v2\.html$/.test(location.pathname))return;
 window.__qaFlow={frames:[],stopped:false};
 function visible(e){if(!e)return false;var r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility==='visible'&&+s.opacity>.02}
 (function frame(){if(__qaFlow.stopped)return;
  var q=s=>document.querySelector(s),f=window.__innSceneFlowState&&__innSceneFlowState(),m=window.__AUD&&__AUD.mediaPlaying&&__AUD.mediaPlaying(),n=window.__innOpeningDirection&&__innOpeningDirection();
  var black=q('#inn-scene-black'),opacity=black?+getComputedStyle(black).opacity:0;
  __qaFlow.frames.push({t:performance.now(),flow:f,media:m,black:opacity,
   card:visible(q('.banner,.placecard')),line:visible(q('#dtxt,#vnbox .vtxt'))?q('#dtxt,#vnbox .vtxt').innerText:'',
   night:n?{cue:n.cue,actor:n.actor,ready:n.ready}:null,
   bami:Array.from(document.querySelectorAll('#innstage .isf[data-k="geokkuri"]')).filter(visible).length,
   cg:q('#inn-story-cg')?.dataset.cut,oldFigure:visible(q('#vnfig')),retry:visible(q('.scene-retry'))});
  requestAnimationFrame(frame);
 })();
})();'''

async def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--url',default='http://127.0.0.1:8000/v2.html');ap.add_argument('--version',required=True);ap.add_argument('--output',default='/tmp/scene-flow');a=ap.parse_args()
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 wrapper=urlopen(a.url).read();payload_url=urljoin(a.url,'play_v2.html');payload=urlopen(payload_url).read()
 assert hashlib.sha256(payload).hexdigest()[:12]==a.version
 reports=[]
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
  for case in ('full_intro','slow_music','failed_music'):
   context=await browser.new_context(viewport={'width':844,'height':390});await context.add_init_script(OBSERVER)
   await context.route('**/v2.html*',lambda route:route.fulfill(status=200,body=wrapper,content_type='text/html'))
   await context.route('**/play_v2.html*',lambda route:route.fulfill(status=200,body=payload,content_type='text/html'))
   attempts=0
   async def music(route):
    nonlocal attempts
    attempts+=1
    if case=='slow_music' and attempts==1:await asyncio.sleep(2.2)
    if case=='failed_music' and attempts==1:await route.fulfill(status=503,body='intentional QA music fault')
    else:await route.continue_()
   if case!='full_intro':await context.route('**/audio/v4/friend-context-v4.mp3',music)
   page=await context.new_page();errors=[];bad=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:bad.append([r.status,r.url]) if r.status>=400 and 'favicon' not in r.url else None)
   await page.goto(a.url,wait_until='domcontentloaded');await page.locator('#game').wait_for()
   frame=await (await page.locator('#game').element_handle()).content_frame()
   await frame.locator('#innmain [data-m="new"]').click(timeout=25000)
   if case=='failed_music':
    await frame.locator('.scene-retry').wait_for(state='visible',timeout=15000)
    assert await frame.evaluate('__innSceneFlowState().black')
    await page.screenshot(path=str(out/(case+'-retry.png')))
    await frame.locator('.scene-retry').click()
   await frame.wait_for_function('__innSceneFlowState()?.settled&&!!document.querySelector("#vnbox .vtxt,#dtxt")?.innerText',timeout=25000)
   if case=='full_intro':
    for i in range(850):
     if await frame.evaluate('!__innSceneFlowState()&&!document.querySelector(".banner,.placecard")&&!!document.querySelector("#bigscene")'):break
     await page.keyboard.press('Enter');await page.wait_for_timeout(180)
    else:raise AssertionError('Intro did not finish')
   await frame.evaluate('__qaFlow.stopped=true');trace=await frame.evaluate('__qaFlow.frames')
   (out/(case+'-frames.json')).write_text(json.dumps(trace,ensure_ascii=False))
   entries={}
   for row in trace:
    f=row.get('flow')
    if not f:continue
    e=entries.setdefault(f['sid'],{'blackFrames':0,'audibleBlackFrames':0,'reveal':None})
    if row['black']>.995:
     e['blackFrames']+=1;m=row.get('media') or {}
     if m.get('started') and m.get('key')==f['music'] and (m.get('now') or 0)>=(m.get('at') or 0) and m.get('busGain',0)>0:e['audibleBlackFrames']+=1
    if f.get('revealAt') and not e['reveal']:e['reveal']=f
   for sid,e in entries.items():
    assert e['blackFrames']>0,(case,sid,e)
    reveal=e['reveal'];assert reveal,(case,sid,e)
    assert not reveal['bypass'],('Expected sound-enabled native entry',case,sid,reveal)
    assert e['audibleBlackFrames']>0,(case,sid,e)
    assert reveal['audioClock']-reveal['audioAt']>=.279,(case,sid,e)
   if case=='full_intro':
    assert set(entries)=={'P1','P2','P3','P5','P10','P10b','P11','P12','P13'},entries
    night=[r for r in trace if r.get('night') and r['flow'] and r['flow']['sid']=='P10b' and r['black']==0]
    assert {'home','out','touch','eyes','bami','return'}<=set(r['night']['cue'] for r in night)
    assert all(r['bami']==0 for r in night if r['night']['cue']!='bami'),[r for r in night if r['night']['cue']!='bami' and r['bami']]
    assert any(r['night']['cue']=='bami' and r['bami']==1 for r in night)
    assert not any(r['oldFigure'] for r in trace if r.get('cg') in ('carriage','driver','village') and r['black']==0)
   assert not errors,errors
   assert not bad if case!='failed_music' else len(bad)==1 and bad[0][0]==503,bad
   reports.append({'case':case,'frames':len(trace),'entries':entries,'errors':errors,'httpFaults':bad})
   print('PASS',case,len(trace),'frames',list(entries),flush=True)
   await context.close()
  await browser.close()
 (out/'report.json').write_text(json.dumps({'version':a.version,'cases':reports},ensure_ascii=False,indent=2))

if __name__=='__main__':asyncio.run(main())
