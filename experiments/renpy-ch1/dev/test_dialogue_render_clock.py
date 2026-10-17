"""Renderer clock must begin at first draw, not inherit the screen's age."""
import ast,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
from test_dialogue_beats import functions
class RenderClock(unittest.TestCase):
 def test_existing_screen_age_and_reconstruction_do_not_skip_or_replay_flinch(self):
  env=functions();plan=dict(person='guard',talk='surprise_talk',react='surprise_react',settled=False,duration=.35)
  env.update(store=SimpleNamespace(r13_dialogue_beat=plan),persistent=SimpleNamespace(room13_motion=True),Fixed=lambda child,**kw:child,Transform=lambda path,**kw:path,renpy=SimpleNamespace(Displayable=object,is_skipping=lambda:False,in_rollback=lambda:False,redraw=lambda *args:None,render=lambda frame,*args:frame))
  src=(Path(__file__).resolve().parents[1]/'game/systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:\n',1)[1]
  tree=ast.parse(textwrap.dedent(src));cls=next(n for n in tree.body if isinstance(n,ast.ClassDef));exec(compile(ast.Module(body=[cls],type_ignores=[]),'renderer','exec'),env)
  profile=dict(canvas=[100,200],frames={key:dict(file=key,offset=[0,0]) for key in ('surprise_talk','surprise_react')})
  art=env['R13DialogueBeat'](plan,profile)
  self.assertEqual(art.render(100,200,100,100),'surprise_react')
  self.assertEqual(art.render(100,200,100.2,100.2),'surprise_react')
  self.assertEqual(art.render(100,200,100.36,100.36),'surprise_talk')
  self.assertTrue(env['store'].r13_dialogue_beat['settled'])
  rebuilt=env['R13DialogueBeat'](env['store'].r13_dialogue_beat,profile)
  self.assertEqual(rebuilt.render(100,200,200,200),'surprise_talk')
if __name__=='__main__':unittest.main()
