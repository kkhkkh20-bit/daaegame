"""실제 시작→편지→입구 UI + 명시적 화면 fixture로 질문·설정·이름표 검증.

renpy_exec는 읽기 전용 계측과 설정 값 변경, 질문/메모 화면 fixture에 쓴다.
첫 입실·메모 구간은 선행 상태/라벨 fixture로 진입하며 실제 연속 진행으로 주장하지 않는다.
외부에서 준비한 ROOM13_URL을 사용하며 서버를 실행하지 않는다.
"""
import asyncio
import json
import os
import traceback
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa/play-review-field'))
URL = os.environ.get('ROOM13_URL', 'http://127.0.0.1:8765/preview/room13-dev/')
SIZES = [('pc',1280,720),('phone',844,390),('small-phone',740,360)]
OUT.mkdir(parents=True, exist_ok=True)
MATRIX_SIZES = SIZES


class FieldQA(UIQA):
    async def py(self, code):
        wrapped='ns={};exec('+ascii(code)+',ns);result=ns.get("result")'
        return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(wrapped)+')'),120)

    async def jump_fixture(self, label):
        await self.py('import renpy\ndef qa_review_jump(**kw):\n renpy.ui.textbutton("검토 계속",clicked=renpy.store.Jump('+repr(label)+'),xpos=500,ypos=300,xsize=280,ysize=88)\nrenpy.exports.define_screen("qa_review_jump",qa_review_jump,modal="True",zorder="200")\nrenpy.exports.show_screen("qa_review_jump");renpy.exports.restart_interaction();result=True')
        await self.press('검토 계속')
        await self.py('import renpy;renpy.exports.hide_screen("qa_review_jump");renpy.exports.restart_interaction();result=True')

    async def advance_until(self, screen, limit=500):
        for _ in range(limit):
            state = await self.state()
            if screen in state['screens']:
                await asyncio.sleep(.6)
                return state
            if 'choice' in state['screens']:
                raise AssertionError(('예상하지 않은 선택 화면',screen,state))
            if 'r13_arrival_card' in state['screens']:
                await self.input(800,400)
            elif 'r13_cinematic_view' in state['screens']:
                await self.press('계속')
            elif 'say' in state['screens']:
                await self.input(640,610)
            else:
                await asyncio.sleep(.2)
        raise AssertionError(('화면 진입 시간 초과',screen,state))

    async def setting_fixture(self, width, height, large):
        await self.p.set_viewport_size(dict(width=width,height=height))
        self.touch = width < 1000
        await self.py('import renpy;s=renpy.store;s.persistent.room13_large_text='+str(large)+';s.persistent.room13_text_small=False;renpy.exports.restart_interaction();result=True')
        await asyncio.sleep(.7)


FOCUS = '''import renpy
def values(action):
 if isinstance(action,(list,tuple)):return [value for a in action for value in values(a)]
 return [repr(getattr(action,'value',None))]
def text(w,depth=0):
 if depth>12:return ''
 if isinstance(w,renpy.text.text.Text):return ''.join(str(x) for x in w.text)
 return ' '.join(text(c,depth+1) for c in w.visit())
result=[]
for f in renpy.display.focus.focus_list:
 if f.x is None or not f.w or not f.h:continue
 try:alt=str(f.widget.style.alt or '')
 except:alt=''
 result.append(dict(text=text(f.widget).strip(),alt=alt,values=values(getattr(f.widget,'clicked',None)),rect=[f.x,f.y,f.w,f.h]))
'''

NAMES = '''import renpy
s=renpy.store;actors=s.r13_stage_people();zoom=s.r13_field_zoom();offset=s.r13_world_offset()
def screen(rect):
 x,y,w,h=rect;return [(x-offset)*zoom,y*zoom,w*zoom,h*zoom]
result=dict(zoom=zoom,offset=offset,
 faces={a['person']:screen(s.r13_actor_face_target(a) or a['rect']) for a in actors},
 labels=[dict(person=n['person'],name=s.R13_NAMES[n['person']],rect=screen(n['rect'])) for n in s.r13_actor_nameplates(actors)])
'''


def overlap(a,b):
    return max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]))*max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))


