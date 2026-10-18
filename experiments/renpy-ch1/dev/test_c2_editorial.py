import unittest,textwrap,copy
from pathlib import Path
import test_meeting_pressure as pressure
class C2Editorial(unittest.TestCase):
 def setUp(self):
  p=pressure.PressurePilot();p.setUp();self.e=p.e;self.s=p.s
  self.s.r13_c2_edit={};self.s.r13_c2_pair_poses={};self.e['R13_MEETING_RESUME_FIELDS']=()
  self.e['CAST'].update({who:{} for who in ('dad','resident_ppul','resident_seori','buri')})
  src=(Path(__file__).resolve().parents[1]/'game/systems/room13_c2_editorial.rpy').read_text().split('init 195 python:\n',1)[1].split('    class R13C2Editorial',1)[0]
  exec(textwrap.dedent(src),self.e)
 def line(self,identity,index,who,pose='neutral'):
  return self.e['r13_meeting_direct_line'](identity,index,(who,'test line',{'pose':pose}),'neutral',pose)
 def test_pair_survives_speaker_switch_and_keeps_authored_pressure(self):
  story=copy.deepcopy(self.s.room13)
  self.line('debate:counter:C2:s3',0,'resident_ppul')
  self.assertEqual(self.s.r13_c2_edit['cue'],'enter')
  self.line('debate:counter:C2:s3',1,'resident_ppul','angry')
  self.line('debate:counter_ok:C2:s3',0,'dad')
  self.assertEqual(self.s.r13_c2_edit['pair'],('resident_ppul','dad'))
  self.assertEqual(self.s.r13_c2_edit['cue'],'hold')
  self.assertEqual(self.s.r13_meeting_direction_poses['resident_ppul'],'angry')
  self.line('debate:counter_ok:C2:s3',0,'dad')
  self.assertEqual(self.s.r13_meeting_direction_poses['resident_ppul'],'angry')
  self.assertIn('r13_c2_edit',self.e['R13_MEETING_RESUME_FIELDS'])
  self.assertEqual(self.s.room13,story)
 def test_third_person_and_topic_change_exit(self):
  self.line('debate:counter:C2:s3',0,'resident_ppul')
  self.line('debate:counter_wrong:C2:s3:over',0,'resident_seori')
  self.assertIsNone(self.s.r13_c2_edit['pair']);self.assertEqual(self.s.r13_c2_edit['cue'],'exit')
  self.line('debate:counter:C2:s3',0,'resident_ppul')
  self.line('meeting:live:C2:s1',0,'resident_ppul')
  self.assertIsNone(self.s.r13_c2_edit['pair'])
 def test_load_keeps_pair_and_pose_but_settles_reaction(self):
  self.line('debate:counter:C2:s3',0,'resident_ppul','angry')
  before=copy.deepcopy(self.s.r13_c2_edit);poses=dict(self.s.r13_c2_pair_poses)
  self.e['r13_c2_edit_after_load']();self.assertEqual(before,self.s.r13_c2_edit);self.assertEqual(poses,self.s.r13_c2_pair_poses)
  self.line('meeting:live:C2:s1',1,'buri');self.assertEqual(self.s.r13_c2_edit['phase'],'pending')
  self.e['r13_c2_edit_after_load']();self.assertEqual(self.s.r13_c2_edit['phase'],'settled')
 def test_other_claims_clear_editorial(self):
  self.line('debate:counter:C2:s3',0,'resident_ppul');self.s.r13_meeting_claim='C3'
  self.line('meeting:live:C3:s1',0,'resident_ppul');self.assertEqual(self.s.r13_c2_edit,{})
