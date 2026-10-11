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
        'Bookstore explains retirement':'엄마랑 서점 열면서 그만뒀지.',
        'Disappearance remains unexplained':'아직 몰라.',
        'Old letter identifies a past stop':'몇 해 전 편지랬지?',
        'Father confirms letter origin':'엄마가 여기서 부쳤어.',
        'Village witnesses motivate visit':'엄마를 기억하는 사람도 있겠다',
        'Father checks return journey':'돌아가는 마차는 언제',
        'Noon final coach':'내일 정오요. 올해 마지막 마차입니다',
        'Snow closes pass':'눈이 쌓이면 고개를 못 넘어요',
        'Closed office motivates lodging':'아빠, 우체국 문 닫혔어.',
        'Photo motivates question':'우리 엄마예요. 여기서 편지를 보냈대요.',
        'Guest confidentiality':'손님 얘긴 함부로 못 해요',
        'Child counts before extra bed':'하나, 둘, 셋… 열하나, 열둘.',
        'Extra bed outside guest count':'저 침대는 안 세는 거예요?',
        'Child independently records clue':'잊을까 봐 적었어.',
        'Child wants to show photo tomorrow':'내일은 내가 사진 보여 줄래.',
        'Father accompanies child':'같이 가자.',
        'Night sound is shared':'아빠, 저 소리… 들려?',
        'Father limits night movement':'문 앞까지만. 옆에 있어.',
        'Child sees light before silence':'저 문 밑에 빛이 새네.',
        'Child sees light extinguish':'조용해졌어. 불도 꺼졌고.',
        'Child sees eyes':'아빠… 위에 눈이…!',
        'Child asks for company when returning':'손 잡고.',
        'Bell only rings on the hour':'아니. 마을 종은 정각에만.',
        'Reporter states amount':'계약금 삼백 냥입니다.',
        'Reporter states waking time':'여섯 시 반에 깼을 땐 이미 없었습니다.',
        'Search needs permission':'다른 방도 허락받고 보겠습니다.',
        'Questioning not guilt':'도둑이라고 정한 건 아닙니다',
        'Father does not assume guilt':'누가 옮겼는지는 아직 모르죠.',
        'Past detective explains intervention':'전 탐정이었습니다.',
        'Father asks investigation permission':'저희도 살펴봐도 되겠습니까?',
        'Deadline is last transport':'위 마을로 가는 마차는 정오가 마지막입니다',
        'Child fears losing mother lead':'할머니 가면, 엄마 얘긴 누구한테 물어?',
        'Child records observed action':'할머니가 이불 보던 것도 적을게',
        'Search begins with physical clues':'주머니부터 보자',
    }
    for fact, phrase in required_facts.items():
        assert any(phrase in t for t in seen), ('Required introduction fact missing', fact, phrase)
    # The grandmother comments on resemblance only after being shown the photo.
    encounter = ('우리 엄마예요', '제 아내입니다',
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
        ('몇 해 전 편지랬지', '엄마가 여기서 부쳤어', '엄마를 기억하는 사람도 있겠다'),
        ('돌아가는 마차는 언제', '내일 정오요', '그다음은 언제', '봄이요. 눈이'),
        ('우체국 문 닫혔어', '아침에 다시 오자', '오늘은 어디서 자', '여관부터 찾아보자', '겨울잠 여관이다'),
        ('하나, 둘, 셋… 열하나, 열둘.', '열셋. 할머니', '손님 침대는 열둘이에요'),
        ('엄마 사진 보고 말이 없어졌어', '잊을까 봐 적었어', '내일은 내가 사진 보여 줄래'),
        ('아빠, 저 소리', '사진은 아침에.', '문 앞까지만.', '저 문 밑에 빛',
         '조용해졌어. 불도 꺼졌고.', '아빠… 위에 눈이', '가서 자, 꼬맹이', '손 잡고.'),
        ('왜 이 방에 있었는지는 할머니께도', '관청에서 조사받으셔야', '전 탐정이었습니다'),
        ('할머니 가면, 엄마 얘긴', '그 전에 살펴보자', '주머니부터 보자'),
    ]
    for chain in chains:
        positions = [next(i for i,t in enumerate(played) if phrase in t) for phrase in chain]
        assert positions == sorted(positions), ('Motive/action out of order', chain, positions)
    assert not any('크르르' in t or '괴물 목소리' in t or '아빠처럼 탐정 할래' in t for t in seen), 'Disconnected role-play remains'
    for sid in ('P10','P10b'):
        child=sum(len(l['line']) for l in native if l['sid']==sid and l['who']=='det1')
        father=sum(len(l['line']) for l in native if l['sid']==sid and l['who']=='det0')
        assert child>father,(sid,child,father)
    assert not any('마부 까로예요' in t or '도착은 늘 제때죠' in t or '언덕 위래' in t for t in seen), 'Old arrival exposition remains'
    assert not errors,errors
    assert not bad,bad
    Path(args.output).write_text(json.dumps({'url':frame.url,'played':native,'errors':errors,'bad':bad},ensure_ascii=False))
    print('Intro OK: actual fresh father POV, welcome→father reply, spoken motives, accompanied night outing/return; errors/HTTP failures 0')
    b.close()
