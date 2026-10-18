"""Actual production presentation, availability and completion integration.
Only unrelated presentation/UI/time endpoints are stubbed; no predicted corrected replies.
"""
import ast,copy,json,re,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(ns,path,name):
 lines=(ROOT/'game'/path).read_text().splitlines(True)
 start=next(i for i,s in enumerate(lines) if s.startswith('    def '+name+'('));end=start+1
 while end<len(lines) and (not lines[end].strip() or lines[end].startswith('        ')):end+=1
 exec(compile(textwrap.dedent(''.join(lines[start:end])),path,'exec'),ns)
class LetterContinuity(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13=dict(day=2,period=0,life_poc=True,case_state='pending',evidence=['M01'],flags=[],read_topics=[],done=[],resident_knowledge={},encounters=[]),r13_topic_shown=None)
  self.n=dict(store=self.store,winter_copy=copy,R13_CASE_DAY=7,R13_TRIAL_DAY=10,R13_NAMES={},ROOM13=json.loads((ROOT/'game/room13-content.json').read_text()),r13_note_encounter=lambda p:None,_r13_review_present=lambda *a:[],_r13_review_opening=lambda *a:[],r13_calendar_key=lambda p:'test',r13_topic_current_context=lambda k:None,r13_abs_time=lambda:4,r13_tick=lambda:None,r13_w2_action_done=lambda *a,**k:None)
  self.n['r13_has']=lambda k:k in self.s['flags']+self.s['evidence']
  self.n['r13_flag']=lambda *keys:self.s['flags'].extend(k for k in keys if k not in self.s['flags'])
  self.n['r13_grant']=lambda keys,source:self.s['evidence'].extend(k for k in keys if k not in self.s['evidence'])
  for name in ('r13_available','r13_finish_topic','r13_finish_action'):load(self.n,'room13_rules.rpy',name)
  for name in ('r13_mother_knowledge','r13_mother_remember_show','r13_present','r13_conversation_opening'):load(self.n,'systems/room13_review_knowledge.rpy',name)
  # Evaluate actual authored sealed-envelope specs, not test-authored equivalents.
  source=(ROOT/'game/systems/room13_use_knowledge.rpy').read_text().split('init 123 python:\n',1)[1].split('\nlabel ',1)[0]
  tree=ast.parse(textwrap.dedent(source))
  for node in tree.body:
   code=ast.unparse(node)
   if code.startswith("ROOM13['activities']['warning_keep'] =") or code.startswith("ROOM13['topics'].update("):
    exec(compile(ast.Module(body=[node],type_ignores=[]),'real-envelope-specs','exec'),self.n)
  # Actual cost override: no time tick required for reading an already located envelope.
  source=(ROOT/'game/systems/room13_poc_route.rpy').read_text()
  self.assertIn('ROOM13["activities"]["warning"]["cost"]=0',source)
  self.n['ROOM13']['activities']['warning']['cost']=0
 @property
 def s(self):return self.store.room13
 def test_m01_opens_same_day_location_topic_without_awarding_unread_letter(self):
  for day in (1,2,3):
   with self.subTest(day=day):
    self.s.update(day=day,flags=[],evidence=['M01'],resident_knowledge={})
    rows=self.n['r13_present']('resident_lamplighter','M01')
    self.assertIn('topic:lamplighter_warning',self.s['flags'])
    self.assertTrue(self.n['r13_available'](self.n['ROOM13']['topics']['lamplighter_warning']))
    self.assertNotIn('E18',self.s['evidence'])
    self.assertNotRegex(str(rows),'내일|모레|3일')
    self.assertIn('오시기 전에',str(rows));self.assertIn('광장 등 밑 점검함',str(rows));self.assertIn('warning_location',self.s['flags']);self.assertNotIn('lamplighter_warning',self.s['read_topics'])
 def test_unknown_or_unowned_record_does_not_unlock(self):
  self.s['evidence']=[];self.n['r13_present']('resident_lamplighter','M01')
  self.assertNotIn('topic:lamplighter_warning',self.s['flags'])
 def test_old_promised_save_reopens_today_without_wait(self):
  self.s['flags']=['mother_letter_promised']
  rows=self.n['r13_conversation_opening']('resident_lamplighter',False)
  self.assertIn('topic:lamplighter_warning',self.s['flags']);self.assertIn('warning_location',self.s['flags']);self.assertNotRegex(str(rows),'3일|내일')
 def test_direct_read_needs_location_and_grants_once_same_day(self):
  spec=self.n['ROOM13']['activities']['warning']
  self.assertFalse(self.n['r13_available'](spec))
  self.s['flags'].append('topic:lamplighter_warning');self.n['r13_finish_topic']('lamplighter_warning')
  self.assertTrue(self.n['r13_available'](spec));before=(self.s['day'],self.s['period'])
  self.n['r13_finish_action']('warning');self.n['r13_finish_action']('warning')
  self.assertEqual(self.s['evidence'].count('E18'),1);self.assertEqual((self.s['day'],self.s['period']),before)
 def test_sealed_branches_available_today_only_after_collection(self):
  for key in ('warning_open_with','warning_open_alone'):
   self.assertFalse(self.n['r13_available'](self.n['ROOM13']['topics'][key]))
  self.s['flags'].append('warning_location')
  self.assertTrue(self.n['r13_available'](self.n['ROOM13']['activities']['warning_keep']))
  self.n['r13_finish_action']('warning_keep');self.assertNotIn('E18',self.s['evidence'])
  for key in ('warning_open_with','warning_open_alone'):
   self.assertTrue(self.n['r13_available'](self.n['ROOM13']['topics'][key]))
  self.n['r13_finish_topic']('warning_open_with')
  self.assertIn('J18',self.s['evidence']);self.assertIn('E18',self.s['evidence'])
  self.assertFalse(self.n['r13_available'](self.n['ROOM13']['topics']['warning_open_alone']))
 def test_received_save_never_reverts_to_wait_or_grants_duplicate(self):
  self.s['evidence'].append('E18');rows=self.n['r13_present']('resident_lamplighter','M01')
  self.assertNotRegex(str(rows),'내일|모레|3일');self.assertEqual(self.s['evidence'].count('E18'),1)
 def test_post_visit_requires_read_letter_not_a_direction_sighting(self):
  source=(ROOT/'game/systems/room13_question_discovery.rpy').read_text()
  literal=re.search(r'    R13_QUESTION_LEADS = (\{.*?\n    \})',source,re.S).group(1)
  self.n['R13_QUESTION_LEADS']=ast.literal_eval(literal)
  for name in ('r13_question_lead_known','r13_question_discovered'):
   load(self.n,'systems/room13_question_discovery.rpy',name)
  self.s['evidence'].append('J02')
  self.assertFalse(self.n['r13_question_discovered']('intro:post_visit',{}))
  self.s['evidence'].append('E18')
  self.assertTrue(self.n['r13_question_discovered']('intro:post_visit',{}))
  self.s['evidence']=[];self.s['read_topics']=['intro:post_visit']
  self.assertTrue(self.n['r13_question_discovered']('intro:post_visit',{}))
 def test_letter_route_can_identify_family_at_post_without_j02(self):
  self.s['evidence']=['M01','E01','E18'];self.n['_r13_intro_present']=lambda *a:[]
  load(self.n,'systems/room13_intro_clues.rpy','r13_present')
  for key in ('E01','M01'):self.n['r13_present']('seryeon',key)
  self.assertIn('intro:post_letter',self.s['flags']);self.assertIn('intro:post_memo',self.s['flags'])
  source=(ROOT/'game/systems/room13_intro_clues.rpy').read_text()
  self.assertIn('need=["intro:post_letter","intro:post_memo"]',source)
  self.assertNotIn('우선 우체국 쪽에서 아내가 들른 흔적을 찾아보겠습니다.',source)

 def test_chronology_is_conditional_and_granny_followup_not_a_second_wait(self):
  night=(ROOT/'game/systems/room13_first_day_flow.rpy').read_text()
  self.assertNotIn('엄마도 우리가 올 걸 알고 있었어',night)
  self.assertIn('혹시 우리가 오면 이 방을 찾을 거라고 생각했나 봐',night)
  route=(ROOT/'game/systems/room13_poc_route.rpy').read_text()
  self.assertIn('title="아내는 쓴 적 없다는데, 그 편지는 누가 썼습니까?",day=[2,4],need=["poc:letter_conflict","warning_exposed"]',route)

if __name__=='__main__':unittest.main()
