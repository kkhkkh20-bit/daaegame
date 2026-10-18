"""Independent winning arguments, limits of observation, and legacy save isolation."""
import copy
import itertools
import unittest
import test_q1_review as legacy
from test_q1_review import block


class Q1Arguments(unittest.TestCase):
    def setUp(self):
        fixture=legacy.Q1Review();fixture.setUp()
        self.e=fixture.e;self.store=fixture.store
        self.e['r13_flag']=self.flag
        self.e['r13_grant']=self.grant
        self.e.update(R13_CONTACT_RECORDS={},r13_contact_presentations=lambda p:[])
        exec(block('systems/room13_q1_arguments.rpy','init 191 python:\n'),self.e)
        self.store.room13.update(q1_rules=2,flags=['lt_dawn','lt_open'],arguments={})

    def flag(self,*keys):
        self.store.room13['flags']=list(dict.fromkeys(self.store.room13['flags']+list(keys)))

    def grant(self,keys,source):
        self.store.room13['evidence']=list(dict.fromkeys(self.store.room13['evidence']+list(keys)))

    def present(self,sid,key,counter=True):
        result,lines=self.e['r13_debate_judge']('Q1',sid,key)
        if result=='half':self.e['r13_debate_half']('Q1',sid,key)
        elif result=='break' and counter:self.e['r13_debate_mark']('broken','Q1',sid)
        return result

    def press(self,sid):
        self.e['r13_q1_press_done'](sid)

    def ready(self):return self.e['r13_debate_ready']('Q1')

    def test_physical_path_without_warehouse_or_transactions(self):
        self.grant(['L04','L07','L15','L16'],'fixture')
        for first,second in [('L04','L07'),('L07','L04')]:
            self.store.room13['debate']={}
            self.assertEqual(self.present('v_trace',first),'half')
            self.assertEqual(self.present('v_trace',second),'break')
            self.present('v_recent','L15');self.press('v_user')
            self.present('v_action','L16')
            self.assertFalse(self.ready())
            self.press('v_permission');self.assertTrue(self.ready())
            self.assertNotIn('L09',self.store.room13['evidence'])

    def test_trade_path_without_rope_or_witnesses(self):
        self.grant(['L09','L18','L19'],'fixture')
        for sid,key in [('v_origin','L09'),('v_trade','L18'),('v_trade','L19'),('v_own','L19')]:self.present(sid,key)
        self.assertFalse(self.ready())
        self.assertNotIn('L20',self.store.room13['evidence'])
        self.press('v_where');self.assertIn('L20',self.store.room13['evidence'])
        self.present('v_slip','L20',counter=False);self.assertFalse(self.ready())
        self.present('v_slip','L20');self.press('v_permission');self.assertTrue(self.ready())

    def test_testimony_path_requires_event_connection_and_scope(self):
        self.grant(['L16','L17'],'fixture')
        self.present('v_action','L16');self.present('v_identity','L17')
        self.press('v_permission');self.assertFalse(self.ready())
        self.present('v_link','L16');self.assertFalse(self.ready())
        self.present('v_link','L17',counter=False);self.assertFalse(self.ready())
        self.present('v_link','L17');self.press('v_permission');self.assertTrue(self.ready())

    def test_paths_combine_without_route_selection_or_order_lock(self):
        self.grant(['L04','L07','L15','L16','L17'],'fixture')
        for sid,key in [('v_trace','L04'),('v_trace','L07'),('v_recent','L15'),('v_identity','L17'),('v_action','L16'),('v_link','L17'),('v_link','L16')]:self.present(sid,key)
        self.press('v_permission');self.assertTrue(self.ready())
        self.assertFalse(self.e['r13_q1_done']('v_user'))

    def test_every_independent_evidence_set_can_win_without_others(self):
        for order in itertools.permutations([('v_action','L16'),('v_identity','L17')]):
            self.store.room13['debate']={};self.store.room13['evidence']=['L16','L17']
            for sid,key in order:self.present(sid,key)
            self.present('v_link','L17');self.present('v_link','L16');self.press('v_permission')
            self.assertTrue(self.ready())

    def test_inventory_alone_repetition_and_unsupported_accusations_do_not_win(self):
        self.grant(['L04','L07','L08','L09','L15','L16','L17','L18','L19','L20'],'fixture')
        self.assertFalse(self.ready())
        self.press('v_permission');self.press('v_where');self.assertFalse(self.ready())
        self.assertEqual(self.present('v_trace','L04'),'half')
        self.assertEqual(self.present('v_trace','L04'),'half')
        self.assertFalse(self.e['r13_q1_done']('v_trace'))
        self.assertEqual(self.present('v_action','L08'),'soft')
        self.assertNotEqual(self.present('v_slip','L20'),'break')

    def test_judge_is_pure_and_rejects_unowned_and_locked_records(self):
        before=copy.deepcopy(self.store.room13)
        self.assertEqual(self.e['r13_debate_judge']('Q1','v_origin','L09')[0],'soft')
        self.assertEqual(self.store.room13,before)
        self.grant(['L06'],'fixture');self.assertEqual(self.present('v_action','L06'),'soft')
        self.assertFalse(self.ready())

    def test_old_in_progress_saves_and_other_cases_keep_their_rules(self):
        del self.store.room13['q1_rules']
        self.store.room13['debate']['broken']['Q1']=['s1']
        self.e['r13_q1_activate']()
        self.assertEqual(self.store.room13['q1_rules'],1)
        self.assertEqual(self.e['r13_debate_statements']('Q1')[0]['id'],'s1')
        self.assertFalse(self.e['r13_debate_ready']('C1'))
        self.store.room13={'day':1,'flags':[],'evidence':[],'debate':{},'propositions':[]}
        self.e['r13_q1_activate']();self.assertEqual(self.store.room13['q1_rules'],3)
        self.assertFalse(self.ready())

    def test_discovery_and_public_evidence_do_not_require_rope(self):
        self.flag('lt_siluk_seen')
        self.assertTrue(self.e['r13_q1_topic_available']('q1v:receipt'))
        self.assertFalse(self.e['r13_q1_topic_available']('q1v:removal'))
        self.grant(['L15'],'fixture');self.assertTrue(self.e['r13_q1_topic_available']('q1v:removal'))
        self.grant(['L09'],'fixture')
        before=copy.deepcopy(self.store.room13)
        self.assertIn('L09',self.e['r13_contact_presentations']('resident_madam'))
        self.assertEqual(before,self.store.room13)
        self.e['r13_present']('resident_madam','L09')
        self.assertIn('L18',self.store.room13['evidence'])
        before=copy.deepcopy(self.store.room13);self.e['r13_present']('resident_madam','L09');self.assertEqual(before,self.store.room13)

    def test_success_review_never_requires_unused_paths_and_hints_are_optional(self):
        self.flag('lt_done','lt_solved','tok_cleared')
        self.assertTrue(all(done for _,done,_ in self.e['r13_q1_review_rows']()))
        self.assertNotIn('입증하지 못한',str(self.e['r13_q1_summary']()))
        before=copy.deepcopy(self.store.room13)
        for _ in range(3):self.assertIsNone(self.e['r13_debate_hint_due']('Q1','v_trace'))
        self.assertEqual(before,self.store.room13)

    def test_missed_deadline_is_not_reported_as_a_failed_argument(self):
        self.flag('lt_done','tok_detained');self.store.room13['period']=2
        summary=str(self.e['r13_q1_summary']())
        self.assertIn('기한',summary);self.assertNotIn('실룩',summary)

if __name__=='__main__':unittest.main()
