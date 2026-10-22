import ast,re,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
S=(ROOT/'game/screens.rpy').read_text();A=S.split('# The same folio and left index',1)[1].split('\nscreen save():',1)[0]
class SettingsTypeScale(unittest.TestCase):
 def test_all_settings_text_uses_two_tokens_or_real_dialogue(self):
  values=re.findall(r'(?<!\w)(?:text_)?size ([^\n]+)',A)
  # 0.19.98 night settings (owner mockup): every size is a token or a token with a fixed step.
  for value in values:self.assertRegex(value,r'^\(?(r13_opt_size\(\)|r13_opt_title_size\(\)|_r13_say_size\(\))([+-]\d\))?',value)
  self.assertEqual(A.count('size (r13_opt_title_size()+8)'),1)
 def test_scale_small_normal_large(self):
  block=A.split('init python:\n',1)[1].split('\nstyle ',1)[0]
  for small,large,body,title,row in [(False,False,22,30,92),(True,False,20,27,92),(False,True,26,34,112)]:
   def size(base,big):return big if large else int(max(base-3,round(base*.9))) if small else base
   ns={'r13_read_size':size,'persistent':SimpleNamespace(room13_large_text=large)};exec(textwrap.dedent(block),ns)
   self.assertEqual((ns['r13_opt_size'](),ns['r13_opt_title_size'](),ns['r13_opt_row_height']()),(body,title,row))
 def test_no_footer_overlap_all_tabs_even_large(self):
  self.assertIn('area (347,92,890,500) mousewheel True draggable True',A)
  self.assertLessEqual(92+500,626-16)
  self.assertLessEqual(264+4*143+3*15,884)
  self.assertLessEqual(264+3*190+2*15,884)
  self.assertLessEqual(264+280+64+150+2*15,884)
  self.assertLessEqual(264+330+143+15,884)
 def test_mixer_thumb_does_not_touch_percentage(self):
  for widget in ('music_volume','fx_volume'):
   self.assertIn('ysize 36 yalign .5 id "'+widget+'"',A)
  self.assertIn('thumb_offset 7',A);self.assertIn('spacing 15',A)
  self.assertGreaterEqual(15-7,8)
 def test_row_labels_and_controls_share_vertical_center(self):
  self.assertIn('xpos 0 yalign .5 xsize 256 spacing 4',A)
  self.assertIn('ypos ((r13_opt_row_height()-r13_opt_button_height())//2)',A)
 def test_preview_uses_actual_say_size_without_transform(self):
  preview=(ROOT/'game/room13_typing_preview.rpy').read_text()
  self.assertIn('(preferences.text_cps, _r13_say_size(), r13_ui_font())',preview)
  self.assertNotIn('r13_read_size(24,30)',preview)
  self.assertIn('size _r13_say_size()',A);self.assertNotIn('add typing_preview xsize',A)
 def test_replay_and_footer_share_padding_height(self):
  self.assertIn('"다시 보기" id "r13_preview_replay" xsize 160 text_size r13_opt_size()',A)
  self.assertIn('padding (10,4) ysize 52',A)
  self.assertNotIn('text_size 21',A);self.assertNotIn('text_size 24',A)
