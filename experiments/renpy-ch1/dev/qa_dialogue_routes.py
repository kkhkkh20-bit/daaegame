"""Focused production question routes and save restoration; no full-game playthrough."""
import sys,asyncio,json,os
from pathlib import Path
sys.path.insert(0,'dev')
from qa_smooth20_dialogue import ReviewQA
ns={}
exec(open('dev/qa_meeting.py').read().split('asyncio.run(main())')[0],ns)
native_jump=ns['native_jump']
from playwright.async_api import async_playwright
async def main():
 out=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-dialogue-routes'));out.mkdir(exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,out)
  await page.goto('http://127.0.0.1:8887/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu')
  await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(2)
  await q.py('''import renpy
s=renpy.store
s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="post")
s.room13_mode=True;s.r13_camera="stage";s.place="우체국";s.r13_scene_bg="r13_post";s.r13_target="resident_jongjong";s.r13_topic="jongjong:work"
result=True''')
  await q.py('import renpy;s=renpy.store;renpy.exports.scene();renpy.exports.show("qa_post",what=s.r13_background(s.R13_PLACES["post"][1]));result=True')
  await native_jump(q,'r13_talk_menu');await q.wait('r13_topics');await page.screenshot(path=str(out/'questions.png'));await q.press('배달 일은 힘들지 않니?');await q.wait('say');await asyncio.sleep(1)
  data=await q.py('import renpy;s=renpy.store;result=dict(version=s.config.version,packet=s.r13_packet,pose=s.r13_current_pose,beat=s.r13_dialogue_beat)')
  print(json.dumps(data,ensure_ascii=False));(out/'route.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));await page.screenshot(path=str(out/'dad-question.png'))
  data['plain_profiles']=await q.py('import renpy;s=renpy.store;result={p:{pose:bool(s.r13_dialogue_source_profile(p,pose,840)) for pose in ("neutral","interview_neutral","thinking","interview_distressed")} for p in s.R13_DIALOGUE_TALK_ART["people"]}')
  await q.say_save(2);await q.say_load(2);await page.screenshot(path=str(out/'restored.png'))
  data['after_load']=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,pose=s.r13_current_pose,person=s.r13_motion_person)')
  data['runtime_loadable']=await q.py('import renpy;s=renpy.store;result={p:all(__import__("renpy").store.renpy.loadable(f["file"]) for profile in e["profiles"].values() for f in profile["frames"].values()) for p,e in s.R13_DIALOGUE_TALK_ART["people"].items()}')
  await q.py('import renpy;s=renpy.store;s.r13_edit(location="square");s.place="광장";s.r13_scene_bg="r13_square";s.r13_target="resident_hyeoni";renpy.exports.scene();renpy.exports.show("qa_square",what=s.r13_background(s.R13_PLACES["square"][1]));result=True')
  await native_jump(q,'r13_talk_menu');await q.wait('r13_topics');await page.screenshot(path=str(out/'hyeoni-questions.png'))
  data['hyeoni']=await q.py('import renpy;s=renpy.store;p=s.r13_dialogue_source_profile("resident_hyeoni","neutral",840);result=dict(pose=s.r13_conversation_pose("resident_hyeoni"),file=p["frames"]["neutral"]["file"],loadable=s.renpy.loadable(p["frames"]["neutral"]["file"]))')
  await q.py('import renpy;s=renpy.store;s.r13_edit(day=2,period=2,location="dining");s.place="식당";s.r13_scene_bg="r13_dining";result=True')
  await native_jump(q,'r13_field');await q.wait('r13_hub');await asyncio.sleep(.5)
  data['dining_hits']=await q.py("""import renpy
s=renpy.store
result=[]
for a in s.r13_stage_people():
 x,y,w,h=s.r13_actor_face(a,0)
 focus=renpy.display.render.focus_at_point(int(x+w/2),int(y+h/2))
 actions=getattr(getattr(focus,'widget',None),'action',[])
 if not isinstance(actions,list):actions=[actions]
 values=[getattr(action,'value',None) for action in actions if action.__class__.__name__=='Return']
 result.append(dict(person=a['person'],face=[x,y,w,h],hits=values))
""")
  await page.screenshot(path=str(out/'dining.png'))
  (out/'route.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));await b.close()
if __name__=='__main__':asyncio.run(main())
