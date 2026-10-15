"""0.18.5 full-body dialogue portraits in the built web release (real browser input).

Natural start: carriage (Daram) -> gate -> Karo topic list -> Karo dialogue line,
save during the line, advance, load, large text and 844x390 touch. Every check
records which full-body file the conversation partner uses and the on-screen
bounds of the portrait. Run from experiments/renpy-ch1 with the repository root
served on :8765 (see ROOM13_GUIDE.md).
"""
import asyncio, json, os, urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa')) / 'fullbody-web'; OUT.mkdir(parents=True, exist_ok=True)
URL = os.environ.get('ROOM13_URL', 'http://localhost:8765/preview/room13-dev/')
PORTRAIT = ("import renpy;s=renpy.store;who=s.r13_motion_person;spec=s.r13_fullbody_spec(who,s.r13_current_pose) if who else None;"
            "b=renpy.exports.get_image_bounds('r13_visitor') if 'r13_visitor' in renpy.exports.get_showing_tags() else None;"
            "result={'who':who,'pose':s.r13_current_pose,'file':(spec or {}).get('file'),'bounds':b,'large':s.persistent.room13_large_text}")


async def main():
    report = {'archive_sha256': json.load(urllib.request.urlopen(URL + 'game-transport.json'))['archive_sha256'], 'checks': []}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'), args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        c = await b.new_context(viewport={'width': 1280, 'height': 720}, has_touch=True)
        pg = await c.new_page(); q = UIQA(pg, OUT); errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        try:
            await pg.goto(URL); await pg.wait_for_function("typeof renpy_exec==='function'", timeout=150000); await q.wait('main_menu')
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
            await q.press('처음부터'); await q.wait('say'); await asyncio.sleep(1.2)
            first = None
            for _ in range(12):
                info = await q.py(PORTRAIT)
                if info['who'] == 'daram' and info['bounds']:
                    first = info; break
                await q.input(810, 610); await asyncio.sleep(.8)
            assert first and first['file'] and 'room13-fullbody-daram-' in first['file'], first
            await q.shot('01-carriage-daram'); report['carriage'] = first
            report['checks'].append('Carriage: Daram is drawn from the full-body set')
            await q.advance(); await q.wait('r13_hub')
            await q.press('까로'); await asyncio.sleep(1.5); await q.shot('02-karo-topics')
            st = await q.state(); report['topic_screens'] = st['screens']
            # Ask the first available question; Karo answers in dialogue.
            topic = await q.py("import renpy;s=renpy.store;names=[n for n in ('r13_entry_karo_topics','r13_topics','r13_entry_topics') if renpy.display.screen.get_screen(n)];result=names")
            report['topic_screen'] = topic
            await q.press('마차가 괜찮은지')
            line = None
            for _ in range(20):
                await asyncio.sleep(.6); st = await q.state()
                if 'say' in st['screens']:
                    info = await q.py(PORTRAIT)
                    if info['who'] == 'karo' and info['bounds']:
                        line = info; break
                    await q.input(810, 610)
                elif 'choice' in st['screens']:
                    await q.input(640, 300)
            assert line and 'room13-fullbody-karo-' in (line['file'] or ''), line
            await q.shot('03-karo-line'); report['karo_line'] = line
            await q.say_save(1); saved = await q.py(PORTRAIT); assert saved == line, (saved, line)
            await q.input(810, 610); await asyncio.sleep(1)
            await q.say_load(1); await asyncio.sleep(1.2); loaded = await q.py(PORTRAIT)
            assert (loaded['who'], loaded['file'], loaded['bounds']) == (line['who'], line['file'], line['bounds']), (loaded, line)
            await q.shot('04-karo-loaded'); report['checks'].append('Save during a Karo line, advance, load: same full-body file and identical portrait bounds')
            await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True'); await asyncio.sleep(1)
            await q.shot('05-large-text'); report['large'] = await q.py(PORTRAIT)
            await pg.set_viewport_size({'width': 844, 'height': 390}); q.touch = True; await asyncio.sleep(1.2)
            await q.shot('06-mobile-landscape-large'); report['mobile'] = await q.py(PORTRAIT)
            await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;renpy.exports.restart_interaction();result=True')
            report['checks'].append('Large text and 844x390 touch viewport screenshots recorded for visual review')
            assert not errors, errors
            report['status'] = 'passed-pending-visual-review'
        except Exception as e:
            report.update(status='failed', error=repr(e)); await pg.screenshot(path=str(OUT / 'failure.png'))
            try: (OUT / 'failure-state.json').write_text(json.dumps(await q.state(), ensure_ascii=False, indent=2))
            except Exception: pass
        report['errors'] = errors
        (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)); print(json.dumps(report, ensure_ascii=False), flush=True)
        await b.close()
        if report['status'] == 'failed': raise SystemExit(1)

asyncio.run(main())
