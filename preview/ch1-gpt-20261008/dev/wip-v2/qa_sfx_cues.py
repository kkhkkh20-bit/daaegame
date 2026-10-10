"""Assert cue regression on the actual compiled page.
Prepared chapter/phase fixtures, not a fresh-game playthrough or listening review.
Uses production dialogue, grant/card handlers, phase objects, music selector and
recorded-source statistics. AudioContext is unlocked by a trusted pointer event.
"""
import json
import os
import shutil
from playwright.sync_api import sync_playwright

URL = os.environ.get('SFX_QA_URL', 'http://127.0.0.1:8000/playT.html')
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 844, 'height': 390})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(URL, wait_until='domcontentloaded')
    page.wait_for_function('window.__T && window.__w209boot && window.__innRecordedSfx', timeout=30000)
    page.wait_for_timeout(16000)

    def run(code):
        return page.evaluate('(code)=>window.__T(code)', code)

    run('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
    page.evaluate('document.querySelector("#innmain")?.remove();window.__w209boot()')
    page.wait_for_timeout(1000)
    run('if(DL){DL.done=null;endDlg()};G.tab="scene";render();window.__sfxAudit=[];["cut9","shock9","found","door","doorOpen","carStop","carDepart"].forEach(k=>{var old=SFX[k];if(old)SFX[k]=function(){window.__sfxAudit.push(k);return old.apply(this,arguments)}})')
    page.evaluate('document.addEventListener("pointerdown",()=>window.__T("S.sound=true;ac().resume()"),{once:true})')
    page.locator('#w209rail [data-w="scene"]').click()
    page.wait_for_function('window.__T("AC && AC.state===\\"running\\"")')
    page.wait_for_timeout(1800)

    def clear():
        run('if(DL){DL.done=null;endDlg()};closeModal();window.__innAudioReset();window.__sfxAudit=[];')

    def state():
        return page.evaluate('()=>({state:__innAudioState(),tense:__innTense(),want:__innWant(),calls:__sfxAudit.slice()})')

    def check(label, condition, data):
        assert condition, f'{label}: {json.dumps(data, ensure_ascii=False)}'
        print('PASS', label, json.dumps(data, ensure_ascii=False), flush=True)

    def speak(who, text, mood=''):
        run('if(DL){DL.done=null;endDlg()};say(' + json.dumps([[who, text, mood]], ensure_ascii=False) + ');')
        page.wait_for_timeout(180)

    clear()
    speak('det1', '…상자 뒤에 뭐가 있어. 털… 같은 거.')
    data = state()
    check('discovery silence/pulse cue', data['tense'] and data['want'] is None and 'cut9' not in data['calls'], data)
    page.wait_for_function('__innAudioState().heartbeat>0', timeout=3000)
    check('discovery heartbeat actually ticks', state()['state']['heartbeat'] > 0, state())
    speak('det0', '바구니랑 수건 좀 빌려 와. 너울 씨께도 알리고.')
    page.wait_for_timeout(1300)
    data = state()
    check('rescue stops heartbeat', not data['tense'], data)

    clear()
    speak('det0', '…엄마 글씨가 맞아.')
    data = state()
    check('mother key breath without impact', data['state']['key'] and not any(k in data['calls'] for k in ('cut9','shock9')), data)
    clear()
    speak('innma', '…솜솜이 아니냐?', 'shock')
    data = state()
    check('grandmother expression without shock sound', 'shock9' not in data['calls'], data)

    clear()
    run('G.found=G.found.filter(id=>id!=="C03");say([["@grant","C03"]],function(){});')
    page.wait_for_timeout(900)
    data = state()
    check('C03 grant one acquisition sound', data['calls'].count('found') == 1 and run('G.found.includes("C03")'), data)
    clear()
    run('G.found=G.found.filter(id=>id!=="C03");G.asked=G.asked.filter(id=>id!=="C03");G.who="nabi";G.tab="talk";render();')
    page.wait_for_timeout(1000)
    page.locator('[data-ask="C03"]').first.click()
    page.wait_for_timeout(350)
    started = run('({asked:G.asked.includes("C03"),dialogue:!!DL})')
    check('native C03 pointer starts dialogue', started['asked'] and started['dialogue'], started)
    for _ in range(60):
        if page.locator('#okfind').is_visible():
            break
        page.keyboard.press('Enter')
        page.wait_for_timeout(130)
    data = state()
    data['cardVisible'] = page.locator('#okfind').is_visible()
    data['asked'] = run('G.asked.includes("C03")')
    check('native C03 question reaches evidence card', data['cardVisible'] and data['asked'], data)
    check('native C03 question one acquisition sound', data['calls'].count('found') == 1, data)
    clear()
    run('G.found=G.found.filter(id=>id!=="C07");window.__innPlay([{grant:"C07",card:true}],function(){});')
    page.wait_for_timeout(900)
    data = state()
    check('card evidence one acquisition sound', data['calls'].count('found') == 1 and page.locator('#okfind').is_visible(), data)

    # Prepared native M5 states, including a cached visible vote panel reopened
    # onto a new native table. Only the real visible nomination button is clicked.
    page.evaluate('window.__rtgNoAuto=true')
    for mode in ('fresh', 'reopened'):
        clear()
        page.evaluate('document.querySelector("body>.rt")?.remove();window.__inMeeting=false')
        page.wait_for_timeout(250)
        run('G.found=Object.keys(EP1INN.EV);G.debate={pi:EP1INN.MEET.phases.findIndex(p=>p.type==="vote"),sus:{}};G.beats.rtVotes={nabi:"seryeon",karo:"seryeon",doto:"seryeon",buri:"seryeon",geokkuri:"seryeon",wanggu:"innma"};window.__rtOpen(CASES[G.ci]);')
        page.wait_for_timeout(2500)
        if mode == 'reopened':
            page.evaluate('window.__m5OldNative=document.querySelector("body>.rt");window.__m5OldPanel=document.querySelector("#rtgvote");window.__T(\'document.querySelector("body>.rt").remove();window.__inMeeting=false;window.__rtOpen(CASES[G.ci]);\')')
            page.wait_for_timeout(2500)
            check('M5 genuinely reopens native table', page.evaluate('document.querySelector("body>.rt")!==window.__m5OldNative && !window.__m5OldNative.isConnected'), {})
        gates = page.evaluate('''()=>Array.from(document.querySelectorAll('.banner,.cutin,.stampfx')).map(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {className:e.className,text:e.textContent,opacity:s.opacity,visibility:s.visibility,display:s.display,rect:{x:r.x,y:r.y,width:r.width,height:r.height}}})''')
        print('M5 transition before pointer', mode, json.dumps(gates,ensure_ascii=False), flush=True)
        # The existing banner transition consumes its closing pointer. Wait for
        # the title to finish, dismiss it with a real tap, then make a new input.
        page.wait_for_function('!document.querySelector(".banner:not(.out),.cutin,.stampfx")', timeout=8000)
        if page.evaluate('!!document.querySelector(".banner.out:not(.skip):not([data-gone])")'):
            visible = page.evaluate('''()=>{const e=document.querySelector('.banner.out:not(.skip):not([data-gone])'),s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)>0.05&&r.width>0&&r.height>0}''')
            check('outgoing banner remains visibly present', visible, gates)
            page.mouse.click(20, 20)
            page.wait_for_timeout(650)
        page.locator('#rtgvote [data-pick="seryeon"]').click()
        page.wait_for_function('document.querySelector(".rt #rtnext .rt-bub p")?.textContent==="세련 씨를 지목합니다. 마지막 설명을 듣겠습니다."', timeout=6000)
        data = state()
        data['wanggu'] = run('G.beats.rtVotes.wanggu')
        check('M5 '+mode+' first nomination owns vote and cue', data['state']['who'] == 'wanggu' and data['state']['line'] == '세련 씨를 지목합니다. 마지막 설명을 듣겠습니다.' and data['wanggu'] == 'seryeon', data)
        page.locator('#rtgbar [data-g="next"]').click()
        page.wait_for_function('document.querySelector(".rt #rtnext .rt-bub p")?.textContent==="[지목] 세련 6표 · 마지막 설명을 듣고 결론"')
        data = state()
        check('M5 '+mode+' native six-vote narration', data['state']['line'] == '[지목] 세련 6표 · 마지막 설명을 듣고 결론' and run('Object.values(G.beats.rtVotes).filter(v=>v==="seryeon").length') == 6, data)
    page.evaluate('document.querySelector("body>.rt")?.remove();window.__inMeeting=false')
    page.wait_for_timeout(250)
    run('G.debate=null;')
    clear()
    run('G.found=Object.keys(EP1INN.EV);G.asked=["C03","C07","C12","C13"];window.__rtOpen(CASES[G.ci]);')
    page.wait_for_timeout(300)
    run('if(DL){DL.done=null;endDlg()};')
    page.evaluate('window.__auditOriginalPh=window.__rtPh')
    for name, selector, confession, hits in [
        ('F3', 'EP1INN.FINAL.phases.find(ph=>ph.type==="debate"&&ph.clock==="정오까지 20분")', False, 0),
        ('F4', 'EP1INN.FINAL.phases[EP1INN.FINAL.phases.length-1]', True, 1),
    ]:
        clear()
        page.evaluate('(selector)=>{let ph=window.__T(selector);if(!ph)throw Error("Missing production phase");window.__rtPh=()=>ph;window.__innAudioLine({w:"seryeon",t:"…네."});window.__innWant();window.__innWant()}', selector)
        data = state()
        check(name + ' production phase confession/one impact', data['state']['confession'] == confession and data['calls'].count('cut9') == hits, data)
    page.evaluate('window.__rtPh=window.__auditOriginalPh;document.querySelector("body>.rt")?.remove()')
    clear()

    def stats():
        return page.evaluate('__innRecordedSfx.stats()')

    for native, key in [('doorOpen','open'), ('door','close')]:
        before = stats()['starts'][key]
        run('SFX.' + native + '()')
        page.wait_for_function('(x)=>__innRecordedSfx.stats().starts[x.key]===x.before+1', arg={'key':key,'before':before})
        page.wait_for_function('(key)=>__innRecordedSfx.stats().live[key]===0', arg=key, timeout=8000)
        check('recorded ' + native + ' starts/ends', stats()['starts'][key] == before+1, stats())
    before = stats()['starts']['open']
    run('SFX.doorOpen();S.sound=false;')
    page.wait_for_timeout(400)
    check('pending door cancelled on mute', stats()['starts']['open'] == before, stats())
    run('S.sound=true;')

    def carriage():
        # Production P2->P1 changes scene identity and resets the native stop latch.
        run('G.beats.inn_pro=0;G.beats.inn_pi=EP1INN.PRO.findIndex(p=>p.sid==="P2");G.beats.inn_bg="carriage";__innWant();G.beats.inn_pi=EP1INN.PRO.findIndex(p=>p.sid==="P1");__innWant();')
        page.wait_for_function('__innRecordedSfx.stats().live.horse===1', timeout=8000)

    carriage()
    before = stats()['starts']['horse']
    run('SFX.carStop()')
    page.wait_for_function('__innRecordedSfx.stats().live.horse===0', timeout=4000)
    page.wait_for_timeout(400)
    check('native carriage stop no restart', stats()['starts']['horse'] == before and stats()['live']['horse'] == 0, stats())
    carriage()
    before = stats()['starts']['horse']
    run('S.sound=false;')
    page.wait_for_function('__innRecordedSfx.stats().live.horse===0', timeout=4000)
    page.wait_for_timeout(400)
    check('carriage mute cancels loop', stats()['starts']['horse'] == before and stats()['live']['horse'] == 0, stats())
    check('recorded decode and page errors', stats()['errors'] == 0 and not errors, {'recorded':stats(),'pageErrors':errors})
    print('PASS prepared production-cue regression; no full-playthrough or listening claim.', flush=True)
    browser.close()
