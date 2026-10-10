"""Reload a real investigation snapshot in the clean build, without QA hooks."""
import argparse
import shutil
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--storage',required=True,help='Actual after-linen snapshot from qa_investigation.py')
parser.add_argument('--url',default='http://127.0.0.1:8000/play_v2.html')
args=parser.parse_args()

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':844,'height':390},storage_state=args.storage)
    page=context.new_page();errors=[];bad=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    page.goto(args.url);page.wait_for_timeout(16000)
    assert page.evaluate('typeof window.__T')=='undefined','QA hook in production build'
    page.locator('#innmain [data-m="cont"]').click()
    page.wait_for_timeout(1800)
    # Resume any ordinary dialogue or room transition through genuine input.
    for _ in range(200):
        note=page.locator('#logic-note')
        if note.count() and note.is_enabled():break
        if page.locator('#tostay2').count():page.locator('#tostay2').click()
        else:page.keyboard.press('Enter')
        page.wait_for_timeout(180)
    page.locator('#logic-note').click()
    assert '수첩에 정리됨' in page.locator('#logic-panel [data-question="linen"]').inner_text()
    for cid in ['C01','C02','C03','C04']:
        assert page.locator('#logic-panel [data-card="'+cid+'"]').count(),cid
    assert not errors,errors
    assert not bad,bad
    print('Clean production continue: actual collected clues and completed notebook survive reload; errors/HTTP failures 0')
    browser.close()
