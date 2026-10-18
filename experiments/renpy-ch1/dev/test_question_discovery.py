"""Causal question gates and side-effect-free field contact decisions."""
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class QuestionDiscovery(unittest.TestCase):
 def setUp(self):
  self.s=types.SimpleNamespace(room13=dict(day=2,period=0,evidence=['E01'],flags=[],read_topics=[],resident_knowledge={}),r13_question_pending=None)
  topics={k:dict(npc='granny') for k in ['granny_letter','granny_rules','life:granny:work','alibi:night1:granny']}
  topics['life:resident_piko:work']=dict(npc='resident_piko')
  self.messages=[];self.calls=[]
  self.n=dict(store=self.s,R13_ALIBI={('night1','resident_kalbaram'):{'claim':[('dad','질문'),('resident_kalbaram','숲에 있었소.'),('resident_kalbaram','아이를 봤소.')]}},ROOM13={'topics':topics,'presentations':[]},config=types.SimpleNamespace(interact_callbacks=[],after_load_callbacks=[]),
   # This isolated discovery fixture has no live-topic layer; integration is tested separately.
   r13_topic_current_fresh=lambda key:False,
   r13_has=lambda k:k in self.s.room13['flags']+self.s.room13['evidence'],r13_edit=lambda **kw:self.s.room13.update(kw),
   r13_topics=lambda p:[(k,v) for k,v in topics.items() if v['npc']==p],r13_before_line=lambda *a:'line',r13_remember_line=lambda k:None,
   r13_conversation_topic_lines=lambda k:[('dad','날짜는요?'),('granny','날짜는 장부에 있어요.'),('dad','확인하겠습니다.')],
   r13_catalog_entries=lambda:[],r13_catalog_object=lambda k:None,r13_catalog_offer=lambda p,k:None,
   r13_met_people=lambda:['granny'],r13_conversation_opening=lambda p,f:[],r13_resident_notice=lambda p:[],R13_OPENING_SCENES={'first_meetings':{}},
   R13_NAMES={'granny':'할머니'},renpy=types.SimpleNamespace(notify=self.messages.append),
   r13_person_action=lambda p,entry=False:('enter',p),r13_offer_for_person=lambda p:None,R13_LIFE_GROUPS=[],Function=lambda f,*a:('notify',f,a))
  source=(ROOT/'game/systems/room13_question_discovery.rpy').read_text().split('init 190 python:\n',1)[1]
  exec(textwrap.dedent(source),self.n)
 def keys(self,p='granny'):return [k for k,_ in self.n['r13_topics'](p)]
 def test_initial_menu_does_not_know_guest_locks_or_first_night(self):
  self.assertEqual(self.keys(),['granny_letter']);self.s.room13['day']=3;self.assertEqual(self.keys(),['granny_letter'])
 def test_real_subject_unlocks_only_related_question(self):
  before=copy.deepcopy(self.s.room13);self.n['r13_question_learn']('topic:granny_letter','granny','눈에 길이 막혀 묵는 분이 늘어서요.')
  self.assertEqual(self.keys(),['granny_letter','life:granny:work'])
  for k in before:self.assertEqual(before[k],self.s.room13[k])
  self.n['r13_question_learn']('object:door',None,'안쪽에 빗장이 두 개 있다.');self.assertIn('granny_rules',self.keys())
 def test_dad_question_and_record_preview_do_not_invent_knowledge(self):
  for who,identity in [('dad','topic:x'),('granny','topic:review:x'),('granny','topic:record_full:x')]:
   self.n['r13_question_learn'](identity,who,'손님이 늘어서 이불이 모자라요.')
  self.assertEqual(self.keys(),['granny_letter'])
 def test_first_night_needs_actual_connection(self):
  self.s.room13['flags']=['night1_seen','tosil_errand_seen'];self.assertNotIn('alibi:night1:granny',self.keys())
  self.n['r13_question_learn']('topic:tosil:forest','resident_tosil','처음은 아저씨네 마차가 온 날 밤이었어요.')
  self.assertIn('alibi:night1:granny',self.keys())
 def test_mother_question_preserves_early_first_night_discovery(self):
  topic=self.n['ROOM13']['topics']['ask_mom:kalbaram']
  self.assertIn('아내',topic['title']);self.assertIn('lodging',topic['need'])
  self.assertFalse(self.n['r13_question_discovered']('kalbaram:edge',{}))
  self.n['r13_question_learn']('topic:ask_mom:kalbaram','resident_kalbaram','숲 끝 덫을 보고 내려왔소.')
  self.assertTrue(self.n['r13_question_discovered']('kalbaram:edge',{}))
  self.assertIn('alibi:night1:resident_kalbaram',topic['flags'])
  self.s.room13['read_topics']=['ask_mom:kalbaram'];self.assertIn('alibi:night1:granny',self.keys())
  self.assertFalse(self.n['r13_question_discovered']('alibi:night1:resident_kalbaram',{}))
 def test_partial_or_skipped_lines_do_not_unlock(self):
  s=self.s;s.r13_question_pending=('topic:granny_letter',0,'묵는 분이 늘어서요.');s.r13_packet=('granny','text');s.r13_read_id='line';s.r13_pages=['a','b'];s.r13_page_i=1;s.r13_conv_skip=False
  self.n['r13_remember_line']('line');self.assertEqual(self.keys(),['granny_letter'])
  s.r13_page_i=2;s.r13_conv_skip=True;self.n['r13_remember_line']('line');self.assertEqual(self.keys(),['granny_letter'])
  s.r13_conv_skip=False;self.n['r13_remember_line']('line');self.assertIn('life:granny:work',self.keys())
 def test_old_saves_preserve_read_topics_not_exposed_menu(self):
  self.s.room13['topic_order']={'granny':['granny_rules','alibi:night1:granny']};self.assertEqual(self.keys(),['granny_letter'])
  self.s.room13['read_topics']=['granny_rules'];self.assertIn('granny_rules',self.keys())
  self.s.room13['topic_transcripts']={'granny_letter':[['granny','묵는 분이 늘어서요.',False]]};self.n['r13_question_migrate']();self.assertIn('life:granny:work',self.keys())
 def test_empty_contact_stays_in_field_without_state_writes(self):
  self.s.room13['read_topics']=['granny_letter'];self.s.room13['resident_knowledge']={'granny':['E01:anonymous']};before=copy.deepcopy(self.s.room13)
  action=self.n['r13_person_action']('granny');self.assertEqual(action[0],'notify');action[1](*action[2]);self.assertIn('할머니',self.messages[-1]);self.assertEqual(before,self.s.room13)
 def test_owned_relevant_unshown_material_keeps_entry(self):
  self.s.room13['read_topics']=['granny_letter'];before=copy.deepcopy(self.s.room13)
  self.assertTrue(self.n['r13_contact_has_content']('granny'));self.assertEqual(before,self.s.room13)
  self.assertEqual(self.n['r13_person_action']('granny')[0],'enter')
 def test_new_use_of_previously_shown_record_remains_reachable(self):
  self.s.room13.update(day=3,evidence=['L00'],flags=['lt_lib_warned'],resident_knowledge={'resident_librarian':['L00:anonymous']})
  self.assertIn('L00',self.n['r13_contact_presentations']('resident_librarian'))
  self.s.room13['flags'].append('lt_lib_safe');self.assertNotIn('L00',self.n['r13_contact_presentations']('resident_librarian'))
  self.s.room13.update(evidence=['M01'],flags=[],resident_knowledge={'resident_lamplighter':['M01:anonymous']})
  self.assertIn('M01',self.n['r13_contact_presentations']('resident_lamplighter'))
 def test_events_entry_and_children_keep_dispatcher(self):
  self.s.room13['read_topics']=['granny_letter'];self.s.room13['evidence']=[]
  self.n['r13_offer_for_person']=lambda p:'event';self.assertEqual(self.n['r13_person_action']('granny')[0],'enter')
  self.n['r13_offer_for_person']=lambda p:None;self.assertEqual(self.n['r13_person_action']('granny',True)[0],'enter')
 def test_first_opening_predicts_cue_without_awarding_it(self):
  self.n['r13_met_people']=lambda:[];self.n['r13_conversation_opening']=lambda p,f:[('resident_piko','그림을 그리고 있어요.')]
  before=copy.deepcopy(self.s.room13);self.assertTrue(self.n['r13_contact_has_content']('resident_piko'));self.assertEqual(before,self.s.room13)
 def test_all_life_phases_have_subject_gates(self):
  for person in self.n['R13_WORK_CUES']:
   for phase in ['work','after','crisis']:self.assertIn('life:'+person+':'+phase,self.n['R13_QUESTION_LEADS'])
if __name__=='__main__':unittest.main()
