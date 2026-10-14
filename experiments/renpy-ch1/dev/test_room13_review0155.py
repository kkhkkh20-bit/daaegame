"""Acquisition order, bookmark isolation, legacy fields, and explicit comparison."""
import copy,json,textwrap,types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
content=json.loads((root/'game/room13-content.json').read_text())
state=dict(day=1,period=1,location='gate',evidence=['E01','G1','G3','G2'],flags=[],records={},encounters=[],read_topics=[],resident_knowledge={})
store=types.SimpleNamespace(room13=copy.deepcopy(state),_history_list=[])
persistent=types.SimpleNamespace(room13_knowledge=['E01','E02'],room13_large_text=False)
retains=[]
renpy=types.SimpleNamespace(loadable=lambda p:False,retain_after_load=lambda:retains.append(True),restart_interaction=lambda:None)
def edit(**kw):
 n=copy.deepcopy(store.room13);n.update(kw);store.room13=n
env=dict(ROOM13=content,store=store,persistent=persistent,config=types.SimpleNamespace(history_length=0,history_callbacks=[]),renpy=renpy,winter_copy=copy,r13_edit=edit,R13_NAMES={},R13_PLACES={})
s=(root/'game/room13_notebook.rpy').read_text().split('init 68 python:\n')[1].split('\ninit 71:')[0]
exec(compile(textwrap.dedent(s),'records','exec'),env)
entries=env['r13_record_entries'];assert entries(order='recent')==['G2','G3','G1','E01']
assert entries(order='acquired')==state['evidence'];assert entries(archive=True,present=True,order='recent')==['G2','G3','G1','E01']
assert not env['r13_record_favorite']('G1')
env['r13_record_toggle_favorite']('G1');assert entries(order='recent',favorite_only=True)==['G1']
assert {k:v for k,v in store.room13.items() if k!='record_ui'}==state
saved=json.loads(json.dumps(store.room13));env['r13_record_toggle_favorite']('G1');assert not env['r13_record_favorite']('G1')
store.room13=saved;assert env['r13_record_favorite']('G1')
before=copy.deepcopy(store.room13);assert not env['r13_record_update_ui']('favorites','unknown',True);assert store.room13==before
assert env['r13_record_unread']('G1');env['r13_record_update_ui']('seen','G1',True);assert not env['r13_record_unread']('G1')
persistent.room13_large_text=True;assert env['r13_record_page_size']()==8;assert env['r13_record_pages'](list(range(34)))==5;assert env['r13_record_selected'](list(range(34)),0,1)==8
persistent.room13_large_text=False;assert env['r13_record_pages'](list(range(34)))==3
# Execute actual gate helpers with grants/marks isolated, not reconstructed logic.
store.room13=copy.deepcopy(state);store.room13['evidence']=[]
def flag(*keys):
 for key in keys:
  if key not in store.room13['flags']:store.room13['flags'].append(key)
def grant(keys,source):
 for key in keys:
  if key not in store.room13['evidence']:store.room13['evidence'].append(key)
env.update(R13_WORLD_LAYOUTS={},R13_OBJECT_NAMES={},r13_flag=flag,r13_grant=grant,r13_mark=lambda *a:None)
s=(root/'game/room13_gate_inspection.rpy').read_text().split('init 63 python:\n')[1].split('\ninit 67 python:')[0]
exec(compile(textwrap.dedent(s),'gate','exec'),env)
env['r13_gate_record_document']('G1');env['r13_gate_record_document']('G3')
assert 'gate_documents_compared' not in store.room13['flags']
env['r13_gate_record_comparison']();assert 'gate_documents_compared' in store.room13['flags']
assert store.room13['evidence']==['G1','G3'] and store.room13['period']==1
before=copy.deepcopy(store.room13);env['r13_gate_record_comparison']();assert store.room13==before
print(json.dumps({'passed':True,'checks':['same-period chronological/recent order','current evidence only in presentation','favorite and seen change UI state only','unknown record rejected','legacy missing UI fields safe','8/12 pagination','separate documents do not imply comparison','explicit comparison grants once without time cost'],'retain_callbacks':len(retains)},indent=2))
