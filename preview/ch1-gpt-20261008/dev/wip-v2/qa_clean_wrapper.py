"""Production wrapper smoke via native input, without __T or evidence seeding."""
import argparse, math, shutil, time
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--url',default='http://127.0.0.1:8000/v2.html?v=06a314a52fdf')
p.add_argument('--version',default='06a314a52fdf')
p.add_argument('--save',default='/tmp/investigation-after-linen.json')
a=p.parse_args()
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    for w,h in [(844,390),(390,844)]:
        context=browser.new_context(viewport={'width':w,'height':h})
        page=context.new_page();errors=[];bad=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
        page.goto(a.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
        frame=page.locator('#game').element_handle().content_frame()
        assert 'build='+a.version in frame.url,frame.url
        assert frame.evaluate('typeof window.__T')=='undefined','QA eval hook leaked into production'
        matrix=page.locator('#game').evaluate('e=>{const m=new DOMMatrix(getComputedStyle(e).transform);return [m.a,m.b,m.c,m.d]}')
        x,y=math.hypot(*matrix[:2]),math.hypot(*matrix[2:])
        assert x>0 and abs(x-y)<1e-7,('Nonuniform scale',matrix)
        assert abs(matrix[0]*matrix[2]+matrix[1]*matrix[3])<1e-7,('Sheared frame',matrix)
        frame.locator('#innmain [data-m="new"]').click()
        deadline=time.monotonic()+80
        while not frame.locator('#inn-story-cg.ready').count() and time.monotonic()<deadline:
            if frame.locator('#inncold').count():frame.locator('#inncold').click()
            else:page.keyboard.press('Enter')
            page.wait_for_timeout(180)
        cg=frame.locator('#inn-story-cg.ready')
        assert cg.count() and cg.is_visible(),'Opening CG did not appear after native new-game input'
        assert cg.get_attribute('data-cut')=='carriage'
        assert cg.locator('.cinema-picture').evaluate('i=>i.complete&&i.naturalWidth>0')
        page.wait_for_timeout(500)
        before=frame.evaluate('__innAudioState().line')
        for _ in range(10):
            page.keyboard.press('Enter');page.wait_for_timeout(220)
            if frame.evaluate('__innAudioState().line')!=before:break
        assert frame.evaluate('__innAudioState().line')!=before,'Native Enter did not advance opening dialogue'
        page.screenshot(path=f'/tmp/clean-wrapper-{w}x{h}.png')
        assert not errors,errors
        assert not bad,bad
        print('PASS',w,h,'exact version/clean hook/uniform transform/native menu→CG→Enter; JS/HTTP0',flush=True)
        context.close()
    if Path(a.save).is_file():
        context=browser.new_context(viewport={'width':844,'height':390},storage_state=a.save)
        page=context.new_page();page.goto(a.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
        frame=page.locator('#game').element_handle().content_frame()
        assert frame.evaluate('typeof __T')=='undefined'
        frame.locator('#innmain [data-m="cont"]').click();page.wait_for_timeout(1800)
        assert frame.locator('#bigscene').is_visible(),'Real saved investigation did not resume'
        assert not frame.locator('#inn-story-cg').count(),'Saved investigation replayed the opening CG'
        page.screenshot(path='/tmp/clean-wrapper-continue.png')
        print('PASS actual saved investigation Continue, no evidence injection',flush=True)
        context.close()
    browser.close()
