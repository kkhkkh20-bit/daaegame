"""Prepared P10b actor/camera regression using native directions and dialogue.

This narrow fixture selects the authored P10b with the QA evaluation hook,
then stops its first native dialogue callback to examine each explicit direction
without advancing story/evidence. It is not a fresh-game playthrough. Real
image loading and the existing stage/portrait renderer remain active.
"""
import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen
from playwright.sync_api import sync_playwright


def frozen_sources(args):
    """Keep exact, unchanged served HTML stable throughout both QA contexts."""
    body=urlopen(args.url).read()
    if args.native_admin:
        payload=urlopen(urljoin(args.url,'play_v2.html')).read()
        digest=hashlib.sha256(payload).hexdigest()
        routes={'**/v2.html*':body,'**/play_v2.html*':payload}
        if args.version:assert args.version in body.decode(),'Wrapper does not select requested version'
    else:
        assert urlsplit(args.url).path.endswith('/playT.html'),'Prepared fixture requires direct playT.html'
        hook=b'window.__T=function(code){return eval(code)};\n'
        assert body.count(hook)==1,'Prepared payload must have exactly the existing QA evaluation hook'
        digest=hashlib.sha256(body.replace(hook,b'')).hexdigest()
        routes={'**/playT.html*':body}
    if args.version:assert digest.startswith(args.version),('Unexpected frozen build',digest,args.version)
    return routes,{'requestedVersion':args.version,'productionPayloadSHA256':digest,'frozenUnchangedHTML':True}


def freeze_context(context,routes):
    def response(body):
        return lambda route:route.fulfill(body=body,content_type='text/html; charset=utf-8')
    for pattern,body in routes.items():
        context.route(pattern,response(body))


DOM = r'''()=>{
 const p=__innOpeningDirection(),q=s=>document.querySelector(s);
 function visible(e){if(!e)return false;const s=getComputedStyle(e),r=e.getBoundingClientRect();let opacity=1;
  for(let n=e;n&&n.nodeType===1;n=n.parentElement){const c=getComputedStyle(n);if(c.display==='none')return false;opacity*=+c.opacity}
  return s.visibility==='visible'&&opacity>.02&&r.width>0&&r.height>0}
 const room=q('#inn-night-walk .night-bedroom'),child=q('#inn-night-walk .night-child'),eyes=q('#inn-night-walk .night-eyes');
 const bami=Array.from(document.querySelectorAll('#innstage .isf[data-k="geokkuri"]'));
 return {night:p.night,ready:p.ready,error:p.error,cue:p.cue,actor:p.actor,reduced:p.reduced,
  room:visible(room),hallChild:visible(child),eyes:visible(eyes),bamiCount:bami.length,bamiVisible:bami.filter(visible).length,
  bamiMood:bami[0]?.dataset.mood||'',bamiPosture:bami[0]?.dataset.posture||'',
  otherActors:Array.from(document.querySelectorAll('#innstage .isf')).filter(visible).map(e=>e.dataset.k),
  classes:document.body.className};
}'''


NATIVE_OBSERVER = r'''(()=>{
 if(!/\/play_v2\.html$/.test(location.pathname))return;
 const trace={frames:[],changes:[],stop:false};window.__qaNativeNight=trace;let last='';
 function visible(e){if(!e)return false;const r=e.getBoundingClientRect(),s=getComputedStyle(e);let o=1;
  for(let n=e;n&&n.nodeType===1;n=n.parentElement){const c=getComputedStyle(n);if(c.display==='none')return false;o*=+c.opacity}
  return r.width>0&&r.height>0&&s.visibility==='visible'&&o>.02}
 function tick(){if(trace.stop)return;
  const p=window.__innOpeningDirection?.(),f=window.__innSceneFlowState?.(),q=s=>document.querySelector(s),b=Array.from(document.querySelectorAll('#innstage .isf[data-k="geokkuri"]'));
  const r={t:performance.now(),sid:p?.scene||f?.sid||null,cue:p?.cue||null,ready:p?.ready||false,
   bami:b.filter(visible).length,bamiCount:b.length,bamiMood:b[0]?.dataset.mood||'',bamiPosture:b[0]?.dataset.posture||'',
   room:visible(q('#inn-night-walk .night-bedroom')),hallChild:visible(q('#inn-night-walk .night-child')),eyes:visible(q('#inn-night-walk .night-eyes')),
   line:q('#dtxt,#vnbox .vtxt')?.innerText||'',who:q('#vnbox .spk9')?.dataset.k||'',black:visible(q('#inn-scene-black')),flow:f};
  trace.frames.push(r);let k=JSON.stringify([r.sid,r.cue,r.bami,r.bamiMood,r.room,r.hallChild,r.eyes,r.line,r.black]);if(k!==last){trace.changes.push(r);last=k}
  requestAnimationFrame(tick);
 }
 requestAnimationFrame(tick);
})();'''


