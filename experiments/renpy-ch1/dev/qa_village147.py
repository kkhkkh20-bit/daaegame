"""2일 시작 상태를 준비한 뒤 실제 지도·대화·저장 UI를 검사한다. 자연 완주는 아니다."""
import asyncio
import ast
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_novel_adaptation import jump, until

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/fix147/web'))
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/')


async def run(q,code):
    return await q.py('ns={};exec('+repr(code)+',ns);result=ns.get("result")')


async def focuses(q):
    return await run(q,'import renpy\nresult=[dict(id=str(getattr(f.widget,"id","") or ""),rect=[f.x,f.y,f.w,f.h]) for f in renpy.display.focus.focus_list if f.x is not None and f.w and f.h]')


async def click_id(q,name):
    await asyncio.sleep(.35)
    matches=[f for f in await focuses(q) if f['id']==name and 0<f['rect'][0]+f['rect'][2]/2<1280 and 0<f['rect'][1]+f['rect'][3]/2<720]
    assert matches,('표시된 조작을 찾지 못함',name,await focuses(q))
    x,y,w,h=matches[0]['rect'];await q.input(x+w/2,y+h/2)


async def shot(q,name):
    await asyncio.sleep(.5)
    await q.p.screenshot(path=str(OUT/(name+'.png')))
    (OUT/(name+'.json')).write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))


async def finish_topics(q):
    # 직전 질문 화면이 대사 시작 직전 한 프레임 남아 있는 것을 완료로 세지 않는다.
    await asyncio.sleep(.9)
    for _ in range(100):
        state=await q.state()
        if 'say' in state['screens']:
            await q.input(900,610)
        elif 'r13_topics' in state['screens']:
            await asyncio.sleep(.7);return
        else:await asyncio.sleep(.2)
    raise AssertionError(('질문 화면 복귀 실패',state))


async def travel(q,target,region):
    before=await run(q,'import renpy;s=renpy.store;result=dict(day=s.room13["day"],period=s.room13["period"],scene=s.room13["v111"]["scene"],gate=s.room13["v111"]["gate"],evidence=s.room13["evidence"],minutes=s.r13_v111_value("elapsed_minutes"))')
    await q.press('지도');await q.wait('r13_map')
    await click_id(q,'r13_map_region_'+region)
    for step in range(9):
        items=await focuses(q)
        match=next((f for f in items if f['id'] in ('map_name_'+target,'map_room_'+target,'map_building_'+target) and 110<f['rect'][0]+f['rect'][2]/2<1190 and 100<f['rect'][1]+f['rect'][3]/2<625),None)
        if match:
            x,y,w,h=match['rect'];await q.input(x+w/2,y+h/2);break
        vp=q.p.viewport_size;scale=min(vp['width']/1280,vp['height']/720)
        await q.p.mouse.move((vp['width']-1280*scale)/2+700*scale,(vp['height']-720*scale)/2+350*scale)
        await q.p.mouse.wheel(500 if step<4 else -1000,0)
        await asyncio.sleep(.4)
    else:raise AssertionError(('지도의 장소를 찾지 못함',target,await focuses(q)))
    await click_id(q,'r13_map_travel');await q.wait('r13_hub')
    after=await run(q,'import renpy;s=renpy.store;result=dict(day=s.room13["day"],period=s.room13["period"],scene=s.room13["v111"]["scene"],gate=s.room13["v111"]["gate"],evidence=s.room13["evidence"],minutes=s.r13_v111_value("elapsed_minutes"))')
    assert before==after,(target,before,after)
    assert (await q.state())['room']['location']==target


async def person(q,person_id):
    for _ in range(60):
        ready=await run(q,'import renpy;sc=renpy.display.screen.get_screen("r13_hub");result=bool(sc and sc.scope.get("world_ready") and not sc.scope.get("world_moving"))')
        if ready:break
        await asyncio.sleep(.2)
    assert ready,('현장 입력 준비 실패',person_id)
    for _ in range(3):
        matches=[]
        for button in (await q.state())['buttons']:
            try:value=ast.literal_eval(button.get('value',''))
            except (ValueError,SyntaxError):continue
            x,y,w,h=button['rect']
            if value==('person',person_id) and 10<x+w/2<1270 and 10<y+h/2<710:matches.append(button)
        if matches:
            button=min(matches,key=lambda b:b['rect'][2]*b['rect'][3])
            x,y,w,h=button['rect'];await q.input(x+w/2,y+h/2);await finish_topics(q);return
        point=await run(q,'import renpy;s=renpy.store\nactors=s.r13_stage_people();a=next(a for a in actors if a["person"]=='+repr(person_id)+')\nr=next(r for r in s.r13_actor_nameplates(actors) if r["person"]=='+repr(person_id)+')["rect"];x,y,w,h=r;off=s.r13_world_offset();z=s.r13_field_zoom()\nresult=dict(x=(x+w/2-off)*z,y=(y+h/2)*z,pan=48 if x+w/2<off else 1232)')
        await q.input(point['pan'],276);await asyncio.sleep(1)
    raise AssertionError(('현장 인물 접근 실패',person_id,point))


