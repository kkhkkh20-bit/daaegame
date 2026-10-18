import asyncio,json,time,subprocess,os
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_debate_board','r13_more_tools',")
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/camera-rhythm-'+os.environ.get('CAMERA_VARIANT','before'));OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  c=await b.new_context(viewport={'width':1280,'height':720},record_video_dir=str(OUT/'raw'),record_video_size={'width':1280,'height':720})
  page=await c.new_page();q=ReviewQA(page,OUT);log=[]
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
   if os.environ.get('CAMERA_VARIANT')=='after':await q.py('import renpy;ns=renpy.store.R13MeetingOrbit.render.__globals__;exec('+repr(Path('/workspace/meeting-camera-candidate.py').read_text())+',ns);result=True')
   await q.py('import renpy,time\ns=renpy.store\nns=s.R13MeetingOrbit.render.__globals__\noriginal=ns[\'r13_meeting_world_view\']\nns[\'_qa_camera_frames\']=[]\nns[\'_qa_camera_original\']=original\nexec("def _qa_camera_probe(claim,focus):\\n import time\\n t=time.perf_counter()\\n value=_qa_camera_original(claim,focus)\\n _qa_camera_frames.append(dict(t=t,view=value[0],moving=value[1],focus=focus,revision=store.r13_meeting_shot_revision,beat=(store.r13_meeting_direction or {}).get(\'beat\'),cost_ms=(time.perf_counter()-t)*1000))\\n return value",ns)\nns[\'r13_meeting_world_view\']=ns[\'_qa_camera_probe\']\nresult=True')
   start=time.monotonic();await asyncio.sleep(1.3)
   await q.input(810,610);await asyncio.sleep(1.5);await q.input(810,610);await asyncio.sleep(1.3)
   await evidence('E35');await until(text='촛대는');await asyncio.sleep(1)
   await q.input(810,610);await asyncio.sleep(1.1);await q.input(810,610);await asyncio.sleep(1.0)
   await until(text='그 방에는');await evidence('E09');await until(text='잠깐 기다리시오');await asyncio.sleep(1.5)
   await q.input(810,610);await asyncio.sleep(1.5);await until(screen='choice');await asyncio.sleep(3)
   choice_time=time.monotonic();await q.press('통로는 주방 레버로만 열린다');await until(text='주방에 누군가');await asyncio.sleep(1.2)
   end=time.monotonic();frames=await q.py("import renpy;result=renpy.store.R13MeetingOrbit.render.__globals__['_qa_camera_frames']");(OUT/'frames.json').write_text(json.dumps(frames));await asyncio.sleep(.3);finish=time.monotonic();v=page.video;await c.close();raw=Path(await v.path())
   duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(raw)]))
   begin=max(0,duration-(finish-start));length=end-start
   subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(begin),'-i',str(raw),'-t',str(length),'-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-profile:v','baseline','-level','3.1','-movflags','+faststart',str(OUT/'meeting-continuous.mp4')],check=True)
   (OUT/'meeting-recording.json').write_text(json.dumps(dict(capture='Actual Playwright video of running RenPy SDK game; no screenshot montage; normal speed',silent=True,initial_fixture='day10, E35/E09 owned, C1 proved; before clip only',actual_actions='Speaker turns, E35 evidence and reaction, E09 counter, same-speaker consecutive lines, choice and answer',raw_file=str(raw),raw_duration=duration,trim_start=begin,clip_seconds=length,choice_seconds=choice_time-start,log=log),ensure_ascii=False,indent=2));print('RECORDED',length,flush=True)
  except Exception:
   await page.screenshot(path=str(OUT/'recording-failure.png'));(OUT/'recording-failure.json').write_text(json.dumps(await q.state(),ensure_ascii=False));raise
  finally:await b.close()
asyncio.run(main())
