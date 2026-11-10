"""147 실제 저장 호환과 준비한 2·7일의 현장 조사·선택·왕복·저장을 웹에서 확인한다."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_village147 import run, slot, settings, travel as base_travel, person, finish_topics, click_id, focuses
from qa_novel_adaptation import until, prepare

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/fix148/web'))
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/')


async def hub(q):
    await asyncio.sleep(.8)
    for _ in range(100):
        state=await q.state()
        if 'say' in state['screens']:await q.input(900,610)
        elif 'r13_hub' in state['screens']:
            ready=await run(q,'import renpy;sc=renpy.display.screen.get_screen("r13_hub");result=bool(sc.scope.get("world_ready") and not sc.scope.get("world_moving"))')
            if ready:await asyncio.sleep(.6);return
            await asyncio.sleep(.15)
        else:await asyncio.sleep(.15)
    raise AssertionError(('현장 복귀 실패',state))


async def object_click(q,key):
    await hub(q)
    for _ in range(4):
        await hub(q)
        point=await run(q,'import renpy;s=renpy.store;k='+repr(key)+'\nr=s.r13_object_target_rect(k,s.ROOM13["objects"][s.room13["location"]][k]);result=s.r13_world_to_screen((r[0]+r[2]/2,r[1]+r[3]/2))')
        if 85<point[0]<1190:
            print('물건 좌표',key,point,flush=True)
            await q.input(*point);await asyncio.sleep(.8)
            if 'say' in (await q.state())['screens'] or 'r13_confirm' in (await q.state())['screens']:return
            print('클릭 직후',await run(q,'import renpy;s=renpy.store;result=dict(actions=s.r13_world148_object_actions('+repr(key)+'),visible=s.r13_object_visible(s.ROOM13["objects"][s.room13["location"]]['+repr(key)+']),offset=s.r13_world_offset(),rect=s.ROOM13["objects"][s.room13["location"]]['+repr(key)+']["rect"])'),flush=True)
            await asyncio.sleep(.5)
            continue
        await q.input(48 if point[0]<85 else 1232,276);await asyncio.sleep(1)
    raise AssertionError(('현장 물건 접근 실패',key,point))


async def travel(q,target,region):
    if target!='school':
        return await base_travel(q,target,region)
    before=await run(q,'import renpy;s=renpy.store;result=dict(day=s.room13["day"],period=s.room13["period"],gate=s.room13["v111"]["gate"],evidence=s.room13["evidence"],minutes=s.r13_v111_value("elapsed_minutes"))')
    await q.press('지도');await q.wait('r13_map');await click_id(q,'r13_map_region_'+region)
    for _ in range(5):
        match=next((f for f in await focuses(q) if f['id'] in ('map_name_school','map_building_school') and 110<f['rect'][0]+f['rect'][2]/2<1190 and 125<f['rect'][1]+f['rect'][3]/2<620),None)
        if match:
            x,y,w,h=match['rect'];await q.input(x+w/2,y+h/2);break
        await q.p.keyboard.press('Shift+ArrowUp');await asyncio.sleep(.5)
    else:raise AssertionError('지도를 위로 옮긴 뒤에도 학교를 찾지 못함')
    await click_id(q,'r13_map_travel');await hub(q)
    assert (await q.state())['room']['location']==target
    after=await run(q,'import renpy;s=renpy.store;result=dict(day=s.room13["day"],period=s.room13["period"],gate=s.room13["v111"]["gate"],evidence=s.room13["evidence"],minutes=s.r13_v111_value("elapsed_minutes"))')
    assert before==after,(before,after)


async def enter_wait(q,key):
    await q.py('\n'.join(['import renpy','def qa148_enter(**kwargs):',' import renpy',' s=renpy.store',
        ' renpy.ui.textbutton("검토 현장",clicked=[s.Hide("qa148_enter"),s.Call("r13_v111_wait",'+repr(key)+')],xpos=500,ypos=300,xsize=280,ysize=80)',
        'renpy.exports.define_screen("qa148_enter",qa148_enter,modal="True",zorder="200")',
        'renpy.exports.show_screen("qa148_enter")','renpy.exports.restart_interaction()','result=True']))
    await q.press('검토 현장');await hub(q)


async def shot(q,name):
    await asyncio.sleep(.5);await q.p.screenshot(path=str(OUT/(name+'.png')))
    (OUT/(name+'.json')).write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))


async def note(q,key):
    return await run(q,'import renpy;result=renpy.store.r13_world148_state('+repr(key)+')')


async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=dict(scope='147 수동 저장을 불러온 뒤 2일 우체국과 7일 화재 후 자유 오후를 직접 준비. 이후 현장 물건·주민 질문·선택·지도 왕복·저장 UI 조작. 자연 완주는 아니다.',checks=[])
    async with async_playwright() as p:
        context=await p.chromium.launch_persistent_context(str(OUT/'profile'),executable_path='/usr/bin/chromium',headless=True,
            args=['--no-sandbox','--enable-unsafe-swiftshader'],viewport=dict(width=1280,height=720),has_touch=True)
        page=context.pages[0];q=SayQA(page,OUT);errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu')
            report['version']=await run(q,'import renpy;result=renpy.config.version');assert report['version']=='0.20.148'
            await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q)
            old=json.loads(Path('/tmp/fix147/web/03-도움기억-저장.json').read_text())['room']
            assert (await q.state())['room']==old
            assert not await note(q,'postal')
            report['checks'].append('147 실제 수동 저장 전체 상태 동일·새 조사 기억은 빈 상태')
            await run(q,'import renpy;s=renpy.store;s.preferences.text_cps=0;s.r13_grant(["V111:E07"],"qa148");result=True')
            await prepare(q,2,'post',['daram'],dict(ui_room_arrival_seen=True),'MS14_D02_S03')
            await run(q,'import renpy;renpy.store.r13_edit(period=0);result=True')
            await enter_wait(q,'morning_finish2')
            await object_click(q,'parcels');await hub(q);assert (await note(q,'postal'))['observed']
            await person(q,'seryeon');await q.press('한 묶음으로 오면 보낸 사람도 같습니까?');await until(q,screen='choice')
            await shot(q,'01-우체국-선택');await q.press('도장은 뭘 확인하는 건가요?');await finish_topics(q)
            assert (await note(q,'postal'))['result']=='listen'
            await q.press('돌아가기');await hub(q)
            await click_id(q,'r13_field_quests');await asyncio.sleep(.7);await shot(q,'02-청취-기록')
            await click_id(q,'r13_quest_journal_close');await hub(q)
            report['checks'].append('2일 실제 우편 묶음→세련 질문→듣기 분기→청취 기록')
            values=dict(ui_room_arrival_seen=True,piko_alive=True,FIRE_EVACUATED=True,D06_S03P_empty_fire_completed=True,
                warehouse_children_school_handover=4,KKOMI_ALIVE=True,BORI_hands='not_rescue_burned',
                D07_S02_handover_completed=True,D07_S02_message_completed=True,route7='uncommitted',OWL_ALIVE=True,NUBI_admitted_setting_fire=True,
                **{'meeting:fire':'win'})
            await prepare(q,7,'school',['daram'],values,'MS14_D07_S02')
            await enter_wait(q,'free_day7')
            await object_click(q,'firewood');await hub(q);assert (await note(q,'aftermath'))['observed']
            await shot(q,'03-학교-남은장작')
            await travel(q,'square','village');await person(q,'resident_bori')
            question=await run(q,'import renpy;result=renpy.store.R13_WORLD148["aftermath"]["question"]')
            await q.press(question);await until(q,screen='choice');await shot(q,'04-화재뒤-보리선택')
            help_title=await run(q,'import renpy;result=next(c["title"] for c in renpy.store.R13_WORLD148["aftermath"]["choices"] if c["result"]=="help")')
            await q.press(help_title);await finish_topics(q);await q.press('돌아가기');await hub(q)
            state=await note(q,'aftermath');assert state['result']=='help' and not state.get('worked')
            await travel(q,'school','village');await object_click(q,'firewood');await q.wait('r13_confirm')
            before=(await q.state())['room'];await q.press('나중에 하기');await hub(q)
            assert (await q.state())['room']==before
            await object_click(q,'firewood');await q.wait('r13_confirm')
            task_title=await run(q,'import renpy;result=renpy.store.R13_WORLD148["aftermath"]["task"]["title"]')
            await q.press(task_title);await hub(q)
            assert (await note(q,'aftermath'))['worked']
            await travel(q,'square','village');await person(q,'resident_bori');await q.press(question);await finish_topics(q)
            assert (await note(q,'aftermath'))['report_seen']
            await q.press('돌아가기');await hub(q)
            await click_id(q,'r13_field_quests');await asyncio.sleep(.7);await shot(q,'05-마을이야기')
            await click_id(q,'r13_quest_journal_close');await hub(q)
            await settings(q);await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await q.press('닫기');await hub(q);saved=(await q.state())['room']
            (OUT/'저장상태.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2))
            await page.reload();await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu');await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q);assert (await q.state())['room']==saved
            report['checks'].append('7일 학교 관찰→광장 보리→학교 왕복·행동 취소·실행·전체 저장 복원')
            report.update(status='통과',pageerrors=errors);assert not errors,errors
        except Exception as error:
            report['error']=repr(error)
            try:await shot(q,'오류-진단')
            except Exception:pass
            raise
        finally:
            (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await context.close()
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':asyncio.run(main())
