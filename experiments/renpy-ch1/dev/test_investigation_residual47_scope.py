import copy,json,unittest
from investigation_native_residual import ROOT,receipt,restore,slot
class ExtraScope(unittest.TestCase):
 def test_source_change_rejected_all47(self):
  r=receipt();docs={f:json.loads((ROOT/'game'/f).read_text()) for f in r['baseline_semantic_sha256']}
  for op in r['operations']:
   changed=copy.deepcopy(docs);n,k=slot(changed[op['file']],op['pointer']);n[k]['file']='assets/UNAPPROVED.webp'
   with self.assertRaises(AssertionError):restore(changed,require_applied=True)
 def test_seori_init_baseline_restored_exact(self):
  f='assets/room13-seori-review-art.json';doc=json.loads((ROOT/'game'/f).read_text());op=next(o for o in receipt()['operations'] if o['file']==f)
  acting={doc['person']:{doc['pose']:copy.deepcopy(doc['spec'])}}
  self.assertEqual(acting[doc['person']][doc['pose']],op['value'])
  acting[doc['person']][doc['pose']]=copy.deepcopy(op['expected'])
  self.assertEqual(acting[doc['person']][doc['pose']],restore({f:doc},require_applied=True)[f]['spec'])
  self.assertNotIn('native_detail',acting[doc['person']][doc['pose']])
