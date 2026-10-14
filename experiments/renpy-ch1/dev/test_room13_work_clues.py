import copy,textwrap,types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
store=types.SimpleNamespace(room13={'day':2,'period':0,'flags':['livelihood_open'],'evidence':[]})
content={'evidence':{},'evidence_sources':{},'topics':{'life:nabi':{'lines':[('nabi','old')],'give':[]}}}
ns=dict(store=store,ROOM13=content,R13_RECORD_SHORT={},winter_copy=copy,
 r13_compare_result=lambda x:'unrelated',r13_present=lambda *a:'base',
 r13_has=lambda k:k in store.room13['evidence'],r13_where=lambda p:'dining',r13_time_target=lambda:'오후까지')
for name in ('room13_livelihood_model.rpy','room13_work_clues.rpy'):
 source=(root/'game/systems'/name).read_text().split(' python:\n',1)[1]
 exec(textwrap.dedent(source),ns)
assert content['topics']['life:nabi']['give']==['J01']
assert content['evidence_sources']['J01']=='nabi'
assert 'J01' not in store.room13['evidence'] # init and work alone never award testimony.
s,r=ns['r13_complete_job'](store.room13,'kitchen','ask')
assert 'J01' not in s['evidence']
assert ns['r13_compare_result'](['M01','J01'])=='unrelated'
store.room13['evidence']=['M01','J01'];before=copy.deepcopy(store.room13)
assert '직접 보여' in ns['r13_compare_result'](['M01','J01'])
assert store.room13==before
assert ns['r13_present']('resident_lamplighter','J01')!='base'
assert ns['r13_present']('buri','J01')=='base'
assert ns['r13_work_available']('kitchen')
ns['r13_where']=lambda p:None
assert not ns['r13_work_available']('kitchen')
print('PASS: testimony requires conversation; owned-only comparison; presentation; absent employer')
