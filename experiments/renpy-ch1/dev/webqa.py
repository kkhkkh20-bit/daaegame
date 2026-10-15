"""Browser QA helpers for the Room13 web build (Playwright + renpy_exec).

Flattened from the per-release helpers qa_room13_ui0122 -> pixel_qa_flow0150 ->
pixel_qa_gate0153 -> pixel_qa_review0155 -> pixel_qa_say_records0155 ->
pixel_qa_ui0156. Use UIQA; see dev/qa_carriage.py for a small example.
"""
import asyncio, ast, json, shutil, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROBE="import renpy\nnames=['main_menu','say','choice','r13_hub','r13_interaction','r13_topics','r13_book','r13_confirm','r13_calendar','r13_map','r13_activities','r13_debate','r13_completion','r13_cinematic_view','r13_crisis','r13_crisis_proof','r13_ending_screen','r13_handoff','save','load','pause_menu','confirm']\ndef txt(w,depth=0):\n if depth>8:return ''\n if isinstance(w,renpy.text.text.Text):return ''.join(str(x) for x in w.text)\n return ' '.join(txt(x,depth+1) for x in w.visit())\nbuttons=[]\nfor f in renpy.display.focus.focus_list:\n if f.x is not None and f.w and f.h:\n  a=getattr(f.widget,'clicked',None)\n  buttons.append({'text':txt(f.widget),'value':str(getattr(a,'value','')),'rect':[f.x,f.y,f.w,f.h]})\nsay=renpy.display.screen.get_screen('say')\nresult={'screens':[n for n in names if renpy.display.screen.get_screen(n)],'room':getattr(renpy.store,'room13',{}),'say':str(say.scope.get('what','')) if say else '', 'buttons':buttons}\n"

