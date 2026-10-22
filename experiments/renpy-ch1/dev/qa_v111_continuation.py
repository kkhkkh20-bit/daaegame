"""Actual existing UI clicks from a genuine D03 play save.
No story-state injection; saved runs are used to avoid repeating checked days.
"""
import asyncio,ast,json,os,re,shutil,subprocess,time
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA,PROBE
from qa_v111_play import Fast
PROBE=PROBE.replace("names=[","names=['_exception',",1)

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/work/v111/continuation'));OUT.mkdir(parents=True,exist_ok=True)
# Test-only extraction of the actual native proof calls: not game progression.
PROOFS={}
for f in (ROOT/'game').glob('room13_v111*.rpy'):
 for m in re.finditer(r'call r13_v111_proof\(([^\n]+)\)',f.read_text()):
  try:args=ast.literal_eval('('+m.group(1)+',)')
  except (ValueError,SyntaxError):continue
  PROOFS[args[0]]=args[1]
PICKS={'private_handoff10':lambda s:1 if s['values'].get('owl_invitation_testimony') else 0,
 'inspect_gate4':lambda s:next(i for i,k in enumerate(['d4_fence_seen','d4_tracks_seen','d4_bucket_seen']) if not s['values'].get(k)),
 'mother_questions11':lambda s:next(i for i,k in enumerate(['mother_q_life','mother_q_invitation','mother_q_return']) if not s['values'].get(k)),
 'morning_prep12':lambda s:3,
 'handover_plan13':lambda s:1 if s['values'].get('handover_prepared13') else 0,
 'transport_cleanup13':lambda s:next((i for i,k in enumerate(['actual_stop_actor_refuses_transport','current_order_execution_stopped','Kkaro_forced_transport_refused','cart_returned','relay_stopped']) if not s['values'].get(k)),5)}
