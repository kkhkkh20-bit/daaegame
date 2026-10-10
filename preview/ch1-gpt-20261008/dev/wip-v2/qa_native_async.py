"""Prepared-state regression for native verdict promises, not a fresh walkthrough.

Evidence is prepared and native DOM handlers are invoked deliberately. Banner
animations finish immediately; flash promises remain pending until this test
releases them, making retry and case-change races deterministic.
"""
import argparse
import shutil
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:8000/playT.html')
args = parser.parse_args()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 844, 'height': 390})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(args.url, wait_until='domcontentloaded')
    page.wait_for_timeout(16000)

    def state(code):
        return page.evaluate('(code)=>window.__T(code)', code)

    def line():
        return page.locator('body>.rt .rt-bub p').inner_text()

    def test(name, callback):
        try:
            callback()
        except Exception:
            print('FAIL:', name, flush=True)
            raise
        print('PASS:', name, flush=True)

    state('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
    page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()')
    page.wait_for_timeout(1000)
    state('if(DL){DL.done=null;endDlg()};G.found=Object.keys(EP1INN.EV).filter(id=>!["C03","C07","C12","C13"].includes(id));G.asked=["C03","C07","C12","C13"];G.exam={};allSpots(CASES[G.ci]).forEach(s=>G.exam[s.ev.id]=true);window.__qaInn=G;window.__savedFlash=flash;window.__savedBanner=banner;window.__qaPending=[];flash=function(){return new Promise(resolve=>window.__qaPending.push(resolve))};banner=function(){return Promise.resolve()};')

    def open_vote():
        state('if(DL){DL.done=null;endDlg()};G=window.__qaInn;G.hp=5;G.wrong=0;window.__rtgReset();G.debate={pi:EP1INN.MEET.phases.findIndex(p=>p.type==="vote"),sus:{}};window.__inMeeting=false;document.querySelectorAll("body>.rt").forEach(e=>e.remove());window.__rtOpen(CASES[G.ci]);')
        page.wait_for_timeout(300)
        assert page.evaluate('window.__rtPh().type') == 'vote'
        assert page.evaluate('window.__qaPending.length') == 0

    def click_vote(person):
        page.evaluate('(person)=>document.querySelector(".vc[data-seat="+person+"]").click()', person)

    def release():
        page.evaluate('window.__qaPending.shift()()')
        page.wait_for_timeout(150)

    def wrong_retry():
        open_vote()
        click_vote('innma')
        click_vote('innma')
        assert state('G.hp') == 4 and state('G.wrong') == 1, 'Repeated wrong vote caused duplicate damage'
        assert page.evaluate('window.__qaPending.length') == 1
        state('window.__rtgReset();G.debate={pi:1,sus:{}};window.__inMeeting=false;document.querySelector("body>.rt").remove();window.__rtOpen(CASES[G.ci]);')
        page.wait_for_timeout(150)
        before = line()
        assert '열세 번째 침대' in before
        release()
        assert line() == before, 'Old wrong verdict overwrote the retried meeting'
        assert state('G.debate.pi') == 1
        assert not page.locator('body>.rt #rtnext').count()

    def successful_vote_case_change():
        open_vote()
        click_vote('seryeon')
        click_vote('seryeon')
        assert page.evaluate('window.__qaPending.length') == 1, 'Repeated correct vote created another verdict'
        state('window.__rtgReset();G=fresh(0);S.screen="case";window.__inMeeting=false;window.__rtOpen(CASES[0],{key:"qaOther",title:"NEW ROUND",seats:[],phases:[{type:"talk",lines:[{w:"det0",t:"NEW ROUND LINE"}]}]});')
        page.wait_for_timeout(150)
        assert line() == 'NEW ROUND LINE'
        release()
        assert line() == 'NEW ROUND LINE', 'Old inn vote overwrote a different case'
        assert state('G.qaOther.pi') == 0

    def current_wrong_verdict():
        open_vote()
        click_vote('innma')
        release()
        assert '증거가 부족해' in line(), 'A current verdict was incorrectly discarded'
        assert state('G.hp') == 4 and state('G.wrong') == 1
        page.evaluate('document.querySelector("#rtnext").click()')
        page.wait_for_timeout(100)
        assert page.evaluate('window.__rtPh().type') == 'vote'

    def current_correct_verdict():
        open_vote()
        click_vote('seryeon')
        release()
        assert '세련 씨를 지목합니다' in line(), 'A current correct vote was incorrectly discarded'
        assert state('G.hp') == 5 and state('G.wrong') == 0

    try:
        test('wrong vote: single damage and stale callback rejected after retry', wrong_retry)
        test('correct vote: duplicate blocked and stale callback rejected after case change', successful_vote_case_change)
        test('current wrong verdict still displays and resumes voting', current_wrong_verdict)
        test('current correct verdict still displays authored dialogue', current_correct_verdict)
        assert not errors, errors
    finally:
        state('flash=window.__savedFlash;banner=window.__savedBanner;')
        browser.close()
