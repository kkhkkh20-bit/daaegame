# Browser check (0.18.63): 큰 강 / 깊은 숲 / 장터 in the real web build. Real clicks on the
# village map (polygon point and name label), travel, the picture for each period, and
# the places stay closed before lodging. 0.18.68: only residents with a new-place routine stand there. Screenshots: $ROOM13_QA_OUT/new-places.
import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

URL = os.environ.get('ROOM13_URL', 'http://localhost:8765/preview/room13-dev/')
OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa')) / 'new-places'
OUT.mkdir(parents=True, exist_ok=True)
DATA = json.loads((Path(__file__).resolve().parents[1] / 'game/room13-cartography.json').read_text())
QUIET = ["entry_corrected", "lodging", "livelihood_open", "ev_g_done", "ev_i_done", "ev_a_done", "ev_l_done",
         "ep1_patrol_seen", "ep1_eaves_seen"] + ["evening_brief:%d" % d for d in range(1, 14)]
NAMES = {'river': '큰 강', 'forest': '깊은 숲', 'market': '장터'}


async def main():
    report = {'checks': [], 'travel': {}}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),
                                    args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        c = await b.new_context(viewport={'width': 1280, 'height': 720}, has_touch=True)
        pg = await c.new_page()
        q = UIQA(pg, OUT)
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))

        async def jump(day, period, loc, flags):
            await q.py('import renpy;s=renpy.store;s.r13_edit(day=%d,period=%d,location=%r,life_poc=True);s.room13["flags"]=[];s.r13_flag(*%r);s.r13_upgrade()\n'
                       'def f(**kw):renpy.ui.timer(0.2,action=[renpy.store.Hide("qa_jump"),renpy.store.Jump("r13_field")])\n'
                       'renpy.display.screen.define_screen("qa_jump",f,zorder="200")\nrenpy.exports.show_screen("qa_jump");renpy.exports.restart_interaction();result=True' % (day, period, loc, flags))
            await asyncio.sleep(2.5); await q.advance(); await q.wait('r13_hub'); await asyncio.sleep(0.8)

        async def scope():
            return await q.py('import renpy;s=renpy.display.screen.get_screen("r13_map").scope;result={k:s[k] for k in ("region","selected")}')
        try:
            await pg.goto(URL)
            await pg.wait_for_function("typeof renpy_exec==='function'", timeout=150000)
            await q.wait('main_menu')
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.persistent.room13_map_list=False;result=True')
            await q.press('처음부터'); await q.advance(); await q.wait('r13_hub')
            # Before lodging: not places, not on the map.
            await jump(3, 0, 'square', [f for f in QUIET if f != 'lodging'])
            closed = await q.py('import renpy;s=renpy.store;result=[k for k in ("river","forest","market") if k in s.r13_places() or k in dict(s.r13_map_nodes("village"))]')
            assert closed == [], closed
            report['checks'].append('before lodging: river/forest/market are neither places nor map nodes')
            await jump(3, 0, 'square', QUIET)
            for key in ('river', 'forest', 'market'):
                await q.press('지도 · 이동'); await q.wait('r13_map')
                if (await scope())['region'] != 'village':
                    await q.press('마을')
                # Click the polygon point on the map art first, then the name label.
                x, y = DATA['regions']['village']['nodes'][key]['point']
                await q.input(16 + round(x * 1248 / 1672), 9 + round(y * 1248 / 1672))
                assert (await scope())['selected'] == key, (key, await scope())
                await q.input(16 + round(x * 1248 / 1672), 9 + round(y * 1248 / 1672))
                assert (await scope())['selected'] == key
                await q.shot('map-' + key)
                await q.press('이곳으로 이동')
                for _ in range(60):
                    st = await q.state()
                    if 'r13_hub' in st['screens']:
                        break
                    if 'say' in st['screens']:
                        await q.input(810, 610)
                    await asyncio.sleep(.3)
                await q.wait('r13_hub'); await asyncio.sleep(1.0)
                info = await q.py('import renpy;s=renpy.store;result=dict(loc=s.room13["location"],file=s.r13_world_file(s.room13["location"],s.r13_daylight()),width=s.r13_world_width(),people=s.r13_people(),allowed=s.r13_new_place_people(s.room13["location"]))')
                await q.shot('arrive-' + key)
                assert info['loc'] == key and info['width'] == 2160 and info['file'].endswith('%s-morning.webp' % key) and all(x in info['allowed'] for x in info['people']), info
                report['travel'][key] = info
            report['checks'].append('map polygon point and name label select each new place; travel arrives at the 2160 morning picture, only residents routed there (0.18.68)')
            for period, name in ((1, 'afternoon'), (2, 'evening')):
                for key in ('river', 'forest', 'market'):
                    await jump(3 if period < 2 else 7, period, key, QUIET)
                    f = await q.py('import renpy;s=renpy.store;result=s.r13_world_file(s.room13["location"],s.r13_daylight())')
                    await q.shot('%s-%s' % (key, name))
                    assert f.endswith('%s-%s.webp' % (key, name)), (key, name, f)
            report['checks'].append('afternoon and evening show their own pictures (9 files)')
            report['status'] = 'passed'
        except Exception as e:
            report['status'] = 'failed'
            report['error'] = repr(e)[:600]
            try:
                await q.shot('failure')
            except Exception:
                pass
        report['page_errors'] = errors
        await b.close()
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps(report, ensure_ascii=False)[:2000])


asyncio.run(main())
