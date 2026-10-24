import asyncio,sys,json,textwrap
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'dev'))
from playwright.async_api import async_playwright
from webqa import UIQA
root=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent/'captures';out.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  pg=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=UIQA(pg,out);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await pg.goto('http://127.0.0.1:8765/preview/room13-dev/');await pg.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=90000)
   await q.wait('main_menu');await q.press('처음부터');await q.wait('say')
   setup='''import renpy
s=renpy.store
s.r13_black_card=False
s.r13_thought_active=False
s.place='마차 안'
s.preferences.text_cps=0
s._history_list=[]
renpy.exports.hide_screen('say')
renpy.exports.scene()
renpy.exports.show('qa_ui_background',what=s.r13_background('winter'))
entries=[('이 마을에 대해 먼저 물어본다.',s.NullAction(),False),('편지에 적힌 내용을 천천히 다시 읽어 보고, 마을에 도착하기 전에 무엇을 알아 두어야 할지 다람이와 이야기해 본다.',s.Function(setattr,s,'ui_review_choice',2),False),('창밖으로 보이는 마을과 길을 자세히 살펴본다.',s.NullAction(),False)]
renpy.exports.show_screen('r13_carriage_choice_list',entries=entries,ready=True,caption='어떻게 할까?')
renpy.exports.restart_interaction()
result=True'''
   await q.py(setup);await asyncio.sleep(2);await q.shot('carriage-before')
   await pg.set_viewport_size({'width':844,'height':390});await q.shot('carriage-mobile-before');await pg.set_viewport_size({'width':1280,'height':720})
   src=(root/'game/systems/room13_reference_ui.rpy').read_text().split('init 79 python:\n',1)[1].split('    # Summaries',1)[0]
   await q.py('import renpy;exec('+repr(textwrap.dedent(src))+',renpy.store.__dict__);result=True')
   screen=(root/'game/systems/room13_carriage_choices.rpy').read_text()
   print(await q.py('import renpy;renpy.store.ui_review_nodes=renpy.game.script.load_string("ui-review-carriage.rpy",'+repr(screen)+');result=repr(renpy.store.ui_review_nodes)[:1500]'),flush=True)
   print(await q.py('''import renpy
queue=list(renpy.store.ui_review_nodes[0])
found=[]
while queue:
 n=queue.pop(0)
 if isinstance(n,(list,tuple)):queue.extend(n)
 elif isinstance(n,renpy.ast.Init):queue.extend(n.block)
 elif isinstance(n,renpy.ast.Screen):
  n.execute()
  found.append('screen executed')
result=found'''),flush=True)
   await q.py(setup);await asyncio.sleep(2);await q.shot('carriage-after-runtime')
   await pg.mouse.move(300,270);await q.shot('carriage-after-hover-runtime')
   for i in range(3):
    await q.py("renpy.exports.hide_screen('r13_carriage_choice_list');renpy.exports.restart_interaction();result=True")
    await q.py(setup)
   await pg.set_viewport_size({'width':844,'height':390});await q.shot('carriage-mobile-after-runtime')
   await pg.keyboard.press('2');await asyncio.sleep(.5)
   assert await q.py('result=getattr(renpy.store,"ui_review_choice",None)')==2
   await q.py('renpy.store.ui_review_choice=0;result=True')
   q.touch=True;await q.input(250,370)
   assert await q.py('result=renpy.store.ui_review_choice')==2
   assert not errors,errors
   (out/'runtime-review.json').write_text(json.dumps({'engine':'RenPy web 0.20.28','method':'disposable runtime loads changed source; NOT rebuilt release','cycles':3,'keyboard_2':True,'touch_second_choice':True,'long_caption':True,'pageerrors':errors},ensure_ascii=False,indent=2))
  finally:await b.close()
asyncio.run(main())
