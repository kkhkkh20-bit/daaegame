import json,unittest,hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class PressureArt(unittest.TestCase):
 def test_registered_poses_preserve_neutral_scale_and_align_feet(self):
  talk=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']['resident_ppul']['profiles']
  poses=json.loads((ROOT/'game/assets/room13-dialogue-pose-source-art.json').read_text())['people']['resident_ppul']['pose_profiles']
  for name,bottom in [('cornered',1473),('collapse',1486)]:
   row=poses[name];self.assertTrue(row['diagnostic_only'])
   for h,p in row['profiles'].items():
    f=p['frames']['neutral'];neutral=talk[h]['frames']['neutral']
    source=ROOT/f['source_master'];self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),f['source_sha256'])
    with Image.open(ROOT/'game'/f['file']) as im,Image.open(ROOT/'game'/neutral['file']) as ref:
     self.assertEqual(im.size,ref.size);self.assertEqual(im.mode,'RGBA')
     ratio=im.height/1528
     self.assertLessEqual(abs(bottom*ratio+f['offset'][1]-(1498*ratio+neutral['offset'][1])),.5)
    self.assertEqual(p['canvas'],talk[h]['canvas'])
 def test_rejected_crowd_not_shipped(self):
  self.assertFalse((ROOT/'game/assets/council-murmur-A-review.ogg').exists())
  self.assertNotIn('meeting_murmur',(ROOT/'game/systems/room13_meeting_pressure.rpy').read_text())