# ---- from qa_room13_ui0122.py
EXTRA="""import renpy
result={'version':renpy.store.config.version,'fast':renpy.store.r13_fast_read,'people':renpy.store.r13_people() if getattr(renpy.store,'room13_mode',False) else [],'speaker':getattr(renpy.store,'dialogue_speaker',None)}
"""
class QA:
 def __init__(self,page,out):self.p=page;self.out=out;self.touch=False;self.events=[];self.seen=set()
 async def py(self,code):return await self.p.evaluate('code=>renpy_exec(code)',code)
 async def state(self):return await self.py('ns={};exec('+repr(PROBE)+',ns);result=ns["result"]')
 async def info(self):return await self.py(EXTRA)
 async def input(self,x,y):
  vp=self.p.viewport_size;s=min(vp['width']/1280,vp['height']/720);x=(vp['width']-1280*s)/2+x*s;y=(vp['height']-720*s)/2+y*s
  if self.touch:await self.p.touchscreen.tap(x,y)
  else:await self.p.mouse.click(x,y)
  await asyncio.sleep(.30)
 async def wait(self,name):
  for _ in range(140):
   st=await self.state()
   if name in st['screens']:await asyncio.sleep(.55);return await self.state()
   await asyncio.sleep(.15)
  raise AssertionError((name,st))
 async def press(self,label):
  await asyncio.sleep(.55);st=await self.state()
  matches=[b for b in st['buttons'] if label in b['text'] and b['rect'][3]>15]
  assert matches,(label,st)
  b=min(matches,key=lambda b:b['rect'][2]*b['rect'][3]);x,y,w,h=b['rect']
  assert 0<=x+w/2<=1280 and 0<=y+h/2<=720,b
  await self.input(x+w/2,y+h/2)
 async def shot(self,name):
  await asyncio.sleep(.2);await self.p.screenshot(path=str(self.out/(name+'.png')))
  (self.out/(name+'.json')).write_text(json.dumps(await self.state(),ensure_ascii=False,indent=2));print('SHOT',name,flush=True)
 async def advance(self):
  for _ in range(230):
   st=await self.state()
   if 'r13_cinematic_view'in st['screens']:await self.press('계속');continue
   if any(x in st['screens'] for x in ['choice','r13_hub','r13_book','r13_confirm','r13_interaction','r13_topics']):
    await asyncio.sleep(.55);return await self.state()
   if 'say'in st['screens']:
    info=await self.info();who=info.get('speaker')
    if who and who not in self.seen:
     self.seen.add(who);await self.shot('speaker-'+str(who))
    await self.input(810,640)
   else:await asyncio.sleep(.2)
  raise AssertionError(st)
 async def cancel_unchanged(self,open_label,screen,close_label):
  before=(await self.state())['room'];await self.press(open_label);await self.wait(screen);await self.press(close_label);await self.wait('r13_hub')
  assert (await self.state())['room']==before,(open_label,'changed state')
  self.events.append(open_label+' cancel retains complete run state')
 async def npc(self,person):
  info=await self.info();assert person in info['people'],info
  i=info['people'].index(person);await self.input(175+285*i,430);await self.advance();await self.wait('r13_interaction')
 async def gate_only(self):
  await self.wait('main_menu');await self.press('처음부터');await self.advance();await self.wait('r13_hub');await self.press('원본 대조');await self.wait('r13_confirm');await self.press('진행한다')
  for _ in range(100):
   st=await self.state();info=await self.info()
   if 'say' in st['screens'] and info.get('speaker')=='karo':break
   if 'say' in st['screens']:await self.input(810,640)
   else:await asyncio.sleep(.2)
  assert info.get('speaker')=='karo',info
  scene=await self.py("import renpy; result={'clock':renpy.store.r13_clock(),'scene_key':renpy.store.r13_scene_key,'daylight':renpy.store.r13_daylight(),'gate_file':renpy.store.r13_art_path('gate'),'background':str(renpy.store.r13_background('winter').child)}")
  assert st['room']['period']==2 and scene['daylight']=='evening' and scene['scene_key'][3]=='evening',scene
  await self.shot('gate-wait-karo-evening')
  return {'status':'passed','checks':['Fresh start and gate wait: Karo first dialogue shows evening background and evening HUD'],'scene':scene}
 async def run(self):
  await self.wait('main_menu');await self.shot('01-title');self.events.append('fresh title')
  await self.press('설정');await self.wait('pause_menu');await self.shot('02-title-settings');await self.press('돌아가기');await self.wait('main_menu')
  await self.press('이어하기');await self.wait('load');await self.shot('03-title-load');await self.press('돌아가기');await self.wait('main_menu')
  await self.press('처음부터');await self.advance();await self.wait('r13_hub');await self.shot('04-entrance')
  await self.press('원본 대조');await self.wait('r13_confirm');await self.shot('05-wait-confirm');await self.press('진행한다');await self.advance();await self.wait('r13_hub')
  assert (await self.state())['room']['period']==2
  assert not any('빠르게'in b['text'] or '해 볼 일'in b['text'] for b in (await self.state())['buttons'])
  await self.shot('06-gate-hub');self.events.append('gate wait real consequence; no read-fast hub control')
  await self.press('설정');await self.wait('pause_menu');a=(await self.info())['fast'];await self.press('읽은 대사 빠르게');assert (await self.info())['fast']!=a
  await self.shot('07-game-settings');await self.press('읽은 대사 빠르게');assert (await self.info())['fast']==a;await self.press('돌아가기');await self.wait('r13_hub');self.events.append('settings read-fast toggle works both directions')
  await self.npc('karo');await self.shot('08-karo-interaction');await self.press('대화하기');await self.wait('r13_topics');await self.shot('09-karo-topics');await self.press('돌아가기');await self.wait('r13_interaction');await self.press('돌아가기');await self.advance()
  await self.cancel_unchanged('현장 활동','r13_activities','돌아가기');await self.cancel_unchanged('이동하기','r13_map','돌아가기')
  await self.press('이동하기');await self.wait('r13_map');await self.press('수리점');await self.advance();await self.wait('r13_hub');await self.shot('10-workshop-hub')
  await self.npc('buri');await self.shot('11-buri-interaction');await self.press('대화하기');await self.wait('r13_topics');await self.shot('12-buri-topics')
  await self.press('마차 수리를 부탁한다');await self.advance();await self.wait('r13_topics');await self.shot('12b-buri-read-topic');self.events.append('Buri selected question plays real dialogue and returns as read')
  before=(await self.state())['room'];await self.press('자료 제시하기');await self.wait('r13_book');await self.shot('13-buri-present');await self.press('제시 취소');await self.advance();assert (await self.state())['room']==before
  assert 'r13_topics' in (await self.state())['screens']
  self.events.append('Buri topics present cancel returns to topics without disclosure or time cost')
  st=await self.state()
  if 'r13_topics'in st['screens']:await self.press('돌아가기');await self.wait('r13_interaction')
  await self.p.set_viewport_size({'width':844,'height':390});self.touch=True;await asyncio.sleep(.7);await self.shot('14-mobile-interaction')
  await self.press('대화하기');await self.wait('r13_topics');await self.shot('15-mobile-topics');await self.press('돌아가기');await self.wait('r13_interaction')
  before=(await self.state())['room'];await self.press('제시하기');await self.wait('r13_book');await self.shot('16-mobile-present');await self.press('제시 취소');await self.advance();assert (await self.state())['room']==before
  assert 'r13_interaction' in (await self.state())['screens']
  self.events.append('Mobile interaction present cancel returns to interaction without disclosure or time cost')
  if 'r13_topics' in (await self.state())['screens']:await self.press('돌아가기');await self.wait('r13_interaction')
  await self.press('돌아가기');await self.advance();await self.wait('r13_hub');await self.shot('17-mobile-hub')
  await self.cancel_unchanged('현장 활동','r13_activities','돌아가기')
  await self.press('설정');await self.wait('pause_menu');await self.shot('18-mobile-settings');a=(await self.info())['fast'];await self.press('읽은 대사 빠르게');assert (await self.info())['fast']!=a;await self.press('읽은 대사 빠르게');await self.press('돌아가기');await self.wait('r13_hub')
  self.events.append('844x390 real touchscreen topics/present/cancel/settings working')
  return {'status':'passed','checks':self.events,'seen_speakers':sorted(self.seen),'info':await self.info()}

