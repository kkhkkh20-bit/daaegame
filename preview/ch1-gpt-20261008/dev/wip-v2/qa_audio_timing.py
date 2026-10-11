"""Authored scene music follows its committed picture; stale loops lose ownership.

Prepared scene fixtures use native dialogue/dir/card and WebAudio, not injected
music cues. This is a timing regression check, not a subjective listening test.
"""
import argparse
import json
import shutil
import time
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:8000/playT.html')
args = parser.parse_args()
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 844, 'height': 390})
    errors, bad = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('response', lambda r: bad.append(r.url) if r.status >= 400 and 'favicon' not in r.url else None)
    page.goto(args.url, wait_until='domcontentloaded')
    page.wait_for_function('typeof __innPresentationState === "function"', timeout=25000)
    page.wait_for_timeout(16000)
    def engine(code): return page.evaluate('(code)=>window.__T(code)', code)
    engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1}')
    page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()')
    page.wait_for_timeout(1500)
    page.mouse.click(1, 1)
    engine('S.sound=true;ac();AC.resume();window.__AUD.sceneGate(false)')
    page.evaluate('''window.__audioFrames=[];window.__audioLog=true;
      (function collect(){if(!window.__audioLog)return;
      const p=__innPresentationState(),a=__innAmb(),s=__innAudioState();
      __audioFrames.push({at:performance.now(),sid:p.sid,owner:p.owner,ready:p.ready,retained:!!(p.loading&&p.cut),transitioning:p.transitioning,cold:p.cold,camera:p.camera,music:a.music,want:a.want,amb:a.cur,heartbeat:s.heartbeatActive,coldHeartbeat:s.coldHeartbeat,line:s.line});
      if(__audioFrames.length>5000)__audioFrames.shift();requestAnimationFrame(collect)})();''')
    rows=[]
    def state(): return page.evaluate('({presentation:__innPresentationState().sid,audio:__innAudioState(),amb:__innAmb()})')
    def stop():
        engine('if(DL){DL.done=null;endDlg()}')
        page.wait_for_timeout(750)
    def prepare(sid):
        stop()
        engine('''var timingScene=EP1INN.PRO.find(s=>s.sid===%s);
          G.beats={inn_pi:EP1INN.PRO.indexOf(timingScene),inn_psid:timingScene.sid,inn_bg:timingScene.bg};
          G.loc=CASES[G.ci].locations.findIndex(l=>l.id===timingScene.loc);G.tab="scene";G.who=null;render();''' % json.dumps(sid))
        page.wait_for_timeout(200)
    def play(sid):
        engine('__innPlay(EP1INN.PRO.find(s=>s.sid===%s).items,function(){window.__timingDone=true})' % json.dumps(sid))
    def advance_until(predicate, limit=140):
        for _ in range(limit):
            if page.evaluate(predicate): return
            if page.evaluate('!!__innPresentationState().loading&&!__innPresentationState().ready'):
                page.wait_for_timeout(180);continue
            if page.locator('#rtgbar [data-g="next"]').is_visible(): page.locator('#rtgbar [data-g="next"]').click()
            elif page.locator('#rtnext').is_visible(): page.locator('#rtnext').click()
            else: page.keyboard.press('Enter')
            page.wait_for_timeout(180)
        raise AssertionError((predicate,state()))
    def wait_music(key):
        page.wait_for_function('(key)=>__innAmb().music===key', arg=key, timeout=10000)

    # A real location card blocks music and carriage before the delayed CG
    # commits. Its prior picture cannot start the next scene's score.
    prepare('P1')
    def delay_picture(route):
        time.sleep(1.2)
        route.continue_()
    page.route('**/art/ch1/cinematics/carriage-family-close.png', delay_picture)
    page.route('**/art/ch1/cinematics/carriage-driver-close.png', delay_picture)
    engine('window.__timingDone=false;banner(EP1INN.PRO.find(s=>s.sid==="P1").title,EP1INN.PRO.find(s=>s.sid==="P1").sub).then(function(){__innPlay(EP1INN.PRO.find(s=>s.sid==="P1").items,function(){window.__timingDone=true})})')
    page.wait_for_timeout(400)
    assert page.evaluate('!__innPresentationState().ready'), state()
    assert page.evaluate('__innAmb().music===null&&__innAmb().cur===null'), state()
    page.wait_for_function('__innPresentationState().ready&&__innPresentationState().sid==="P1"', timeout=15000)
    page.wait_for_function('__innAmb().cur==="carriage"', timeout=5000)
    wait_music('inn_travel')
    page.unroute('**/art/ch1/cinematics/carriage-family-close.png', delay_picture)
    made=page.evaluate('__AUD.stats.inst')
    # Native @dir gaps and split narration retain the same presentation owner.
    advance_until('__innAudioState().who==="karo"')
    page.wait_for_timeout(350)
    assert page.evaluate('__innAmb().cur===null'), state()
    assert page.evaluate('["stage","driver"].includes(__innPresentationState().camera)'), state()
    page.wait_for_function('__innPresentationState().ready',timeout=5000)
    assert page.evaluate('__AUD.stats.inst')==made, ('P1 source restarted across direction',state())
    page.unroute('**/art/ch1/cinematics/carriage-driver-close.png', delay_picture)
    rows.append({'scene':'P1 native dialogue/driver','state':state()})
    print('PASS P1 committed picture, native direction/driver, carriage stop, same score',flush=True)
    advance_until('window.__timingDone===true')

    # Same travel score remains paused behind the next real location card and
    # only resumes with the committed village picture.
    prepare('P2')
    engine('window.__timingDone=false;banner(EP1INN.PRO.find(s=>s.sid==="P2").title,EP1INN.PRO.find(s=>s.sid==="P2").sub).then(function(){__innPlay(EP1INN.PRO.find(s=>s.sid==="P2").items,function(){window.__timingDone=true})})')
    page.wait_for_timeout(400)
    if page.evaluate('!__innPresentationState().ready'):
        assert page.evaluate('__innAmb().music===null'), state()
    page.wait_for_function('__innPresentationState().ready&&__innPresentationState().sid==="P2"&&__innPresentationState().camera==="village"', timeout=10000)
    wait_music('inn_travel')
    assert page.evaluate('__innAmb().cur===null'), state()
    rows.append({'scene':'P2 village after card','state':state()})
    print('PASS P2 card→committed village music',flush=True)

    # The real ten-o-clock direction silences P10. Changing to the authored
    # night corridor cancels the remaining scheduled bells and keeps it quiet.
    prepare('P10'); play('P10')
    advance_until('__innAudioState().bell')
    page.wait_for_timeout(250)
    assert page.evaluate('__innAmb().music===null&&__innAudioState().scopedSources>0'), state()
    prepare('P10b'); play('P10b')
    page.wait_for_timeout(300)
    assert page.evaluate('__innAmb().music===null&&!__innAudioState().bell&&__innAudioState().scopedSources===0'), state()
    advance_until('__innAudioState().heartbeatActive')
    page.wait_for_timeout(700)
    assert page.evaluate('__innTense()'), state()
    rows.append({'scene':'P10b authored night pulse','state':state()})
    print('PASS P10 bells→P10b silence/pulse',flush=True)
    stop()
    engine('S.screen="board";render()')
    page.wait_for_timeout(400)
    assert page.evaluate('!__innTense()&&!__innAudioState().coldHeartbeat&&__innAudioState().scopedSources===0'), state()

    # Father's opening bypasses the former culprit camera for both entry paths.
    engine('S.screen="case";G=fresh(CASES.findIndex(c=>c.id==="inn"));G.beats={inn_pi:0,inn_bg:"carriage"};render();__innCold(function(){window.__coldTimingFinished=true})')
    assert page.evaluate('window.__coldTimingFinished===true&&!document.querySelector("#inncold")&&!__innAudioState().coldHeartbeat'),state()
    print('PASS father opening callback, no culprit camera or cold pulse',flush=True)
    # Retained legacy controller cancellation is a separate prepared fixture.
    engine('EP1INN.OPENING_POV="legacy";__innCold(function(){window.__legacyColdTimingFinished=true})')
    page.wait_for_function('__innAudioState().coldHeartbeat', timeout=4000)
    page.wait_for_timeout(400)
    assert page.evaluate('__innAmb().cur===null'), state()
    page.locator('#inncold .sk').click()
    page.wait_for_timeout(350)
    assert page.evaluate('!__innAudioState().coldHeartbeat'), state()
    page.wait_for_timeout(700)
    assert page.evaluate('!__innAudioState().coldHeartbeat'), 'Old cold callback restarted pulse'
    print('PASS cold skip cancels heartbeat generation',flush=True)
    engine('EP1INN.OPENING_POV="father"')
    # This cold fixture callback does not open a game scene; remove its input
    # shield explicitly before exercising menu ownership cleanup below.
    engine('document.querySelector("#inncold")?.remove();window.__innColdTransition=false;__AUD.sceneGate(false)')
    stop()
    # Native meeting metadata must survive owner initialization and still
    # distinguish pressure, silence, pulse and a calm return. All four lines
    # are reused from the authored council script rather than synthetic cues.
    engine('''G.beats={inn_pro:1,inn_i9:1};render();
      var timingPulse=EP1INN.MEET.phases[1].stms[0].ok.find(l=>l.audio==="pulse");
      var timingCalm=EP1INN.MEET.phases[1].stms[0].ok.find(l=>l.audio==="calm");
      var timingPress=EP1INN.MEET.phases.flatMap(p=>p.stms||[]).flatMap(l=>l.ok||[]).find(l=>l.audio==="press");
      var timingSilence=EP1INN.MEET.phases.flatMap(p=>p.stms||[]).flatMap(l=>l.ok||[]).find(l=>l.audio==="silence");
      __rtgReset();window.__inMeeting=false;
      __rtOpen(CASES[G.ci],{key:"qaAudioTiming",title:"원탁 회의",seats:[],phases:[{type:"talk",lines:[timingPress,timingSilence,timingPulse,timingCalm]}]})''')
    page.wait_for_function('__innAudioState().cue==="press"', timeout=5000)
    wait_music('inn_meet_press')
    advance_until('__innAudioState().cue==="silence"')
    page.wait_for_function('__innAmb().music===null', timeout=5000)
    advance_until('__innAudioState().cue==="pulse"')
    page.wait_for_function('__innTense()', timeout=5000)
    advance_until('__innAudioState().cue==="calm"')
    page.wait_for_function('!__innTense()', timeout=5000)
    wait_music('inn_meet')
    rows.append({'scene':'Native council authored pressure/silence/pulse/calm','state':state()})
    print('PASS native council pressure/silence/pulse/calm',flush=True)
    engine('__rtgReset();document.querySelector("body>.rt")?.remove();window.__inMeeting=false')
    page.wait_for_timeout(200)
    engine('G.beats={inn_pro:1,inn_final:1,inn_ei:1};S.screen="case";render();__innDir({who:"det1",sfx:"carDepart"})')
    page.wait_for_timeout(200)
    assert page.evaluate('__innAmb().dep'), state()
    engine('S.screen="board";render()')
    page.wait_for_timeout(400)
    assert page.evaluate('!__innAmb().dep&&__innAudioState().scopedSources===0'), state()
    page.evaluate('window.__audioLog=false')
    frames=page.evaluate('__audioFrames')
    retained=[f for f in frames if f['retained'] and f['sid']=='P1']
    if page.evaluate('__innStoryArt.driver===true'):
        assert retained, 'Delayed driver camera did not exercise atomic retention'
        assert all(f['music']=='inn_travel' and f['line']=='' for f in retained), ('Retained camera lost its score or emitted its next cue',retained)
    # Give audio's 220-ms poll / 80-ms turn fade a 400-ms boundary allowance.
    blocked_start=None
    for frame in frames:
        if frame['owner'] and not frame['ready'] and not frame['cold'] and not frame['retained']:
            if blocked_start is None: blocked_start=frame['at']
            if frame['at']-blocked_start>400:
                assert frame['music'] is None, ('Music before presentation commit',frame)
                assert frame['amb'] is None, ('Ambience before presentation commit',frame)
        else: blocked_start=None
    assert not errors, errors
    assert not bad, bad
    print('PASS picture/card/music owner, native @dir continuity, P1→P2, P10→P10b, bell/pulse/cold/departure cancellation; JS/HTTP errors 0', flush=True)
    print(json.dumps(rows,ensure_ascii=False), flush=True)
    browser.close()
