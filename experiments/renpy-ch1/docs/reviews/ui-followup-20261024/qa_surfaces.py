"""Disposable web-engine source review; does not rebuild or modify release files."""
import asyncio,json,sys,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent/'captures'
sys.path.insert(0,str(ROOT/'dev'))
from playwright.async_api import async_playwright
from webqa import UIQA

async def load_screens(q,path):
 source=(ROOT/'game'/path).read_text()
 await q.py('import renpy;renpy.store.ui_followup_nodes=renpy.game.script.load_string('+repr('qa-'+path.replace('/','-'))+','+repr(source)+');result=True')
 await q.py('''import renpy
queue=list(renpy.store.ui_followup_nodes[0])
while queue:
 n=queue.pop(0)
 if isinstance(n,(list,tuple)):queue.extend(n)
 elif isinstance(n,renpy.ast.Init):queue.extend(n.block)
 elif isinstance(n,renpy.ast.Screen):n.execute()
renpy.exports.restart_interaction()
result=True''')

async def main():
 OUT.mkdir(exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  pg=await b.new_page(viewport={'width':1280,'height':720},has_touch=True)
  q=UIQA(pg,OUT);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await pg.goto('http://127.0.0.1:8765/preview/room13-dev/')
   await pg.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=150000)
   await q.wait('main_menu');await asyncio.sleep(3);await q.shot('main-current-desktop')
   await q.press('처음부터');await q.wait('say')
   await q.py('''import renpy
s=renpy.store
s.r13_edit(day=2,period=0,location="inn",flags=["lodging","entry_corrected"])
s.r13_black_card=False
s.r13_thought_active=False
s.r13_camera="stage"
s.place="여관 · 접수대"
s.preferences.text_cps=0
s.r13_packet=("granny","잘 왔구나. 여기 앉아서 천천히 이야기하자.")
s.r13_directed_pose="joy"
s.r13_expression="expressive"
renpy.exports.scene()
renpy.exports.show("qa_background",what=s.r13_background(s.R13_PLACES["inn"][1]))
s.r13_speaker("granny","expressive","joy")
renpy.exports.show_screen("say",who=s.R13_NAMES["granny"],what=s.r13_packet[1])
renpy.exports.restart_interaction()
result=True''')
   await q.shot('dialogue-before-desktop')
   await load_screens(q,'systems/room13_night_ui.rpy')
   await q.shot('dialogue-after-desktop')
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('renpy.store.r13_set_text_size("large");renpy.exports.restart_interaction();result=True')
   await q.shot('dialogue-after-mobile-large')
   for _ in range(3):
    await q.press('더보기');await q.press('설정');await q.wait('pause_menu');await q.press('닫기');await q.wait('say')
   await pg.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('''import renpy
s=renpy.store
s.r13_set_text_size("normal")
renpy.exports.hide_screen("r13_more_tools")
renpy.exports.hide_screen("say")
renpy.exports.scene()
renpy.exports.show("qa_background",what=s.r13_background(s.R13_PLACES["inn"][1]))
s.ui_followup_choice=0
s.ui_followup_entries=[("이 마을은 어떤 곳인가요?",s.Function(setattr,s,"ui_followup_choice",1),False),("오늘 아침에 누가 다녀갔나요?",s.Function(setattr,s,"ui_followup_choice",2),True),("여관에 도착했을 때 보았던 물건에 대해 조금 더 자세히 말씀해 주실 수 있나요?",s.Function(setattr,s,"ui_followup_choice",3),False)]
renpy.exports.show_screen("r13_side_question_list",person="granny",pose="joy",entries=s.ui_followup_entries,ready=True,return_action=s.Hide("r13_side_question_list"))
renpy.exports.restart_interaction()
result=True''')
   await q.shot('questions-before-desktop')
   src=(ROOT/'game/systems/room13_side_questions.rpy').read_text().split('init 80 python:\n',1)[1].split('\nscreen ',1)[0]
   await q.py('exec('+repr(textwrap.dedent(src))+',renpy.store.__dict__);result=True')
   await load_screens(q,'systems/room13_side_questions.rpy')
   await q.shot('questions-after-desktop')
   await pg.mouse.move(800,215);await asyncio.sleep(.5);await q.shot('questions-after-hover')
   await pg.keyboard.press('2');await asyncio.sleep(.3)
   assert await q.py('result=renpy.store.ui_followup_choice')==2
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('renpy.store.r13_set_text_size("large");renpy.exports.restart_interaction();result=True')
   await q.shot('questions-after-mobile-large')
   await q.press('다음 질문');await q.shot('questions-long-mobile-large');await q.press('여관에 도착했을 때')
   assert await q.py('result=renpy.store.ui_followup_choice')==3
   await q.py('''import renpy
s=renpy.store
s.ui_followup_many=s.ui_followup_entries*4
renpy.exports.show_screen("r13_side_question_list",person="granny",pose="joy",entries=s.ui_followup_many,ready=True,return_action=s.Hide("r13_side_question_list"))
renpy.exports.restart_interaction()
result=True''')
   await q.shot('questions-many-mobile-large')
   for _ in range(3):
    await q.press('다음 질문');await q.press('이전 질문')
   bounds=await q.py('''import renpy
s=renpy.store
pages=s.r13_side_question_pages(s.ui_followup_many)
result={"pages":len(pages),"rows":sum(len(p) for p in pages),"bottoms":[s.R13_SIDE_QUESTION_TOP+42+sum(h for e,h in p)+8*(len(p)-1) for p in pages],"limit":s.r13_control_upper_y()-96}''')
   assert bounds['rows']==12 and all(y<bounds['limit'] for y in bounds['bottoms']),bounds
   for _ in range(3):
    await q.press('돌아가기')
    assert await q.py('result=renpy.get_screen("r13_side_question_list") is None')
    await q.py('renpy.exports.show_screen("r13_side_question_list",person="granny",pose="joy",entries=renpy.store.ui_followup_many,ready=True,return_action=renpy.store.Hide("r13_side_question_list"));renpy.exports.restart_interaction();result=True')
   assert not errors,errors
   (OUT/'surfaces-result.json').write_text(json.dumps({'engine':'0.20.28 web','method':'temporary source load, not rebuilt release','dialogue_settings_return_cycles':3,'question_return_cycles':3,'question_page_cycles':3,'keyboard':True,'touch':True,'bounds':bounds,'pageerrors':errors},ensure_ascii=False,indent=2))
  finally:await b.close()
asyncio.run(main())
