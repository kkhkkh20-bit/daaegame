import copy,json,unittest
from investigation_native_residual import ROOT,receipt,restore,run,slot
class ResidualScope(unittest.TestCase):
 def test_exact_six_and_baseline(self):
  self.assertEqual(run(),6)
  ops=receipt()['operations'];self.assertEqual({o['value']['file'] for o in ops},{'assets/room13-action-resident_momo-living_lampnumber.webp','assets/room13-action-granny-living_keyledger.webp','assets/room13-group-buri-cooperative.webp','assets/room13-group-resident_tok-cooperative.webp','assets/map-action27/PO-2--resident_librarian.webp','assets/map-action27/VA-5--resident_guldol.webp'})
 def test_missing_flag_rejected(self):
  r=receipt();docs={p:json.loads((ROOT/'game'/p).read_text()) for p in r['baseline_semantic_sha256']};o=r['operations'][0];n,k=slot(docs[o['file']],o['pointer']);n[k]['native_detail']=False
  with self.assertRaises(AssertionError):restore(docs,require_applied=True)
 def test_crop_or_source_change_rejected(self):
  r=receipt();docs={p:json.loads((ROOT/'game'/p).read_text()) for p in r['baseline_semantic_sha256']};o=r['operations'][0];n,k=slot(docs[o['file']],o['pointer']);n[k]['crop'][2]-=1
  with self.assertRaises(AssertionError):restore(docs,require_applied=True)
if __name__=='__main__':unittest.main()
