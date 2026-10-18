"""First-case information boundaries, partial failure, continuity and checkpoint isolation."""
import copy
import textwrap
import types
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def block(file,marker):
    return textwrap.dedent((ROOT/'game'/file).read_text().split(marker,1)[1].split('\nlabel ',1)[0].split('\nscreen ',1)[0].split('\n# ===',1)[0])

class Q1Review(unittest.TestCase):
    def setUp(self):
        self.store=types.SimpleNamespace(room13=dict(day=4,period=0,evidence=[],flags=[],propositions=[],debate=dict(broken={},pressed={},misses={},closed={})),r13_q1_checkpoint_saved=False,r13_q1_checkpoint_failed=False)
        self.saves={};self.loaded=[]
        self.persistent=types.SimpleNamespace(r13_q1_results={},r13_mornings={})
        def save(slot,**kw):self.saves[slot]=copy.deepcopy(self.store.room13)
        def edit(**kw):self.store.room13.update(kw)
        e=self.e=dict(store=self.store,winter_copy=copy,persistent=self.persistent,r13_edit=edit,
            r13_has=lambda k:k in self.store.room13['flags']+self.store.room13['evidence'],
            ROOM13={k:{} for k in ('evidence','activities','topics')},R13_RECORD_SHORT={},R13_CONTEXT_ACTIVITIES={},R13_OBJECT_NAMES={},R13_TOPIC_LABELS={},R13_NIGHT_TALK_COND={},R13_EVENT_OFFERS={},R13_OFFER_ACTORS={},
            r13_topics=lambda p:[],r13_present=lambda *a:[],r13_meeting_cast=lambda *a:[],r13_meeting_plate=lambda *a:None,
            r13_first_mystery_notes=lambda:[],r13_conversation_opening=lambda *a:[],
            r13_morning_record=lambda:self.persistent.r13_mornings,
            renpy=types.SimpleNamespace(save=save,can_load=lambda slot:slot in self.saves,retain_after_load=lambda:None,save_persistent=lambda:None,load=lambda slot:self.loaded.append(slot),slot_json=lambda slot:dict(r13_day=self.saves[slot]['day']),notify=lambda *a:None))
        e['ROOM13']['objects']={'square':{}}
        exec(block('systems/room13_debate.rpy','init 98 python:\n'),e)
        exec(block('systems/room13_ep1_lamp_thief.rpy','init 152 python:\n'),e)
        exec(block('systems/room13_q1_review.rpy','init 181 python:\n'),e)
    def test_questions_only_use_discovered_facts_and_do_not_change_state(self):
        self.store.room13['flags']=['lt_dawn']
        before=copy.deepcopy(self.store.room13)
        notes=self.e['r13_q1_notes']()
        self.assertEqual(len(notes),1)
        self.assertNotIn('실룩',str(notes));self.assertNotIn('창고',str(notes))
        self.assertEqual(before,self.store.room13)
        self.store.room13['evidence']=['L04']
        self.assertEqual(self.e['r13_q1_notes']()[-1]['keys'],['L04'])
        self.assertNotIn('실룩',str(self.e['r13_q1_notes']()))
    def test_partial_evidence_still_opens_meeting(self):
        self.store.room13['evidence']=['L06']
        self.assertTrue(self.e['r13_debate_engageable']('Q1'))
        self.assertFalse(self.e['r13_debate_arguable']('Q1'))
    def test_number_note_never_invents_loan_and_rope_never_invents_child(self):
        j=self.e['r13_debate_judge']
        self.assertNotIn('지난주',str(j('Q1','s1','L03')))
        self.assertNotIn('진료소',str(j('Q1','s1','L03')))
        self.store.room13['evidence']=['L04','L07']
        self.assertEqual(j('Q1','s5','L07')[0],'break')
        self.assertNotIn('따님',str(j('Q1','s5','L07')))
    def test_rope_requires_both_observations_and_has_specific_soft_response(self):
        j=self.e['r13_debate_judge']
        self.store.room13['evidence']=['L07']
        self.assertEqual(j('Q1','s5','L07')[0],'soft')
        self.assertIn('직접 대조',str(j('Q1','s5','L07')))
        self.assertIn('뜯긴 자리',str(j('Q1','s5','L04')))
        self.assertIn('창고의 조각',str(j('Q1','s3','L04')))
        self.assertEqual(j('Q1','s1','L14')[0],'break')
        self.assertNotIn('공구 자국은 없습니다',str(j('Q1','s1','L14')))
    def test_partial_review_distinguishes_missing_evidence_and_unused_evidence(self):
        self.store.room13['flags']=['lt_dawn','lt_done','tok_detained']
        self.store.room13['evidence']=['L03','L06','L10']
        self.e['r13_debate_mark']('broken','Q1','s1')
        self.e['r13_debate_close']('Q1','partial')
        before=copy.deepcopy(self.store.room13)
        lines=str(self.e['r13_q1_review_lines']())
        self.assertIn('등을 연 사람',lines);self.assertIn('가지고 있던 자료',lines);self.assertIn('조사를 보완',lines)
        self.assertNotIn('L09',lines);self.assertNotIn('입구',lines)
        self.assertEqual(before,self.store.room13)
    def test_all_broken_without_conclusion_is_not_missing_evidence(self):
        self.store.room13['evidence']=['L03','L04','L06','L07','L09','L10']
        for sid in ('s1','s2','s3','s4','s5'):self.e['r13_debate_mark']('broken','Q1',sid)
        self.e['r13_debate_close']('Q1','partial')
        text=str(self.e['r13_q1_review_lines']())
        self.assertIn('결론을 확정하지 않았다',text)
        self.assertNotIn('조사를 보완',text)
    def test_deadline_does_not_reveal_unheard_suspects(self):
        self.store.room13['flags']=['lt_done','tok_detained']
        self.assertEqual(self.e['r13_q1_review_rows'](),[])
        self.assertIn('기한',str(self.e['r13_q1_summary']()))
        self.assertNotIn('실룩',str(self.e['r13_q1_summary']()))
    def test_aftermath_distinguishes_detention_release_and_returned_fragment(self):
        for flags,expect,absent in [(['tok_detained'],'끌려간','다시 넣었다'),(['tok_cleared','lt_solved'],'못 돌려받았어요','다시 넣었다'),(['tok_cleared','lt_solved','madam_store_opened'],'다시 넣었다','끌려간')]:
            self.store.room13['flags']=flags
            text=str(self.e['r13_q1_lamp_aftermath']())
            self.assertIn(expect,text);self.assertNotIn(absent,text)
        self.store.room13['flags']=['tok_detained']
        self.assertNotIn('실룩',str(self.e['r13_q1_afterthought']()))
    def test_native_checkpoint_preserves_full_state_and_does_not_overwrite_slots(self):
        self.store.room13.update(cash=7,run_token='run-a',records={'L04':{'source':'lamp'}})
        before=copy.deepcopy(self.store.room13)
        self.e['r13_q1_save_checkpoint']('meeting')
        slot=self.e['r13_q1_checkpoint_slot']('meeting')
        for k,v in before.items():self.assertEqual(self.saves[slot][k],v)
        self.store.r13_q1_checkpoint_saved=False
        self.e['r13_q1_save_checkpoint']('result')
        result=self.e['r13_q1_checkpoint_slot']('result')
        self.assertNotEqual(slot,result)
        self.assertEqual(len(self.saves),2)
        self.store.room13=copy.deepcopy(self.saves[slot])
        self.assertEqual(self.e['r13_q1_previous_result'](),result)
        self.e['r13_q1_restore_slot'](result)
        self.assertEqual(self.loaded,[result])
        self.store.room13['run_token']='new-run'
        self.assertIsNone(self.e['r13_q1_previous_result']())
    def test_save_failure_never_offers_missing_checkpoint(self):
        def fail(*a,**kw):raise OSError('disk full')
        self.e['renpy'].save=fail
        self.e['r13_q1_save_checkpoint']('meeting')
        self.assertTrue(self.store.r13_q1_checkpoint_failed)
        self.assertFalse(self.e['r13_q1_can_restore']('meeting'))

if __name__=='__main__':unittest.main()
