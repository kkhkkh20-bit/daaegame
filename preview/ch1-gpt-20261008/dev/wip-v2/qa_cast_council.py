"""Prepared native council regression for distinct cast art and cue stability.

Uses real authored lines and native council seats; it is not a fresh playthrough.
Checks expression/source consistency, immutable render markup (no seat repaint
loop), clipped source cells, restrained motion in tension and reduced motion.
"""
import argparse
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

CAST = ['det1','innma','seryeon','nabi','geokkuri','doto','buri','karo','wanggu']


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    ap.add_argument('--out',default='/tmp/cast-council')
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        for preference in ['no-preference','reduce']:
            page=browser.new_page(viewport={'width':844,'height':390},reduced_motion=preference)
            errors=[];bad=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
            page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
            def e(code):return page.evaluate('(code)=>__T(code)',code)
            e('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
            page.evaluate('document.querySelector("#innmain").remove();__w209boot()');page.wait_for_timeout(1000)
            page.wait_for_function('__innDialogueState().assets.every(a=>a.ready)')
            rows=page.evaluate('''()=>{let a=[];const cast=new Set(['det0','det1','innma','seryeon','nabi','geokkuri','doto','buri','karo','wanggu']);function walk(o){if(!o||typeof o!=="object")return;if(Array.isArray(o)&&cast.has(o[0])&&typeof o[1]==="string"){a.push({w:o[0],t:o[1],m:typeof(o[6]||o[2])==="string"?(o[6]||o[2]):""});return}if(o.w&&typeof o.t==="string"){a.push(o);return}Object.values(o).forEach(walk)}walk(EP1INN);return a}''')
            def open_line(row):
                e('if(DL){DL.done=null;endDlg()};__rtgReset();document.querySelectorAll("body>.rt").forEach(n=>n.remove());window.__inMeeting=false;__rtOpen(CASES[G.ci],'+json.dumps({'key':'qaCast','title':'인물 검수','seats':page.evaluate('EP1INN.MEET.seats'),'phases':[{'type':'talk','topic':'인물 표정 검수','lines':[row]}]},ensure_ascii=False)+');')
                page.wait_for_function('(t)=>document.querySelector("#rtnext .rt-bub p")?.textContent===t',arg=row['t'])
                page.wait_for_timeout(350)
            normal=next(r for r in rows if r.get('w')=='wanggu' and r.get('audio') not in ['pulse','silence'])
            open_line(normal)
            seats=page.locator('#rtg .seat>svg.inn-council-cast')
            assert seats.count()==len(CAST),(seats.count(),page.locator('#rtg .seat').count())
            sources=seats.evaluate_all('xs=>xs.map(n=>({k:n.dataset.k,src:n.dataset.src,view:n.getAttribute("viewBox"),clip:n.querySelector("clipPath rect").outerHTML,rect:n.getBoundingClientRect().toJSON()}))')
            assert set(r['k'] for r in sources)==set(CAST),sources
            assert all('/dialogue-v2/' in r['src'] and r['rect']['width']>0 and r['rect']['height']>0 for r in sources),sources
            assert not page.locator('#rtg .seat>img').count(),'Old identity remains among council seats'
            geometry=page.locator('#rtg .seat').evaluate_all('xs=>xs.map(s=>{const a=s.querySelector("svg.inn-council-cast"),c=getComputedStyle(a);return {k:s.dataset.k,classes:s.className,style:s.getAttribute("style"),seat:s.getBoundingClientRect().toJSON(),svg:a.getBoundingClientRect().toJSON(),svgStyle:{height:c.height,top:c.top,width:c.width},crop:a.getAttribute("viewBox")}})')
            (out/f'geometry-{preference}.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2)+'\n')
            # Pointer/cue updates should not replace seats with identical art.
            page.evaluate('''()=>{window.__castRepaints=[];window.__castObserver=new MutationObserver(ms=>ms.forEach(m=>{if(m.target.closest?.("#rtg .seat"))window.__castRepaints.push(m.target.className.baseVal||m.target.className)}));__castObserver.observe(document.querySelector("#rtg"),{childList:true,subtree:true})}''')
            page.wait_for_timeout(900)
            assert page.evaluate('__castRepaints.length')==0,page.evaluate('__castRepaints')
            page.evaluate('__castObserver.disconnect()')
            page.screenshot(path=str(out/f'council-{preference}.png'))
            print('PASS',preference,'9 new council identities / source clips / no idle repaint loop',flush=True)
            for k in CAST+['det0']:
                # Deliberately repeat the same authored sentence with four
                # moods: the reaction cache must include mood, not just text.
                row=next(r for r in rows if r.get('w')==k)
                for i,mood in enumerate(['neutral','think','worried','angry' if k in ['karo','seryeon','wanggu'] else 'joy']):
                    utterance={'w':k,'t':row['t'],'m':mood};open_line(utterance)
                    expected=page.evaluate('(a)=>__innDialogueArt(a.k,a.m)',{'k':k,'m':mood})
                    # Native markup places pf(L.w,L.m) in .rt-big beside the
                    # text bubble. The visual design hides that legacy tile;
                    # the authored seat remains the visible speaker actor.
                    faces=page.locator('#rtnext .rt-big svg.inn-pixel-face')
                    assert faces.count(),(k,mood,'Native council speaker has old generic face')
                    assert faces.first.get_attribute('data-src')==expected['src'],(k,mood)
                    assert [float(v) for v in faces.first.get_attribute('viewBox').split()]==expected['face']+[expected['face'][2]],(k,mood)
                    if k!='det0':
                        actor=page.locator('#rtg .seat[data-k="'+k+'"]>svg.inn-council-cast')
                        assert actor.get_attribute('data-expression')==faces.first.get_attribute('data-expression'),(k,mood)
            print('PASS',preference,'40 native council speaker faces / expression agreement',flush=True)
            # Native location banner: visible actors must stop idle movement
            # while the authored presentation is in front of the council.
            open_line(normal)
            e('banner("여관 식당","아침");true')
            page.wait_for_timeout(150)
            assert page.locator('.banner').count()
            assert page.evaluate('__innMotionState().paused'),page.evaluate('__innMotionState()')
            assert page.locator('#rtg .seat svg').evaluate_all('xs=>xs.flatMap(x=>x.getAnimations({subtree:true})).filter(a=>a.playState==="running"&&a.effect.getKeyframes().some(f=>f.translate||f.transform||f.rotate||f.scale)).length')==0
            page.wait_for_function('!document.querySelector(".banner")')
            print('PASS',preference,'native banner pauses cast motion',flush=True)
            # Read the live native authored object so its audio metadata is
            # preserved independently of the portrait-fixture normalization.
            pulse=page.evaluate('''()=>{let found=null;function walk(o){if(!o||typeof o!=="object"||found)return;if(o.audio==="pulse"&&o.w&&typeof o.t==="string"){found=o;return}Object.values(o).forEach(walk)}walk(EP1INN);return found}''')
            assert pulse,'Native authored pulse cue missing'
            open_line(pulse);state=page.evaluate('__innMotionState()')
            assert state['actors'] and all(a['quiet'] for a in state['actors']),state
            if preference=='reduce':
                moving=page.locator('#rtg .seat svg').evaluate_all('xs=>xs.flatMap(x=>x.getAnimations({subtree:true})).filter(a=>a.playState==="running"&&a.effect.getKeyframes().some(f=>f.translate||f.transform||f.rotate||f.scale)).length')
                assert moving==0,moving
            assert not errors,errors
            assert not bad,bad
            print('PASS',preference,'tension/reduced-motion restraint; JS/HTTP0',flush=True)
            page.close()
        browser.close()


if __name__=='__main__':main()