# ---- from pixel_qa_flow0150.py
FLOW_PROBE=PROBE.replace('names=[',"names=['r13_arrival_card','_exception','r13_entry_topics','r13_entry_karo_topics','r13_object_context',")
MATRIX='''import renpy,copy
s=renpy.store
original=copy.deepcopy(s.room13)
rows=[];failures=[]
try:
 links={key:(place,obj) for (place,obj),keys in s.R13_CONTEXT_ACTIVITIES.items() for key in keys}
 for key,a in s.ROOM13['activities'].items():
  n=copy.deepcopy(original);n.update(day=max(a.get('day',[1,13])[0],8 if key.startswith('w2_') else 1),period=a.get('period',[0])[0],location=a['place'],done=[])
  n['case_state']=a.get('case','prevented');n['flags']=['lodging'];n['evidence']=[];n['passage_open']=True
  for flag in a.get('need',[]):n['evidence' if flag in s.ROOM13['evidence'] else 'flags'].append(flag)
  for name,values in a.get('state',{}).items():n[name]=values[0]
  for name,values in a.get('not_state',{}).items():
   if n.get(name) in values:n[name]='rescued' if name=='daram_state' else None
  n['observations']={'first':{'time':(n['day']-1)*4+n['period']-1,'load':'day_low'}}
  n['scout_revision']=n.get('convoy_revision',0)
  s.room13=n
  available={k for k,a in s.r13_actions()}
  routed={k for obj in s.ROOM13['objects'].get(n['location'],{}) for k,a in s.r13_object_actions(obj)}
  if key not in available:failures.append([key,'fixture not eligible'])
  if available!=routed:failures.append([key,'unrouted eligible activity',sorted(available-routed)])
  obj=links[key][1]
  if key not in [k for k,a in s.r13_object_actions(obj)]:failures.append([key,'missing own context'])
  fixture_state=copy.deepcopy(n)
  n['done']=[key];s.room13=n
  if key in [k for k,a in s.r13_object_actions(obj)]:failures.append([key,'completed action repeats'])
  n['done']=[];n['day']=a.get('day',[1,13])[1]+1;s.room13=n
  if key in [k for k,a in s.r13_object_actions(obj)]:failures.append([key,'invalid day allowed'])
  rows.append({'activity':key,'location':a['place'],'object':obj,'eligible_actions':sorted(available),'state':fixture_state})
 for loc,objects in s.ROOM13['objects'].items():
  n=copy.deepcopy(original);n['location']=loc;n['flags']=['lodging'];s.room13=n
  for obj in objects:
   if bool(s.r13_bed_available(obj))!=(loc=='room13' and obj=='bed'):failures.append([loc,obj,'sleep location mismatch'])
 n=copy.deepcopy(original);n['location']='room13';n['flags']=[];s.room13=n
 if s.r13_bed_available('bed'):failures.append(['room13','bed','sleep before lodging'])
 for displaced_case,displaced_flags in [('occurred',['lodging']),('pending',['lodging','family_room_unusable'])]:
  for loc in ('room13','guestroom','clinic'):
   n=copy.deepcopy(original);n.update(location=loc,case_state=displaced_case,flags=displaced_flags);s.room13=n
   if bool(s.r13_bed_available('bed'))!=(loc=='guestroom'):failures.append([loc,'bed','displaced sleep mismatch'])
  if 'guestroom'not in s.r13_places():failures.append(['guestroom','not reachable after displacement'])
finally:s.room13=original
result={'kind':'injected-activity-eligibility-and-sleep-location-fixtures','rows':rows,'failures':failures,'state_restored':s.room13==original}
'''
class FlowQA(QA):
 async def py(self,code):return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),35)
 async def state(self):
  st=await self.py('ns={};exec('+ascii(FLOW_PROBE)+',ns);result=ns["result"]');assert '_exception'not in st['screens'],st;return st
 async def advance(self):
  for _ in range(260):
   st=await self.state()
   if 'r13_arrival_card'in st['screens']:
    await self.shot('arrival-'+str(st['room'].get('location','opening')));await self.input(800,400);continue
   if 'r13_cinematic_view'in st['screens']:await self.press('계속');continue
   if any(x in st['screens'] for x in ('choice','r13_hub','r13_book','r13_confirm','r13_topics','r13_entry_topics','r13_entry_karo_topics','r13_object_context','r13_map')):
    await asyncio.sleep(.5);return await self.state()
   if 'say'in st['screens']:await self.input(810,640)
   else:await asyncio.sleep(.15)
  raise AssertionError(st)
 async def value(self,value):
  st=await self.state();matches=[]
  for b in st['buttons']:
   try:v=ast.literal_eval(b.get('value',''))
   except (ValueError,SyntaxError):v=b.get('value','')
   if v==value and b['rect'][2]>0 and b['rect'][3]>0:matches.append(b)
  assert matches,('No direct target',value,st)
  if isinstance(value,tuple) and value[0]=='person':matches=[b for b in matches if not b['text'].strip()] or matches
  b=min(matches,key=lambda x:x['rect'][2]*x['rect'][3]);x,y,w,h=b['rect'];await self.input(x+w/2,y+h/2)
 async def natural_entry(self,route='proof'):
  await self.wait('main_menu');await self.press('처음부터');await self.advance();await self.wait('r13_hub');await self.shot('01-direct-entry')
  buttons=(await self.state())['buttons'];assert not any(x in b['text'] for b in buttons for x in ('현장 활동','여관에서 쉬기','조사하기','대화하기','제시하기'))
  before=(await self.state())['room'];await self.press('까로');await self.advance();await self.wait('r13_entry_karo_topics');await self.shot('02-karo-direct');await self.press('마저 둘러본다');await self.advance();await self.wait('r13_hub');assert (await self.state())['room']==before
  await self.value(('person','guard'));await self.wait('r13_entry_topics');await self.shot('03-guard-direct');await self.press('주변을 더');await self.wait('r13_hub');assert (await self.state())['room']==before
  if getattr(self,'gallery_say',False):
   await self.press('까로');await self.wait('r13_entry_karo_topics');await self.press('짐 좀 부탁합니다');await self.wait('say');assert (await self.info())['speaker']=='karo';await self.shot('02b-karo-real-dialogue');await self.advance();await self.wait('r13_hub')
  if route=='proof':
   for obj in ('booth','rules'):
    await self.value(('object',obj));await self.advance();await self.wait('r13_hub')
   st=await self.state();assert {'G1','G2'}<=set(st['room']['evidence']);assert st['room']['period']==1
   await self.value(('person','guard'));await self.wait('r13_entry_topics');await self.press('확인한 자료');await self.wait('r13_book')
   title=await self.py("import renpy;result=renpy.store.ROOM13['evidence']['G1']['name']");await self.press(title);await self.press('보여주기');await self.advance();await self.wait('choice');await self.shot('03b-proof-reason-choice')
   if getattr(self,'choice_persistence',False):await self.choice_save_restore()
   if getattr(self,'force_choice_migration',False):await self.forced_choice_migration()
   await self.press('원본에는 두 명');await self.advance();await self.wait('r13_hub');assert (await self.state())['room']['period']==1
  else:
   await self.value(('person','guard'));await self.wait('r13_entry_topics');await self.press('원본 대조');await self.wait('r13_confirm');await self.press('진행한다');await self.advance();await self.wait('r13_hub');assert (await self.state())['room']['period']==2
  assert 'entry_corrected'in (await self.state())['room']['flags'];await self.shot('04-entry-complete');self.events.append('Natural '+route+' entry; visible Karo direct click; guard/direct object interactions')
 async def travel(self,label,region=None):
  # 0.18.50: the map has no 마을/여관 안 tabs; inn rooms are reached from inside the inn.
  if region=='여관 안' and (await self.state())['room']['location'] not in ('inn','dining','kitchen','hall','room13','guestroom','passage'):
   await self.travel('여관 접수대')
  await self.press('지도 · 이동');await self.wait('r13_map')
  if region and region!='여관 안' and region!='마을':await self.press(region)
  await self.press(label);await self.press('이곳으로 이동');await self.advance();await self.wait('r13_hub')
 async def natural_exploration(self):
  before=(await self.state())['room'];await self.press('지도 · 이동');await self.wait('r13_map');await self.shot('05-spatial-map');await self.press('진료실');assert not any('이곳으로 이동'in b['text'] for b in (await self.state())['buttons']);await self.press('현장으로 돌아가기');await self.wait('r13_hub');assert (await self.state())['room']==before
  await self.travel('여관 접수대');assert (await self.state())['room']['location']=='inn';await self.value(('person','granny'));await self.advance();await self.wait('r13_topics');await self.press('방을 부탁한다');await self.advance();await self.wait('r13_topics');assert 'lodging'in (await self.state())['room']['flags'];await self.press('돌아가기');await self.advance();await self.wait('r13_hub');await self.shot('06-inn-direct')
  await self.travel('13호실','여관 안');assert (await self.state())['room']['location']=='room13';await self.value(('object','bed'));await self.advance();await self.wait('r13_object_context');await self.shot('07-real-bed');before=(await self.state())['room'];await self.press('침대에서 잠자기');await self.wait('r13_confirm');await self.press('아직 할 일이');await self.advance();await self.wait('r13_hub');assert (await self.state())['room']==before
  await self.travel('수리점','마을');await self.value(('person','buri'));await self.advance();await self.wait('r13_topics');await self.shot('08-buri-direct-topics');before=(await self.state())['room'];await self.value('present');await self.wait('r13_book');await self.press('제시 취소');await self.wait('r13_topics');assert (await self.state())['room']==before;await self.press('돌아가기');await self.advance();await self.wait('r13_hub')
  await self.travel('마을 입구');await self.value(('person','karo'));await self.advance();await self.wait('r13_topics');await self.value('present');await self.wait('r13_book');await self.press(await self.py("import renpy;result=renpy.store.ROOM13['evidence']['E01']['name']"));st=await self.state();assert any('까로에게 보여주기'in b['text'] for b in st['buttons']);assert not any('부리에게 보여주기'in b['text'] for b in st['buttons']);before=st['room'];await self.press('까로에게 보여주기');await self.advance();await self.wait('r13_confirm');await self.shot('09-recipient-confirm');await self.press('취소한다');await self.advance();await self.wait('r13_topics');assert (await self.state())['room']==before;await self.press('돌아가기');await self.advance();await self.wait('r13_hub')
  await self.press('수첩');await self.wait('r13_book');await self.press(await self.py("import renpy;result=renpy.store.ROOM13['evidence']['E01']['name']"));assert not any('보여주기'in b['text'] for b in (await self.state())['buttons']);await self.press('닫기');await self.wait('r13_hub')
  await self.p.set_viewport_size({'width':844,'height':390});self.touch=True;await self.travel('13호실','여관 안');await self.value(('object','bed'));await self.advance();await self.wait('r13_object_context');await self.shot('10-mobile-bed-context');before=(await self.state())['room'];await self.press('침대에서 잠자기');await self.wait('r13_confirm');await self.press('아직 할 일이');await self.advance();await self.wait('r13_hub');assert (await self.state())['room']==before;await self.press('지도 · 이동');await self.wait('r13_map');await self.shot('11-mobile-map');await self.press('현장으로 돌아가기');await self.wait('r13_hub')
  self.events.append('Natural direct-map lodging/bed and sleep cancel; Buri→Karo recipient isolation; notebook has no stale present action; 844x390 touch map/bed')
  before=(await self.state())['room'];await self.value(('object','bed'));await self.advance();await self.wait('r13_object_context');await self.press('침대에서 잠자기');await self.wait('r13_confirm');await self.press('잠자리에 든다');await self.advance();await self.wait('choice');await self.press('다람이 옆에 앉는다');await self.advance();await self.wait('r13_hub');after=(await self.state())['room'];assert after['day']==before['day']+1 and after['period']==0 and after['location']=='inn',after;await self.shot('12-mobile-real-sleep-next-day');self.events.append('Actual room-bed sleep executes first-night scenes and reaches day2 morning inn')

 async def activity_click_fixtures(self,matrix):
  shots=[]
  for i,row in enumerate(matrix['rows']):
   state=row['state']
   await self.py("import renpy\ns=renpy.store\ns.room13="+ascii(state)+"\ns.place=s.R13_PLACES[s.room13['location']][0]\nrenpy.exports.scene()\nrenpy.exports.show('qa_flow_background',what=s.r13_background(s.R13_PLACES[s.room13['location']][1]))\nrenpy.exports.restart_interaction()\nresult=True")
   await self.wait('r13_hub');await self.value(('object',row['object']));await self.advance();await self.wait('r13_object_context')
   st=await self.state();assert any(b['value']==repr(('activity',row['activity'])) for b in st['buttons']),('activity missing from actual object screen',row['activity'],st)
   name='activity-%02d-%s'%(i,row['activity']);await self.shot(name);shots.append({'activity':row['activity'],'file':name+'.png','object':row['object']})
   before=st['room'];await self.value(('activity',row['activity']));await self.wait('r13_confirm');assert (await self.state())['room']==before
   # Fixture exits the confirmation via an explicit label reset, so synthetic
   # day/state combinations cannot accidentally run unrelated story events.
   # No activity is completed or claimed naturally played by this matrix.
   await self.py("import renpy\ns=renpy.store\nfor f in renpy.display.focus.focus_list:\n action=getattr(f.widget,'action',None)\n if getattr(action,'value',None) is False:\n  f.widget.action=s.Jump('r13_field');f.widget.clicked=f.widget.action\nresult=True")
   await self.press('돌아간다');await self.wait('r13_hub');assert (await self.state())['room']==before
  return {'kind':'injected-state-real-object-and-activity-clicks-to-confirmation-not-completion','shots':shots}

 async def map_lock_fixtures(self):
  original=(await self.state())['room'];checks=[]
  cases=[('unregistered',1,[],False),('lodging',1,['lodging'],False),('passage-known-closed',5,['lodging','passage_known'],False),('passage-open',5,['lodging','passage_known'],True),('week2-no-signal',8,['lodging'],False),('week2-signal',8,['lodging','E19'],False),('displaced-guestroom',4,['lodging','family_room_unusable'],False)]
  for name,day,flags,opened in cases:
   state=json.loads(json.dumps(original));state.update(day=day,period=0,location='gate',flags=flags,passage_open=opened,evidence=[])
   await self.py('import renpy;s=renpy.store;s.room13='+ascii(state)+';renpy.exports.restart_interaction();result=True');await self.wait('r13_hub');await self.press('지도 · 이동');await self.wait('r13_map')
   allowed=await self.py('import renpy;result=renpy.store.r13_places()')
   for region,label in [('village','마을'),('inn','여관 안')]+([('mountain','북쪽 산길')]if day>=8 else []):
    await self.press(label)
    data=await self.py("import renpy;s=renpy.store;result={'region':renpy.display.screen.get_screen('r13_map').scope['region'],'nodes':s.r13_map_nodes(%r)}"%region);assert data['region']==region,data
    keys=[key for key,point in data['nodes']]
    if not opened:assert 'passage'not in keys
    if 'E19'not in flags:assert 'greenhouse'not in keys
    if 'family_room_unusable'not in flags:assert 'guestroom'not in keys
    assert 'altar'not in keys
    for key,(x,y) in data['nodes']:
     await self.input(30+x,143+y);st=await self.state();can_move=any('이곳으로 이동'in b['text']for b in st['buttons']);assert can_move==(key in allowed and key!='gate'),(name,key,can_move,allowed)
     assert st['room']==state,(name,key,'map selection changed world')
     checks.append({'scenario':name,'region':region,'node':key,'travel_enabled':can_move})
   await self.shot('map-lock-'+name);await self.press('현장으로 돌아가기');await self.wait('r13_hub');assert (await self.state())['room']==state
  await self.py('import renpy;renpy.store.room13='+ascii(original)+';renpy.exports.restart_interaction();result=True')
  return {'kind':'injected-map-access-states-real-pin-selection-not-travel','checks':checks}

 async def bed_boundary_fixtures(self):
  base=(await self.state())['room'];n=json.loads(json.dumps(base));n.update(day=4,period=3,location='inn',case_state='occurred',victim_state='dead',daram_state='held',flags=['lodging','family_room_unusable'],done=[])
  await self.py('import renpy;s=renpy.store;s.room13='+ascii(n)+';renpy.exports.restart_interaction();result=True');await self.wait('r13_hub');await self.travel('13호실','여관 안');await self.value(('object','bed'));await self.advance();await self.wait('r13_hub');assert 'r13_object_context'not in (await self.state())['screens'];assert (await self.state())['room']['day']==4
  await self.travel('임시 객실','여관 안');await self.shot('bed-displaced-clean-guestroom');await self.value(('object','bed'));await self.advance();await self.wait('r13_object_context');before=(await self.state())['room'];await self.press('침대에서 잠자기');await self.wait('r13_confirm');await self.press('아직 할 일이');await self.advance();await self.wait('r13_hub');assert (await self.state())['room']==before
  await self.value(('object','bed'));await self.advance();await self.wait('r13_object_context');await self.press('침대에서 잠자기');await self.wait('r13_confirm');await self.press('잠자리에 든다');await self.advance();await self.wait('r13_hub');after=(await self.state())['room'];assert after['day']==5 and after['period']==0 and after['daram_state']=='held' and after['case_state']=='occurred',after;assert after['evidence']==before['evidence'];await self.shot('bed-displaced-next-morning')
  n=json.loads(json.dumps(base));n.update(day=4,period=0,location='inn',case_state='pending',victim_state='alive',daram_state='with_dad',flags=['lodging'],done=[])
  await self.py('import renpy;renpy.store.room13='+ascii(n)+';renpy.exports.restart_interaction();result=True');await self.wait('r13_hub');await self.travel('13호실','여관 안');await self.value(('object','bed'));await self.advance();await self.wait('r13_object_context');await self.press('침대에서 잠자기');await self.wait('r13_confirm');await self.press('잠자리에 든다');await self.advance();await self.wait('choice');st=await self.state();assert st['room']['day']==4 and st['room']['period']==2 and st['room']['case_state']=='pending';assert any('반송품은 미루고'in b['text']for b in st['buttons']);await self.shot('bed-day4-case-not-skipped')
  return {'kind':'injected-boundary-states-with-real-map-bed-confirmation-inputs','checks':['Crime-scene bed cannot sleep after displacement','Temporary guestroom reached on map, bed cancel preserves state','Temporary bed advances to day5 without releasing held Daram or changing evidence','Day4 early sleep reaches case choice instead of skipping to day5']}

 async def forced_choice_migration(self):
  check=await self.py("""import renpy,copy
s=renpy.store
before=copy.deepcopy(s.room13);speaker=s.dialogue_speaker
bounds=renpy.exports.get_image_bounds('r13_visitor')
assert bounds is not None
s.room13['visual_revision']='pixel-b-acting-v2'
s.r13_upgrade()
renpy.exports.restart_interaction()
after=copy.deepcopy(s.room13)
for key in ('visual_revision','checks','last_inspection'):before.pop(key,None);after.pop(key,None)
assert before==after,('story state changed',before,after)
assert s.dialogue_speaker==speaker,('speaker changed',speaker,s.dialogue_speaker)
result={'kind':'injected-old-visual-revision-on-natural-proof-choice','story_state_preserved':before==after,'speaker_preserved':s.dialogue_speaker==speaker,'revision':s.room13['visual_revision'],'bounds_before':bounds}
""")
  await self.wait('choice');check['bounds_after']=await self.py("import renpy;result=renpy.exports.get_image_bounds('r13_visitor')");assert check['bounds_before']==check['bounds_after'],check;assert check['revision']=='pixel-b-front-v3';await self.shot('choice-forced-old-revision-restored');self.events.append(check)

 async def choice_save_restore(self):
  before=(await self.state())['room'];bounds=await self.py("import renpy;result=renpy.exports.get_image_bounds('r13_visitor')")
  await self.press('설정');await self.wait('pause_menu');await self.press('저장');await self.wait('save');await self.press('1쪽 2번');await asyncio.sleep(.5);await self.press('돌아가기');st=await self.state()
  if 'pause_menu'in st['screens']:await self.press('돌아가기')
  await self.wait('choice');await self.press('설정');await self.wait('pause_menu');await self.press('불러오기');await self.wait('load');await self.press('1쪽 2번');await self.press('예');await self.wait('choice');assert (await self.state())['room']==before
  restored=await self.py("import renpy;result=renpy.exports.get_image_bounds('r13_visitor')");assert restored==bounds,('choice portrait bounds changed after load',bounds,restored);await self.shot('choice-real-save-load-restored');self.events.append('Actual proof-choice save/load preserves state and left-portrait bounds')

