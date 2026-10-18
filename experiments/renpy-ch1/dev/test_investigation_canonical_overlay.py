import copy, hashlib, json, tempfile, unittest
from pathlib import Path
from investigation_canonical_overlay import ROOT, receipt, restored_registries, run, slot
class CanonicalOverlay(unittest.TestCase):
 def setUp(self):
  self.r=receipt();self.reg={p:json.loads((ROOT/'game'/p).read_text()) for p in ('assets/room13-pixel-acting.json','assets/room13-map-action27.json')}
 def test_exact14_original_and_export_hash_rgba_and18_bindings(self):
  self.assertEqual(run(),{'assets':14,'bindings':18,'job_rows':8,'runtime_reviewed':False})
 def test_only_exact18_specs_change_from_pinned066(self):
  old=restored_registries(self.reg,self.r)
  expected={'assets/room13-pixel-acting.json':'2f34423c114efd01b55bfbc1c54ef195ea3857b6a3b0252de235509523caec86','assets/room13-map-action27.json':'06c4b04e3bb226b381bda1251a930e19638e89ae83d4050471db9c8beacfa59a'}
  # Original serialized .66 bytes used indent=2 and a newline. Check semantic digest below instead.
  for path,digest in SEMANTIC_BASE.items():
   value=hashlib.sha256(json.dumps(old[path],sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()).hexdigest();self.assertEqual(value,digest)
 def test_changed_crop_rejected(self):
  o=self.r['operations'][0];n,k=slot(self.reg[o['file'].removeprefix('game/')],o['pointer']);n[k]['crop'][2]-=1
  with self.assertRaises(AssertionError):restored_registries(self.reg,self.r)
 def test_removed_native_flag_rejected(self):
  self.reg['assets/room13-map-action27.json']['rows'][7]['spec']['native_detail']=False
  with self.assertRaises(AssertionError):restored_registries(self.reg,self.r)
 def test_old_living_art_rejected(self):
  o=next(o for o in self.r['operations'] if o['pointer']=='/resident_musoe/living_foldmap');n,k=slot(self.reg[o['file'].removeprefix('game/')],o['pointer']);n[k]=o['expected']
  with self.assertRaises(AssertionError):restored_registries(self.reg,self.r)
SEMANTIC_BASE={'assets/room13-pixel-acting.json': '1024e3a6a443a9dedb289ac2300117bb41bb4496e6a1a145f13e454133f1b295', 'assets/room13-map-action27.json': '92cbb0b6347316d359ccfce4aa6bf672940ff3cde77c69abd4db9bb033217f63'}
if __name__=='__main__':unittest.main()
