"""Focused real Chromium/Ren'Py renderer fixtures, plus a natural fresh-start screen."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/smooth20-screen-review'));OUT.mkdir(parents=True,exist_ok=True)
SETUP='''import renpy
s=renpy.store
s.room13=s.r13_new();s.r13_edit(day=1,period=1,location="gate")
s.room13_mode=True;s.persistent.room13_motion=True;s.persistent.room13_large_text=False
s.r13_cg_active=False;s.r13_meeting_active=False;s.r13_thought_active=False
s.qa_person="guard";s.qa_slot="neutral";s.qa_height=560;s.qa_title="Source-master renderer fixture"
def smooth_gallery(**kwargs):
 s=renpy.store
 renpy.ui.add(s.r13_background(s.R13_PLACES[s.room13["location"]][1]))
 renpy.ui.add(s.Solid("#00000060"))
 renpy.ui.add(s.Transform(s.r13_close_art(s.qa_person,"neutral",s.qa_height),xpos=s.r13_close_x(s.qa_person,"neutral",s.qa_height),xanchor=.5,ypos=s.r13_close_y(s.qa_person,s.qa_height,50,"neutral")))
 renpy.ui.text(s.qa_title,xpos=20,ypos=10,size=20,font=s.r13_ui_font(),color="#ffffff")
renpy.display.screen.define_screen("qa_smooth_gallery",smooth_gallery,zorder="200")
renpy.exports.show_screen("qa_smooth_gallery");renpy.exports.restart_interaction();result=True
'''
class ReviewQA(UIQA):
 async def py(self,code):return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)
async def main():
 report={'kind':'real web renderer fixtures; not a full-game playthrough','captures':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  page.on('console',lambda m: print('BROWSER',m.type,m.text,flush=True) if m.type=='error' else None)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8887/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu')
   report['version']=await q.py('import renpy;result=renpy.store.config.version');print('READY',report['version'],flush=True)
   await q.py(SETUP)
   people=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
   selected={k:v for k,v in people.items() if not os.environ.get('ROOM13_QA_SOURCE_COMMIT') or v['source_commit']==os.environ['ROOM13_QA_SOURCE_COMMIT']}
   report['selected_people']=list(selected)
   for who in ([] if os.environ.get("ROOM13_QA_QUICK") else selected):
    for h,slots in [(560,['neutral','joy','angry','anxious','surprise_react','surprise_talk']),(760,['neutral']),(840,['neutral'])]:
     for slot in slots:
      name=f'{who}-{h}-{slot}'
      await q.py('import renpy\ns=renpy.store\ns.qa_person=%r;s.qa_height=%r;s.qa_slot=%r;s.qa_title=%r\ns.r13_dialogue_beat=dict(person=s.qa_person,talk=s.qa_slot,react=None,settled=True,duration=.35)\nrenpy.exports.restart_interaction();result=True'%(who,h,slot,name))
      await asyncio.sleep(.10);await page.screenshot(path=str(OUT/(name+'.png')))
      assert not await q.py('import renpy;result=bool(renpy.display.screen.get_screen("_exception"))')
      report['captures'].append(name)
    print('CAPTURED',who,flush=True)
   # Real timed Displayable: normal reaction duration, then calm talk frame.
   await q.py('import renpy\ns=renpy.store\ns.qa_person="resident_nero";s.qa_height=560;s.qa_title="reaction -> talk 0.35 sec"\ns.r13_dialogue_beat=dict(person="resident_nero",talk="surprise_talk",react="surprise_react",settled=False,duration=.35)\nrenpy.exports.restart_interaction();result=True')
   await page.screenshot(path=str(OUT/'reaction-start.png'));await asyncio.sleep(.5);await page.screenshot(path=str(OUT/'reaction-settled.png'))
   await asyncio.sleep(.4)
   report['reaction_completion']=await q.py('import renpy;result=renpy.store.r13_dialogue_beat')
   assert report['reaction_completion']['settled']
   report['skip_rollback_motion']=await q.py('import renpy\ns=renpy.store\nplan=dict(person="resident_nero",talk="surprise_talk",react="surprise_react",settled=False,duration=.35)\nresult=dict(skip=s.r13_dialogue_phase(plan,0,True,True),motion_off=s.r13_dialogue_phase(plan,0,False,False),elapsed=s.r13_dialogue_phase(plan,.36,False,True))')
   assert all(v=='surprise_talk' for v in report['skip_rollback_motion'].values())
   # New page starts cleanly and enters the natural game, without gallery fixtures.
   await page.reload();await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(2)
   await page.screenshot(path=str(OUT/'natural-start.png'));report['natural_start']=await q.state()
   for _ in range(35):
    st=await q.state()
    if 'say' in st['screens'] and await q.py('import renpy;result=renpy.store.r13_dialogue_beat is not None'):break
    if any('씬 건너뛰기' in v['text'] for v in st['buttons']):await q.press('씬 건너뛰기')
    else:await q.input(810,640)
   await q.wait('say')
   report['before_save']=await q.py('import renpy;result=dict(beat=renpy.store.r13_dialogue_beat,packet=renpy.store.r13_packet)')
   await page.screenshot(path=str(OUT/'natural-dialogue.png'))
   await q.say_save(2);await q.say_load(2)
   report['after_load']=await q.py('import renpy;result=dict(beat=renpy.store.r13_dialogue_beat,packet=renpy.store.r13_packet)')
   assert report['before_save']['packet']==report['after_load']['packet']
   assert report['after_load']['beat'] and report['after_load']['beat']['settled']
   await page.screenshot(path=str(OUT/'after-load.png'))
   report['status']='passed'
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
if __name__=='__main__':asyncio.run(main())
