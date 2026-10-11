"""Native next-morning question using storage from a real fresh-game playthrough."""
import argparse
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save', required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', default='/tmp/father-view-question.json')
    args = parser.parse_args()
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 844, 'height': 390}, storage_state=args.save)
        page = context.new_page()
        errors, bad, lines = [], [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('response', lambda r: bad.append(r.url) if r.status >= 400 and 'favicon' not in r.url else None)
        page.goto(args.url, wait_until='domcontentloaded')
        page.wait_for_timeout(16000)
        frame = page.locator('#game').element_handle().content_frame()
        assert 'build=' + args.version in frame.url, frame.url
        assert frame.evaluate('typeof __T') == 'undefined'
        frame.locator('#innmain [data-m="cont"]').click()
        page.wait_for_timeout(1800)
        if frame.locator('#closeNotice:visible').count():
            frame.locator('#closeNotice').click()
        frame.locator('#w209rail .g>[data-w="move"]').click()
        frame.locator('#innmove [data-room-id="hall"]').click()
        page.wait_for_timeout(2200)
        point = None
        for direction in (None, '#fsar', '#fsar', '#fsal'):
            if direction and frame.locator(direction + ':visible').count():
                frame.locator(direction).click()
                page.wait_for_timeout(700)
            point = frame.evaluate('''()=>{const r=document.querySelector('#bigscene').getBoundingClientRect();
              for(let y=Math.max(12,r.top+12);y<Math.min(innerHeight-12,r.bottom-12);y+=6)
               for(let x=Math.max(12,r.left+12);x<Math.min(innerWidth-12,r.right-12);x+=6)
                if(document.elementFromPoint(x,y)?.closest('#bigscene')&&window.__innNpcHit(x,y)==='geokkuri')return {x,y};return null}''')
            if point:
                break
        assert point, 'Bat has no reachable opaque pixels'
        offset = page.locator('#game').bounding_box()
        page.mouse.click(offset['x'] + point['x'], offset['y'] + point['y'])
        page.wait_for_timeout(1800)
        quiet = 0
        for _ in range(90):
            if frame.locator('#dlgveil').count():
                quiet = 0
                page.keyboard.press('Enter')
                page.wait_for_timeout(180)
            else:
                quiet += 1
                page.wait_for_timeout(200)
                if quiet >= 6:
                    break
        frame.locator('.fstalk').wait_for(state='visible')
        page.wait_for_timeout(800)
        frame.locator('[data-ask="C07"]:visible').click()
        frame.locator('#dlgveil').wait_for(state='visible')
        page.wait_for_timeout(200)
        for _ in range(100):
            if not frame.locator('#dlgveil').count():
                break
            state = frame.evaluate('__innAudioState()')
            item = {'who': state['who'], 'line': state['line']}
            if not lines or lines[-1] != item:
                lines.append(item)
            page.keyboard.press('Enter')
            page.wait_for_timeout(210)
        else:
            raise AssertionError('C07 question did not finish')
        frame.locator('#okfind').wait_for(state='visible')
        frame.locator('#okfind').click()
        page.wait_for_timeout(700)
        text = '\n'.join(x['line'] or '' for x in lines)
        for required in ('어젯밤 그 언니야', '문 앞에서 둘이 놀랐지', '어젯밤엔 소리가 나서', '밤이예요', '밤에는 늘 그 자리에'):
            assert required in text, (required, lines)
        assert '혼자 나왔어' not in text and '꼭 깨울게' not in text, lines
        assert not frame.locator('#inn-story-cg,#inncold').count()
        assert not errors and not bad, (errors, bad)
        Path(args.output).write_text(json.dumps({'nativeQuestion': 'C07', 'lines': lines, 'errors': errors, 'httpFailures': bad}, ensure_ascii=False, indent=2), encoding='utf-8')
        print('PASS actual investigation save → native hall/Bat pointer/C07; accompanied night continuity, no opening CG, JS/HTTP0')
        browser.close()


if __name__ == '__main__':
    main()
