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
        note=page.locator('#w209rail .g>[data-w="ev"]')
        if note.count() and note.is_enabled():break
        if page.locator('#tostay2').count():page.locator('#tostay2').click()
        else:page.keyboard.press('Enter')
        page.wait_for_timeout(180)
    page.wait_for_timeout(800)
    page.locator('#w209rail .g>[data-w="ev"]').click()
    page.locator('.crec2').wait_for(state='visible')
    for cid in ['C01','C02','C04']:
        assert page.locator('.crec2 [data-crs="'+cid+'"]').count(),cid
    if not page.locator('.crec2 [data-crs="C03"]').count():
        page.locator('.crec2 [data-crt="t"]').click()
    assert page.locator('.crec2 [data-crs="C03"]').count(),'Collected witness testimony was lost'
    assert not page.locator('#logic-note,#logic-panel').count(),'Retired deduction quiz returned'
    assert not errors,errors
    assert not bad,bad
    print('Clean production continue: actual collected clues and testimony survive reload in the icon inventory; no extra quiz; errors/HTTP failures 0')
    browser.close()
