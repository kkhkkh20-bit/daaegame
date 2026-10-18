import ast,re,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
S=(ROOT/'game/screens.rpy').read_text();A=S.split('# The same folio and left index',1)[1].split('\nscreen save():',1)[0]
class SettingsTypeScale(unittest.TestCase):
 def test_all_settings_text_uses_two_tokens_or_real_dialogue(self):
  values=re.findall(r'(?<!\w)(?:text_)?size ([^\n]+)',A)
  for value in values:self.assertTrue(value.startswith(('r13_opt_size()','r13_opt_title_size()','_r13_say_size()')),value)
  self.assertEqual(A.count('size r13_opt_title_size()'),1)
 def test_scale_small_normal_large(self):
  block=A.split('init python:\n',1)[1].split('\nstyle ',1)[0]
  for small,large,body,title,row in [(False,False,22,30,92),(True,False,20,27,92),(False,True,26,34,112)]:
   def size(base,big):return big if large else int(max(base-3,round(base*.9))) if small else base
   ns={'r13_read_size':size,'persistent':SimpleNamespace(room13_large_text=large)};exec(textwrap.dedent(block),ns)
   self.assertEqual((ns['r13_opt_size'](),ns['r13_opt_title_size'](),ns['r13_opt_row_height']()),(body,title,row))
 def test_no_footer_overlap_all_tabs_even_large(self):
  self.assertIn('area (292,124,914,484) mousewheel True draggable True scrollbars "vertical"',A)
  self.assertLessEqual(124+484,630-16)
  self.assertLessEqual(322+4*132+3*8,904)
  self.assertLessEqual(322+300+70+164+2*8,904)
  self.assertLessEqual(322+360+132+8,904)
 def test_row_labels_and_controls_share_vertical_center(self):
  self.assertIn('xpos 0 yalign .5 xsize 304 spacing 4',A)
  self.assertIn('ypos ((r13_opt_row_height()-56)//2)',A)
 def test_preview_uses_actual_say_size_without_transform(self):
  preview=(ROOT/'game/room13_typing_preview.rpy').read_text()
  self.assertIn('(preferences.text_cps, _r13_say_size(), r13_ui_font())',preview)
  self.assertNotIn('r13_read_size(24,30)',preview)
  self.assertIn('size _r13_say_size()',A);self.assertNotIn('add typing_preview xsize',A)
 def test_replay_and_footer_share_padding_height(self):
  self.assertIn('"다시 보기" id "r13_preview_replay" xsize 160 ysize 56 padding (10,8)',A)
  self.assertNotIn('text_size 21',A);self.assertNotIn('text_size 24',A)
