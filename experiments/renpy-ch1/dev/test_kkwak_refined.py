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
 def test_reviewed_expressions_preserve_native_pixels_and_neutral(self):
  people=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people']
  images=people['resident_kkwak']['images']
  self.assertEqual(len({v['file'] for v in images.values()}),6)
  for e,v in images.items():
   self.assertTrue(v['native_detail'])
   self.assertNotIn('fallback',v)
   if e=='neutral': continue
   src=np.asarray(Image.open(ROOT/f'art/incoming/kkwak-expressions-20261017/kwaeksun-{e}-candidate-v1.png').convert('RGBA'))
   dst=np.asarray(Image.open(ROOT/'game'/v['file']).convert('RGBA'))
   self.assertEqual(src.shape,dst.shape)
   self.assertTrue(np.array_equal(src,dst))
   self.assertEqual(v['map'][0],1.0)
  self.assertTrue(all(i.get('native_detail') for i in images.values()))
