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
    # Assert the actual story facts rather than the former explanatory wording.
    required_facts = {
        'Marriage, detective retirement and bookstore': '결혼 뒤 탐정 일을 접고 서점을 열었다',
        'Sudden disappearance and old letter': '엄마가 갑자기 사라지고 옛 편지를 꺼냈다',
        'Letter is years old': '몇 해 전 편지야',
        'Mother search leads to this village': '아이 엄마를 아십니까? 이 마을에서 편지를 부쳤는데요',
        'Child wants to help find mother': '나도 아빠처럼 탐정 할래. 엄마 찾는 것도 같이 할래',
        'Father accepts child observations': '아빠가 놓친 건 네가 알려 줘',
        'Child must not go ahead alone': '대신 혼자 먼저 가지 않기',
        'Former detective disclosed to villagers': '예전에 탐정 일을 했습니다',
        'Mother information motivates intervention': '할머니가 가시면 엄마 얘기도 못 듣겠네',
        'Search starts with limited physical clues': '주머니와 이불부터 살펴보자',
        'Child records observed behavior': '할머니가 이불 보던 것도 적을게',
    }
    for fact, phrase in required_facts.items():
        assert any(phrase in t for t in seen), ('Required introduction fact missing', fact, phrase)
    assert any('크르르. 내 책을' in t for t in seen), 'Shared bedtime routine not played'
    assert any('책 말고 간식이야' in t for t in seen), 'Child did not correct the familiar story'
    assert not errors,errors
    assert not bad,bad
    print('Fresh intro → investigation OK; family bookstore, sudden disappearance, former detective, child observer and limited intervention shown; errors/HTTP failures 0')
    b.close()
