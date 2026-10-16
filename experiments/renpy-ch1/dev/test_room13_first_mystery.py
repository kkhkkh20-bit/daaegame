"""Real init helpers: choices, save-local effects, legacy and late-case preservation."""
import r13_timeline_env  # noqa: F401  날짜표 상수 (game/systems/room13_timeline.rpy)
import ast,copy,json,textwrap,types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=(root/'game/room13_first_mystery.rpy').read_text().split('init 76 python:\n',1)[1].split('\nscreen ',1)[0]
module=ast.parse(textwrap.dedent(source));module.body=[n for n in module.body if not isinstance(n,ast.ClassDef)]
content=json.loads((root/'game/room13-content.json').read_text())
state={'day':1,'period':1,'evidence':[],'flags':[],'done':[],'read_topics':[],'resident_knowledge':{}}
store=types.SimpleNamespace(room13=copy.deepcopy(state));calls=[]
def flag(*keys):
 n=copy.deepcopy(store.room13)
 for key in keys:
  if key not in n['flags']:n['flags'].append(key)
 store.room13=n
def finish(key):
 if key in store.room13['done']:return
 store.room13=copy.deepcopy(store.room13);store.room13['done'].append(key);store.room13['period']+=1;store.room13['evidence']+=content['activities'][key]['give']
def present(person,key,identity=False):calls.append((person,key,identity));return [('base','preserved')]
e=dict(ROOM13=content,store=store,r13_flag=flag,r13_finish_action=finish,r13_conversation_topic_lines=lambda key:content['topics'][key]['lines'],r13_present=present,r13_has=lambda k:k in store.room13['flags'] or k in store.room13['evidence'],r13_secret_route_available=lambda:True)
exec(compile(module,'first-mystery','exec'),e)
check=e['r13_plan_check']
assert not check(0,'window')[0] and not check(0,'center')[0] and check(0,'books')[0]
for a in e['R13_PLAN_ENDPOINTS']:
 for b in e['R13_PLAN_ENDPOINTS']:assert check(1,endpoints=(a,b))[0]==(set((a,b))=={'books','kitchen'})
assert not check(2,reason='insulation')[0] and check(2,reason='latch')[0]
assert e['r13_plan_pair'](('books','flue'),'kitchen')==('flue','kitchen')
assert e['r13_plan_pair'](('books','kitchen'),'books')==('kitchen',)
assert e['r13_plan_pair']((),'invalid')==()
before=copy.deepcopy(store.room13)
assert len(e['r13_first_mystery_notes']())==1 and store.room13==before
assert '13호실에는' not in str(e['r13_first_mystery_notes']())
flag('entry_corrected','inn_front_door_claim')
assert len(e['r13_first_mystery_notes']())==2
assert not e['r13_plan_has_lens']()
store.room13['inspection_items']={'inventory':['magnifier']};assert e['r13_plan_has_lens']()
e['r13_finish_action']('map');assert 'E04'in store.room13['evidence'] and store.room13['period']==2 and 'first_plan_compared'in store.room13['flags']
before=copy.deepcopy(store.room13);e['r13_finish_action']('map');assert store.room13==before
assert e['r13_present']('granny','E37')==[('base','preserved')] and store.room13==before
assert 'plan_reviewed_with_buri'not in store.room13['flags'];r=e['r13_present']('buri','E04');assert 'plan_reviewed_with_buri'in store.room13['flags'] and len(r)>1
assert not store.room13.get('passage_open',False)
store.room13['evidence'].append('E37');r=e['r13_present']('granny','E37');assert 'inn_claim_retracted'in store.room13['flags'];assert any(p[2].get('expression')=='distressed'for p in r if len(p)>2)
assert len(e['r13_present']('granny','E37'))==1
assert '세탁물' in str(e['r13_conversation_topic_lines']('mystery:door'))
assert '복도 쪽 문밖에 없어요' not in str(e['r13_conversation_topic_lines']('mystery:door'))
assert '인정했다' in str(e['r13_first_mystery_notes']())
store.room13['day']=8;before=copy.deepcopy(store.room13);assert e['r13_present']('granny','E37')==[('base','preserved')] and before==store.room13
assert len(calls)==5
# Old completed map saves retain their evidence and never pay again; no new required keys.
store.room13=copy.deepcopy(state);store.room13.update(done=['map'],evidence=['E04']);before=copy.deepcopy(store.room13);e['r13_finish_action']('map');assert before==store.room13
assert len(e['r13_first_mystery_notes']())==2
main=(root/'game/room13.rpy').read_text();segment=main.split('label r13_argument_menu:',1)[1].split('label r13_link_reason',1)[0]
assert 'call r13_debate_run(r13_claim)' in segment
debate=(root/'game/systems/room13_debate.rpy').read_text();loop=debate.split('label r13_debate_loop:',1)[1].split('label r13_debate_unanswerable',1)[0]
# Cancelling the evidence book (falsy item) skips judging and jumps back to the same claim's board.
assert 'if r13_item:' in loop and loop.rstrip().endswith('jump r13_debate_loop')
assert 'jump r13_talk_menu'not in loop and 'jump r13_person_actions'not in loop
print(json.dumps({'passed':True,'checks':['all diagram candidate pairs','reasonable wrong hypothesis rejected','read-only notes no unseen clue disclosure','tool ownership check','once-only old activity reward/time','owned evidence required; base presentation always invoked','presentation changes response without opening passage','first/repeat admission and late-case preserved','old completed save no re-payment','trial cancel returns same claim']},ensure_ascii=False,indent=2))
