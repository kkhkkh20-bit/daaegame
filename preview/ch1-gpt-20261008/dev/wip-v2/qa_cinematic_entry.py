"""Observe native opening entry from document start, before any CG is ready.

Actual New Game, main-menu Continue, and administrator Opening are clicked in
the clean published wrapper. No game state, scenes, dialogue, or evidence are
injected, and no presentation hooks (which can synchronize the renderer) are
called. rAF observations and mutation diagnostics only read DOM/CSS.

Separate media faults delay the family's native image decode Promise after
the actual entry action, or fail its first network request. Those faults alter
only the image environment, to expose uncovered/loading/retry frames. One
Chromium is used, with contexts and cases executed sequentially. The payload
and wrapper are frozen as unchanged bytes so a concurrent build cannot change
the measured version.
"""
import argparse
import asyncio
import hashlib
import json
import shutil
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

from playwright.async_api import async_playwright


OBSERVER = r'''(()=>{
 if(!/\/play_v2\.html$/.test(location.pathname))return;
 const trace={frames:[],changes:[],events:[],rawInputEvents:[],stopped:false};window.__qaEntryTrace=trace;
 let last='',serial=0;const ids=new WeakMap();
 const identity=e=>{if(!e)return null;if(!ids.has(e))ids.set(e,++serial);return ids.get(e)};
 const source=e=>{const s=e&&(e.getAttribute('href')||e.getAttribute('src'));return s&&s.startsWith('data:')?'embedded:'+s.length:s};
 function view(e){
  if(!e)return null;const r=e.getBoundingClientRect(),own=getComputedStyle(e);
  let opacity=1,show=r.width>0&&r.height>0&&own.visibility==='visible';
  for(let p=e;p&&p.nodeType===1;p=p.parentElement){const s=getComputedStyle(p);show=show&&s.display!=='none';opacity*=+s.opacity}
  return {id:identity(e),show,opacity,box:[r.x,r.y,r.width,r.height],src:source(e),
   zIndex:own.zIndex,pointerEvents:own.pointerEvents,
   classes:e.className&&e.className.baseVal||String(e.className||''),
   decoded:e.tagName==='IMG'?e.complete&&e.naturalWidth>0:null};
 }
 function full(v){return !!(v&&v.show&&v.opacity>.995&&v.box[0]<=1&&v.box[1]<=1&&v.box[0]+v.box[2]>=innerWidth-1&&v.box[1]+v.box[3]>=innerHeight-1)}
 function snap(kind){
  const q=s=>document.querySelector(s),cg=q('#inn-story-cg'),world=q('#bigscene'),line=q('#dtxt,#vnbox .vtxt');
  const s={t:performance.now(),timeOrigin:performance.timeOrigin,kind,url:location.href,
   body:document.body?.className||'',boot:view(q('#bootld')),main:view(q('#innmain')),admin:view(q('#inn-admin')),
   cg:view(cg),cut:cg?.dataset.cut||null,owner:cg?.dataset.owner||null,picture:view(cg?.querySelector('.cinema-picture')),
   cgCount:document.querySelectorAll('#inn-story-cg').length,app:view(q('#app')),world:view(world),
   bg:q('#bigscene>svg[data-bg]')?.dataset.bg||null,legacySeat:view(q('image.innseat')),
   oldFigure:view(q('#vnfig')),oldStage:view(q('#innstage')),banner:view(q('.banner,.placecard')),
   bannerText:q('.banner,.placecard')?.innerText||'',lineView:view(line),line:line?.innerText||'',
   retry:view(q('.cinema-retry')),fault:window.__qaImageFault?{...window.__qaImageFault}:null};
  const cover=full(s.boot)||full(s.main)||full(s.admin)||full(s.cg);
  s.covered=cover;s.cgReady=!!(s.cg?.show&&s.cg.opacity>.995&&cg.classList.contains('ready')&&s.picture?.decoded);
  s.rawWorld=!!(s.world?.show&&s.world.opacity>.005&&!cover);
  s.rawLegacySeat=!!(s.legacySeat?.show&&s.legacySeat.opacity>.005&&!cover);
  s.rawOldFigure=!!(s.oldFigure?.show&&s.oldFigure.opacity>.005&&!cover);
  s.earlyDialogue=!!(s.line&&s.lineView?.show&&s.lineView.opacity>.005&&s.cut==='carriage'&&!s.cgReady);
  const k=JSON.stringify([s.body,s.boot?.opacity,s.main?.show,s.cg?.id,s.cg?.classes,s.picture?.decoded,s.bg,
   s.world?.show,s.legacySeat?.show,s.oldFigure?.show,s.rawWorld,s.rawLegacySeat,s.earlyDialogue,s.bannerText,s.line]);
  if(kind==='raf')trace.frames.push(s);
  if(k!==last){trace.changes.push(s);last=k}return s;
 }
 window.__qaEntryDOM=function(){return snap('read')};
 new MutationObserver(()=>snap('mutation')).observe(document,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style','href','src']});
 document.addEventListener('click',e=>{const b=e.target.closest?.('[data-m],[data-admin-scene],[data-w],.cinema-retry');
  if(b)trace.events.push({t:performance.now(),timeOrigin:performance.timeOrigin,html:b.outerHTML.slice(0,250)})},true);
 ['pointerdown','pointerup','click'].forEach(type=>window.addEventListener(type,e=>{
  if(document.querySelector('.cinema-retry'))trace.rawInputEvents.push({t:performance.now(),type,trusted:e.isTrusted,connected:e.target.isConnected,html:e.target.outerHTML.slice(0,250)})
 },true));
 (function frame(){if(trace.stopped)return;snap('raf');requestAnimationFrame(frame)})();
})();'''


