import copy,json,unittest,hashlib
from investigation_native_residual import ROOT,receipt,restore,run,slot
class ResidualScope(unittest.TestCase):
 def test_exact34_and_original_eight_baseline(self):
  self.assertEqual(run(),34)
  ops=receipt()['operations']
  self.assertEqual({(o['file'],o['pointer']) for o in ops},{('assets/room13-map-action27.json', '/rows/41/spec'), ('assets/room13-pixel-acting.json', '/resident_solbang/neutral'), ('assets/room13-map-action27.json', '/rows/43/spec'), ('assets/room13-map-action27.json', '/rows/48/spec'), ('assets/room13-map-action27.json', '/rows/31/spec'), ('assets/room13-map-action27.json', '/rows/15/spec'), ('assets/room13-pixel-acting.json', '/resident_ubak/living_measure'), ('assets/room13-map-action27.json', '/rows/39/spec'), ('assets/room13-pixel-acting.json', '/resident_ttadak/living_repair'), ('assets/room13-map-action27.json', '/rows/22/spec'), ('assets/room13-pixel-acting.json', '/buri/action_1'), ('assets/room13-pixel-acting.json', '/resident_yeoni/neutral'), ('assets/room13-pixel-acting.json', '/buri/action_2'), ('assets/room13-map-action27.json', '/rows/11/spec'), ('assets/room13-map-action27.json', '/rows/0/spec'), ('assets/room13-pixel-acting.json', '/resident_momo/living_lampnumber'), ('assets/room13-map-action27.json', '/rows/35/spec'), ('assets/room13-pixel-acting.json', '/resident_siluk/neutral'), ('assets/room13-pixel-acting.json', '/resident_solbang/work_herb_bundle'), ('assets/room13-life-groups.json', '/groups/0/members/0/spec'), ('assets/room13-map-action27.json', '/rows/45/spec'), ('assets/room13-pixel-acting.json', '/nabi/action_2'), ('assets/room13-map-action27.json', '/rows/18/spec'), ('assets/room13-map-action27.json', '/rows/44/spec'), ('assets/room13-map-action27.json', '/rows/46/spec'), ('assets/room13-life-groups.json', '/groups/0/members/1/spec'), ('assets/room13-pixel-acting.json', '/resident_tok/neutral'), ('assets/room13-map-action27.json', '/rows/2/spec'), ('assets/room13-pixel-acting.json', '/granny/living_keyledger'), ('assets/room13-map-action27.json', '/rows/1/spec'), ('assets/room13-map-action27.json', '/rows/12/spec'), ('assets/room13-map-action27.json', '/rows/21/spec'), ('assets/room13-map-action27.json', '/rows/47/spec'), ('assets/room13-map-action27.json', '/rows/17/spec')})
  self.assertEqual(hashlib.sha256(json.dumps(ops[:8],sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest(),'1edd9f68910a9815b874ef59c25f153e78ed88d2ea2a5397dfd0b4966119fc22')
 def test_missing_flag_rejected(self):
  r=receipt();docs={p:json.loads((ROOT/'game'/p).read_text()) for p in r['baseline_semantic_sha256']};o=r['operations'][0];n,k=slot(docs[o['file']],o['pointer']);n[k]['native_detail']=False
  with self.assertRaises(AssertionError):restore(docs,require_applied=True)
 def test_crop_or_source_change_rejected(self):
  r=receipt();docs={p:json.loads((ROOT/'game'/p).read_text()) for p in r['baseline_semantic_sha256']}
  for o in r['operations']:
   changed=copy.deepcopy(docs);n,k=slot(changed[o['file']],o['pointer']);n[k]['crop'][2]-=1
   with self.assertRaises(AssertionError):restore(changed,require_applied=True)
if __name__=='__main__':unittest.main()
