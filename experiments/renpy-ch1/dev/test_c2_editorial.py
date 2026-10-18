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
 def test_player_exchange_never_uses_pair_or_player_portrait(self):
  story=copy.deepcopy(self.s.room13)
  for identity,who in [('debate:counter:C2:s3','resident_ppul'),('debate:counter_ok:C2:s3','dad'),('debate:counter_wrong:C2:s3:weak','resident_ppul')]:
   self.line(identity,0,who)
   self.assertIsNone(self.s.r13_c2_edit['pair'])
   self.assertNotEqual(self.s.r13_c2_edit['visual'],'dad')
   self.assertNotEqual(self.s.r13_c2_edit['listener'],'dad')
  self.assertEqual(self.s.room13,story)
 def test_third_person_uses_real_resident(self):
  self.line('debate:counter_wrong:C2:s3:over',0,'resident_seori')
  self.assertEqual(self.s.r13_c2_edit['visual'],'resident_seori')
  self.assertIsNone(self.s.r13_c2_edit['pair'])
 def test_old_save_drops_player_pair_without_changing_dialogue(self):
  self.line('debate:counter_ok:C2:s3',0,'dad')
  token=self.s.r13_c2_edit['token']
  self.s.r13_c2_edit.update(pair=('resident_ppul','dad'),visual='dad',listener='dad')
  self.e['r13_c2_edit_after_load']()
  self.assertEqual(self.s.r13_c2_edit['token'],token)
  self.assertEqual(self.s.r13_c2_edit['phase'],'settled')
  self.assertIsNone(self.s.r13_c2_edit['pair'])
  self.assertNotEqual(self.s.r13_c2_edit['visual'],'dad')
 def test_other_claims_clear_editorial(self):
  self.line('debate:counter:C2:s3',0,'resident_ppul');self.s.r13_meeting_claim='C3'
  self.line('meeting:live:C3:s1',0,'resident_ppul');self.assertEqual(self.s.r13_c2_edit,{})
