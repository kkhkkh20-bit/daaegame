import asyncio,json,time,subprocess,base64,sys,ast
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_debate_board','r13_more_tools',")
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump,ns
native_load=ns['native_load']
OUT=Path('/workspace/daaegame-reactions/reports/c2-editorial');OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=await b.new_context(viewport={'width':1280,'height':720});await c.add_init_script(path='/workspace/capture_game_audio.js');page=await c.new_page();q=ReviewQA(page,OUT);report={};events=[]
  async def snap():
   return await q.py('import renpy;s=renpy.store;result=dict(edit=s.r13_c2_edit,poses=s.r13_c2_pair_poses,direction_poses=s.r13_meeting_direction_poses,packet=s.r13_packet,page=s.r13_page_i,pressure=s.r13_meeting_pressure_level("resident_ppul"),propositions=s.room13["propositions"],evidence=s.room13["evidence"],broken=[st["id"] for st in s.r13_debate_statements("C2") if s.r13_debate_is_broken("C2",st["id"])])')
  async def until(text=None,screen=None,hold=.25):
   for _ in range(60):
    st=await q.state()
    if (text and text in st['say']) or (screen and screen in st['screens']):return st
    if 'say' in st['screens']:
     events.append(dict(t=time.monotonic(),say=st['say']));await q.input(810,610);await asyncio.sleep(hold)
    else:await asyncio.sleep(.1)
   raise AssertionError((text,screen,st))
  async def back():
   await q.py('import renpy\ndef _qa_back(**kwargs):\n import renpy\n renpy.ui.textbutton("검토 뒤로",clicked=renpy.store.Rollback(checkpoints=2),xpos=1060,ypos=90)\nrenpy.exports.define_screen("qa_back",_qa_back,zorder="200");renpy.exports.show_screen("qa_back");renpy.exports.restart_interaction();result=True')
   await q.press('검토 뒤로');await q.py('import renpy;renpy.exports.hide_screen("qa_back");renpy.exports.restart_interaction();result=True');await asyncio.sleep(.3)
  async def evidence():
   await q.press('자료 보여주기');await q.wait('r13_book');label=await q.py('import renpy;s=renpy.store;result=s.R13_RECORD_SHORT.get("E09",s.r13_catalog_title("E09")[:8])');await q.press(label);await q.press('이 주장에 근거로 낸다');await q.wait('say')
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E09"],propositions=["C1"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.preferences.text_cps=0;s.preferences.afm_enable=False;s.persistent.room13_motion=True;s.r13_carriage_skip=False;result=True')
   await native_jump(q,'r13_trial');await until(screen='r13_meeting_agenda');await q.press('다람이의 방어가');await until(text='아이가 촛대로');await asyncio.sleep(.3)
   report['nested_before']=await snap();await q.press('자료 보여주기');await q.wait('r13_book');await q.py('import renpy;renpy.exports.save("qa-c2-nested");result=True');await native_load(q,'qa-c2-nested');await q.wait('say');report['nested_after']=await snap()
   assert report['nested_before']['edit']['token']==report['nested_after']['edit']['token'];assert report['nested_before']['packet']==report['nested_after']['packet'];assert report['nested_after']['edit']['pair'] is None
   # Re-enter first live line so the clip includes its actual listener cut.
   await q.press('›');await q.press('‹');await until(text='아이가 촛대로')
   cap=await page.evaluate('window.__startGameCapture()');start=time.monotonic()
   for i in range(5):
    await asyncio.sleep(2);events.append(dict(t=time.monotonic(),state=await snap()));await q.input(810,610)
   await until(text='그 방에는');await q.press('발언 선택');await q.wait('r13_debate_board');await evidence();await until(text='잠깐 기다리시오',hold=.65);await asyncio.sleep(2)
   report['enter']=await snap();await q.py('import renpy;renpy.exports.save("qa-c2-counter");result=True');await page.screenshot(path=str(OUT/'01-confrontation-entry.png'))
   await q.input(810,610);await asyncio.sleep(2);report['pressure_hold']=await snap();await until(screen='choice');await asyncio.sleep(1.5)
   await q.press('통로는 주방 레버로만 열린다');await q.wait('say');await asyncio.sleep(2);report['speaker_switch']=await snap();await page.screenshot(path=str(OUT/'02-dad-answer-fixed-sides.png'))
   await until(text='주방에 누군가',hold=1.2);await asyncio.sleep(2)
   for _ in range(5):
    if (await snap())['edit'].get('pair') is None:break
    await q.input(810,610);await asyncio.sleep(.7)
   report['exit']=await snap();await page.screenshot(path=str(OUT/'03-third-person-return.png'))
   await asyncio.sleep(max(0,38-(time.monotonic()-start)))
   meta=await page.evaluate('window.__stopGameCapture()');raw=Path('/workspace/c2-editorial.webm')
   with raw.open('wb') as f:
    for offset in range(0,meta['bytes'],500000):f.write(base64.b64decode(await page.evaluate('(n)=>window.__gameCaptureChunk(n)',offset)))
   subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-profile:v','baseline','-c:a','aac','-b:a','128k','-movflags','+faststart',str(OUT/'actual-c2.mp4')],check=True)
   report['capture']=dict(capture=cap,media=meta,wall=time.monotonic()-start);print('VIDEO READY',flush=True)
   assert report['enter']['edit']['pair']==['resident_ppul','dad'],report['enter']
   assert report['speaker_switch']['edit']['pair']==['resident_ppul','dad'],report['speaker_switch']
   assert report['speaker_switch']['edit']['speaker']=='dad'
   assert report['exit']['edit']['pair'] is None
   report['rollback_diagnostic']=await q.py('import renpy;result=dict(can=renpy.exports.can_rollback(),enabled=renpy.config.rollback_enabled,store=renpy.store._rollback,contexts=len(renpy.game.contexts),context=renpy.game.context().rollback,loglen=len(renpy.game.log.log))');print('ROLLBACK',report['rollback_diagnostic'],flush=True)
   # Actual engine rollback through the root-context authored exchange.
   for _ in range(12):
    await back()
    if (await snap())['edit'].get('pair'):break
   report['rollback']=await snap();assert report['rollback']['edit'].get('pair'),report['rollback']
   await q.say_save(6);before=await snap();await q.say_load(6);after=await snap();report['save_load']={'before':before,'after':after}
   for key in ('poses','direction_poses','pressure','propositions','evidence','broken','packet','page'):assert before[key]==after[key],(key,before,after)
   assert before['edit']['pair']==after['edit']['pair'];assert after['edit']['phase']=='settled'
   await q.py('import renpy;s=renpy.store;s.persistent.room13_motion=False;renpy.exports.restart_interaction();result=True');await asyncio.sleep(.5);await q.state();await page.screenshot(path=str(OUT/'04-motion-off-pair.png'));report['motion_off']=await snap()
   assert report['motion_off']['edit']['pair']==after['edit']['pair']
   # Roll back within the same root context to the original pre-choice counter.
   for _ in range(20):
    if (await snap())['edit'].get('token',[None])[0]=='debate:counter:C2:s3':break
    await back()
   report['before_skip']=await snap();assert report['before_skip']['edit']['token'][0]=='debate:counter:C2:s3'
   await q.py('import renpy;renpy.store.r13_toggle_fast_all();result=True');await q.wait('choice');report['skip']=await snap()
   assert report['skip']['edit']['pair']==['resident_ppul','dad']
   assert report['skip']['propositions']==report['before_skip']['propositions'];assert report['skip']['broken']==report['before_skip']['broken']
   await q.press('그 통로는 할머니만 썼다');await q.wait('say');report['third_party']=await snap();assert report['third_party']['edit']['speaker']=='resident_seori';assert report['third_party']['edit']['pair'] is None
   assert report['third_party']['edit']['phase']=='settled'
   await page.screenshot(path=str(OUT/'05-third-party-motion-off.png'))
   await q.py('import renpy;s=renpy.store;s.persistent.room13_motion=True;renpy.exports.restart_interaction();result=True')
   report['passed']=True
  except Exception as exc:
   report['error']=repr(exc);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   report['events']=events;(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
   if not report.get('passed'):
    print('INSPECT READY',flush=True)
    env=dict(q=q,page=page,snap=snap,until=until,evidence=evidence,back=back,native_load=native_load,asyncio=asyncio,report=report,OUT=OUT,json=json)
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
