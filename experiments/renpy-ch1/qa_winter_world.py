"""Scene ownership, state persistence, knowledge gates and calendar reachability."""
import copy,json,textwrap,types
from pathlib import Path
R=Path(__file__).resolve().parent
s={'WINTER':json.loads((R/'game/winter-story.json').read_text()),'winter_copy':copy,
   'json':json,'renpy':types.SimpleNamespace(file=lambda p:open(R/'game'/p))}
code=(R/'game/winter_rules.rpy').read_text().split('    def winter_new():',1)[1]
exec('def winter_new():'+textwrap.dedent(code),s)
exec(textwrap.dedent((R/'game/winter_world.rpy').read_text().split('init 46 python:\n',1)[1].split('\nlabel winter_talk:')[0]),s)
w=s['WINTER_WORLD'];a=s['WINTER']['actions']
for rows in s['WINTER_SPOTS'].values():
 for who,x,y,width,height,pose in rows:
  assert y+height<=592,(who,'feet hidden behind footer')
owned=list(w['owners'])
for place,spec in w['places'].items():
 for k,obj in spec['objects'].items():
  x,y,width,height=obj['rect'];assert x>=0 and y>=0 and x+width<=1280 and y+height<=720
  owned+=obj['actions']
  assert all(a[key]['place']==place for key in obj['actions'])
assert set(owned)==set(a) and len(owned)==len(set(owned)),'Every paid action has exactly one physical or NPC owner'
state=s['winter_new']();before=copy.deepcopy(state)
state=s['winter_inspection_mark'](state,'desk',(640,400))
assert before==s['winter_new']() and state['period']==before['period']
assert s['winter_inspection_mark'](state,'desk',(640,400))==state
moved=s['winter_move'](state,'room');assert moved['checks']==state['checks']
assert 'mother' not in s['winter_target_options'](dict(state,location='passage'),'object','door')
assert 'witness' not in s['winter_target_options'](state,'person','resident_nubi')
assert s['winter_goal'](state).startswith('접수대')
# Existing saves without optional observation dictionaries are supported.
assert s['winter_seen'](state,'hello:guard')['seen']==['hello:guard']
for status in ('detained','dead'):
 z=dict(state,day=6,witness=status);assert not any(r[0]=='resident_nubi' for r in s['winter_people'](z))
assert any(r[0]=='resident_tori' for r in s['winter_people'](dict(state,day=2,location='square')))
assert not any(r[0]=='resident_tori' for r in s['winter_people'](dict(state,day=3,location='square')))
route=[['karo','post','granny'],['appointment','receipt','bed'],['ritual','meter','witness'],['protect','surveillance','timing'],['hidden','mother','symptoms'],['repair','fuel','escape'],['ledger','order','death']]
for day,keys in enumerate(route,1):
 for key in keys:
  where=a[key]['place']
  if key in w['owners'] and w['owners'][key]!='mom':
   where=s['winter_where'](state,w['owners'][key])
  state=s['winter_move'](state,where)
  if key in w['owners']:
   who=w['owners'][key]
   assert who=='mom' or who in [p[0] for p in s['winter_people'](state)],(day,key,who)
   assert key in s['winter_target_options'](state,'person',who)
  else:
   obj=next(k for k,v in w['places'][state['location']]['objects'].items() if key in v['actions'])
   assert key in s['winter_target_options'](state,'object',obj)
  state=s['winter_apply'](state,key)
 state=s['winter_next_day'](state)
print(json.dumps({'groups':10,'mapped_actions':len(owned),'physical_objects':sum(len(p['objects']) for p in w['places'].values()),'true_route_scene_reachable':True,'passed':True}))

# No duplicate actors anywhere in the world, across all 42 calendar slots.
for day in range(1,15):
 for period in range(4):
  for witness in ['available','safe','detained','dead']:
   z=dict(s['winter_new'](),day=day,period=period,witness=witness)
   encountered=[]
   for place in s['WINTER']['places']:
    actors=s['winter_people'](dict(z,location=place))
    encountered += [row[0] for row in actors]
    for who,x,y,width,height,pose in actors:assert y+height<=592
   assert len(encountered)==len(set(encountered)),(day,period,encountered)
   if witness in ['dead','detained']:assert 'resident_nubi' not in encountered
# Repeating a weekday does not resurrect a missed one-time appointment.
z=dict(s['winter_new'](),day=9,location='square')
assert s['winter_where'](z,'resident_tori')=='square'
assert 'appointment' not in s['winter_target_options'](z,'person','resident_tori')
# A free topic follows its speaker; a physical activity stays at its site.
z=dict(s['winter_new'](),day=4,period=1,location='post',evidence=['surveillance'])
assert s['winter_where'](z,'karo')=='post'
assert 'timing' in s['winter_target_options'](z,'person','karo')
assert 'escape' not in s['winter_target_options'](dict(z,day=5),'person','karo')
assert s['winter_morning'](dict(z,day=5,witness='detained'))[0][0]!='resident_nubi'
print('14-day schedules, event overrides, moving topics and missing appointments: passed')

# A changed second-week greeting is unread even if last week's was heard.
z=dict(s['winter_new'](),day=8,first_result='protected',seen=['hello:granny'])
assert s['winter_greeting_key'](z,'granny') not in z['seen']
assert s['winter_greeting_key'](z,'guard')=='hello:guard'
assert s['winter_greeting'](z,'granny')!=s['winter_greeting'](dict(z,first_result='restricted'),'granny')
