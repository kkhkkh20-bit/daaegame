import asyncio,json,time,subprocess,base64,sys,ast
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_meeting_agenda','r13_debate_board','r13_more_tools',")
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump,ns
native_load=ns['native_load']
OUT=Path('/workspace/daaegame-reactions/reports/c2-typing-audit');OUT.mkdir(exist_ok=True)
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
   await q.press('발언 선택');await q.wait('r13_debate_board')
   await q.py('import renpy;s=renpy.store;s.preferences.text_cps=34;result=True')
   await present();await until(text='촛대가 떨어진 뒤')
   async def clip(name,duration):
    await page.evaluate('window.__startGameCapture()');await asyncio.sleep(duration);meta=await page.evaluate('window.__stopGameCapture()')
    raw=OUT/(name+'.webm')
    with raw.open('wb') as f:
     for off in range(0,meta['bytes'],500000):f.write(base64.b64decode(await page.evaluate('(n)=>window.__gameCaptureChunk(n)',off)))
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-c:v','libx264','-crf','22','-pix_fmt','yuv420p','-c:a','aac',str(OUT/(name+'.mp4'))],check=True);raw.unlink()
   report['core_normal']=await snap();assert report['core_normal']['music']==0 and report['core_normal']['ambience']==0
   report['typing_config']=await q.py('import renpy;s=renpy.store;result=dict(cps=s.preferences.text_cps,enabled=s.persistent.room13_typing_sound,allowed=s.typing_allowed,mute=s.preferences.get_mute("sfx"),gain=s.r13_meeting_channel_gain("typing"))')
   await clip('01-normal-typing',1.4)
   await q.py('import renpy;renpy.store.preferences.set_mute("sfx",True);result=True')
   await q.input(810,610);await clip('02-sfx-muted',1.4)
   await q.py('import renpy;s=renpy.store;s.preferences.set_mute("sfx",False);s.preferences.text_cps=0;result=True')
   await q.input(810,610)
   # Complete the currently slow page before observing instant-mode silence.
   await asyncio.sleep(.2);await clip('03-instant-text',1.0)
   report['end']=await snap();report['passed']=True
  finally:
   (OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
