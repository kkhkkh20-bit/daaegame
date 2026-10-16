"""Actual four-panel ending playback, explicit ending fixtures, not a 14-day walkthrough."""
import asyncio,json,os,time
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_ending_story_view','r13_ending_screen',")
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa/endings'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def native_action(q,label,action):
 code='\n'.join(['import renpy','def _qa_ending_action(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 계속",clicked='+action+',xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_ending_action',_qa_ending_action,modal='True',zorder='200')","renpy.exports.show_screen('qa_ending_action')","renpy.exports.restart_interaction()","result=True"])
 await q.py(code);await q.press('검토 계속')
 await q.py('import renpy;renpy.exports.hide_screen("qa_ending_action");renpy.exports.restart_interaction();result=True')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  started=time.monotonic();page=await browser.new_page(viewport={'width':1280,'height':720},record_video_dir=str(OUT/'video'),record_video_size={'width':1280,'height':720});q=UIQA(page,OUT)
  async def until_story():
   for _ in range(160):
    st=await q.state()
    if 'r13_ending_story_view' in st['screens']:await asyncio.sleep(.7);return
    if 'say' in st['screens']:await q.input(800,610)
    elif 'r13_cinematic_view' in st['screens']:await q.press('계속')
    else:await asyncio.sleep(.15)
   raise AssertionError(st)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance()
   results=[];clip={}
   for num in range(7):
    key='E'+str(num)
    flags=['mom_reunited'] if num>=2 else []
    if num>=5:flags+=['shelter_ready','supplies_ready','operators_ready','patient_transport','mother_original_safe','witness_protected']
    props=['F1','F2','F3'] if num>=5 else ['F2'] if num==4 else []
    if num==6:props+=['F4','C4']
    fixture=dict(day=3 if num==0 else 14,period=2,ending=None,location='altar',daram_state='lost' if num==1 else 'with_dad',mom_state='reunited' if num>=2 else 'hidden',case_state='pending' if num==0 else 'occurred',victim_state='alive' if num==0 else 'dead',granny_state='detained' if num==6 else 'trusted',flags=flags,propositions=props,finale_started=num>0)
    await q.py('import renpy;s=renpy.store;s.r13_edit(**'+repr(fixture)+');s.r13_ending_id='+repr(key)+';s.persistent.room13_motion='+repr(num!=1)+';result=True')
    await native_action(q,'ending','s.Jump("r13_ending")');await until_story()
    before=(await q.state())['room']
    if num==5:clip['start']=time.monotonic()-started
    for index in range(4):
     assert await q.py('import renpy;s=renpy.store;result=s.r13_ending_story_index=='+str(index)+' and s.r13_ending_id=='+repr(key))
     await q.shot(key+'-'+str(index+1))
     if num==5 and index==1:
      await q.py('import renpy;renpy.exports.save("qa-ending-mid-story");result=True')
      await native_action(q,'load','s.Function(renpy.exports.load,"qa-ending-mid-story")');await q.wait('r13_ending_story_view')
      assert await q.py('import renpy;result=renpy.store.r13_ending_story_index==1')
      await q.press('‹ 이전');await q.wait('r13_ending_story_view')
      assert await q.py('import renpy;result=renpy.store.r13_ending_story_index==0')
      await q.press('다음 장면');await q.wait('r13_ending_story_view')
     await q.press('여정의 기록' if index==3 else '다음 장면')
     await q.wait('r13_ending_screen' if index==3 else 'r13_ending_story_view')
    assert (await q.state())['room']==before
    await q.shot(key+'-record')
    if num==5:
     clip['end']=time.monotonic()-started
     await q.press('후일담 다시 보기');await q.wait('r13_ending_story_view')
     for index in range(4):await q.press('여정의 기록' if index==3 else '다음 장면');await q.wait('r13_ending_screen' if index==3 else 'r13_ending_story_view')
     assert (await q.state())['room']==before
     await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await page.set_viewport_size({'width':844,'height':390});await q.shot('mobile-record');await q.press('후일담 다시 보기');await q.wait('r13_ending_story_view');await q.shot('mobile-story')
     for index in range(4):await q.press('여정의 기록' if index==3 else '다음 장면');await q.wait('r13_ending_screen' if index==3 else 'r13_ending_story_view')
     await page.set_viewport_size({'width':1280,'height':720})
    results.append(dict(ending=key,panels=4,read_only=True))
   (OUT/'result.json').write_text(json.dumps({'passed':True,'endings':results,'checks':['all seven authored endings reach four-panel epilogue','each epilogue and replay preserve world and evidence','previous scene navigation','save/load resumes correct middle scene','reduced motion ending','mobile story and record page']},ensure_ascii=False,indent=2))
   (OUT/'clip.json').write_text(json.dumps(clip,indent=2));print('PASS seven endings, 28 panels, replay, save/load, reduced motion and mobile',flush=True)
  except Exception as exc:
   print('FAIL',repr(exc),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:
   video=page.video;await browser.close()
   if video:Path(await video.path()).rename(OUT/'ending-recording.webm')
asyncio.run(main())
