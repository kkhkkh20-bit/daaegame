"""Focused actual meeting/post routes and restored portraits, not a full campaign QA."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/meeting-source-review'));OUT.mkdir(exist_ok=True)
async def main():
 report={}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await browser.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8887/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');report['version']=await q.py('import renpy;result=renpy.store.config.version');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(1)
   await q.py('import renpy;s=renpy.store;s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=7,period=2,location="dining",case_state="occurred",victim_state="dead",evidence=list(s.ROOM13["evidence"]),propositions=[]);s.r13_flag("entry_corrected","lodging");result=True')
   await native_jump(q,'r13_trial')
   for _ in range(15):
    if await q.py('import renpy;s=renpy.store;result=bool(s.r13_meeting_active and s.r13_meeting_focus)'):break
    await q.input(810,640);await asyncio.sleep(.2)
   await q.wait('say');await asyncio.sleep(1)
   report['meeting']=await q.py('import renpy;s=renpy.store;result=dict(active=s.r13_meeting_active,focus=s.r13_meeting_focus,packet=s.r13_packet,kind=s.r13_meeting_kind(s.r13_debate_session(s.r13_meeting_claim)))');assert report['meeting']['active']
   await page.screenshot(path=str(OUT/'meeting-speaking.png'));await q.say_save(2);await q.say_load(2);await page.screenshot(path=str(OUT/'meeting-restored.png'))
   report['meeting_restored']=await q.py('import renpy;s=renpy.store;result=dict(active=s.r13_meeting_active,focus=s.r13_meeting_focus,packet=s.r13_packet,kind=s.r13_meeting_kind(s.r13_debate_session(s.r13_meeting_claim)))');assert report['meeting_restored']==report['meeting']
   report['heights']=await q.py('import renpy\ns=renpy.store\nresult={}\nfor height in (740,776,840,876):\n p=s.r13_dialogue_source_profile("resident_hyeoni","neutral",height)\n art=s.r13_fullbody_close_art("resident_hyeoni","neutral",height)\n render=renpy.display.render.render(art,1280,1000,0,0)\n result[height]=dict(canvas=p["canvas"],size=list(render.get_size()),file=p["frames"]["neutral"]["file"])')
   await q.py('import renpy;s=renpy.store;s.r13_meeting_active=False;s.r13_meeting_direct_end();s.r13_edit(day=2,period=1,location="post");s.place="우체국";s.r13_target="seryeon";s.r13_scene_bg=s.R13_PLACES["post"][1];renpy.exports.scene();renpy.exports.show("qa_post",what=s.r13_background(s.r13_scene_bg));result=True')
   await native_jump(q,'r13_talk_menu');await q.wait('r13_topics');await page.screenshot(path=str(OUT/'seryeon-post-questions.png'))
   report['post_menu']=await q.py('import renpy;s=renpy.store;pose=s.r13_conversation_pose("seryeon");p=s.r13_dialogue_source_profile("seryeon",pose,840);result=dict(pose=pose,file=p["frames"]["neutral"]["file"])');assert report['post_menu']['pose']=='chair_listen'
   await asyncio.sleep(.2);st=await q.state();button=next(b for b in st['buttons'] if '1  ' in b['text']);x,y,w,h=button['rect'];await q.input(x+w/2,y+h/2);await q.wait('say');await page.screenshot(path=str(OUT/'seryeon-post-dialogue.png'))
   # Save the actual authored line state. A forced speaker during Dad's line
   # is only a render fixture and correctly resets when Ren'Py resumes it.
   await q.input(810,640);await q.wait('say');await asyncio.sleep(.3)
   report['chair_before_save']=await q.py('import renpy;s=renpy.store;result=dict(pose=s.r13_current_pose,packet=s.r13_packet)')
   await q.say_save(3);await q.say_load(3);await page.screenshot(path=str(OUT/'seryeon-chair-restored.png'))
   report['chair_restored']=await q.py('import renpy;s=renpy.store;result=dict(pose=s.r13_current_pose,packet=s.r13_packet)');assert report['chair_restored']==report['chair_before_save']
   await q.py('import renpy;s=renpy.store;s.r13_speaker("seryeon","thinking");renpy.exports.restart_interaction();result=True');await page.screenshot(path=str(OUT/'seryeon-chair-read.png'))
   report['chair_read_fixture']=await q.py('import renpy;s=renpy.store;result=dict(pose=s.r13_current_pose,file=s.r13_dialogue_source_profile("seryeon",s.r13_current_pose,840)["frames"]["neutral"]["file"])');assert report['chair_read_fixture']['pose']=='chair_read'
   report['authored_fixtures']=[]
   for who,pose in (('resident_ppul','kneel_stone'),('resident_teacher','write_attendance'),('resident_teacher','collapse_attendance')):
    result=await q.py('import renpy;s=renpy.store;who='+repr(who)+';pose='+repr(pose)+';expression,selected=s.r13_line_performance("qa:authored",0,(who,"fixture","neutral",pose));s.r13_speaker(who,expression,selected);renpy.exports.restart_interaction();spec=s.r13_fullbody_spec(who,selected);result=dict(person=who,requested=pose,selected=selected,current=s.r13_current_pose,file=spec["file"],image=spec["image"])')
    assert result['selected']==pose and result['current']==pose
    report['authored_fixtures'].append(result);await page.screenshot(path=str(OUT/(who+'-'+pose+'.png')))
   report['status']='passed'
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await browser.close()
if __name__=='__main__':asyncio.run(main())
