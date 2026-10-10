"""Fresh-game introduction via pointer/keyboard input; stops at investigation."""
import shutil
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':844,'height':390});errors=[];bad=[];seen=set()
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    pg.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');pg.wait_for_timeout(16000)
    pg.locator('[data-m="new"]').click()
    for i in range(800):
        st=pg.evaluate('window.__T("({beats:G&&G.beats,dl:!!DL})")')
        text=pg.evaluate('window.__innAudioState().line')
        if text:seen.add(text)
        if st['beats'] and st['beats'].get('inn_pro'):break
        if st['dl']:pg.keyboard.press('Enter')
        elif pg.locator('#inncold').count():pg.mouse.click(400,250)
        else:pg.keyboard.press('Enter')
        pg.wait_for_timeout(180)
    assert st['beats'].get('inn_pro'),st
    assert any('편지를 보고 왔습니다' in t for t in seen),'Mother-search purpose missing'
    assert any('먼저 주머니가 왜 여기 있었는지만' in t for t in seen),'Limited investigation motive missing'
    assert not errors,errors
    assert not bad,bad
    print('Fresh intro → investigation OK; mother-search purpose and limited intervention shown; errors/HTTP failures 0')
    b.close()
