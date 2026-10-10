"""Native character rendering/motion regression with authored dialogue.

Prepared introduction state only; no art or evidence is injected. Authored
lines run through native say/@dir. This verifies rendering and motion behavior;
it does not judge artistic consistency inside the approved source images.
"""
import argparse
import json
import shutil

from playwright.sync_api import sync_playwright


CAST = ['det0','det1','innma','seryeon','nabi','geokkuri','doto','buri','wanggu','karo']
SURFACES = '#innstage .isf img,.fstalk .tstage .tfig img,.spk9 img'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--only-motion-mode',choices=['no-preference','reduce'],help='Run one preference for a focused regression')
    args = parser.parse_args()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        for reduced in ([args.only_motion_mode] if args.only_motion_mode else ('no-preference','reduce')):
            page = browser.new_page(viewport={'width':844,'height':390},reduced_motion=reduced)
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            # Independently detect accumulated intervals, including timers outside
            # the new module's own diagnostic object.
            page.add_init_script('''(()=>{
              const set=window.setInterval.bind(window),clear=window.clearInterval.bind(window);
              window.__qaIntervals=new Map();
              window.setInterval=function(fn,ms,...args){const id=set(fn,ms,...args);
                window.__qaIntervals.set(id,{ms,signature:String(fn).slice(0,240)});return id};
              window.clearInterval=function(id){window.__qaIntervals.delete(id);return clear(id)};
            })()''')
            page.goto(args.url,wait_until='domcontentloaded')
            page.wait_for_timeout(16000)
            def engine(code):
                return page.evaluate('(code)=>window.__T(code)',code)
            engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));'
                   'S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
            page.evaluate('()=>{document.querySelector("#innmain").remove();window.__w209boot()}')
            page.wait_for_timeout(1600)
            assert page.evaluate('typeof window.__innMotionState==="function"'), 'Build lacks character motion module'
            lines=page.evaluate('''()=>{
              const known=new Set(['det0','det1','innma','seryeon','nabi','geokkuri','doto','buri','wanggu','karo']),out=[];
              function visit(o){if(!o||typeof o!=='object')return;
                if(Array.isArray(o)&&known.has(o[0])&&typeof o[1]==='string'){out.push(o);return}
                if(known.has(o.w)&&typeof o.t==='string'){out.push([o.w,o.t,o.m||'']);return}
                Object.values(o).forEach(x=>{if(x&&typeof x==='object')visit(x)});
              }visit(window.EP1INN);return out;
            }''')
            assert set(x[0] for x in lines)==set(CAST), ('Missing authored cast',set(x[0] for x in lines))
            def mood(line):
                return (line[6] if len(line)>6 and line[6] else line[2] if len(line)>2 else '') or 'neutral'
            def pick(who,wanted=None):
                matches=[line for line in lines if line[0]==who and (wanted is None or mood(line) in wanted)]
                assert matches, ('Missing authored expression fixture',who,wanted)
                return matches[0]
            def motion():
                return page.evaluate('window.__innMotionState()')
            def show(line):
                rows=[['@dir','who:'+('det1' if line[0]=='det0' else line[0])+';chime:0;ms:80'],line]
                engine('if(DL){DL.done=null;endDlg()};say('+json.dumps(rows,ensure_ascii=False)+',null);')
                page.wait_for_timeout(700)
                assert engine('!!DL'), ('Native authored dialogue did not start',line)
                state=motion()
                assert state['timerCount']==1, ('Motion timer duplicated',state)
                assert state['reduced']==(reduced=='reduce'),state
                return state
            def images():
                return page.locator(SURFACES).evaluate_all('''images=>images.filter(i=>{
                  const r=i.getBoundingClientRect(),s=getComputedStyle(i);
                  return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none';
                }).map(i=>{const r=i.getBoundingClientRect(),s=getComputedStyle(i);return {
                  src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0,
                  natural:[i.naturalWidth,i.naturalHeight],rect:r.toJSON(),render:s.imageRendering,
                  rotate:s.rotate,scale:s.scale,
                  moving:(i.closest('.isf,.tfig,.spk9')||i).getAnimations({subtree:true}).filter(a=>a.playState==='running'&&a.effect.getKeyframes().some(k=>
                    k.transform||k.translate||k.rotate||k.scale)).length};})''')
            def check_art():
                found=images()
                assert found and all(i['loaded'] for i in found), ('Character art failed to load',found)
                for image in found:
                    assert image['render'] in ('pixelated','crisp-edges'), ('Blurred character surface',image)
                    rect=image['rect'];natural=image['natural']
                    assert abs(rect['width']/rect['height']-natural[0]/natural[1])<.025, ('Art is stretched',image)
                    assert rect['right']>0 and rect['left']<page.viewport_size['width'], ('Actor completely offscreen',image)
                    assert image['rotate'] in ('none','0deg'), ('Continuous rotation blurs pixel edges',image)
                    assert image['scale'] in ('none','1','1 1'), ('Continuous scale distorts pixel edges',image)
                    if reduced=='reduce':
                        assert image['moving']==0, ('Reduced-motion still animates an actor',image)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Character creates horizontal page overflow'
                return found

            # Every appearing character must still have visible loaded approved art.
            for who in CAST:
                show(pick(who))
                check_art()
            print(reduced,'PASS all ten authored speakers render without stretching/blur/old rotation',flush=True)

            # Available approved Daram expression files must actually change through
            # native mood fields, rather than merely updating a diagnostic label.
            expression_sources=[]
            for wanted,expected in [({'think','memo'},'memo'),({'joy','laugh','smile'},'joy')]:
                line=pick('det1',wanted)
                state=show(line)
                source=page.locator('#innstage .isf img').get_attribute('src')
                assert expected in source, ('Native body expression did not change',line,state,source)
                expression_sources.append(source)
                assert any(actor['k']=='det1' and actor['mood'] in wanted for actor in state['actors']),state
                check_art()
            assert len(set(expression_sources))==2,expression_sources
            state=show(pick('det1',{'sad','worried','cower'}))
            assert 'daram-worried-dialogue.png' in page.locator('#innstage .isf img').get_attribute('src'), 'Distress still uses smiling neutral art'
            assert 'daram-worried-dialogue.png' in page.locator('.spk9 img').get_attribute('src'), 'Body/portrait worry expression diverges'
            relevant=[actor for actor in state['actors'] if actor['k']=='det1']
            assert relevant and all(actor['quiet'] for actor in relevant), ('Distress line receives idle/playful motion',state)
            print(reduced,'PASS native available expressions and restrained distress motion',flush=True)
            for wanted,expected in [({'sad','worried'},'concerned'),({'smile'},'bright-smile')]:
                show(pick('innma',wanted))
                source=page.locator('#innstage .isf img').get_attribute('src')
                portrait=page.locator('.spk9 img').get_attribute('src')
                assert expected in source and expected in portrait, ('Grandma approved expression missing',source,portrait)
            # Add punctuation to an authored neutral utterance as a rendering
            # fixture: punctuation alone must never request angry approved art.
            neutral_neoul=[pick('wanggu',{'neutral'}).copy()]
            neutral_neoul[0][1]+='!'
            show(neutral_neoul[0])
            assert '/neoul-angry-' not in page.locator('#innstage .isf img').get_attribute('src')
            # Some authored rules have no mood tag. Text-based admonishment must
            # choose the same expression for the large actor and speaker crop.
            rule=next((l for l in lines if l[0]=='wanggu' and any(word in l[1] for word in ['규정','규약','규칙','기록하겠습니다'])),None)
            assert rule, 'Authored regulation dialogue missing'
            show(rule)
            assert page.locator('#innstage .isf img').get_attribute('src')==page.locator('.spk9 img').get_attribute('src'), 'Neoul rule body/speaker expression diverges'


            # Repeated native updates must not append duplicate motion layers or
            # allocate another persistent interval per rendered actor.
            line=pick('det1',{'neutral'})
            show(line)
            before=page.evaluate('window.__qaIntervals.size')
            layer_before={(a['k'],a['surface'],a['part']):a['layerCount'] for a in motion()['actors']}
            for _ in range(6):
                show(line)
            after=page.evaluate('window.__qaIntervals.size')
            assert after<=before+1, ('Intervals accumulate after repeated dialogue',before,after)
            schedulers=page.evaluate("Array.from(window.__qaIntervals.values()).filter(x=>x.ms===160&&x.signature.includes('active=inn()')).length")
            assert schedulers==1, ('Character scheduler count differs from diagnostic API',schedulers)

            state=motion()
            assert len({(a['k'],a['surface'],a['part']) for a in state['actors']})==len(state['actors']), ('Duplicate actor surface entries',state)
            for actor in state['actors']:
                assert actor['layerCount']<=layer_before.get((actor['k'],actor['surface'],actor['part']),actor['layerCount']), ('Motion layers accumulate',state)
            if reduced=='reduce':
                page.evaluate('''()=>{window.__qaTailChanges=[];window.__qaTailObserver=new MutationObserver(ms=>{
                  ms.forEach(m=>{if(m.attributeName==='src'&&m.target.closest('#innstage'))
                    window.__qaTailChanges.push(m.target.getAttribute('src'))})});
                  window.__qaTailObserver.observe(document.body,{subtree:true,attributes:true,attributeFilter:['src']});}''')
                tail=motion()['tailFrames']
                page.wait_for_timeout(3700)
                assert page.evaluate('window.__qaTailChanges.length')==0, ('Reduced-motion still swaps tail frames',page.evaluate('window.__qaTailChanges'))
                assert motion()['tailFrames']==tail, ('Reduced-motion increments tail animation frames',motion())
            print(reduced,'PASS single timer/layers and reduced-motion tail freeze',flush=True)

            page.set_viewport_size({'width':390,'height':844})
            for who in ('det1','innma','wanggu','geokkuri'):
                show(pick(who))
                check_art()
                page.screenshot(path='/tmp/character-motion-'+reduced+'-'+who+'-portrait.png')
            print(reduced,'PASS portrait character rendering and page bounds',flush=True)
            for who in ('innma','nabi','seryeon','wanggu'):
                engine('if(DL){DL.done=null;endDlg()};G.who='+json.dumps(who)+';G.tab="talk";render();')
                page.wait_for_timeout(850)
                assert page.locator('.fstalk .tstage .tfig img:visible').count(), ('Native talk actor missing',who)
                check_art()
                assert motion()['timerCount']==1,motion()
            print(reduced,'PASS native talk-stage character surfaces',flush=True)
            # Prepared single-line phases exercise the actual native council
            # renderer with existing authored dialogue and the real seat layout.
            native_cases=[(pick('det1',{'joy','laugh','smile'}),'daram-v4/daram-joy-profile'),
                          (pick('innma',{'sad','worried'}),'innma-concerned-v5'),
                          (neutral_neoul[0],None)]
            for row,expected in native_cases:
                council={'w':row[0],'t':row[1],'m':mood(row)}
                code=('if(DL){DL.done=null;endDlg()};window.__rtgReset();'
                      'document.querySelectorAll("body>.rt").forEach(x=>x.remove());window.__inMeeting=false;'
                      'window.__rtOpen(CASES[G.ci],{key:"qaMotion",title:"QA",seats:EP1INN.MEET.seats,'
                      'phases:[{type:"talk",lines:['+json.dumps(council,ensure_ascii=False)+']}]});')
                engine(code)
                page.wait_for_function('(t)=>{const p=document.querySelector("body>.rt #rtnext .rt-bub p");return p&&p.textContent===t}',arg=council['t'],timeout=12000)
                page.wait_for_timeout(500)
                sources=page.locator('#rtg .seat img,#rtg .seat>svg>image').evaluate_all('''async xs=>Promise.all(xs.map(async x=>{
                  const src=x.getAttribute('src')||x.getAttribute('href');
                  if(x.tagName.toLowerCase()==='img')return {src,ok:x.complete&&x.naturalWidth>0};
                  const probe=new Image();probe.src=src;try{await probe.decode()}catch(e){}return {src,ok:probe.complete&&probe.naturalWidth>0};
                }))''')
                assert sources and all(x['ok'] for x in sources), ('Native council images missing',sources)
                if expected:
                    assert any(expected in x['src'] for x in sources), ('Native approved expression missing',council,sources)
                else:
                    neoul=[x for x in sources if 'neoul-' in x['src']]
                    assert neoul and all('neoul-angry-' not in x['src'] for x in neoul),neoul
                assert motion()['timerCount']==1,motion()
            pulse=page.evaluate("""()=>{let found=null;function scan(o){if(!o||typeof o!=='object'||found)return;
              if(o.audio==='pulse'&&o.w&&o.t){found=o;return}Object.values(o).forEach(scan)}
              scan(EP1INN);return found}""")
            assert pulse,'No authored pulse fixture'
            engine('window.__rtgReset();document.querySelectorAll("body>.rt").forEach(x=>x.remove());window.__inMeeting=false;'
                   'window.__rtOpen(CASES[G.ci],{key:"qaMotionPulse",seats:EP1INN.MEET.seats,phases:[{type:"talk",lines:['+
                   json.dumps(pulse,ensure_ascii=False)+']}]});')
            page.wait_for_function('(t)=>{const p=document.querySelector("body>.rt #rtnext .rt-bub p");return p&&p.textContent===t}',arg=pulse['t'],timeout=12000)
            page.wait_for_timeout(500)
            state=motion()
            assert state['actors'] and all(a['quiet'] for a in state['actors']), ('Heart-pulse scene retains playful idle motion',state)
            print(reduced,'PASS native council Daram/Grandma sources and Neoul punctuation restraint',flush=True)

            assert not errors,errors
            page.close()
        browser.close()
        print('PASS character motion QA; JavaScript errors: 0',flush=True)


if __name__=='__main__':
    main()
