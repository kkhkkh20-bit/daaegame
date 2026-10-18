import unittest
from pathlib import Path
G={}
for name in ('recommended_model.py','recommended_opening_model.py','recommended_ep23_model.py','recommended_ep456_model.py'):
 exec((Path(__file__).parent/name).read_text(),G)
def f(n,*args):return G['r13_rec_'+n](*args)
def act(s,*keys):
 for key in keys:s=f('apply',s,key)
 return s
class OpeningTests(unittest.TestCase):
 def test_entry_hides_unknown_village_until_actual_access(self):
  s=f('opening_state');self.assertEqual(s['day'],1)
  self.assertEqual([k for k,t in f('available',s)],['entry_report'])
  with self.assertRaises(ValueError):f('next_day',s)
  s=act(s,'entry_report','entry_original')
  self.assertTrue(f('opening_present',s,['entry_list','entry_original']))
  self.assertFalse(f('opening_present',s,['entry_list']))
  s=act(s,'entry_present')
  self.assertEqual([k for k,t in f('available',s)],['entry_inn'])
 def test_day1_contact_and_reunion_not_wait_wall(self):
  s=act(f('opening_state'),'entry_report','entry_original','entry_present','entry_inn')
  s=act(s,'repair','records','contact','delivery_wait','reply','meet')
  self.assertEqual((s['day'],s['mother']),(1,'M2'))
  s=f('evening',s);s=act(s,'room','shelter')
  s=f('next_day',s)
  self.assertEqual((s['day'],s['mother']),(2,'M2'))
  self.assertIn('piko',dict(f('available',s)))
  self.assertNotIn('오늘 아내와',f('action_lines',s,'piko')[0][1])
 def test_no_forgery_or_granny_import(self):
  text=(Path(__file__).parent/'recommended_opening_ui.rpy').read_text()
  self.assertNotIn('r13_carriage\n',text)
  self.assertNotIn('할머니',text)
  self.assertNotIn('위조',text)
 def test_entry_requires_earned_documents(self):
  with self.assertRaises(ValueError):f('opening_present',f('opening_state'),['entry_original','entry_list'])

class FamilyGoalTests(unittest.TestCase):
 def test_reunion_changes_goal_and_requires_actual_road_check(self):
  s=act(f('opening_state'),'entry_report','entry_original','entry_present','entry_inn','repair','records','contact','delivery_wait','reply','meet')
  self.assertIn('셋이',f('main_objective',s))
  self.assertNotIn('어디에',f('main_objective',s))
  s=f('evening',s);s=act(s,'room','shelter')
  self.assertIn('까로',f('main_objective',s))
  s=act(s,'family_route')
  self.assertIn('고갯길',f('main_objective',s))
  self.assertIn('family_travel',s['facts'])

class HearingKnowledgeTests(unittest.TestCase):
 def test_manifest_step_never_claims_unearned_altar_visit(self):
  s=f('e456_admin_seed',6)
  step=f('e456_hearing',s)[4]
  self.assertNotIn('가 보았습니다',str(step))
  self.assertNotIn('확인한 겁니다',str(step))
