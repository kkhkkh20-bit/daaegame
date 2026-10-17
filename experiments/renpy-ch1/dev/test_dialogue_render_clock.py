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
 def test_stale_dialogue_plan_cannot_replace_meeting_or_action_art(self):
  from check_dialogue_bindings import load_functions
  env=load_functions(Path(__file__).resolve().parents[1]/'game/room13_fullbody_dialogue.rpy')
  def forbidden(*args):raise AssertionError('stale dialogue plan replaced separate authored art')
  env.update(r13_dialogue_source_profile=lambda *args:None,r13_dialogue_beat_art=forbidden,r13_dialogue_source_neutral=lambda *args:None,r13_fullbody_spec=lambda *args:None)
  self.assertIsNone(env['r13_fullbody_close_art']('guard','living_stamp',840))
  env['r13_dialogue_source_profile']=lambda *args: {'frames':{}}
  env['r13_dialogue_beat_art']=lambda *args:'approved dialogue'
  self.assertEqual(env['r13_fullbody_close_art']('guard','neutral',840),'approved dialogue')
if __name__=='__main__':unittest.main()
