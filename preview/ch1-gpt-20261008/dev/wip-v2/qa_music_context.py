"""Prepared authored dialogue checks for mood music and the live media engine.

Uses actual EP lines, not injected music cues. This is a focused fixture, not
a fresh full-game walkthrough or a subjective listening/real-device test.
"""
import json
import shutil
from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    browser=playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':844,'height':390})
    errors=[];bad=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    page.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');page.wait_for_timeout(16000)
    def engine(code):return page.evaluate('(code)=>window.__T(code)',code)
    engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
    page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1500)
    page.mouse.click(1,1)
    engine('S.sound=true;ac();AC.resume();window.__AUD.sceneGate(false)')
    rows=[]
    def clear():
        engine('if(DL){DL.done=null;endDlg()};window.__innAudioReset();G.beats={inn_pro:1,inn_i9:1};G.tab="scene";G.who=null')
        page.wait_for_timeout(150)
    def expect(label,key,line=None):
        # The real dialogue controller may introduce a character before the
        # selected authored line. Advance that introduction with native input.
        for _ in range(80):
            page.wait_for_timeout(200)
            actual=page.evaluate('__innWant()')
            if actual==key and (not line or line in page.evaluate('__innAudioState().line')):break
            if not engine('!!DL'):break
            page.keyboard.press('Enter')
        assert actual==key,(label,actual,key,page.evaluate('__innAudioState()'))
        if line:assert line in page.evaluate('__innAudioState().line'),(label,line,page.evaluate('__innAudioState()'))
        page.wait_for_function('(key)=>__AUD.cur===key',arg=key,timeout=10000)
        rows.append({'scene':label,'key':key,'line':page.evaluate('__innAudioState().line')})

    clear();expect('idle investigation','inn_inv')
    clear();engine('G.tab="talk";G.who="nabi";say([EP1INN.TALK.nabi.find(t=>t.id==="T_na3").lines[0]],function(){})')
    expect('Nabi friendly conversation','inn_friend','할머니는 어떤 분입니까?')
    # Re-reading/changing an ordinary line inside this same dialogue must not
    # start another song source every time the player advances text.
    before=page.evaluate('__AUD.stats.inst')
    for _ in range(8):page.evaluate('__innWant();__AUD.tick()')
    page.wait_for_timeout(400)
    assert page.evaluate('__AUD.stats.inst')==before,'Same mood restarts the media instance'

    clear();engine('G.tab="talk";G.who="buri";say([EP1INN.TALK.buri.find(t=>t.id==="T_bu3").lines[1]],function(){})')
    expect('Cold guest claim','inn_serious','차갑고')
    clear();engine('G.tab="talk";G.who="geokkuri";say([EP1INN.TALK.geokkuri.find(t=>t.id==="T_ba3").lines.find(l=>String(l[1]).includes("당연하죠. 그게 똑바론데요"))],function(){})')
    expect('Bami upside-down joke','inn_comic','당연하죠. 그게 똑바론데요')
    clear();engine('G.tab="talk";G.who="geokkuri";say([EP1INN.TALK.geokkuri.find(t=>t.id==="C13").lines[1]],function(){})')
    expect('Bami useful witness account','inn_inv')

    clear();engine('G.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P3")};say([EP1INN.PRO.find(s=>s.sid==="P3").items.find(l=>Array.isArray(l)&&l[0]==="innma"&&String(l[1]).startsWith("어서 와요"))],function(){})')
    expect('First inn welcome','inn_friend')
    engine('if(DL){DL.done=null;endDlg()};say([EP1INN.PRO.find(s=>s.sid==="P3").items.find(l=>Array.isArray(l)&&String(l[1]).includes("아이 엄마를 찾고"))],function(){})')
    expect('Mother question changes same scene','inn_serious')
    engine('if(DL){DL.done=null;endDlg()};say([EP1INN.PRO.find(s=>s.sid==="P3").items.find(l=>Array.isArray(l)&&String(l[1]).startsWith("우선 들어와요"))],function(){})')
    expect('Welcome returns gently','inn_friend')
    clear();engine('G.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P10")};say([EP1INN.PRO.find(s=>s.sid==="P10").items.find(l=>Array.isArray(l)&&String(l[1]).startsWith("크르르"))],function(){})')
    expect('Family monster voice','inn_comic')
    engine('if(DL){DL.done=null;endDlg()};say([EP1INN.PRO.find(s=>s.sid==="P10").items.find(l=>Array.isArray(l)&&String(l[1]).startsWith("아빠처럼 탐정 할래"))],function(){})')
    expect('Family promise','inn_friend')

    clear();engine('say([EP1INN.LOCS.find(l=>l.id==="bed13").obs.find(o=>o.id==="o_under").say.find(l=>String(l[1]).startsWith("…상자 뒤"))],function(){})')
    page.wait_for_timeout(250)
    assert page.evaluate('__innTense()') and page.evaluate('__innWant()') is None,'Discovery loses its silence'
    page.wait_for_function('__AUD.cur===null',timeout=5000)
    clear();engine('G.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P10b")};')
    assert page.evaluate('__innWant()') is None,'Night corridor starts a friendly/comic song'
    clear();expect('Return to investigation','inn_inv')
    mapping=page.evaluate('Object.fromEntries(["inn_inv","inn_serious","inn_comic","inn_friend"].map(k=>[k,__AUD.SONGS[k].media]))')
    assert len(set(mapping.values()))==4 and all(v.startswith('audio/v4/') for v in mapping.values()),mapping
    assert not errors,errors
    assert not bad,bad
    print('PASS authored mood turns, live media sources, same-mood continuity, discovery/night silence; JS/HTTP errors 0',flush=True)
    print(json.dumps({'scenes':rows,'files':mapping},ensure_ascii=False),flush=True)
    browser.close()
