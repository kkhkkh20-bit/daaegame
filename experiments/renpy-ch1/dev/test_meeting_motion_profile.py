"""A review candidate: pacing must remain bounded and motion preferences win."""
import unittest, textwrap, types
from pathlib import Path
class MotionProfile(unittest.TestCase):
 def setUp(self):
  src=(Path(__file__).resolve().parents[1]/'game/room13_meeting_camera.rpy').read_text()
  src=src[src.index('    def r13_meeting_motion_profile'):src.index('    def r13_meeting_world_slot')]
  self.now=0.0;self.store=types.SimpleNamespace(r13_meeting_previous_focus='a',r13_meeting_shot_revision=1,r13_meeting_direction={'beat':'interrupt'})
  self.env=dict(R13_MEETING_SPEED_LINES=False,store=self.store,persistent=types.SimpleNamespace(room13_motion=True),renpy=types.SimpleNamespace(is_skipping=lambda:False,in_rollback=lambda:False,display=types.SimpleNamespace(core=types.SimpleNamespace(get_time=lambda:self.now))),r13_meeting_cast=lambda c,s:[('a',0),('b',0),('c',0)],r13_debate_session=lambda c:'x')
  exec(textwrap.dedent(src),self.env)
 def test_ease_is_continuous_monotone_and_stops(self):
  f=self.env['r13_meeting_motion_ease'];v=[f(i/1000) for i in range(1001)]
  self.assertAlmostEqual(v[0],0);self.assertAlmostEqual(v[-1],1)
  self.assertTrue(all(a<=b+1e-12 for a,b in zip(v,v[1:])))
  self.assertLess(1-f(.999),.000001)
 def test_distinct_pacing_and_bounded_long_moves(self):
  f=self.env['r13_meeting_motion_profile'];self.assertLess(f('interrupt')[1],f('listen')[1]);self.assertGreater(f('reversal')[0],0)
  for beat in ('listen','interrupt','gasp','reversal','press','explain','resolve'):
   hold,duration=f(beat,20);self.assertGreater(duration,0);self.assertLessEqual(hold+duration,.6)
 def test_interrupt_moves_and_disabled_motion_snaps(self):
  f=self.env['r13_meeting_world_view'];self.assertEqual(f('C','b'),(0.0,True));self.now=.09
  view,moving=f('C','b');self.assertGreater(view,0);self.assertLess(view,1);self.assertTrue(moving)
  self.env['persistent'].room13_motion=False;self.assertEqual(f('C','b'),(1.0,False))
 def test_profile_does_not_jump_when_line_beat_changes_mid_pan(self):
  f=self.env['r13_meeting_world_view'];f('C','b');self.now=.09;before=f('C','b');self.store.r13_meeting_direction={'beat':'gasp'};self.assertEqual(before,f('C','b'))
 def test_speed_card_settles_without_interpolating_and_does_not_repeat(self):
  self.env['R13_MEETING_SPEED_LINES']=True;f=self.env['r13_meeting_world_view']
  self.assertEqual(f('C','b'),(1.0,True));self.now=.19
  self.assertEqual(f('C','b'),(1.0,False));self.now=.3
  self.assertEqual(f('C','b'),(1.0,False))
  self.store.r13_meeting_shot_revision=2;self.env['renpy'].in_rollback=lambda:True
  self.assertEqual(f('C','b'),(1.0,False))
if __name__=='__main__':unittest.main()
