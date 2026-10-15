# Browser check (0.18.63): drawer puzzle pictures (ART_REQUEST_01822) in the real web build,
# reached by real clicks: take the three tools, open the drawer, paper -> rubbing -> ruler in the
# groove -> push the panel -> take the magnifier. Screenshots: $ROOM13_QA_OUT/drawer-puzzle.
import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

URL = os.environ.get('ROOM13_URL', 'http://localhost:8765/preview/room13-dev/')
OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa')) / 'drawer-puzzle'
OUT.mkdir(parents=True, exist_ok=True)
STATE = 'import renpy;s=renpy.store;st=s.r13_inspection_state();result=dict(layers=s.r13_drawer_layers(),inv=st["inventory"],paper=st["paper_placed"],rubbing=st["rubbing"],held=st["groove_held"],open=st["compartment_open"])'


async def main():
    report = {'steps': []}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),
                                    args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        c = await b.new_context(viewport={'width': 1280, 'height': 720}, has_touch=True)
        pg = await c.new_page()
        q = UIQA(pg, OUT)
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))

        async def step(name, x=None, y=None, press=None, expect=None):
            if press:
                await q.press(press)
            if x is not None:
                await q.input(x, y)
            await asyncio.sleep(1.0)
            st = await q.py(STATE)
            await q.shot(name)
            report['steps'].append(dict(name=name, state=st))
            if expect:
                assert expect(st), (name, st)
        try:
            await pg.goto(URL)
            await pg.wait_for_function("typeof renpy_exec==='function'", timeout=150000)
            await q.wait('main_menu')
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
            await q.press('처음부터'); await q.advance(); await q.wait('r13_hub')
            await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=1,location="room13",life_poc=True,evidence=["M01","E03"]);s.r13_flag("lodging","entry_corrected");s.r13_upgrade()\n'
                       'def f(**kw):renpy.ui.timer(0.2,action=[renpy.store.Hide("qa_jump"),renpy.store.Jump("r13_field")])\n'
                       'renpy.display.screen.define_screen("qa_jump",f,zorder="200")\nrenpy.exports.show_screen("qa_jump");renpy.exports.restart_interaction();result=True')
            await asyncio.sleep(2.5); await q.advance(); await q.wait('r13_hub')
            # The desk close-up as the room's desk object opens it (label r13_inspect_desk), in a new context.
            await q.py('import renpy\ndef f(**kw):renpy.ui.timer(0.2,action=[renpy.store.Hide("qa_desk"),renpy.store.Function(renpy.exports.call_in_new_context,"r13_inspect_desk")])\n'
                       'renpy.display.screen.define_screen("qa_desk",f,zorder="200")\nrenpy.exports.show_screen("qa_desk");renpy.exports.restart_interaction();result=True')
            # A new context is not in the probe's screen list: wait, then use fixed 1280x720 points.
            await asyncio.sleep(3.0)
            await q.shot('desk')
            for x, y in ((362, 377), (535, 355), (567, 477)):
                await q.input(x, y); await asyncio.sleep(0.6)
            await step('0-drawer-closed', 962, 368, expect=lambda s: s['layers'] == [] and sorted(s['inv']) == ['paper', 'pencil', 'ruler'])
            await q.input(253, 682)  # inventory 1: 얇은 종이
            await step('1-paper', 587, 460, expect=lambda s: s['paper'] and s['layers'] == ['paper'])
            await q.input(253, 682)  # inventory 1 after the paper is used: 짧은 연필
            await step('2-rubbing', 587, 460, expect=lambda s: s['rubbing'] and s['layers'] == ['rubbing'])
            await q.input(487, 682)  # inventory 2: 납작한 자
            await step('3-ruler-in-groove', 963, 528, expect=lambda s: s['held'] and s['layers'] == ['held', 'rubbing'])
            await step('4-open', 958, 300, expect=lambda s: s['open'] and s['layers'] == ['open', 'rubbing'])
            await step('5-magnifier', 926, 340, expect=lambda s: 'magnifier' in s['inv'])
            report['status'] = 'passed'
        except Exception as e:
            report['status'] = 'failed'
            report['error'] = repr(e)[:400]
            try:
                await q.shot('failure')
            except Exception:
                pass
        report['page_errors'] = errors
        await b.close()
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps(report, ensure_ascii=False)[:2500])


asyncio.run(main())
