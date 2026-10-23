"""지도 보고서 U09: 실제 잠김 클릭, 상태 보존, PC/휴대폰 공통 UI 검수.

첫 입구는 실제 새 게임으로 진입하고 검수용으로 지도 화면을 직접 연다.
모든 지역 외형 검수만 이동 목록을
명시적인 공개 장소 fixture로 넓힌다. 이동 조건 검증이나 완주로 세지 않는다.
"""
import asyncio
import json
import os
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright
from webqa import UIQA

OUT = Path(os.environ.get("ROOM13_QA_OUT", "/tmp/room13-qa/map-review"))
URL = os.environ.get("ROOM13_URL", "http://127.0.0.1:8765/preview/room13-dev/")
OUT.mkdir(parents=True, exist_ok=True)


class MapQA(UIQA):
    async def py(self, code):
        return await super().py("ns={};exec(" + ascii(code) + ",ns);result=ns.get('result')")

    async def input(self,x,y):
        vp=self.p.viewport_size
        scale=min(vp["width"]/1280,vp["height"]/720)
        if not self.touch:
            px=(vp["width"]-1280*scale)/2+x*scale;py=(vp["height"]-720*scale)/2+y*scale
            await self.p.mouse.move(px,py)
            await asyncio.sleep(.18)
            await self.p.mouse.click(px,py)
            await asyncio.sleep(.3)
            return
        client=await self.p.context.new_cdp_session(self.p)
        try:
            await client.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":(vp["width"]-1280*scale)/2+x*scale,"y":(vp["height"]-720*scale)/2+y*scale}]})
            # Model a short finger contact explicitly; every assertion still uses
            # the first tap, with no repeat or mouse fallback.
            await asyncio.sleep(.12)
            await client.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]})
        finally:await client.detach()
        await asyncio.sleep(.3)

    async def rect(self, widget_id):
        return await self.py('import renpy\nw=renpy.exports.get_widget("r13_map",'+repr(widget_id)+')\nresult=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if f.widget is w and f.x is not None),None)')

    async def click_id(self, widget_id):
        rect = await self.rect(widget_id)
        assert rect, widget_id
        x,y,w,h=rect
        assert 0 <= x+w/2 <= 1280 and 0 <= y+h/2 <= 720, rect
        await self.input(x+w/2,y+h/2)
        prefix="map_name_" if widget_id.startswith("map_name_") else "map_room_" if widget_id.startswith("map_room_") else None
        if prefix:
            selected=await self.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["selected"]')
            assert selected==widget_id[len(prefix):],(widget_id,selected,rect)

    async def drag_focus_place(self,key):
        target=await self.py('import renpy;result=renpy.store.r13_cart_focus("village",'+repr(key)+')')
        for _ in range(5):
            current=await self.py('import renpy;v=renpy.exports.get_widget("r13_map","r13_map_view");result=[v.xadjustment.value,v.yadjustment.value]')
            dx=max(-450,min(450,target[0]-current[0]));dy=max(-180,min(180,target[1]-current[1]))
            if abs(dx)+abs(dy)<48:break
            vp=self.p.viewport_size;scale=min(vp["width"]/1280,vp["height"]/720);ox=(vp["width"]-1280*scale)/2;oy=(vp["height"]-720*scale)/2
            client=await self.p.context.new_cdp_session(self.p)
            await client.send("Input.dispatchTouchEvent",{"type":"touchStart","touchPoints":[{"x":ox+640*scale,"y":oy+340*scale}]})
            for step in range(1,11):
                await asyncio.sleep(.025)
                await client.send("Input.dispatchTouchEvent",{"type":"touchMove","touchPoints":[{"x":ox+(640-dx*step/10)*scale,"y":oy+(340-dy*step/10)*scale}]})
            await client.send("Input.dispatchTouchEvent",{"type":"touchEnd","touchPoints":[]});await client.detach();await asyncio.sleep(.4)
        print("DRAG_FOCUS",key,current,target,flush=True)

    async def focus_place(self, key):
        if self.touch:return await self.drag_focus_place(key)
        await self.py('import renpy;s=renpy.store;v=renpy.exports.get_widget("r13_map","r13_map_view");x,y=s.r13_cart_focus("village",'+repr(key)+');v.xadjustment.change(x);v.yadjustment.change(y);renpy.exports.restart_interaction();result=True')
        await asyncio.sleep(.4)


