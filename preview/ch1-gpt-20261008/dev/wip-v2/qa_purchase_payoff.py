"""Native payoff regression using explicitly prepared states.

This verifies evidence ownership/order, a legacy final-save recovery and the
authored ending interfaces. It does not claim a fresh walkthrough or prove
that players will buy chapter 2; qa_flow --resume covers the actual clue route.
No production dialogue/phase is rewritten by this test.
"""
import argparse
import json
import shutil
from playwright.sync_api import sync_playwright
from qa_scene_guidance import Investigation


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:8000/playT.html')
parser.add_argument('--only-final', action='store_true')
parser.add_argument('--only-ending', action='store_true')
parser.add_argument('--only-legacy', action='store_true', help='Only check old final-save recovery through actual witness UI')
args = parser.parse_args()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=shutil.which('chromium'),
                                       args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 844, 'height': 390})
    page = context.new_page()
    errors, bad = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: bad.append(response.url)
            if response.status >= 400 and 'favicon' not in response.url else None)
    page.goto(args.url, wait_until='domcontentloaded')
    page.wait_for_timeout(16000)

    def engine(code):
        return page.evaluate('(code)=>window.__T(code)', code)

    def prepare(with_record=True):
        engine('if(DL){DL.done=null;endDlg()};'
               'window.__rtgReset();document.querySelectorAll("body>.rt").forEach(e=>e.remove());'
               'window.__inMeeting=false;S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));'
               'S.prog.inn.introDone=true;'
               'S.prog.inn.beats={inn_pro:1,inn_i9:1,inn_life_confirmed:1,inn_meeting_version:2};')
        page.evaluate('document.querySelector("#innmain")?.remove();window.__w209boot()')
        page.wait_for_timeout(500)
        engine('if(DL){DL.done=null;endDlg()};G.beats.inn_meet=1;'
               'G.found=Object.keys(EP1INN.EV).filter(id=>!'+json.dumps([] if with_record else ['C14'])+'.includes(id));'
               'G.asked=[];G.exam={};allSpots(CASES[G.ci]).forEach(s=>G.exam[s.ev.id]=true);'
               'G.unlocked=CASES[G.ci].locations.map(l=>l.req).filter(Boolean);'
               'G.beats.rtVotes={nabi:"seryeon",buri:"seryeon",doto:"seryeon",geokkuri:"seryeon",karo:"seryeon",wanggu:"seryeon"};'
               'G.beats.rtTally={seryeon:6};G.tab="scene";render();')
        page.wait_for_timeout(400)

    def record_lines():
        page.evaluate('''()=>{
          clearInterval(window.__payoffSample);
          window.__payoffLines=[];
          window.__payoffSample=setInterval(()=>{
            const line=window.__innAudioState().line;
            if(line&&window.__payoffLines.at(-1)?.line!==line)
              window.__payoffLines.push({line,votes:window.__T('JSON.parse(JSON.stringify(G.beats.rtVotes||{}))'),
                beats:window.__T('Object.assign({},G.beats)')});
          },30);
        }''')

    def queue_tick():
        return page.evaluate('''()=>{
          const q=s=>document.querySelector(s), click=s=>{const e=q(s);if(e&&!e.disabled){e.click();return true}return false};
          if(q('#rtgq')){click('#rtgq');return true}
          if(window.__T('!!DL')){window.__T('advance()');return true}
          if(q('#rtnext')){click('#rtnext');return true}
          return false;
        }''')

    def drain(limit=220):
        quiet = 0
        for _ in range(limit):
            if engine('!!(G.innfinal&&G.innfinal.done)&&!!G.beats.inn_final'):
                return
            if queue_tick():
                quiet = 0
            elif page.locator('.flash,.banner').count():
                # Final acceptance waits for the real hush/objection promise;
                # lack of a dialogue bubble during that animation is not idle.
                quiet = 0
            else:
                quiet += 1
                if quiet >= 6:
                    return
            page.wait_for_timeout(150)
        raise AssertionError(('Native dialogue did not finish', engine('G.innfinal'),
                              page.locator('body').inner_text()[-500:]))

    def present(evidence):
        page.evaluate('''(id)=>{
          if(!document.body.classList.contains('rtg-drw'))document.querySelector('#rtgbar [data-g="ev"]').click();
          document.querySelector('.rt [data-bl="'+id+'"]').click();
          const examine=document.querySelector('#rtexam');if(examine)examine.click();
        }''', evidence)
        # The native toolbar syncs after the drawer selection. Clicking its
        # disabled HTML button in the same JS tick silently discards the tap.
        page.wait_for_function('()=>{const b=document.querySelector("#rtgbar [data-g=present]");return b&&!b.disabled}')
        page.locator('#rtgbar [data-g="present"]').click()
        page.wait_for_timeout(650)
        drain()

    def final_snapshot():
        return engine('({phase:G.innfinal.pi,step:window.__rtgStep(EP1INN.FINAL.phases[3].stms[0]),'
                      'votes:G.beats.rtVotes,tally:G.beats.rtTally,final:G.beats.inn_final||0,'
                      'cleared:G.beats.inn_case_cleared||0,child:G.beats.inn_child_heard||0})')

    def npc(npc_id, investigation):
        if page.locator('#closeNotice:visible').count():
            investigation.click('#closeNotice')
        elif page.locator('#closeNotice').count():
            page.wait_for_function('!document.getElementById("closeNotice")', timeout=12000)
        page.wait_for_function('(id)=>{const im=document.querySelector("#bigscene svg image.wn9[data-k="+id+"]");return im&&window.__innMask()[im.getAttribute("href")]==="ok"}', arg=npc_id)
        point = None
        for direction in [None, '#fsar', '#fsar', '#fsal']:
            if direction and page.locator(direction+':visible').count():
                investigation.click(direction)
                page.wait_for_timeout(550)
            point = page.evaluate('''(id)=>{
              const r=document.querySelector('#bigscene').getBoundingClientRect();
              for(let y=Math.max(12,r.top+12);y<Math.min(innerHeight-12,r.bottom-12);y+=6)
                for(let x=Math.max(12,r.left+12);x<Math.min(innerWidth-12,r.right-12);x+=6)
                  if(document.elementFromPoint(x,y)?.closest('#bigscene')&&
                    [[0,0],[-6,0],[6,0],[0,-6],[0,6]].every(([dx,dy])=>window.__innNpcHit(x+dx,y+dy)===id))return {x,y};
              return null;
            }''', npc_id)
            if point:
                break
        assert point, ('NPC has no reachable opaque pixels', npc_id)
        page.mouse.click(point['x'], point['y'])
        page.wait_for_timeout(400)
        investigation.drain()
        assert investigation.state()['tab'] == 'talk'

    if not args.only_ending:
        if not args.only_legacy:
            prepare()
            record_lines()
            engine('G.innfinal={pi:3,sus:{}};window.__innOpenFinal()')
            page.wait_for_timeout(2000)
            drain()
            assert page.evaluate('__rtPh()===EP1INN.FINAL.phases[3]'), 'Final resume reset the proof to F1'
            initial = final_snapshot()
            assert initial['step'] == 0
            present('C14')
            assert final_snapshot() == initial, 'Premature witness record advanced proof or awarded outcome metadata'
            present('C09')
            assert final_snapshot() == initial, 'Wrong clue advanced proof or awarded outcome metadata'
            present('C10')
            assert final_snapshot()['step'] == 1 and final_snapshot()['phase'] == 3
            present('C14')
            assert final_snapshot()['step'] == 1 and final_snapshot()['phase'] == 3, 'Record skipped the seal-owner proof'
            present('C12')
            assert final_snapshot()['step'] == 2 and final_snapshot()['phase'] == 3
            before = page.evaluate('__payoffLines')
            assert not any('노름판에서 잃었습니다' in row['line'] for row in before), 'Confession occurred before direct witness-record presentation'
            present('C14')
            lines = page.evaluate('__payoffLines')
            if not any('노름판에서 잃었습니다' in row['line'] for row in lines):
                print('F3 diagnostic', final_snapshot(), page.locator('body').inner_text()[-1800:],
                      [row['line'] for row in lines], flush=True)
            assert any('노름판에서 잃었습니다' in row['line'] for row in lines), 'Direct record did not earn the authored confession'
            assert any('배상 요구는 거두겠습니다' in row['line'] for row in lines), 'Victory did not withdraw the unfair payment demand'
            assert all(value == 'seryeon' for value in engine('G.beats.rtVotes').values())
            assert engine('!!G.beats.inn_case_cleared&&!!G.beats.inn_child_heard'), 'Victory failed to clear the family or accept the child witness'
            print('PASS native F3: premature/wrong clues preserve proof and outcomes; C10 → C12 → direct C14 earns confession and withdrawal', flush=True)

        # A released old save may already be at phase 3 with an old T_ka2
        # question but no newly introduced witness card. It must return to a
        # real witness encounter and never synthesize evidence on load.
        prepare(False)
        engine('G.asked.push("T_ka2");G.beats.inn_karo_gamble=1;'
               'G.hp=3;G.battle={cul:"seryeon",phase:"fight",round:3,si:0,miss:0,lives:3,max:5};G.innfinal={pi:3,sus:{}};'
               'window.__innOpenFinal()')
        page.wait_for_timeout(2000)
        drain()
        assert engine('!!G.innfinal.hold&&G.innfinal.hold.need.includes("C14")'), 'Legacy final save has no missing-witness recovery'
        assert not engine('G.found.includes("C14")||G.asked.includes("C14")'), 'Legacy migration auto-awarded witness record'
        assert not page.locator('body>.rt').count(), 'Missing record left an unwinnable final overlay'
        assert engine('G.hp') == 3, 'Opening the paused final replenished its remaining health'
        engine('saveProg();persist()')
        page.reload(wait_until='domcontentloaded')
        page.wait_for_timeout(16000)
        page.locator('#innmain [data-m="cont"]').click()
        page.wait_for_timeout(2000)
        drain()
        if not engine('!!G.innfinal&&G.innfinal.pi===3&&!!G.innfinal.hold'):
            print('Legacy Continue diagnostic', engine('({g:G.innfinal,slot:S.prog.inn&&S.prog.inn.innfinal,hp:G.hp,battle:G.battle,beat:G.beats.inn_final})'), flush=True)
        assert engine('G.innfinal.pi===3&&!!G.innfinal.hold'), 'Saved recovery lost its final proof location'
        assert engine('G.hp') == 3, 'Continue replenished the paused final health'
        assert not engine('G.found.includes("C14")||G.asked.includes("C14")')
        actual = Investigation(page)
        actual.drain()
        actual.move('plaza')
        npc('karo', actual)
        if not engine('G.asked.includes("T_ka2")') and page.locator('[data-ask="T_ka2"]:visible').count():
            actual.click('[data-ask="T_ka2"]')
        else:
            # Asked topics are intentionally removed. The native C09 showing
            # path recovers an old record without rewriting asked on load.
            page.locator('#showev').click()
            page.wait_for_timeout(800)
            page.locator('[data-show="C09"]').click()
            try:
                page.wait_for_function("(code)=>window.__T('!!DL')||document.querySelector('#innins')||window.__T(code)",arg='G.found.includes("C14")',timeout=10000)
            except Exception:
                page.screenshot(path='/tmp/purchase-legacy-show-diagnostic.png')
                print('Legacy SHOW input diagnostic',actual.state(),page.locator('body').inner_text()[-1400:],page.evaluate('({guard:window.__innGuarded,swallowed:window.__swallowed,g:window.__g199,show:window.__evShow,modal:document.querySelector("#ov .modal")?.outerHTML.slice(0,500)})'),flush=True)
                raise
        actual.drain()
        if not engine('G.found.includes("C14")||G.asked.includes("C14")'):
            page.screenshot(path='/tmp/purchase-legacy-show-diagnostic.png')
            print('Legacy SHOW diagnostic',actual.state(),actual.spoken[-15:],page.locator('body').inner_text()[-1400:],flush=True)
        assert engine('G.found.includes("C14")||G.asked.includes("C14")'), 'Native old-witness encounter did not recover the new record'
        actual.click('#w209rail .g>[data-w="scene"]')
        actual.drain()
        actual.click('#w209rail .g>[data-w="ev"]')
        assert page.locator('#inn-final-record-resume').is_enabled(), 'Collected record left the native resume button disabled'
        actual.click('#inn-final-record-resume')
        page.wait_for_timeout(2000)
        drain()
        assert page.evaluate('__rtPh()===EP1INN.FINAL.phases[3]'), 'Real witness investigation failed to resume F3'
        assert not engine('G.innfinal.hold')
        assert engine('G.hp') == 3, 'Native evidence-record resume replenished final health'
        print('PASS legacy phase-3 final save: no auto C14, reload retains recovery, real plaza/Karo encounter restores same proof', flush=True)

    if not args.only_final and not args.only_legacy:
        # Use the native epilogue controller from E4 through E5 and the teaser.
        # Scenes are prepared; the comparison and ending controls are real.
        prepare()
        record_lines()
        engine('G.beats.inn_final=1;window.__innRunEnd(3)')
        compared = False
        for _ in range(300):
            if page.locator('#inn-mother-lead').count():
                assert not engine('G.beats.inn_mother_lead'), 'Handwriting comparison was credited before looking'
                assert page.evaluate('__innMotherLeadState().visible')
                page.locator('#inn-mother-lead [data-mother-action="compare"]').click()
                page.wait_for_timeout(500)
                assert engine('!!G.beats.inn_mother_lead')
                assert page.evaluate('__innMotherLeadState().compared')
                page.screenshot(path='/tmp/purchase-mother-comparison.png')
                page.locator('#inn-mother-lead [data-mother-action="record"]').click()
                compared = True
            if page.locator('#inn-ch2-peek').count():
                break
            queue_tick()
            page.wait_for_timeout(180)
        assert compared, 'E4 never offered the direct handwriting comparison'
        page.locator('#inn-ch2-peek').wait_for(state='visible')
        assert engine('!!G.beats.inn_end'), 'Teaser blocked chapter-1 completion save'
        for _ in range(4):
            page.keyboard.press('Enter')
        assert not engine('G.beats.inn_ch2_peek_seen'), 'Teaser was skipped before its reveal'
        page.wait_for_function('__innChapter2PeekState().stage==="missing"')
        page.wait_for_timeout(200)
        page.screenshot(path='/tmp/purchase-chapter2-missing.png')
        page.wait_for_function('__innChapter2PeekState().ready')
        page.wait_for_timeout(350)
        assert page.locator('#inn-ch2-peek .peek-stolen').evaluate('e=>+getComputedStyle(e).opacity') == 0, 'Missing-item reveal never removed the item'
        page.screenshot(path='/tmp/purchase-chapter2-preview.png')
        page.locator('#inn-ch2-peek .peek-finish').click()
        page.wait_for_timeout(350)
        assert not page.locator('#inn-ch2-peek').count()
        assert engine('!!G.beats.inn_ch2_peek_seen')
        assert page.locator('#inn-ch2-replay').is_visible()
        engine('saveProg();persist()')
        page.reload(wait_until='domcontentloaded')
        page.wait_for_timeout(16000)
        page.locator('#innmain [data-m="cont"]').click()
        page.wait_for_timeout(1500)
        assert engine('!!G.beats.inn_end&&!!G.beats.inn_mother_lead&&!!G.beats.inn_ch2_peek_seen')
        assert not page.locator('#inn-ch2-peek').count(), 'Completed-save Continue forced another teaser'
        page.locator('#inn-ch2-replay').click()
        page.wait_for_function('__innChapter2PeekState().ready')
        page.keyboard.press('Escape')
        page.wait_for_timeout(250)
        assert not page.locator('#inn-ch2-peek').count(), 'Native replay could not finish'
        print('PASS E4/E5: actual compare/record, native teaser reveal/early-input guard, completed save Continue/replay', flush=True)

    assert not errors, errors
    assert not bad, bad
    print('RESULT prepared payoff QA passed; JS and HTTP errors 0', flush=True)
    browser.close()
