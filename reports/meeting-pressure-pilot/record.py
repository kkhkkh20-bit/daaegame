import asyncio,json,time,subprocess,base64,os
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_debate_board','r13_more_tools',")
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/pressure-review-'+os.environ.get('PRESSURE_VARIANT','after'));OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  c=await b.new_context(viewport={'width':1280,'height':720})
  await c.add_init_script(path='/workspace/capture_game_audio.js');page=await c.new_page();q=ReviewQA(page,OUT);log=[]
  async def until(text=None,screen=None):
   for _ in range(40):
    st=await q.state()
    if (text and text in st['say']) or (screen and screen in st['screens']):return
    if 'say' in st['screens']:
     log.append(dict(t=time.monotonic(),say=st['say']));await q.input(810,610);await asyncio.sleep(.30)
    else:await asyncio.sleep(.1)
   raise AssertionError((text,screen,st))
  async def evidence(key):
   await q.press('자료 보여주기');await q.wait('r13_book')
   label=await q.py('import renpy;s=renpy.store;result=s.R13_RECORD_SHORT.get('+repr(key)+',s.r13_catalog_title('+repr(key)+')[:8])')
   await q.press(label);await asyncio.sleep(.7);await q.press('이 주장에 근거로 낸다');await q.wait('say')
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E35","E09"],propositions=["C1"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.preferences.text_cps=0;s.preferences.afm_enable=False;s.persistent.room13_motion=True;s.r13_carriage_skip=False;result=True')
   await native_jump(q,'r13_trial');await until(screen='r13_meeting_agenda');await q.press('다람이의 방어가');await until(text='아이가 촛대로');await asyncio.sleep(.6)
   if os.environ.get('PRESSURE_VARIANT')=='before':
    await q.py('import renpy;s=renpy.store;ns=s.R13MeetingOrbit.render.__globals__;exec('+repr(Path('/workspace/camera-baseline-functions.py').read_text())+',ns);s.r13_meeting_pressure_enabled=lambda claim=None:False;result=True')
   await q.py('import renpy,time\ns=renpy.store\nns=s.r13_meeting_pressure_change.__globals__\nns[\'_qa_pressure_log\']=[]\nns[\'_qa_pressure_original\']=ns[\'r13_meeting_pressure_change\']\nns[\'_qa_settle_original\']=ns[\'r13_meeting_collective_settle\']\nexec("def _qa_pressure_event(claim,sid,event,amount):\\n result=_qa_pressure_original(claim,sid,event,amount)\\n _qa_pressure_log.append(dict(t=renpy.display.core.get_time(),event=event,changed=result,level=r13_meeting_pressure_level(\'resident_ppul\'),sid=sid))\\n return result\\ndef _qa_collective_settle():\\n r=getattr(store,\'r13_meeting_collective\',None)\\n _qa_pressure_log.append(dict(t=renpy.display.core.get_time(),event=\'collective_end\',reaction=dict(r) if r else None,poses=dict(store.r13_meeting_direction_poses)))\\n return _qa_settle_original()",ns)\nns[\'r13_meeting_pressure_change\']=ns[\'_qa_pressure_event\']\nns[\'r13_meeting_collective_settle\']=ns[\'_qa_collective_settle\']\nresult=True')
   capture=await page.evaluate('window.__startGameCapture()');print('CAPTURE',capture,flush=True)
   start=time.monotonic();await asyncio.sleep(1.3)
   await q.input(810,610);await asyncio.sleep(1.5);await q.input(810,610);await asyncio.sleep(1.3)
   await evidence('E35');await until(text='촛대는');await asyncio.sleep(1)
   await q.input(810,610);await asyncio.sleep(1.1);await q.input(810,610);await asyncio.sleep(1.0)
   await until(text='그 방には' if False else '그 방에는');await q.shot('01-pressure-held-after-group');first=await q.py('import renpy;s=renpy.store;result=dict(level=s.r13_meeting_pressure_level("resident_ppul"),poses=s.r13_meeting_direction_poses,slots=s.r13_meeting_art_slots)');assert first['level']==(0 if os.environ.get('PRESSURE_VARIANT')=='before' else 1),first;await evidence('E09');await until(text='잠깐 기다리시오');await asyncio.sleep(1.5)
   await q.input(810,610);await asyncio.sleep(1.5);await until(screen='choice');await asyncio.sleep(3)
   choice_time=time.monotonic();await q.press('겁 많은 아이는 그 길로 못 간다');await until(text='겁 많은 아이가');await asyncio.sleep(1.5);await q.shot('02-successful-counter');await until(text='그 방에는');await q.shot('03-recovery-held');await asyncio.sleep(1.5)
   end=time.monotonic();meta=await page.evaluate('window.__stopGameCapture()');raw=OUT/'actual-game-audio.webm'
   with raw.open('wb') as f:
    for offset in range(0,meta['bytes'],500000):f.write(base64.b64decode(await page.evaluate('(n)=>window.__gameCaptureChunk(n)',offset)))
   state=await q.py('import renpy;s=renpy.store;result=dict(level=s.r13_meeting_pressure_level("resident_ppul"),events=[list(v) for v in s.r13_meeting_pressure_events],pose=s.r13_meeting_direction_poses,collective=s.r13_meeting_collective,music_gain=s.r13_meeting_channel_gain("music"),ambience_gain=s.r13_meeting_channel_gain("ambience"),broken=[st["id"] for st in s.r13_debate_statements("C2") if s.r13_debate_is_broken("C2",st["id"])])')
   subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(raw),'-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-profile:v','baseline','-level','3.1','-c:a','aac','-b:a','128k','-movflags','+faststart',str(OUT/'comparison.mp4')],check=True)
   (OUT/'capture.json').write_text(json.dumps(dict(capture=capture,media=meta,seconds=end-start,state=state,first_pressure=first,event_log=await q.py("import renpy;result=renpy.store.r13_meeting_pressure_change.__globals__['_qa_pressure_log']"),log=log,initial_fixture='day10, E35/E09 owned, C1 proved; actual UI after this',audio='Live WebAudio output captured with canvas MediaRecorder; no post-produced sound'),ensure_ascii=False,indent=2));print('RECORDED',end-start,state,flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'recording-failure.png'));(OUT/'recording-failure.json').write_text(json.dumps(await q.state(),ensure_ascii=False));raise
  finally:await b.close()
asyncio.run(main())
