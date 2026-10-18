import copy,json,unittest,hashlib
from investigation_native_residual import ROOT,receipt,restore,run,slot
class ResidualScope(unittest.TestCase):
 def test_exact_eight_and_original_six_baseline(self):
  self.assertEqual(run(),8)
  ops=receipt()['operations'];self.assertEqual({o['value']['file'] for o in ops},{'assets/room13-action-resident_momo-living_lampnumber.webp','assets/room13-action-granny-living_keyledger.webp','assets/room13-group-buri-cooperative.webp','assets/room13-group-resident_tok-cooperative.webp','assets/map-action27/PO-2--resident_librarian.webp','assets/map-action27/VA-5--resident_guldol.webp','assets/map-action27/PO-1--resident_sling.webp','assets/room13-pixel-acting-ubak.webp'})
  self.assertEqual(hashlib.sha256(json.dumps(ops[:6],sort_keys=True,ensure_ascii=True,separators=(",",":")).encode()).hexdigest(),'76a2c035cf8c4adc4b7551313ca73c334772b24494902feceb6f29a29a2724cd')
  self.assertEqual({(o["file"],o["pointer"]) for o in ops},{('assets/room13-life-groups.json', '/groups/0/members/1/spec'), ('assets/room13-life-groups.json', '/groups/0/members/0/spec'), ('assets/room13-pixel-acting.json', '/granny/living_keyledger'), ('assets/room13-map-action27.json', '/rows/22/spec'), ('assets/room13-pixel-acting.json', '/resident_ubak/living_measure'), ('assets/room13-pixel-acting.json', '/resident_momo/living_lampnumber'), ('assets/room13-map-action27.json', '/rows/12/spec'), ('assets/room13-map-action27.json', '/rows/18/spec')})
 def test_missing_flag_rejected(self):
  r=receipt();docs={p:json.loads((ROOT/'game'/p).read_text()) for p in r['baseline_semantic_sha256']};o=r['operations'][0];n,k=slot(docs[o['file']],o['pointer']);n[k]['native_detail']=False
  with self.assertRaises(AssertionError):restore(docs,require_applied=True)
 def test_crop_or_source_change_rejected(self):
  r=receipt();docs={p:json.loads((ROOT/'game'/p).read_text()) for p in r['baseline_semantic_sha256']}
  for o in r['operations']:
   changed=copy.deepcopy(docs);n,k=slot(changed[o['file']],o['pointer']);n[k]['crop'][2]-=1
   with self.assertRaises(AssertionError):restore(changed,require_applied=True)
if __name__=='__main__':unittest.main()
