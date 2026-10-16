# Natural start check (0.18.79): the published page opened WITHOUT a query in a fresh browser
# profile, real mouse input only for play (the probe only reads state). Title -> 처음부터 ->
# opening -> gate hub; the gate questions with back, the evidence book with cancel, a wrong
# and the right record, the wait confirm with cancel and accept; save, reload the page and
# load the save from the title. A second run opens the page with WebGL disabled and checks the
# boot guard: the game stops on the first renderer error, the story does not run on and the
# log does not grow. With ROOM13_OLD_DIR (an extracted older preview/room13-dev), a save made
# by that build is loaded by this one in the same profile. Screenshots and report: $ROOM13_QA_OUT/boot.
import asyncio, json, os, sys, time
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

URL = os.environ.get('ROOM13_URL', 'http://localhost:8765/preview/room13-dev/')
OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa')) / 'boot'
OUT.mkdir(parents=True, exist_ok=True)
CHROME = os.environ.get('ROOM13_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
ONLY = os.environ.get('QA_BOOT_ONLY', '')


Q_EXPLAIN = '신청과 이름 목록이 다른 이유를 묻는다'
Q_WAIT = '원본과 다시 맞춰 달라고 한다'


def same_clock(a, b):
    return all(a.get(k) == b.get(k) for k in ('day', 'period', 'location', 'evidence', 'flags'))


async def guard_topics(q):
    st = await q.state()
    if 'r13_entry_topics' not in st['screens']:
        await q.value(('person', 'guard'))
        await q.advance()
        await q.wait('r13_entry_topics')


async def desktop_flow(q, pg, step, report):
    base = (await q.state())['room']
    # Questions open and close without changing anything.
    await guard_topics(q)
    await step('entry-topics')
    await q.press('돌아가기'); await q.advance(); await q.wait('r13_hub')
    assert same_clock((await q.state())['room'], base), 'back changed state'
    await step('entry-back')
    # Ask why the list differs (an ordinary question).
    await guard_topics(q)
    await q.press(Q_EXPLAIN)
    st = await q.advance()
    after = (await q.state())['room']
    assert after['day'] == 1 and after['period'] == 1 and 'entry_corrected' not in after['flags'], after
    await step('explain-answered')
    # Wait: the confirm opens; cancelling leaves time and flags alone.
    await guard_topics(q)
    before = (await q.state())['room']
    await q.press(Q_WAIT); await q.wait('r13_confirm')
    await step('wait-confirm')
    await q.press('돌아간다')
    await q.advance()
    assert same_clock((await q.state())['room'], before), 'wait cancel changed state'
    await step('wait-cancelled')
    # Evidence book: open, close.
    await guard_topics(q)
    before = (await q.state())['room']
    await q.press('보여주기'); await q.wait('r13_book')
    await step('book-open')
    report['book_buttons'] = [x['text'].strip()[:40] for x in (await q.state())['buttons']]
    await q.press('그만두기')
    await q.advance()
    assert same_clock((await q.state())['room'], before), 'book cancel changed state'
    await step('book-cancelled')
    # Wrong record: the travel letter does not settle the entry.
    await guard_topics(q)
    await q.press('보여주기'); await q.wait('r13_book')
    letter = await q.py("import renpy;result=renpy.store.R13_RECORD_SHORT['E01']")
    await q.press(letter)
    await q.press('돌목에게 보여주기')
    await q.advance()
    st = await q.state()
    await step('wrong-record')
    for _ in range(4):
        if 'r13_hub' in st['screens']:
            break
        if 'r13_entry_topics' in st['screens']:
            await q.press('돌아가기')
        elif 'choice' in st['screens']:
            await q.input(640, 300)
        st = await q.advance()
    room = (await q.state())['room']
    assert 'entry_corrected' not in room['flags'] and room['period'] == 1, room
    # The reservation original on the booth shelf: a real click on the shelf in the picture.
    pos = await q.py("import renpy;s=renpy.store;x,y,w,h=s.ROOM13['objects']['gate']['gate_documents']['rect'];o=s.r13_world_offset();result=[x+w/2-o,y+h/2]")
    report['shelf_click'] = pos
    await q.input(*pos)
    await q.advance(); await q.wait('r13_hub')
    room = (await q.state())['room']
    assert 'G1' in room['evidence'], room['evidence']
    await step('documents')
    # Save before the right record.
    await q.press('메뉴'); await asyncio.sleep(1.0)
    report['menu_screens'] = (await q.state())['screens']
    report['menu_buttons'] = [x['text'].strip()[:30] for x in (await q.state())['buttons']]
    await q.press('저장'); await q.wait('save')
    await step('save-screen')
    await q.press('1쪽 1번'); await asyncio.sleep(1.0)
    report['after_slot_buttons'] = [x['text'].strip()[:30] for x in (await q.state())['buttons']]
    for _ in range(3):
        st = await q.state()
        if 'r13_hub' in st['screens'] and not any(n in st['screens'] for n in ('save', 'pause_menu')):
            break
        await q.press('돌아가기'); await asyncio.sleep(.8)
    await q.wait('r13_hub')
    saved = (await q.state())['room']
    await step('saved')
    # Right record: G1 settles the entry, time does not move.
    await guard_topics(q)
    await q.press('보여주기'); await q.wait('r13_book')
    title = await q.py("import renpy;result=renpy.store.R13_RECORD_SHORT['G1']")
    await q.press(title); await q.press('돌목에게 보여주기')
    st = await q.advance()
    if 'choice' in st['screens']:  # older builds asked for the reason
        await step('right-record-choice')
        await q.press('원본에는 두 명'); await q.advance()
    await q.wait('r13_hub')
    room = (await q.state())['room']
    assert 'entry_corrected' in room['flags'] and room['period'] == 1, room
    await step('right-record-done')
    # Reload the page (same browser profile), load slot 1 from the title.
    await pg.reload()
    await pg.wait_for_function("typeof renpy_exec==='function'", timeout=180000)
    await q.wait('main_menu')
    await step('title-after-reload')
    await q.press('불러오기'); await q.wait('load')
    await q.press('1쪽 1번')
    st = await q.state()
    if 'confirm' in st['screens']:
        await q.press('예')
    await q.wait('r13_hub')
    loaded = (await q.state())['room']
    assert loaded == saved, 'loaded state differs from the save'
    await step('loaded')
    # Wait accepted from the loaded save: the guard re-checks the original and the entry is settled
    # (this build does not spend a period on it; the clock is recorded, not changed).
    await guard_topics(q)
    await q.press(Q_WAIT); await q.wait('r13_confirm')
    await q.press('진행한다')
    await q.advance(); await q.wait('r13_hub')
    room = (await q.state())['room']
    assert 'entry_corrected' in room['flags'] and room['day'] == 1, room
    report['wait_accept_clock'] = [room['day'], room['period'], saved['period']]
    await step('wait-accepted')


async def natural(p, report, label, viewport, touch=False):
    b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--enable-unsafe-swiftshader'])
    c = await b.new_context(viewport=viewport, has_touch=touch)
    pg = await c.new_page()
    q = UIQA(pg, OUT)
    q.touch = touch
    logs = []
    pg.on('console', lambda m: logs.append(m.text))
    steps = []

    async def step(name, cond=None):
        st = await q.state()
        await q.shot(label + '-' + name)
        steps.append(dict(name=name, screens=st['screens'], room={k: st['room'].get(k) for k in ('day', 'period', 'location', 'flags', 'evidence')} if st.get('room') else None))
        if cond is not None:
            assert cond(st), (name, st['screens'])
        return st
    try:
        await pg.goto(URL)  # no query string
        await pg.wait_for_function("typeof renpy_exec==='function'", timeout=180000)
        await q.wait('main_menu')
        await step('title', lambda s: 'main_menu' in s['screens'])
        await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')  # reading speed only
        await q.press('처음부터')
        st = await q.advance()
        await step('gate-hub', lambda s: 'r13_hub' in s['screens'] and s['room']['location'] == 'gate' and s['room']['day'] == 1)
        if label == 'desktop':
            await desktop_flow(q, pg, step, report)
        report[label] = dict(status='passed', steps=steps, console_lines=len(logs),
                             errors=[l for l in logs if 'Traceback' in l or 'Error' in l][:5])
    except Exception as e:
        report[label] = dict(status='failed', error=repr(e)[:600], steps=steps, console_lines=len(logs))
        try:
            await q.shot(label + '-failure')
        except Exception:
            pass
    await b.close()


async def old_save(p, report, old_dir):
    """A save written by the previous public build (0.18.68), loaded by this build in the same
    browser profile and origin (the old build is served under /old68/ by request routing)."""
    import mimetypes, tempfile
    prof = tempfile.mkdtemp(prefix='r13prof', dir=str(OUT))
    c = await p.chromium.launch_persistent_context(prof, executable_path=CHROME, args=['--no-sandbox', '--enable-unsafe-swiftshader'], viewport={'width': 1280, 'height': 720})
    base = URL.split('/preview/')[0]

    async def serve(route):
        rel = route.request.url.split('/old68/', 1)[1].split('?')[0]
        f = Path(old_dir) / rel
        if f.is_dir():
            f = f / 'index.html'
        if not f.exists():
            return await route.fulfill(status=404, body='')
        await route.fulfill(status=200, body=f.read_bytes(), headers={'Content-Type': mimetypes.guess_type(str(f))[0] or 'application/octet-stream'})
    await c.route(base + '/old68/**', serve)
    pg = c.pages[0] if c.pages else await c.new_page()
    q = UIQA(pg, OUT)
    logs = []
    pg.on('console', lambda m: logs.append(m.text))
    res = {}
    try:
        await pg.goto(base + '/old68/preview/room13-dev/')
        await pg.wait_for_function("typeof renpy_exec==='function'", timeout=180000)
        await q.wait('main_menu')
        res['old_version'] = await q.py('import renpy;result=renpy.config.version')
        await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
        await q.press('처음부터'); await q.advance(); await q.wait('r13_hub')
        await guard_topics(q); await q.press(Q_EXPLAIN); await q.advance()
        st = await q.state()
        if 'r13_entry_topics' in st['screens']:
            await q.press('돌아가기'); await q.advance()
        await q.wait('r13_hub')
        await q.press('메뉴'); await asyncio.sleep(1.0); await q.press('저장'); await q.wait('save')
        await q.press('1쪽 1번'); await asyncio.sleep(1.0)
        for _ in range(3):
            st = await q.state()
            if 'r13_hub' in st['screens'] and 'save' not in st['screens']:
                break
            await q.press('돌아가기'); await asyncio.sleep(.8)
        saved = (await q.state())['room']
        await q.shot('oldsave-0.18.68-saved')
        await asyncio.sleep(3.0)  # let the save reach IndexedDB
        await pg.goto(URL)
        await pg.wait_for_function("typeof renpy_exec==='function'", timeout=180000)
        await q.wait('main_menu')
        res['new_version'] = await q.py('import renpy;result=renpy.config.version')
        await q.press('불러오기'); await q.wait('load')
        await q.shot('oldsave-new-load-screen')
        await q.press('1쪽 1번')
        st = await q.state()
        if 'confirm' in st['screens']:
            await q.press('예')
        await q.wait('r13_hub')
        loaded = (await q.state())['room']
        # world_art_revisions is refreshed on load when a place's layout changed (0.18.79 changed
        # the slot actions of six places); it only re-centres check marks. Everything else stays.
        res['diff'] = sorted(k for k in set(saved) | set(loaded) if saved.get(k) != loaded.get(k))
        res['art_revision_updated'] = sorted(k for k, v in loaded.get('world_art_revisions', {}).items() if saved.get('world_art_revisions', {}).get(k) != v)
        res['same_state'] = res['diff'] in ([], ['world_art_revisions'])
        await q.shot('oldsave-new-loaded')
        # Play on: the right record settles the entry.
        pos = await q.py("import renpy;s=renpy.store;x,y,w,h=s.ROOM13['objects']['gate']['gate_documents']['rect'];o=s.r13_world_offset();result=[x+w/2-o,y+h/2]")
        await q.input(*pos); await q.advance(); await q.wait('r13_hub')
        await guard_topics(q); await q.press('보여주기'); await q.wait('r13_book')
        await q.press(await q.py("import renpy;result=renpy.store.R13_RECORD_SHORT['G1']")); await q.press('돌목에게 보여주기')
        await q.advance(); await q.wait('r13_hub')
        res['continued'] = 'entry_corrected' in (await q.state())['room']['flags']
        res['status'] = 'passed' if res['same_state'] and res['continued'] else 'failed'
    except Exception as e:
        res.update(status='failed', error=repr(e)[:600])
        try:
            await q.shot('oldsave-failure')
        except Exception:
            pass
    res['errors'] = [l for l in logs if 'Traceback' in l or 'Exception' in l][:5]
    report['oldsave'] = res
    await c.close()


async def nogl(p, report):
    b = await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox', '--disable-3d-apis', '--disable-webgl', '--disable-webgl2'])
    c = await b.new_context(viewport={'width': 1280, 'height': 720})
    pg = await c.new_page()
    logs = []
    pg.on('console', lambda m: logs.append((time.time(), m.text)))
    await pg.goto(URL)
    await asyncio.sleep(75)
    n1 = len(logs)
    await asyncio.sleep(30)
    n2 = len(logs)
    info = await asyncio.wait_for(pg.evaluate("()=>({guard:window.r13BootFailure||null,overlay:!!document.getElementById('r13-boot-failure')})"), 20)
    await pg.screenshot(path=str(OUT / 'nogl-stopped.png'))
    # The retry button reloads the page (a fresh boot; it fails again here because WebGL is off).
    retried = False
    try:
        async with pg.expect_navigation(timeout=15000):
            await pg.click('#r13-boot-failure button >> nth=0', timeout=5000)
        retried = True
    except Exception as e:
        retried = repr(e)[:200]
    syncs = [l for _, l in logs if 'syncfs' in l]
    hub = [l for _, l in logs if 'room13.rpy' in l]
    report['nogl'] = dict(status='passed' if info['overlay'] and n2 == n1 and not hub and retried is True else 'failed', console_after_75s=n1, console_after_105s=n2,
                          syncfs_warnings=len(syncs), story_lines_in_log=len(hub), guard=info['guard'], overlay=info['overlay'], retry_reloads=retried)
    await b.close()


async def main():
    report = {'url': URL}
    async with async_playwright() as p:
        if ONLY in ('', 'desktop'):
            await natural(p, report, 'desktop', {'width': 1280, 'height': 720})
        if ONLY in ('', 'mobile'):
            await natural(p, report, 'mobile', {'width': 844, 'height': 390}, touch=True)
        if os.environ.get('ROOM13_OLD_DIR') and ONLY in ('', 'oldsave'):
            await old_save(p, report, os.environ['ROOM13_OLD_DIR'])
        if ONLY in ('', 'nogl'):
            await nogl(p, report)
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps({k: (v.get('status') if isinstance(v, dict) else v) for k, v in report.items()}, ensure_ascii=False))


asyncio.run(main())