def native_admin(args):
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    routes,source=frozen_sources(args)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':844,'height':390},service_workers='block');freeze_context(context,routes);context.add_init_script(NATIVE_OBSERVER)
        page=context.new_page();errors=[];bad=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
        try:
            page.goto(args.url,wait_until='domcontentloaded')
            frame=page.locator('#game').element_handle().content_frame()
            frame.locator('#innmain [data-m="set"]').click(timeout=25000)
            frame.locator('#innopt [data-admin-open]').click()
            frame.locator('#inn-admin [data-admin-scene="night"]').click()
            frame.wait_for_url('**testScene=night*')
            assert frame.evaluate('typeof __T')=='undefined','Actual native route must use the clean published wrapper'
            captured=set();deadline=time.monotonic()+90
            while time.monotonic()<deadline:
                r=frame.evaluate('window.__qaNativeNight.frames.at(-1)')
                if r and r['sid']=='P10b' and r['cue'] and r['ready'] and not r['black']:
                    key='home-return' if r['cue']=='home' and 'return' in captured else r['cue']
                    if key not in captured and (key!='bami' or r['bami']==1):
                        page.screenshot(path=str(out/('native-'+key+'.png')));captured.add(key)
                    if frame.locator('#vnbox .vtxt').count():page.keyboard.press('Enter')
                if r and r['sid']=='P11' and r['line'] and not r['black']:break
                page.wait_for_timeout(180)
            else:raise AssertionError('Actual administrator P10b did not finish')
            trace=frame.evaluate('window.__qaNativeNight.stop=true;window.__qaNativeNight')
            rows=[r for r in trace['frames'] if r['sid']=='P10b'];cues=list(dict.fromkeys(r['cue'] for r in rows if r['cue']))
            assert cues==['home','out','touch','eyes','bami','return'],cues
            home_after=[r for r in rows if r['cue']=='home' and r['t']>next(r['t'] for r in rows if r['cue']=='return')]
            assert home_after,'Native return never reached explicit bedroom home'
            for r in rows:
                assert r['bami']<2 and not (r['room'] and r['hallChild']),r
                if r['cue']!='bami':assert r['bami']==0,r
                if r['bami']:
                    assert r['bamiPosture']=='dialogue-hanging',r
                    if r['who'].split('|')[0] in ('det0','det1'):assert r['bamiMood']=='',r
            assert any(r['bami']==1 for r in rows),'Native Bami encounter never appeared'
            assert not errors and not bad,(errors,bad)
            result={'fixture':'actual main settings → administrator night, native Enter; no game-state/evidence injection',
                'url':frame.url,'source':source,'frames':len(rows),'cueOrderWithFinalHome':cues+['home'],'errors':errors,'httpFailures':bad,'trace':trace}
            (out/'native-report.json').write_text(json.dumps(result,ensure_ascii=False))
            print('PASS actual administrator P10b',len(rows),'frames: explicit cues, resident exit, hanging posture, no father/child mood contamination or room/hall overlap; JS/HTTP 0',flush=True)
        finally:context.close();browser.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--output',default='/tmp/night-direction')
    parser.add_argument('--native-admin',action='store_true')
    parser.add_argument('--version',help='Expected production payload SHA256 prefix; QA hook is excluded from prepared hash')
    args=parser.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);reports=[]
    if args.native_admin:return native_admin(args)
    routes,source=frozen_sources(args)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        try:
            for reduced in (False,True):
                context=browser.new_context(viewport={'width':844,'height':390},reduced_motion='reduce' if reduced else 'no-preference',service_workers='block')
                freeze_context(context,routes)
                page=context.new_page();errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                try:
                    page.goto(args.url,wait_until='domcontentloaded')
                    frame=page.locator('#game').element_handle().content_frame() if page.locator('#game').count() else page
                    assert frame.evaluate('typeof __T')=='function','Prepared fixture requires playT QA hook'
                    frame.locator('#innmain [data-m="new"]').click(timeout=25000)
                    frame.wait_for_function('!!document.querySelector("#dlgveil")',timeout=25000)
                    def engine(code):return frame.evaluate('(code)=>__T(code)',code)
                    engine('if(DL){DL.done=null;endDlg()}G.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P10b")};__innStart()')
                    frame.wait_for_function('__innOpeningDirection().ready&&!!__T("DL")',timeout=25000)
                    engine('DL.done=null;endDlg()')
                    states=[]
                    for cue in ('home','out','touch','eyes','bami','return','home'):
                        frame.evaluate('(cue)=>Promise.resolve(__innDir({night:cue,who:cue==="bami"?"geokkuri":"none",chime:0,ms:0}))',cue)
                        engine('say([["det0","괜찮다. 같이 가자.","nervous","",null,null,"shock"]],function(){})')
                        page.wait_for_timeout(300 if cue!='return' else 1000)
                        state=frame.evaluate(DOM);states.append(state)
                        assert state['cue']==cue and state['ready'],state
                        assert state['bamiVisible']==(1 if cue=='bami' else 0),state
                        assert state['bamiCount']==(1 if cue=='bami' else 0),state
                        if cue=='bami':
                            assert state['bamiMood']=='','Father mood contaminated Bami'
                            assert state['bamiPosture']=='dialogue-hanging',state
                        assert state['room']==(cue=='home'),state
                        assert not (state['room'] and state['hallChild']),state
                        assert state['eyes']==(cue=='eyes'),state
                        page.screenshot(path=str(out/(('reduced' if reduced else 'normal')+'-'+cue+'.png')))
                        engine('DL.done=null;endDlg()')
                    # A pending/old captured night cannot keep an actor or its
                    # hiding classes after an actual game-state replacement.
                    frame.evaluate('__innDir({night:"bami",who:"geokkuri",chime:0})')
                    engine('say([["geokkuri","가서 자."]],function(){})')
                    page.wait_for_timeout(200)
                    engine('S.screen="main"')
                    page.wait_for_timeout(100)
                    assert frame.locator('#inn-night-walk').count()==0
                    assert frame.locator('#innstage .isf[data-k="geokkuri"]').count()==0
                    assert not frame.evaluate('document.body.classList.contains("inn-night-direction")||document.body.classList.contains("inn-night-dark")')
                    # A non-night resident keeps its own expression when father
                    # or daughter speaks. Native D keeps actor ownership fixed.
                    engine('S.screen="case";G.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P3")};__innStart()')
                    frame.wait_for_function('__innSceneFlowState().settled&&!!__T("DL")',timeout=25000)
                    engine('DL.done=null;endDlg()')
                    expression_states=[]
                    for actor in ('innma','wanggu'):
                        frame.evaluate('(actor)=>__innDir({who:actor,chime:0,ms:0})',actor)
                        for speaker,mood in ((actor,'think'),('det0','sad'),('det1','shock')):
                            engine('say('+json.dumps([[speaker,'같이 이야기해 보자.','','',None,None,mood]],ensure_ascii=False)+',function(){})')
                            page.wait_for_timeout(200)
                            got=frame.locator('#innstage .isf').evaluate_all('(a)=>a.map(n=>({actor:n.dataset.k,mood:n.dataset.mood}))')
                            assert got==[{'actor':actor,'mood':'think'}],(actor,speaker,mood,got)
                            expression_states.append({'speaker':speaker,'speakerMood':mood,'stage':got})
                            engine('DL.done=null;endDlg()')
                    # With no resident, father selects a neutral daughter;
                    # daughter then owns her own initial expression.
                    for speaker,mood,expected in (('det0','sad',''),('det1','shock','shock')):
                        frame.evaluate('__innDir({who:"none",chime:0,ms:0})')
                        page.wait_for_timeout(300)
                        engine('say('+json.dumps([[speaker,'우리끼리 이야기하자.','','',None,None,mood]],ensure_ascii=False)+',function(){})')
                        page.wait_for_timeout(200)
                        got=frame.locator('#innstage .isf').evaluate_all('(a)=>a.map(n=>({actor:n.dataset.k,mood:n.dataset.mood}))')
                        assert got==[{'actor':'det1','mood':expected}],(speaker,mood,got)
                        expression_states.append({'speaker':speaker,'speakerMood':mood,'initialDuo':got})
                        engine('DL.done=null;endDlg()')
                    assert not errors,errors
                    reports.append({'source':source,'reduced':reduced,'fixture':'prepared P10b/P3, native dirRun/say, stopped original dialogue continuation','states':states,'residentExpressions':expression_states,'errors':errors})
                    print('PASS',reduced,'explicit night phases, Bami exit, hanging pose, home/hall exclusivity, main cleanup; resident and initial duo expression ownership',flush=True)
                finally:context.close()
        finally:browser.close()
    (out/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
