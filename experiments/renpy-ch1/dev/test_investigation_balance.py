import copy,json,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
class InvestigationBalance(unittest.TestCase):
 def env(self,actors,location='school',offered=None):
  e=dict(store=SimpleNamespace(room13={'location':location}),r13_stage_people=lambda entry=False:actors,r13_world_width=lambda:1800 if location=='school' else 1280,r13_offer_for_person=lambda who:who==offered,r13_ma_feet=lambda a:(a['x']+a['width']/2,a['y']+a['height']))
  exec(textwrap.dedent((ROOT/'game/systems/room13_investigation_balance.rpy').read_text().split('init 180 python:\n')[1]),e);return e
 def actor(self,person='resident_bori',**kw):
  return dict(dict(person=person,pose='neutral',x=200,y=300,width=200,height=240,rect=[200,300,200,240],depth=540,slot=[309,535,240,'class_back'],occlusion=[[0,400],[726,400],[726,570]],contact='standing'),**kw)
 def test_school_reserves_teacher_lane_without_resizing_or_moving_masks(self):
  a=self.actor();old=copy.deepcopy(a);b=self.env([a])['r13_stage_people']()[0]
  self.assertEqual(a,old);self.assertEqual(b['x'],366);self.assertEqual(b['height'],240);self.assertEqual(b['occlusion'],a['occlusion'])
  self.assertEqual(b['rect'][0]-a['rect'][0],166)
 def test_events_and_absent_people_are_preserved(self):
  a=self.actor();self.assertEqual(self.env([a],offered=a['person'])['r13_stage_people'](),[a]);self.assertEqual(self.env([])['r13_stage_people'](),[])
  a=self.actor(slot=[600,640,240,'counter']);self.assertEqual(self.env([a],'post',a['person'])['r13_stage_people'](),[a])
 def test_carried_foreground_follows_hands_not_world_furniture(self):
  a=self.actor('resident_nubi',pose='map27_in_1',map27_keepouts=[[(10,20),(30,40)]])
  b=self.env([a])['r13_balance_translate'](a,220)
  self.assertEqual(b['map27_keepouts'],[[(230,20),(250,40)]]);self.assertEqual(b['occlusion'],a['occlusion'])
 def test_post_separates_visitors_and_preserves_working_poses(self):
  a=self.actor('resident_momo',x=518,width=110,slot=[580,646,318,'counter']);b=self.actor('resident_ppul',x=672,width=169,slot=[757,632,332,'counter'])
  got=self.env([a,b],'post')['r13_stage_people']();self.assertEqual({a['person'] for a in got},{a['person'],b['person']})
  self.assertAlmostEqual(got[0]['x']+got[0]['width']/2,600,delta=1);self.assertAlmostEqual(got[1]['x']+got[1]['width']/2,970,delta=1)
 def test_piko_bed_has_one_scale_and_same_seat_all_periods(self):
  rows=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'];row=next(r for r in rows if r['request_id']=='CL-1')
  self.assertEqual(row['min_day'],11)
  for v in row['variants'].values():
   self.assertEqual(v['render_height'],240);self.assertEqual(v['target'],[1150,408]);self.assertEqual(v['anchor'],'seat')
 def test_daram_pose_heads_remain_consistent_at_same_depth(self):
  from test_spatial_contacts import SpatialContacts
  contacts=SpatialContacts().env([])['R13_HOME_CONTACTS'];specs=json.loads((ROOT/'game/assets/room13-pixel-acting.json').read_text())['daram']
  for loc,poses in contacts.items():
   heads={key:specs['action_1' if key=='rest' else key]['head'][3]*v[3]/specs['action_1' if key=='rest' else key]['crop'][3] for key,v in poses.items()}
   self.assertLess(max(heads[k] for k in ('rest','action_2','inspect_floor'))-min(heads[k] for k in ('rest','action_2','inspect_floor')),1)
   self.assertGreater(heads['rest'],heads['action_1'])
if __name__=='__main__':unittest.main()
