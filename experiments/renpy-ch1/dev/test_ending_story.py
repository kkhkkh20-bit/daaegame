"""Ending panels stay inside their atlases and never rewrite the case state."""
import copy,json,textwrap,types,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class EndingStory(unittest.TestCase):
 def setUp(self):
  self.data=json.loads((ROOT/'game/assets/room13-ending-stories.json').read_text())['endings']
  self.state=dict(flags=[],propositions=[],victim_state='dead',evidence=[],day=14)
  self.env=dict(R13_ENDING_STORIES=self.data,room13=self.state,r13_has=lambda flag:flag in self.state['flags'])
  src=(ROOT/'game/systems/room13_ending_story.rpy').read_text().split('    def r13_ending_story_frame',1)[1].split('\ntransform ',1)[0]
  exec(textwrap.dedent('    def r13_ending_story_frame'+src),self.env)
 def test_all_seven_endings_have_four_complete_panels(self):
  self.assertEqual(set(self.data),{'E'+str(i) for i in range(7)})
  for key,frames in self.data.items():
   self.assertEqual(len(frames),4)
   self.assertEqual(len({tuple(f["rect"]) for f in frames}),4)
   for frame in frames:
    with Image.open(ROOT/'game'/frame['file']) as im:w,h=im.size
    x,y,cw,ch=frame['rect'];self.assertGreater(cw,0);self.assertGreater(ch,0)
    self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0);self.assertLessEqual(x+cw,w);self.assertLessEqual(y+ch,h)
    self.assertTrue(frame['heading']);self.assertLess(len(frame['caption']),120)
 def test_captions_do_not_grant_records_or_change_world_state(self):
  original=copy.deepcopy(self.state);data=copy.deepcopy(self.data)
  for key in self.data:
   for i in range(4):self.env['r13_ending_story_frame'](key,i)
  self.assertEqual(self.state,original);self.assertEqual(self.data,data)
 def test_imperfect_ending_does_not_invent_a_supply_shortage(self):
  frame=self.env['r13_ending_story_frame']
  self.assertIn('옮기지 못한 장작',frame('E4',1)['caption'])
  self.state['flags']=['supplies_ready']
  self.assertIn('옮길 손',frame('E4',1)['caption'])
  self.state['flags'].append('patient_transport')
  self.assertIn('모아 둔 물자는 있었다',frame('E4',1)['caption'])
  self.assertIn('회복을 뒷받침할 기록',frame('E4',2)['caption'])
 def test_surviving_elder_is_not_given_a_death_caption(self):
  self.assertIn('잃은 사람',self.env['r13_ending_story_frame']('E5',2)['caption'])
  self.state['victim_state']='alive'
  self.assertNotIn('잃은 사람',self.env['r13_ending_story_frame']('E5',2)['caption'])
  self.assertIn('살아 돌아왔다고',self.env['r13_ending_story_frame']('E5',2)['caption'])
  self.assertIn('고대 장치',self.env['r13_ending_story_frame']('E6',2)['caption'])
 def test_camera_remains_inside_overscan_and_stops(self):
  tick=self.env['r13_ending_camera_tick'];t=types.SimpleNamespace()
  for direction in (-1,1):
   for elapsed in (0,1,5,10,100):
    result=tick(t,elapsed,0,direction)
    self.assertIsInstance(t.xoffset,int);self.assertIsInstance(t.yoffset,int)
    self.assertGreaterEqual(t.xoffset,-64);self.assertLessEqual(t.xoffset,0)
    self.assertGreaterEqual(t.yoffset,-36);self.assertLessEqual(t.yoffset,0)
    if elapsed>=10:self.assertIsNone(result)
if __name__=='__main__':unittest.main()
