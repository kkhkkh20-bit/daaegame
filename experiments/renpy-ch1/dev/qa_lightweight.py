"""같은 로컬 서버·통신 조건에서 시작과 입구 비용을 재는 부분 시험."""
import asyncio
import json
import os
import time
from pathlib import Path

from playwright.async_api import async_playwright
from webqa import SayQA

OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-lightweight'))
URL = os.environ.get('ROOM13_URL', 'http://127.0.0.1:8765/preview/room13-dev/')


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport={'width': 1280, 'height': 720}, has_touch=True)
        q = SayQA(page, OUT)
        cdp = await page.context.new_cdp_session(page)
        await cdp.send('Network.enable')
        await cdp.send('Network.setCacheDisabled', {'cacheDisabled': False})
        await cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 20, 'downloadThroughput': 3 * 1024 * 1024, 'uploadThroughput': 1024 * 1024})
        await cdp.send('Performance.enable')
        requests, finished, errors = {}, [], []
        cdp.on('Network.responseReceived', lambda e: requests.update({e['requestId']: e['response']['url']}))
        cdp.on('Network.loadingFinished', lambda e: finished.append({'url': requests.get(e['requestId'], ''), 'bytes': e.get('encodedDataLength', 0)}))
        page.on('pageerror', lambda e: errors.append(str(e)))

        async def sample():
            metrics = {m['name']: m['value'] for m in (await cdp.send('Performance.getMetrics'))['metrics']}
            memory = await q.py('import renpy;result=dict(version=renpy.config.version,image_cache_bytes=renpy.display.im.cache.get_total_size()*4,image_cache_limit_bytes=renpy.display.im.cache.cache_limit*4)')
            memory.update(requests=len(finished), cdp_reported_transfer_bytes=sum(r['bytes'] for r in finished), js_heap_bytes=metrics.get('JSHeapUsedSize'))
            return memory

        try:
            start = time.monotonic()
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')", timeout=240000)
            await q.wait('main_menu')
            ready_s = time.monotonic() - start
            main = await sample()
            await asyncio.sleep(10)
            idle = await sample()
            await page.screenshot(path=str(OUT / '메인.png'))
            print('시작 확인', round(ready_s, 2), main, flush=True)
            (OUT / '시작_측정.json').write_text(json.dumps(dict(ready_s=ready_s,main=main,idle=idle,resources=finished),ensure_ascii=False,indent=2))
            await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
            await q.press('처음부터')
            for _ in range(180):
                state = await q.state()
                if 'r13_hub' in state['screens']:
                    break
                if 'choice' in state['screens']:
                    await q.press('편지를 접는다')
                elif 'r13_cinematic_view' in state['screens']:
                    await q.press('계속')
                else:
                    await q.input(900, 600)
            else:
                raise AssertionError(state)
            await asyncio.sleep(2)
            hub = await sample()
            # 현재 상호작용에서 쓰는 이름표와 현장 인물 결과의 반복 계산 비용. 캐시를 비우거나 게임 상태를 바꾸지 않는다.
            code = 'import renpy,time\ns=renpy.store\nrows=[]\nfor name in ["r13_stage_people","r13_objects_over_actors"]:\n f=getattr(s,name);start=time.perf_counter()\n for i in range(10):f()\n rows.append([name,(time.perf_counter()-start)*1000/10])\nstart=time.perf_counter()\nfor i in range(200):s.r13_asset_path("file:assets/ui-b-options/b_opt_panel.png")\nrows.append(["r13_asset_path",(time.perf_counter()-start)*1000/200])\nresult=rows'
            profile = await q.py('ns={};exec('+repr(code)+',ns);result=ns["result"]')
            await page.screenshot(path=str(OUT / '입구.png'))
            report = dict(scope='빈 캐시의 새 브라우저(실행 중 HTTP 캐시는 허용), 로컬 서버, 3MiB/s·20ms, 한 번 측정. 실제 기기·인터넷 속도 보장 아님. CDP 일부 응답 바이트가 0이어서 해당 합은 실제 전송량 비교에 사용하지 않는다.', ready_s=ready_s, main=main, main_idle_10s=idle, hub=hub, profile_ms=profile, pageerrors=errors, resources=finished)
            assert not errors, errors
            (OUT / '측정.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
            print(json.dumps({k: v for k, v in report.items() if k != 'resources'}, ensure_ascii=False), flush=True)
        finally:
            await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