async def settings(q):
    await click_id(q,'r13_options_gear');await q.press('설정');await q.wait('pause_menu');await q.press('저장')


async def slot(q):
    rows=[f for f in await focuses(q) if 410<=f['rect'][2]<=430 and 65<=f['rect'][3]<=165]
    # 불러오기에서는 빈 슬롯이 비활성이라 포커스 목록에 저장된 칸만 남는다.
    rows.sort(key=lambda f:(f['rect'][1],f['rect'][0]));assert rows,rows
    x,y,w,h=rows[0]['rect'];await q.input(x+w/2,y+h/2)


async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=dict(scope='새 게임 시작 뒤 2일 첫 자유 대기를 직접 준비. 이후 실제 지도·주민·선택·저장 조작. 자연 완주가 아님.',checks=[])
    async with async_playwright() as p:
        context=await p.chromium.launch_persistent_context(str(OUT/'profile'),executable_path='/usr/bin/chromium',headless=True,
            args=['--no-sandbox','--enable-unsafe-swiftshader'],viewport=dict(width=1280,height=720),has_touch=True)
        page=context.pages[0];q=SayQA(page,OUT);errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu');report['version']=await run(q,'import renpy;result=renpy.config.version')
            assert report['version']=='0.20.147',report
            await run(q,'import renpy;renpy.store.preferences.text_cps=0;result=True')
            await q.press('처음부터');await until(q,screen='r13_hub')
            await run(q,'import renpy;s=renpy.store;s.r13_flag("v111:applied:option:sleep1:0","entry_corrected","lodging");s.r13_v111_set("gate_registered",True);s.r13_v111_set("day",2);s.r13_grant(["V111:E01","V111:E06"],"qa147");s.r13_edit(location="square",period=0);s.r13_v111_set("location:daram","square");s.r13_v111_scene("MS14_D02_S01");s.r13_v111_arrive(["daram"]);result=True')
            await jump(q,'r13_v111_lamp_rope');await until(q,screen='r13_hub');await asyncio.sleep(1)
            await travel(q,'post','village');await shot(q,'01-우체국-첫방문')
            await person(q,'resident_owlgp');await q.press('엽서를 쓰시는 중이세요?');await until(q,screen='choice')
            await shot(q,'02-엽서-참여선택');await q.press('안부부터 물어보시면 어떨까요?');await finish_topics(q)
            await q.press('돌아가기');await q.wait('r13_hub')
            assert await run(q,'import renpy;result=renpy.store.r13_visit147_state("postcard").get("result")=="help"')
            report['checks'].append('공공 우체국 실제 지도 이동·엽서 도움·본편 대기 복귀')
            await settings(q);await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await q.press('닫기');await q.wait('r13_hub')
            saved=(await q.state())['room'];await shot(q,'03-도움기억-저장')
            await page.reload();await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu');await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await q.wait('r13_hub');assert (await q.state())['room']==saved
            report['checks'].append('실제 저장 UI·브라우저 재시작·불러오기 후 전체 상태 동일')
            await travel(q,'inn','inn');await shot(q,'04-여관-생활현장')
            await person(q,'resident_tori');await q.press('소매가 걸렸니?');await until(q,screen='choice')
            await page.set_viewport_size(dict(width=844,height=390));q.touch=True
            await shot(q,'05-소매-휴대폰선택')
            await q.press('잠깐 옆에서 볼게요.');await finish_topics(q);await q.press('돌아가기');await q.wait('r13_hub')
            await page.set_viewport_size(dict(width=1280,height=720));q.touch=False
            assert await run(q,'import renpy;result=renpy.store.r13_visit147_state("sleeve").get("result")=="watch"')
            await person(q,'resident_yeoni');await q.press('바느질을 조금 도와드릴까요?');await until(q,screen='choice')
            await q.press('지금은 돕기 어렵겠습니다.');await finish_topics(q);await q.press('돌아가기');await q.wait('r13_hub')
            report['checks'].append('소매 구경·휴대폰 선택·기존 수선 의뢰 별도 거절')
            await travel(q,'clinic','village');await shot(q,'06-진료소-이른방문')
            await travel(q,'school','village');await shot(q,'07-학교-이른방문')
            assert await run(q,'import renpy;s=renpy.store;result=not s.r13_v111_owned("E13") and not s.r13_v111_owned("E16")')
            report['checks'].append('진료소·학교 첫 방문 후 미래 자료 미획득·오전 유지')
            report['state']=(await q.state())['room'];report['pageerrors']=errors;assert not errors,errors
            report['status']='통과'
        except Exception as error:
            report['error']=repr(error)
            try:await shot(q,'오류-진단')
            except Exception:pass
            raise
        finally:
            (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
            await context.close()
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':asyncio.run(main())
