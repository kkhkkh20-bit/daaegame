"""Field residents breathe (0.18.37, owner) but their hit masks and dialogue close-ups stay still."""
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
  def idle(*args,**kwargs):self.calls.append((args,kwargs));return ('idle',args)
  env={'renpy':SimpleNamespace(displayable=lambda art:art),'R13AuthoredIdle':idle,'R13_FIELD_IDLE':True}
  exec(CODE,env);self.make=env['r13_idle_art'];self.env=env
 def test_field_art_breathes_with_contact(self):
  for contact in ('standing','surface','background_chair','hanging','portable_stool'):
   with self.subTest(contact=contact):
    self.calls.clear();art=object()
    out=self.make(art,'karo','activity',{},200,300,contact=contact)
    self.assertEqual(out[0],'idle')
    self.assertEqual(self.calls[0][1],dict(contact=contact,field=True))
 def test_hit_mask_is_still(self):
  art=object();self.assertIs(self.make(art,'karo','activity',{},200,300,contact='standing',still=True),art)
  self.assertFalse(self.calls)
 def test_dialogue_and_questions_remain_still(self):
  for speaking in (True,False):
   art=object();self.assertIs(self.make(art,'karo','neutral',{},400,500,contact='dialogue_bust',speaking=speaking),art)
  self.assertFalse(self.calls)
 def test_switch_turns_field_idle_off(self):
  self.env['R13_FIELD_IDLE']=False
  art=object();self.assertIs(self.make(art,'karo','neutral',{},200,300,contact='standing'),art)
if __name__=='__main__':unittest.main()
