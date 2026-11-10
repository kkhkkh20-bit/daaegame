"""실제 Android 설정에서 149 저장 전체 복원과 물품/배운 방법 화면을 터치한다."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_village147 import run,slot,click_id,focuses
from qa_world148 import hub
from qa_exploration149 import reach

ROOT=Path('/tmp/fix149');OUT=ROOT/'web-mobile'

async def main():
    OUT.mkdir(exist_ok=True);report=dict(scope='앞선 준비 경로의 수동 저장을 실제 Android 844×390 설정으로 복원. 물품·방법·돌아가기 터치. 자연 완주 아님.')
    async with async_playwright() as p:
        context=await p.chromium.launch_persistent_context(str(ROOT/'web/profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader'],viewport=dict(width=844,height=390),has_touch=True,is_mobile=True,user_agent='Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36')
        page=context.pages[0];q=SayQA(page,OUT);q.touch=True;errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/?v=0.20.149'));await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu');await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q);saved=json.loads((ROOT/'web/저장상태.json').read_text());assert (await q.state())['room']==saved
            assert await run(q,'import renpy;result=renpy.store.r13_touch_ui()')
            await run(q,'import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
            await click_id(q,'r13_field_items149');await reach(q,'r13_ex149_bag');await page.screenshot(path=str(OUT/'01-물품-큰글씨.png'))
            rows=[f for f in await focuses(q) if f['id'] in ('ex149_bag_back','ex149_notes')];assert len(rows)==2,rows
            scale=min(844/1280,390/720);heights=[round(row['rect'][3]*scale,2) for row in rows];assert min(heights)>=44,heights
            await click_id(q,'ex149_notes');await reach(q,'r13_ex149_notes');await page.screenshot(path=str(OUT/'02-배운방법-큰글씨.png'))
            await click_id(q,'ex149_notes_back');await reach(q,'r13_ex149_bag');await click_id(q,'ex149_bag_back');await hub(q)
            assert (await q.state())['room']==saved;assert not errors,errors
            report.update(status='통과',whole_save_restored=True,control_css_heights=heights,pageerrors=errors)
        except Exception as error:
            report['error']=repr(error)
            try:await page.screenshot(path=str(OUT/'오류.png'))
            except Exception:pass
            raise
        finally:
            (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await context.close()
    print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':asyncio.run(main())
