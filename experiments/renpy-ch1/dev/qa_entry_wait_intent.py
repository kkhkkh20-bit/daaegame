"""Focused real-dispatcher check: waiting is explicit and cancellation is harmless."""
import asyncio,json,os,sys
from pathlib import Path
sys.path.insert(0,'dev')
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-entry-wait'))
class Q(UIQA):
 async def py(self,code):
  return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)
async def main():
 OUT.mkdir(parents=True,exist_ok=True)
 report={'kind':'Day-1 entry UI fixture; actual guard dispatcher, not full gameplay','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://localhost:8776/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000)
   await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=1,period=1,location="gate",evidence=["E01"]);s.room13_mode=True;s.persistent.room13_motion=False;s.r13_meeting_active=False;s.place=s.R13_PLACES["gate"][0];s.r13_scene_bg=s.R13_PLACES["gate"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   code='\n'.join(['import renpy','def qa_jump(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 시작",clicked=s.Jump("r13_entry_guard_menu"),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_jump',qa_jump,modal='True',zorder='200')","renpy.exports.show_screen('qa_jump')","renpy.exports.restart_interaction()","result=True"])
   await q.py(code);await q.press('검토 시작');await q.py('import renpy;renpy.exports.hide_screen("qa_jump");renpy.exports.restart_interaction();result=True');await q.wait('r13_entry_topics')
   for mobile in [False,True]:
    tag='mobile' if mobile else 'pc';q.touch=mobile
    await page.set_viewport_size({'width':844 if mobile else 1280,'height':390 if mobile else 720})
    await q.py('import renpy;renpy.store.persistent.room13_large_text='+repr(mobile)+';renpy.exports.restart_interaction();result=True')
    await q.shot(tag+'-guard-questions');before=await q.room()
    await q.press('원본 담당자를 기다리겠습니다.');await q.wait('r13_confirm');await q.shot(tag+'-wait-confirm')
    assert await q.room()==before
    await q.press('돌아간다');await q.wait('r13_entry_topics');assert await q.room()==before
    await q.press('자료 보여주기');await q.wait('r13_book');await q.press('그만두기');await q.wait('r13_entry_topics');assert await q.room()==before
    report['checks'].append(tag+': explicit wait opens confirmation; cancel and separate evidence presentation preserve complete state and return to guard questions')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
