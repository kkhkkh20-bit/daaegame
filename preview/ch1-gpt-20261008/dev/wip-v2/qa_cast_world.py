"""Prepared investigation regression for separately authored full-body atlases.

Rooms/prologue completion are browser state fixtures, not a fresh walkthrough.
NPCs open through real pointer input. Source pixels are read without editing;
an independent canvas sampler checks body/transparent/other-cell coordinates,
furniture occlusion, floor/ceiling anchors and cropped viewport geometry.
One temporary readiness gate exercises cold fallback without changing assets.
Native authored lines exercise motion, quiet/reduced-motion and feature cleanup.
"""
import argparse
import hashlib
import json
import shutil

from playwright.sync_api import sync_playwright


ROOMS={'dining':['innma','seryeon'],'kitchen':['nabi','buri'],
       'front':['wanggu'],'plaza':['karo'],'hall':['geokkuri'],'dotoroom':['doto']}
EDGES={'innma':579,'seryeon':635,'nabi':694,'buri':694,
       'wanggu':615,'karo':852,'geokkuri':34,'doto':675}
CAST=['det0','det1','innma','seryeon','nabi','geokkuri','doto','buri','wanggu','karo']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--viewport',choices=['landscape','portrait'],default='landscape')
    parser.add_argument('--skip-motion',action='store_true')
    parser.add_argument('--character',choices=[k for ks in ROOMS.values() for k in ks],help='Only rerun one world actor after a focused failure')
    args=parser.parse_args()
    size={'width':844,'height':390} if args.viewport=='landscape' else {'width':390,'height':844}
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport=size);errors=[];bad=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
        page.add_init_script('''(()=>{const native=window.setInterval.bind(window),clear=window.clearInterval.bind(window);window.__qaCastTimers=new Map();window.setInterval=function(fn,ms,...rest){const id=native(fn,ms,...rest);window.__qaCastTimers.set(id,{ms,source:String(fn)});return id};window.clearInterval=function(id){window.__qaCastTimers.delete(id);return clear(id)}})()''')
        try:
            response=page.goto(args.url,wait_until='domcontentloaded')
            print('LOADED HTML SHA256',hashlib.sha256(response.body()).hexdigest(),args.viewport,flush=True)
            page.wait_for_timeout(16000)
            def state(code):return page.evaluate('(code)=>window.__T(code)',code)
            state('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
            page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1500)
            assert page.evaluate('typeof __innWorldActors==="function"'),'World atlas API missing'
            planned=page.evaluate('__innDialogueManifest.world')
            assert all(k in planned for ks in ROOMS.values() for k in ks),'Eight world actors are not present in manifest'
            page.wait_for_function('Object.values(__innDialogueManifest.world).every(a=>__innDialogueArtReady(a.src))')
            page.evaluate('''()=>{
              window.__qaCastPixels={};window.__qaCastRead=async function(src){if(__qaCastPixels[src])return __qaCastPixels[src];const i=new Image();i.src=src;await i.decode();const c=document.createElement('canvas');c.width=i.naturalWidth;c.height=i.naturalHeight;const context=c.getContext('2d');context.drawImage(i,0,0);return __qaCastPixels[src]={w:c.width,h:c.height,p:context.getImageData(0,0,c.width,c.height).data}};
              window.__qaCastSamples=async function(k){
                const im=document.querySelector('#bigscene image.wn9[data-k="'+k+'"]'),host=im.closest('svg.wn9-world')||im,raw=await __qaCastRead(im.getAttribute('href')),c=im.__worldCrop||[0,0,raw.w,raw.h],m=host.getScreenCTM(),result={opaque:[],empty:[],occluded:[],outside:[],edge:null};
                const occluders=await Promise.all(Array.from(document.querySelectorAll('#bigscene image.wo9')).map(async i=>({r:i.getBoundingClientRect(),raw:await __qaCastRead(i.getAttribute('href'))})));
                const alpha=(x,y)=>x<0||y<0||x>=raw.w||y>=raw.h?0:raw.p[(y*raw.w+x)*4+3];
                const project=(x,y)=>{if(im.__worldCrop){let p=host.createSVGPoint();p.x=x;p.y=y;return p.matrixTransform(m)}const r=im.getBoundingClientRect();return {x:r.left+x/raw.w*r.width,y:r.top+y/raw.h*r.height}};
                const covered=p=>occluders.some(o=>{let r=o.r;if(p.x<r.left||p.x>=r.right||p.y<r.top||p.y>=r.bottom)return false;let x=Math.floor((p.x-r.left)/r.width*o.raw.w),y=Math.floor((p.y-r.top)/r.height*o.raw.h);return o.raw.p[(y*o.raw.w+x)*4+3]>60});
                const usable=p=>{if(p.x<52||p.x>innerWidth-52||p.y<75||p.y>innerHeight-10)return false;const e=document.elementFromPoint(p.x,p.y);return e&&e.closest('#bigscene')&&!e.closest('.hot,.fsa,button,#w209rail')};
                let x0=raw.w,y0=raw.h,x1=-1,y1=-1;
                for(let y=Math.ceil(c[1]);y<c[1]+c[3];y++)for(let x=Math.ceil(c[0]);x<c[0]+c[2];x++)if(alpha(x,y)>=32){x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y)}
                const center=project((x0+x1+1)/2,(y0+y1+1)/2);result.center={x:center.x,y:center.y};
                if(im.__worldCrop){const world=document.querySelector('#bigscene svg[data-inn-world],#bigscene svg[data-bg]'),inv=world.getScreenCTM().inverse(),p=project((x0+x1+1)/2,k==='geokkuri'?y0:y1+1);result.edge=new DOMPoint(p.x,p.y).matrixTransform(inv).y;result.foreground=[x0,y0,x1+1,y1+1]}
                for(let y=Math.ceil(c[1])+5;y<c[1]+c[3]-5;y+=5)for(let x=Math.ceil(c[0])+5;x<c[0]+c[2]-5;x+=5){let a=alpha(x,y),p=project(x+.5,y+.5);if(!usable(p))continue;if(a>160){(covered(p)?result.occluded:result.opaque).push({x:p.x,y:p.y})}else if(a<10){let clean=true;for(let yy=-3;yy<=3&&clean;yy++)for(let xx=-3;xx<=3;xx++)if(alpha(x+xx,y+yy)>30){clean=false;break}if(clean&&!covered(p))result.empty.push({x:p.x,y:p.y})}}
                if(im.__worldCrop){const face=__innDialogueManifest.characters[k].neutral.face,p=project(face[0]+face[2]/2,face[1]+face[2]/2);if(p.x>0&&p.x<innerWidth&&p.y>0&&p.y<innerHeight)result.outside.push({x:p.x,y:p.y})}
                for(const key of ['opaque','empty','occluded'])result[key]=result[key].slice(0,80);return result;
              };
            }''')
            def room(lid):
                page.wait_for_function('!document.querySelector("body>.cutin,.iris,.banner")')
                state('if(DL){DL.done=null;endDlg()};G.beats.inn_pro=1;G.beats.inn_i9=1;G.loc=CASES[G.ci].locations.findIndex(l=>l.id==='+json.dumps(lid)+');G.who=null;goTab("scene");render();')
                page.wait_for_timeout(650)
            def samples(k):return page.evaluate('(k)=>__qaCastSamples(k)',k)
            def hit(p):return page.evaluate('(p)=>__innNpcHit(p.x,p.y)',p)
            def visible_samples(k):
                for _ in range(12):
                    found=samples(k)
                    if found['opaque']:return found
                    # A previous native entrance may still be clearing. An
                    # already-centred actor needs a settle wait, not a pan.
                    if 80<found['center']['x']<size['width']-80:
                        page.wait_for_timeout(170);continue
                    # SVG geometric bboxes retain the full atlas even when its
                    # paint is clipped. Pan toward independently sampled alpha.
                    direction='fsar' if found['center']['x']>size['width']/2 else 'fsal'
                    button=page.locator('#'+direction+':visible')
                    if button.count() and not button.is_disabled():button.click();page.wait_for_timeout(170)
                    else:
                        state('var qaImage=document.querySelector(\'#bigscene image.wn9[data-k="'+k+'"]\'),qaTile=qaImage.closest("svg.wn9-world")||qaImage,qaScroll=document.getElementById("fsscroll");qaTile.scrollIntoView({inline:"center",block:"nearest"});')
                        page.wait_for_timeout(170)
                page.screenshot(path='/tmp/cast-world-no-pointer-'+k+'.png')
                print('DIAG native world:',state('({room:CASES[G.ci].locations[G.loc].id,tab:G.tab,who:G.who,dl:!!DL,freeze:window.__dlFreeze,body:document.body.className,world:window.__innWorld&&__innWorld.state()})'),flush=True)
                print('DIAG controls:',page.locator('#fsal,#fsar,#innmove,#dlgveil,#ovfz').evaluate_all('ns=>ns.map(n=>({id:n.id,disabled:n.disabled,rect:n.getBoundingClientRect().toJSON(),visible:getComputedStyle(n).visibility,display:getComputedStyle(n).display}))'),flush=True)
                raise AssertionError(('No unobscured pointer sample',k,found))

            # Cold render retains approved standalone art until the shared
            # decoded-asset gate opens. No network/source artifacts are altered.
            page.evaluate('window.__qaCastReady=__innDialogueArtReady;window.__innDialogueArtReady=()=>false')
            room('kitchen')
            assert page.locator('svg.wn9-world').count()==0,'Loading atlas displaced legacy world fallback'
            assert all('dialogue-v2' not in a['src'] for a in page.evaluate('__innWorldActors()')),'Legacy pose was replaced before readiness'
            page.evaluate('window.__innDialogueArtReady=window.__qaCastReady;document.dispatchEvent(new Event("inn-dialogue-art-ready"))')
            page.wait_for_function('document.querySelectorAll("#bigscene svg.wn9-world").length===2')
            page.wait_for_timeout(300)
            assert all('dialogue-v2' in a['src'] for a in page.evaluate('__innWorldActors()')),'Legacy posture correction overwrote a ready atlas'
            print('PASS decoded readiness retains fallback and atomically replaces kitchen full bodies',flush=True)

            seen=set();outside_count=0;occlusion_count=0
            for lid,keys in ROOMS.items():
                for k in keys:
                    if args.character and k!=args.character:continue
                    room(lid)
                    page.wait_for_function('(k)=>Array.from(document.querySelectorAll("#bigscene svg.wn9-world")).some(n=>n.dataset.k===k)',arg=k)
                    actor=next(a for a in page.evaluate('__innWorldActors()') if a['k']==k)
                    assert actor['crop']==planned[k]['crop'] and actor['src']==planned[k]['src'] and actor['maskReady'],('Incorrect source/crop/alpha',actor)
                    found=visible_samples(k)
                    assert abs(found['edge']-EDGES[k])<.02,('Painted feet/ceiling drift',k,found['edge'],EDGES[k])
                    source_width=found['foreground'][2]-found['foreground'][0];source_height=found['foreground'][3]-found['foreground'][1]
                    assert abs(actor['bounds'][2]/actor['bounds'][3]-source_width/source_height)<.0001,('Full-body source was stretched',actor)
                    body=next((p for p in found['opaque'] if hit(p)==k),None)
                    assert body,('Opaque full-body pixels do not target native actor',k,found)
                    for p in found['outside']:
                        assert hit(p)!=k,('Adjacent dialogue cell accepts world click',k,p);outside_count+=1
                    for p in found['occluded']:
                        assert hit(p)=='',('Table foreground does not block actor behind it',k,p);occlusion_count+=1
                    label=page.locator('.npc.w9[data-npc="'+k+'"] span').bounding_box()
                    transparent=next((p for p in found['empty'] if not label or not(label['x']-4<=p['x']<=label['x']+label['width']+4 and label['y']-4<=p['y']<=label['y']+label['height']+4)),None)
                    assert transparent and hit(transparent)!=k,('Transparent body margin targets actor',k,transparent)
                    page.locator('.npc.w9[data-npc="'+k+'"]').evaluate('b=>b.dataset.nohit="1"')
                    assert hit(body)!=k,('Disabled native actor accepts body click',k)
                    page.locator('.npc.w9[data-npc="'+k+'"]').evaluate('b=>delete b.dataset.nohit')
                    page.screenshot(path='/tmp/cast-world-'+args.viewport+'-'+k+'.png')
                    page.mouse.click(body['x'],body['y'])
                    try:
                        page.wait_for_function('(k)=>__T("G.tab")==="talk"&&__T("G.who")===k',arg=k,timeout=5000)
                    except Exception:
                        page.screenshot(path='/tmp/cast-world-click-failed-'+args.viewport+'-'+k+'.png')
                        print('DIAG click:',k,body,'live alpha target:',hit(body),flush=True)
                        print('DIAG after click:',state('({tab:G.tab,who:G.who,dl:DL&&{i:DL.i,line:DL.lines[DL.i]},found:G.found,freeze:window.__dlFreeze,body:document.body.className,obs:document.querySelector(".innobs")?.textContent,notice:G.notice})'),flush=True)
                        print('DIAG target DOM:',page.evaluate('(p)=>document.elementFromPoint(p.x,p.y)?.outerHTML.slice(0,600)',body),flush=True)
                        raise
                    page.wait_for_function('(k)=>Array.from(document.querySelectorAll(".fstalk svg.dialogue-bust")).some(n=>n.dataset.k===k)',arg=k)
                    talk=page.locator('.fstalk svg.dialogue-bust').first.get_attribute('viewBox')
                    assert talk!=' '.join(map(str,planned[k]['crop'])),('Dialogue reuses room full-body composition',k,talk)
                    assert page.locator('.fstalk svg.dialogue-bust').count()==1,'Dialogue surface duplicated'
                    page.wait_for_function('!document.querySelector("body>.cutin,.iris,.banner")')
                    seen.add(k);print('PASS',args.viewport,k,'full body, alpha input, anchor and separate native dialogue close-up',flush=True)
            assert len(seen)==(1 if args.character else 8),'Not all selected world actors were exercised'
            # Off-crop portrait cells and tabletop samples can lie outside the
            # narrow phone viewport. The full landscape suite requires both;
            # portrait still checks any such pixels that are actually visible.
            if not args.character and args.viewport=='landscape':
                assert outside_count>0,'Atlas adjacent-cell regression was not exercised'
                assert occlusion_count>0,'Table foreground regression was not exercised'
            print('COVERAGE adjacent-cell points',outside_count,'table-occluded points',occlusion_count,flush=True)
            if not args.skip_motion:
                authored=page.evaluate('''()=>{const out={};function visit(o){if(!o||typeof o!=='object')return;if(Array.isArray(o)&&typeof o[0]==='string'&&typeof o[1]==='string'&&o[0]!=='@dir'){(out[o[0]]||(out[o[0]]=[])).push(o);return}Object.values(o).forEach(visit)}visit(EP1INN);return out}''')
                def speak(k,wanted=None):
                    rows=authored[k]
                    line=next((l for l in rows if wanted is None or (l[6] if len(l)>6 and l[6] else l[2] if len(l)>2 else '') in wanted),None)
                    assert line,('Missing authored motion fixture',k,wanted)
                    state('if(DL){DL.done=null;endDlg()};G.tab="scene";G.who=null;render();say('+json.dumps([['@dir','who:'+('det1' if k=='det0' else k)+';chime:0;ms:80'],line],ensure_ascii=False)+',null);')
                    page.wait_for_timeout(550)
                    return page.evaluate('__innMotionState()')
                for k in CAST:
                    motion=speak(k)
                    assert any(a['k']==k for a in motion['actors']),('New actor is absent from motion scheduler',k,motion)
                    transforms=page.locator('svg.dialogue-bust').evaluate_all('ns=>ns.map(n=>({rotate:getComputedStyle(n).rotate,scale:getComputedStyle(n).scale,layers:n.querySelectorAll(".cm-bust-layer").length}))')
                    assert all(t['rotate'] in ['none','0deg'] and t['scale'] in ['none','1'] and t['layers']<=1 for t in transforms),transforms
                motion=speak('det1',{'sad','worried','cower'})
                assert all(a['quiet'] for a in motion['actors'] if a['k']=='det1'),'Distressed Daram keeps playful motion'
                page.emulate_media(reduced_motion='reduce');speak('det1')
                moving=page.locator('[data-cm-k],.cm-part').evaluate_all('ns=>ns.reduce((a,n)=>a+n.getAnimations({subtree:false}).filter(x=>x.playState==="running").length,0)')
                assert moving==0,('Reduced-motion actors still animate',moving)
                assert page.evaluate('__innMotionState().timerCount')==1
                timers=page.evaluate('Array.from(__qaCastTimers.values()).filter(t=>t.ms===160&&t.source.includes("active=inn()")).length')
                assert timers==1,('Persistent motion scheduler duplicated',timers)
                print('PASS ten native speakers, quiet distress, reduced motion and one shared motion timer',flush=True)
            assert not errors,errors
            assert not bad,bad
            print('PASS full-body atlas integration; JS/HTTP errors 0',flush=True)
        finally:
            browser.close()


if __name__=='__main__':main()
