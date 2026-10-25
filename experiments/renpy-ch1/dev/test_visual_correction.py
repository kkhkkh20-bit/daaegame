import ast,re,textwrap,unittest
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
 def blit(self,image,pos):self.ops.append(('blit',image.size,pos,image.visual))
class VisualCorrection(unittest.TestCase):
 def test_selected_paper_has_identical_panel_geometry(self):
  s=(ROOT/'game/room13_ui_art.rpy').read_text().split('init 58 python:\n',1)[1].split('\ninit 61:',1)[0]
  tree=ast.parse(textwrap.dedent(s));node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='R13PaperFrame')
  def transform(child,**properties):return dict(child=child,**properties)
  def render(visual,width,height,st,at):return SimpleNamespace(size=(width,height),visual=visual)
  ns={'renpy':SimpleNamespace(Displayable=Displayable,Render=Render,render=render),
      'r13_sticker_button':lambda:dict(asset='shared_sticker'),
      'Transform':transform,'TintMatrix':lambda color:('tint',color)}
  exec(compile(ast.Module(body=[node],type_ignores=[]),'paper','exec'),ns)
  normal=ns['R13PaperFrame']().render(164,56,0,0).ops;selected=ns['R13PaperFrame'](ink=True).render(164,56,0,0).ops
  # The same asset is rendered at the same size and origin in both states;
  # the darker state adds a colour transform, never a different hit footprint.
  self.assertEqual([(x[0],x[1],x[2]) for x in normal],[(x[0],x[1],x[2]) for x in selected])
  self.assertEqual(normal[0][1:3],((164,56),(0,0)))
  self.assertEqual(normal[0][3]['child'],selected[0][3]['child']['child'])
  self.assertNotEqual(normal,selected)
 def test_option_states_share_frame(self):
  s=(ROOT/'game/screens.rpy').read_text().split('style r13opt_button is button:',1)[1].split('style r13opt_button_text',1)[0]
  # All five states now share the same sticker surface family.
  self.assertNotIn('R13InkPanel',s);self.assertEqual(s.count('r13_sticker_button('),5);self.assertNotIn('b_opt_choice',s)
 def test_preview_not_stretched_and_font_unchanged(self):
  s=(ROOT/'game/screens.rpy').read_text();self.assertIn('add typing_preview\n',s);self.assertNotIn('add typing_preview xsize',s)
  p=(ROOT/'game/room13_typing_preview.rpy').read_text();self.assertIn('r13_ui_font()',p);self.assertIn('font=signature[2]',p)
 def test_map_footer_gaps_and_right_inset(self):
  source=(ROOT/'game/room13_map_village_b.rpy').read_text()
  tabs=ast.literal_eval(re.search(r'for key,title,rect in (\(.*\)):',source).group(1))
  rects=[rect for key,title,rect in tabs]
  rects.extend(ast.literal_eval(rect) for caption,rect in re.findall(r'use r13_village_b_control\("([^"]+)",(\([^\n]+?\)),',source))
  self.assertEqual(len(rects),5)
  helper=source.split('screen r13_village_b_control(',1)[1].split('\nscreen ',1)[0]
  area=re.search(r'area (\([^\n]+\))',helper).group(1)
  for touch in (False,True):
   targets=[]
   for bx,by,bw,bh in rects:
    targets.append(eval(area,dict(r13_touch_ui=lambda:touch),dict(bx=bx,by=by,bw=bw,bh=bh)))
   self.assertEqual(len({y+h/2 for x,y,w,h in targets}),1)
   for x,y,w,h in targets:
    self.assertGreaterEqual(x,16)
    self.assertLessEqual(x+w,1280-16)
    self.assertLessEqual(y+h,720-8)
    if touch:self.assertGreaterEqual(h*360/720,44)
   for (x,y,w,h),(nx,ny,nw,nh) in zip(targets,targets[1:]):self.assertGreaterEqual(nx-x-w,8)
 def test_header_text_same_centerline(self):
  navigation=(ROOT/'game/room13_navigation.rpy').read_text()
  self.assertIn('use r13_map_village_b(',navigation)
  village=(ROOT/'game/room13_map_village_b.rpy').read_text()
  view=ast.literal_eval(re.search(r'R13_VILLAGE_B_VIEW = (\([^\n]+\))',village).group(1))
  # The approved village title has its own strip ABOVE the draggable map. Read
  # the live rectangles so a later harmless position change cannot hide overlap.
  strips=[tuple(map(int,row)) for row in re.findall(r'add Solid\("[^"]+"\) xpos (\d+) ypos (\d+) xysize \((\d+),(\d+)\)',village)]
  strip=next(rect for rect in strips if rect[0]==view[0] and rect[2]==view[2] and rect[1]+rect[3]==view[1])
  fixed=re.findall(r'    fixed:\n        area (\([^\n]+\))\n(.*?)(?=\n    \S|\Z)',village,re.S)
  title=ast.literal_eval(next(area for area,body in fixed if '다람탐정 · 마을 지도' in body))
  current=ast.literal_eval(next(area for area,body in fixed if '"현재 · "' in body))
  for rect in (title,current):
   self.assertGreaterEqual(rect[0],strip[0])
   self.assertGreaterEqual(rect[1],strip[1])
   self.assertLessEqual(rect[0]+rect[2],strip[0]+strip[2])
   self.assertLessEqual(rect[1]+rect[3],view[1])
  self.assertLessEqual(title[0]+title[2]+8,current[0])
  self.assertLessEqual(abs(title[1]+title[3]/2-current[1]-current[3]/2),4)
  # Inn/forest now share the village notebook footer instead of an outer band.
  nav=(ROOT/'game/room13_navigation.rpy').read_text()
  self.assertIn('use r13_map_diary_footer(region,selected,ready,local_guide,close_action)',nav)
  self.assertIn('xpos 640 ypos 78 xanchor .5',nav)