# ---- from pixel_qa_gate0153.py
class GateQA(FlowQA):
 async def state(self):
  probe=FLOW_PROBE.replace('names=[',"names=['r13_gate_document_inspection','r13_records',")
  st=await self.py('ns={};exec('+ascii(probe)+',ns);result=ns["result"]')
  assert '_exception' not in st['screens'],st
  return st
 async def population(self):
  return await self.py("import renpy;s=renpy.store;sc=renpy.display.screen.get_screen('r13_hub');result={'entry':sc.scope['entry'],'scheduled':s.r13_people(),'actors':s.r13_stage_people(sc.scope['entry']),'clock':[s.room13['day'],s.room13['period']]}")
 async def portrait(self):
  return await self.py("import renpy;s=renpy.store;w=renpy.exports.get_widget('say','what');result={'speaker':s.dialogue_speaker,'thought':s.r13_thought_active,'portrait':renpy.exports.get_widget('say','r13_dialogue_portrait') is not None,'frame':renpy.exports.get_widget('say','dialogue_portrait_frame') is not None,'text':w.text if w else None}")

# ---- from pixel_qa_review0155.py
class ReviewQA(GateQA):
 async def room(self):return (await self.state())['room']
 async def save(self,slot):
  await self.press('옵션');await self.wait('pause_menu');await self.press('저장');await self.wait('save');await self.press('1쪽 '+str(slot)+'번');await self.press('돌아가기')
  if 'pause_menu'in(await self.state())['screens']:await self.press('돌아가기')
  await self.wait('r13_hub')
 async def load(self,slot):
  await self.press('옵션');await self.wait('pause_menu');await self.press('불러오기');await self.wait('load');await self.press('1쪽 '+str(slot)+'번');await self.press('예');await self.wait('r13_hub')
 async def docs(self):await self.input(1128,410);await self.wait('r13_gate_document_inspection')
 async def present(self,key='G1'):
  await self.press('돌목');await self.wait('r13_entry_topics');await self.press('제시');await self.wait('r13_book');label=await self.py("import renpy;result=renpy.store.R13_RECORD_SHORT["+repr(key)+"]");await self.press(label);await self.press('돌목에게 보여주기');await self.advance();await self.wait('choice')
 async def records(self):
  return await self.py("import renpy;s=renpy.store;sc=renpy.display.screen.get_screen('r13_records');result={'order':sc.scope['order'],'entries':sc.scope['entries'],'selected':sc.scope['selected_record'],'page_size':s.r13_record_page_size(),'ui':s.room13.get('record_ui',{}),'large':s.persistent.room13_large_text}")

