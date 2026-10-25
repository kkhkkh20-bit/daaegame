from playwright.sync_api import sync_playwright
from pathlib import Path
import json
out=Path('/workspace/daaegame/experiments/renpy-ch1/docs/reviews/codex-03')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader'])
 page=b.new_page(viewport={'width':1280,'height':720})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 try:
  page.goto('http://127.0.0.1:8765/preview/room13-dev/',wait_until='domcontentloaded')
  page.wait_for_function("typeof renpy_exec === 'function'",timeout=60000)
  page.wait_for_timeout(10000)
  result=page.evaluate("async()=>await renpy_exec(\"import renpy; result={'version':renpy.store.config.version,'menu':bool(renpy.display.screen.get_screen('main_menu'))}\")")
  print(result,flush=True)
  page.screenshot(path=str(out/'기존웹_실행확인.png'))
  def py(code):
   return page.evaluate("code=>Promise.race([renpy_exec(code),new Promise((_,r)=>setTimeout(()=>r(Error('응답 시간 초과')),30000))])",code)
  print('fixture',py("import renpy; s=renpy.store; s.room13=s.r13_new(); s.room13.update(day=3,period=0,location='gate',life_poc=True); s.room13['flags']=['entry_corrected','lodging','livelihood_open']; renpy.exports.show_screen('r13_map',initial_region='village'); renpy.exports.restart_interaction(); result=s.r13_places()"),flush=True)
  page.wait_for_timeout(3000)
  print('before',py("import renpy; s=renpy.store; v=renpy.display.screen.get_widget('r13_map','r13_map_view'); result={'selected':renpy.display.screen.get_screen('r13_map').scope['selected'],'scroll':[v.xadjustment.value,v.yadjustment.value],'river':s.r13_cart_label_point('river')}"),flush=True)
  page.mouse.move(1100,450);page.mouse.down();page.mouse.move(550,200,steps=20);page.mouse.up();page.wait_for_timeout(1000)
  print('drag',py("import renpy; v=renpy.display.screen.get_widget('r13_map','r13_map_view'); result=[v.xadjustment.value,v.yadjustment.value]"),flush=True)
  page.mouse.wheel(0,250);page.wait_for_timeout(1000)
  page.keyboard.press('Shift+ArrowRight');page.wait_for_timeout(1000)
  pos=py("import renpy; v=renpy.display.screen.get_widget('r13_map','r13_map_view'); x,y=renpy.store.r13_cart_label_point('river'); result=[16+x-v.xadjustment.value,y-v.yadjustment.value]")
  print('river_screen',pos,flush=True)
  page.screenshot(path=str(out/'기존웹_강가_이동후.png'))
  assert 16<pos[0]<1264 and 0<pos[1]<548,pos
  page.mouse.click(*pos);page.wait_for_timeout(1000)
  selected=py("import renpy; result=renpy.display.screen.get_screen('r13_map').scope['selected']")
  print('selected',selected,flush=True)
  assert selected=='river',selected
  page.screenshot(path=str(out/'기존웹_강가_선택.png'))
 except Exception as e: print(type(e).__name__,str(e),flush=True)
 print('pageerrors',json.dumps(errors,ensure_ascii=False),flush=True)
 b.close()