async def main():
 server=subprocess.Popen(['python3','-m','http.server','8766','--bind','127.0.0.1'],cwd=ROOT.parents[1],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  async with async_playwright() as pw:
   profile=OUT/'profile'
   if not profile.exists():shutil.copytree(os.environ.get('V111_PROFILE_SOURCE','/workspace/work/v111/browser/profile-shelter'),profile,ignore=shutil.ignore_patterns('Singleton*','LOCK','lockfile'))
   b=await pw.chromium.launch_persistent_context(str(profile),executable_path='/usr/bin/chromium',viewport=dict(width=1280,height=720),headless=True,args=['--no-sandbox','--remote-debugging-port=9223','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
   try:
    for page in b.pages:await page.close()
    pg=await b.new_page();q=Fast(pg,OUT);events=[];heard=[];book=None;wrong_recipient=0;map_target=None;shots=set();tries={};last=None;stale=0
    await pg.goto('http://localhost:8766/preview/room13-dev/',wait_until='domcontentloaded',timeout=180000)
    await pg.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await asyncio.sleep(10);await q.input(1100,600);await q.wait('main_menu')
    await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
    print('BUILD_VERSION',await q.py('import renpy;result=renpy.store.config.version'),flush=True)
    # Original profile saves belong to localhost:8766. IndexedDB is origin
    # scoped; export only an existing save, never modify its narrative state.
    slot=os.environ.get('V111_RESUME','v111-sleep3')
    exists=await q.py('import renpy;result=renpy.exports.can_load('+repr(slot)+')')
    if not exists:raise AssertionError('Actual play save unavailable at this origin: '+slot)
    for old,new in json.loads(os.environ.get('V111_COPY_SLOTS','{}')).items():
     await q.py('import renpy;renpy.loadsave.copy_save('+repr(old)+','+repr(new)+');result=True')
    code='import renpy;renpy.exports.load('+repr(slot)+')'
    await pg.evaluate('code=>{renpy_exec("exec("+JSON.stringify(code)+")").catch(()=>{});return true;}',code)
    await asyncio.sleep(3);await pg.evaluate("window._renpy_cmd_callback({data:true})")
    for step in range(20000):
     st=await q.py('import renpy;ns={};exec('+repr(PROBE)+',ns);result=ns["result"];s=renpy.store;result["v111_probe"]=dict(gate=s.room13.get("v111",{}).get("gate"),claim=getattr(s,"v111_claim",None),binding=s.r13_v111_binding(),scene=s.room13.get("v111",{}).get("scene"),packet=list(getattr(s,"r13_packet",[])[:2]))');room=st['room'];v=room.get('v111',{});values=v.get('values',{});screens=st['screens'];gate=v.get('gate');loc=room.get('location')
     assert '_exception' not in screens,('Game exception',sc if 'sc' in locals() else None)
     extra=st.pop('v111_probe')
     sc=extra['scene']
     if os.environ.get('V111_FIELD_AUDIT') and 'r13_hub' in screens:
      await asyncio.sleep(.8)
      snapshots=[];before=json.dumps(room,sort_keys=True)
      width=await q.py('import renpy;result=renpy.store.r13_world_width()')
      for view in (('initial','right','left') if width>1280 else ('initial',)):
       if view!='initial':
        arrow='›' if view=='right' else '‹'
        current=await q.state()
        if not any(b.get('text','').strip()==arrow for b in current.get('buttons',[])):continue
        await q.press(arrow);await asyncio.sleep(1)
       geometry=await q.py('import renpy;s=renpy.store;actors=s.r13_stage_people();result=dict(offset=s.r13_world_offset(),ui=s.r13_field_ui_rects(s.r13_world_offset()),faces=[dict(person=a["person"],rect=s.r13_actor_face_target(a)) for a in actors],labels=s.r13_actor_nameplates(actors),period=s.r13_daylight(),background=s.r13_world_file(s.room13["location"],s.r13_daylight()))')
       def overlap(a,b):return bool(a and max(a[0],b[0])<min(a[0]+a[2],b[0]+b[2]) and max(a[1],b[1])<min(a[1]+a[3],b[1]+b[3]))
       issues=[(kind,row['person'],row['rect']) for kind in ('faces','labels') for row in geometry[kind] if any(overlap(row['rect'],r) for r in geometry['ui'])]
       geometry['issues']=issues;snapshots.append(geometry);await q.shot('field-audit-'+view)
      for name,viewport in [('portrait',dict(width=390,height=844)),('phone-landscape',dict(width=844,height=390))]:
       await pg.set_viewport_size(viewport);await asyncio.sleep(1)
       geometry=await q.py('import renpy;s=renpy.store;actors=s.r13_stage_people();result=dict(offset=s.r13_world_offset(),ui=s.r13_field_ui_rects(s.r13_world_offset()),faces=[dict(person=a["person"],rect=s.r13_actor_face_target(a)) for a in actors],labels=s.r13_actor_nameplates(actors),period=s.r13_daylight(),background=s.r13_world_file(s.room13["location"],s.r13_daylight()))')
       geometry['view']=name
       geometry['control_height']=await q.py('import renpy;result=renpy.store.r13_control_height()')
       geometry['issues']=[(kind,row['person'],row['rect']) for kind in ('faces','labels') for row in geometry[kind] if any(overlap(row['rect'],r) for r in geometry['ui'])]
       snapshots.append(geometry);await q.shot('field-audit-'+name)
      after=await q.py('import renpy;result=renpy.store.room13');assert before==json.dumps(after,sort_keys=True),'Field presentation changed story state'
      report=dict(status='passed' if not any(x['issues'] for x in snapshots) else 'issues',scope='Actual saved field, existing pan controls, phone viewports; no story-state injection',snapshots=snapshots)
      (OUT/'field-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));assert report['status']=='passed',report
      return
     if os.environ.get('V111_WRONG_RECIPIENT') and wrong_recipient==2:
      assert 'say' not in screens,('Wrong recipient advanced story',gate,st.get('say'))
      if 'r13_hub' in screens:
       assert gate=='portrait_show4' and 'V111:E18' not in room['evidence'],(gate,room['evidence'])
       print('WRONG_RECIPIENT_REJECTED',flush=True);wrong_recipient=3
     if room['day']==13 and values.get('family_location')=='school' and values.get('busy:mom')=='daram_guard':
      assert values.get('location:daram')=='school' and values.get('location:mom')=='school',('Protected family followed Dad away from school',gate,loc,values)
     if 'say' in screens:
      line=dict(scene=sc,packet=extra.get('packet'))
      if not heard or line!=heard[-1]:heard.append(line)
     if 'say' in screens and sc=='MS14_D13_S01' and extra.get('packet',[None,None])[1]=='새가 아래를 보는데.' and 'blanket_after_art' not in shots:
      await asyncio.sleep(.4);await q.shot('blanket-after-art');shots.add('blanket_after_art')
     if os.environ.get('V111_STOP_AFTER_BLANKET') and 'blanket_after_art' in shots and sc!='MS14_D13_S01':
      assert values.get('pandol_blanket_mended') and 'V111:E13_MENDING' in room['evidence']
      assert not await q.py('import renpy;result="r13_ep_cut" in renpy.exports.get_showing_tags()')
      (OUT/'blanket-art-report.json').write_text(json.dumps(dict(status='passed',version='0.19.86',scope='Actual school blanket click, authored repair dialogue, owned record, cut cleanup on next scene',final=room),ensure_ascii=False,indent=2));return
     state=(gate,sc,tuple(screens),st.get('say'))
     stale=stale+1 if state==last else 0;last=state
     assert stale<25,('Input did not progress',state)
     if step%5==0:
      print('PROGRESS',step,sc,gate,loc,screens,flush=True)
      (OUT/'current.json').write_text(json.dumps(dict(scene=sc,gate=gate,location=loc,screens=screens,say=st.get('say')),ensure_ascii=False))
     if 'r13_hub' in screens and sc and gate!='travel':
      save_key='v111-continue-'+gate
      if save_key not in shots:
       await q.py('import renpy;renpy.exports.save('+repr(save_key)+');result=True');shots.add(save_key)
       if gate in ('teacher_relief_check13','carrier_receipt12','device_detach14','transport_cleanup13','blanket_mend13'):await q.shot('field-'+gate)
     if sc and sc not in shots and 'say' in screens:
      await q.shot(sc);shots.add(sc);events.append(dict(step=step,scene=sc,gate=gate,day=room['day'],values=values,evidence=room['evidence']));print('SCENE',sc,gate,flush=True)
     if ((os.environ.get('V111_STOP_DAY') and room['day']>=int(os.environ['V111_STOP_DAY'])) or (os.environ.get('V111_STOP_GATE')==gate)) and 'r13_hub' in screens:
      (OUT/'checkpoint-report.json').write_text(json.dumps(dict(status='checkpoint_reached',day=room['day'],scope='Actual clicks from previous genuine save; later days not yet tested',events=events,final=room),ensure_ascii=False,indent=2));return
     if values.get('story14_completed'):
      checks=[]
      assert values.get('carried_dry_blankets',0)>=0,values
      checks.append('Blanket quantity never negative at completion')
      if values.get('route7')=='prevented':
       assert values.get('OWL_ALIVE') is True and not values.get('DARAM_DETAINED'),values
       checks.append('Prevented case keeps Owl alive and Daram free')
      elif values.get('route7')=='murder':
       assert values.get('OWL_ALIVE') is False and values.get('DARAM_DETAINED') is False,values
       checks.append('Incident remains fatal; day10 actual release persists')
      if values.get('route12')=='late_exposure':
       assert values.get('alive:kid_dodam') is False and values.get('alive:kid_saemi') is True,values
       checks.append('Late medical findings keep Dodam and Saemi distinct')
      else:
       assert values.get('alive:kid_dodam') is not False,values
       checks.append('Prevention does not create late ingestion death')
      outcome=values.get('outcome13')
      if outcome=='all_rescued':
       assert values.get('all_cart_handed') and all(values.get('handed:'+p) for p in values.get('cart_roster',[])),values
       assert values.get('device_joint_control') and values.get('current_transport_chain_stopped'),values
       checks.append('Every actual passenger handed over; transport stopped; device jointly locked')
      elif outcome=='family_priority':
       assert values.get('family_benefits_received') and values.get('night14_lodging')=='gate' and not values.get('all_cart_handed'),values
       checks.append('Family departure keeps gate lodging without inventing other rescues')
      elif outcome=='partial_rescue':
       assert not values.get('all_cart_handed'),values
       assert sum(bool(values.get('handed:'+p)) for p in values.get('cart_roster',[]))==1,values
       for patient in values.get('cart_roster',[]):
        assert values.get('location:'+patient)==('school' if values.get('handed:'+patient) else 'square'),(patient,values)
       checks.append('Partial receipt does not become full rescue')
      elif outcome=='crowd_violence':
       assert values.get('crowd_injury') is True,values
       checks.append('Violence consequence retained through ending')
       forbidden=ROOT/'game/v111/records.json'
       original=json.loads(forbidden.read_text())['records']
       dad_offer=original['MS14_D14_S05_L0015']['text']
       assert not any(h['scene']=='MS14_D14_S05' and h['packet'][1]==dad_offer for h in heard),heard
       if values.get('family_location')=='school':
        away={original['MS14_D13_C_L0006']['text'],original['MS14_D13_C_L0007']['text']}
        assert not any(h['scene']=='MS14_D13_C' and h['packet'][1] in away for h in heard),heard
       checks.append('Off-site child dialogue and immediate Dad cookie reconciliation excluded')
      if values.get('buri_device_present') and not values.get('buri_supply_participated'):
       original=json.loads((ROOT/'game/v111/records.json').read_text())['records']
       false_recall=original['MS14_D14_S02_L0046']['text']
       assert not any(h['scene']=='MS14_D14_S02' and h['packet'][1]==false_recall for h in heard),heard
       checks.append('Non-participating Buri never claims hauling school supplies')
      report=dict(status='passed',scope='Existing-save continuation; actual field/map/topic/notebook clicks, no narrative state injection',checks=checks,heard=heard,events=events,final=room)
      (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));return
     if 'say' in screens:await q.input(900,590);continue
     if 'choice' in screens:
      await asyncio.sleep(.5)
      branch_slot='v111-branch-'+str(sc)
      if branch_slot not in shots:
       await q.py('import renpy;renpy.exports.save('+repr(branch_slot)+');result=True');shots.add(branch_slot)
      items=await q.py('import renpy;result=[i.caption for i in renpy.display.screen.get_screen("choice").scope["items"] if i.action is not None]')
      preferred=next((t for t in ['하차한 사람부터 부축한다','그릇을 돌려주러 같이 가자.','오늘 안에 학교 자리를 확인하고 옮긴다.','아이들은 학교에서 기다리게 하자.','다람과 남고 까로를 의료진에게 보낸다','짐 안에 둔다','준비된 물자를 학교로 옮긴다','없는 운반수단을 지금 구한다','배식 전에 더 살핀다','돌목에게 감독을 맡긴다','조건을 더 묻는다','거절하고 현장에 남는다','엄마와 다람이 곁에 남게 한다','안에서 직접 듣는다','토실이 이름을 쓰겠다면 기다린다'] if t in items),items[0])
      # Once the family offer has been clarified, refuse it rather than looping.
      if '거절하고 현장에 남는다' in items and values.get('family_offer_terms_seen'):preferred='거절하고 현장에 남는다'
      overrides=json.loads(os.environ.get('V111_BRANCHES','{}'))
      requested=overrides.get(str(sc),[])
      if isinstance(requested,str):requested=[requested]
      preferred=next((caption for caption in requested if caption in items),preferred)
      print('CHOICE',sc,items,'PICK',preferred,flush=True)
      await q.press(preferred);continue
     if 'r13_crisis_proof' in screens:
      claim=extra['claim'];title=claim[5:];correct=PROOFS[title]
      selected=room['arguments'].get(claim,[]);missing=[k for k in correct if 'V111:'+k not in selected]
      if missing:book='V111:'+missing[0];await q.press('근거를 내놓는다')
      else:await q.press('논리를 연결한다')
      continue
     if 'r13_book' in screens:
      if not book:
       if sc=='MS14_D13_S04' and values.get('current_order_execution_stopped') and not values.get('relay_stopped'):book='V111:E13_ORDER'
       elif sc=='MS14_D14_S02' and os.environ.get('V111_DEVICE_RECORD')=='supply':book='V111:E14_SUPPLY'
       else:book='V111:E13_HANDOVER'
      if wrong_recipient==2:await asyncio.sleep(.2);continue
      entries=await q.py('import renpy;result=list(renpy.display.screen.get_screen("r13_book").scope["entries"])')
      assert book in entries,(book,entries)
      name=await q.py('import renpy;result=renpy.store.ROOM13["evidence"]['+repr(book)+']["name"]')
      try:await q.press(name)
      except AssertionError:
       page=await q.py('import renpy;s=renpy.store;c=renpy.display.screen.get_screen("r13_book").scope;e=c["entries"];result=[e.index('+repr(book)+')//s.r13_record_page_size(),s.r13_record_page(e,c["page"])]')
       await q.press('이전' if page[0]<page[1] else '다음');continue
      await q.press('보여주기');book=None
      if wrong_recipient==1:wrong_recipient=2
      continue
     if gate=='labor_sheet4' and step%5==0:
      print('LABOR_DEBUG',await q.py('import renpy;s=renpy.store;result=dict(people=s.r13_visible_people(),questions=[(x[0],str(x[1])) for x in s.r13_v111_questions("neoul")],pick=getattr(s,"v111_pick",None),binding=s.r13_v111_binding())'),flush=True)
     opts=extra['binding'].get('options',[])
     if gate=='morning_prep12' and os.environ.get('V111_PREP12'):
      idx=next((i for i,k in enumerate(['medicine_locked','warm_seat_ready','carrier_arrived']) if not values.get(k)),3)
     else:idx=PICKS.get(gate,lambda s:0)(dict(values=values))
     if gate=='morning_prep12' and os.environ.get('V111_MADAM') and not values.get('madam_observer_consent'):idx=4
     if gate=='transport_cleanup13' and idx==5 and os.environ.get('V111_BURI') and not values.get('buri_device_consent'):idx=6
     opt=opts[idx] if opts else None
     if gate=='portrait_show4' and os.environ.get('V111_WRONG_RECIPIENT') and wrong_recipient==0:opt=dict(opt,person='resident_somi')
     if 'r13_topics' in screens:
      person_id=await q.py('import renpy;result=renpy.display.screen.get_screen("r13_topics").scope["person"]')
      if gate=='portrait_show4' and os.environ.get('V111_WRONG_RECIPIENT') and wrong_recipient==0 and person_id=='resident_somi':
       book='V111:E09';wrong_recipient=1;await q.press('자료');continue
      choices=[o for o in opts if o.get('person')==person_id]
      if not choices:await q.press('돌아가기');continue
      chosen=opt if opt in choices else choices[0]
      if chosen.get('present'):book=chosen['present']
      await q.press(chosen['title']);continue
     if 'r13_map' in screens:
      target=map_target or next(o['move'] for o in opts if o.get('move'))
      map_target=None
      region=await q.py('import renpy;result=renpy.store.r13_map_region('+repr(target)+')')
      await q.press({'village':'마을','inn':'여관 안','mountain':'숲·산길'}[region]);await q.value(target)
      if 'r13_map'in (await q.state())['screens']:await q.press('이곳으로 이동')
      continue
     if 'r13_hub' in screens:
      assert opt,('Empty field',extra)
      if opt.get('location')!=loc:
       map_target=opt['location'];await q.press('지도');continue
      if opt.get('move'):map_target=opt['move'];await q.press('지도');continue
      if opt.get('person'):
       p=opt['person'];buttons=[x for x in st['buttons'] if x.get('value')==repr(('person',p)) and x['text'].strip()]
       if buttons:await q.value(('person',p));continue
       x=await q.py('import renpy;s=renpy.store;result=next(a["x"] for a in s.r13_stage_people() if a["person"]=='+repr(p)+')-s.r13_world_offset()')
       if x<0 or x>1280:
        await q.press('‹' if x<0 else '›');await asyncio.sleep(.7)
       else:await asyncio.sleep(.35)
       continue
      if opt.get('object'):
       key=opt['object'];attempt=tries.get((gate,key),0);tries[(gate,key)]=attempt+1
       fx,fy=[(.5,.5),(.1,.1),(.9,.9),(.1,.9),(.9,.1),(.25,.5),(.75,.5)][attempt%7]
       rect=await q.py('import renpy;result=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if f.x is not None and f.w and f.h for a in (getattr(f.widget,"clicked",None) if isinstance(getattr(f.widget,"clicked",None),(list,tuple)) else [getattr(f.widget,"clicked",None)]) if getattr(a,"value",None)=='+repr(('object',key))+'),None)')
       if rect:x,y=rect[0]+rect[2]*fx,rect[1]+rect[3]*fy
       else:
        x,y=await q.py('import renpy;s=renpy.store;x,y,w,h=s.ROOM13["objects"][s.room13["location"]]['+repr(key)+']["rect"];result=[x+w*'+str(fx)+'-s.r13_world_offset(),y+h*'+str(fy)+']')
       if not 0<=x<1280:await q.press('‹' if x<0 else '›');await asyncio.sleep(.7)
       else:await asyncio.sleep(.25);await q.input(x,y)
       continue
     await asyncio.sleep(.1)
    raise AssertionError('Continuation step limit reached')
   except BaseException as error:
    await pg.screenshot(path=str(OUT/'failure.png'))
    raw=await q.py('import renpy;ns={};exec('+repr(__import__('webqa').PROBE)+',ns);result=ns["result"]')
    (OUT/'failure-state.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2))
    texts=[x['text'] for x in raw.get('buttons',[]) if 'Error:' in x.get('text','') or 'Traceback' in x.get('text','')]
    if texts:print('GAME_EXCEPTION',texts[0][-2500:],flush=True)
    raise RuntimeError(str(error)[:800]) from None
   finally:await b.close()
 finally:server.terminate();server.wait(timeout=10)
if __name__=='__main__':asyncio.run(main())
