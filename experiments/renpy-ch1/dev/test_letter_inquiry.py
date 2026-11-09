"""문서의 제시 순서·보유·응답 완료를 실제 바인딩으로 확인한다."""
import copy,json,unittest
from types import SimpleNamespace
from test_play_review_field import load_function,ROOT

class LetterInquiry(unittest.TestCase):
    def env(self,values=None):
        state=SimpleNamespace(room13=dict(day=2,location='square',v111=dict(gate='chorong_documents2',scene='MS14_D02_S01',values=values or {}),evidence=['V111:E01','V111:E06','V111:E03']))
        env=dict(store=state,R13_V111_BINDINGS=json.loads((ROOT/'game/v111/field-bindings.json').read_text()),r13_v111_value=lambda key:state.room13['v111']['values'].get(key))
        for name in ('r13_v111_binding','r13_v111_direct_topic','r13_v111_present_index'):
            load_function('game/room13_v111.rpy',name,env)
        return env,state

    def test_either_owned_document_can_start_and_each_response_only_closes_its_own_topic(self):
        for first,flag in [('V111:E01','chorong_invitation_checked2'),('V111:E06','chorong_memo_checked2')]:
            with self.subTest(first=first):
                env,state=self.env();before=copy.deepcopy(state.room13);b=env['r13_v111_binding']()
                self.assertEqual({o['present'] for o in b['options']},{'V111:E01','V111:E06'})
                self.assertIsNotNone(env['r13_v111_present_index'](b,'resident_lamplighter',first))
                self.assertEqual(state.room13,before)
                state.room13['v111']['values'][flag]=True;b=env['r13_v111_binding']()
                self.assertEqual([o['present'] for o in b['options']],[k for k in ('V111:E06','V111:E01') if k!=first])
                self.assertIsNone(env['r13_v111_present_index'](b,'resident_lamplighter',first))

    def test_wrong_owner_unowned_or_other_record_does_not_match_a_document_reply(self):
        env,state=self.env();b=env['r13_v111_binding']();before=copy.deepcopy(state.room13)
        for person,key in [('granny','V111:E01'),('resident_lamplighter','V111:E03'),('resident_lamplighter','V111:E27'),('resident_lamplighter',None)]:
            self.assertIsNone(env['r13_v111_present_index'](b,person,key))
        self.assertEqual(state.room13,before)
        state.room13['evidence'].remove('V111:E06')
        self.assertIsNone(env['r13_v111_present_index'](b,'resident_lamplighter','V111:E06'))

    def test_presentation_goes_directly_to_the_common_record_picker(self):
        env,_=self.env();b=env['r13_v111_binding']()
        self.assertEqual(env['r13_v111_direct_topic']('chorong_documents2','resident_lamplighter','square',b['options'],[]),'present')
        self.assertIsNone(env['r13_v111_direct_topic']('chorong_documents2','granny','square',b['options'],[]))

class InquiryFollowups(unittest.TestCase):
    def env(self,gate,values=None):
        env,state=LetterInquiry().env(values)
        env['r13_v111_owned']=lambda key:'V111:'+key in state.room13['evidence']
        state.room13['v111']['gate']=gate
        state.room13['location']='gate' if gate=='gate_investigate' else 'square'
        return env,state

    def test_gate_application_requires_owned_original_and_is_removed_only_after_reply(self):
        env,state=self.env('gate_investigate');binding=env['r13_v111_binding']()
        original=next(o for o in binding['options'] if o['index']==3)
        self.assertTrue(original['present_only'])
        self.assertEqual(env['r13_v111_present_index'](binding,'guard','V111:E03'),3)
        state.room13['evidence'].remove('V111:E03')
        self.assertIsNone(env['r13_v111_present_index'](binding,'guard','V111:E03'))
        state.room13['v111']['values']['gate_application_acknowledged']=True
        after=env['r13_v111_binding']()
        self.assertNotIn(3,[o['index'] for o in after['options']])
        self.assertIn(5,[o['index'] for o in after['options']])

    def test_followups_require_both_answers_and_each_disappears_independently(self):
        for flags in ({},{'chorong_memo_checked2':True},{'chorong_invitation_checked2':True}):
            env,_=self.env('go_box',flags)
            self.assertEqual([o['index'] for o in env['r13_v111_binding']()['options']],[0])
        env,state=self.env('go_box',{'chorong_memo_checked2':True,'chorong_invitation_checked2':True})
        self.assertEqual([o['index'] for o in env['r13_v111_binding']()['options']],[0,1,2])
        state.room13['v111']['values']['chorong_scope_asked2']=True
        self.assertEqual([o['index'] for o in env['r13_v111_binding']()['options']],[0,1])
        state.room13['v111']['values']['chorong_secrecy_asked2']=True
        self.assertEqual([o['index'] for o in env['r13_v111_binding']()['options']],[0])
