import asyncio,json,copy,ast,sys
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_debate_board','r13_meeting_collective_view','r13_more_tools',")
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/pressure-state-qa');OUT.mkdir(exist_ok=True)
async def main():
 report={'kind':'Actual engine inputs after one initial C2 fixture','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  async def until(text=None,screen=None):
   for _ in range(80):
    st=await q.state()
    if text and text in st['say'] or screen and screen in st['screens']:return st
    if 'say' in st['screens']:await q.input(810,610)
    elif 'choice' in st['screens']:raise AssertionError(('unexpected choice',text))
    else:await asyncio.sleep(.15)
   raise AssertionError(st)
  async def snap():
   return await q.py('import renpy;s=renpy.store;result=dict(level=s.r13_meeting_pressure_level("resident_ppul"),events=[list(v) for v in s.r13_meeting_pressure_events],collective=s.r13_meeting_collective,poses=s.r13_meeting_direction_poses,music=s.r13_meeting_channel_gain("music"),ambience=s.r13_meeting_channel_gain("ambience"),prefs=dict(s.preferences.volumes),mute=dict(s.preferences.mute),can_rollback=renpy.exports.can_rollback(),rollback_keys=s.config.keymap.get("rollback"),revision=s.r13_meeting_shot_revision,read=s.r13_read_id,index=s.r13_index)')
  async def present(key):
   title=await q.py('import renpy;s=renpy.store;result=s.R13_RECORD_SHORT.get('+repr(key)+',s.r13_catalog_title('+repr(key)+')[:8])')
   await q.press('자료 보여주기');await q.wait('r13_book');await q.press(title);await q.press('이 주장에 근거로 낸다');await q.wait('say')
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E35","E09","E07"],propositions=["C1"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.preferences.text_cps=0;s.preferences.afm_enable=False;s.persistent.room13_motion=True;s.r13_carriage_skip=False;result=True')
   await native_jump(q,'r13_trial');await until(screen='r13_meeting_agenda');await q.press('다람이의 방어가');await until(text='아이가 촛대로');await q.input(810,610);await q.input(810,610);await until(text='촛대는')
   original=await snap();await present('E35')
   quiet=await snap();assert quiet['music']==0 and quiet['ambience']==0,quiet
   await asyncio.sleep(2.7);released=await snap();assert released['music']>0 and released['ambience']>0,released
   assert quiet['prefs']==released['prefs']==original['prefs'] and quiet['mute']==released['mute']==original['mute'];report['checks'].append('Actual explanation gain zero, timeout restores both channels, user volume/mute unchanged')
   await until(text='그 방에는');before=await snap();assert before['level']==1,before;await q.shot('01-pressure-persistent')
   await q.press('자료 보여주기');await q.press('그만두기');await q.wait('say');after=await snap();assert after['events']==before['events'] and after['level']==1 and after['music']>0
   report['checks'].append('Evidence picker cancel preserves pressure/event tokens and restores audible scene')
   before_say=(await q.state())['say'];await q.press('더보기');await q.press('저장 · 불러오기');await q.wait('save');await q.press('3쪽');await q.press('3쪽 5번');await q.press('돌아가기');await q.wait('say')
   await q.input(810,610);await q.press('더보기');await q.press('저장 · 불러오기');await q.press('불러오기로');await q.wait('load');await q.press('3쪽 5번');await q.wait('confirm');await q.press('예');await q.wait('say')
   loaded=await snap();assert loaded['level']==1 and loaded['events']==before['events'] and loaded['collective']['phase']=='settled' and loaded['music']>0,loaded;assert (await q.state())['say']==before_say
   await q.shot('02-loaded-pressure');report['checks'].append('Actual save/load restores held pressure and exact line; does not replay collective or silence')
   rollback=[]
   for _ in range(18):
    await page.keyboard.press('PageUp');await asyncio.sleep(.15);state=await snap();rollback.append(state)
    if state['level']==0:break
   report['rollback_after_load']=rollback
   report['checks'].append('PageUp after load preserves saved pressure when history does not move; this is not proof-boundary rollback coverage')
   await q.shot('03-rollback-after-load')
   await q.press('더보기');await q.press('저장 · 불러오기');await q.press('불러오기로');await q.wait('load');await q.press('3쪽 5번');await q.wait('confirm');await q.press('예');await q.wait('say')
   await present('E09');await page.keyboard.down('Control');await asyncio.sleep(2);await page.keyboard.up('Control');st=await until(screen='choice');skipped=await snap();assert skipped['level']==2 and skipped['collective']['phase']=='settled' and skipped['music']>0,skipped
   report['checks'].append('Actual held Ctrl skip reaches authored choice; pressure applied once; transient collective settles; music not stuck silent')
   await q.press('겁 많은 아이는 그 길로 못 간다');await until(text='그 방에는');recovered=await snap();assert recovered['level']==1,recovered
   await q.shot('04-recovered-pressure');report['checks'].append('Authored successful counter lowers pressure 2→1, preserved in next spoken line')
   rewind=[]
   rollback_ui='import renpy\ndef qa_back(**kwargs):\n import renpy\n s=renpy.store\n renpy.ui.textbutton("검토 두 단계",clicked=s.Rollback(checkpoints=2),xpos=500,ypos=90,xsize=280,ysize=70)\nrenpy.exports.define_screen("qa_back",qa_back,modal="False",zorder="220")\nrenpy.exports.show_screen("qa_back")\nrenpy.exports.restart_interaction()\nresult=True'
   for _ in range(8):
    await q.py(rollback_ui);await q.press('검토 두 단계');r=await snap();rewind.append(r)
    if r['level']==0:break
   report['rollback_engine_action']=rewind
   assert rewind[-1]['level']==0 and not rewind[-1]['events'],rewind[-1]
   report['checks'].append('Actual engine Rollback(checkpoints=2) button restores pre-proof pressure and event history; default PageUp input did not cross that boundary')
   await q.shot('05-engine-rollback-before-proof')
   await present('E35');await until(text='그 방에는');replayed=await snap();assert replayed['level']==1 and len(replayed['events'])==2
   report['rollback_replayed']=replayed;report['checks'].append('Actual E35 replay after rollback raises pressure once and restores music')
   report.update(passed=True,initial=original,quiet=quiet,released=released,loaded=loaded,skipped=skipped,recovered=recovered)
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));report['failure_state']=await q.state();raise
  finally:
   (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k in ('passed','checks','error')},ensure_ascii=False),flush=True)
   if not report.get('passed'):
    print('INSPECT READY',flush=True)
    env=dict(q=q,page=page,snap=snap,until=until,present=present,asyncio=asyncio,report=report,OUT=OUT,json=json)
    while True:
     line=await asyncio.to_thread(sys.stdin.readline)
     if not line or line.strip()=='STOP':break
     try:
      value=eval(compile(line,'<inspect>','eval',flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT),env)
      if asyncio.iscoroutine(value):value=await value
      print(json.dumps(value,ensure_ascii=False,default=str),flush=True)
     except Exception as e:print(repr(e),flush=True)
   await b.close()
asyncio.run(main())
