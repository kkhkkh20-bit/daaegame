"""Clean SDK build: authored scene, cross-packet rollback, same-pose fallback."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_remaining_approved22 import setup
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/expression-clean-01936');OUT.mkdir(exist_ok=True)
SNAP='''import renpy
s=renpy.store
result=dict(version=s.config.version,identity=getattr(s,'identity',None),read_id=s.r13_read_id,index=s.r13_index,page=s.r13_page_i,packet=s.r13_packet,beat=s.r13_dialogue_beat,person=s.r13_motion_person,pose=s.r13_current_pose,visible='r13_visitor' in renpy.exports.get_showing_tags())'''
async def main():
 report={'kind':'Clean final SDK build; production labels unchanged; fixture state only','shots':{}}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  async def snap(name):
   r=await q.py(SNAP);report['shots'][name]=r;await page.screenshot(path=str(OUT/(name+'.png')));print(name,json.dumps(r,ensure_ascii=False),flush=True);return r
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.5)
   await setup(q,2,'store',flags=['ev_g_done']);await native_jump(q,'r13_ep1_siluk');await q.wait('say')
   for _ in range(12):
    s=await q.py(SNAP)
    if s['beat'] and s['beat']['person']=='kid_siluk2':break
    await q.input(900,615);await asyncio.sleep(.1)
   s=await snap('01-authored-child-joy');assert s['beat']['talk']=='joy' and s['person']=='kid_siluk2'
   await q.say_save(4);await q.say_load(4);s=await snap('02-save-load-joy');assert s['beat']['talk']=='joy'
   for _ in range(8):
    if 'choice' in (await q.state())['screens']:break
    await q.input(900,615);await asyncio.sleep(.1)
   await q.press('아이에게 묻는다');await q.wait('say');s=await snap('03-next-packet-child-one');assert s['identity']=='ep1:siluk:kid'
   traversed=[]
   for i in range(4):
    can=await q.py('import renpy;result=dict(can=renpy.exports.can_rollback(),enabled=renpy.config.rollback_enabled,store_rollback=getattr(renpy.store,"_rollback",None))');print('ROLLBACK',can,flush=True)
    await q.py('import renpy\ndef _qa_back(**kwargs):\n import renpy\n s=renpy.store\n renpy.ui.textbutton("검수 되돌리기",clicked=[s.Hide("qa_back"),s.Rollback()],xpos=500,ypos=300)\nrenpy.exports.define_screen("qa_back",_qa_back,modal="True",zorder="200");renpy.exports.show_screen("qa_back");renpy.exports.restart_interaction();result=True')
    await q.press('검수 되돌리기');await asyncio.sleep(.5);s=await q.py(SNAP);traversed.append(dict(s,rollback_capability=can))
    if s['identity']=='ep1:siluk' and s['index']==2:break
   report['rollback_traversal']=traversed
   s=await snap('04-cross-packet-rollback-result');report['cross_packet_rollback']=bool(s['identity']=='ep1:siluk' and s['beat'] and s['beat']['talk']=='joy')
   # No production function or label replacement: invoke the compiled renderer for an unreviewed text.
   await q.py('import renpy;s=renpy.store;s.r13_dialogue_beat=dict(person="daram",talk="joy",react=None,settled=True,duration=.35);s.r13_speaker("daram","neutral","neutral");renpy.exports.restart_interaction();result=True')
   before=await snap('05-controlled-prior-joy')
   await q.py('import renpy;s=renpy.store;s.r13_dialogue_beat_begin("qa:unknown",0,("daram","검수용 미등록 대사"),"neutral");s.r13_speaker("daram","neutral","neutral");renpy.exports.restart_interaction();result=True')
   after=await snap('06-controlled-fallback-neutral');assert after['beat'] is None and before['pose']==after['pose']=='neutral'
   # Intentionally authored special remains available and is not converted to a narration beat.
   report['special_guard']=await q.py('import renpy;s=renpy.store;p=s.r13_dialogue_source_profile("kid_kkomi","door_peek",840);result=dict(file=p["frames"]["neutral"]["file"],plan=s.r13_dialogue_narration_plan((None,"검수",dict(show="kid_kkomi",pose="door_peek",expression="surprise")),s.R13_DIALOGUE_TALK_ART["people"]))')
   assert report['special_guard']['plan'] is None and 'dialogue-pose-source' in report['special_guard']['file']
   report['status']='passed' if report['cross_packet_rollback'] else 'expression_checks_passed_rollback_not_verified'
  except Exception as e:
   report['status']='failed';report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
