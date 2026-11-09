"""현재 상대·자료·이미 들은 답을 바탕으로 조사 반응을 고른다."""
import ast
import copy
from pathlib import Path
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_inquiry_reactions.rpy'


class InquiryReactions(unittest.TestCase):
    def setUp(self):
        env={}
        source=SOURCE.read_text().split('init 350 python:\n',1)[1]
        exec(compile(ast.parse(textwrap.dedent(source)),'자료별 조사 반응','exec'),env)
        self.choose=env['r13_inquiry_reaction_block']

    def test_gate_records_have_distinct_scopes(self):
        for key,block in [('E01','gate_invitation_scope139'),('E02','gate_list_repeat139'),
                          ('E04','gate_rules_scope139'),('E30','gate_unfamiliar_record139')]:
            self.assertEqual(self.choose('gate_investigate','guard','V111:'+key,{}),block)

    def test_application_is_only_recalled_after_actual_acknowledgment(self):
        self.assertIsNone(self.choose('gate_investigate','guard','V111:E03',{}))
        self.assertIsNone(self.choose('gate_investigate','guard','V111:E03',{'gate_application_acknowledged':False}))
        self.assertEqual(self.choose('gate_investigate','guard','V111:E03',{'gate_application_acknowledged':True}),
                         'gate_application_repeat139')

    def test_chorong_does_not_replace_either_first_document_reply(self):
        for gate in ('chorong_documents2','go_box'):
            for key,other_flag in [('E01','chorong_memo_checked2'),('E06','chorong_invitation_checked2')]:
                self.assertIsNone(self.choose(gate,'resident_lamplighter','V111:'+key,{}))
                self.assertIsNone(self.choose(gate,'resident_lamplighter','V111:'+key,{other_flag:True}))

    def test_chorong_only_repeats_the_specific_document_already_checked(self):
        for gate in ('chorong_documents2','go_box'):
            self.assertEqual(self.choose(gate,'resident_lamplighter','V111:E06',{'chorong_memo_checked2':True}),
                             'chorong_memo_repeat139')
            self.assertEqual(self.choose(gate,'resident_lamplighter','V111:E01',{'chorong_invitation_checked2':True}),
                             'chorong_invitation_repeat139')
            self.assertEqual(self.choose(gate,'resident_lamplighter','V111:E03',{}),
                             'chorong_unfamiliar_record139')

    def test_other_places_or_people_keep_the_existing_reaction_system(self):
        for gate,person in [('gate_choice','guard'),('registered_menu','guard'),('gate_investigate','granny'),
                            ('lamp_rope','resident_lamplighter'),('go_box','guard'),('chorong_documents2','daram'),
                            ('post_menu','seryeon')]:
            self.assertIsNone(self.choose(gate,person,'V111:E01',{'chorong_invitation_checked2':True}))

    def test_cancel_or_non_record_is_not_a_new_reaction(self):
        for gate,person in [('gate_investigate','guard'),('chorong_documents2','resident_lamplighter')]:
            for shown in (None,False,'','E01','V111:',('present','V111:E01')):
                self.assertIsNone(self.choose(gate,person,shown,{}))

    def test_selection_never_mutates_the_callers_knowledge_or_returns_a_result(self):
        values={'gate_application_acknowledged':True,'chorong_memo_checked2':True,
                'chorong_invitation_checked2':True,'meeting:gate':None,'tries:gate':1,
                'elapsed_minutes':30,'owned':['V111:E01','V111:E06']}
        before=copy.deepcopy(values)
        for gate,person in [('gate_investigate','guard'),('chorong_documents2','resident_lamplighter'),
                            ('go_box','resident_lamplighter')]:
            for shown in ('V111:E01','V111:E02','V111:E03','V111:E04','V111:E06','V111:E30'):
                result=self.choose(gate,person,shown,values)
                self.assertTrue(result is None or isinstance(result,str))
        self.assertEqual(values,before)


if __name__=='__main__':unittest.main()
