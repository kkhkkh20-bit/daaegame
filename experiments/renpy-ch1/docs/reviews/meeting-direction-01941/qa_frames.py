import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
OUT=Path('/workspace/meeting-01941-frames');OUT.mkdir(exist_ok=True)
async def main():
 report={'kind':'production renderer with explicit authored-line fixtures','shots':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(1)
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=0,location="dining",case_state="occurred",victim_state="dead",evidence=list(s.ROOM13["evidence"]));s.room13_mode=True;s.persistent.room13_motion=True;s.preferences.text_cps=0;result=True')
   cues=await q.py('import renpy;result=[list(k) for k,v in renpy.store.R13_MEETING_LINE_CUES.items() if v.get("slot")]')
   for i,cue in enumerate(cues):
    claim=cue[0].split(':')[2];who=cue[2];label=f'{i:02}-{claim}-{who}'
    record=await q.py('''import renpy
s=renpy.store
cue='''+repr(cue)+'''
claim=cue[0].split(':')[2];who=cue[2]
s.r13_meeting_direct_end();s.r13_meeting_claim=claim;s.r13_meeting_active=True;s.r13_meeting_focus=who;s.r13_meeting_intro=False
packet=(who,cue[3],"anxious" if who=="nabi" else "neutral")
s.r13_meeting_direct_line(cue[0],cue[1],packet,packet[2],packet[2])
renpy.exports.show_screen('r13_meeting_stage',claim=claim,focus=who,close=True)
renpy.exports.restart_interaction()
result=dict(claim=claim,person=who,slots=s.r13_meeting_art_slots,listener=s.r13_meeting_listener,poses=s.r13_meeting_direction_poses,kind=s.r13_meeting_kind(s.r13_debate_session(claim)))''')
    await asyncio.sleep(.7);await page.screenshot(path=str(OUT/(label+'.png')));report['shots'].append(dict(label=label,**record));print(label,record,flush=True)
   for claim in ('C2','F1','Q1','Q3'):
    record=await q.py('import renpy;s=renpy.store;s.r13_meeting_direct_end();s.r13_meeting_claim='+repr(claim)+';s.r13_meeting_active=True;renpy.exports.show_screen("r13_meeting_stage",claim='+repr(claim)+',focus=None,close=False);renpy.exports.restart_interaction();result=dict(cast=s.r13_meeting_cast('+repr(claim)+',s.r13_debate_session('+repr(claim)+')),kind=s.r13_meeting_kind(s.r13_debate_session('+repr(claim)+')))')
    await asyncio.sleep(.4);await page.screenshot(path=str(OUT/(claim+'-ensemble.png')));report['shots'].append(dict(label=claim+'-ensemble',**record));print(claim,'ensemble',flush=True)
   report['status']='captured'
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
