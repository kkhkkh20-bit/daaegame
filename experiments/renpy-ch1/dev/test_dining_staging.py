import json,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class DiningStaging(unittest.TestCase):
 def test_six_residents_get_distinct_floor_slots(self):
  layout=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())['dining']
  source=(ROOT/'game/room13_acting.rpy').read_text();body=source.split('    def r13_stage_people(entry=False):',1)[1].split('\n    def ',1)[0]
  spec=dict(crop=[0,0,200,400],foot=[100,400],head=[50,0,100,100],contact='standing')
  names=['nabi','resident_owlgp','resident_tok','resident_mulgyeol','resident_dalgeurak','resident_hyeoni']
  env=dict(store=types.SimpleNamespace(room13=dict(day=2,period=2,location='dining',flags=[])),r13_layout=lambda location:layout,r13_visible_people=lambda:names,r13_living_pose=lambda *a:'neutral',r13_acting_spec=lambda *a:spec,r13_actor_geometry=lambda *a:(200,400),r13_world_display_height=lambda p,pose,h,l:h,r13_activity_text=lambda p:'',R13_STAGE_CACHE={},R13_STAGE_FLOORS={},R13_STAGE_POSITIONS={},R13_STAGE_COUNTERS={},R13_CROWD_SLOTS={},R13_STAGE_CRITICAL={},R13_CALENDAR={},r13_field_ui_rects=lambda offset:[],r13_control_height=lambda:64)
  helper=source[source.index('    def r13_staged_activity('):].split('\n    def ',1)[0]
  exec(textwrap.dedent(helper),env)
  exec('def r13_stage_people(entry=False):'+'\n'+textwrap.indent(textwrap.dedent(body),'    '),env)
  actors=env['r13_stage_people']();self.assertEqual(len(actors),6);self.assertEqual(len({a['slot'] for a in actors}),6)
  self.assertEqual(len({(a['x'],a['y']) for a in actors}),6)
  self.assertEqual(next(a for a in actors if a['person']=='nabi')['pose'],'action_2')
  self.assertEqual(set(a['person'] for a in actors),set(names))
 def test_existing_action_selection_is_state_specific(self):
  source=(ROOT/'game/room13_acting.rpy').read_text();body=source.split('    def r13_living_pose(person,location,period):',1)[1].split('    def r13_visible_people',1)[0];flags=set()
  poses={'doto':{'neutral':{},'action_1':{},'action_2':{}},'bami':{'neutral':{},'action_1':{},'action_2':{}}}
  env=dict(R13_ACTING=poses,R13_LIVING_ALLOWED={},store=types.SimpleNamespace(room13={'day':1}),r13_has=lambda f:f in flags,R13_WEEK2_DAY=11)
  exec('def r13_living_pose(person,location,period):'+'\n'+textwrap.indent(textwrap.dedent(body),'    '),env);pick=env['r13_living_pose']
  self.assertEqual(pick('doto','square',0),'action_1');self.assertEqual(pick('bami','inn',0),'action_1');flags.add('bami_protected')
  for period in range(3):self.assertEqual(pick('bami','inn',period),'action_2')
  data=json.loads((ROOT/'game/assets/room13-pixel-acting.json').read_text());self.assertEqual(data['resident_sling']['activity']['contact'],'crouching')
if __name__=='__main__':unittest.main()
