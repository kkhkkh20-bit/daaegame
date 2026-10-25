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
  view=re.search(r'id "r13_settings_body"\n\s+area (\([^\n]+\)) mousewheel',A).group(1)
  footer=A.split('textbutton "설정 초기화"',1)[1].split('key "game_menu"',1)[0]
  footer_rects=re.findall(r'xpos (\d+) ypos (\([^\n]+?\)) xsize (\d+)',footer)
  self.assertEqual(len(footer_rects),5)
  row=A.split('screen r13_opt_row(',1)[1].split('\nscreen ',1)[0]
  row_width=int(re.search(r'xsize (\d+) ysize r13_opt_row_height',row).group(1))
  controls_x,gap=map(int,re.search(r'hbox:\n\s+xpos (\d+)[^\n]+spacing (\d+)',row).groups())
  height_expr=re.search(r'def r13_opt_button_height\(\):\n\s+#[^\n]+\n\s+return ([^\n]+)',A).group(1)
  for touch in (False,True):
   ns=dict(r13_touch_ui=lambda:touch)
   vx,vy,vw,vh=eval(view,ns)
   height=eval(height_expr,ns)
   self.assertLessEqual(row_width,vw-8)
   rects=[(int(x),eval(y,ns),int(w),height) for x,y,w in footer_rects]
   self.assertLessEqual(vy+vh,min(y for x,y,w,h in rects)-16)
   for x,y,w,h in rects:self.assertLessEqual(y+h,720-16)
   for (x,y,w,h),(nx,ny,nw,nh) in zip(rects,rects[1:]):self.assertGreaterEqual(nx-x-w,8)
  # Measure each row's real children, including repeated options and both
  # administrator states, against the current notebook content width.
  lines=A.splitlines()
  rows=[]
  for i,line in enumerate(lines):
   if re.match(r'\s+use r13_opt_row\(',line):
    indent=len(line)-len(line.lstrip());body=[]
    for child in lines[i+1:]:
     if child.strip() and len(child)-len(child.lstrip())<=indent:break
     body.append(child)
    rows.append('\n'.join(body))
  self.assertGreaterEqual(len(rows),10)
  for body in rows:
   for branch in re.split(r'^\s+else:\s*$',body,flags=re.M):
    widths=list(map(int,re.findall(r'\bxsize (\d+)',branch)))
    repeat=re.search(r'for [^\n]+ in (\([^\n]+\)):',branch)
    if repeat:widths*=len(ast.literal_eval(repeat.group(1)))
    if widths:self.assertLessEqual(controls_x+sum(widths)+gap*(len(widths)-1),row_width)
 def test_mixer_thumb_does_not_touch_percentage(self):
  for widget in ('music_volume','fx_volume'):
   self.assertIn('ysize 36 yalign .5 id "'+widget+'"',A)
  row=A.split('screen r13_opt_row(',1)[1].split('\nscreen ',1)[0]
  gap=int(re.search(r'hbox:\n[^\n]+spacing (\d+)',row).group(1))
  thumb_offset=int(re.search(r'thumb_offset (-?\d+)',A).group(1))
  self.assertIn('Crop((16,16,36,36)',A)
  self.assertGreaterEqual(gap-abs(thumb_offset),8)
  for widget in ('music_volume','fx_volume'):
   self.assertRegex(A,r'id "'+widget+r'"\n\s+text [^\n]+id "'+widget+r'_percent"[^\n]+xsize 64 yalign \.5')
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
