"""Exercise production rule functions through real ten-day routes, without Ren'Py."""
import copy, json, textwrap
from pathlib import Path
R=Path(__file__).resolve().parent
scope={'WINTER':json.loads((R/'game/winter-story.json').read_text()),'winter_copy':copy}
code=(R/'game/winter_rules.rpy').read_text().split('    def winter_new():',1)[1]
exec('def winter_new():'+textwrap.dedent(code),scope)
f=lambda k:scope[k]
s=f('winter_new')()
# An executable complete route with all action budgets and deadlines enforced.
route=[['karo','post','granny'],['appointment','receipt','bed'],['ritual','meter','witness'],['protect','surveillance','timing'],['hidden','mother','symptoms'],['repair','fuel','escape'],['ledger','order','death'],[],[]]
for day,actions in enumerate(route,1):
 assert s['day']==day
 for key in actions:
  before=copy.deepcopy(s)
  s=f('winter_apply')(s,key)
  assert key in s['done'],(day,key,s)
  assert before['ap']-s['ap']==1
  assert before['done']!=s['done']
  assert f('winter_apply')(s,key)==s,'duplicate action spends time'
 if day==3:
  c=scope['WINTER']['claims']['granny']['claims'][0]
  assert f('winter_proves')(s,c,['receipt','bed'])
 if day==6:
  # Incomplete mid-hearing does not block later investigation or final day.
  assert s['ap']==0
 if day==7:
  for c in scope['WINTER']['claims']['final']['claims']:
   assert any(f('winter_proves')(s,c,list(reversed(path))) for path in c['paths']), c['id']
   s=f('winter_mark')(s,c['id'])
 s=f('winter_next_day')(s)
assert s['day']==10 and f('winter_ending')(s)=='truth',s
assert f('winter_next_day')(s)==s
assert not f('winter_missing')(s)
# Empty route advances to a real ending; lack of clues never stalls the calendar.
bare=f('winter_new')()
for _ in range(9):bare=f('winter_next_day')(bare)
assert bare['witness']=='dead' and f('winter_ending')(bare)=='separated'
assert not f('winter_visible')(bare,'mother')
# Early disclosure changes custody, later rescue remains possible until day 7.
early=f('winter_new')();early.update(day=4,evidence=['witness'],witness='detained')
assert not f('winter_visible')(early,'protect')
early.update(day=6,evidence=['witness','order','registry'])
assert f('winter_apply')(early,'rescue')['witness']=='safe'
early.update(day=8,witness='dead');assert not f('winter_visible')(early,'rescue')
# Knowledge and current-run evidence are required, independently of prior endings.
fresh=f('winter_new')()
assert not f('winter_visible')(fresh,'repair')
assert not f('winter_visible')(fresh,'mother')
assert not f('winter_proves')(fresh,scope['WINTER']['claims']['final']['claims'][0],['ledger','order'])
assert f('winter_move')(fresh,'passage')['location']=='inn'
# Day-two encounter is missable, but the day-five alternate map is possible.
two=f('winter_new')();two['day']=2;assert f('winter_visible')(two,'appointment')
two['day']=3;assert not f('winter_visible')(two,'appointment')
two['day']=5;assert f('winter_visible')(two,'map')
# No invisible debt or action spending through free movement/inspection.
zero=f('winter_new')();zero['ap']=0;assert f('winter_apply')(zero,'granny')==zero
assert f('winter_move')(zero,'post')['ap']==0
# A traced mother is not secure until an actual relocation is completed.
x=f('winter_new')();x.update(day=5,evidence=['map','sightings'],facts=['passage_known'])
x=f('winter_apply')(x,'mother');assert 'mother_traced' in x['facts'] and 'mother_secure' not in x['facts']
x['evidence'].append('timing');x=f('winter_apply')(x,'relocate');assert 'mother_secure' in x['facts']
# Partial preparation cannot manufacture true ending.
for field,value in [('witness','dead'),('mother_day',8)]:
 altered=copy.deepcopy(s);altered[field]=value;assert f('winter_ending')(altered)!='truth'
for missing in ['repair','fuel','escape']:
 altered=copy.deepcopy(s);altered['evidence'].remove(missing);assert f('winter_ending')(altered)!='truth'
# Data references, speaking actors, evidence and dependency keys exist.
keys=set(scope['WINTER']['actions'])|set(scope['WINTER']['evidence'])|{'passage_known','mother','mother_secure'}
for key,a in scope['WINTER']['actions'].items():
 assert a['place'] in scope['WINTER']['places']
 assert all(v in keys for v in a['need']),(key,a['need'])
 assert all(v in scope['WINTER']['evidence'] for v in a['give'])
 assert a['start']<=a['end']<=9
print(json.dumps({'checks':20,'route':route,'result':'passed','true_ending_day':s['day']},ensure_ascii=False))
