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
        'Marriage, detective retirement and bookstore': '엄마와 결혼하고 서점을 열면서, 탐정 일은 그만뒀다.',
        'Sudden disappearance remains unexplained': '엄마는 왜 갑자기 사라졌을까',
        'Letter is years old': '몇 해 전 편지야',
        'Old letter identifies a past stop, not current whereabouts': '엄마가 여기 우체국에서 부친 거야',
        'Village witnesses motivate the journey': '엄마를 기억하는 사람도 있겠다',
        'Closed post office leads to lodging': '오늘은 잘 곳부터 찾자',
        'Mother search leads to this village': '옛 편지를 여기서 부쳤더군요',
        'Grandmother cares despite withholding guest information': '찾느라 걱정이 많겠구나',
        'Child counts beds before noticing the extra one': '하나, 둘, 셋… 열하나, 열둘.',
        'Extra bed is outside the guest-bed count': '저 침대는 안 세는 거예요?',
        'Child wants to help find mother': '아빠처럼 탐정 할래. 나도 엄마 찾을래.',
        'Father accepts child observations': '네가 본 건 수첩에 적어 줘',
        'Child must not go ahead alone': '대신 혼자 먼저 가지 않기',
        'Former detective disclosed to villagers': '전 탐정이었습니다',
        'Inn owner is asked for circumstances, not declared guilty': '왜 이 방에 있었는지는 할머니께도 묻겠습니다',
        'Village bell rings only at the hour': '마을 종이야. 정각에만 쳐. 반 시엔 안 치고.',
        'Questioning is distinguished from guilt': '도둑이라고 정한 건 아닙니다',
        'Noon deadline is the last transport': '위 마을로 가는 마차는 정오가 마지막입니다',
        'Father also opposes blame without checking': '확인도 없이 누굴 도둑으로 몰 순 없고',
        'Child identifies loss of mother information': '할머니 가면, 엄마 얘긴 누구한테 물어?',
        'Mother information motivates intervention': '엄마 얘기도 들어야지',
        'Search starts with limited physical clues': '주머니부터 보자',
        'Child records observed behavior': '할머니가 이불 보던 것도 적을게',
        'Night outing begins with being woken by a sound': '이불 끄는 소리에 다람이 눈을 뜬다',
        'Child first checks from her own doorway': '다람이 방문을 조금 연다',
        'Child knowingly rationalizes breaking the promise': '혼자 가지 말랬는데… 문 앞까지만 보자',
    }
    for fact, phrase in required_facts.items():
        assert any(phrase in t for t in seen), ('Required introduction fact missing', fact, phrase)
    # The grandmother comments on resemblance only after being shown the photo.
    encounter = ('아이 엄마를 찾고 있습니다', '아빠가 엄마 사진을 내민다',
                 '사진 속 엄마를 닮았구나')
    positions = [next(i for i, t in enumerate(played) if phrase in t) for phrase in encounter]
    assert positions == sorted(positions), ('Photo encounter out of order', positions)
    # The player hears each motive before the consequential action.
    chains = [
        ('몇 해 전 편지야', '엄마가 여기 우체국에서 부친 거야', '엄마를 기억하는 사람도 있겠다'),
        ('우체국 문이 닫혔네', '오늘은 잘 곳부터 찾자', '겨울잠 여관!'),
        ('하나, 둘, 셋… 열하나, 열둘.', '열셋. 할머니', '손님 침대는 열둘이에요'),
        ('왜 이 방에 있었는지는 할머니께도', '관청에서 조사받으셔야', '전 탐정이었습니다'),
        ('할머니 가면, 엄마 얘긴', '엄마 얘기도 들어야지', '주머니부터 보자'),
    ]
    for chain in chains:
        positions = [next(i for i,t in enumerate(played) if phrase in t) for phrase in chain]
        assert positions == sorted(positions), ('Motive/action out of order', chain, positions)
    assert any('크르르. 내 책을' in t for t in seen), 'Shared bedtime routine not played'
    assert any('책 말고 간식!' in t for t in seen), 'Child did not correct the familiar story'
    assert not errors,errors
    assert not bad,bad
    print('Fresh intro → investigation OK; old-letter journey, warm photo encounter, night choice, noon inquiry and fair intervention connected; errors/HTTP failures 0')
    b.close()
