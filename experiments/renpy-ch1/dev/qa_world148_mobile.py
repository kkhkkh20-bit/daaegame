"""실제 Android 브라우저 설정에서 저장 복원과 마을 이야기 쪽 넘김을 확인한다."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_village147 import run, slot, click_id, focuses
from qa_world148 import hub

ROOT=Path('/tmp/fix148')
OUT=ROOT/'web-mobile'


async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=dict(scope='앞선 준비 경로의 실제 수동 저장을 Android 844×390 설정에서 복원하고 기록 UI 조작. 자연 완주는 아니다.')
    async with async_playwright() as p:
        context=await p.chromium.launch_persistent_context(str(ROOT/'web/profile'),executable_path='/usr/bin/chromium',headless=True,
            args=['--no-sandbox','--enable-unsafe-swiftshader'],viewport=dict(width=844,height=390),has_touch=True,is_mobile=True,
            user_agent='Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36')
        page=context.pages[0];q=SayQA(page,OUT);q.touch=True;errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        try:
            await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/?v=0.20.148'))
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu');report['version']=await run(q,'import renpy;result=renpy.config.version');assert report['version']=='0.20.148'
            await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q)
            expected=json.loads((ROOT/'web/저장상태.json').read_text());assert (await q.state())['room']==expected
            report['entire_saved_state_restored']=True
            report['touch_mode']=await run(q,'import renpy;result=renpy.store.r13_touch_ui()');assert report['touch_mode']
            await click_id(q,'r13_field_quests');await asyncio.sleep(.7)
            info=await run(q,'import renpy;sc=renpy.display.screen.get_screen("r13_sidequest_journal146");result={k:sc.scope[k] for k in ("section","page","per_page","pages")}')
            assert info['section']=='world' and info['per_page']==1 and info['pages']==2,info
            await page.screenshot(path=str(OUT/'01-마을이야기-첫쪽.png'))
            buttons=[f for f in await focuses(q) if f['id'] in ('r13_world148_quests','r13_world148_notes','r13_quest_journal_close','r13_quest_journal_next')]
            scale=min(844/1280,390/720);heights=[round(f['rect'][3]*scale,2) for f in buttons]
            assert len(heights)==4 and min(heights)>=44,heights
            report['control_css_heights']=heights
            await click_id(q,'r13_quest_journal_next');await asyncio.sleep(.7)
            assert await run(q,'import renpy;result=renpy.display.screen.get_screen("r13_sidequest_journal146").scope["page"]==1')
            await page.screenshot(path=str(OUT/'02-화재뒤-기록.png'))
            await click_id(q,'r13_world148_quests');await asyncio.sleep(.5)
            assert await run(q,'import renpy;result=renpy.display.screen.get_screen("r13_sidequest_journal146").scope["section"]=="quests"')
            await click_id(q,'r13_world148_notes');await asyncio.sleep(.5)
            assert await run(q,'import renpy;result=renpy.display.screen.get_screen("r13_sidequest_journal146").scope["page"]==0')
            await click_id(q,'r13_quest_journal_close');await hub(q)
            assert (await q.state())['room']==expected
            report.update(status='통과',pageerrors=errors);assert not errors,errors
        except Exception as error:
            report['error']=repr(error)
            try:await page.screenshot(path=str(OUT/'오류.png'))
            except Exception:pass
            raise
        finally:
            (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await context.close()
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':asyncio.run(main())
