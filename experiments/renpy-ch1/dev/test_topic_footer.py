import ast
import re
import textwrap
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TopicFooter(unittest.TestCase):
 def test_topic_tools_and_return_have_separate_spaces_inside_the_book(self):
  source=(ROOT/'game/systems/room13_side_questions.rpy').read_text()
  rects={caption:(int(x),int(w)) for x,w,caption in re.findall(r'use r13_notebook_topic_action\((\d+),(\d+),"([^"]+)"',source)}
  self.assertEqual(set(rects),{'자료 제시','기록','더보기','돌아가기'})
  ordered=[rects[k] for k in ('자료 제시','기록','더보기','돌아가기')]
  list_left=int(re.search(r'pos \((\d+),R13_SIDE_QUESTION_TOP',source).group(1))
  list_width=int(re.search(r'xsize (\d+) ysize height padding',source).group(1))
  for x,w in ordered:
   self.assertGreaterEqual(x,list_left)
   self.assertLessEqual(x+w,list_left+list_width)
   self.assertGreaterEqual(w*360/720,44)
  for (x,w),(nx,nw) in zip(ordered,ordered[1:]):self.assertGreaterEqual(nx-x-w,8)
  self.assertEqual(ordered[-1][0],max(x for x,w in ordered))
  self.assertEqual(len({w for x,w in ordered}),1)
  self.assertEqual(ordered[0][0],list_left)
  self.assertEqual(sum(ordered[-1]),list_left+list_width)

 def test_footer_and_question_pager_have_separate_touch_areas(self):
  source=(ROOT/'game/systems/room13_side_questions.rpy').read_text()
  block=source.split('init 80 python:\n',1)[1].split('\nscreen ',1)[0]
  tree=ast.parse(textwrap.dedent(block))
  node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_notebook_topic_y')
  action=source.split('screen r13_notebook_topic_action(',1)[1].split('\nscreen ',1)[0]
  action_area=re.search(r'area (\([^\n]+\))',action).group(1)
  pager_area=re.search(r'id "r13_topics_previous"\n\s+area (\([^\n]+\))',source).group(1)
  for touch in (False,True):
   ns=dict(r13_touch_ui=lambda:touch)
   exec(compile(ast.Module(body=[node],type_ignores=[]),'<topic-y>','exec'),ns)
   x,y,w,h=eval(action_area,ns,dict(x=0,w=1))
   px,py,pw,ph=eval(pager_area,ns)
   self.assertLessEqual(py+ph,y-8)
   self.assertLessEqual(y+h,720-16)
   if touch:self.assertGreaterEqual(h*360/720,44)
