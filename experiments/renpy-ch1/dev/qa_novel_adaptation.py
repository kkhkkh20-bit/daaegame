"""소설 적용 장면의 웹 표시와 저장 복원. 장면 시작 상태를 준비하는 부분 시험이다."""
import asyncio
import json
import os
from pathlib import Path

from playwright.async_api import async_playwright
from webqa import SayQA

OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-novel-web'))
URL = os.environ.get('ROOM13_URL', 'http://127.0.0.1:8765/preview/room13-dev/')


async def jump(q, label):
    await q.py('\n'.join([
        'import renpy',
        'def qa_novel_jump(**kwargs):',
        ' import renpy',
        ' s=renpy.store',
        ' renpy.ui.textbutton("검토 계속",clicked=[s.Hide("qa_novel_jump"),s.Jump('+repr(label)+')],xpos=500,ypos=300,xsize=280,ysize=80)',
        'renpy.exports.define_screen("qa_novel_jump",qa_novel_jump,modal="True",zorder="200")',
        'renpy.exports.show_screen("qa_novel_jump")',
        'renpy.exports.restart_interaction()',
        'result=True',
    ]))
    await q.press('검토 계속')


async def prepare(q, day, location, actors, values, scene=None):
    code = ['import renpy', 's=renpy.store',
            's.r13_v111_set("day",'+str(day)+')',
            's.r13_edit(day='+str(day)+',period=1,location='+repr(location)+')']
    code += ['s.r13_v111_set('+repr(k)+','+repr(v)+')' for k, v in values.items()]
    code += ['s.r13_v111_arrive('+repr(actors)+')']
    if scene:
        code += ['s.r13_v111_scene('+repr(scene)+')']
    code += ['s.place=s.R13_PLACES['+repr(location)+'][0]',
             's.r13_scene_bg=s.R13_PLACES['+repr(location)+'][1]',
             'renpy.exports.scene()',
             'renpy.exports.show("novel_background",what=s.r13_background(s.r13_scene_bg))',
             'result=True']
    await q.py('\n'.join(code))


async def until(q, text=None, screen=None):
    for _ in range(160):
        st = await q.state()
        assert '_exception' not in st['screens'], st
        shown = st.get('say', '').replace('\n', ' ')
        if (text and text in shown) or (screen and screen in st['screens']):
            return st
        if 'say' in st['screens']:
            await q.input(900, 610)
        elif 'choice' in st['screens'] and screen == 'r13_hub':
            await q.press('편지를 접는다')
        elif 'r13_cinematic_view' in st['screens']:
            await q.press('계속')
        else:
            await asyncio.sleep(.15)
    raise AssertionError((text, screen, st))


async def capture(q, name):
    await asyncio.sleep(.5)
    await q.p.screenshot(path=str(OUT/(name+'.png')))
    (OUT/(name+'.json')).write_text(json.dumps(await q.state(), ensure_ascii=False, indent=2))


async def save_and_load(q):
    # 현재 여섯 칸 UI의 실제 설정 탭과 실제 슬롯을 누른다.
    await q.press('더보기')
    await asyncio.sleep(.3)
    await q.press('설정')
    await q.wait('pause_menu')
    await q.press('저장')
    await asyncio.sleep(.4)
    rects = await q.py('import renpy;result=sorted([[f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if f.x is not None and 400<=f.w<=440 and 80<=f.h<=160],key=lambda r:(r[1],r[0]))')
    assert len(rects) == 6, rects
    x, y, w, h = rects[1]
    await q.input(x+w/2, y+h/2)
    if 'confirm' in (await q.state())['screens']:
        await q.press('예')
    await q.press('닫기')
    await q.wait('say')
    await q.press('더보기')
    await asyncio.sleep(.3)
    await q.press('설정')
    await q.wait('pause_menu')
    await q.press('저장')
    await q.press('불러오기')
    await q.input(x+w/2, y+h/2)
    await q.wait('confirm')
    await q.press('예')
    await q.wait('say')


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'scope': '장면 시작 상태를 준비한 웹 부분 시험. 전체 자연 플레이 아님.', 'checks': []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME', '/usr/bin/chromium'),
                                          args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport={'width': 1280, 'height': 720}, has_touch=True)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        q = SayQA(page, OUT)
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')", timeout=180000)
            await q.wait('main_menu')
            await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
            await q.press('처음부터')
            await until(q, screen='r13_hub')
            await prepare(q, 5, 'gate', ['daram', 'resident_lamplighter'], {})
            await jump(q, 'r13_v111_warning_read5')
            await until(q, text='그날 밤 초롱 씨 오는 길목')
            assert not await q.py('import renpy;result=bool(renpy.store.r13_v111_value("mother_first_contact_read5"))')
            await capture(q, '01_첫편지_PC')
            await page.set_viewport_size({'width': 844, 'height': 390})
            await capture(q, '02_첫편지_휴대폰')
            await page.set_viewport_size({'width': 1280, 'height': 720})
            saved = await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,read=s.r13_v111_value("mother_first_contact_read5"))')
            await save_and_load(q)
            loaded = await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,read=s.r13_v111_value("mother_first_contact_read5"))')
            assert saved == loaded, (saved, loaded)
            await until(q, screen='r13_crisis_proof')
            assert await q.py('import renpy;result=renpy.store.r13_v111_value("mother_first_contact_read5") is True')
            report['checks'].append('첫 편지 PC·휴대폰 표시, 전문 청취 전후 상태, 실제 저장·불러오기 복원')
            await prepare(q, 11, 'greenhouse', ['mom', 'daram'], dict(route7='murder', OWL_ALIVE=False,
                DARAM_DETAINED=False, family_reunited=True, mother_first_contact_read5=True, mother_contact_relay10=True))
            await jump(q, 'r13_v111_mother_life11')
            await until(q, text='초롱 아저씨가 그저께')
            await capture(q, '03_재회_PC')
            await page.set_viewport_size({'width': 844, 'height': 390})
            await capture(q, '04_재회_휴대폰')
            await page.set_viewport_size({'width': 1280, 'height': 720})
            report['checks'].append('이미 들은 연락 경위를 반복하지 않는 재회 장면 PC·휴대폰 표시')
            await prepare(q, 14, 'school', ['mom', 'daram'], dict(ending14='morning', piko_alive=False,
                portrait='unfinished', portrait_waiting_for_mom=True, family_reunited=True, DARAM_DETAINED=False))
            await jump(q, 'r13_v111_cookie14')
            await until(q, text='아이가 조그만 코를 그려 넣는다')
            await capture(q, '05_초상화_PC')
            await page.set_viewport_size({'width': 844, 'height': 390})
            await capture(q, '06_초상화_휴대폰')
            await page.set_viewport_size({'width': 1280, 'height': 720})
            await until(q, text='눈 감아 봐')
            assert await q.py('import renpy;s=renpy.store;result=s.r13_v111_value("portrait")=="child_completed" and not s.r13_v111_value("portrait_waiting_for_mom")')
            report['checks'].append('초상화 완성 PC·휴대폰 표시와 행동 뒤 상태 저장')
            report['version'] = await q.py('import renpy;result=renpy.store.config.version')
            assert report['version'] == '0.20.97'
            assert not errors, errors
            report.update(status='passed', page_errors=errors)
        except Exception as error:
            report.update(status='failed', error=repr(error), page_errors=errors)
            await page.screenshot(path=str(OUT/'실패.png'))
            raise
        finally:
            (OUT/'결과.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
            await browser.close()
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(main())
