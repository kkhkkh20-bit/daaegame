"""Title cover: real mouse/keyboard navigation, mobile, settings and fresh start."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/title-qa'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=UIQA(page,OUT)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=150000);await q.wait('main_menu');await asyncio.sleep(2.5)
   st=await q.state();assert not any(any(label in v['text'] for label in ('이어하기','불러오기')) for v in st['buttons']),st
   assert await q.py('result=renpy.display.screen.get_screen("main_menu").scope["title_focus"]')=='new'
   await q.shot('title-desktop')
   # Reuse the loaded page so two software-rendered games do not compete for the GPU.
   desktop=page;keys=q
   await desktop.mouse.click(650,360)
   await desktop.mouse.move(446,506);await asyncio.sleep(.4)
   await desktop.keyboard.press('ArrowDown');await keys.shot('title-keyboard')
   assert await keys.py('result=renpy.display.screen.get_screen("main_menu").scope["title_focus"]')=='settings'
   await desktop.keyboard.press('Enter');await keys.wait('pause_menu');await keys.press('닫기');await keys.wait('main_menu')
   await q.press('설정');await q.wait('pause_menu');await q.shot('title-settings');await q.press('닫기');await q.wait('main_menu')
   await q.press('음악 출처');await q.shot('title-credits');await q.press('닫기');await q.wait('main_menu')
   await q.py('import renpy;renpy.store.persistent.room13_motion=False;renpy.exports.restart_interaction();result=True');await q.shot('title-motion-off')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True;await q.shot('title-mobile');await q.press('설정');await q.wait('pause_menu');await q.shot('title-settings-mobile');await q.press('닫기');await q.wait('main_menu')
   if os.environ.get('ROOM13_TITLE_SMOKE_ONLY')=='1':
    info={'passed':True,'scope':'title-settings','version':(await q.info())['version'],'checks':['fresh title','keyboard down and Enter from focused new-game button','settings open and return','music credits','motion off','844x390 touch settings and return']}
    (OUT/'result.json').write_text(json.dumps(info,ensure_ascii=False,indent=2));print('PASS',info,flush=True);return
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;renpy.store.persistent.room13_motion=True;renpy.exports.restart_interaction();result=True')
   await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance();await q.wait('r13_hub');await q.shot('fresh-start')
   await q.press('메뉴');await q.press('저장 · 불러오기');await q.wait('save');await q.press('1쪽 1번');await q.press('돌아가기');await q.wait('r13_hub')
   await q.press('메뉴');await q.press('메인화면');await q.wait('confirm');await q.press('예');await q.wait('main_menu');await q.shot('title-with-save')
   st=await q.state();assert any('이어하기' in v['text'] for v in st['buttons']),st
   menu=[v for v in st['buttons'] if v['text'].strip() in ('이어하기','처음부터','불러오기','설정')]
   assert len(menu)==4,menu
   assert len({tuple(v['rect'][2:]) for v in menu})==1,menu
   assert len({v['rect'][0] for v in menu})==2,menu
   assert len({v['rect'][1] for v in menu})==2,menu
   positions={v['text'].strip():tuple(v['rect'][:2]) for v in menu}
   columns=sorted({pos[0] for pos in positions.values()})
   rows=sorted({pos[1] for pos in positions.values()})
   assert positions=={'이어하기':(columns[0],rows[0]),'처음부터':(columns[1],rows[0]),
                      '불러오기':(columns[0],rows[1]),'설정':(columns[1],rows[1])},positions
   for v in st['buttons']:
    x,y,w,h=v['rect'];assert y+h<=720 and x+w<=1280,v
   await q.press('불러오기');await q.wait('load');await q.shot('title-load');await q.press('돌아가기');await q.wait('main_menu')
   await q.press('이어하기');await q.wait('r13_hub');await q.shot('continued-game')
   info={'passed':True,'checks':['fresh title disables unavailable continue/load and focuses new game','down-arrow keyboard focus moves from new game to settings','settings returns to title','music credits opens and closes','motion-off title remains readable','844x390 touch settings and return','new game reaches the gate hub','save and return confirmation','four equally sized menu controls occupy the approved two rows and two columns within bounds','load screen returns and continue resumes saved hub'],'version':(await q.info())['version']}
   (OUT/'result.json').write_text(json.dumps(info,ensure_ascii=False,indent=2));print('PASS',info,flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await b.close()
asyncio.run(main())
