"""0.18.5 inn lobby/hall chips and guide in the built web release: mouse,
keyboard (Tab/Enter, Escape), 844x390 touch. Explicit day-two lodging fixture."""
import asyncio, json, os, urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa')) / 'inn-v4'; OUT.mkdir(parents=True, exist_ok=True)
URL = os.environ.get('ROOM13_URL', 'http://localhost:8765/preview/room13-dev/')
GUIDE = "import renpy;result=bool(renpy.display.screen.get_screen('r13_inn_guide'))"


async def main():
    report = {'archive_sha256': json.load(urllib.request.urlopen(URL + 'game-transport.json'))['archive_sha256'], 'checks': []}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'), args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        c = await b.new_context(viewport={'width': 1280, 'height': 720}, has_touch=True)
        pg = await c.new_page(); q = UIQA(pg, OUT); errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        try:
            await pg.goto(URL); await pg.wait_for_function("typeof renpy_exec==='function'", timeout=150000); await q.wait('main_menu')
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True'); await q.press('처음부터'); await q.advance(); await q.wait('r13_hub')
            await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="inn");s.r13_flag("entry_corrected","lodging");s.r13_upgrade();w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True')
            await q.input(1220, 50); await q.wait('r13_hub'); before = await q.room(); await q.shot('01-lobby')
            await pg.mouse.move(640 - 0, 614); await asyncio.sleep(.5); await q.shot('02-lobby-hover-upstairs')
            await q.press('안내도'); await asyncio.sleep(1); assert await q.py(GUIDE); await q.shot('03-guide')
            await pg.keyboard.press('Escape'); await asyncio.sleep(1); assert not await q.py(GUIDE); assert await q.room() == before
            report['checks'].append('Guide opens from the lobby and Escape closes it without any state change')
            await q.press('안내도'); await asyncio.sleep(1); await q.press('닫기'); await asyncio.sleep(1); assert not await q.py(GUIDE)
            focus = await q.py("import renpy;f=renpy.display.focus.get_focused();result=str(getattr(f,'id',None)) if f else None")
            report['guide_focus_after_close'] = focus
            await q.press('2층으로'); await q.advance(); await q.wait('r13_hub'); r = await q.room(); assert r['location'] == 'hall' and (r['day'], r['period']) == (before['day'], before['period'])
            await q.shot('04-hall'); report['checks'].append('Lobby chip to hall: zero time cost')
            await pg.set_viewport_size({'width': 844, 'height': 390}); q.touch = True; await asyncio.sleep(1.2)
            await q.shot('05-hall-844x390'); await q.press('안내도'); await asyncio.sleep(1); await q.shot('06-guide-844x390')
            await q.press('닫기'); await asyncio.sleep(1)
            await q.press('1층 로비'); await q.advance(); await q.wait('r13_hub'); assert (await q.room())['location'] == 'inn'; await q.shot('07-lobby-844x390')
            await q.press('주방'); await q.advance(); await q.wait('r13_hub'); assert (await q.room())['location'] == 'kitchen'
            report['checks'].append('844x390 touch: guide open/close, hall->lobby->kitchen chips')
            assert not errors, errors
            report['status'] = 'passed-pending-visual-review'
        except Exception as e:
            report.update(status='failed', error=repr(e)); await pg.screenshot(path=str(OUT / 'failure.png'))
        report['errors'] = errors
        (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)); print(json.dumps(report, ensure_ascii=False), flush=True)
        await b.close()
        if report['status'] == 'failed': raise SystemExit(1)

asyncio.run(main())
