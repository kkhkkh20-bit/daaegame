"""Native authored-opening routes plus the captured chapter investigation/debate."""
import argparse
import asyncio
import json
import shutil
from pathlib import Path
from playwright.async_api import async_playwright
from qa_web import Trial, AUDIO_PROBE

ROOT=Path(__file__).resolve().parent
EP=json.loads((ROOT/'game/chapter-source.json').read_text())['episode']
ARRIVAL=json.loads((ROOT/'game/village-story.json').read_text())
TIMELINE=json.loads((ROOT/'game/village-state.json').read_text())

class SourceTrial(Trial):
 async def state(self):
  result=await self.page.evaluate('renpy_exec("import renpy; result=dict(renpy.store.trial_state(), **renpy.store.source_state())")')
  if result.get('exception'):
   await self.shot('exception');raise AssertionError('Native RenPy exception; see exception.png')
  return result
 async def advance_until(self,key,value=True,limit=1200):
  for _ in range(limit):
   st=await self.state()
   if st.get(key)==value:
    await self.page.wait_for_timeout(550);return st
   if self.errors:raise AssertionError(self.errors)
   if _ % 150 == 149:print('ADVANCE',self.width,key,st.get('line'),st.get('text'),flush=True)
   if st['inspect']:await self.click(225,535)
   else:await self.click(830,665)
  await self.shot('failure');raise AssertionError((key,value,{k:v for k,v in (await self.state()).items() if k not in ('lines','effects')}))
 async def move(self,key):
  await self.click(842,635);await self.wait('map')
  pos={'plaza':(335,578),'front':(405,303),'kitchen':(590,460),'hall':(738,135),'dotoroom':(982,91),'bed13':(977,316),'dining':(152,380)}
  x,y=pos[key];await self.click(x+112,y+45);await self.wait('roam');assert (await self.state())['location']==key
 async def interact(self,x,y):
  await self.wait('roam')
  await self.click(x,y);await self.wait('roam',False);await self.advance_until('roam')
 async def question(self,key,second=False):
  person=next(k for k,v in EP['TALK'].items() if any(q['id']==key for q in v))
  st=await self.state();point=next(p for p in st['residents'] if p['id']==person)
  await self.click(point['x']+95,point['y']+140);await self.wait('questions')
  st=await self.state();index=st['available_topics'].index(key)
  await self.click(640,169+index*63);await self.wait('questions',False)
  if key=='T_se4':
   await self.advance_until('roam');return
  await self.advance_until('questions')
  st=await self.state();await self.click(640,169+len(st['available_topics'])*63);await self.wait('roam')
 async def arrival_move(self,key):
  await self.wait('village_map')
  pos={'gate':(155,435),'fountain':(430,295),'lane':(680,455),'post':(740,215),'inn':(990,330)}
  x,y=pos[key];await self.click(x+10,y-20);await self.wait('village_map',False)
  if key=='post':
   await self.page.wait_for_timeout(550);await self.shot('post-exterior')
  else:
   assert (await self.state())['background']=='outdoor-'+key
  await self.advance_until('village_map' if key=='post' else 'village_place')
  if key!='post':await self.shot('outdoor-'+key)
 async def arrival_topic(self,key):
  await self.wait('village_questions')
  st=await self.state();person='granny' if st['village_inn'] else st['village_location']
  # The resident chooser overlays the inn screen only during an interview.
  if key in ('room','inn_town'):person='granny'
  qs=ARRIVAL['questions'][person];index=next(i for i,q in enumerate(qs) if q['id']==key)
  before=len(st['lines']);await self.click(640,169+index*63);await self.wait('village_questions',False)
  if key=='room' and st['post_closed']:
   await self.advance_until('roam');return
  await self.page.wait_for_timeout(550);await self.shot('speaking-'+key)
  if person in ('gate','fountain','lane'):
   assert (await self.state())['background']=='outdoor-'+person,'Interview changed outdoor location'
  await self.advance_until('village_questions')
  st=await self.state();assert len(st['lines'])>before
  assert key in st['village_seen']
  await self.shot('topic-'+key)
 async def arrival_action(self,action):
  await self.wait('village_place');st=await self.state()
  if action=='map':await self.click(730,642);await self.wait('village_map');return
  if action=='stay':
   before=len(st['lines']);await self.click(960,638);await self.wait('village_inn')
   assert len((await self.state())['lines'])==before,'Inn greeted before grandmother was clicked'
   await self.shot('inn-before-talk');await self.click(680,360);await self.wait('village_questions')
   await self.arrival_topic('room')
   if not st['post_closed']:
    await self.click(640,295);await self.wait('village_inn');await self.click(965,640);await self.wait('village_map')
   return
  if action=='stone':
   await self.click(430,350);await self.wait('village_place',False);await self.advance_until('village_place');return
  before=len(st['lines']);await self.click(825,210 if st['village_location']=='lane' else 365);await self.wait('village_questions')
  assert len((await self.state())['lines'])==before,'Resident spoke before a topic was chosen'
  await self.shot('questions-'+st['village_location'])
  key='seryeon' if st['village_location']=='inn' else st['village_location']
  await self.arrival_topic(key)
  qs=ARRIVAL['questions'][st['village_location']]
  await self.click(640,169+len(qs)*63);await self.wait('village_place')
 async def arrival_route(self,rich=False):
  await self.advance_until('village_place');st=await self.state()
  assert st['village_location']=='gate' and not st['village_map'] and not st['met']
  assert st['music']=='assets/town-bright.mp3' and st['pulse'] is None and not st['cold']
  assert any(p['id'].startswith('COLD_') and p['t']=='……죽었어?' for p in st['lines'])
  await self.shot('gate-first-control');await self.arrival_action('map');await self.shot('village-map')
  st=await self.state();assert not st['inventory'] and not st['post_closed']
  carriage=[p['t'] for p in st['lines'] if p['id'].startswith('V_CARRIAGE')]
  assert carriage and not any('엄마' in p or '편지' in p or '탐정' in p for p in carriage)
  checks=['criminal_cold_hook_restored_without_face','cold_heartbeat_stops_before_carriage','immediate_control_at_gate','friendly_carriage_without_mother_exposition','bright_new_town_theme','map_before_case_no_evidence']
  if rich:
   await self.arrival_move('inn');await self.arrival_action('stay');assert not (await self.state())['post_closed'];checks.append('click_grandmother_and_room_topic_before_checkin')
   for key in ('gate','fountain','lane','inn'):
    await self.arrival_move(key)
    if key!='inn':assert (await self.state())['camera']=='stage'
    await self.arrival_action('talk')
    if key=='fountain':await self.arrival_action('stone');await self.shot('stone')
    await self.arrival_action('map')
   await self.save();saved=(await self.state())['met'];saved_state=await self.state();await self.load();await self.wait('village_map');assert (await self.state())['minutes']==saved_state['minutes'] and (await self.state())['trust']==saved_state['trust'];assert (await self.state())['met']==saved and (await self.state())['stone'];checks.append('optional_encounters_and_stone_saved')
   prior=await self.state();await self.arrival_move('lane');await self.arrival_action('talk');await self.arrival_action('map');assert (await self.state())['trust']==prior['trust'];assert (await self.state())['met'].count('geokkuri')==1;checks.append('revisit_without_duplicate_first_meeting')
  await self.arrival_move('post');st=await self.state();assert st['post_closed'];await self.shot('post-closed-map')
  await self.arrival_move('inn');await self.arrival_action('stay');st=await self.state();assert st['stage']=='investigation' and not st['pulse']
  if not rich:assert not st['met'] and not st['stone'];checks.append('case_reachable_with_no_optional_resident_or_stone')
  else:
   assert '어제 문 앞에서 봤죠? 제 돈이 없어졌습니다.' in [p['t'] for p in st['lines']];checks.append('case_recognizes_previous_meeting')
  return checks+['question_menu_before_optional_dialogue','inn_no_auto_greeting','closed_post_office_then_sleep_then_case']
 async def evidence(self,key,duel=False):
  await self.click(227,485);await self.wait('evidence')
  index=(await self.state())['inventory'].index(key)
  for _ in range(index//6):await self.click(286,576)
  slot=index%6;await self.click(199+(slot%2)*230,240+(slot//2)*110);await self.wait('evidence',False)
 async def proof(self,phase,row,keys):
  st=await self.advance_until('debate');assert st['phase']==phase,(phase,st)
  await self.click(350,220+row*87);await self.wait('debate');assert (await self.state())['statement']==row
  for key in keys:
   await self.evidence(key)
   if key==keys[-1]:break
   await self.advance_until('debate')

async def run(browser,out,w,h,discovery_only=False):
 c=await browser.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000);await c.add_init_script(AUDIO_PROBE);pg=await c.new_page();t=SourceTrial(pg,w,h,out)
 await pg.goto('http://127.0.0.1:8093/preview/renpy-ch1-test/');await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.shot('title');await t.click(320,425)
 checks=await t.arrival_route(rich=w>=1000);st=await t.state();await t.shot('investigation')
 await t.interact(225,430);assert 'bed13:side-box' in (await t.state())['checks'];await t.interact(450,230);assert 'bed13:window' in (await t.state())['checks'];await t.shot('checked-room');checks.append('ordinary_object_replies_and_persistent_checks')
 assert {'steps','doorOpen','door','bell10','slam'}<=set(st['effects']);assert not {'roll','carStop','carDepart'}&set(st['effects']);checks.append('opening_effects_without_horses_or_pulse_leak');print('OPENING',w,flush=True)
 await t.interact(850,515);assert not (await t.state())['found'];checks.append('original_late_discovery_gate')
 await t.move('dining');await t.click(785,385);await t.wait('questions');st=await t.state();assert 'T_ma6' not in st['available_topics'];await t.click(640,169+len(st['available_topics'])*63);await t.wait('roam');await t.move('bed13');checks.append('somsom_topic_hidden_before_discovery')
 await t.interact(900,280);await t.interact(610,365);await t.move('kitchen');await t.question('C03');await t.move('front');await t.interact(340,495);await t.move('dining');await t.question('T_se2',True);assert 'T_se4' not in (await t.state())['available_topics'];checks.append('cross_character_accusation_requires_heard_fact');await t.question('C12',True);await t.move('bed13');assert {'bed13:side-box','bed13:window'}<=set((await t.state())['checks'])
 await t.click(850,515);await t.wait('roam',False)
 pulse_seen=False; pulse_heard=False
 for _ in range(400):
  st=await t.state()
  if st['roam']:break
  if st['pulse']:
   pulse_seen=True;assert st['music'] is None;assert st['typing'] is None
   if st['fx'] is None:pulse_heard |= any(a['rms']>1e-5 for a in await pg.evaluate('__probeAudio()'))
   if not (out/'discovery.png').exists():await t.shot('discovery')
  if st.get('camera')=='held' and not (out/'held.png').exists():
   await pg.wait_for_timeout(650)
   assert not await pg.evaluate("(code)=>renpy_exec(code)", 'import renpy; result=renpy.exports.showing("visitor")'), 'Old actor remains over CG'
   await t.shot('held')
  await t.click(830,665)
 assert pulse_seen and pulse_heard and st['found'];assert st['pulse'] is None;checks.append('discovery_silence_heartbeat_and_crowd');print('FOUND',w,flush=True)
 assert st['minutes']>=1920 and any(p['id']=='innma' for p in st['residents'])
 await t.wait('roam');await t.click(1125,385);await t.wait('questions');state=await t.state();assert 'T_ma6' in state['available_topics'];await t.click(640,169+len(state['available_topics'])*63);await t.wait('roam');checks.append('discovery_unlocks_topic_and_relocates_grandmother')
 if discovery_only:
  await t.interact(740,190);await t.click(730,450);await t.advance_until('code');await t.click(260,550);assert (await t.state())['code_error']
  for x,count in [(424,1),(568,1),(712,0),(856,2)]:
   for _ in range(count):await t.click(x,294)
  await t.click(260,550);await t.wait('code',False);await t.advance_until('roam');assert 'C11' in (await t.state())['inventory'];await t.shot('opened-room')
  await t.interact(295,530);assert 'C05' in (await t.state())['inventory']
  await t.click(1038,45);await t.wait('evidence')
  index=(await t.state())['inventory'].index('C05')
  for _ in range(index//6):await t.click(286,576)
  slot=index%6;await t.click(199+(slot%2)*230,240+(slot//2)*110);await t.shot('fur-evidence');await t.click(374,576);await t.wait('evidence',False)
  await t.move('hall');await t.interact(430,170);await t.question('C07');await t.question('C13')
  state=await t.state();texts=[p['t'] for p in state['lines']]
  expected='지금도 거꾸로 있네.' if w>=1000 else '아빠, 위에 누가 있어.'
  assert expected in texts and not any(t in texts for t in ('아빠, 어젯밤 그 언니야.','문 앞에서 둘이 놀랐지? 미안.','어젯밤엔 소리가 나서 잠깐 나갔습니다.'))
  assert {'C06','C07','C13'}<=set(state['inventory'])
  await t.move('plaza');await t.shot('morning-gate');await t.question('T_ka2')
  assert (out/'held.png').exists();assert not t.errors and not t.failed and not t.bad
  result=dict(viewport=[w,h],touch=w<1000,checks=checks+['held_cg_from_black','matching_gray_fur_evidence','bami_meeting_continuity_without_fictional_night_encounter','matching_morning_gate_and_witness_interview','wrong_code_then_opened_chest'],errors=t.errors,failed_requests=t.failed,bad_responses=t.bad,stage=st['stage'])
  await c.close();return result
 await t.interact(740,190);await t.click(730,450);await t.advance_until('code');await t.click(260,550);assert (await t.state())['code_error']
 for x,count in [(424,1),(568,1),(712,0),(856,2)]:
  for _ in range(count):await t.click(x,294)
 await t.click(260,550);await t.wait('code',False);await t.advance_until('roam');assert 'C11' in (await t.state())['inventory'];await t.interact(295,530)
 await t.save();saved=(await t.state())['inventory'];await pg.reload();await pg.wait_for_function("typeof renpy_exec==='function'",timeout=60000);await t.state();await t.click(320,500);await t.wait('loading');await t.click(760,245);await t.wait('roam');assert (await t.state())['inventory']==saved;checks.append('source_save_survives_refresh')
 await t.move('hall');await t.interact(430,170);await t.question('C07');await t.question('C13');await t.move('dotoroom');await t.interact(340,495);await t.move('plaza');await t.question('T_ka2');await t.move('dining');await t.question('T_se4');await t.move('front');assert any(p['id']=='seryeon' for p in (await t.state())['residents']);checks.append('heard_karo_fact_unlocks_question_and_changes_seryeon_location');await t.move('bed13');await t.click(964,635);await t.advance_until('debate');await t.shot('meeting');assert (await t.state())['phase']==1
 # A wrong record cannot solve the breathing question, and pressing is required.
 await t.evidence('C01');await t.wait('debate');assert (await t.state())['phase']==1
 await t.click(110,485);await t.advance_until('debate');assert (await t.state())['pressed'];await t.evidence('C04');await t.advance_until('choice');await t.shot('breathing-choice');await t.click(600,180);await t.advance_until('debate');assert (await t.state())['phase']==3;checks.append('life_check_requires_question_and_evidence')
 await t.proof(3,1,['C02','C03']);await t.advance_until('debate');assert (await t.state())['phase']==7
 await t.click(350,307);await t.wait('debate');await t.evidence('C06');await t.advance_until('debate');await t.save();await t.evidence('C07');await t.advance_until('debate');await t.load();await t.wait('debate');assert (await t.state())['step']==1;checks.append('original_comparison_save_restores');await t.evidence('C07');await t.advance_until('debate');await t.evidence('C08');await t.advance_until('debate');assert (await t.state())['phase']==8
 await t.proof(8,2,['C04','C10']);await t.advance_until('choice');await t.shot('vote');await t.click(600,272)
 await t.advance_until('choice')
 support_before=(await t.state())['trust'];support_retries=0
 while (await t.state())['support_hearing']:
  st=await t.state();people=[p for p in TIMELINE['voters'] if st['trust'].get(p,-1)<2]
  person=people[0];await t.click(600,180);await t.advance_until('evidence')
  if support_retries==0:
   # A record unrelated to this resident's worry cannot buy agreement.
   wrong=next(k for k in st['inventory'] if k not in TIMELINE['support'][person]['ids'])
   index=st['inventory'].index(wrong)
   for _ in range(index//6):await t.click(286,576)
   await t.click(199+(index%6%2)*230,240+(index%6//2)*110)
   await t.advance_until('choice');assert (await t.state())['trust']==st['trust']
   await t.click(600,180);await t.advance_until('evidence');checks.append('unrelated_proof_cannot_buy_support')
  key=next(k for k in TIMELINE['support'][person]['ids'] if k in st['inventory']);index=st['inventory'].index(key)
  for _ in range(index//6):await t.click(286,576)
  await t.click(199+(index%6%2)*230,240+(index%6//2)*110)
  for _ in range(150):
   state=await t.state()
   if state['choice'] or state['debate']:break
   await t.click(830,665)
  support_retries+=1
 await t.advance_until('debate');checks.append('four_residents_support_without_changing_case_truth');assert (await t.state())['group']=='final';await t.shot('final')
 await t.proof(0,0,['C05','C01']);await t.advance_until('debate');await t.proof(1,0,['C13','C01']);await t.advance_until('debate');await t.proof(3,0,['C10','C12','C14']);await t.advance_until('complete_screen');await t.shot('complete');st=await t.state();assert st['complete'] and st['pulse'] is None;assert not t.errors and not t.failed and not t.bad
 checks.extend(['original_four_meeting_rounds','original_three_final_rounds_and_vote','source_after_story_to_end'])
 # Every spoken line has either captured-source or authored-opening provenance.
 allowed=set()
 def collect(value):
  if isinstance(value,dict):
   if 'w'in value and 't'in value:allowed.add((value['w'],value['t']))
   for v in value.values():collect(v)
  elif isinstance(value,list):
   if len(value)>1 and isinstance(value[0],str) and isinstance(value[1],str):allowed.add((value[0],value[1]))
   else:
    for v in value:collect(v)
 collect(EP);collect(ARRIVAL);collect(TIMELINE)
 for person,line in TIMELINE["hesitant_votes"].items():
  raw="geokkuri" if person=="bami" else "wanggu" if person=="neoul" else person
  allowed.add((raw,line))
 for person,spec in TIMELINE["support"].items():
  for key in ("ask","ok","wrong"):allowed.add((person,spec[key]))
 allowed.update([('???',p['say']) for p in EP['COLD'] if p.get('say') and not p['say'].startswith('(')])
 allowed.update([('seryeon','어제 문 앞에서 봤죠? 제 돈이 없어졌습니다.'),('wanggu','신고받고 왔습니다. 주머니 모양은요?')])
 assert all((p['w'],p['t']) in allowed for p in st['lines'] if p['w']!='narr');checks.append('all_executed_spoken_lines_have_original_or_authored_provenance')
 result=dict(viewport=[w,h],touch=w<1000,checks=checks,spoken_lines=sum(p['w']!='narr' for p in st['lines']),effects=sorted(set(st['effects'])),support_hearings=support_retries,support_before=support_before,final=st,errors=t.errors,failed_requests=t.failed,bad_responses=t.bad)
 await c.close();return result

async def main(args):
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader']);runs=[]
  for w,h in ([(1280,720)] if args.desktop_only else [(844,390)] if args.mobile_only else [(1280,720),(844,390)]):
   folder=out/f'{w}x{h}';folder.mkdir(exist_ok=True);r=await run(b,folder,w,h,args.discovery_only);runs.append(r);print(json.dumps({k:v for k,v in r.items() if k!='final'},ensure_ascii=False),flush=True)
  await b.close()
 (out/'report.json').write_text(json.dumps(runs,ensure_ascii=False,indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',default='/tmp/daram-source-qa');a.add_argument('--desktop-only',action='store_true');a.add_argument('--discovery-only',action='store_true');a.add_argument('--mobile-only',action='store_true');asyncio.run(main(a.parse_args()))
