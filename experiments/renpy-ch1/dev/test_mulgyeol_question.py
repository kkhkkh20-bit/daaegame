"""Source contract for knowledge-before-question; no UI/playthrough claim."""
import ast,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MulgyeolQuestion(unittest.TestCase):
 def setUp(self):
  s=(ROOT/'game/systems/room13_new_cast.rpy').read_text()
  block=s.split('init 145 python:\n',1)[1].split('\ninit ',1)[0].split('\nlabel ',1)[0]
  tree=ast.parse(textwrap.dedent(block));self.topics={}
  # Read actual author calls, not a duplicated fixture with corrected wording.
  for n in tree.body:
   if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='_r13_nc_topic':
    c=n.value;key=ast.literal_eval(c.args[0])
    if key.startswith('mulgyeol:water'):self.topics[key]=dict(title=ast.literal_eval(c.args[2]),lines=ast.literal_eval(c.args[3]),**{kw.arg:ast.literal_eval(kw.value) for kw in c.keywords})
 def test_both_questions_state_purpose_without_guessing_dawn_or_water(self):
  self.assertEqual(len(self.topics),2)
  for row in self.topics.values():
   self.assertIn('아내를 찾고 있습니다',row['lines'][0][1])
   for word in ('새벽','물 길러','해 뜨기','숲','낯선'):
    self.assertNotIn(word,row['title']);self.assertNotIn(word,row['lines'][0][1])
 def test_helped_path_retains_actual_witness_clues(self):
  t=self.topics['mulgyeol:water'];self.assertEqual(t['need'],['mulgyeol_helped'])
  text=str(t['lines'][1:]);self.assertIn('해 뜨기 전에',text);self.assertIn('숲으로',text);self.assertIn('【도토리】',text);self.assertIn('찾으시는 분인지는 모르겠어요',text)
 def test_cold_path_retains_cost_of_refusal_without_free_acorn_clue(self):
  t=self.topics['mulgyeol:water_cold'];self.assertEqual(t['need'],['mulgyeol_fell']);self.assertEqual(t['not_flags'],['mulgyeol_helped'])
  text=str(t['lines'][1:]);self.assertIn('해 뜨기 전에',text);self.assertNotIn('도토리',text)
if __name__=='__main__':unittest.main()