DECODE_FAULT = r'''(()=>{
 if(!/\/play_v2\.html$/.test(location.pathname))return;
 const nativeDecode=HTMLImageElement.prototype.decode;if(!nativeDecode)throw Error('Native decode is required');
 const info={calls:0,pending:0,gate:null,released:null,delayMs:__DELAY__};window.__qaImageFault=info;
 let release,gateStarted=false;const gate=new Promise(r=>release=r);
 function open(reason){if(gateStarted)return;gateStarted=true;info.gate={t:performance.now(),reason};
  setTimeout(()=>{info.released=performance.now();release()},info.delayMs)}
 document.addEventListener('click',e=>{const b=e.target.closest?.('[data-m="new"],[data-m="cont"]');if(b)open('native:'+b.dataset.m)},true);
 if(new URLSearchParams(location.search).get('testScene')==='cold'){
  window.addEventListener('load',()=>{(function wait(){if(document.querySelector('#bootld')){setTimeout(wait,20);return}open('admin:cold:boot-removed')})()});
 }
 HTMLImageElement.prototype.decode=function(){
  const decoded=nativeDecode.apply(this,arguments);
  if(!/\/carriage-family-close\.png(?:\?|$)/.test(this.src))return decoded;
  info.calls++;info.pending++;
  return Promise.resolve(decoded).then(()=>gate).finally(()=>{info.pending--});
 };
})();'''


STOP_OBSERVER = r'''(()=>{
 if(!/\/play_v2\.html$/.test(location.pathname))return;
 const stops=[];window.__qaMediaStops=stops;
 ['stopPropagation','stopImmediatePropagation','preventDefault'].forEach(name=>{
  const original=Event.prototype[name];Event.prototype[name]=function(){
   if(document.querySelector('.cinema-retry')){
    const c=this.currentTarget;stops.push({t:performance.now(),method:name,type:this.type,
     target:this.target?.outerHTML?.slice(0,250)||String(this.target),currentTarget:c===window?'window':c===document?'document':c?.outerHTML?.slice(0,200)||String(c),
     stack:new Error('media input observation').stack});
   }
   return original.apply(this,arguments);
  };
 });
})();'''