async def main():
    report={"scope":"새 게임으로 첫 입구 진입 후 지도 화면 직접 열기 fixture. 장소 클릭은 실제 입력. 전체 지역 외형은 공개 장소 목록 fixture.","checks":[],"measurements":[],"mouse_input":"마우스이동→180ms hover→첫클릭1회", "touch_input":"CDP 실제 접촉120ms, 스크롤은 손가락드래그, 각장소 첫탭1회 뒤 선택값 확인", "archive_sha256":json.load(urllib.request.urlopen(URL+"game-transport.json"))["archive_sha256"]}
    errors=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=os.environ.get("ROOM13_CHROME","/usr/bin/chromium"),args=["--no-sandbox","--enable-unsafe-swiftshader"])
        page=await browser.new_page(viewport={"width":1280,"height":720},has_touch=True)
        q=MapQA(page,OUT)
        page.on("pageerror",lambda error:errors.append(str(error)))
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000)
            await q.wait("main_menu")
            report["version"]=(await q.info())["version"]
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
            await q.press("처음부터")
            for _ in range(260):
                st=await q.state()
                if "r13_hub" in st["screens"]:break
                if "choice" in st["screens"] and any("편지를 접는다" in b["text"] for b in st["buttons"]):
                    await q.press("편지를 접는다")
                else:await q.input(640,300)
            await q.wait("r13_hub")
            before=(await q.state())["room"]
            await q.py('import renpy;renpy.exports.show_screen("r13_map");renpy.exports.restart_interaction();result=True')
            await q.wait("r13_map")
            selected=await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["selected"]')
            assert await q.py('import renpy;result="workshop" in dict(renpy.store.r13_map_locked_nodes("village"))')
            for name,viewport in (("pc",{"width":1280,"height":720}),("touch844",{"width":844,"height":390}),("touch740",{"width":740,"height":360})):
                await page.set_viewport_size(viewport)
                q.touch=name!="pc"
                await asyncio.sleep(.5)
                await q.focus_place("workshop")
                await q.click_id("map_locked_name_workshop")
                assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["map_notice"]')=="수리점 · 지금은 이곳으로 갈 수 없습니다."
                assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["selected"]')==selected
                assert (await q.state())["room"]==before
                await q.shot(name+"-locked")
                await q.focus_place("gate")
                await q.click_id("map_name_gate")
                assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["map_notice"]') is None
            report["checks"].append("PC/844/740에서 잠긴 수리점 클릭 안내, 현재 선택·진행 전체 상태 보존, 허용 장소 선택 시 안내 해제")
            # Only this view fixture widens visible destinations. Do not execute travel.
            await q.py('import renpy;s=renpy.store;s._qa_map_places=s.r13_places;s.r13_places=lambda:list({k for r in s.R13_MAP_NODES.values() for k in r if k not in s.R13_V111_MAP_ALIASES and k not in ("greenhouse","altar","ancient","passage")});renpy.exports.restart_interaction();result=True')
            for name,viewport in (("pc",{"width":1280,"height":720}),("touch844",{"width":844,"height":390}),("touch740",{"width":740,"height":360})):
                await page.set_viewport_size(viewport)
                q.touch=name!="pc"
                for large in (False,True):
                    prefix=name+("-large" if large else "-normal")
                    await q.py('import renpy;renpy.store.persistent.room13_large_text='+str(large)+';renpy.exports.restart_interaction();result=True')
                    await q.press("마을")
                    await q.focus_place("inn")
                    await q.click_id("map_name_inn")
                    await q.shot(prefix+"-village")
                    measured=[]
                    controls=(await q.state())["buttons"]
                    for wid,label in (("r13_map_region_village","마을"),("r13_map_region_inn","여관 안"),("r13_map_region_mountain","숲·산길"),("r13_map_travel","이곳으로 이동"),("r13_map_close","현장으로")):
                        rect=next((b["rect"] for b in controls if b["text"].strip()==label),None)
                        assert rect,wid
                        scale=min(viewport["width"]/1280,viewport["height"]/720)
                        if q.touch:assert min(rect[2],rect[3])*scale>=44,(wid,rect,scale)
                        assert rect[1]+rect[3]<=704,(wid,rect)
                        measured.append({"id":wid,"rect":rect,"css_height":rect[3]*scale})
                    await q.press("여관 안")
                    await q.shot(prefix+"-inn")
                    await q.py('import renpy;v=renpy.exports.get_widget("r13_map","map_inn_list");v.yadjustment.change(v.yadjustment.range);renpy.exports.restart_interaction();result=True')
                    await asyncio.sleep(.3)
                    await q.click_id("map_room_room13")
                    await q.shot(prefix+"-room13")
                    await q.press("숲·산길")
                    await q.shot(prefix+"-mountain")
                    assert not await q.py('import renpy;s=renpy.store;result=s.r13_cart_cover_visible("greenhouse") or s.r13_cart_cover_visible("altar")')
                    assert (await q.state())["room"]==before
                    report["measurements"].append({"mode":prefix,"controls":measured})
            # Lowest map labels remain reachable above the permanent status/footer strip.
            await q.press("마을")
            for key in ("laundry","somi"):
                await q.focus_place(key)
                rect=await q.rect("map_name_"+key)
                print("LOWER_TARGET",key,rect,flush=True)
                await q.click_id("map_name_"+key)
                chosen=await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["selected"]')
                print("LOWER_SELECTED",chosen,flush=True)
                assert chosen==key,(key,chosen,rect)
                rect=await q.rect("map_name_"+key)
                assert rect[1]+rect[3]<=548,(key,rect)
                await q.shot("touch740-large-"+key)
            await q.py('import renpy;s=renpy.store;s.r13_places=s._qa_map_places;renpy.exports.restart_interaction();result=True')
            await q.press("현장으로")
            await q.wait("r13_hub")
            assert (await q.state())["room"]==before
            assert not errors,errors
            report.update(passed=True,page_errors=errors,state_preserved=True)
        except Exception as error:
            report.update(passed=False,error=repr(error),page_errors=errors)
            await q.shot("failure")
            raise
        finally:
            (OUT/"result.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
            print(json.dumps(report,ensure_ascii=False),flush=True)
            await browser.close()


if __name__=="__main__":asyncio.run(main())
