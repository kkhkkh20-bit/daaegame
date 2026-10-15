"""Optional-tool loop: no evidence/time bypass, real ownership and repeat/save safety."""
import ast,copy,json,textwrap,types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
content=json.loads((root/'game/room13-content.json').read_text())
block=(root/'game/room13_tool_discovery.rpy').read_text().split('init 73 python:\n',1)[1].split('\nscreen ',1)[0]
base=dict(day=2,period=0,location='workshop',evidence=[],flags=['observed:workshop:plans'],inspection_items={'inventory':['magnifier']},read_topics=[],daram_state='with_dad',case_state='pending',done=[],arguments={},propositions=[],kitchen_switch=False,passage_open=False,records={},resident_knowledge={})
store=types.SimpleNamespace(room13=copy.deepcopy(base));base_calls=[]
def base_present(person,key,identity=False):
 base_calls.append((person,key,identity));return [('baseline','original response')]
def original_topics(person):
 return [(k,v)for k,v in content['topics'].items() if v['npc']==person and env['r13_available'](v) and (store.room13['daram_state'] in ('with_dad','rescued') or not any(p=='daram'for p,t in v['lines']))]
env=dict(winter_copy=copy,ROOM13=content,store=store,r13_topics=original_topics,r13_present=base_present,r13_conversation_topic_lines=lambda key:content['topics'][key]['lines'],r13_object_visible=lambda spec:True,renpy=types.SimpleNamespace(restart_interaction=lambda:None))
env['r13_has']=lambda key:key in store.room13['flags'] or key in store.room13['evidence']
# Use the existing availability/actions functions, not a mirrored tool implementation.
rules=(root/'game/room13_rules.rpy').read_text().split('init 55 python:\n',1)[1].split('\nlabel ',1)[0]
module=ast.parse(textwrap.dedent(rules))
for n in module.body:
 if isinstance(n,ast.FunctionDef) and n.name in ('r13_available','r13_actions'):
  exec(compile(ast.Module(body=[n],type_ignores=[]),'existing-rules','exec'),env)
env['r13_w2_actions_allowed']=lambda spec:True
exec(compile(textwrap.dedent(block),'tool-discovery','exec'),env)
# Buri's plan follow-up wraps the calendar topic lines at init 77.
late=(root/'game/room13_tool_discovery.rpy').read_text().split('init 77 python:\n',1)[1]
exec(compile(textwrap.dedent(late),'tool-discovery-late','exec'),env)
checks=[]
transition=env['r13_tool_transition'];target=env['r13_tool_target']
for patch in [{'inspection_items':{}},{'flags':[]},{'location':'room13'},{'location':'guestroom'}]:
 state=copy.deepcopy(base);state.update(patch);n,changed=transition(state,'plans');assert not changed and n==state
state=copy.deepcopy(base);state.update(location='room13',flags=['observed:room13:bed']);assert target('bed',state)is None
state['evidence']=['E03'];assert target('bed',state)=='seam'
checks.append('No tool, no direct object observation, wrong location or missing E03 cannot record')
# Plans intentionally work before E04 while the E04/map acquisition remains unchanged.
original=copy.deepcopy(base);n,changed=transition(original,'plans');assert changed and not n['evidence']
assert original==base and set(n)-set(base)=={'tool_discoveries'}
for k in base:assert n[k]==base[k],k
assert n['tool_discoveries']['plans']==dict(day=2,period=0,place='workshop',evidence_id='E04')
checks.append('Before-E04 diagram observation adds only one optional note; no evidence/time/flags/passages')
again,changed=transition(json.loads(json.dumps(n)),'plans');assert not changed and again==n
checks.append('JSON save/load and repeated use retain one note with original timestamp')
store.room13=copy.deepcopy(base);assert not any(k.startswith('tool:')for k,v in env['r13_topics']('buri'))
store.room13=n;assert 'tool:plans'in dict(env['r13_topics']('buri'))
assert 'tool:seam'not in dict(env['r13_topics']('daram'))
checks.append('Only the actually recorded observation exposes its own question')
# Real map eligibility unchanged, and its existing cost remains one time segment.
store.room13=copy.deepcopy(base);before_actions=[k for k,v in env['r13_actions']()]
store.room13=n;after_actions=[k for k,v in env['r13_actions']()];assert before_actions==after_actions and 'map'in after_actions
assert content['activities']['map'].get('cost',1)==1 and content['activities']['map']['give']==['E04']
assert any('밖에서 창과 창 사이' in text for who,text in env['r13_conversation_topic_lines']('tool:plans'))
for day,period in [(content['activities']['map']['day'][0]-1,0),(2,3),(content['activities']['map']['day'][1]+1,0)]:
 store.room13=copy.deepcopy(n);store.room13.update(day=day,period=period)
 assert not any('밖에서 창 사이'in text for who,text in env['r13_conversation_topic_lines']('tool:plans'))
 assert not store.room13['evidence']
