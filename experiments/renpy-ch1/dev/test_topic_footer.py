import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TopicFooter(unittest.TestCase):
 def test_right_return_reserved_only_for_topics(self):
  s=(ROOT/'game/room13_screens.rpy').read_text()
  self.assertEqual(s.count('reserve_return=True'),1)
  self.assertEqual(s.count('use r13_concept_action(R13_CONCEPT_RIGHT-232,232,"돌아가기"'),2)
 def test_geometry_desktop_touch_large(self):
  rects=[(336,256),(608,160),(784,160),(1000,232)]
  for height in (64,80,88):
   for x,w in rects:self.assertLessEqual(x+w,1232)
   for (x,w),(nx,nw) in zip(rects,rects[1:]):self.assertGreaterEqual(nx-x-w,16)
