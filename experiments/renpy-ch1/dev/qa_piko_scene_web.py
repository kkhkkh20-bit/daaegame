"""3일 사망 직전 상태를 준비해 실제 선택·휴대폰 표시·브라우저 재시작 저장 복원을 검사한다."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_novel_adaptation import jump, until

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/piko-106-web'))
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/')

async def run(q,code):
    return await q.py('ns={};exec('+repr(code)+',ns);result=ns.get("result")')

async def view(q):
    return await run(q,'import renpy;s=renpy.store;v=s.r13_v111_value;result=dict(near=s.r13_piko_scene_near,read={k:bool(v("piko_scene_read:"+k)) for k in ("posture","portrait","daram")},evidence=list(s.room13["evidence"]),minutes=v("elapsed_minutes"),tries=v("tries:lamp"),alive=v("piko_alive"),portrait=v("portrait"),variant=v("E09.variant"))')

async def check_geometry(q):
    data=await run(q,'import renpy;s=renpy.store;result=[]\nfor entry in s.R13_PIKO_SCENE_CHOICES:\n w=renpy.text.text.Text(entry["caption"],font=s.R13_UI_BOLD_FONT,size=s.r13_type("emphasis"),xsize=382)\n size=renpy.display.render.render(w,382,104,0,0).get_size()\n result.append([entry["key"],list(size)])')
    assert all(w<=382 and h<=84 for _,(w,h) in data),data
    return data

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
        context=await browser.new_context(viewport={'width':1280,'height':720},has_touch=True)
        page=await context.new_page();q=SayQA(page,OUT);errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            await page.goto(URL)
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu')
            await run(q,'import renpy;renpy.store.preferences.text_cps=0;renpy.store.persistent.room13_large_text=False;result=True')
            await q.press('처음부터');await until(q,screen='r13_hub')
            await run(q,'import renpy;s=renpy.store;s.r13_flag("v111:applied:option:sleep2:0");s.r13_v111_set("day",3);s.r13_v111_set("lamp_bound2",False);s.r13_v111_set("piko_sheltered",False);s.r13_v111_set("piko_alive",True);s.r13_edit(day=3,period=0,location="square");s.place=s.R13_PLACES["square"][0];result=True')
            await jump(q,'r13_v111_day3');await until(q,screen='r13_piko_scene')
            initial=await view(q)
            assert initial['alive'] is False and initial['variant']=='unfinished'
            print('피코 현장 도착',flush=True)
            geometry_pc=await check_geometry(q)
            await page.screenshot(path=str(OUT/'피코현장_PC.png'))
            await q.press('받은 초상을 다시 본다');await q.wait('r13_pw_picture')
            await page.screenshot(path=str(OUT/'피코현장_받은초상.png'))
            await q.press('닫기');await until(q,screen='r13_piko_scene')
            await q.press('그림을 접고 설명으로 듣는다');await q.wait('r13_piko_scene')
            await q.press('다람에게 말을 건넨다');await until(q,screen='r13_piko_scene')
            await page.set_viewport_size({'width':844,'height':390});q.touch=True
            await run(q,'import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
            await asyncio.sleep(.5)
            geometry_phone=await check_geometry(q)
            controls=await run(q,'import renpy;result=[[f.widget.id,[f.x,f.y,f.w,f.h]] for f in renpy.display.focus.focus_list if f.x is not None and str(getattr(f.widget,"id","") or "").startswith("r13_piko_")]')
            scale=min(844/1280,390/720)
            assert len(controls)==5 and all(rect[3]*scale>=44 for _,rect in controls),controls
            await page.screenshot(path=str(OUT/'피코현장_휴대폰_큰글씨.png'))
            print('PC·휴대폰 표시 확인',flush=True)
            saved=await view(q)
            assert not saved['near'] and saved['read']==dict(posture=False,portrait=True,daram=True)
            assert {k:v for k,v in saved.items() if k not in ('near','read')}=={k:v for k,v in initial.items() if k not in ('near','read')}
            await run(q,'import renpy;renpy.exports.save("qa-piko-scene-web-106");result=True')
            await q.press('피코가 있는 쪽을 다시 본다')
            await q.press('초롱 씨에게 발견 당시 모습을 묻는다');await until(q,screen='r13_piko_scene')
            assert (await view(q))['read']['posture']
            await page.reload()
            await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
            await q.wait('main_menu')
            await run(q,'import renpy\ndef qa_piko_web_load(**kwargs):\n import renpy\n s=renpy.store\n renpy.ui.textbutton("검수 저장 불러오기",clicked=[s.Hide("qa_piko_web_load"),s.Function(renpy.exports.load,"qa-piko-scene-web-106")],xpos=420,ypos=300,xsize=440,ysize=80)\nrenpy.exports.define_screen("qa_piko_web_load",qa_piko_web_load,modal="True",zorder="200")\nrenpy.exports.show_screen("qa_piko_web_load");renpy.exports.restart_interaction();result=True')
            await q.press('검수 저장 불러오기');await q.wait('r13_piko_scene')
            assert await view(q)==saved
            await page.screenshot(path=str(OUT/'피코현장_브라우저재시작_저장복원.png'))
            await q.press('등 쪽으로 간다');await until(q,screen='r13_hub')
            assert await run(q,'import renpy;s=renpy.store;result=s.room13["v111"]["gate"]=="lamp_inspect3" and not s.r13_ep_cut_current')
            assert not errors,errors
            report=dict(status='통과',version=await run(q,'import renpy;result=renpy.config.version'),scope='실제 시작 뒤 사망 직전 상태 fixture; 선택·브라우저 재시작 복원',geometry_pc=geometry_pc,geometry_phone=geometry_phone,phone_targets=controls,saved=saved,pageerrors=errors)
            (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps(report,ensure_ascii=False),flush=True)
        finally:
            await browser.close()

if __name__=='__main__':asyncio.run(main())
