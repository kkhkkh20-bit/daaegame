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
  # 0.19.98 night settings: every state is one of the shared night-button frames.
  self.assertNotIn('R13InkPanel',s);self.assertEqual(s.count('assets/ui-night/opt_btn_'),5)
 def test_preview_not_stretched_and_font_unchanged(self):
  s=(ROOT/'game/screens.rpy').read_text();self.assertIn('add typing_preview\n',s);self.assertNotIn('add typing_preview xsize',s)
  p=(ROOT/'game/room13_typing_preview.rpy').read_text();self.assertIn('r13_ui_font()',p);self.assertIn('font=signature[2]',p)
 def test_map_footer_gaps_and_right_inset(self):
  tabs=(366,364);travel=(772-24,232);back=(1020-24,232)
  self.assertGreaterEqual(travel[0]-sum(tabs),16);self.assertGreaterEqual(back[0]-sum(travel),16);self.assertEqual(1256-sum(back),28)
 def test_header_text_same_centerline(self):
  s=(ROOT/'game/room13_navigation.rpy').read_text()
  self.assertIn('area (46,20,190,76)',s);self.assertIn('area (260,20,950,76)',s)
  self.assertIn('text "여관 안내" yalign .5',s);self.assertIn('r13_location_path()) yalign .5',s)
