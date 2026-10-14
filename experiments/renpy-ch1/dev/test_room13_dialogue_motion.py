"""Ensure field rendering and masks bypass all idle wrappers and dialogue closeups remain still after their ATL entrance."""
import ast
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest
SOURCE=(Path(__file__).resolve().parents[1]/'game/room13_motion.rpy').read_text()
start=SOURCE.index('    def r13_idle_art(')
end=SOURCE.index('\n    class ',start)
CODE=compile(ast.parse(textwrap.dedent(SOURCE[start:end])),'room13_motion.rpy','exec')
class MotionScope(unittest.TestCase):
 def setUp(self):
  self.calls=[]
  def idle(*args):self.calls.append(args);return ('idle',args)
  env={'renpy':SimpleNamespace(displayable=lambda art:art),'R13AuthoredIdle':idle}
  exec(CODE,env);self.make=env['r13_idle_art']
 def test_field_art_identity_and_mask_identity(self):
  for contact in ('standing','surface','background_chair','hanging','portable_stool'):
   with self.subTest(contact=contact):
    art=object();self.assertIs(self.make(art,'karo','activity',{},200,300,contact=contact),art)
    self.assertIs(self.make(art,'karo','activity',{},200,300,contact=contact),art)
  self.assertFalse(self.calls)
 def test_dialogue_and_questions_remain_still(self):
  for speaking in (True,False):
   art=object();self.assertIs(self.make(art,'karo','neutral',{},400,500,contact='dialogue_bust',speaking=speaking),art)
  self.assertFalse(self.calls)
 def test_field_spec_with_front_crop_does_not_enable_motion(self):
  art=object();self.assertIs(self.make(art,'karo','neutral',{'contact':'dialogue_bust'},200,300,contact='standing'),art)
if __name__=='__main__':unittest.main()
