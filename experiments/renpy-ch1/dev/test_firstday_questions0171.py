import textwrap,types,unittest
from pathlib import Path
class FirstdayQuestions(unittest.TestCase):
 def test_only_replaced_road_question_is_filtered(self):
  source=(Path(__file__).resolve().parents[1]/'game/systems/room13_first_day_flow.rpy').read_text().split('    _r13_firstday_topics=r13_topics',1)[1]
  rows=[(k,{'npc':'karo'}) for k in ('life:karo:work','unlocked:followup','karo_road')]
  for state in ({'day':1,'life_poc':True,'read_topics':[]},{'day':1,'life_poc':True,'read_topics':['life:karo:work']},{'day':2,'life_poc':True,'read_topics':['life:karo:work']}):
   ns={'store':types.SimpleNamespace(room13=state),'_r13_firstday_topics':lambda person:rows}
   exec(textwrap.dedent(source),ns)
   self.assertEqual([k for k,t in ns['r13_topics']('karo')],['life:karo:work','unlocked:followup'])
 def test_old_non_poc_saves_keep_original_questions(self):
  source=(Path(__file__).resolve().parents[1]/'game/systems/room13_first_day_flow.rpy').read_text().split('    _r13_firstday_topics=r13_topics',1)[1]
  ns={'store':types.SimpleNamespace(room13={'day':1}),'_r13_firstday_topics':lambda person:[('karo_road',{})]};exec(textwrap.dedent(source),ns);self.assertEqual(ns['r13_topics']('karo'),[('karo_road',{})])
if __name__=='__main__':unittest.main()
