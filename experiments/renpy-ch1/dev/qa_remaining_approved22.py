"""Actual authored event routes with explicit state fixtures; no campaign playthrough."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
OUT=Path('/workspace/remaining22-runtime');OUT.mkdir(exist_ok=True)
ROUTES=[
 ('r13_wf_hideout',4,'school',[],['F13'],['kid_kkomi:door_peek','kid_kkomi:hideout_proud','kid_bang:cling_leg']),
 ('r13_ws_teacher_talk',12,'school',[],[],['resident_teacher:write_attendance']),
 ('r13_ws_lab',12,'facility',['mom_reunited'],[],['mom:show_fragments']),
 ('r13_ws_soup',12,'school',[],[],['kid_dodam:lick_ladle','kid_saemi:hide_bowl']),
 ('r13_cv_morning',13,'square',[],[],['npc_pandol:point_name']),
 ('r13_cv_night',13,'square',['teacher_on_cart'],[],['resident_teacher:collapse_attendance','resident_badook:block_cart']),
 ('r13_cv_altar',14,'altar',['cv_night','ws_tosil_kept','mom_reunited'],[],['resident_tosil:hold_storybook','granny:withdraw_hand']),
 ('r13_nt_after_trial',10,'square',['nt_lit_lamps','owl_hat'],[],['chorong_mother:offer_lantern'])]
SNAP='''import renpy
s=renpy.store
person=s.r13_motion_person;pose=s.r13_current_pose
p=s.r13_dialogue_source_profile(person,pose,840) if person else None
result=dict(person=person,pose=pose,identity=getattr(s,'identity',None),packet=s.r13_packet,file=p['frames']['neutral']['file'] if p else None,canvas=p['canvas'] if p else None,visible='r13_visitor' in renpy.exports.get_showing_tags())'''
async def setup(q,day,location,flags=(),evidence=(),period=0):
 await q.py('import renpy;s=renpy.store;s.r13_end_skip_modes();s.r13_ep_line_art_clear();s.room13=s.r13_new();s.r13_upgrade();s.r13_flag(*'+repr(['entry_corrected','lodging']+list(flags))+');s.r13_edit(day='+str(day)+',period='+str(period)+',location='+repr(location)+',case_state="occurred",daram_state="with_dad",evidence='+repr(list(evidence))+');s.room13_mode=True;s.r13_camera="stage";s.r13_meeting_active=False;s.r13_thought_active=False;s.r13_cg_active=False;s.r13_motion_person=None;s.R13_STAGE_CACHE.clear();s.place=s.R13_PLACES.get('+repr(location)+',("장면",))[0];renpy.exports.hide("r13_visitor");result=True')
 await q.py('import renpy;s=renpy.store;renpy.exports.scene();renpy.exports.show("qa_scene",what=s.r13_background(s.R13_PLACES['+repr(location)+'][1]));result=True')
async def main():
 report={'routes':[],'poses':{},'save_restore':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto('http://127.0.0.1:8891/preview/room13-dev/');await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.8)
   report['version']=await q.py('import renpy;result=renpy.store.config.version')
   selected=os.environ.get('ROOM13_ROUTE_FILTER')
   for label,day,loc,flags,evidence,wanted in ROUTES:
    if selected and label not in selected.split(','):continue
    print('ROUTE',label,flush=True);await setup(q,day,loc,flags,evidence);await native_jump(q,label);seen=set()
    for step in range(100):
     st=await q.state();snap=await q.py(SNAP);key=str(snap['person'])+':'+str(snap['pose'])
     if key in wanted and key not in seen and snap['visible'] and 'say' in st['screens']:
      assert snap['file'] and 'dialogue-pose-source/' in snap['file'],snap
      await asyncio.sleep(.25);await page.screenshot(path=str(OUT/(key.replace(':','--')+'.png')));report['poses'][key]=snap;seen.add(key);print('CAPTURE',key,flush=True)
      if key=='mom:show_fragments':
       await q.say_save(5);await q.say_load(5);restored=await q.py(SNAP);assert restored==snap,(snap,restored);report['save_restore'].append(restored);await page.screenshot(path=str(OUT/'mom-restored.png'))
     if seen==set(wanted):break
     if 'choice' in st['screens']:
      assert label=='r13_wf_hideout',st;await q.press('출석부를 보여 준다')
     elif 'say' in st['screens']:await q.input(900,615)
     elif any('계속' in x['text'] for x in st['buttons']):await q.press('계속')
     else:await asyncio.sleep(.15)
    assert seen==set(wanted),(label,seen,st,snap);report['routes'].append(dict(label=label,seen=sorted(seen)))
   # Native post-afternoon questions and dialogue use the two chair conversions.
   await setup(q,2,'post',period=1);await q.py('import renpy;s=renpy.store;s.r13_target="seryeon";s.r13_scene_bg=s.R13_PLACES["post"][1];renpy.exports.scene();renpy.exports.show("qa_post",what=s.r13_background(s.r13_scene_bg));result=True');await native_jump(q,'r13_talk_menu');await q.wait('r13_topics');await page.screenshot(path=str(OUT/'seryeon-chair-questions.png'))
   report['chair_menu']=await q.py('import renpy;s=renpy.store;pose=s.r13_conversation_pose("seryeon");p=s.r13_dialogue_source_profile("seryeon",pose,840);result=dict(pose=pose,file=p["frames"]["neutral"]["file"])');assert report['chair_menu']['pose']=='chair_listen'
   st=await q.state();bt=min((x for x in st['buttons'] if '1  ' in x['text']),key=lambda x:x['rect'][3]);x,y,w,h=bt['rect'];await q.input(x+w/2,y+h/2);await q.wait('say');await q.input(900,615);await q.wait('say');before=await q.py(SNAP);await q.say_save(6);await q.say_load(6);assert await q.py(SNAP)==before;report['save_restore'].append(before)
   for expression,pose in [('neutral','chair_listen'),('thinking','chair_read')]:
    await q.py('import renpy;s=renpy.store;s.r13_speaker("seryeon",'+repr(expression)+');renpy.exports.restart_interaction();result=True');snap=await q.py(SNAP);assert snap['pose']==pose;report['poses']['seryeon:'+pose]=snap;await page.screenshot(path=str(OUT/('seryeon--'+pose+'.png')))
   # Real Solbang field and topic route, plus explicit renderer phase fixtures.
   await setup(q,2,'forest');await native_jump(q,'r13_field');await q.wait('r13_hub');await page.screenshot(path=str(OUT/'solbang-field.png'));report['solbang_field']=await q.py('import renpy;s=renpy.store;result=next(x for x in s.r13_stage_people() if x["person"]=="resident_solbang")');assert report['solbang_field']['pose']=='work_herb_bundle'
   report['solbang_field_hit']=await q.py('import renpy;s=renpy.store;a=next(x for x in s.r13_stage_people() if x["person"]=="resident_solbang");x,y,w,h=s.r13_actor_face(a,0);f=renpy.display.render.focus_at_point(int(x+w/2-s.r13_world_offset()),int(y+h/2));acts=getattr(getattr(f,"widget",None),"action",[]);acts=acts if isinstance(acts,(tuple,list)) else [acts];result=[str(getattr(a,"value",None)) for a in acts]')
   assert any('resident_solbang' in x for x in report['solbang_field_hit'])
   await q.py('import renpy;s=renpy.store;s.r13_target="resident_solbang";result=True');await native_jump(q,'r13_talk_menu');await q.wait('r13_topics');st=await q.state();bt=min((x for x in st['buttons'] if '약초' in x['text']),key=lambda x:x['rect'][3]);x,y,w,h=bt['rect'];await q.input(x+w/2,y+h/2);await q.wait('say');await q.input(900,615);await q.wait('say');before=await q.py(SNAP);await page.screenshot(path=str(OUT/'solbang-dialogue.png'));await q.say_save(4);await q.say_load(4);assert await q.py(SNAP)==before;report['save_restore'].append(before)
   report['solbang_frames']=[]
   for slot in ('neutral','joy','angry','anxious','surprise_react','surprise_talk'):
    await q.py('import renpy;s=renpy.store;s.r13_dialogue_beat=s.dict(person="resident_solbang",talk='+repr(slot)+',react=None,settled=True,duration=.35);s.r13_speaker("resident_solbang","neutral");renpy.exports.restart_interaction();result=True');await page.screenshot(path=str(OUT/('solbang-'+slot+'.png')));report['solbang_frames'].append(slot)
   report['surprise_skip']=await q.py('import renpy;s=renpy.store;p=s.dict(person="resident_solbang",talk="surprise_talk",react="surprise_react",settled=False,duration=.35);result=[s.r13_dialogue_phase(p,0),s.r13_dialogue_phase(p,.36),s.r13_dialogue_phase(p,0,True)]');assert report['surprise_skip']==['surprise_react','surprise_talk','surprise_talk']
   await q.py('import renpy;s=renpy.store;s.r13_dialogue_beat_settle();s.r13_toggle_fast_all();result=True');await asyncio.sleep(.8);await q.py('import renpy;renpy.store.r13_end_skip_modes();result=True');report['after_skip']=await q.py(SNAP);await page.screenshot(path=str(OUT/'solbang-after-skip.png'))
   report['status']='passed'
  except Exception as e:report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:(OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
