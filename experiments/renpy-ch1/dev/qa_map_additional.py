"""A03/A05 browser checks. Explicit day-2/map-layout fixtures, actual device input.

This is not a story playthrough. A03 uses the authoritative go_box availability;
A05 widens only public map destinations for input coverage, then restores state.
"""
import asyncio
import json
import os
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright
from qa_map_review import MapQA

OUT = Path(os.environ.get("ROOM13_QA_OUT", "/tmp/room13-qa/map-additional"))
URL = os.environ.get("ROOM13_URL", "http://127.0.0.1:8765/preview/room13-dev/")
OUT.mkdir(parents=True, exist_ok=True)


async def map_info(q):
    return await q.py('import renpy;s=renpy.display.screen.get_screen("r13_map");v=renpy.exports.get_widget("r13_map","r13_map_view");result=dict(selected=s.scope["selected"],pan=[v.xadjustment.value,v.yadjustment.value] if v else None)')


async def mouse_drag(q, start=(800, 400), end=(350, 200)):
    await q.p.mouse.move(*start)
    await asyncio.sleep(.2)
    await q.p.mouse.down()
    await q.p.mouse.move(*end, steps=20)
    await q.p.mouse.up()
    await asyncio.sleep(.5)


async def reset_pan(q, x, y):
    # Deterministic start only. The measured movement uses actual browser input.
    await q.py('import renpy;v=renpy.exports.get_widget("r13_map","r13_map_view");v.xadjustment.change('+str(x)+');v.yadjustment.change('+str(y)+');renpy.exports.restart_interaction();result=True')
    await asyncio.sleep(.4)