# ---- from pixel_qa_say_records0155.py
class SayQA(ReviewQA):
 async def line(self):return await self.py("import renpy;s=renpy.store;result={'packet':s.r13_packet,'read_id':s.r13_read_id,'index':s.r13_index,'speaker':s.r13_packet[0],'portrait_speaker':s.dialogue_speaker,'entries':s.entries,'identity':s.identity,'room':s.room13}")
 async def say_save(self,slot):
  await self.press('옵션');await self.wait('pause_menu');await self.press('저장');await self.wait('save');await self.press('1쪽 '+str(slot)+'번');await self.press('돌아가기')
  if 'pause_menu'in(await self.state())['screens']:await self.press('돌아가기')
  await self.wait('say')
 async def say_load(self,slot):
  await self.press('옵션');await self.wait('pause_menu');await self.press('불러오기');await self.wait('load');await self.press('1쪽 '+str(slot)+'번');await self.press('예');await self.wait('say')
 async def favorite_during_line(self,key,slot,advance=True):
  initial=await self.line();await self.press('기록');await self.wait('r13_records');label=await self.py('import renpy;result=renpy.store.R13_RECORD_SHORT['+repr(key)+']');await self.press(label);await self.press('관심 표시');await self.press('닫기');await self.wait('say');saved=await self.line();assert {k:v for k,v in initial.items()if k!='room'}=={k:v for k,v in saved.items()if k!='room'};assert {k:v for k,v in initial['room'].items()if k!='record_ui'}=={k:v for k,v in saved['room'].items()if k!='record_ui'}
  await self.say_save(slot);after_save=await self.line();(self.out/('trace-'+str(slot)+'-after-save.json')).write_text(json.dumps(after_save,ensure_ascii=False,indent=2));assert saved==after_save,('changed while closing save UI',saved,after_save);await self.press('기록');await self.wait('r13_records');await self.press(label);await self.press('관심 해제');await self.press('닫기');await self.wait('say');assert key not in(await self.room())['record_ui']['favorites'];before_load=await self.line();(self.out/('trace-'+str(slot)+'-before-load.json')).write_text(json.dumps(before_load,ensure_ascii=False,indent=2));await self.say_load(slot);loaded=await self.line();(self.out/('trace-'+str(slot)+'-after-load.json')).write_text(json.dumps(loaded,ensure_ascii=False,indent=2));assert saved==loaded,(saved,loaded);await self.shot('say-'+initial['speaker']+'-'+str(slot)+'-restored');following=None
  if advance:
   await self.input(810,625);await self.wait('say');following=await self.line();assert following['index']==saved['index']+1,(following,saved)
  return {'before':initial,'saved':saved,'loaded':loaded,'next_line':following}

