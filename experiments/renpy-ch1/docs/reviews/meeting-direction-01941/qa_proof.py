import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
OUT=Path('/workspace/meeting-01941-proof');OUT.mkdir(exist_ok=True)
async def main():
 report={'kind':'native calls to production evidence route with explicit state fixture','lines':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  async def state():return await q.py('import renpy;s=renpy.store;result=dict(id=s.r13_read_id,index=s.r13_index,packet=s.r13_packet,slots=s.r13_meeting_art_slots,poses=s.r13_meeting_direction_poses,reaction=s.r13_meeting_reaction,listener=s.r13_meeting_listener,proofs=s.room13["propositions"])')
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.press('처음부터');await asyncio.sleep(.5)
   await q.py('''import renpy
s=renpy.store
s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=10,period=0,location="dining",case_state="occurred",victim_state="dead",evidence=["E12"],propositions=[])
s.r13_flag("entry_corrected","lodging","witness:nabi");s.room13_mode=True;s.preferences.text_cps=0;s.persistent.room13_motion=True;s.r13_meeting_claim="C3";s.r13_meeting_active=True;s.r13_meeting_intro=False
def launch(**kwargs):
 s=renpy.store
 renpy.ui.textbutton("Proof fixture",clicked=[s.Hide('qa_proof_launch'),s.Call('r13_debate_present_record','C3','s2','E12')],xpos=300,ypos=300,xsize=500,ysize=80)
renpy.exports.define_screen('qa_proof_launch',launch,modal='True',zorder='250');renpy.exports.show_screen('qa_proof_launch');renpy.exports.restart_interaction();result=True''')
   await q.press('Proof fixture')
   for n in range(20):
    st=await state()
    if st['id'].startswith('debate:break:C3:s2:E12'):break
    await q.input(800,610)
   assert st['packet'][0]=='nabi',st
   await asyncio.sleep(.4);await page.screenshot(path=str(OUT/'01-nabi-e12.png'));report['lines'].append(st)
   assert st['slots']=={'nabi':'witness_hesitate'} and st['poses']['nabi']=='anxious',st
   await q.say_save(6);await q.say_load(6);report['loaded']=await state();assert report['loaded']['packet']==st['packet'] and report['loaded']['slots']==st['slots']
   for n in range(6):
    await q.input(800,610);await asyncio.sleep(.4);st=await state();report['lines'].append(st);await page.screenshot(path=str(OUT/(f'{n+2:02}-line.png')));print(st['id'],st['index'],st['packet'],st['poses'],flush=True)
    if st['id'].startswith('meeting:gasp:'):break
   report['before_rollback']=await state();await page.keyboard.press('PageUp');await asyncio.sleep(.5);report['after_rollback']=await state();report['rollback_changed']=report['before_rollback']['id']!=report['after_rollback']['id'] or report['before_rollback']['index']!=report['after_rollback']['index']
   assert report['after_rollback']['proofs']==[],report['after_rollback']
   report['status']='passed_except_rollback_unverified' if not report['rollback_changed'] else 'passed'
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
asyncio.run(main())
