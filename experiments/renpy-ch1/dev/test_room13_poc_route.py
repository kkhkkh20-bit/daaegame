"""Owned evidence, observed work, free pickup and first-three-day economy boundaries."""
import r13_timeline_env  # noqa: F401  날짜표 상수 (game/systems/room13_timeline.rpy)
import copy,json,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PocRouteTest(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13=dict(life_poc=True,day=2,period=0,case_state='pending',flags=[],evidence=[],read_topics=[],done=[],livelihood={}))
  self.data=json.loads((ROOT/'game/room13-content.json').read_text());self.data['topics']['intro:lamplighter_mother']={'day':[2,3]};self.data['topics']['intro:post_visit']={'day':[2,3]};self.data['topics']['intro:direction']={'day':[1,3]}
  s=self.store
  def has(k):return k in s.room13['flags'] or k in s.room13['evidence']
  def flag(*keys):s.room13['flags']=list(dict.fromkeys(s.room13['flags']+list(keys)))
  def present(person,key,identity=False):
   if key=='E18' and person=='granny' and has(key):flag('warning_exposed')
   return [('base','base response')]
  def topics(person):return [(k,t) for k,t in self.data['topics'].items() if t.get('npc')==person and all(has(n) for n in t.get('need',[]))]
  self.ns=dict(store=s,winter_copy=copy,ROOM13=self.data,R13_RECORD_SHORT={},r13_has=has,r13_flag=flag,r13_topics=topics,r13_present=present,
   r13_compare_result=lambda selected:'base comparison',r13_intro_goal=lambda:'base goal',r13_campaign_goal=lambda:'base goal',
   r13_learning_job_context=lambda key,state=None:'base job',r13_first_mystery_notes=lambda:[dict(title='base note')])
  exec(textwrap.dedent((ROOT/'game/systems/room13_livelihood_model.rpy').read_text().split('init 91 python:\n')[1]),self.ns)
  exec(textwrap.dedent((ROOT/'game/systems/room13_poc_route.rpy').read_text().split('init 100 python:\n')[1].split('\nlabel r13_poc_night_review:')[0]),self.ns)
 def test_work_opens_followup_only_after_owned_note_presentation(self):
  # 0.18.91: no jobs; showing the owned note is enough to open the follow-up question.
  s=self.store.room13;s['evidence']=['M01']
  self.assertNotIn('poc:nabi_packet',[k for k,t in self.ns['r13_topics']('nabi')])
  self.ns['r13_present']('nabi','M01');self.assertNotIn('J04',s['evidence'])
  self.assertIn('poc:nabi_packet',[k for k,t in self.ns['r13_topics']('nabi')]);self.assertNotIn('J04',s['evidence'])
  self.assertEqual(self.data['topics']['poc:nabi_packet']['give'],['J04'])
 def test_previous_work_is_recognized_without_new_trust_flags(self):
  s=self.store.room13;s.update(day=3,evidence=['M01']);s['livelihood']['jobs']=[dict(day=2,key='delivery')]
  self.ns['r13_present']('karo','M01');self.assertIn('poc:karo_box',[k for k,t in self.ns['r13_topics']('karo')]);self.assertNotIn('J05',s['evidence'])
 def test_witness_presentations_open_same_day_without_granting_letter(self):
  s=self.store.room13
  for day in (2,3):
   for key in ('J04','J05'):
    with self.subTest(day=day,key=key):
     s.update(day=day,evidence=[key],flags=[])
     rows=self.ns['r13_present']('resident_lamplighter',key)
     self.assertIn('topic:lamplighter_warning',s['flags']);self.assertNotIn('E18',s['evidence'])
     self.assertNotRegex(str(rows),'내일|모레|3일')
     before=copy.deepcopy(s);self.ns['r13_present']('resident_lamplighter',key);self.assertEqual(s,before)
  s.update(day=2,evidence=[],flags=[]);before=copy.deepcopy(s)
  self.assertEqual(self.ns['r13_present']('resident_lamplighter','J04'),[('base','base response')]);self.assertEqual(s,before)
 def test_letter_comparison_requires_both_owned_and_presentation_preserves_disclosure(self):
  s=self.store.room13;s['day']=3;s['evidence']=['E01'];self.assertEqual(self.ns['r13_compare_result'](['E01','E18']),'base comparison');self.assertNotIn('poc:letter_conflict',s['flags'])
  s['evidence'].append('E18');self.ns['r13_compare_result'](['E01','E18']);self.assertIn('poc:letter_conflict',s['flags'])
  self.assertNotIn('poc:granny_letter',[k for k,t in self.ns['r13_topics']('granny')]);self.ns['r13_present']('granny','E18');self.assertIn('warning_exposed',s['flags']);self.assertIn('poc:granny_letter',[k for k,t in self.ns['r13_topics']('granny')]);self.assertNotIn('J06',s['evidence'])
 def test_old_saves_and_post_case_keep_original_routes(self):
  s=self.store.room13;s.update(evidence=['M01','E01','E18'],livelihood={'jobs':[{'key':'kitchen'}]},flags=['poc:note_shown:nabi'])
  for changes in ({'life_poc':False},{'life_poc':True,'case_state':'occurred'},{'case_state':'pending','day':8}):
   s.update(changes);self.assertNotIn('poc:nabi_packet',[k for k,t in self.ns['r13_topics']('nabi')]);self.assertEqual(self.ns['r13_compare_result'](['E01','E18']),'base comparison')
 def test_free_envelope_is_still_acquired_once_with_actual_finish_rule(self):
  self.assertEqual(self.data['activities']['warning']['cost'],0)
  ns=self.ns;s=self.store.room13;s.update(day=3,period=3)
  ns.update(r13_abs_time=lambda:11,r13_w2_action_done=lambda *a,**k:None)
  def grant(keys,source):s['evidence']=list(dict.fromkeys(s['evidence']+keys))
  ns['r13_grant']=grant;ns['r13_tick']=lambda:s.update(period=s['period']+1)
  source=(ROOT/'game/room13_rules.rpy').read_text().split('    def r13_finish_action(key):',1)[1].split('    def r13_mark(',1)[0]
  exec(textwrap.dedent('    def r13_finish_action(key):'+source),ns)
  ns['r13_finish_action']('warning');current=self.store.room13;self.assertEqual(current['period'],3);self.assertIn('E18',current['evidence']);before=copy.deepcopy(current);ns['r13_finish_action']('warning');self.assertEqual(current,before)
 def test_first_three_day_income_routes_and_debt_never_require_shop(self):
  # 0.18.91: no jobs and no lodging, so no debt ever builds up.
  settle=self.ns['r13_settle_lodging'];wallet=self.ns['r13_wallet']
  skipped=dict(day=2,period=2,flags=['livelihood_open']);skipped=settle(skipped);self.assertEqual(wallet(skipped)['debt'],0);self.assertEqual(skipped['period'],2)
 def test_shop_purchase_alone_or_unaccepted_gift_never_counts_as_help(self):
  # 0.18.91: help no longer gates the mother questions; checking it never writes state.
  s=self.store.room13;s['resident_help']=[dict(person='nabi',kind='purchase',completed=True)]
  before=copy.deepcopy(s);self.assertTrue(self.ns['r13_poc_helped']('nabi'));self.assertEqual(s,before)
 def test_accepted_help_opens_question_without_faking_work_or_granting_testimony(self):
  s=self.store.room13;s['evidence']=['M01'];s['resident_help']=[dict(person='nabi',kind='gift',item='requested_item',completed=True,day=2)]
  self.ns['r13_present']('nabi','M01');self.assertIn('poc:nabi_packet',[k for k,t in self.ns['r13_topics']('nabi')]);self.assertFalse(self.ns['r13_poc_worked']('kitchen'));self.assertNotIn('J04',s['evidence']);self.assertEqual(self.ns['r13_wallet'](s)['jobs'],[])
 def test_world_menu_goal_queries_are_read_only(self):
  s=self.store.room13;s.update(day=3,period=2,evidence=['M01','J02']);before=copy.deepcopy(s)
  self.assertIn('내일 오전',self.ns['r13_poc_goal']());self.ns['r13_first_mystery_notes']();self.ns['r13_learning_job_context']('kitchen');self.assertEqual(s,before)
if __name__=='__main__':unittest.main()