def summary(trace):
    frames = trace['frames']
    ready = [r for r in frames if r['cgReady'] and r['cut'] == 'carriage']
    first = ready[0]['t'] if ready else None
    opening = [r for r in frames if first is None or r['t'] <= first]
    loading = [r for r in frames if r['cg'] and 'loading' in r['cg']['classes']]
    return {
        'frames': len(frames), 'mutationsAndChanges': len(trace['changes']),
        'documentTimeOrigin': frames[0]['timeOrigin'] if frames else None,
        'firstFrameMs': frames[0]['t'] if frames else None, 'firstFamilyCGMs': first,
        'initialFramesThroughFirstCG': len(opening),
        'rawWorldFrames': sum(r['rawWorld'] for r in frames),
        'rawLegacySeatFrames': sum(r['rawLegacySeat'] for r in frames),
        'rawOldFigureFrames': sum(r['rawOldFigure'] for r in frames),
        'earlyDialogueFrames': sum(r['earlyDialogue'] for r in frames),
        'duplicateCGFrames': sum(r['cgCount'] > 1 for r in frames),
        'loadingFrames': len(loading),
        'loadingSpanMs': loading[-1]['t']-loading[0]['t'] if loading else 0,
        'loadingWithoutCardFrames': sum(bool(r['cg'] and 'loading' in r['cg']['classes'] and not (r['banner'] and r['banner']['show'])) for r in frames),
        'placeCardWithOwnedCGFrames': sum(bool(r['banner'] and r['banner']['show'] and r['cg'] and r['cg']['show'] and r['cut']=='carriage') for r in frames),
        'placeCardWithFamilyCGFrames': sum(bool(r['banner'] and r['banner']['show'] and r['cgReady'] and r['cut']=='carriage') for r in frames),
        'retryFrames': sum(bool(r['retry'] and r['retry']['show']) for r in frames),
        'fault': frames[-1].get('fault') if frames else None,
        'nativeEvents': trace['events'],
        'retryRawInputEvents': trace['rawInputEvents'],
    }


async def get_frame(page):
    await page.locator('#game').wait_for(state='attached')
    return await (await page.locator('#game').element_handle()).content_frame()


async def settle_family(frame):
    await frame.locator('#inn-story-cg.ready[data-cut="carriage"]').wait_for(state='visible',timeout=25000)
    await frame.wait_for_function('!!document.querySelector("#dtxt,#vnbox .vtxt")?.innerText.trim()',timeout=12000)
    await frame.page.wait_for_timeout(350)


