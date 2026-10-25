"""생존 확정·현재 등장·미완료인 부엉이만 기록읽기를 돕는다."""
import itertools
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class OwlReading(unittest.TestCase):
 def test_presence_and_once_guard(self):
  label=(ROOT/'game/room13_v111_owl_prevent.rpy').read_text().split('label r13_v111_owl_reading8:',1)[1]
  guard=next(line.strip()[3:-1] for line in label.splitlines() if line.strip().startswith('if '))
  for alive,done,present in itertools.product((None,False,True),(None,False,True),(False,True)):
   values={'OWL_ALIVE':alive,'owl_reading8_done':done}
   skip=eval(guard,dict(r13_v111_value=values.get,r13_v111_actor_ready=lambda _:present))
   self.assertEqual(not skip,alive is True and not done and present)
if __name__=='__main__':unittest.main()
