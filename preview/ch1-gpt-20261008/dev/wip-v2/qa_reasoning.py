"""Prepared-evidence deduction UI/engine regression; not a fresh-game walkthrough.

Expected answers are independently authored here, never read from the UI's DB.
Physical evidence and testimony are deliberately stored in separate inventories.
"""
import argparse
import shutil
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:8000/playT.html')
args = parser.parse_args()
ANSWERS = {
    'linen': [('C03', 'C02')],
    'time': [('C07', 'C06'), ('C08', 'C13')],
    'location': [('C10', 'C04')],
    'contact': [('C01', 'C05')],
    'seal': [('C12', 'C10')],
}

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    for viewport in [{'width': 844, 'height': 390}, {'width': 390, 'height': 844}]:
        page = browser.new_page(viewport=viewport)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(args.url, wait_until='domcontentloaded')
        page.wait_for_timeout(16000)
        page.evaluate('''()=>{window.__logicInputStops=[];for(const name of ['stopPropagation','stopImmediatePropagation']){const old=Event.prototype[name];Event.prototype[name]=function(){if(this.target?.closest?.('#logic-panel'))window.__logicInputStops.push({type:this.type,method:name,stack:new Error().stack});return old.call(this)}}}''')

        def state(code):
            return page.evaluate('(code)=>window.__T(code)', code)

        def button(selector):
            before = page.evaluate('({fx:window.__fxEaten||0,guard:window.__innGuarded||0,dl:window.__T("!!DL")})')
            page.locator('#logic-panel ' + selector).click()
            after = page.evaluate('({fx:window.__fxEaten||0,guard:window.__innGuarded||0,dl:window.__T("!!DL")})')
            if before != after:
                print('Input diagnostic', selector, before, after, flush=True)

        def choose(pair, option=0):
            for card in pair:
                button('[data-card="' + card + '"]')
            button('[data-option="' + str(option) + '"]')
            selected = page.locator('#logic-panel [data-card][aria-pressed="true"]').evaluate_all('(els)=>els.map(e=>e.dataset.card)')
            assert set(selected) == set(pair), (pair, selected, page.evaluate('window.__logicInputStops.slice(-12)'), page.locator('#logic-panel').inner_text())
            assert page.locator('#logic-panel [data-option="' + str(option) + '"]').get_attribute('aria-pressed') == 'true'

        def solve(question):
            for pair in ANSWERS[question]:
                choose(pair)
                page.wait_for_timeout(600)
                button('[data-act="submit"]')
            assert page.locator('#logic-panel .lp-summary').count() == 1

        state('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1,inn_snowWitness:1,inn_locationClaim:1};')
        page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()')
        page.wait_for_timeout(1000)
        state('if(DL){DL.done=null;endDlg()};G.found=Object.keys(EP1INN.EV).filter(id=>!["C03","C07","C12","C13"].includes(id));G.asked=["C03","C07","C12","C13"];G.exam={};allSpots(CASES[G.ci]).forEach(s=>G.exam[s.ev.id]=true);G.hp=5;G.wrong=0;')
        page.evaluate('window.__proofDone=0;window.__logicOpen("linen",{mode:"meet",done:()=>window.__proofDone++})')
        # Duplicate cards cannot occupy both evidence slots.
        button('[data-card="C02"]'); button('[data-card="C02"]')
        button('[data-option="0"]')
        assert page.locator('#logic-panel [data-act="submit"]').is_disabled()
        choose(('C01', 'C02'))
        button('[data-act="submit"]')
        assert state('G.hp') == 4 and state('G.wrong') == 1
        assert page.locator('#logic-panel .lp-feedback.error').count() == 1
        assert page.evaluate('window.__proofDone') == 0
        button('[data-slot="0"]'); button('[data-slot="0"]')
        choose(ANSWERS['linen'][0], 1)
        page.wait_for_timeout(600); button('[data-act="submit"]')
        assert state('G.hp') == 3 and state('G.wrong') == 2
        button('[data-option="0"]')
        page.wait_for_timeout(600); button('[data-act="submit"]')
        assert page.evaluate('window.__proofDone') == 0, 'Success must wait for explicit presentation'
        button('[data-act="finish"]')
        assert page.evaluate('window.__proofDone') == 1
        assert not page.evaluate('window.__logicBusy()')
        assert state('G.hp') == 3 and state('G.wrong') == 2

        for question in ANSWERS:
            print('Checking', viewport, question, flush=True)
            state('if(DL){DL.done=null;endDlg()}')
            opened = page.evaluate('(id)=>window.__logicOpen(id,{mode:"notebook",done:()=>window.__proofDone++})', question)
            assert opened, ('Notebook refused to open', question, state('!!DL'))
            solve(question)
            before = page.evaluate('window.__proofDone')
            button('[data-act="finish"]')
            assert page.evaluate('window.__proofDone') == before + 1
        assert set(state('G.reason.solved')) == set(ANSWERS)
        clean = state('sanitizeState({v:3,prog:{inn:Object.assign(fresh(G.ci),{introDone:true,reason:{version:1,solved:["linen","linen","bogus","time","seal"],drafts:{cheat:true}}})}}).prog.inn.reason')
        assert clean == {'version': 1, 'solved': ['linen', 'time', 'seal']}, clean
        assert state('sanitizeState({v:3,prog:{inn:Object.assign(fresh(G.ci),{introDone:true,reason:{version:999,solved:["linen"]}})}}).prog.inn.reason||null') is None

        # A saved solved record cannot bypass the official meeting claim.
        state('G.reason={version:1,solved:["linen"]};G.hp=5;G.wrong=0;G.debate={pi:1,sus:{}};window.__rtgReset();window.__rtOpen(CASES[G.ci])')
        page.wait_for_timeout(2200)
        for _ in range(25):
            if page.locator('.rt-bub.stm').count(): break
            page.evaluate('document.querySelector("#rtnext")?.click();document.querySelector("#rtgq")?.click()')
            page.wait_for_timeout(200)
        page.evaluate('document.querySelector("#rtnx").click()')
        page.wait_for_timeout(250)
        assert page.evaluate('window.__rtPh().stms[1].reason') == 'linen'
        page.evaluate('document.querySelector("#rtgbar [data-g=ev]").click()')
        page.wait_for_timeout(200)
        page.evaluate('document.querySelector(".rt [data-bl=C01]").click()')
        page.wait_for_timeout(200)
        page.evaluate('document.querySelector("#rtgbar [data-g=present]").click()')
        page.wait_for_timeout(200)
        assert page.locator('#logic-panel').count() == 1, 'Recorded answer bypassed claim gate'
        assert state('G.hp') == 5 and state('G.wrong') == 0, 'Legacy wrong verdict ran before proof UI'
        assert state('G.debate.pi') == 1
        solve('linen')
        assert state('G.debate.pi') == 1
        button('[data-act="finish"]')
        page.wait_for_timeout(1600)
        assert not page.locator('#logic-panel').count()
        assert page.locator('#rtnext').count() or page.locator('#rtgq').count(), 'Native correct response did not run'
        assert state('G.hp') == 5 and state('G.wrong') == 0

        # Cancelled proof callbacks are stale even if the same claim is reopened.
        page.evaluate('()=>{window.__logicReset();window.__savedOpen=window.__logicOpen;window.__logicOpen=(id,opt)=>{window.__staleDone=opt.done;return window.__savedOpen(id,opt)}}')
        state('window.__rtgReset();G.debate={pi:1,sus:{}};document.querySelector("body>.rt")?.remove();window.__inMeeting=false;window.__rtOpen(CASES[G.ci])')
        page.wait_for_timeout(2200)
        page.evaluate('document.querySelector("#rtnx").click()')
        page.wait_for_timeout(200)
        page.evaluate('document.querySelector("#rtgbar [data-g=ev]").click()')
        page.wait_for_timeout(200)
        page.evaluate('document.querySelector(".rt [data-bl=C01]").click()')
        page.wait_for_timeout(200)
        page.evaluate('document.querySelector("#rtgbar [data-g=present]").click()')
        page.wait_for_timeout(200)
        assert page.locator('#logic-panel').count() == 1
        page.evaluate('()=>{window.__rtgReset();window.__staleDone();window.__logicOpen=window.__savedOpen}')
        assert not page.evaluate('window.__logicBusy()')
        assert state('G.debate.pi') == 1
        assert page.evaluate('window.__rtgStep(window.__rtPh().stms[1])') == 0
        assert not errors, errors
        print(viewport, 'OK: five independently answered puzzles, two-stage time, wrong pair/conclusion, exact damage, explicit finish, save sanitizer, mandatory native claim, stale callback', flush=True)
        page.close()
    browser.close()
