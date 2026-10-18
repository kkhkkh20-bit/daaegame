"""Protect acquisition/presentation boundaries and prevent legacy-route unlocks."""
import r13_timeline_env  # noqa: F401  날짜표 상수 (game/systems/room13_timeline.rpy)
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class IntroCluesTest(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13=dict(life_poc=True,day=2,case_state='pending',flags=[],evidence=[]))
  s=self.store
  def has(k):return k in s.room13['evidence'] or k in s.room13['flags']
  def flag(*keys):s.room13['flags']=list(dict.fromkeys(s.room13['flags']+list(keys)))
  self.ns=dict(store=s,ROOM13=dict(evidence={k:{} for k in ('E01','E03','M01')},evidence_sources={},topics={}),R13_RECORD_SHORT={},r13_has=has,r13_flag=flag,
   r13_compare_result=lambda x:'base',r13_present=lambda *a:'base',r13_conversation_topic_lines=lambda k:[],r13_topics=lambda p:[],r13_home_with_daram=lambda:True,r13_first_mystery_notes=lambda:[{}])
  exec(textwrap.dedent((ROOT/'game/systems/room13_intro_clues.rpy').read_text().split('init 97 python:\n')[1].split('\nscreen r13_entry_daram_topics():')[0]),self.ns)
 def test_comparison_requires_both_owned_records(self):
  f=self.ns['r13_compare_result'];s=self.store.room13
  self.assertEqual(f(['E01','M01']),'base');self.assertEqual(s['flags'],[])
  s['evidence']=['E01','M01'];self.assertIn('도토리',f(['M01','E01']));self.assertIn('mother_expected_family',s['flags']);self.assertIn('letter_no_acorn',s['flags'])
  before=copy.deepcopy(s);f(['E01','M01']);self.assertEqual(s,before)
 def test_testimony_requires_followup_read(self):
  f=self.ns['r13_present'];s=self.store.room13
  self.assertEqual(f('resident_lamplighter','M01'),'base');self.assertEqual(s['flags'],[])
  s['evidence']=['M01'];self.assertNotEqual(f('resident_lamplighter','M01'),'base')
  self.assertIn('intro:memo_shown',s['flags']);self.assertNotIn('J02',s['evidence'])
  t=self.ns['ROOM13']['topics']['intro:lamplighter_mother'];self.assertEqual(t['give'],['J02']);self.assertEqual(t['need'],['intro:memo_shown'])
 def test_post_identity_requires_two_separate_owned_presentations(self):
  f=self.ns['r13_present'];s=self.store.room13
  for entry in ('J02','E18'):
   for order in (('M01','E01'),('E01','M01')):
    with self.subTest(entry=entry,order=order):
     s.update(evidence=[entry,'E01','M01'],flags=[])
     f('seryeon',entry);self.assertEqual(s['flags'],[])
     first_flag='intro:post_memo' if order[0]=='M01' else 'intro:post_letter'
     f('seryeon',order[0]);self.assertEqual(s['flags'],[first_flag]);self.assertNotIn('J03',s['evidence'])
     before=copy.deepcopy(s);f('seryeon',order[0]);self.assertEqual(s,before)
     f('seryeon',order[1]);self.assertEqual(set(s['flags']),{'intro:post_letter','intro:post_memo'});self.assertNotIn('J03',s['evidence'])
     if entry=='E18':self.assertNotIn('J02',s['evidence'])
  t=self.ns['ROOM13']['topics']['intro:post_visit']
  self.assertEqual(set(t['need']),{'intro:post_memo','intro:post_letter'})
  self.assertEqual(t['give'],['J03'])
 def test_post_identity_cannot_substitute_ownership_for_actual_presentations(self):
  f=self.ns['r13_present'];s=self.store.room13
  for owned,shown in ((['E18','E01'],'M01'),(['E18','M01'],'E01'),(['E18'],'M01')):
   with self.subTest(owned=owned,shown=shown):
    s.update(evidence=owned,flags=[]);before=copy.deepcopy(s)
    self.assertEqual(f('seryeon',shown),'base');self.assertEqual(s,before)
  s.update(evidence=['E18','E01','M01'],flags=[])
  t=self.ns['ROOM13']['topics']['intro:post_visit']
  self.assertFalse(all(self.ns['r13_has'](key) for key in t['need']))
  f('seryeon','M01');self.assertFalse(all(self.ns['r13_has'](key) for key in t['need']))
  f('seryeon','E01');self.assertTrue(all(self.ns['r13_has'](key) for key in t['need']))
  self.assertNotIn('J03',s['evidence'])
 def test_legacy_and_later_case_do_not_unlock_intro(self):
  s=self.store.room13;s['evidence']=['M01'];s['life_poc']=False
  self.assertEqual(self.ns['r13_present']('resident_lamplighter','M01'),'base');self.assertEqual(s['flags'],[])
  s['life_poc']=True;s['case_state']='occurred';self.assertEqual(self.ns['r13_present']('resident_lamplighter','M01'),'base');self.assertEqual(s['flags'],[])
 def test_day_three_keeps_existing_envelope_unlock(self):
  s=self.store.room13;s['day']=3;s['evidence']=['M01']
  self.ns['_r13_intro_present']=lambda *a:self.ns['r13_flag']('topic:lamplighter_warning')
  self.ns['r13_present']('resident_lamplighter','M01')
  self.assertIn('topic:lamplighter_warning',s['flags']);self.assertIn('intro:memo_shown',s['flags'])
if __name__=='__main__':unittest.main()