async def main():
    report=dict(scope="새 게임 진입 후 day2 go_box 상태 및 공개장소 목록 fixture. 실제 입력 검증이며 이야기 완주 아님.",
                archive_sha256=json.load(urllib.request.urlopen(URL+"game-transport.json"))["archive_sha256"], checks=[])
    errors=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=os.environ.get("ROOM13_CHROME","/usr/bin/chromium"),args=["--no-sandbox","--enable-unsafe-swiftshader"])
        page=await browser.new_page(viewport=dict(width=1280,height=720),has_touch=True)
        q=MapQA(page,OUT)
        page.on("pageerror",lambda error:errors.append(str(error)))
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000)
            await q.wait("main_menu")
            report["version"]=(await q.info())["version"]
            await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
            await q.press("처음부터")
            for _ in range(260):
                st=await q.state()
                if "r13_hub" in st["screens"]:break
                if "choice" in st["screens"] and any("편지를 접는다" in b["text"] for b in st["buttons"]):await q.press("편지를 접는다")
                else:await q.input(640,300)
            await q.wait("r13_hub")
            await q.py('import renpy;s=renpy.store;s._qa_a03_saved=s.winter_copy.deepcopy(s.room13);s.room13["day"]=2;s.room13["location"]="square";s.room13["v111"].update(gate="go_box",scene="MS14_D02_S01");renpy.exports.show_screen("r13_map",initial_region="mountain");renpy.exports.restart_interaction();result=True')
            await q.wait("r13_map")
            before=(await q.state())["room"]
            assert await q.py('import renpy;result=renpy.store.r13_map_label("forest")')=="깊은 숲 · 교환함"
            assert (await map_info(q))["selected"]=="forest"
            for name,viewport,touch in (("pc",dict(width=1280,height=720),False),("touch740",dict(width=740,height=360),True)):
                await page.set_viewport_size(viewport);q.touch=touch
                for large in (False,True):
                    await q.py('import renpy;renpy.store.persistent.room13_large_text='+str(large)+';renpy.exports.restart_interaction();result=True')
                    await q.shot(name+("-large" if large else "-normal")+"-box-destination")
                    assert (await q.state())["room"]==before
            report["checks"].append("교환함행: 깊은 숲·교환함 표시, PC/740 보통·큰글씨, 이동 미확정 상태 보존")
            for gate in ("box_inspect","box_note","envelope_show","lamp_rope"):
                await q.py('import renpy;s=renpy.store;s.room13["v111"]["gate"]='+repr(gate)+';renpy.exports.restart_interaction();result=True')
                assert await q.py('import renpy;result=renpy.store.r13_map_label("forest")')=="깊은 숲"
            report["checks"].append("교환함 조사/쪽지/우체국/아침 이전 단계에서 오래된 보조명 없음")
            await q.py('import renpy;s=renpy.store;s.room13=s.winter_copy.deepcopy(s._qa_a03_saved);s._qa_a05_places=s.r13_places;s.r13_places=lambda:list({k for r in s.R13_MAP_NODES.values() for k in r if k not in s.R13_V111_MAP_ALIASES and k not in ("greenhouse","altar","ancient","passage")});renpy.exports.hide_screen("r13_map");renpy.exports.show_screen("r13_map",initial_region="village");renpy.exports.restart_interaction();result=True')
            await page.set_viewport_size(dict(width=1280,height=720));q.touch=False
            await q.wait("r13_map")
            before=(await q.state())["room"]
            await reset_pan(q,160,0)
            previous=await map_info(q)
            await page.mouse.move(640,350);await page.mouse.wheel(0,520);await asyncio.sleep(.5)
            after=await map_info(q)
            assert after["pan"][1]>previous["pan"][1],(previous,after)
            assert after["selected"]==previous["selected"]
            report["checks"].append("실제 마우스 휠로 세로 지도 이동, 선택/진행 불변")
            await reset_pan(q,0,0)
            previous=await map_info(q)
            await mouse_drag(q)
            after=await map_info(q)
            assert after["pan"][0]>previous["pan"][0] and after["pan"][1]>previous["pan"][1],(previous,after)
            assert after["selected"]==previous["selected"]
            report["checks"].append("실제 마우스 드래그로 가로·세로 이동, 선택/진행 불변")
            await reset_pan(q,160,160)
            moves=[]
            for key,axis,direction in (("Shift+ArrowRight",0,1),("Shift+ArrowLeft",0,-1),("Shift+ArrowDown",1,1),("Shift+ArrowUp",1,-1),("PageDown",1,1),("PageUp",1,-1)):
                previous=await map_info(q)
                await page.keyboard.press(key);await asyncio.sleep(.3)
                after=await map_info(q)
                assert (after["pan"][axis]-previous["pan"][axis])*direction>0,(key,previous,after)
                assert after["selected"]==previous["selected"]
                assert (await q.state())["room"]==before
                moves.append(dict(key=key,before=previous["pan"],after=after["pan"]))
            report["keyboard_pans"]=moves
            report["checks"].append("Shift+4방향 및 PageUp/Down 실제 키 입력으로 지도 이동, 선택/진행 불변")
            await q.focus_place("post");await q.click_id("map_name_post")
            await q.shot("pc-post-reachable")
            assert (await q.state())["room"]==before
            # Arrow focus navigation must remain usable alongside modified-arrow
            # panning. Activate only a verified destination target, never travel.
            keyboard_target=None
            for key in ("ArrowRight","ArrowDown","ArrowLeft","ArrowUp")*3:
                await page.keyboard.press(key);await asyncio.sleep(.2)
                keyboard_target=await q.py('import renpy;s=renpy.store;f=renpy.display.focus.get_focused();result=next((k for k,p in s.r13_map_nodes("village") for prefix in ("map_name_","map_building_") if renpy.exports.get_widget("r13_map",prefix+k) is f),None)')
                if keyboard_target:break
            assert keyboard_target,"keyboard could not focus a visible destination"
            await page.keyboard.press("Enter");await asyncio.sleep(.3)
            assert (await map_info(q))["selected"]==keyboard_target
            assert (await q.state())["room"]==before
            report["keyboard_selected"]=keyboard_target
            report["checks"].append("기본 방향키로 지도 장소 포커스 후 Enter 선택, 여행 미확정")
            # Deterministically put an eligible name under the non-button footer
            # area; a UI panel must not dispatch that obscured map target.
            hidden=await q.py('import renpy;s=renpy.store;v=renpy.exports.get_widget("r13_map","r13_map_view");x,y,w,h=s.r13_cart_name_rect("laundry");v.xadjustment.change(max(0,x-80));v.yadjustment.change(max(0,y-565));renpy.exports.restart_interaction();result=[x,y,w,h]')
            await asyncio.sleep(.4)
            rect=await q.rect("map_name_laundry")
            if rect and 548<=rect[1]+rect[3]/2<596:
                previous=(await map_info(q))["selected"]
                await q.input(rect[0]+rect[2]/2,rect[1]+rect[3]/2)
                assert (await map_info(q))["selected"]==previous,("obscured-name-clickthrough",rect)
                report["checks"].append("고정 안내띠 아래 숨은 장소 클릭이 선택으로 전달되지 않음")
            else:report["hidden_target_probe"]=dict(rect=rect,note="목표를 고정띠 뒤에 배치하지 못해 별도 확인 필요")
            await page.set_viewport_size(dict(width=740,height=360));q.touch=True
            await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
            for key in ("post","laundry","somi"):
                await q.drag_focus_place(key)
                rect=await q.rect("map_name_"+key)
                assert rect and rect[1]+rect[3]<=548,(key,rect)
                await q.click_id("map_name_"+key)
                assert (await q.state())["room"]==before
                await q.shot("touch740-large-"+key)
            report["checks"].append("740 큰글씨 실제 손가락 드래그 뒤 우체국·빨래터·솜이네 첫 탭 선택, 여행 미확정")
            await q.py('import renpy;s=renpy.store;s.r13_places=s._qa_a05_places;s.room13=s._qa_a03_saved;renpy.exports.hide_screen("r13_map");renpy.exports.restart_interaction();result=True')
            assert not errors,errors
            report.update(passed=True,page_errors=errors)
        except Exception as error:
            report.update(passed=False,error=repr(error),page_errors=errors)
            await q.shot("failure")
            raise
        finally:
            (OUT/"result.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
            print(json.dumps(report,ensure_ascii=False),flush=True)
            await browser.close()


if __name__=="__main__":asyncio.run(main())
