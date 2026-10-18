import asyncio,json,time,subprocess,base64,sys,ast
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_debate_board','r13_more_tools',")
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump,ns
native_load=ns['native_load']
OUT=Path('/workspace/daaegame-reactions/reports/c2-event-audio');OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=await b.new_context(viewport={'width':1280,'height':720});await c.add_init_script(path='/workspace/capture_game_audio.js');page=await c.new_page();q=ReviewQA(page,OUT);report={}
  async def snap():
   return await q.py('import renpy;s=renpy.store;result=dict(editorial=s.r13_c2_edit,line=s.r13_meeting_audio_line,mix=s.r13_meeting_audio_mix,music=s.r13_meeting_channel_gain("music"),ambience=s.r13_meeting_channel_gain("ambience"),prefs=dict(s.preferences.volumes),mute=dict(s.preferences.mute),proof=s.r13_meeting_proof_reveal,collective=s.r13_meeting_collective,table_source=s.R13_C2_TABLE_IMPACT,hits=s.r13_meeting_audio_hits,quiet_clock=bool(renpy.display.screen.get_screen("r13_meeting_quiet_clock")),packet=s.r13_packet,page=s.r13_page_i,tempo=s.r13_meeting_tempo_stage(),music_path=s.renpy.music.get_playing(channel="music"),ambience_path=s.renpy.music.get_playing(channel="ambience"))')
  async def until(text=None,screen=None):
   for _ in range(60):
    st=await q.state()
    if (text and text in st['say']) or (screen and screen in st['screens']):return st
    if 'say' in st['screens']:await q.input(810,610)
    else:await asyncio.sleep(.1)
   raise AssertionError((text,screen,st))
  async def present():
   await q.press('자료 보여주기');await q.wait('r13_book');title=await q.py('import renpy;s=renpy.store;result=s.R13_RECORD_SHORT.get("E09",s.r13_catalog_title("E09")[:8])');await q.press(title);await q.press('이 주장에 근거로 낸다');await q.wait('say')
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터')
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=["E09"],propositions=["C1"]);s.r13_flag("entry_corrected","lodging");s.room13_mode=True;s.preferences.text_cps=0;s.preferences.afm_enable=False;s.persistent.room13_motion=True;s.r13_carriage_skip=False;s.preferences.set_volume("music",.37);s.preferences.set_volume("sfx",.26);result=True')
   await native_jump(q,'r13_trial');await until(screen='r13_meeting_agenda');await q.press('다람이의 방어가');await until(text='그 방에는');await asyncio.sleep(1.1);report['normal']=await snap();assert report['normal']['music']==.45;assert report['normal']['ambience_path']=='assets/council-smallroom-murmur.ogg'
   # Actual nested material-picker cancellation, no substitute effect played.
   await q.press('자료 보여주기');await q.wait('r13_book');await q.press('그만두기');await q.wait('say');report['cancel']=await snap();assert report['cancel']['music']==.45
   await q.press('발언 선택');await q.wait('r13_debate_board');await present()
   await until(text='촛대가 떨어진 뒤');report['silent_start']=await snap();assert report['silent_start']['music']==report['silent_start']['ambience']==0
   capture=await page.evaluate('window.__startGameCapture()')
   await asyncio.sleep(6);report['silent_after_6s']=await snap();assert report['silent_after_6s']['music']==report['silent_after_6s']['ambience']==0;assert not report['silent_after_6s']['quiet_clock']
   await page.screenshot(path=str(OUT/'01-held-core-line.png'))
   # Save exact silent reading point, to verify load cleanup later.
   await q.py('import renpy;renpy.exports.save("qa-c2-silent");result=True')
   await q.input(810,610);await asyncio.sleep(1);report['same_proof_next_page']=await snap();assert report['same_proof_next_page']['music']==0
   await until(text='그럼 할아버지를');await asyncio.sleep(.7);report['reaction_release']=await snap();assert report['reaction_release']['music']==.45 and report['reaction_release']['ambience']==.65
   await until(screen='choice');await q.press('통로는 주방 레버로만 열린다');await q.wait('say');report['duck_start']=await snap();assert report['duck_start']['music']==.14;await page.screenshot(path=str(OUT/'02-player-speech-resident-reaction.png'))
   await q.py('import renpy;s=renpy.store;ns=s.r13_meeting_direct_audio.__globals__;ns["_qa_volume_calls"]=[];ns["_qa_volume_original"]=ns["renpy"].music.set_volume;exec("def _qa_volume(value,*args,**kwargs):\\n _qa_volume_calls.append(dict(value=value,channel=kwargs.get(\'channel\',\'music\')))\\n return _qa_volume_original(value,*args,**kwargs)",ns);ns["renpy"].music.set_volume=ns["_qa_volume"];result=True')
   await asyncio.sleep(4);await q.input(810,610);await asyncio.sleep(.7);report['duck_next_line']=await snap();assert report['duck_next_line']['music']==.14
   report['continuous_block_volume_calls']=await q.py('import renpy;result=renpy.store.r13_meeting_direct_audio.__globals__["_qa_volume_calls"]');assert not report['continuous_block_volume_calls'],report['continuous_block_volume_calls']
   await until(text='주방에 누군가');await asyncio.sleep(.4);report['npc_release']=await snap();assert report['npc_release']['music']==.45
   meta=await page.evaluate('window.__stopGameCapture()');raw=Path('/workspace/c2-event-audio.webm')
   with raw.open('wb') as f:
    for offset in range(0,meta['bytes'],500000):f.write(base64.b64decode(await page.evaluate('(n)=>window.__gameCaptureChunk(n)',offset)))
   subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(OUT/'event-audio-control.mp4')],check=True);report['capture']=dict(capture=capture,media=meta)
   await q.py('import renpy;s=renpy.store;ns=s.r13_meeting_direct_audio.__globals__;ns["renpy"].music.set_volume=ns["_qa_volume_original"];result=True')
   # Load intentionally releases the saved silence, rather than replaying a hit.
   await native_load(q,'qa-c2-silent');await q.wait('say');await asyncio.sleep(.3);report['load']=await snap();assert report['load']['music']==.45 and report['load']['ambience']==.65;assert report['load']['packet']==report['silent_start']['packet']
   await page.keyboard.down('Control');await asyncio.sleep(1.4);await page.keyboard.up('Control');await until(screen='choice');report['skip']=await snap();assert report['skip']['music']>0 and report['skip']['ambience']>0
   # Exception callback is exercised without crashing the game or suppressing errors.
   await q.py('import renpy;s=renpy.store;s.r13_meeting_audio_apply("silent");result=s.config.exception_handler(None)');report['exception_cleanup']=await snap();assert report['exception_cleanup']['music']==.45
   await q.py('import renpy;s=renpy.store;s.r13_meeting_audio_apply("silent");s.r13_meeting_active=False;s.r13_meeting_direct_end();result=True');report['scene_exit']=await snap();assert report['scene_exit']['music']>0 and report['scene_exit']['ambience']>0;assert report['scene_exit']['mix'] is None
   for name,state in list(report.items()):
    if isinstance(state,dict) and 'prefs' in state:
     assert state['prefs']==report['normal']['prefs'] and state['mute']==report['normal']['mute'],name
     assert state['editorial'].get('visual')!='dad' and not state['editorial'].get('pair'),name
   assert report['normal']['table_source'] is None;report['passed']=True
  except Exception as exc:
   report['error']=repr(exc);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('RESULT',report.get('passed'),report.get('error'),flush=True)
   if not report.get('passed'):
    print('INSPECT READY',flush=True);env=dict(q=q,page=page,snap=snap,until=until,present=present,native_load=native_load,asyncio=asyncio,report=report,OUT=OUT,json=json)
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
