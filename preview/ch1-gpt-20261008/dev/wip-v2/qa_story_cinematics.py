"""Authored opening pictures: real dialogue input, source cues, and cleanup.

Focused prepared scenes, not a claim of a full fresh-game or phone-device run.
Screenshots preserve both faces/clues in portrait and landscape for review.
"""
import argparse
import json
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright


parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
parser.add_argument('--screenshots',default='/tmp/story-cinematics-qa')
parser.add_argument('--viewport',choices=['both','landscape','portrait'],default='both')
args=parser.parse_args()
output=Path(args.screenshots);output.mkdir(parents=True,exist_ok=True)

with sync_playwright() as playwright:
    browser=playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    viewports=[{'width':844,'height':390},{'width':390,'height':844}]
    if args.viewport!='both':viewports=[v for v in viewports if (v['width']>v['height'])==(args.viewport=='landscape')]
    for viewport in viewports:
        page=browser.new_page(viewport=viewport)
        errors=[];bad=[];requests=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('response',lambda response:bad.append(response.url) if response.status>=400 and 'favicon' not in response.url else None)
        page.on('request',lambda request:requests.append(request.url))
        page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
        page.wait_for_function('typeof __innStoryCinematics==="function"')
        def engine(code):return page.evaluate('(code)=>window.__T(code)',code)
        engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
        page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1500)

        def stop():
            engine('if(DL){DL.done=null;endDlg()}')
            page.wait_for_timeout(150)
        def prepare(sid):
            stop()
            engine(f'''var cinematicScene=EP1INN.PRO.find(s=>s.sid==={json.dumps(sid)});
              G.beats={{inn_pi:EP1INN.PRO.indexOf(cinematicScene),inn_bg:cinematicScene.bg}};
              G.loc=CASES[G.ci].locations.findIndex(l=>l.id===cinematicScene.loc);G.tab="scene";
              G.who=null;render();''')
            page.wait_for_timeout(250)
        def line():return engine('DL&&String(DL.lines[DL.i][7]||DL.lines[DL.i][1])||""')
        def expect(cut):
            page.wait_for_function('(cut)=>__innStoryCinematics().cut===cut&&__innStoryCinematics().visible',arg=cut,timeout=10000)
            image=page.locator('#inn-story-cg .cinema-picture')
            assert image.evaluate('(e)=>e.complete&&e.naturalWidth>0'),'CG did not decode'
            assert image.evaluate('(e)=>getComputedStyle(e).pointerEvents')=='none','Picture catches dialogue taps'
            assert page.locator('#innstage').evaluate('(e)=>getComputedStyle(e).visibility')=='hidden','Duplicate actor over CG'
            assert page.locator('#vnbox .vband').is_visible(),'Dialogue vanished under CG'
            if viewport['width']<viewport['height']:
                assert image.evaluate('(e)=>getComputedStyle(e).objectFit')=='contain','Portrait cuts off faces/clues'
                assert page.locator('#inn-story-cg .cinema-surround').is_visible(),'Portrait backdrop missing'
            page.wait_for_timeout(420)
            page.screenshot(path=str(output/f'{cut}-{viewport["width"]}x{viewport["height"]}.png'))

        # A build with no approved picture must not request its absent file.
        prepare('P1')
        art=page.evaluate('__innStoryArt')
        page.evaluate('__innStoryArt={carriage:false,village:false,seal:false}')
        first=len(requests)
        engine('say([EP1INN.PRO.find(s=>s.sid==="P1").items.find(l=>Array.isArray(l)&&l[0]==="det1")],function(){})')
        page.wait_for_timeout(250)
        assert page.locator('#inn-story-cg').count()==0,'Missing art hides the working stage'
        assert not any('/art/ch1/cinematics/' in url for url in requests[first:]),'Missing art was requested'
        stop();page.evaluate('(art)=>{window.__innStoryArt=art}',art)

        # P1 uses the existing play controller, all authored family lines and
        # native directions. The driver and father's answer restore the stage.
        prepare('P1')
        engine('window.__cinematicDone=0;__innPlay(EP1INN.PRO.find(s=>s.sid==="P1").items,function(){window.__cinematicDone++})')
        expect('carriage')
        original=engine('DL.i')
        for _ in range(2):page.mouse.click(viewport['width']*.5,viewport['height']*.5);page.wait_for_timeout(220)
        assert engine('DL.i')!=original,'A photo prevented native dialogue advancement'
        assert page.evaluate('__innStoryCinematics().cut')=='carriage','Same family conversation lost its picture'
        memory_seen=False
        for _ in range(140):
            if engine('DL&&DL.lines[DL.i][0]==="karo"'):break
            if not memory_seen and '엄마 찾으면' in line():
                page.wait_for_function('__innStoryCinematics().tone==="memory"')
                page.wait_for_timeout(400)
                assert page.locator('#inn-story-cg .cinema-picture').evaluate('(e)=>getComputedStyle(e).filter')!='none','Missing-mother cue kept the bright travel tone'
                page.screenshot(path=str(output/f'carriage-memory-{viewport["width"]}x{viewport["height"]}.png'))
                memory_seen=True
            page.keyboard.press('Enter');page.wait_for_timeout(180)
        assert memory_seen,'The mother-search cue was skipped'
        assert engine('DL&&DL.lines[DL.i][0]==="karo"'),'Driver cue unreachable'
        page.wait_for_timeout(100)
        assert page.locator('#inn-story-cg').count()==0,'Family cut remained behind the driver'
        assert page.locator('#innstage').evaluate('(e)=>getComputedStyle(e).visibility')=='visible','Actor did not return'
        for _ in range(50):
            if page.evaluate('window.__cinematicDone===1'):break
            page.keyboard.press('Enter');page.wait_for_timeout(180)
        assert page.evaluate('window.__cinematicDone===1'),'P1 controller completion changed or duplicated'

        prepare('P2')
        engine('__innPlay(EP1INN.PRO.find(s=>s.sid==="P2").items,function(){})')
        expect('village')
        # Removing the live dialogue on a transition must clean its picture in
        # the same DOM turn. No animation/timer may reattach an old layer.
        stop()
        assert page.locator('#inn-story-cg').count()==0,'Ended dialogue left its CG'
        assert not page.evaluate('document.body.classList.contains("inn-story-cg-active")'),'Actor hiding class leaked'

        prepare('P13')
        engine('say(EP1INN.PRO.find(s=>s.sid==="P13").items.filter(l=>Array.isArray(l)&&(/베개 밑|세련 씨 주머니가 맞습니까|맞습니다. 제 도장이에요/.test(l[1]))),function(){})')
        expect('seal')
        stop()
        engine('say([EP1INN.PRO.find(s=>s.sid==="P13").items.find(l=>Array.isArray(l)&&/너울 씨가 봉인띠를 자르고/.test(l[1]))],function(){})')
        page.wait_for_timeout(150)
        assert page.locator('#inn-story-cg').count()==0,'Intact seal still shown after it was cut'

        # An actual native skip button removes the picture, and reduced motion
        # shows the same picture without a fade or zoom.
        prepare('P1');page.emulate_media(reduced_motion='reduce')
        # #ovfz keeps a non-skippable veil for 700 ms. A prepared skippable
        # dialogue must begin after that native reuse period, so #skip is
        # actually created by the controller rather than added by this test.
        page.wait_for_timeout(800)
        engine('say([EP1INN.PRO.find(s=>s.sid==="P1").items.find(l=>Array.isArray(l)&&l[0]==="det1")],function(){},true)')
        expect('carriage')
        assert page.locator('#inn-story-cg .cinema-picture').evaluate('(e)=>getComputedStyle(e).animationName')=='none','Reduced-motion fade remains'
        page.locator('#skip').click();page.wait_for_timeout(150)
        assert page.locator('#inn-story-cg').count()==0,'Native skip left a picture'
        page.emulate_media(reduced_motion='no-preference')

        # Save a real prologue location, reload, and use the native Continue
        # button. The resumed scene must rebuild its own cut, without remnants.
        prepare('P2')
        engine('saveProg();persist();')
        page.reload(wait_until='domcontentloaded');page.wait_for_timeout(16000)
        assert page.locator('#inn-story-cg').count()==0,'Title screen shows stale saved CG'
        page.locator('#innmain [data-m="cont"]').click()
        expect('village')
        page.locator('#w209rail [data-more]').click()
        page.locator('#w209more [data-w="main"]').click()
        # The native Main action saves and reloads the full bundle. Wait for
        # its actual menu instead of treating a 200-ms reload as a failure.
        page.locator('#innmain').wait_for(state='visible',timeout=25000)
        assert page.locator('#innmain').count()==1,'Native main menu not reached'
        assert page.locator('#inn-story-cg').count()==0,'Returning to main left a CG'
        assert not errors,errors
        assert not bad,bad
        print('PASS',viewport,'authored 3 cuts, native tap/driver/skip, missing-art fallback, portrait/reduced motion, save-resume/main cleanup; JS/HTTP errors 0',flush=True)
        page.close()
    browser.close()
