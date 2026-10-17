import copy,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
class SpatialContacts(unittest.TestCase):
 def env(self,actors,location='square',offer=False):
  state=dict(location=location,case_state='occurred',trial_result='pending')
  e=dict(store=SimpleNamespace(room13=state),r13_stage_people=lambda entry=False:actors,r13_offer_for_person=lambda who:offer,r13_home_with_daram=lambda:True,r13_world_width=lambda:1920,r13_ma_shape=lambda who,pose:.75,r13_acting_spec=lambda who,pose:dict(foot=[50,200],seat=[50,160],contact='floor_sit'),r13_actor_geometry=lambda who,pose:(100,200))
  exec(textwrap.dedent((ROOT/'game/systems/room13_spatial_contacts.rpy').read_text().split('init 179 python:\n')[1]),e)
  return e
 def test_no_new_residents_and_offer_guard(self):
  self.assertEqual(self.env([])['r13_stage_people'](),[])
  a=dict(person='resident_sling',pose='activity',depth=600,x=4)
  self.assertEqual(self.env([a],offer=True)['r13_stage_people'](),[a])
  self.assertEqual(self.env([dict(a,pose='event_pose')])['r13_stage_people'](),[dict(a,pose='event_pose')])
 def test_elevated_contact_preserves_pose_scale_and_ground_depth(self):
  a=dict(person='resident_sling',pose='activity',depth=600);original=copy.deepcopy(a)
  x=self.env([a])['r13_stage_people']()[0]
  self.assertEqual(a,original);self.assertEqual(x['depth'],520);self.assertEqual(x['elevation'],86)
  self.assertEqual(x['height'],148);self.assertLessEqual(abs(x['y']+x['height']-434),1)
 def test_rest_is_seated_with_floor_contact(self):
  x=self.env([dict(person='daram',pose='neutral',depth=600)],'room13')['r13_stage_people']()[0]
  self.assertEqual(x['pose'],'action_1');self.assertEqual(x['y']+x['height'],620)
 def test_other_furniture_and_locations_unchanged(self):
  for loc,person,pose in [('square','resident_yeoni','living_mend'),('square','resident_dalgeurak','map27_sq_1'),('clinic','resident_sling','activity')]:
   a=dict(person=person,pose=pose,depth=600);self.assertEqual(self.env([a],loc)['r13_stage_people'](),[a])
 def test_nabi_same_depth_head_size_and_support(self):
  import json
  rows=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows']
  for row in rows:
   if row['request_id'] not in ('KI-1','KI-2','KI-3','KI-4','KI-5'):continue
   v=row['variants']['morning'];s=row['spec'];target=94 if row['request_id']=='KI-2' else 120
   self.assertLess(abs(s['head'][3]*v['render_height']/s['crop'][3]-target),.4)
   self.assertEqual(v['target'],[1835,354] if row['request_id']=='KI-2' else [700,542])
 def test_seori_original_and_two_eye_metadata(self):
  import json,hashlib
  from PIL import Image
  row=json.loads((ROOT/'game/assets/room13-seori-review-art.json').read_text());s=row['spec']
  self.assertEqual(s['facing'],'front-left-threequarter')
  self.assertNotEqual(s['anchors']['eyes_left'],s['anchors']['eyes_right'])
  source=ROOT/'art/approved-seori-threequarter-v2/source-original.png'
  self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),s['source_sha256'])
  self.assertEqual(Image.open(source).size,(1037,1516))
if __name__=='__main__':unittest.main()

