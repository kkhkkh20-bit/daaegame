"""A01/A02: 명시적 2일차 fixture 이후 실제 생각·초롱·자료 UI 검수.

연속 자연 진행을 주장하지 않는다. 날짜/장소/단계/등장인물/기존 만남은 fixture다.
안내를 열고 닫는 동안 room13 전체 불변을 비교한다. 대사 읽음 이력과 화면
설정은 게임의 통상 UI 동작이며 진행 상태와 별도로 기록한다. 서버/빌드 생성 없음.
"""
import asyncio
import json
import os
import traceback
from pathlib import Path

from playwright.async_api import async_playwright
from qa_play_review_field import FieldQA, FOCUS

OUT = Path(os.environ.get('ROOM13_QA_OUT', '/workspace/work/daram-additional-qa/guidance'))
URL = os.environ.get('ROOM13_URL', 'http://127.0.0.1:8765/preview/room13-dev/')
OUT.mkdir(parents=True, exist_ok=True)
STAGES = [
    ('lamp_rope', 'square', 'MS14_D02_S01', None, '덮개 지지 끈'),
    ('go_box', 'square', 'MS14_D02_S01', None, '깊은 숲의 교환함'),
    ('box_inspect', 'forest', 'MS14_D02_S01', None, '교환함과 주변'),
    ('box_note', 'forest', 'MS14_D02_S01', None, '쪽지를 교환함에 직접'),
    ('travel', 'forest', 'MS14_D02_S02', 'post', '우체국에서 초대 편지의 발신인'),
]
SIZES = [('pc', 1280, 720, False), ('small-phone-large', 740, 360, True)]

TEXTS = '''import renpy
sc=renpy.display.screen.get_screen('r13_hub');seen=set();texts=[];thought=None
def walk(w):
 global thought
 if id(w) in seen:return
 seen.add(id(w))
 if isinstance(w,renpy.text.text.Text):
  t=''.join(str(x) for x in w.text);texts.append(t)
  if t==renpy.store.r13_v111_goal():
   thought=dict(text=t,render_size=list(renpy.display.render.render(w,542,720,0,0).get_size()))
 for c in w.visit():walk(c)
walk(sc)
result=dict(texts=texts,thought=thought,open=renpy.store.r13_goal_open)
'''


class GuidanceQA(FieldQA):
    async def room(self):
        return await self.py('import renpy,copy;result=copy.deepcopy(renpy.store.room13)')

    async def click_focus(self, predicate):
        rows = [r for r in await self.py(FOCUS) if predicate(r)]
        rows = [r for r in rows if 0 < r['rect'][0]+r['rect'][2]/2 < 1280 and 0 < r['rect'][1]+r['rect'][3]/2 < 720]
        assert rows, ('누를 대상 없음', await self.py(FOCUS))
        row = min(rows, key=lambda r: r['rect'][2]*r['rect'][3])
        x, y, w, h = row['rect']
        await self.input(x+w/2, y+h/2)
        return row

    async def person(self):
        state = await self.state()
        if any('사람 보기' in b['text'] for b in state['buttons']):
            await self.press('사람 보기')
        for side in (None, 48, 1232):
            if side is not None:
                await self.input(side, 276)
                await asyncio.sleep(.7)
            rows = await self.py(FOCUS)
            if any(r['text'] == '초롱' and 0 < r['rect'][0]+r['rect'][2]/2 < 1280 for r in rows):
                return await self.click_focus(lambda r: r['text'] == '초롱')
        raise AssertionError(('초롱 이름 버튼 없음', rows))

    async def fixture(self, gate, location, scene, travel_to):
        # Seed existing encounters so repetition does not add a new meeting row.
        await self.py('''import renpy
s=renpy.store
s.r13_edit(day=2,period=0,location=%r)
s.r13_v111_set('day',2)
s.room13['v111']['scene']=%r
s.room13['v111']['travel_to']=%r
s.place=s.R13_PLACES[%r][0]
s.r13_v111_talk_person=None;s.r13_goal_open=False;s.r13_carriage_skip=False
s.r13_v111_context(%r);s.key=%r
s.r13_v111_arrive(['daram','resident_lamplighter'])
s.r13_note_encounter('resident_lamplighter');s.r13_note_encounter('dad')
s.r13_records_view=dict(tab='relations',page=0,detail=None)
result=True
''' % (location, scene, travel_to, location, gate, gate))
        await self.jump_fixture('r13_v111_wait_again')
        await self.wait('r13_hub')


