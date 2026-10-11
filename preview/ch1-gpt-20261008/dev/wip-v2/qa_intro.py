"""Actual fresh opening: father POV, native reply order and motives before actions."""
import argparse
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
ap.add_argument('--version')
ap.add_argument('--output',default='/tmp/father-opening-intro.json')
args=ap.parse_args()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':844,'height':390});errors=[];bad=[];seen=set();played=[]
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    pg.goto(args.url,wait_until='domcontentloaded');pg.wait_for_timeout(16000)
    frame=pg.locator('#game').element_handle().content_frame() if pg.locator('#game').count() else pg
    if args.version:
        assert 'build='+args.version in frame.url,frame.url
        assert frame.evaluate('typeof __T')=='undefined','QA hook in published payload'
    native=[]
    frame.locator('[data-m="new"]').click()
    for i in range(800):
        audio=frame.evaluate('window.__innAudioState()')
        story=frame.evaluate('window.__innPresentationState()')
        text=audio['line'];sid=story.get('sid')
        st={'dl':bool(frame.locator('#vnbox .vtxt').count()),'done':story.get('phase')=='investigation'}
        assert not frame.locator('#inncold').count(),'Culprit-only opening violates father POV'
        assert not audio['coldHeartbeat'],'Old opening pulse overlaps father scene'
        if text:
            seen.add(text)
            if not played or played[-1] != text:played.append(text)
            key=(sid,audio['who'],text)
            if not native or key!=(native[-1]['sid'],native[-1]['who'],native[-1]['line']):
                native.append({'sid':sid,'who':audio['who'],'line':text})
        if st['done']:break
        if st['dl']:pg.keyboard.press('Enter')
        else:pg.keyboard.press('Enter')
        pg.wait_for_timeout(180)
    assert st['done'],st
    # Assert the actual story facts rather than the former explanatory wording.
    required_facts = {
        'Family bookstore explains detective retirement': '탐정은 그만뒀지. 엄마랑 서점 열면서.',
        'Sudden disappearance remains unexplained': '엄마는 왜 갑자기 사라졌을까',
        'Letter is years old': '몇 해 전 편지야',
        'Old letter identifies a past stop, not current whereabouts': '엄마가 여기 우체국에서 부친 거야',
        'Village witnesses motivate the journey': '엄마를 기억하는 사람도 있겠다',
        'Father asks about the return journey': '돌아가는 마차는 언제 출발합니까',
        'Next noon is the final departure': '내일 정오요. 올해 마지막 마차입니다',
        'Snow explains the long transport gap': '눈이 쌓이면 고개를 못 넘어요',
        'Closed post office leads to lodging': '여관부터 찾아보자',
        'Mother search leads to this village': '몇 해 전에 여기서 편지를 부쳤더군요',
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
        'Child asks father about the sound': '아빠, 저 소리… 들려?',
        'Father hears the same sound': '응. 복도 쪽이네.',
        'Mother search is spoken before moving': '손님 있으면 엄마 사진 보여 주자.',
        'Father goes with child, stopping at the door': '문 앞까지만 같이 보자. 아빠 옆에 있어.',
        'No answer makes father decide to return': '대답이 없네. 돌아가자.',
        'Father also sees the hanging resident': '저기… 천장에 매달려 있군요.',
        'Father brings child back': '안 놓아. 같이 가자.',
        'Mother question is postponed until morning': '응. 아침에 물어보자.',
    }
    for fact, phrase in required_facts.items():
        assert any(phrase in t for t in seen), ('Required introduction fact missing', fact, phrase)
    # The grandmother comments on resemblance only after being shown the photo.
    encounter = ('제 아내를 찾고 있습니다', '이 사진 속 사람을 기억하십니까',
                 '사진 속 엄마를 닮았구나')
    positions = [next(i for i, t in enumerate(played) if phrase in t) for phrase in encounter]
    assert positions == sorted(positions), ('Photo encounter out of order', positions)
    welcome=[l for l in native if l['sid']=='P3']
    assert welcome[0]['who']=='innma' and welcome[0]['line'].startswith('어서 와요'),welcome[:2]
    assert welcome[1]['who']=='det0' and '묵을 수 있을까요' in welcome[1]['line'],welcome[:2]
    assert not [l for l in native if l['who']=='narr' and l['sid'] in ('P1','P10b')], 'Opening changed to a narrator/child-only camera'
    assert not any('잠들어 있다' in l['line'] or '주무시네' in l['line'] for l in native),'Father cannot witness the night while asleep'
    # The player hears each motive before the consequential action.
    chains = [
        ('몇 해 전 편지야', '엄마가 여기 우체국에서 부친 거야', '엄마를 기억하는 사람도 있겠다'),
        ('돌아가는 마차는 언제', '내일 정오요', '그다음은 언제', '봄이요. 눈이', '내일 오전엔 우체국'),
        ('우체국 문이 닫혔네', '아침에 다시 와야겠다', '오늘은 어디서 자', '여관부터 찾아보자', '겨울잠 여관이다'),
        ('하나, 둘, 셋… 열하나, 열둘.', '열셋. 할머니', '손님 침대는 열둘이에요'),
        ('왜 이 방에 있었는지는 할머니께도', '관청에서 조사받으셔야', '전 탐정이었습니다'),
        ('할머니 가면, 엄마 얘긴', '엄마 얘기도 들어야지', '주머니부터 보자'),
        ('아빠, 저 소리', '응. 복도 쪽이네.', '손님 있으면 엄마 사진', '문 앞까지만 같이', '저 문 밑에 빛',
         '조용해졌어. 불도 꺼졌고.', '대답이 없네. 돌아가자.', '저기… 천장에', '안 놓아. 같이 가자.', '응. 아침에 물어보자.'),
    ]
    for chain in chains:
        positions = [next(i for i,t in enumerate(played) if phrase in t) for phrase in chain]
        assert positions == sorted(positions), ('Motive/action out of order', chain, positions)
    assert any('크르르. 내 책을' in t for t in seen), 'Shared bedtime routine not played'
    assert any('책 말고 간식!' in t for t in seen), 'Child did not correct the familiar story'
    assert not any('마부 까로예요' in t or '도착은 늘 제때죠' in t or '언덕 위래' in t for t in seen), 'Old arrival exposition remains'
    assert not errors,errors
    assert not bad,bad
    Path(args.output).write_text(json.dumps({'url':frame.url,'played':native,'errors':errors,'bad':bad},ensure_ascii=False))
    print('Intro OK: actual fresh father POV, welcome→father reply, spoken motives, accompanied night outing/return; errors/HTTP failures 0')
    b.close()
