import ast,json,textwrap,unittest
from pathlib import Path
B=Path(__file__).resolve().parents[1]
class JobPoseCandidate(unittest.TestCase):
 def setUp(self):
  self.rows=json.loads((B/'art/investigation-jobs-20261018/receipt.json').read_text())['rows']
  src=(B/'game/room13_acting.rpy').read_text();start=src.index('    def r13_staged_activity(');end=src.index('    def r13_staged_art(',start)
  self.e={'R13_CALENDAR':{'resident_musoe':1,'resident_lamplighter':1,'buri':1},'r13_calendar_activity':lambda p:'calendar','r13_activity_text':lambda p:'fallback'};exec(textwrap.dedent(src[start:end]),self.e)
  src=(B/'game/systems/room13_map_action27.rpy').read_text();start=src.index('    def r13_map27_variant(');end=src.index('    def r13_map27_geometry(',start);exec(textwrap.dedent(src[start:end]),self.e)
 def test_source_and_exact_two_rows(self):
  from investigation_job_overlay import run
  self.assertEqual(run(B),2)
 def test_only_two_neutral_labels_override_calendar(self):
  spec={'source_kind':'temporary_canonical_neutral_fallback_no_old_art','action_ko':'truthful'}
  self.assertEqual(self.e['r13_staged_activity']('resident_musoe',spec),'주변을 살핀다.');self.assertEqual(self.e['r13_staged_activity']('resident_lamplighter',spec),'truthful')
  self.assertEqual(self.e['r13_staged_activity']('buri',spec),'calendar');self.assertEqual(self.e['r13_staged_activity']('resident_musoe',{'action_ko':'other'}),'calendar')
 def test_jobs_only_select_existing_pose_in_workshop(self):
  f=self.e['r13_map27_variant']
  for r in self.rows:
   a={'person':r['person'],'pose':r['replace_poses'][0]};s={'location':'workshop','day':2,'period':0}
   self.assertIsNotNone(f(r,a,s,'morning',1800,False))
   for loc in ['square','gate','clinic','inn']:self.assertIsNone(f(r,a,dict(s,location=loc),'morning',1800,False))
   for pose in ['event_stone','event_injured','neutral','distressed']:self.assertIsNone(f(r,dict(a,pose=pose),s,'morning',1800,False))
   self.assertIsNone(f(r,a,s,'morning',1800,True))
 def test_chorong_no_evening_all_place_activation(self):
  r=self.rows[0];self.assertEqual(r['person'],'resident_lamplighter');self.assertIsNone(self.e['r13_map27_variant'](r,{'person':r['person'],'pose':'living_inspectlamp'},{'location':'workshop','day':2,'period':2},'evening',1800,False))
if __name__=='__main__':unittest.main()
