import asyncio,json,sys
from pathlib import Path
sys.path.insert(0,'dev')
from playwright.async_api import async_playwright
from webqa import UIQA,FLOW_PROBE
import os
OUT=Path(os.environ.get('ROOM13_UI_QA_OUT','/tmp/room13-direct-investigation'))
class Q(UIQA):
 async def py(self,code):return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)
 async def state(self):
  probe=FLOW_PROBE.replace('names=[',"names=['r13_resident_approach','r13_meeting_agenda','r13_debate_board','r13_records',")
  st=await self.py('ns={};exec('+ascii(probe)+',ns);result=ns["result"]');assert '_exception'not in st['screens'],st;return st
 async def jump(self,label):
  code='\n'.join(['import renpy','def qa_jump(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 시작",clicked=s.Jump('+repr(label)+'),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_jump',qa_jump,modal='True',zorder='200')","renpy.exports.show_screen('qa_jump')","renpy.exports.restart_interaction()","result=True"])
  await self.py(code);await self.press('검토 시작');await self.py('import renpy;renpy.exports.hide_screen("qa_jump");renpy.exports.restart_interaction();result=True')
 async def until(self,name):
  for _ in range(100):
   st=await self.state()
   if name in st['screens']:await asyncio.sleep(.4);return st
   if 'say'in st['screens']:await self.input(810,610)
   else:await asyncio.sleep(.2)
  raise AssertionError((name,st))
async def main():
 report={'kind':'Isolated design prototype; not a production release','checks':[]}
 async with async_playwright() as p:
  OUT.mkdir(parents=True,exist_ok=True)
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=Q(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8776/preview/room13-dev/')
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000)
   await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.preferences.afm_enable=False;result=True')
   await q.press('처음부터');await q.press('씬 건너뛰기');await q.wait('say')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("say");s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="inn",evidence=["E01"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.persistent.room13_motion=False;s.persistent.room13_large_text=False;s.persistent.r13_pan_hint_seen=True;s.config.variants=[v for v in s.config.variants if v!="touch"];s.r13_world_cameras={};s.r13_field_location=None;s.place=s.R13_PLACES["inn"][0];s.r13_scene_bg=s.R13_PLACES["inn"][1];s.r13_carriage_skip=False;renpy.exports.scene();renpy.exports.show("qa_bg",what=s.r13_background(s.r13_scene_bg));result=True')
   await q.jump('r13_field');await q.wait('r13_hub');await q.press('할머니');await q.until('r13_resident_approach');await q.press('아내 편지');await q.wait('say')
   await q.shot('01-pc-dialogue')
   st=await q.state();labels=[v['text'].strip() for v in st['buttons']];assert '기록' in labels and '더보기' in labels and not any(v in labels for v in ('백로그','자동','대사 건너뛰기')),labels
   await q.press('더보기');await q.shot('02-pc-more');await page.keyboard.press('Escape');await q.wait('say')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True;await asyncio.sleep(.4);await q.shot('03-mobile-dialogue')
   before=await q.room();line=(await q.state())['say']
   await q.press('더보기');await q.shot('04-mobile-more');assert await q.room()==before
   await q.press('현재 대화 건너뛰기');await q.shot('05-mobile-skip-confirm');assert await q.room()==before
   await q.press('계속 읽기');await q.wait('say');assert await q.room()==before and (await q.state())['say']==line
   report['checks'].append('Playback helpers absent from dialogue dock; More is rightmost; More and skip-cancel preserve exact story and current line')
   await q.press('더보기');await q.press('대화 기록');await asyncio.sleep(.4);await q.shot('06-mobile-backlog');await q.press('대화로 돌아가기');await q.wait('say');assert await q.room()==before
   await q.py('import renpy;renpy.store.preferences.afm_time=99;result=True')
   await q.press('더보기');await q.press('자동 읽기');await q.shot('06b-mobile-auto-running')
   assert await q.py('import renpy;result=renpy.store.preferences.afm_enable')
   await q.press('자동 읽기 중');assert not await q.py('import renpy;result=renpy.store.preferences.afm_enable')
   report['checks'].append('Auto is entered from More; the visible running indicator stops it with a real tap')
   await q.until('r13_topics');await q.py('import renpy;renpy.store.preferences.afm_enable=True;renpy.exports.restart_interaction();result=True');await q.shot('07-mobile-questions')
   assert not any('자동 읽기 중' in v['text'] for v in (await q.state())['buttons'])
   await q.py('import renpy;renpy.store.preferences.afm_enable=False;result=True')
   st=await q.state();actions=[v for v in st['buttons'] if v['text'].strip() in ('자료 보여주기','기록','더보기')];assert [v['text'].strip() for v in sorted(actions,key=lambda a:a['rect'][0])]==['자료 보여주기','기록','더보기'],actions
   assert all(v['rect'][3]==80 for v in actions),actions
   before=await q.room();await q.press('자료 보여주기');await q.wait('r13_book');await q.press('그만두기');await q.wait('r13_topics');assert await q.room()==before
   await q.press('기록');await asyncio.sleep(.3);await q.press('닫기');await q.wait('r13_topics');assert {k:v for k,v in (await q.room()).items() if k!='record_ui'}=={k:v for k,v in before.items() if k!='record_ui'}
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False;await asyncio.sleep(.3);await q.shot('08-pc-questions')
   report['checks'].append('PC and mobile actual NPC questions retain primary presentation; material and record cancellation return to same questions; mobile outer tap targets remain 80 high')
   report['passed']=True
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'))
   try:report['failure_state']=await q.state()
   except:pass
   raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='failure_state'},ensure_ascii=False),flush=True);await b.close()
asyncio.run(main())
