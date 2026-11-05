"""읽기 개선 시안. 자연 시작 뒤 proof·ending 상태 fixture를 준비해 실제 입력한다."""
import asyncio,copy,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_novel_adaptation import jump
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/reading-review-web'));OUT.mkdir(parents=True,exist_ok=True)
async def run(q,code):return await q.py('ns={};exec('+repr(code)+',ns);result=ns.get("result")')
async def press_id(q,name,screen='r13_proof_workspace'):
 rect=await run(q,'import renpy;w=renpy.display.screen.get_widget('+repr(screen)+','+repr(name)+');f=next(f for f in renpy.display.focus.focus_list if f.widget is w and f.x is not None);result=[f.x,f.y,f.w,f.h]')
 x,y,w,h=rect;await q.input(x+w/2,y+h/2)
async def texts(q,screen):
 return await run(q,'import renpy\nsc=renpy.display.screen.get_screen('+repr(screen)+')\nseen=set();result=[]\ndef walk(w):\n if id(w) in seen:return\n seen.add(id(w))\n if isinstance(w,renpy.text.text.Text):result.append("".join(str(t) for t in w.text))\n for child in w.visit():walk(child)\nwalk(sc)')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True);q=SayQA(page,OUT);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
   await q.wait('main_menu');await run(q,'import renpy;s=renpy.store;s.preferences.text_cps=0;s.persistent.room13_pw_controls_seen=False;result=True')
   await q.press('처음부터');print('새 게임 시작',flush=True)
   for _ in range(180):
    st=await q.state()
    if 'r13_hub' in st['screens']:break
    if 'choice' in st['screens']:await q.press('편지를 접는다')
    elif 'r13_cinematic_view' in st['screens']:await q.press('계속')
    else:await q.input(900,600)
   else:raise AssertionError(st)
   print('입구 도착',flush=True)
   await run(q,'import renpy;s=renpy.store;s.r13_v111_commit("MS14_D01_S02_L0019");s.r13_v111_commit("MS14_D01_S03_L0002");s.r13_v111_commit("MS14_D01_S03_L0007");s.r13_grant(["V111:E01","V111:E02","V111:E03","V111:E04"],"qa");result=True')
   await jump(q,'r13_v111_gate_proof')
   await q.wait('r13_proof_workspace');await asyncio.sleep(.4);print('자료 화면',flush=True)
   await page.screenshot(path=str(OUT/'자료_처음안내_PC.png'))
   tries=await run(q,'import renpy;result=renpy.store.r13_v111_value("tries:gate")')
   await press_id(q,'r13_pw_open_E04');await page.screenshot(path=str(OUT/'자료_본문_PC.png'))
   assert '출처 펼치기' in '\n'.join(await texts(q,'r13_proof_workspace'))
   await press_id(q,'r13_pw_check_E04')
   args=await run(q,'import renpy;s=renpy.store;result=s.room13["arguments"]["v111:함께 들어갈 근거를 고른다"]')
   assert args==['V111:E04'],args
   assert await run(q,'import renpy;result=renpy.store.r13_v111_value("tries:gate")')==tries
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await run(q,'import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(.4)
   assert not await run(q,'import renpy;result=renpy.display.screen.get_screen("r13_proof_workspace").scope["quote_open"]')
   await page.screenshot(path=str(OUT/'자료_본문_휴대폰큰글씨.png'));print('휴대폰 자료 읽기',flush=True)
   await press_id(q,'r13_pw_enlarge');await asyncio.sleep(.3)
   assert await run(q,'import renpy;result=bool(renpy.display.screen.get_screen("r13_pw_picture"))')
   await q.press('닫기');assert not await run(q,'import renpy;result=bool(renpy.display.screen.get_screen("r13_pw_picture"))')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await run(q,'import renpy;s=renpy.store;s.persistent.room13_large_text=False;renpy.exports.hide_screen("r13_proof_workspace");renpy.exports.hide_screen("r13_hub");renpy.exports.hide_screen("say");renpy.exports.scene();s.r13_cg_active=True;s.r13_end_cut_key="END-09";renpy.exports.show("review_ending",what=s.r13_end_cut_art("END-09"));renpy.exports.show_screen("r13_end_card",name="남겨진 이름",stat="지킨 사람 7 · 잃은 사람 2",lost="피코 · 톡");renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(.6);before=copy.deepcopy((await q.state())['room'])
   assert not any('지킨 사람' in t for t in await texts(q,'r13_end_card'))
   await page.screenshot(path=str(OUT/'결말_첫화면_PC.png'))
   await q.press('여정의 기록 보기');assert any('지킨 사람 7' in t for t in await texts(q,'r13_end_card'))
   await page.screenshot(path=str(OUT/'결말_기록_PC.png'))
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await asyncio.sleep(1);await run(q,'import renpy;renpy.exports.restart_interaction();result=True');await asyncio.sleep(.5)
   await page.screenshot(path=str(OUT/'결말_기록_휴대폰.png'))
   await q.press('기록 접기');await asyncio.sleep(1);print('휴대폰 결말 접기',flush=True);await page.screenshot(path=str(OUT/'결말_첫화면_휴대폰.png'))
   assert await run(q,'import renpy;sc=renpy.display.screen.get_screen("r13_end_card");result=bool(sc) and not sc.scope["details_open"]')
   card_text=await texts(q,'r13_end_card');assert any('남겨진 이름' in t for t in card_text)
   assert not any('지킨 사람' in t for t in card_text)
   assert any('여정의 기록 보기' in b['text'] for b in (await q.state())['buttons'])
   assert (await q.state())['room']==before
   assert not errors,errors
   report=dict(status='통과',publication='미공개 시안',checks=['첫 안내·이름 읽기·체크 선택 역할','읽기·선택 기회 미소모','PC·휴대폰 큰글씨 자료 상세','휴대폰 그림 확대·닫기','결말 집계 기본 숨김·열기·접기','결말 기록 UI world state 불변'],pageerrors=errors)
   (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True)
  finally:await browser.close()
if __name__=='__main__':asyncio.run(main())
