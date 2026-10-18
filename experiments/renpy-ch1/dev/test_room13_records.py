"""Actual record categories, safe presentation filtering, and old-save/history behavior."""
import copy,json,textwrap,types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
content=json.loads((root/'game/room13-content.json').read_text())
source=(root/'game/room13_notebook.rpy').read_text().split('init 68 python:\n',1)[1].split('\ninit 71:',1)[0].split('\nscreen ',1)[0]
s=types.SimpleNamespace(room13={'evidence':[]},_history_list=[],room13_mode=True,r13_thought_active=False)
persistent=types.SimpleNamespace(room13_knowledge=[])
config=types.SimpleNamespace(history_length=None,history_callbacks=[])
names={v['npc']:v['npc'] for v in content['topics'].values()}
env=dict(ROOM13=content,store=s,persistent=persistent,config=config,R13_NAMES=names,R13_PLACES={'inn':('여관',)},renpy=types.SimpleNamespace(filter_text_tags=lambda t,allow:t,loadable=lambda p:False))
env["r13_touch_ui"]=lambda:False
exec(compile(textwrap.dedent(source),'records-init','exec'),env)
assert len(content['evidence'])==40
assert {k for k in content['evidence'] if env['r13_record_category'](k)=='testimony'}=={'E06','E10','E11','E12','E15','E34'}
assert config.history_length==250 and len(config.history_callbacks)==1
s.room13={'evidence':['E01','E06','E06','unknown','E10'],'encounters':[],'read_topics':[],'resident_knowledge':{}}
persistent.room13_knowledge=['E01','E02','E12']
assert env['r13_record_entries']('testimony')==['E06','E10']
# A saved favorite-only filter must not hide records after the feature is removed.
assert env['r13_record_entries']('testimony',favorite_only=True)==['E06','E10']
assert env['r13_record_entries']('evidence')==['E01']
assert env['r13_record_entries']('testimony',True)==['E12']
assert env['r13_record_entries']('testimony',True,True)==['E06','E10']
assert env['r13_record_entries']('evidence',True,True)==['E01']
entries=list(range(34));assert env['r13_record_pages'](entries)==3
assert env['r13_record_page'](entries,100)==2
assert env['r13_record_selected'](entries,1,1)==12
assert env['r13_record_selected'](entries,33,2)==33
assert env['r13_record_selected']([],None,3) is None
# Legacy recovery uses only this save's actual topics/presentations; no invented time/place.
topic=next(iter(content['topics']));person=content['topics'][topic]['npc']
s.room13.update(read_topics=[topic],resident_knowledge={person:['E01:anonymous']})
before=copy.deepcopy(s.room13);assert env['r13_met_people']()==[person];assert s.room13==before
s.room13.update(day=2,location='inn');s.r13_thought_active=True
entry=types.SimpleNamespace(who='아빠',what='내가 실제로 한 생각.')
env['r13_history_stamp'](entry);s._history_list=[entry,types.SimpleNamespace(who='까로',what='실제 발언.'),types.SimpleNamespace(who=None,what='실제 서술.')]
rows=env['r13_history_rows']();assert [r['kind'] for r in rows]==['서술','발언','독백'];assert rows[-1]['stamp']=='2일 · 여관'
assert [r['what'] for r in rows]==['실제 서술.','실제 발언.','내가 실제로 한 생각.']
assert 'does_not_establish' not in (root/'game/room13_notebook.rpy').read_text()
print(json.dumps({'pass':True,'evidence':34,'testimony':6,'page_size':12,'checks':['explicit categories','acquired only and no duplicates','archive never submitted','34 entries pagination','old save factual people recovery without mutations','real history and thought distinction','limitation copy removed only from UI']},ensure_ascii=False,indent=2))