def targets(rows,width,height,minimum=44):
    scale=min(width/1280,height/720)
    return [dict(**row,css_width=round(row['rect'][2]*scale,2),css_height=round(row['rect'][3]*scale,2),meets_target=min(row['rect'][2:])*scale>=minimum-.01) for row in rows]


async def main():
    report=dict(scope='첫 시작·편지·입구는 실제 UI 진행. 크기/글자 설정과 다페이지 질문은 화면 fixture, 첫 입실·메모는 선행 상태/라벨 fixture 후 실제 지도 이동.',checks=[],measurements=[],page_errors=[])
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
        context=await browser.new_context(viewport=dict(width=1280,height=720),has_touch=True)
        page=await context.new_page();q=FieldQA(page,OUT)
        page.on('pageerror',lambda error:report['page_errors'].append(str(error)))
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function'",timeout=300000)
            await q.wait('main_menu')
            report['version']=await q.py('import renpy;result=renpy.config.version')
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
            await q.press('처음부터')
            await q.wait('say')
            # The opening's centered text precedes the regular carriage dialogue.
            # Wait via actual clicks until the seated daughter is on stage.
            for _ in range(100):
                actor=await q.py('import renpy;s=renpy.store;result=dict(place=s.place,tags=sorted(renpy.exports.get_showing_tags()))')
                if actor['place']=='마차 안' and 'r13_visitor' in actor['tags']:break
                await q.input(640,610)
                await asyncio.sleep(.2)
            else:raise AssertionError(('마차 인물 대사에 도달하지 못함',actor))
            for tag,width,height in MATRIX_SIZES:
                for large in (False,True):
                    await q.setting_fixture(width,height,large)
                    rows=[r for r in await q.py(FOCUS) if '더보기' in r['text'] or '건너뛰기' in r['text']]
                    assert rows,await q.py(FOCUS)
                    measured=targets(rows,width,height)
                    if tag!='pc':
                        assert all(r['meets_target'] for r in measured),measured
                        assert all(r['rect'][1]+r['rect'][3]<=704 for r in rows),rows
                    text=await q.py('''import renpy
s=renpy.store;sc=renpy.display.screen.get_screen('say');w=renpy.exports.get_widget('say','what')
size=renpy.display.render.render(w,1090,720,0,0).get_size()
result=dict(top=s.r13_night_say_top(sc.scope.get('what')),height=size[1],text=sc.scope.get('what'))
''')
                    # Text renders include font descent; compare against the visible
                    # link glyphs, not transparent padding of the larger hit target.
                    visual_top=min(r['rect'][1]+r['rect'][3]/2-(14 if tag!='pc' else 10) for r in rows)
                    assert text['top']+text['height']<=visual_top,dict(text=text,targets=rows)
                    report['measurements'].append(dict(screen='dialogue',size=tag,large=large,targets=measured,text=text))
                    await q.shot('dialogue-'+tag+('-large' if large else '-normal'))
            await q.advance_until('choice')
            assert any('편지를 접는다' in b['text'] for b in (await q.state())['buttons'])
            for tag,width,height in MATRIX_SIZES:
                for large in (False,True):
                    await q.setting_fixture(width,height,large)
                    rows=[r for r in await q.py(FOCUS) if any(t in r['text'] for t in ('마지막 줄을 본다','글씨를 살핀다','편지를 접는다'))]
                    assert len(rows)==3,rows
                    # Existing seated Daram remains at x850; rows stay in the left safe region.
                    assert all(r['rect'][0]+r['rect'][2]<=640 and r['rect'][1]+r['rect'][3]<=610 for r in rows),rows
                    measured=targets(rows,width,height)
                    if tag!='pc':assert all(r['meets_target'] for r in measured),measured
                    report['measurements'].append(dict(screen='carriage',size=tag,large=large,targets=measured))
                    await q.shot('carriage-'+tag+('-large' if large else '-normal'))
            await q.press('마지막 줄을 본다');await q.advance_until('choice')
            assert any('✓ 마지막 줄을 본다' in b['text'] for b in (await q.state())['buttons'])
            await q.press('글씨를 살핀다');await q.advance_until('choice')
            assert any('✓ 글씨를 살핀다' in b['text'] for b in (await q.state())['buttons'])
            await q.press('편지를 접는다');await q.advance_until('r13_hub')
            report['checks'].append('새 게임→마차 두 조사→읽음 표시→편지 접기→입구 실제 진행')
            room_before=(await q.state())['room']
            for tag,width,height in MATRIX_SIZES:
                for large in (False,True):
                    await q.setting_fixture(width,height,large)
                    await asyncio.sleep(.5)
                    layout=await q.py(NAMES);focus=await q.py(FOCUS)
                    measured=[]
                    for label in layout['labels']:
                        actual=[r for r in focus if r['text']==label['name']]
                        if not actual:continue # Name outside the visible camera window.
                        rect=actual[0]['rect']
                        overlaps=[person for person,face in layout['faces'].items() if overlap(rect,face)>1]
                        measured.append(dict(person=label['person'],rect=rect,overlaps_faces=overlaps))
                        assert not overlaps,measured[-1]
                        if label['person']=='karo':
                            face=layout['faces']['karo']
                            distance=((rect[0]+rect[2]/2-face[0]-face[2]/2)**2+(rect[1]+rect[3]/2-face[1]-face[3]/2)**2)**.5
                            measured[-1]['distance_from_head']=distance
                            assert distance<120,measured[-1]
                    assert measured,layout
                    report['measurements'].append(dict(screen='gate-nameplates',size=tag,large=large,labels=measured,layout=layout))
                    await q.shot('gate-'+tag+('-large' if large else '-normal'))
            # Open actual settings through the game's gear and menu, without jumping labels.
            await q.setting_fixture(740,360,True)
            await q.input(1222,52);await q.press('설정');await q.wait('pause_menu')
            for tag,width,height in MATRIX_SIZES:
                for large in (False,True):
                    await q.setting_fixture(width,height,large)
                    await q.press('읽기')
                    rows=[r for r in await q.py(FOCUS) if r['text'] in ('작게','보통','크게','느리게','빠르게','즉시','닫기','읽기','소리','화면','저장 · 불러오기') or r['alt']=='닫기']
                    assert len(rows)>=10,rows
                    measured=targets(rows,width,height)
                    if tag!='pc':assert all(r['meets_target'] for r in measured),measured
                    assert all(r['rect'][1]+r['rect'][3]<=704 for r in rows),rows
                    report['measurements'].append(dict(screen='settings',size=tag,large=large,targets=measured))
                    await q.shot('settings-'+tag+('-large' if large else '-normal'))
            await page.set_viewport_size(dict(width=390,height=844));await asyncio.sleep(.7);await q.shot('settings-portrait')
            await q.setting_fixture(844,390,False);await q.press('닫기');await q.wait('r13_hub')
            assert (await q.state())['room']==room_before
            report['checks'].append('크기·글자 설정과 세로→가로 회전 뒤 날짜·장소·진행 상태 보존')
            # Explicit layout fixture: existing gate question titles repeated to force pages.
            await q.py('''import renpy
s=renpy.store
titles=[o['title'] for o in s.R13_V111_BINDINGS['gate_investigate']['options'] if o.get('person')=='guard']
entries=[(title,s.NullAction(),False) for title in titles]*3
renpy.exports.show_screen('r13_side_question_list',person='guard',pose='neutral',entries=entries,ready=True,return_action=s.Hide('r13_side_question_list'))
renpy.exports.restart_interaction();result=True
''')
            for tag,width,height in MATRIX_SIZES:
                for large in (False,True):
                    await q.setting_fixture(width,height,large)
                    await q.py('import renpy;renpy.display.screen.get_screen("r13_side_question_list").scope["page"]=0;renpy.exports.restart_interaction();result=True')
                    await asyncio.sleep(.5)
                    data=await q.py('''import renpy
s=renpy.store;sc=renpy.display.screen.get_screen('r13_side_question_list')
result=dict(page=sc.scope['page'],pages=len(s.r13_side_question_pages(sc.scope['entries'])))
''')
                    assert data['pages']>1,data
                    rows=[r for r in await q.py(FOCUS) if r['text'].startswith(('1 ','2 ','3 ','4 ')) or r['text'] in ('← 이전 질문','다음 질문 →','돌아가기')]
                    assert rows,await q.py(FOCUS)
                    measured=targets(rows,width,height)
                    if tag!='pc':assert all(r['meets_target'] for r in measured),measured
                    await q.shot('question-fixture-'+tag+('-large' if large else '-normal'))
                    await q.press('다음 질문')
                    assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_side_question_list").scope["page"]')==1
                    await q.press('이전 질문')
                    assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_side_question_list").scope["page"]')==0
                    report['measurements'].append(dict(screen='question-fixture',size=tag,large=large,targets=measured,pages=data['pages']))
            await q.py('import renpy;renpy.exports.hide_screen("r13_side_question_list");renpy.exports.restart_interaction();result=True')
            assert (await q.state())['room']==room_before
            report['checks'].append('질문 다페이지 fixture의 실제 이전/다음 클릭과 게임 상태 보존')
            # Explicit prerequisite + label fixture. Keep the gate location; use
            # real map/travel inputs so the authored scene initializes the room.
            # This does not count as continuous play through the gate/inn story.
            await q.py("import renpy;s=renpy.store;s.r13_v111_set('gate_registered',True);s.r13_v111_scene('MS14_D01_S05');result=True")
            await q.jump_fixture('r13_v111_room_observe')
            await q.wait('r13_hub')
            assert (await q.state())['room']['v111']['gate']=='travel'
            await q.press('지도');await q.wait('r13_map')
            await q.press('여관 안');await q.press('13호실');await q.press('이곳으로 이동')
            await q.advance_until('say')
            assert '아내가 머물던 방' in (await q.state())['say']
            await q.shot('room-arrival-fixture')
            await q.advance_until('r13_hub')
            assert await q.py("import renpy;result=renpy.store.r13_v111_value('ui_room_arrival_seen')")
            # 2026-10-29 외부 검토 C: 도착하면 첫 입실 장면이 바로 이어져 책상 메모 차례(note_pick)에서 멈춘다. 침대를 누를 필요가 없다.
            assert (await q.state())['room']['v111']['gate']=='note_pick'
            # Room13 opens on the bed side; pan left through its real camera control.
            await q.input(48,276);await asyncio.sleep(1)
            for tag,width,height in SIZES:
                await q.setting_fixture(width,height,False)
                rows=[r for r in await q.py(FOCUS) if "('object', 'mother_note')" in r['values']]
                if not rows:
                    debug=await q.py("import renpy;s=renpy.store;sc=renpy.display.screen.get_screen('r13_hub');spec=s.ROOM13['objects']['room13']['mother_note'];a=sc.scope['world_adjustment'];result=dict(spec=spec,visible=s.r13_object_visible(spec),binding=s.r13_v111_binding(),offset=s.r13_world_offset(),cameras=s.r13_world_cameras,adjustment=[a.value,a.range],rect=s.r13_object_target_rect('mother_note',spec),room=s.room13)")
                    (OUT/'memo-debug.json').write_text(json.dumps(debug,ensure_ascii=False,indent=2))
                assert rows,await q.py(FOCUS)
                measured=targets(rows,width,height)
                if tag!='pc':assert all(r['meets_target'] for r in measured),measured
                report['measurements'].append(dict(screen='memo-target-fixture',size=tag,targets=measured))
                await q.shot('memo-target-fixture-'+tag)
            rows=[r for r in await q.py(FOCUS) if "('object', 'mother_note')" in r['values']]
            x,y,w,h=rows[0]['rect'];await q.input(x+w/2,y+h/2)
            await q.advance_until('r13_hub')
            assert 'V111:E06' in (await q.state())['room']['evidence']
            report['checks'].append('첫 입실/메모 라벨 fixture: 첫 입실 생각 표시, 실제 침대·카메라 이동·메모 클릭, 메모 자료 획득')
            assert not report['page_errors'],report['page_errors']
            assert not await q.py('import renpy;result=renpy.display.screen.get_screen("_exception") is not None')
            report['status']='passed-pending-visual-review'
        except Exception:
            report['status']='failed';report['error']=traceback.format_exc()
            await page.screenshot(path=str(OUT/'failure.png'))
            try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
            except Exception:pass
        finally:
            (OUT/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
            print(json.dumps(dict(status=report.get('status'),error=report.get('error'),measurements=len(report['measurements'])),ensure_ascii=False),flush=True)
            await browser.close()
    if report['status']=='failed':raise SystemExit(1)


if __name__=='__main__':asyncio.run(main())
