"""최종 전송 묶음에서 앞서 만든 실제 저장을 열고 모바일 선택 화면을 검사한다."""
import asyncio
import base64
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_village147 import run, slot, travel, person, finish_topics
from qa_novel_adaptation import until

ROOT=Path('/tmp/fix147')
OUT=ROOT/'web-final'


async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=dict(scope='앞선 147 웹 검수의 실제 수동 저장을 최종 묶음에서 불러온 뒤 모바일 선택. 자연 완주가 아니다.')
    async with async_playwright() as p:
        context=await p.chromium.launch_persistent_context(str(ROOT/'web/profile'),executable_path='/usr/bin/chromium',headless=True,
            args=['--no-sandbox','--enable-unsafe-swiftshader'],viewport=dict(width=844,height=390),has_touch=True,is_mobile=True,
            user_agent='Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36')
        page=context.pages[0];q=SayQA(page,OUT);q.touch=True;errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        try:
            await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/?v=0.20.147'))
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu')
            report['version']=await run(q,'import renpy;result=renpy.config.version');assert report['version']=='0.20.147'
            await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await q.wait('r13_hub');await asyncio.sleep(1)
            saved=json.loads((ROOT/'web/03-도움기억-저장.json').read_text())['room']
            assert (await q.state())['room']==saved
            report['restored_entire_room']=True
            await page.screenshot(path=str(OUT/'01-최종묶음-저장복원.png'))
            exported=await run(q,'import os,base64,renpy\np=os.path.join(renpy.config.savedir,"1-1.save") if renpy.config.savedir else ""\nresult=dict(exists=os.path.isfile(p),data=base64.b64encode(open(p,"rb").read()).decode("ascii") if os.path.isfile(p) else None)')
            if exported['exists']:
                folder=Path('/workspace/work/fix147/saves');folder.mkdir(parents=True,exist_ok=True)
                (folder/'QA147-2일-엽서도움.save').write_bytes(base64.b64decode(exported['data']))
            report['qa_save_exported']=exported['exists']
            await travel(q,'inn','inn');await person(q,'resident_tori');await q.press('소매가 걸렸니?');await until(q,screen='choice')
            await asyncio.sleep(.7)
            report['touch_mode']=await run(q,'import renpy;result=renpy.store.r13_touch_ui()')
            state=await q.state();captions=await run(q,'import renpy;result=[r["title"] for r in renpy.store.R13_VISITS147["sleeve"]["choices"]]')
            choices=[button for button in state['buttons'] if any(text in button['text'] for text in captions)]
            assert len(choices)==3,choices
            scale=min(844/1280,390/720)
            report['choice_css_heights']=[round(button['rect'][3]*scale,2) for button in choices]
            if report['touch_mode']:assert min(report['choice_css_heights'])>=44,report
            await page.screenshot(path=str(OUT/'02-실제모바일설정-생활선택.png'))
            await q.press('지금은 도와드리기 어렵겠어요.');await finish_topics(q)
            assert await run(q,'import renpy;result=renpy.store.r13_visit147_state("sleeve").get("result")=="decline"')
            report.update(status='통과',pageerrors=errors);assert not errors,errors
        except Exception as error:
            report['error']=repr(error)
            try:await page.screenshot(path=str(OUT/'오류.png'))
            except Exception:pass
            raise
        finally:
            (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
            await context.close()
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':asyncio.run(main())
