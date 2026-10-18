import copy,json,unittest
from investigation_source2_overlay import ROOT,KEY,receipt,restore,run
class SourceTwo(unittest.TestCase):
 def test_hash_rgba_full_baseline(self):self.assertEqual(run(),2)
 def test_exact_specs_reject_foot_and_stature_change(self):
  doc=json.loads((ROOT/'game'/KEY).read_text())
  for o in receipt()['operations']:
   person,pose=o['pointer'].strip('/').split('/')
   for field,value in [('foot',[0,0]),('stature_ratio',2)]:
    changed=copy.deepcopy(doc);changed[person][pose][field]=value
    with self.assertRaises(AssertionError):restore({KEY:changed},require_applied=True)
 def test_child_stature_unchanged(self):
  o=receipt()['operations'][1];self.assertEqual(o['expected']['stature_ratio'],o['value']['stature_ratio'])
