"""Fresh-game introduction via pointer/keyboard input; stops at investigation."""
import shutil
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':844,'height':390});errors=[];bad=[];seen=set();played=[]
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    pg.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');pg.wait_for_timeout(16000)
    pg.locator('[data-m="new"]').click()
    for i in range(800):
        st=pg.evaluate('window.__T("({beats:G&&G.beats,dl:!!DL})")')
        text=pg.evaluate('window.__innAudioState().line')
        if text:
            seen.add(text)
            if not played or played[-1] != text:played.append(text)
        if st['beats'] and st['beats'].get('inn_pro'):break
        if st['dl']:pg.keyboard.press('Enter')
        elif pg.locator('#inncold').count():pg.mouse.click(400,250)
        else:pg.keyboard.press('Enter')
        pg.wait_for_timeout(180)
    assert st['beats'].get('inn_pro'),st
    # Assert the actual story facts rather than the former explanatory wording.
    required_facts = {
        'Marriage, detective retirement and bookstore': '결혼하고 탐정 일을 접었지. 서점을 열고.',
        'Sudden disappearance and old letter': '엄마가 갑자기 사라져, 난 옛 편지를 꺼냈다.',
        'Letter is years old': '몇 해 전 편지야',
        'Mother search leads to this village': '옛 편지를 여기서 부쳤더군요',
        'Child wants to help find mother': '아빠처럼 탐정 할래. 엄마 찾게.',
        'Father accepts child observations': '네가 본 건 수첩에 적어 줘',
        'Child must not go ahead alone': '대신 혼자 먼저 가지 않기',
        'Former detective disclosed to villagers': '전 탐정이었습니다',
        'Child identifies loss of mother information': '할머니 가면, 엄마 얘긴 누구한테 물어?',
        'Mother information motivates intervention': '엄마 얘기도 들어야지',
        'Search starts with limited physical clues': '주머니부터 보자',
        'Child records observed behavior': '할머니가 이불 보던 것도 적을게',
        'Night outing begins with being woken by a sound': '이불 끄는 소리. 다람이 깬다. 아빠는 잔다.',
        'Child first checks from her own doorway': '다람이 방문을 조금 연다',
    }
    for fact, phrase in required_facts.items():
        assert any(phrase in t for t in seen), ('Required introduction fact missing', fact, phrase)
    # The grandmother comments on resemblance only after being shown the photo.
    encounter = ('아이 엄마를 찾고 있습니다', '아빠가 엄마 사진을 내민다',
                 '사진 속 엄마를 닮았구나')
    positions = [next(i for i, t in enumerate(played) if phrase in t) for phrase in encounter]
    assert positions == sorted(positions), ('Photo encounter out of order', positions)
    assert any('크르르. 내 책을' in t for t in seen), 'Shared bedtime routine not played'
    assert any('책 말고 간식!' in t for t in seen), 'Child did not correct the familiar story'
    assert not errors,errors
    assert not bad,bad
    print('Fresh intro → investigation OK; family bookstore, sudden disappearance, former detective, child observer and limited intervention shown; errors/HTTP failures 0')
    b.close()
