"""Focused real-input QA for the date lock and optional ink study.

The prepared investigation fixture has finished the introduction and collected
C01/C02/C04/C05 plus Nabi's statement. No puzzle solution, permission, headboard
observation, C11 or comparison is seeded. This is not a fresh-game walkthrough.
"""
import argparse
import shutil
from playwright.sync_api import sync_playwright


def run(browser, url, size, only_ink=False):
    context = browser.new_context(viewport={'width': size[0], 'height': size[1]})
    page = context.new_page()
    errors, bad = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: bad.append(response.url)
            if response.status >= 400 and 'favicon' not in response.url else None)

    def engine(code):
        return page.evaluate('(code)=>window.__T(code)', code)

    def state():
        return engine('({found:G.found.slice(),asked:G.asked.slice(),'
                      'obs:(G.obsSeen||[]).slice(),beats:G.beats,hp:G.hp,'
                      'wrong:G.wrong||0,dl:!!DL})')

    def drain():
        quiet = 0
        for _ in range(160):
            if state()['dl']:
                page.keyboard.press('Enter')
                quiet = 0
            elif page.locator('#innpad').count():
                return
            elif page.locator('#okfind').count():
                page.locator('#okfind').click()
                quiet = 0
            elif page.locator('#tostay2').count():
                page.wait_for_timeout(750)
                page.locator('#tostay2').click()
                quiet = 0
            else:
                quiet += 1
                if quiet >= 6:
                    return
            page.wait_for_timeout(230)
        raise AssertionError(('Dialogue did not settle', state()))

    def click(selector):
        page.wait_for_timeout(800)
        try:
            page.locator(selector).first.click(timeout=9000)
        except Exception:
            page.screenshot(path=f'/tmp/puzzle-failure-{size[0]}x{size[1]}.png')
            print('Click failed', selector, state(), errors, flush=True)
            raise
        page.wait_for_timeout(300)

    def bounds():
        modal = page.locator('.inn-room-puzzle')
        for target in [modal] + list(modal.locator('button').all()):
            rect = target.bounding_box()
            assert rect and rect['x'] >= 0 and rect['y'] >= 0, rect
            assert rect['x'] + rect['width'] <= size[0] + 1, rect
            assert rect['y'] + rect['height'] <= size[1] + 1, rect
            if target.evaluate('e=>e.tagName') == 'BUTTON':
                assert rect['width'] >= 44 and rect['height'] >= 44, ('Small touch target', rect)
        assert not modal.evaluate('e=>e.scrollHeight>e.clientHeight+1'), (
            'Puzzle needs scrolling', size)

    page.goto(url, wait_until='domcontentloaded')
    page.wait_for_timeout(16000)
    engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));'
           'S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_sunnote:1};'
           'S.prog.inn.found=["C01","C02","C04","C05"];'
           'S.prog.inn.asked=["C03"];S.prog.inn.obsSeen=["o_under"];')
    page.evaluate('()=>{document.querySelector("#innmain").remove();window.__w209boot()}')
    page.wait_for_timeout(1600)
    drain()
    print('Prepared investigation', size, flush=True)
    if only_ink:
        engine('G.beats.inn_lock=1;G.beats.inn_ledger_permission=1;render();')
        page.wait_for_timeout(1000)
        drain()
    else:
        initial = state()
        assert not initial['beats'].get('inn_lock')
        assert 'C11' not in initial['found']
        assert 'o_inn_head2' not in initial['obs']

        # Genuine pointer starts consent before the pad. No date is automatically
        # exposed for players who have not observed the headboard.
        click('#bigscene [data-obs="o_inn_lock"]')
        assert not page.locator('#innpad').count(), 'Pad appeared before consent'
        spoken = []
        for _ in range(130):
            line = engine('DL&&DL.lines[DL.i]&&String(DL.lines[DL.i][7]||DL.lines[DL.i][1])')
            if line:
                spoken.append(line)
            if page.locator('#innpad').count():
                break
            page.keyboard.press('Enter')
            page.wait_for_timeout(230)
        assert any('첫째 권만 봐요' in s for s in spoken), spoken
        assert state()['beats'].get('inn_ledger_permission'), state()
        page.wait_for_timeout(900)
        assert page.locator('.inn-room-puzzle').count(), ('Permission finished without a pad', state(), engine('({freeze:!!window.__dlFreeze,cut:!!window.__innCutting,blocked:!!document.querySelector("body>.rt,#innmove,#wmap,.banner,.placecard")})'))
        print('Consent and pad', size, flush=True)
        bounds()
        assert '열한' not in page.locator('.rp-clue').inner_text()
        assert '둘째 날' not in page.locator('.rp-clue').inner_text()
        click('#innhint')
        assert '머리판' in page.locator('#innmsg').inner_text()
        assert '1102' not in page.locator('.inn-room-puzzle').inner_text()
        click('#innopen')
        assert not state()['beats'].get('inn_lock')
        assert state()['hp'] == initial['hp'] and state()['wrong'] == initial['wrong']
        page.screenshot(path=f'/tmp/puzzle-before-date-{size[0]}x{size[1]}.png')
        page.keyboard.press('Escape')
        assert not page.locator('.inn-room-puzzle').count()

        click('#bigscene [data-obs="o_inn_head2"]')
        drain()
        assert 'o_inn_head2' in state()['obs'], state()
        print('Headboard observed', size, flush=True)
        click('#bigscene [data-obs="o_inn_lock"]')
        page.wait_for_timeout(900)
        assert '열한 번째 달 둘째 날' in page.locator('.rp-clue').inner_text()
        click('#innhint')
        click('#innhint')
        assert '1102' not in page.locator('#innmsg').inner_text()
        assert '일, 일' not in page.locator('#innmsg').inner_text()

        # Four fresh keyboard digits, real mouse controls and an incorrect attempt.
        page.locator('#innpad [data-d="0"]').focus()
        page.keyboard.type('1109', delay=80)
        click('#innopen')
        assert not state()['beats'].get('inn_lock')
        assert state()['hp'] == initial['hp'] and state()['wrong'] == initial['wrong']
        click('[data-digit="3"][data-step="-1"]')
        assert page.locator('[data-d="3"]').inner_text() == '8'
        # A held key produces one update; repeated keydown does not spill into
        # another digit or a newly opened action.
        page.locator('[data-d="3"]').focus()
        page.keyboard.down('3')
        page.keyboard.down('3')
        page.keyboard.up('3')
        assert page.locator('[data-d="3"]').inner_text() == '3'
        page.locator('[data-d="0"]').focus()
        page.keyboard.type('1203', delay=80)
        assert [page.locator(f'[data-d="{i}"]').inner_text() for i in range(4)] == list('1203')
        page.screenshot(path=f'/tmp/puzzle-date-{size[0]}x{size[1]}.png')
        bounds()
        page.keyboard.press('Escape')

        # Draft and permission survive the real save path and a browser reload.
        page.reload(wait_until='domcontentloaded')
        page.wait_for_timeout(16000)
        click('#innmain [data-m="cont"]')
        drain()
        click('#bigscene [data-obs="o_inn_lock"]')
        page.wait_for_timeout(900)
        assert [page.locator(f'[data-d="{i}"]').inner_text() for i in range(4)] == list('1203'), state()
        assert state()['beats'].get('inn_ledger_permission')
        print('Draft reloaded', size, flush=True)
        # Keyboard navigation remains inside the dialog.
        page.locator('#innclose').focus()
        page.keyboard.press('Tab')
        assert page.evaluate('document.activeElement.id') == 'innopen'
        page.keyboard.press('Shift+Tab')
        assert page.evaluate('document.activeElement.id') == 'innclose'
        page.locator('[data-d="0"]').focus()
        page.keyboard.type('1102', delay=80)
        page.keyboard.press('Enter')
        drain()
        assert state()['beats'].get('inn_lock'), state()
        assert 'C11' not in state()['found'], 'Opening a box automatically granted the ledger'
        assert page.locator('#bigscene image[data-world-prop="chest_open_with_C11"]').count() == 1
        assert not page.locator('#bigscene [data-obs="o_inn_lock"]').count()
        print('Native box opened', size, flush=True)

    # Optional comparison is entered from native records after the two items
    # were collected. It uses the original images and never grants evidence.
    click('#w209rail .g>[data-w="ev"]')
    click('.crec2 [data-crs="C05"]')
    # Each native action must keep its own hit area. The old all:unset rule
    # made its enlarged ::after cover the whole record detail and intercept
    # the neighbouring comparison button.
    for action, title in (('d', '자세히 보기'), ('m', '다람 메모')):
        selector = f'.crec2 .orig9 .e9opt [data-o="{action}"]'
        assert page.locator(selector).evaluate('e=>getComputedStyle(e).position') == 'relative'
        click(selector)
        assert page.locator('#e9pop b').inner_text() == title
        click('#e9pop')
        assert not page.locator('#e9pop').count()
    click('[data-room-puzzle="ink"]')
    page.wait_for_timeout(900)
    bounds()
    assert page.locator('.rp-seal img').evaluate('i=>i.complete&&i.naturalWidth===512')
    assert page.locator('.rp-trace img').evaluate('i=>i.complete&&i.naturalWidth===512')
    before_ink = state()
    click('#rp-overlap')
    assert not state()['beats'].get('inn_ink_compared')
    assert state()['found'] == before_ink['found']
    page.screenshot(path=f'/tmp/puzzle-ink-before-{size[0]}x{size[1]}.png')
    click('#rp-mirror')
    click('#rp-overlap')
    assert page.locator('.inn-room-puzzle').get_attribute('data-overlaid') == 'true'
    assert state()['beats'].get('inn_ink_compared')
    assert state()['found'] == before_ink['found'] and state()['asked'] == before_ink['asked']
    assert state()['hp'] == before_ink['hp'] and state()['wrong'] == before_ink['wrong']
    bounds()
    page.screenshot(path=f'/tmp/puzzle-ink-match-{size[0]}x{size[1]}.png')
    page.keyboard.press('Escape')
    assert page.locator('.crec2').count(), 'Comparison destroyed its underlying records'

    # State replacement cancels the overlay before a stale control can save to
    # another game. The original opened-box bit remains sufficient for legacy
    # progress; partial digits are never required by investigation/meeting.
    click('[data-room-puzzle="ink"]')
    page.wait_for_timeout(900)
    engine('G=JSON.parse(JSON.stringify(G));')
    page.wait_for_timeout(300)
    assert not page.locator('.inn-room-puzzle').count()
    assert state()['beats'].get('inn_lock')
    assert not page.locator('#bigscene [data-obs="o_inn_lock"]').count()
    clean = engine('sanitizeState({prog:{inn:Object.assign({},G,{beats:Object.assign({},G.beats,{inn_pin_d0:9,inn_pin_d1:-1,inn_pin_d2:"2",inn_pin_d3:99,inn_pin_hint:3})})}}).prog.inn.beats')
    assert clean['inn_pin_d0'] == 9 and all(k not in clean for k in ('inn_pin_d1','inn_pin_d2','inn_pin_d3','inn_pin_hint')), clean
    assert not errors, errors
    assert not bad, bad
    scope='optional mirror study, touch/keyboard, state cancellation' if only_ink else 'consent, clue boundary, touch/keyboard, wrong answer, save draft, original box state, optional mirror study, state cancellation'
    print(f'PASS {size[0]}×{size[1]}: {scope}', flush=True)
    context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--one-size', action='store_true', help='Run 844×390 only')
    parser.add_argument('--only-ink', action='store_true', help='Prepare an already opened box and focus on optional comparison')
    args = parser.parse_args()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        for size in ((844,390),) if args.one_size else ((844,390),(390,844),(640,360)):
            run(browser, args.url, size, args.only_ink)
        browser.close()


if __name__ == '__main__':
    main()
