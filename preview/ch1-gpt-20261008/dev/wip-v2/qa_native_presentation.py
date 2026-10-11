"""Prepared-state ownership regression for native prologue presentation.

This is not a fresh-game walkthrough. It invokes the existing __innPlay and
__innStart controllers, then deliberately changes S.screen, G or the authored
pro/end index before a native continuation can run. The main-screen fixture
changes only S.screen to "board", retaining G to isolate the screen guard;
it is not a main-menu click walkthrough. Direction timers execute
normally. Only the browser fixture's banner function is temporarily replaced
with a deferred Promise, making old/new owner release deterministic. No engine
source, dialogue data, evidence or production assets are edited by this test.
Normal current owners complete through real Enter input. A separate final check
restores the real banner implementation and verifies the actual P5 chapter card
and automatic progression, including its presentation pause.
"""
import argparse
import json
import shutil
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--only-real-title',action='store_true',help='Only verify actual native chapter-card DOM and normal progression')
    args=parser.parse_args()
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':844,'height':390})
        errors=[];bad=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('response',lambda response:bad.append(response.url) if response.status>=400 and 'favicon' not in response.url else None)
        page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
        def state(code):return page.evaluate('(code)=>window.__T(code)',code)
        state('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
        page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1400)
        state('if(DL){DL.done=null;endDlg()};window.__qaNativePending=[];window.__qaNativeSavedBanner=banner;banner=function(title,sub){return new Promise(function(resolve){window.__qaNativePending.push({title:title,sub:sub,resolve:resolve})})};window.__qaNativeDone=0;')
        print('INFO prepared native state; real dir timers, deferred banner Promise; window.banner exposed:',page.evaluate('typeof window.banner'),flush=True)
        def prepare(phase='pro',sid='P3'):
            beats={'inn_pi':state(f'EP1INN.PRO.findIndex(s=>s.sid==={json.dumps(sid)})')} if phase=='pro' else {'inn_pro':1,'inn_final':1,'inn_ei':0}
            state(f'''if(DL){{DL.done=null;endDlg()}};S.screen="case";
                G=fresh(CASES.findIndex(c=>c.id==="inn"));G.introDone=true;S.prog.inn=G;
                G.beats={json.dumps(beats)};G.tab="scene";G.who=null;render();
                while(window.__qaNativePending.length)window.__qaNativePending.shift().resolve();
                window.__qaNativeDone=0;''')
            page.wait_for_timeout(70)
            assert not state('!!DL'),'A previous fixture reintroduced dialogue'
            assert page.evaluate('window.__qaNativePending.length')==0,'A previous fixture reopened a banner'
        def release():
            assert page.evaluate('window.__qaNativePending.length')==1,'Native banner release is ambiguous'
            page.evaluate('window.__qaNativePending.shift().resolve()')
            page.wait_for_timeout(100)
        def no_continuation(label):
            assert not state('!!DL'),(label,'Old owner inserted dialogue',state('DL&&DL.lines'))
            assert page.evaluate('window.__qaNativeDone')==0,(label,'Old owner completed')
            assert page.evaluate('window.__qaNativePending.length')==0,(label,'Old owner opened another banner')
            print('PASS',label,flush=True)
        def mutate(kind):
            if kind=='pro sid':state('G.beats.inn_pi=EP1INN.PRO.findIndex(s=>s.sid==="P13")')
            elif kind=='end sid':state('G.beats.inn_ei=1')
            elif kind=='main screen':state('S.screen="board"')
            elif kind=='replacement G':state('var nativeReplacement=fresh(G.ci);nativeReplacement.introDone=true;nativeReplacement.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P3")};G=nativeReplacement;S.prog.inn=nativeReplacement')
            else:raise AssertionError(kind)
        def complete_current(expected):
            page.wait_for_function('!!__T("DL")')
            assert state('String(DL.lines[DL.i][7]||DL.lines[DL.i][1])')==expected
            for _ in range(25):
                if page.evaluate('window.__qaNativeDone')==1:break
                page.keyboard.press('Enter');page.wait_for_timeout(150)
            assert page.evaluate('window.__qaNativeDone')==1,'Current owner did not complete'
            assert not state('!!DL'),'Current owner left dialogue open'
            page.wait_for_timeout(80)
            assert page.evaluate('window.__qaNativeDone')==1,'Current owner completed twice'
        def real_title():
            # Restore the real implementation for this separate visual check.
            # The preceding deterministic assertions exercise Promise ownership;
            # this one confirms the actual chapter card exists and expires.
            state('banner=window.__qaNativeSavedBanner')
            page.evaluate('''()=>{window.__qaNativeRealBanners=[];window.__qaNativeRealObserver=new MutationObserver(records=>records.forEach(r=>Array.from(r.addedNodes).forEach(n=>{if(n.nodeType===1&&n.matches('.banner'))window.__qaNativeRealBanners.push({text:n.textContent,t:performance.now()})})));window.__qaNativeRealObserver.observe(document.body,{childList:true})}''')
            prepare(sid='P5');state('__innStart()')
            observed=False
            for _ in range(240):
                card=page.evaluate('''()=>{var normal=s=>s.replace(/\\s+/g,' ').trim(),title=normal(__T('EP1INN.title')),e=Array.from(document.querySelectorAll('.banner')).find(n=>{var b=n.querySelector('.mid b');return b&&normal(b.textContent)===title});
                    if(!e)return null;var r=e.getBoundingClientRect(),p=__innPresentationState();return {text:e.innerText,width:r.width,height:r.height,ready:p.ready,transitioning:p.transitioning,dl:__T('!!DL'),sid:__T('G.beats.inn_psid')}}''')
                if card:
                    assert card['width']>0 and card['height']>0,'Native chapter card is present but has no visible layout'
                    assert state('EP1INN.chapter') in card['text'],'Native chapter subtitle is missing'
                    assert not card['dl'] and not card['ready'] and card['transitioning'],'Native chapter card overlaps committed dialogue/music'
                    assert card['sid']=='P5','Native chapter card belongs to a later scene'
                    # Capture once the native letter animation has finished.
                    page.wait_for_timeout(1000)
                    page.screenshot(path='/tmp/native-P5-chapter-title.png')
                    observed=True;break
                if state('!!DL'):page.keyboard.press('Enter')
                page.wait_for_timeout(130)
            if not observed:
                print('DIAG actual banners:',json.dumps(page.evaluate('window.__qaNativeRealBanners.map(b=>({text:b.text,t:b.t}))'),ensure_ascii=False),flush=True)
                print('DIAG final:',json.dumps(state('({pi:G.beats.inn_pi,sid:G.beats.inn_psid,screen:S.screen,dl:DL&&{i:DL.i,typing:DL.typing,line:DL.lines[DL.i]},pro:G.beats.inn_pro})'),ensure_ascii=False),flush=True)
                page.screenshot(path='/tmp/native-P5-title-diagnostic.png')
            page.evaluate('window.__qaNativeRealObserver.disconnect()')
            assert observed,'Actual native P5 chapter title never appeared'
            page.wait_for_function('__T("G.beats.inn_psid")==="P10"',timeout=5000)
            page.wait_for_function('!!__T("DL")',timeout=5000)
            assert state('G.beats.inn_psid')=='P10','Actual native chapter card did not advance normally'
            print('PASS actual native P5 chapter card DOM, subtitle, presentation pause and automatic P10 progression',flush=True)

        try:
            if args.only_real_title:
                real_title()
                assert not errors,errors
                assert not bad,bad
                print('PASS actual native chapter card; JS/HTTP errors 0',flush=True)
                return
            # Native item sequencing: the delayed direction and banner branches
            # must each reject all four changes, including same-G scene changes.
            for kind in ['pro sid','end sid','main screen','replacement G']:
                for mechanism in ['dir','banner']:
                    prepare('end' if kind=='end sid' else 'pro')
                    if mechanism=='dir':
                        state('__innPlay([{dir:{ms:180}},["det1","QA STALE DIR"]],function(){window.__qaNativeDone++})')
                    else:
                        state('__innPlay([{banner:["QA delayed place","QA time"]},["det1","QA STALE BANNER"]],function(){window.__qaNativeDone++})')
                        assert page.evaluate('window.__qaNativePending.length')==1
                    mutate(kind)
                    if mechanism=='banner':release()
                    else:page.wait_for_timeout(280)
                    no_continuation('native '+mechanism+' rejects '+kind)
            for phase in ['pro','end']:
                prepare(phase)
                state('__innPlay([{dir:{ms:180}},["det1","QA CURRENT DIR"]],function(){window.__qaNativeDone++})')
                complete_current('QA CURRENT DIR')
                print('PASS native dir progresses current '+phase+' owner with real Enter',flush=True)
            prepare()
            state('__innPlay([{banner:["QA current place","QA time"]},["det1","QA CURRENT BANNER"]],function(){window.__qaNativeDone++})')
            release();complete_current('QA CURRENT BANNER')
            print('PASS native banner progresses current owner with real Enter',flush=True)

            # __innStart enters the actual runPro controller. Its initial place
            # banner cannot start old authored P2 dialogue after owner changes.
            for kind in ['pro sid','main screen','replacement G']:
                prepare(sid='P2');state('__innStart()')
                assert page.evaluate('window.__qaNativePending.length')==1
                mutate(kind);release();no_continuation('runPro initial banner rejects '+kind)
            prepare(sid='P2');state('__innStart()');release()
            page.wait_for_function('!!__T("DL")')
            expected=state('EP1INN.PRO.find(s=>s.sid==="P2").items.find(Array.isArray)[1]')
            assert state('String(DL.lines[DL.i][7]||DL.lines[DL.i][1])')==expected,'Current runPro banner did not start authored P2'
            print('PASS current runPro place banner starts authored scene',flush=True)

            # Exercise P5's real authored dialogue/directions before releasing
            # its chapter-title Promise. This is the distinct after-title branch.
            for kind in ['pro sid','replacement G','current owner']:
                prepare(sid='P5');state('__innStart()');release()
                for _ in range(180):
                    if page.evaluate('window.__qaNativePending.length')==1:break
                    if state('!!DL'):page.keyboard.press('Enter')
                    page.wait_for_timeout(130)
                assert page.evaluate('window.__qaNativePending.length')==1,('Authored P5 never opened its chapter title',state('({pi:G.beats.inn_pi,sid:G.beats.inn_psid,dl:!!DL})'))
                assert page.evaluate('window.__qaNativePending[0].title')==state('EP1INN.title'),'P5 resumed another place banner before its chapter title'
                assert not state('!!DL'),'Chapter title overlaps live dialogue'
                if kind!='current owner':
                    mutate(kind);release();no_continuation('runPro chapter title rejects '+kind)
                else:
                    release()
                    expected_sid=state('EP1INN.PRO[EP1INN.PRO.findIndex(s=>s.sid==="P5")+1].sid')
                    assert state('G.beats.inn_psid')==expected_sid,'Current chapter title did not advance to next authored scene'
                    assert page.evaluate('window.__qaNativePending.length')==1,'Current chapter title did not request next scene place banner'
                    release();page.wait_for_function('!!__T("DL")')
                    print('PASS current runPro chapter title advances and starts authored '+expected_sid,flush=True)
            real_title()
            assert not errors,errors
            assert not bad,bad
            print('PASS prepared native presentation ownership; stale timers/Promises rejected, current native owners progress; JS/HTTP errors 0',flush=True)
        finally:
            state('if(DL){DL.done=null;endDlg()};S.screen="board";banner=window.__qaNativeSavedBanner;while(window.__qaNativePending.length)window.__qaNativePending.shift().resolve()')
            browser.close()


if __name__=='__main__':main()