async def capture(page, frame, label, output, records, diagnostics, expected_version, delayed=False, expect_retry=False):
    if delayed:
        await frame.wait_for_function('!!document.querySelector("#inn-story-cg.loading")',timeout=12000)
        await page.screenshot(path=str(output/(label+'-loading.png')))
    if expect_retry:
        await frame.locator('.cinema-retry').wait_for(state='visible',timeout=12000)
        await page.screenshot(path=str(output/(label+'-retry.png')))
        diagnostics['retryBeforeClick']=await frame.evaluate('(()=>{const b=document.querySelector(".cinema-retry"),r=b?.getBoundingClientRect();return {dom:__qaEntryDOM(),connected:!!b?.isConnected,onclick:typeof b?.onclick,hit:r?document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.outerHTML.slice(0,250):null}})()')
        await frame.locator('.cinema-retry').click()
        diagnostics['retryAfterClick']=await frame.evaluate('({dom:__qaEntryDOM(),connected:!!document.querySelector(".cinema-retry")?.isConnected,onclick:typeof document.querySelector(".cinema-retry")?.onclick})')
    try:
        await settle_family(frame)
    except Exception:
        trace=await frame.evaluate('window.__qaEntryTrace')
        diagnostics['mediaStops']=await frame.evaluate('window.__qaMediaStops||[]')
        await page.screenshot(path=str(output/(label+'-failed.png')))
        (output/(label+'-failed.json')).write_text(json.dumps({'summary':summary(trace),'trace':trace,'diagnostics':diagnostics},ensure_ascii=False))
        (output/(label+'-failed.html')).write_text(await frame.content())
        raise
    assert 'build='+expected_version in frame.url, frame.url
    assert await frame.evaluate('typeof __T') == 'undefined', 'Production payload contains a QA evaluation hook'
    await page.screenshot(path=str(output/(label+'-ready.png')))
    trace = await frame.evaluate('window.__qaEntryTrace')
    report = summary(trace)
    report.update(label=label,url=frame.url,errors=list(diagnostics['errors']),httpFailures=list(diagnostics['http']),requestFailures=list(diagnostics['failed']),familyNetwork=list(diagnostics['familyNetwork']),forbiddenLoopRequests=list(diagnostics['forbiddenLoopRequests']))
    if expect_retry:
        report['retryBeforeClick']=diagnostics['retryBeforeClick']
        report['retryAfterClick']=diagnostics['retryAfterClick']
    if 'nativeMainReload' in diagnostics:
        report['nativeMainReload']=diagnostics['nativeMainReload']
    (output/(label+'.json')).write_text(json.dumps({'summary':report,'trace':trace},ensure_ascii=False))
    records.append(report)
    assert report['frames'] and report['firstFamilyCGMs'] is not None, report
    assert report['initialFramesThroughFirstCG'] > 1, 'Observer did not include pre-CG frames'
    for key in ('rawWorldFrames','rawLegacySeatFrames','rawOldFigureFrames','earlyDialogueFrames','duplicateCGFrames'):
        assert report[key] == 0, (label,key,report)
    assert not diagnostics['errors'], diagnostics
    assert not diagnostics['http'], diagnostics
    assert not diagnostics['forbiddenLoopRequests'], diagnostics['forbiddenLoopRequests']
    assert report['placeCardWithOwnedCGFrames'] > 0, (label,'Primary picture/loading cover absent beneath first place card')
    if not delayed and not expect_retry:
        assert report['placeCardWithFamilyCGFrames'] > 0, (label,'Family CG absent beneath first place card')
    if delayed:
        assert report['fault'] and report['fault']['calls'] > 0 and report['fault']['gate'], report
        assert report['loadingSpanMs'] >= 1000 and report['loadingFrames'] > 20, (label,'Decode fault did not exercise actual pending entry',report)
        assert report['loadingWithoutCardFrames'] > 20, (label,'Decode fault did not outlast the native place card',report)
        assert report['fault']['pending'] == 0 and report['fault']['released'], report
    if expect_retry:
        assert report['retryFrames'] > 0, report
    print(json.dumps(report,ensure_ascii=False),flush=True)


