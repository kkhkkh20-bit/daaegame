"""공개판 로딩 시간 측정. 캐시 없는 새 브라우저, CDP 로 네트워크 조건을 건다."""
import asyncio, json, sys, time
sys.path.insert(0, '/home/user/daaegame/experiments/renpy-ch1/dev')
from playwright.async_api import async_playwright
from webqa import UIQA

URL = 'https://kkhkkh20-bit.github.io/daaegame/preview/room13-dev/'
# 이름: (내려받기 kbps, 올리기 kbps, 왕복 지연 ms). None 은 조절 없음(이 컨테이너 회선 그대로).
PROFILES = {
    'none': None,
    '4g_20m': (20000, 5000, 60),
    'slow4g_1.6m': (1600, 750, 150),
}


async def run(pw, name, cond, repeat=False):
    browser = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
    ctx = await browser.new_context(viewport={'width': 1280, 'height': 720}, service_workers=('block' if cond else 'allow'))
    pg = await ctx.new_page()
    cdp = await ctx.new_cdp_session(pg)
    await cdp.send('Network.enable')
    if cond:
        down, up, lat = cond
        await cdp.send('Network.emulateNetworkConditions', dict(offline=False, latency=lat,
            downloadThroughput=down * 1000 / 8, uploadThroughput=up * 1000 / 8))
    total = {'bytes': 0, 'n': 0}
    def fin(e):
        total['bytes'] += e.get('encodedDataLength', 0); total['n'] += 1
    cdp.on('Network.loadingFinished', fin)
    marks = {}
    rounds = 2 if repeat else 1
    for r in range(rounds):
        total['bytes'] = 0; total['n'] = 0
        t0 = time.monotonic()
        await pg.goto(URL, wait_until='domcontentloaded', timeout=900000)
        m = {'html': time.monotonic() - t0}
        await pg.wait_for_function("typeof renpy_exec==='function'", timeout=900000, polling=200)
        m['engine'] = time.monotonic() - t0
        q = UIQA(pg, None)
        clicks = 0
        while True:
            try:
                st = await q.py('import renpy;result=[n for n in ("main_menu","say","_exception") if renpy.display.screen.get_screen(n)]')
            except Exception:
                st = []
            if 'main_menu' in st:
                break
            if time.monotonic() - t0 > 900:
                m['menu'] = None; break
            # 시작 화면이 클릭을 기다리면 한 번 누른다(사람도 누른다). 누른 횟수를 같이 적는다.
            if time.monotonic() - m['engine'] > 3 and clicks < 20:
                await pg.mouse.click(1100, 600); clicks += 1
            await asyncio.sleep(.5)
        m.setdefault('menu', time.monotonic() - t0)
        m['clicks_before_menu'] = clicks
        m['bytes_to_menu'] = total['bytes']
        # 「처음부터」 → 첫 대사
        t1 = time.monotonic()
        try:
            await q.press('처음부터')
            while time.monotonic() - t1 < 600:
                st = await q.py('import renpy;result=[n for n in ("say","r13_cinematic_view","choice","r13_hub","_exception") if renpy.display.screen.get_screen(n)]')
                if st:
                    m['first_screen'] = st; break
                await asyncio.sleep(.3)
            m['menu_to_first'] = time.monotonic() - t1
        except Exception as e:
            m['first_err'] = str(e)[:200]
        m['bytes_total'] = total['bytes']; m['requests'] = total['n']
        await pg.screenshot(path='/tmp/claude-0/-home-user/e8c4e0c2-3da8-5349-b9af-6a9743c98000/scratchpad/load_%s_%d.png' % (name, r))
        marks['visit%d' % (r + 1)] = m
        print(name, r + 1, json.dumps(m, ensure_ascii=False), flush=True)
    await browser.close()
    return marks


async def main():
    names = sys.argv[1:] or list(PROFILES)
    out = {}
    async with async_playwright() as pw:
        for n in names:
            out[n] = await run(pw, n, PROFILES[n], repeat=(n == 'none'))
    print(json.dumps(out, ensure_ascii=False, indent=1))

asyncio.run(main())
