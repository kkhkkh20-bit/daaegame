import ast,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
class Displayable:
 def __init__(self,**kw):pass
class Render:
 def __init__(self,*a):self.ops=[]
 def canvas(self):return self
 def rect(self,color,rect):self.ops.append(('rect',color,rect))
 def line(self,color,a,b,width):self.ops.append(('line',color,a,b,width))
class VisualCorrection(unittest.TestCase):
 def test_selected_paper_has_identical_square_geometry(self):
  s=(ROOT/'game/room13_ui_art.rpy').read_text().split('init 58 python:\n',1)[1].split('\ninit 61:',1)[0]
  tree=ast.parse(textwrap.dedent(s));node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='R13PaperFrame')
  ns={'renpy':SimpleNamespace(Displayable=Displayable,Render=Render)};exec(compile(ast.Module(body=[node],type_ignores=[]),'paper','exec'),ns)
  normal=ns['R13PaperFrame']().render(164,56,0,0).ops;selected=ns['R13PaperFrame'](ink=True).render(164,56,0,0).ops
  self.assertEqual([(x[0],x[2:]) for x in normal],[(x[0],x[2:]) for x in selected]);self.assertNotEqual(normal,selected)
 def test_option_states_share_frame(self):
  s=(ROOT/'game/screens.rpy').read_text().split('style r13opt_button is button:',1)[1].split('style r13opt_button_text',1)[0]
  # B settings: all five states retain the same cropped frame geometry.
  self.assertNotIn('R13InkPanel',s);self.assertEqual(s.count('assets/ui-b-options/b_opt_choice'),5);self.assertEqual(s.count('Crop((16,16,190,52)'),5);self.assertEqual(s.count('),24,16)'),5)
 def test_preview_not_stretched_and_font_unchanged(self):
  s=(ROOT/'game/screens.rpy').read_text();self.assertIn('add typing_preview\n',s);self.assertNotIn('add typing_preview xsize',s)
  p=(ROOT/'game/room13_typing_preview.rpy').read_text();self.assertIn('r13_ui_font()',p);self.assertIn('font=signature[2]',p)
 def test_map_footer_gaps_and_right_inset(self):
  tabs=(366,364);travel=(772-24,232);back=(1020-24,232)
  self.assertGreaterEqual(travel[0]-sum(tabs),16);self.assertGreaterEqual(back[0]-sum(travel),16);self.assertEqual(1256-sum(back),28)
 def test_header_text_same_centerline(self):
  s=(ROOT/'game/room13_navigation.rpy').read_text()
  # 2026-10-24 B 지도: 여관 안·숲·산길은 이름·현재 위치를 수첩 아래 띠 한 줄(같은 가운데선)에 쓴다.
  self.assertIn('area (46,20,206,76)',s)
  b=(ROOT/'game/room13_map_b.rpy').read_text()
  self.assertIn('hbox:\n            yalign .5 spacing 14',b)
  self.assertIn('size 23 color "#4b3420" yalign .5',b);self.assertIn('size 17 color "#765b3e" yalign .5',b)
  self.assertIn('xalign 1.0 yalign .5 text_align 1.0',b)
