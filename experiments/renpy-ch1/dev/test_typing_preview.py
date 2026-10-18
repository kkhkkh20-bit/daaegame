"""Headless contract tests only, not native renderer proof."""
import textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
class Displayable:
 def __init__(self,**kwargs):pass
class Render:
 def __init__(self,*args):pass
 def get_size(self):return (860,80)
 def blit(self,*args):pass
class PreviewTest(unittest.TestCase):
 def setUp(self):
  self.times=[];self.children=[];self.redraws=[]
  self.pref=SimpleNamespace(text_cps=34)
  self.size=24
  def text(*a,**kw):
   child=SimpleNamespace(args=a,kw=kw);self.children.append(child);return child
  def render(child,w,h,st,at):self.times.append(st);return Render()
  renpy=SimpleNamespace(Displayable=Displayable,Render=Render,render=render,redraw=lambda *a:self.redraws.append(a))
  ns=dict(renpy=renpy,preferences=self.pref,r13_read_size=lambda *a:self.size,_r13_say_size=lambda:self.size,r13_ui_font=lambda:'test.ttf',R13DialogueText=text)
  source=(ROOT/'game/room13_typing_preview.rpy').read_text().split('init 71 python:\n',1)[1]
  exec(textwrap.dedent(source),ns);self.p=ns['R13TypingPreview']()
 def draw(self,t):self.p.render(860,88,t,t)
 def test_initial_and_hover_clock(self):
  self.draw(10);self.draw(10.5);self.assertEqual(self.times,[0,.5]);self.assertEqual(len(self.children),1)
 def test_replay_starts_at_zero_without_preference_write(self):
  self.draw(10);self.p.restart();self.draw(15);self.assertEqual(self.times,[0,0]);self.assertEqual(self.pref.text_cps,34)
 def test_each_speed_including_instant(self):
  for cps in (24,34,55,0):
   self.pref.text_cps=cps;self.draw(cps+100)
   self.assertEqual(self.children[-1].kw['slow_cps'],cps);self.assertEqual(self.times[-1],0)
 def test_same_speed_replays(self):
  self.draw(10);self.p.restart();self.draw(20);self.assertEqual(len(self.children),2)
 def test_size_change_restarts(self):
  self.draw(10);self.size=30;self.draw(12);self.assertEqual(self.children[-1].kw['size'],30);self.assertEqual(self.times[-1],0)
 def test_no_say_callbacks_or_preference_mutation(self):
  self.draw(10);self.assertFalse(self.children[-1].kw['slow_abortable'])
  source=(ROOT/'game/room13_typing_preview.rpy').read_text()
  for forbidden in ('renpy.say(', 'renpy.music.', 'save_persistent(', 'preferences.text_cps ='):
   self.assertNotIn(forbidden,source)
 def test_screen_hooks(self):
  source=(ROOT/'game/screens.rpy').read_text()
  self.assertIn('default typing_preview = R13TypingPreview()',source)
  self.assertIn('[Preference("text speed",speed_value),Function(typing_preview.restart)]',source)
  self.assertIn('add typing_preview',source)
  self.assertNotIn('add typing_preview xsize',source)
if __name__=='__main__':unittest.main(verbosity=2)
