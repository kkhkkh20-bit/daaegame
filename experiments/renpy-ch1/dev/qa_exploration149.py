"""148 실제 저장 호환 뒤 준비한 2일의 무상 조달·현장 사용·원래 등 고정을 조작한다."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_village147 import run, person, finish_topics, click_id, settings, slot, focuses
from qa_world148 import hub, enter_wait
from qa_novel_adaptation import prepare, jump

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/fix149/web'))
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/?v=0.20.149')

async def screen(q,name):
    return await run(q,'import renpy;result=bool(renpy.display.screen.get_screen('+repr(name)+'))')

async def reach(q,name):
    await asyncio.sleep(.5)
    for _ in range(130):
        state=await q.state()
        assert '_exception' not in state['screens'],state
        if 'say' in state['screens']:
            await q.input(900,610)
        elif await screen(q,name):
            await asyncio.sleep(.5);return
        else:await asyncio.sleep(.15)
    raise AssertionError(('화면 도착 실패',name,await q.state()))

async def shot(q,name):
    await asyncio.sleep(.5);await q.p.screenshot(path=str(OUT/(name+'.png')))

async def state(q):
    return await run(q,'import renpy;s=renpy.store;result=dict(note=s.r13_ex149_state(),items=s.r13_wallet(s.room13)["items"],borrowed=s.r13_wallet(s.room13)["borrowed"],bound=s.r13_v111_value("lamp_bound2"),money_keys={k:v for k,v in s.room13.get("livelihood",{}).items() if k in ("cash","debt")})')

async def obj(q,key):
    await hub(q)
    for _ in range(4):
        point=await run(q,'import renpy;s=renpy.store;k='+repr(key)+';r=s.r13_object_target_rect(k,s.ROOM13["objects"][s.room13["location"]][k]);result=s.r13_world_to_screen((r[0]+r[2]/2,r[1]+r[3]/2))')
        if 85<point[0]<1190:
            await q.input(*point);await asyncio.sleep(.6);return
        await q.input(48 if point[0]<85 else 1232,276);await asyncio.sleep(1);await hub(q)
    raise AssertionError(('현장 물건 접근 실패',key,point))

async def travel(q,target,region):
    before=await run(q,'import renpy;s=renpy.store;result=[s.room13["day"],s.room13["period"],s.room13["v111"]["gate"],s.room13["evidence"],s.r13_v111_value("elapsed_minutes")]')
    await q.press('지도');await q.wait('r13_map');await click_id(q,'r13_map_region_'+region)
    for _ in range(12):
        match=next((f for f in await focuses(q) if f['id']=='map_name_'+target and 110<f['rect'][0]+f['rect'][2]/2<1190 and 140<f['rect'][1]+f['rect'][3]/2<615),None)
        if match:
            x,y,w,h=match['rect'];await q.input(x+w/2,y+h/2);break
        point=await run(q,'import renpy;s=renpy.store;v=renpy.exports.get_widget("r13_map","r13_map_view");z=renpy.display.screen.get_screen("r13_map").scope.get("village_zoom",1.0);x,y=s.R13_VILLAGE_B_PLACES['+repr(target)+']["label_center"];result=[88+x*z-v.xadjustment.value,122+y*z-v.yadjustment.value]')
        key='Left' if point[0]<110 else 'Right' if point[0]>1190 else 'Up' if point[1]<140 else 'Down'
        await q.p.keyboard.press('Shift+Arrow'+key);await asyncio.sleep(.6)
    else:raise AssertionError(('지도 이동 실패',target,point))
    await click_id(q,'r13_map_travel');await hub(q)
    after=await run(q,'import renpy;s=renpy.store;result=[s.room13["day"],s.room13["period"],s.room13["v111"]["gate"],s.room13["evidence"],s.r13_v111_value("elapsed_minutes")]')
    assert before==after and (await q.state())['room']['location']==target,(before,after,target)

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=dict(scope='148 실제 수동 저장 호환 확인 뒤 2일 오전·오후·밤을 직접 준비. 나머지는 실제 지도·물품·주민·확인창 조작. 자연 완주 아님.',checks=[])
    async with async_playwright() as p:
        context=await p.chromium.launch_persistent_context(str(OUT/'profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader'],viewport=dict(width=1280,height=720),has_touch=True)
        page=context.pages[0];q=SayQA(page,OUT);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu');report['version']=await run(q,'import renpy;result=renpy.config.version');assert report['version']=='0.20.149'
            await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q)
            old=json.loads(Path('/tmp/fix148/web/저장상태.json').read_text());assert (await q.state())['room']==old
            report['checks'].append('148 실제 수동 저장 전체 상태 동일')
            await run(q,'import renpy;s=renpy.store;s.preferences.text_cps=0;s.room13.pop("livelihood",None);s.room13["v111"].pop("exploration149",None);s.r13_ex149_held=None;result=True')
            await prepare(q,2,'market',['daram'],dict(ui_room_arrival_seen=True),'MS14_D02_S03')
            await run(q,'import renpy;renpy.store.r13_edit(period=0);result=True');await enter_wait(q,'morning_finish2')
            await person(q,'resident_eunho');await q.press('묶음끈과 표준추를 쓸 수 있을까요?');await reach(q,'r13_ex149_shop')
            await shot(q,'01-돈없는-물품조달')
            for item in ('cord','weight'):
                await click_id(q,'ex149_receive_'+item);await reach(q,'r13_ex149_shop')
            current=await state(q);assert current['items']==['cord','weight'] and not current['money_keys'],current
            await click_id(q,'ex149_shop_back');await finish_topics(q);await q.press('돌아가기');await hub(q)
            await travel(q,'gate','village');await hub(q);await person(q,'karo');await q.press('수레 옆의 두 짐을 살펴봐도 될까요?');await reach(q,'r13_ex149_closeup')
            for key in ('large_tag','small_tag','box'):
                await click_id(q,'ex149_look_'+key);await reach(q,'r13_ex149_closeup')
            await click_id(q,'ex149_tie');await reach(q,'choice');await shot(q,'02-짐-옮기는-방법')
            await q.press('작은 상자를 큰 상자 위에 그냥 얹는다');await reach(q,'r13_ex149_closeup');assert not (await state(q))['note'].get('delivery_tied')
            await click_id(q,'ex149_tie');await reach(q,'choice');await q.press('두 상자를 겹쳐 끈으로 묶는다');await reach(q,'r13_confirm');await q.press('더 살펴보기');await reach(q,'r13_ex149_closeup');assert not (await state(q))['note'].get('delivery_tied')
            await click_id(q,'ex149_tie');await reach(q,'choice');await q.press('두 상자를 겹쳐 끈으로 묶는다');await reach(q,'r13_confirm');await q.press('두 짐 묶기');await reach(q,'r13_ex149_closeup')
            await shot(q,'03-실제-묶은-짐')
            assert not (await state(q))['note'].get('knot_method')
            await click_id(q,'ex149_report_delivery');await reach(q,'r13_ex149_closeup');assert (await state(q))['note']['knot_method']
            await click_id(q,'ex149_closeup_back');await finish_topics(q);await q.press('돌아가기');await hub(q)
            report['checks'].append('두 짐표·밑면 관찰→잘못 얹기·재선택→묶기 취소·실행→실제 까로 확인으로 방법 습득')
            await travel(q,'store','village');await hub(q);await click_id(q,'r13_field_items149');await reach(q,'r13_ex149_bag');await click_id(q,'ex149_select_weight');await hub(q);await obj(q,'scale');await reach(q,'r13_ex149_closeup');await click_id(q,'ex149_look_pivot');await reach(q,'r13_ex149_closeup')
            await shot(q,'04-추로-저울-확인');await click_id(q,'ex149_closeup_back');await hub(q)
            assert 'weight' in (await state(q))['items']
            await run(q,'import renpy;renpy.store.r13_edit(period=1);result=True');await hub(q)
            await person(q,'resident_eunho');await q.press('표준추를 올려 봤는데, 함께 다시 재 주시겠어요?');await finish_topics(q)
            assert (await state(q))['note']['scale_corrected']
            await q.press('빌린 표준추를 돌려드리겠습니다.');await finish_topics(q)
            assert 'weight' not in (await state(q))['items'] and not (await state(q))['borrowed']
            await q.press('돌아가기');await hub(q);report['checks'].append('표준추 실제 현장 사용·회수→오후 은호와 빈 접시부터 재확인→실제 반납, 돈 생성 없음')
            (OUT/'오후검증-상태.json').write_text(json.dumps((await q.state())['room'],ensure_ascii=False,indent=2))
            await prepare(q,2,'square',['daram'],dict(ui_room_arrival_seen=True,lamp_latch_seen2=None,lamp_cord2=None,lamp_bound2=None,D02_afternoon="nero",selected_afternoon_work_completed=True,piko_sheltered=False),'MS14_D02_S05')
            await run(q,'import renpy;renpy.store.r13_edit(period=2);result=True');await jump(q,'r13_lamp_prep2');await hub(q)
            await obj(q,'lamp');await hub(q);assert await run(q,'import renpy;result=renpy.store.r13_v111_value("lamp_latch_seen2") is True')
            await click_id(q,'r13_field_items149');await reach(q,'r13_ex149_bag');await click_id(q,'ex149_select_cord');await hub(q);await obj(q,'lamp');await reach(q,'r13_confirm')
            await shot(q,'05-다른현장-물품사용');await q.press('더 살펴보기');await hub(q);assert not (await state(q))['bound'] and 'cord' in (await state(q))['items']
            await obj(q,'lamp');await reach(q,'r13_confirm');await q.press('걸쇠 고정하기');await hub(q)
            current=await state(q);assert current['bound'] and 'cord' not in current['items'] and not current['money_keys'],current
            report['checks'].append('실제 걸쇠 관찰→다른 곳에서 얻은 방법·끈 사용→취소 무변이→기존 본편 lamp_bound2와 끈 소모')
            await click_id(q,'r13_field_items149');await reach(q,'r13_ex149_bag');await click_id(q,'ex149_notes');await reach(q,'r13_ex149_notes');await shot(q,'06-알게된-방법');await click_id(q,'ex149_notes_back');await reach(q,'r13_ex149_bag');await click_id(q,'ex149_bag_back');await hub(q)
            saved=(await q.state())['room'];(OUT/'저장상태.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2));await settings(q);await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await q.press('닫기');await hub(q)
            await page.reload();await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000);await q.wait('main_menu');await q.press('설정');await q.wait('pause_menu');await q.press('불러오기');await slot(q)
            if 'confirm' in (await q.state())['screens']:await q.press('예')
            await hub(q);assert (await q.state())['room']==saved
            report.update(status='통과',pageerrors=errors,state=current);assert not errors,errors
        except Exception as error:
            report['error']=repr(error)
            try:(OUT/'오류상태.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
            except Exception:pass
            try:await shot(q,'오류')
            except Exception:pass
            raise
        finally:
            (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await context.close()
    print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':asyncio.run(main())