async def main(args):
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    wrapper=urlopen(args.url).read();payload_url=urljoin(args.url,'play_v2.html')
    payload=urlopen(payload_url).read();payload_hash=hashlib.sha256(payload).hexdigest()
    assert args.version in wrapper.decode(), 'Wrapper does not select requested published version'
    assert payload_hash.startswith(args.version), ('Frozen payload hash differs from requested version',payload_hash,args.version)
    records=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        async def context_for(fault=None):
            context=await browser.new_context(viewport={'width':844,'height':390},service_workers='block')
            await context.add_init_script(OBSERVER)
            if fault=='decode':await context.add_init_script(DECODE_FAULT.replace('__DELAY__',str(args.decode_delay_ms)))
            if fault=='retry':await context.add_init_script(STOP_OBSERVER)
            diagnostics={'errors':[],'http':[],'failed':[],'familyNetwork':[],'forbiddenLoopRequests':[]};requests={'family':0,'aborted':0}
            async def route_media(route):
                if 'carriage-family-close.png' in route.request.url:
                    requests['family']+=1
                    diagnostics['familyNetwork'].append({'event':'request','url':route.request.url,'number':requests['family']})
                    if fault=='retry' and requests['aborted']==0:
                        requests['aborted']+=1;await route.abort('failed');return
                await route.continue_()
            await context.route('**/art/**',route_media)
            await context.route('**/play_v2.html*',lambda route:route.fulfill(body=payload,content_type='text/html; charset=utf-8'))
            await context.route('**/v2.html*',lambda route:route.fulfill(body=wrapper,content_type='text/html; charset=utf-8'))
            page=await context.new_page()
            page.on('pageerror',lambda e:diagnostics['errors'].append(str(e)))
            page.on('request',lambda r:diagnostics['forbiddenLoopRequests'].append(r.url) if 'horse-carriage-loop' in r.url else None)
            def response(r):
                if r.status>=400 and 'favicon' not in r.url:diagnostics['http'].append({'status':r.status,'url':r.url})
                if 'carriage-family-close.png' in r.url:diagnostics['familyNetwork'].append({'event':'response','url':r.url,'status':r.status})
            page.on('response',response)
            page.on('requestfailed',lambda r:diagnostics['failed'].append({'url':r.url,'error':r.failure}))
            cdp=await context.new_cdp_session(page);await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
            await page.goto(args.url,wait_until='domcontentloaded')
            frame=await get_frame(page)
            await frame.locator('#innmain').wait_for(state='visible',timeout=25000)
            return context,page,frame,diagnostics,requests
        try:
            if args.cases in ('all','retry'):
                context,page,frame,diagnostics,requests=await context_for('retry')
                try:
                    await frame.locator('#innmain [data-m="new"]').click()
                    await capture(page,frame,'network-failure-retry',output,records,diagnostics,args.version,expect_retry=True)
                    assert requests['aborted']==1 and requests['family']>=2,requests
                    family_failures=[r for r in diagnostics['failed'] if 'carriage-family-close.png' in r['url']]
                    assert len(family_failures)==1,diagnostics
                finally:await context.close()
            for fault,prefix in ((None,'normal'),('decode','decode-delayed')):
                if args.cases not in ('all','normal' if fault is None else 'delayed'):continue
                context,page,frame,diagnostics,requests=await context_for(fault)
                try:
                    await frame.locator('#innmain [data-m="new"]').click()
                    await capture(page,frame,prefix+'-fresh',output,records,diagnostics,args.version,delayed=fault=='decode')
                    fresh_origin=await frame.evaluate('performance.timeOrigin')
                    await frame.locator('#w209rail [data-more]:visible').first.click()
                    await frame.locator('#w209more [data-w="main"]').click()
                    await frame.locator('#innmain').wait_for(state='visible',timeout=25000)
                    main_origin=await frame.evaluate('performance.timeOrigin')
                    assert main_origin!=fresh_origin, ('Native More→Main must reload its document, rearming the decode environment',fresh_origin,main_origin)
                    diagnostics['nativeMainReload']={'freshTimeOrigin':fresh_origin,'mainTimeOrigin':main_origin,'actualDocumentReplaced':True}
                    await frame.locator('#innmain [data-m="cont"]').click()
                    await capture(page,frame,prefix+'-continue',output,records,diagnostics,args.version,delayed=fault=='decode')
                finally:await context.close()
                context,page,frame,diagnostics,requests=await context_for(fault)
                try:
                    await frame.locator('#innmain [data-m="set"]').click()
                    await frame.locator('#innopt [data-admin-open]').click()
                    await frame.locator('#inn-admin [data-admin-scene="cold"]').click()
                    await frame.wait_for_url('**testScene=cold*')
                    await capture(page,frame,prefix+'-admin-cold',output,records,diagnostics,args.version,delayed=fault=='decode')
                finally:await context.close()
        finally:await browser.close()
    paths=['New Game']
    if any(s['label'].endswith('continue') for s in records):paths.append('main menu Continue')
    if any(s['label'].endswith('admin-cold') for s in records):paths.append('administrator Opening')
    report={'version':args.version,'payloadSha256':payload_hash,'unchangedFrozenPublishedBytes':True,
        'actualNativePaths':paths,
        'DOMOnlyObserverFromDocumentStart':True,'gameStateInjection':False,
        'mediaFault':'native family image decode Promise delayed after real entry action; first family network request failed once',
        'cases':records,'status':'PASS'}
    (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(f'PASS: {len(records)} cases, {len(paths)} actual native paths; every initial rAF observed; raw world/legacy seat/old figure/early dialogue 0; Chromium closed',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/v2.html')
    parser.add_argument('--version',required=True)
    parser.add_argument('--output',default='/tmp/cinematic-entry')
    parser.add_argument('--decode-delay-ms',type=int,default=3500)
    parser.add_argument('--cases',choices=('all','normal','delayed','retry'),default='all')
    asyncio.run(main(parser.parse_args()))
