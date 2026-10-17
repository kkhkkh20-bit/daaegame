"""Approved neutral retains source detail; unapproved expressions cannot leak in."""
import json, unittest
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class KkwakRefined(unittest.TestCase):
 def test_source_and_runtime_visible_pixels_equal(self):
  src=np.asarray(Image.open(ROOT/'art/incoming/kkwak-refined-20261017/kwaeksun-refined-candidate-v1.png').convert('RGBA'))
  dst=np.asarray(Image.open(ROOT/'game/assets/room13-role-resident_kkwak-refined-v1.webp').convert('RGBA'))
  self.assertEqual(src.shape,dst.shape)
  self.assertTrue(np.array_equal(src[...,3],dst[...,3]))
  self.assertTrue(np.array_equal(src[src[...,3]>0],dst[src[...,3]>0]))
 def test_only_approved_neutral_and_opt_in(self):
  people=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people']
  images=people['resident_kkwak']['images']
  self.assertEqual(len({v['file'] for v in images.values()}),1)
  for e,v in images.items():
   self.assertTrue(v['native_detail'])
   if e!='neutral': self.assertEqual(v['fallback'],'neutral');self.assertEqual(v['candidate_approval'],'pending')
  self.assertEqual([p for p,v in people.items() if any(i.get('native_detail') for i in v['images'].values())],['resident_kkwak'])