async def main():
    report = dict(scope=__doc__, checks=[], stages=[], page_errors=[])
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME', '/usr/bin/chromium'), args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport=dict(width=1280, height=720), has_touch=True)
        q = GuidanceQA(page, OUT)
        page.on('pageerror', lambda error: report['page_errors'].append(str(error)))
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function'", timeout=300000)
            await q.wait('main_menu')
            report['version'] = await q.py('import renpy;result=renpy.config.version')
            assert await q.py('import renpy;result=hasattr(renpy.store,"r13_day2_guidance")'), '새 안내 빌드가 필요합니다.'
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
            await q.press('처음부터')
            await q.wait('say')
            for gate, location, scene, travel_to, expected in STAGES:
                await q.fixture(gate, location, scene, travel_to)
                stage = dict(gate=gate, location=location, scene=scene, travel_to=travel_to, expected=expected, views=[], repeats=[])
                report['stages'].append(stage)
                before = await q.room()
                stage['before'] = before
                goal = await q.py('import renpy;result=renpy.store.r13_v111_goal()')
                assert expected in goal, (gate, goal)
                # Existing remembered relations tab must not divert the new link.
                for tag, width, height, large in SIZES:
                    await q.setting_fixture(width, height, large)
                    await q.click_focus(lambda r: r['text'] in ('생각', '새 생각'))
                    await asyncio.sleep(.4)
                    text = await q.py(TEXTS)
                    assert text['open'] and text['thought'], text
                    assert expected in text['thought']['text'], text
                    assert not any('의문 0개' in t for t in text['texts']), text
                    # The thought viewport has 116 virtual px. Text must fit fully.
                    assert text['thought']['render_size'][1] <= 116, text
                    controls = [r for r in await q.py(FOCUS) if r['text'] in ('접기', '모은 자료 보기')]
                    assert len(controls) == 2, controls
                    assert all(0 <= r['rect'][0] and r['rect'][0]+r['rect'][2] <= 1280 and 0 <= r['rect'][1] and r['rect'][1]+r['rect'][3] <= 720 for r in controls), controls
                    stage['views'].append(dict(size=tag, text=text, controls=controls))
                    await q.shot(gate+'-'+tag+'-thought')
                    await q.press('모은 자료 보기')
                    await q.wait('r13_records')
                    tab = await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result=sc.scope["tab"]')
                    assert tab == 'all', ('자료 탭 연결 실패', tab)
                    await q.shot(gate+'-'+tag+'-materials')
                    await q.click_focus(lambda r: r['alt'] == '닫기' or r['text'] == '닫기')
                    await q.wait('r13_hub')
                    assert not await q.py('import renpy;result=renpy.store.r13_goal_open')
                    assert await q.room() == before, ('생각·자료 열람이 상태 변경', gate, before, await q.room())
                if gate != 'travel':
                    for index in range(2):
                        await q.person()
                        say = await q.wait('say')
                        assert expected in say['say'] if gate != 'lamp_rope' else '덮개 지지 끈을 먼저 잡아' in say['say'], say
                        stage['repeats'].append(say['say'])
                        await q.shot(gate+'-repeat-'+str(index+1))
                        await q.advance_until('r13_hub')
                        assert await q.room() == before, ('초롱 재클릭이 상태 변경', gate, before, await q.room())
                name = await q.py('import renpy;result=renpy.store.r13_object_name("lamp")')
                stage['lamp_name'] = name
                assert ('덮개 지지 끈' in name) == (gate == 'lamp_rope'), (gate, name)
                if gate == 'lamp_rope':
                    await q.setting_fixture(1280, 720, False)
                    if any('주변 살피기' in b['text'] for b in (await q.state())['buttons']):
                        await q.press('주변 살피기')
                    for side in (None, 48, 1232):
                        if side is not None:
                            await q.input(side,276);await asyncio.sleep(.7)
                        rows = [r for r in await q.py(FOCUS) if '덮개 지지 끈' in r['alt'] and 0 < r['rect'][0]+r['rect'][2]/2 < 1280]
                        if rows:break
                    assert rows, ('등불 접근성 이름 없음', await q.py(FOCUS))
                    x,y,w,h=rows[0]['rect']
                    await page.mouse.move(x+w/2,y+h/2);await asyncio.sleep(.5)
                    await q.shot('lamp-rope-name-hover')
                    stage['lamp_target']=rows[0]
                stage['after'] = await q.room()
                assert stage['after'] == before, (gate, before, stage['after'])
                report['checks'].append(gate+' 생각·자료 링크·반복 안내의 진행 상태 불변')
            assert not report['page_errors'], report['page_errors']
            report['status'] = 'passed-pending-visual-review'
        except Exception:
            report['status'] = 'failed'
            report['error'] = traceback.format_exc()
            await page.screenshot(path=str(OUT/'failure.png'))
        finally:
            (OUT/'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
            print(json.dumps(dict(status=report.get('status'), checks=report['checks'], error=report.get('error')), ensure_ascii=False), flush=True)
            await browser.close()
    if report['status'] == 'failed':
        raise SystemExit(1)


if __name__ == '__main__':
    asyncio.run(main())
