"""New reviewed originals stay lossless; fallback is never counted as expression art."""
import hashlib,json,unittest
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
REPORT=json.loads((R/'art/incoming/reviewed-batches-20261017/connection-report.json').read_text())
FB=json.loads((R/'game/assets/room13-fullbody-dialogue.json').read_text())['people']
class ReviewedBatches(unittest.TestCase):
 def test_original_pixels_and_frame_margin(self):
  seen=set()
  for row in REPORT['expressions']+REPORT['poses']+REPORT['actions']:
   source=R/row['source'];spec=row['image'];self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),spec['source_sha256'])
   src=np.array(Image.open(source).convert('RGBA'));dst=np.array(Image.open(R/'game'/spec['file']).convert('RGBA'))
   self.assertTrue(np.array_equal(src,dst),row['source']);self.assertEqual(int(src[:,:,3].min()),0);self.assertGreaterEqual(int(src[:,:,3].max()),250)
   self.assertFalse(any((edge>32).any() for edge in [src[0,:,3],src[-1,:,3],src[:,0,3],src[:,-1,3]]),row['source'])
   self.assertNotIn(spec['source_sha256'],seen);seen.add(spec['source_sha256']);self.assertTrue(spec['native_detail'])
 def test_distinct_expression_connections_and_held_joy(self):
  for row in REPORT['expressions']:
   spec=FB[row['person']]['images'][row['key']];self.assertEqual(spec,row['image']);self.assertNotIn('fallback',spec);self.assertNotEqual(spec['file'],FB[row['person']]['images']['neutral']['file'])
  self.assertEqual(FB['resident_teacher']['images']['joy']['fallback'],'neutral')
 def test_pose_uses_mapped_native_image(self):
  for row in REPORT['poses']:
   spec=FB[row['person']]['poses'][row['key']];self.assertEqual(spec['mapped_image'],row['image']);self.assertEqual(spec['figure'],FB[row['person']]['figure'])
