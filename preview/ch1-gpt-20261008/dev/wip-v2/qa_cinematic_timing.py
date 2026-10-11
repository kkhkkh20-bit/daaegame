"""Native scene/camera continuity through direction gaps and stale image loads.

Uses prepared authored prologue locations and the existing controller, with
real keyboard/pointer turns. This is a timing regression, not a full playthrough.
"""
import argparse
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--viewport',choices=['both','landscape','portrait'],default='both')
    parser.add_argument('--screenshots',default='/tmp/cinematic-timing')
    args=parser.parse_args()
    output=Path(args.screenshots);output.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        viewports=[{'width':844,'height':390},{'width':390,'height':844}]
        if args.viewport!='both':
            viewports=[v for v in viewports if (v['width']>v['height'])==(args.viewport=='landscape')]
        for viewport in viewports:
            page=browser.new_page(viewport=viewport)
            errors=[];bad=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('response',lambda response:bad.append(response.url) if response.status>=400 and 'favicon' not in response.url else None)
            page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
            def engine(code):return page.evaluate('(code)=>window.__T(code)',code)
            engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
            page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1400)
            page.wait_for_function('typeof __innPresentationState==="function"')
            def stop():
                engine('if(DL){DL.done=null;endDlg()}')
                page.evaluate('__innStoryCinematicReset()')
                page.wait_for_timeout(180)
            def start(sid):
                stop()
                engine(f'G.beats={{inn_pi:EP1INN.PRO.findIndex(s=>s.sid==={json.dumps(sid)})}};__innStart()')
            def state():
                return engine('({sid:G.beats.inn_psid,done:!!G.beats.inn_pro,dl:!!DL,who:DL&&DL.lines[DL.i]&&DL.lines[DL.i][0],text:DL&&String(DL.lines[DL.i][7]||DL.lines[DL.i][1])||""})')
            def presentation():
                return page.evaluate('()=>{var p=__innPresentationState();return {sid:p.sid,owner:p.owner,camera:p.camera,cut:p.cut,ready:p.ready,transitioning:p.transitioning}}')
            def trace():
                page.evaluate('''()=>{window.__timingFrames=[];window.__timingNodes=new WeakMap();window.__timingNodeCounter=0;
                  window.__timingRAF=requestAnimationFrame(function frame(){var p=__innPresentationState(),n=document.querySelector('#inn-story-cg');
                    if(n&&!__timingNodes.has(n))__timingNodes.set(n,++__timingNodeCounter);
                    __timingFrames.push({t:performance.now(),sid:p.sid,owner:p.owner,cut:p.cut,ready:p.ready,
                      visible:!!(n&&n.classList.contains('ready')),node:n&&__timingNodes.get(n),dl:__T('!!DL'),
                      cue:p.cue,banner:!!document.querySelector('.banner')});
                    window.__timingRAF=requestAnimationFrame(frame)});}''')
            def frames():
                page.evaluate('cancelAnimationFrame(window.__timingRAF)')
                return page.evaluate('window.__timingFrames')
            def turn():
                page.keyboard.press('Enter');page.wait_for_timeout(180)

            # P1 uses two deliberately separate CGs. Hold the driver image's
            # first real request to prove the previous shot survives decoding.
            driver_ready=page.evaluate('!!__innStoryArt.driver')
            held_driver=[]
            if driver_ready:
                page.route('**/art/ch1/cinematics/carriage-driver-close.png',lambda route:held_driver.append(route))
            start('P1');trace();driver_seen=False;driver_released=False
            for _ in range(280):
                s=state();p=presentation()
                if p['camera']=='driver' and not driver_released:
                    if driver_ready:
                        page.wait_for_timeout(100)
                        assert held_driver,'Driver CG request was not intercepted'
                        assert presentation()['cut']=='carriage' and not presentation()['ready'],'Next CG exposes the old native stage while decoding'
                        assert page.locator('#inn-story-cg').count()==1,'The committed family picture disappears during loading'
                        page.wait_for_timeout(200)
                        assert presentation()['cut']=='carriage','Family camera changed before driver picture decoded'
                        for route in held_driver:route.continue_()
                        page.unroute('**/art/ch1/cinematics/carriage-driver-close.png')
                        page.wait_for_function('__innStoryCinematics().cut==="driver"&&__innStoryCinematics().visible')
                    driver_released=True
                if s['who']=='karo':
                    driver_seen=True
                    if driver_ready:
                        assert presentation()['cut']=='driver','Karo speaks under the family picture'
                        page.screenshot(path=str(output/f'P1-driver-{viewport["width"]}x{viewport["height"]}.png'))
                if driver_seen and s['sid']=='P1' and s['who']=='det0':
                    assert presentation()['camera']=='driver','Father reply resets the family camera'
                if s['sid']=='P2' and s['dl']:break
                if s['dl']:turn()
                else:page.wait_for_timeout(80)
            else:raise AssertionError('P1 native camera sequence did not reach P2')
            p1=frames();assert driver_seen,'The authored driver entry was skipped'
            if driver_ready:
                shots=[f for f in p1 if f['sid']=='P1' and f['visible']]
                sequence=[]
                for f in shots:
                    if not sequence or sequence[-1]!=f['cut']:sequence.append(f['cut'])
                assert sequence==['carriage','driver'],('P1 jumps between old/native/family/driver pictures',sequence)
                first=shots[0]['t'];last=shots[-1]['t'];inside=[f for f in p1 if f['sid']=='P1' and first<=f['t']<=last and not f['banner']]
                assert all(f['visible'] for f in inside),'Native stage flashes between the two P1 pictures'
                assert len({f['node'] for f in shots if f['cut']=='carriage'})==1,'Family CG was recreated during P1'
                assert len({f['node'] for f in shots if f['cut']=='driver'})==1,'Driver CG was recreated during P1'

            # P2 contains a genuine DL=null @dir between the first observation
            # and Daram's arrival. It must retain one decoded picture instance.
            start('P2');trace()
            for _ in range(140):
                s=state()
                if s['sid']=='P3':break
                if s['dl']:turn()
                else:page.wait_for_timeout(80)
            else:raise AssertionError('P2 native transition did not reach P3')
            p2=frames();shown=[f for f in p2 if f['sid']=='P2' and f['visible']]
            assert shown,'P2 arrival picture never appeared'
            started=shown[0]['t'];stable=[f for f in p2 if f['sid']=='P2' and f['t']>=started and not f['banner']]
            assert all(f['cut']=='village' and f['visible'] and f['ready'] for f in stable),('P2 camera disappeared between native batches',stable)
            assert len({f['node'] for f in stable})==1,'P2 repeatedly rebuilt the arrival image'
            assert any(not f['dl'] for f in stable),'No actual P2 direction gap was exercised'
            assert presentation()['transitioning'],'New scene commits audio under its native banner'
            assert page.locator('#inn-story-cg').count()==0,'P2 picture leaks into P3'
            page.screenshot(path=str(output/f'P2-to-P3-{viewport["width"]}x{viewport["height"]}.png'))
            page.wait_for_function('!!__T("DL")')
            stop()

            # The seal stays intact across Neoul -> Seryeon directions, then
            # retires at the authored cutting action. It never returns later.
            start('P13');trace();seal_seen=False;cut_seen=False;screen_taken=False
            for _ in range(500):
                s=state();p=presentation()
                if p['cut']=='seal' and p['ready']:
                    seal_seen=True
                    if not screen_taken:
                        page.screenshot(path=str(output/f'P13-seal-{viewport["width"]}x{viewport["height"]}.png'));screen_taken=True
                if s['text'].startswith('너울이 봉인띠를 자르고'):
                    cut_seen=True
                    assert p['camera']=='stage' and p['cut'] is None,'Intact seal picture survives its opening action'
                if cut_seen:assert p['cut'] is None,'Intact seal returns after it was opened'
                if s['done']:break
                if s['dl']:turn()
                else:page.wait_for_timeout(80)
            else:raise AssertionError('P13 native controller failed to complete')
            p13=frames();seal=[f for f in p13 if f['cut']=='seal' and f['visible']]
            assert seal_seen and cut_seen,'Native seal reveal/opening was skipped'
            assert len({f['node'] for f in seal})==1,'Seal shot restarted during character directions'
            first=seal[0]['t'];last=seal[-1]['t'];inside=[f for f in p13 if first<=f['t']<=last]
            assert all(f['cut']=='seal' and f['visible'] and f['ready'] for f in inside),('Seal camera flickers during its owned beat',inside)
            assert any(not f['dl'] for f in inside),'No genuine seal direction gap was exercised'
            assert not page.evaluate('document.body.classList.contains("inn-story-cg-active")'),'Original stage stays hidden after opening'
            assert page.locator('#inn-story-cg').count()==0,'Seal picture survives investigation start'
            page.screenshot(path=str(output/f'P13-investigation-{viewport["width"]}x{viewport["height"]}.png'))

            # A captured game's loaded picture cannot be adopted by a newly
            # loaded game, even if the old dialogue object still exists.
            stop()
            engine('var oldScene=EP1INN.PRO.find(s=>s.sid==="P2");G.beats={inn_pi:EP1INN.PRO.indexOf(oldScene),inn_bg:oldScene.bg};render();say([["det1","겨울잠 여관! 언덕 위래."]],function(){})')
            page.wait_for_function('__innStoryCinematics().visible')
            engine('var replacement=fresh(G.ci);replacement.introDone=true;replacement.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P1"),inn_bg:"carriage"};G=replacement;S.prog.inn=replacement')
            page.wait_for_timeout(100)
            assert not presentation()['ready'],'New game adopts the previous game dialogue as a camera cue'
            assert page.locator('#inn-story-cg').count()==0,'Old decoded image survived captured G change'
            stop()

            # The night walk owns a captured game as well. Moving to another
            # game while its dialogue remains cannot leave the bedroom overlay
            # or darkening/hiding classes over the new investigation.
            start('P10b')
            page.wait_for_function('__innOpeningDirection().ready')
            engine('var nightReplacement=fresh(G.ci);nightReplacement.introDone=true;nightReplacement.beats={inn_pro:1};G=nightReplacement;S.prog.inn=nightReplacement')
            page.wait_for_timeout(100)
            assert page.locator('#inn-night-walk').count()==0,'Night overlay adopts a replacement game'
            assert not page.evaluate('document.body.classList.contains("inn-night-direction")||document.body.classList.contains("inn-night-dark")'),'Night scene leaves actor hiding/darkening on a replacement game'
            assert not presentation()['ready'],'Replacement investigation commits the previous night dialogue'
            stop()

            # Hold the actual image request, leave its game, then deliver it.
            # This exercises a real delayed onload, rather than calling handlers.
            held=[]
            page.route('**/art/ch1/cinematics/carriage-family-close.png',lambda route:held.append(route))
            engine('G.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P1"),inn_bg:"carriage"};render();say([["det1","마지막 봉지야. 작은 반은 아빠 몫!"]],function(){})')
            page.wait_for_function('__innStoryCinematics().loading==="carriage"')
            page.wait_for_timeout(100)
            assert held,'Delayed CG request was not intercepted'
            assert not presentation()['ready'],'Image is committed before decoding'
            engine('if(DL){DL.done=null;endDlg()};G.beats={inn_pro:1};render()')
            page.wait_for_timeout(50)
            for route in held:route.continue_()
            page.unroute('**/art/ch1/cinematics/carriage-family-close.png')
            page.wait_for_timeout(300)
            assert page.locator('#inn-story-cg').count()==0,'Late image reattached its previous scene'
            assert not page.evaluate('document.body.classList.contains("inn-story-cg-active")'),'Late image hides the current stage'
            assert not errors,errors
            assert not bad,bad
            print('PASS',viewport,'native P1/P2/P13 camera continuity, driver atomic decode:',driver_ready,'actual null-DL directions, banner commit, seal opening, captured-game and real delayed-onload cleanup; JS/HTTP errors 0',flush=True)
            page.close()
        browser.close()


if __name__=='__main__':main()
