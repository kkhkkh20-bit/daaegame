"""B notebook visual integration in the shipped web engine, disposable profile."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/r13-notebook-browser'))
OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True)
  q=UIQA(page,OUT);errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  async def settled_shot(name):
   await page.wait_for_load_state('networkidle',timeout=60000)
   await asyncio.sleep(1.5)
   await q.shot(name)
  try:
   await page.goto(URL)
   await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=150000)
   await q.wait('main_menu');await settled_shot('01-main-desktop')
   await q.press('설정');await q.wait('pause_menu');await settled_shot('02-settings')
   await q.press('닫기');await q.wait('main_menu')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await settled_shot('03-main-mobile')
   await q.press('처음부터');await q.wait('say')
   await q.py('''import renpy
s=renpy.store
s.r13_edit(day=2,period=0,location="inn",flags=["lodging","entry_corrected"])
s.room13.pop("v111",None)
s.r13_black_card=False
s.r13_thought_active=False
s.r13_camera="stage"
s.place="여관 · 접수대"
s.preferences.text_cps=0
s.persistent.room13_window_alpha="d4"
s.r13_packet=("granny","잘 왔구나. 여기 앉아서 천천히 이야기하자.")
s.r13_directed_pose="joy"
s.r13_expression="expressive"
renpy.exports.scene()
renpy.exports.show("qa_background",what=s.r13_background(s.R13_PLACES["inn"][1]))
s.r13_speaker("granny","expressive","joy")
renpy.exports.show_screen("say",who=s.R13_NAMES["granny"],what=s.r13_packet[1])
renpy.exports.restart_interaction()
result=True''')
   await settled_shot('04-dialogue-mobile')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await settled_shot('05-dialogue-desktop')
   await q.py('''import renpy
s=renpy.store
renpy.exports.hide_screen("say")
renpy.exports.hide("r13_visitor")
s.r13_qa_ui_pick=0
entries=[("마을에 관해서",s.SetVariable("r13_qa_ui_pick",1),False),("장터에 관해서",s.SetVariable("r13_qa_ui_pick",2),True),("이곳의 겨울에 관해서",s.SetVariable("r13_qa_ui_pick",3),False),("이곳에 오기 전에는",s.SetVariable("r13_qa_ui_pick",4),False),("여관에 관해서",s.SetVariable("r13_qa_ui_pick",5),False),("다시 물어볼 이야기",s.SetVariable("r13_qa_ui_pick",6),True)]
renpy.exports.show_screen("r13_side_question_list",person="granny",pose="joy",entries=entries,ready=True,return_action=s.Hide("r13_side_question_list"))
renpy.exports.show_screen("r13_notebook_topic_tools",ready=True,person="granny",present_action=s.NullAction())
renpy.exports.restart_interaction()
result=True''')
   await settled_shot('06-questions-desktop')
   await q.press('장터에 관해서')
   assert await q.py('result=renpy.store.r13_qa_ui_pick==2')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.py('renpy.store.r13_set_text_size("large");renpy.exports.restart_interaction();result=True')
   await settled_shot('07-questions-mobile')
   await q.press('다음 질문');await settled_shot('08-questions-mobile-page2')
   await q.py('''import renpy
s=renpy.store
renpy.exports.hide_screen("r13_side_question_list")
renpy.exports.hide_screen("r13_notebook_topic_tools")
entries=[("마지막 줄을 본다",s.SetVariable("r13_qa_ui_pick",1),False),("글씨를 살핀다",s.SetVariable("r13_qa_ui_pick",2),False),("편지를 접는다",s.SetVariable("r13_qa_ui_pick",3),False)]
renpy.exports.show_screen("r13_notebook_choice_list",person="granny",pose="joy",title="선택",entries=entries,ready=True,caption="편지를 살펴볼까?")
renpy.exports.restart_interaction()
result=True''')
   await settled_shot('09-choices-mobile')
   await q.press('글씨를 살핀다')
   assert await q.py('result=renpy.store.r13_qa_ui_pick==2')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('renpy.store.r13_set_text_size("normal");renpy.exports.restart_interaction();result=True')
   await settled_shot('10-choices-desktop')
   await q.py('renpy.exports.hide_screen("r13_notebook_choice_list");renpy.exports.show_screen("r13_map",initial_region="inn");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_map');await settled_shot('11-map-inn')
   await q.press('마을')
   await page.wait_for_function("performance.getEntriesByType('resource').some(e=>e.name.includes('room13-map-village.webp') && e.responseEnd>0)",timeout=60000)
   await settled_shot('12-map-village')
   assert not errors,errors
   result={'passed':True,'version':(await q.info())['version'],'pageerrors':errors,'checks':['main/settings PC and mobile','dialogue paper','read questions remain actionable','mobile pagination','paper choice actions','original map image loaded before capture']}
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
   print('PASS',result,flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:await browser.close()

if __name__=='__main__':asyncio.run(main())
