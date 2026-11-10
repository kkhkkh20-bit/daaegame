"""실제 물품·등 고정 조작에서 내보낸 상태로 저장 UI 검수를 재개한다."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_village147 import run,slot,settings
from qa_world148 import hub,enter_wait

ROOT=Path('/tmp/fix149');OUT=ROOT/'web'
async def main():
    expected=json.loads((OUT/'저장상태.json').read_text());report=dict(scope='앞서 실제 물품·추·등 고정 조작으로 얻어 내보낸 상태를 다시 준비하여, 덮어쓰기 확인·브라우저 재시작·불러오기를 실제 UI로 검수. 연속 자연 완주 아님.')
    async with async_playwright() as p:
        context=await p.chromium.launch_persistent_context(str(OUT/'profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader'],viewport=dict(width=1280,height=720),has_touch=True)
        page=context.pages[0];q=SayQA(page,OUT);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            url='http://127.0.0.1:8765/preview/room13-dev/?v=0.20.149'
            await page.goto(url);await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000);await q.wait('main_menu')
            await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q)
            await run(q,'import renpy,json;s=renpy.store;s.room13=json.loads('+repr(json.dumps(expected,ensure_ascii=False))+');s.r13_ex149_held=None;s.place=s.R13_PLACES[s.room13["location"]][0];s.r13_scene_bg=s.R13_PLACES[s.room13["location"]][1];renpy.exports.scene();renpy.exports.show("novel_background",what=s.r13_background(s.r13_scene_bg));result=True')
            await enter_wait(q,expected['v111']['gate']);assert (await q.state())['room']==expected
            await settings(q);await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await q.press('닫기');await hub(q)
            await page.reload();await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000);await q.wait('main_menu');await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q);assert (await q.state())['room']==expected
            await page.screenshot(path=str(OUT/'07-브라우저재시작-복원.png'));assert not errors,errors
            report.update(status='통과',whole_state_restored=True,pageerrors=errors)
        except Exception as e:
            report['error']=repr(e)
            try:await page.screenshot(path=str(OUT/'저장오류.png'))
            except Exception:pass
            raise
        finally:
            (OUT/'저장-결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await context.close()
    print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':asyncio.run(main())