# ---- from pixel_qa_ui0156.py
class UIQA(SayQA):
 async def state(self):
  probe=FLOW_PROBE.replace('names=[',"names=['r13_resident_approach','r13_gate_document_inspection','r13_records',")
  st=await self.py('ns={};exec('+ascii(probe)+',ns);result=ns["result"]');assert '_exception'not in st['screens'],st;return st
 async def advance(self):
  for _ in range(350):
   st=await self.state()
   if 'r13_arrival_card'in st['screens']:await self.input(800,400);continue
   if 'r13_cinematic_view'in st['screens']:await self.press('계속');continue
   if any(n in st['screens']for n in ('r13_resident_approach','choice','r13_hub','r13_book','r13_confirm','r13_topics','r13_entry_topics','r13_entry_karo_topics','r13_object_context','r13_map')):await asyncio.sleep(.5);return await self.state()
   if 'say'in st['screens']:await self.input(810,610)
   else:await asyncio.sleep(.15)
  raise AssertionError(st)
 async def camera(self):return await self.py('import renpy;s=renpy.store;result={"offset":s.r13_world_offset(),"cameras":s.r13_world_cameras,"width":s.r13_world_width()}')
 async def options_cancel(self):
  before=await self.room();cam=await self.camera();await self.press('옵션');await self.wait('pause_menu');await self.press('돌아가기');assert await self.room()==before and await self.camera()==cam
