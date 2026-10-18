"""Exact evidence, atomic arguments, shared three-error limit and legacy isolation."""
import copy
import unittest
import test_q1_arguments as base
from test_q1_review import block

class Q1Difficulty(unittest.TestCase):
    def setUp(self):
        f=base.Q1Arguments();f.setUp()
        self.e=f.e;self.store=f.store;self.grant=f.grant;self.press=f.press
        self.e['ROOM13'].setdefault('evidence_sources',{})
        exec(block('systems/room13_q1_difficulty.rpy','init 192 python:\n'),self.e)
        self.store.room13['q1_rules']=3

    def present(self,sid,key,choices=None):
        result,_=self.e['r13_debate_judge']('Q1',sid,key)
        if result=='half':self.e['r13_debate_half']('Q1',sid,key)
        elif result=='break':
            self.assertTrue(self.e['r13_q1_prepare_counter'](sid,key))
            rounds=self.e['r13_debate_statement']('Q1',sid)['counter']['rounds']
            outcome,_=self.e['r13_q1_commit_counter'](sid,choices or ['correct']*len(rounds))
            if outcome=='correct':self.e['r13_debate_mark']('broken','Q1',sid)
            return outcome
        else:self.e['r13_q1_reject_evidence'](sid,key,result)
        return result

    def ready(self):return self.e['r13_debate_ready']('Q1')
    def done(self,sid):return self.e['r13_q1_done'](sid)
    def errors(self):return self.e['r13_q1_formal_errors']()
    def scope(self):
        self.press('v_permission');self.assertFalse(self.ready())
        self.press('h_work');self.assertIn('L21',self.store.room13['evidence'])
        self.assertEqual(self.present('h_scope','L21'),'half')
        self.assertEqual(self.present('h_scope','L22'),'correct')
        self.press('v_permission');self.assertTrue(self.ready())

    def test_physical_requires_trace_time_user_action_and_authority(self):
        self.grant(['L04','L07','L15','L16'],'test')
        for sid,key in [('v_trace','L04'),('v_trace','L07'),('v_recent','L15')]:self.present(sid,key)
        self.press('v_user');self.present('v_action','L16')
        self.scope();self.assertEqual(self.errors(),0)
        self.assertNotIn('L09',self.store.room13['evidence'])

    def test_trade_requires_source_transaction_ownership_acquisition_and_authority(self):
        self.grant(['L09','L18','L19'],'test')
        for sid,key in [('v_origin','L09'),('v_trade','L19'),('v_trade','L18'),('v_own','L19')]:self.present(sid,key)
        self.press('h_work');self.assertNotIn('L21',self.store.room13['evidence'])
        self.press('v_where');self.present('v_slip','L20');self.scope()
        self.assertNotIn('L16',self.store.room13['evidence'])

    def test_witnesses_require_identity_action_same_event_continuity_and_authority(self):
        self.grant(['L16','L17'],'test')
        self.assertFalse(self.e['r13_q1_node_open'](self.e['r13_debate_statement']('Q1','v_action')))
        self.present('v_identity','L17');self.present('v_action','L16')
        self.press('h_work');self.assertNotIn('L21',self.store.room13['evidence'])
        self.present('v_link','L16');self.present('v_link','L17');self.scope()
        self.assertNotIn('L09',self.store.room13['evidence'])

    def test_second_round_failure_awards_no_partial_proof(self):
        self.grant(['L16','L17'],'test')
        self.present('v_identity','L17');self.present('v_action','L16')
        self.present('v_link','L16')
        self.assertEqual(self.present('v_link','L17',['correct','first']),'wrong')
        self.assertFalse(self.done('v_link'));self.assertFalse(self.ready());self.assertEqual(self.errors(),1)
        self.assertNotIn('v_link',self.store.room13['q1_argument_proofs'])
        self.assertEqual(self.present('v_link','L17'),'correct');self.assertEqual(self.errors(),1)

    def test_evidence_and_interpretation_share_limit_across_routes(self):
        self.grant(['L17','L09','L06'],'test')
        self.present('v_identity','L06');self.assertEqual(self.errors(),1)
        self.present('v_identity','L17',['first']);self.assertEqual(self.errors(),2)
        self.present('v_origin','L09',['second']);self.assertEqual(self.errors(),3)
        self.assertTrue(self.e['r13_debate_closed']('Q1'))
        self.assertFalse(self.e['r13_q1_prepare_counter']('v_identity','L17'))
        self.assertFalse(self.e['r13_q1_record_error']({'failed':'extra'}));self.assertEqual(self.errors(),3)
        self.assertIn('세 번',str(self.e['r13_q1_summary']()))

    def test_prepare_requires_exact_evidence_and_paired_distinct_records(self):
        self.grant(['L04','L07','L17'],'test')
        self.assertFalse(self.e['r13_q1_prepare_counter']('v_identity','L04'))
        self.assertEqual(self.present('v_trace','L04'),'half')
        self.assertEqual(self.present('v_trace','L04'),'half')
        self.assertFalse(self.e['r13_q1_prepare_counter']('v_trace','L04'))
        self.assertFalse(self.done('v_trace'));self.assertEqual(self.errors(),0)

    def test_invalid_stale_duplicate_and_unowned_submissions_do_not_commit(self):
        commit=self.e['r13_q1_commit_counter'];prepare=self.e['r13_q1_prepare_counter']
        self.assertEqual(commit('v_identity',['correct'])[0],'invalid')
        self.grant(['L17','L09'],'test');self.assertTrue(prepare('v_identity','L17'))
        self.assertEqual(commit('v_origin',['correct'])[0],'invalid')
        self.assertEqual(commit('v_identity',[])[0],'invalid')
        self.store.room13['q1_argument_pending']['supports']=['L09']
        self.assertEqual(commit('v_identity',['correct'])[0],'invalid')
        prepare('v_identity','L17');self.store.room13['evidence'].remove('L17')
        self.assertEqual(commit('v_identity',['correct'])[0],'invalid')
        self.grant(['L17'],'test');prepare('v_identity','L17')
        self.assertEqual(commit('v_identity',['correct'])[0],'correct')
        self.assertEqual(commit('v_identity',['first'])[0],'invalid');self.assertEqual(self.errors(),0)

    def test_evaluation_is_pure_and_withdrawal_does_not_cost_error(self):
        self.grant(['L17'],'test');self.e['r13_q1_prepare_counter']('v_identity','L17')
        before=copy.deepcopy(self.store.room13)
        self.assertEqual(self.e['r13_q1_evaluate_counter']('v_identity',['first'])[0],'wrong')
        self.assertEqual(before,self.store.room13)
        self.e['r13_edit'](q1_argument_pending={});self.assertEqual(self.errors(),0)
        self.assertFalse(self.done('v_identity'))

    def test_question_and_already_proved_are_not_wrong_rebuttals(self):
        self.grant(['L17'],'test');self.present('v_identity','L17')
        self.present('v_identity','L17');self.assertEqual(self.errors(),0)
        self.e['r13_q1_reject_evidence']('h_work','L17','soft');self.assertEqual(self.errors(),0)

    def test_rules_two_saves_keep_previous_contract(self):
        self.store.room13['q1_rules']=2
        self.assertFalse(self.e['r13_q1_hard']())
        self.assertNotIn('h_scope',[s['id'] for s in self.e['r13_debate_statements']('Q1')])
        self.assertFalse(self.e['r13_q1_record_error']({}));self.assertEqual(self.errors(),0)

    def test_each_dynamic_choice_fits_existing_choice_component(self):
        for st in self.e['R13_Q1_HARD_ARGUMENTS']:
            for r in st.get('counter',{}).get('rounds',[]):
                for key,text in r['options']:self.assertLessEqual(len(text),24,(st['id'],text))

if __name__=='__main__':unittest.main()
