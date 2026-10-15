"""Behavior tests for the optional portable-case reducer (no Ren'Py renderer)."""
import copy,json,textwrap,types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=(root/'game/room13_inspection.rpy').read_text()
block=source.split('init 66 python:\n',1)[1].split('\nscreen ',1)[0]
env={'winter_copy':copy,'json':json,'renpy':types.SimpleNamespace(loadable=lambda p:False,Displayable=object),'store':types.SimpleNamespace(room13=None),'ROOM13':{'objects':{}},'r13_object_visible':lambda spec:True,'r13_object_name':lambda key:key}
exec(compile(textwrap.dedent(block),'inspection-init','exec'),env)
transition=env['r13_inspection_transition'];state=env['r13_inspection_state']()
checks=[]
def step(view,target,item=None):
 global state
 before=copy.deepcopy(state);state,result=transition(state,view,target,item)
 assert before is not state
 assert len(state['inventory'])==len(set(state['inventory']))
 assert set(state)=={'version','inventory','taken','seen','paper_placed','rubbing','compartment_open','groove_held'}
 return result
for key in ['pencil','paper','ruler']:
 step('desk',key);assert key in state['inventory']
 step('desk',key);assert state['inventory'].count(key)==1
checks.append('unique pickups including repeated clicks')
r=step('drawer','tag','pencil');assert not state['rubbing'] and '종이' in r['message']
r=step('drawer','compartment','ruler');assert not state['compartment_open'] and 'ruler' in state['inventory']
r=step('drawer','divider','ruler');step('desk','cup');r=step('drawer','compartment');assert not state['compartment_open']
checks.append('wrong motions and a released groove do not open; nothing consumed')
before=copy.deepcopy(state['inventory']);step('desk','cup','paper');assert state['inventory']==before
checks.append('wrong item/target keeps inventory')
step('drawer','tag','paper');assert state['paper_placed'] and 'paper' not in state['inventory']
step('desk','paper');assert 'paper' not in state['inventory']
checks.append('placed paper never respawns or duplicates')
state=json.loads(json.dumps(state));step('drawer','tag','pencil');assert state['rubbing'] and 'pencil' in state['inventory']
r=step('drawer','tag','pencil');assert r['message']=='탁본은 이미 완성됐다.'
step('drawer','divider','ruler');step('drawer','compartment','ruler');assert state['compartment_open'] and 'ruler' in state['inventory']
step('drawer','compartment');assert 'magnifier' in state['inventory']
step('drawer','compartment');assert state['inventory'].count('magnifier')==1
checks.append('save-roundtrip mid-puzzle preserves completion and one reward')
r=step('desk','letters','magnifier');assert r['lens']==('desk','letters') and 'magnifier' in state['inventory']
r=step('drawer','buttons','magnifier');assert r['lens']==('drawer','buttons')
checks.append('reusable magnifier returns real render targets in both views')
finished=copy.deepcopy(state);r=step('drawer','divider','ruler');assert state==finished and r['message']=='이미 열려 있다.'
checks.append('repeat completion cannot farm anything')
for displaced,location,expected in [(False,'room13',True),(False,'guestroom',False),(True,'room13',False),(True,'guestroom',True)]:
 env['store'].room13={'location':location,'case_state':'occurred' if displaced else 'pending','inspection_items':state}
 env['r13_has']=lambda key:key=='lodging'
 assert env['r13_inspection_available']()==expected
 assert env['r13_inspection_state']()==state
checks.append('portable state follows family; active crime scene rejects new kit')
assert not any(k in state for k in ['evidence','day','period','flags','propositions','arguments'])
# Knowing the motion is enough: a fresh case opens without any rubbing (0.18.20).
env['store'].room13=None;fresh=env['r13_inspection_state']()
fresh,_=transition(fresh,'desk','ruler');fresh,_=transition(fresh,'drawer','divider','ruler');fresh,_=transition(fresh,'drawer','compartment','ruler')
assert fresh['compartment_open'] and not fresh['rubbing'] and 'ruler' in fresh['inventory']
checks.append('known motion opens without rubbing')
print(json.dumps({'pass':True,'checks':checks,'final_items':state['inventory']},ensure_ascii=False,indent=2))
