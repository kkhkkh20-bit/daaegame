import asyncio,json,sys,os
from pathlib import Path
sys.path.insert(0,'dev')
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-side-questions-qa'))
OUT.mkdir(parents=True,exist_ok=True)
class Q(UIQA):
 async def py(self,code): return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)
async def main():
 report={'kind':'Actual conversation dispatcher plus 0/8/12-topic layout fixtures; fixture topics combine story stages and repeat some labels, not simultaneous eligibility or a full playthrough','checks':[],'captures':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000)
   await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");renpy.exports.hide("r13_visitor");s.r13_edit(day=3,period=0,location="workshop",flags=["entry_corrected","lodging"]);s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.r13_camera="stage";s.r13_meeting_active=False;s.r13_cg_active=False;s.r13_thought_active=False;s.place=s.R13_PLACES["workshop"][0];s.r13_scene_bg=s.R13_PLACES["workshop"][1];s.r13_target="buri";renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));s.qa_topics_original=s.r13_topics_in_order;s.qa_safe_original=s.r13_safe_question_action;result=True')
   # Actual authored topic titles, including later stages: visual fixtures only.
   await q.py('import renpy;s=renpy.store;s.qa_buri=[(k,v) for k,v in s.ROOM13["topics"].items() if v.get("npc")=="buri"][:8];result=True')
   for width,height,big,prefix in [(1280,720,False,'pc'),(844,390,True,'mobile')]:
    await page.set_viewport_size({'width':width,'height':height});q.touch=big
    await q.py('import renpy;renpy.store.persistent.room13_large_text='+repr(big)+';result=True')
    for count in [0,8,12]:
     await q.py('import renpy;s=renpy.store;s.qa_rows=(s.qa_buri*2)[:'+str(count)+'];s.r13_topics_in_order=lambda person,rows=s.qa_rows:rows;renpy.exports.hide_screen("r13_topics");renpy.exports.show_screen("r13_topics",person="buri");renpy.exports.restart_interaction();result=True')
     await asyncio.sleep(.5);await page.mouse.move(5,5);await q.shot(prefix+'-'+str(count));report['captures'].append(prefix+'-'+str(count))
     st=await q.state()
     for button in st['buttons']:
      x,y,w,h=button['rect'];assert x>=0 and y>=0 and x+w<=1281 and y+h<=721,button
     if count==12:
      before=await q.room();await q.press('다음 질문');await q.shot(prefix+'-12-page2');assert await q.room()==before
      st=await q.state();assert any('이전 질문' in x['text'] for x in st['buttons'])
      await q.py('import renpy;s=renpy.store;s.qa_selected=None;s.qa_expected=s.r13_side_question_pages([(s.r13_calendar_topic_title(k,v),s.Return(k),False) for k,v in s.qa_rows])[1][0][0][1].value;s.r13_safe_question_action=lambda action,store=s:store.SetVariable("qa_selected",action.value);renpy.exports.restart_interaction();result=True')
      await page.keyboard.press('1');await asyncio.sleep(.4)
      assert await q.py('import renpy;s=renpy.store;result=s.qa_selected==s.qa_expected')
      await q.py('import renpy;s=renpy.store;s.r13_safe_question_action=s.qa_safe_original;renpy.exports.restart_interaction();result=True')
      await q.press('이전 질문');assert await q.room()==before
      report['checks'].append(prefix+' explicit pagination forward/back preserves complete state')
   await q.py('import renpy;s=renpy.store;s.r13_topics_in_order=s.qa_topics_original;renpy.exports.hide_screen("r13_topics");s.persistent.room13_large_text=False;result=True')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   # Enter the actual dispatcher, rather than merely showing a screen.
   code='\n'.join(['import renpy','def qa_jump(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 계속",clicked=s.Jump("r13_talk_menu"),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_jump',qa_jump,modal='True',zorder='200')","renpy.exports.show_screen('qa_jump')","renpy.exports.restart_interaction()","result=True"])
   await q.py(code);await q.press('검토 계속');await q.py('import renpy;renpy.exports.hide_screen("qa_jump");renpy.exports.restart_interaction();result=True');await q.wait('r13_topics')
   await q.shot('pc-actual-topics')
   for mobile in [False,True]:
    if mobile:
     await page.set_viewport_size({'width':844,'height':390});q.touch=True
     await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
    before=await q.room();await q.press('자료 보여주기');await q.wait('r13_book');await q.press('그만두기');await q.wait('r13_topics');assert await q.room()==before
    await q.press('기록');assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records") is not None');await q.press('닫기');await q.wait('r13_topics');assert await q.room()==before
    report['checks'].append(('mobile' if mobile else 'pc')+' actual present/record/cancel retains state and returns to topics')
   await q.shot('mobile-actual-topics')
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;renpy.store.persistent.room13_large_text=False;renpy.exports.restart_interaction();result=True')
   before=await q.py('import renpy;s=renpy.store;result=[k for k,v in s.r13_topics_in_order("buri")]')
   assert before
   await page.keyboard.press('1');await q.wait('say');await q.shot('selected-question-dialogue')
   for _ in range(80):
    st=await q.state()
    if 'r13_topics' in st['screens']:break
    if 'choice' in st['screens']:
     raise AssertionError('Unexpected story choice in selected topic')
    await q.input(810,640)
   await q.wait('r13_topics');await q.shot('read-topic-return')
   assert await q.py('import renpy;s=renpy.store;result=s.r13_calendar_topic_seen('+repr(before[0])+',s.ROOM13["topics"].get('+repr(before[0])+',{}))')
   report['checks'].append('numeric shortcut selects actual first question, dialogue plays, returns as read')
   await q.press('돌아가기');await asyncio.sleep(.6);st=await q.state();assert 'r13_topics' not in st['screens'];report['checks'].append('actual back closes topics (dispatcher fixture resumes opening context)')
   assert not await q.py('import renpy;result=renpy.display.screen.get_screen("_exception") is not None')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