checks.append('Comparison hint follows existing map day/time availability; cost/grant remain only on map')
# Presenting still invokes the entire original pipeline exactly once.
store.room13=copy.deepcopy(n);snapshot=copy.deepcopy(store.room13)
assert env['r13_present']('buri','E04')==[('baseline','original response')]
assert base_calls[-1]==('buri','E04',False) and store.room13==snapshot
store.room13['evidence']=['E04'];assert env['r13_present']('buri','E04')==[('baseline','original response')]
store.room13['read_topics']=['tool:plans'];before=len(base_calls);reply=env['r13_present']('buri','E04');assert len(base_calls)==before+1 and reply!=[('baseline','original response')]
assert env['r13_present']('granny','E04')==[('baseline','original response')]
store.room13['day']=8;assert env['r13_present']('buri','E04')==[('baseline','original response')]
checks.append('Presentation retains original pipeline and requires owned record plus completed optional question')
store.room13=state;store.room13,_=transition(store.room13,'bed');assert 'tool:seam'in dict(env['r13_topics']('daram'))
store.room13['daram_state']='held';assert 'tool:seam'not in dict(env['r13_topics']('daram'))
checks.append('Daram follow-up remains unavailable while child is held')
store.room13=copy.deepcopy(base);before=copy.deepcopy(store.room13);assert env['r13_tool_notes']()==[] and store.room13==before
store.room13=n;notes=env['r13_tool_notes']();assert len(notes)==1 and notes[0]['evidence_id']=='E04' and not store.room13['evidence']
assert all(not content['topics'][k]['give'] and not content['topics'][k]['flags'] for k in ('tool:plans','tool:seam'))
checks.append('Legacy save view is read-only; notes associate with E04 without falsely granting it')
store.room13=copy.deepcopy(base);assert env['r13_tool_record']('plans') is True
first=copy.deepcopy(store.room13);assert env['r13_tool_record']('plans') is False and store.room13==first
source=(root/'game/room13_tool_discovery.rpy').read_text()
assert 'action Function(r13_tool_record' not in source
assert 'action Return("record")' in source and '$ r13_tool_recorded=r13_tool_record(key)' in source
assert 'if r13_tool_recorded:\n                $ source_fx("found")' in source
checks.append('Commit occurs after screen Return; first-save signal true once and repeat false')

child=copy.deepcopy(state);child['tool_discoveries']={'seam':{'day':2,'period':0,'place':'room13','evidence_id':'E03'}}
for status,expected in [('with_dad',True),('rescued',True),('held',False),('hospital',False),('missing',False)]:
 child['daram_state']=status;assert env['r13_tool_can_ask_child']('bed',child)==expected
child['daram_state']='with_dad';child['tool_discoveries']={};assert not env['r13_tool_can_ask_child']('bed',child)
checks.append('Seam popup directly reaches child conversation only when companion is present and note exists')
print(json.dumps({'pass':True,'checks':checks},ensure_ascii=False,indent=2))
