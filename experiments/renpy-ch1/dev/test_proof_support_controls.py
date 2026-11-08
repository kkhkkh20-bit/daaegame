"""자료창 보조 버튼의 외형 변경이 주 제출과 다른 화면에 번지지 않는지 확인한다."""
import ast
from pathlib import Path
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]


class ProofSupportControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=(ROOT/'game/room13_controls.rpy').read_text().split('init 110 python:',1)[1].split('\nscreen ',1)[0]
        tree=ast.parse(textwrap.dedent(source))
        wanted=[node for node in tree.body if (
            isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='R13_SOFT_SUPPORT_CONTROLS' for t in node.targets)
        ) or (isinstance(node,ast.FunctionDef) and node.name=='r13_control_soft_support')]
        env={}
        exec(compile(ast.Module(body=wanted,type_ignores=[]),'자료 보조 버튼 범위','exec'),env)
        cls.soft=staticmethod(env['r13_control_soft_support'])

    def test_proof_reading_and_return_actions_use_the_question_paper(self):
        for control in ('r13_pw_back_list','r13_pw_investigate','r13_pw_observe','r13_pw_press','r13_pw_origin','r13_pw_fold'):
            with self.subTest(control=control):self.assertTrue(self.soft(control))

    def test_fire_reading_and_return_actions_follow_the_same_rule(self):
        for control in ('r13_fire_words','r13_fire_site','r13_fire_sources','r13_fire_back','r13_fire_origin','r13_fire_press'):
            with self.subTest(control=control):self.assertTrue(self.soft(control))

    def test_submit_and_selection_controls_keep_their_existing_emphasis(self):
        for control in ('r13_pw_submit','r13_fire_submit','r13_fire_sources_submit','r13_pw_single','r13_pw_pair','r13_pw_tab_all','r13_fire_slot_0','r13_fire_choice_lamp','r13_fire_pick_E06_FIRE'):
            with self.subTest(control=control):self.assertFalse(self.soft(control))
        # 다른 호출처가 보조 ID를 주 행동으로 쓰더라도 빨간 주 행동 판을 보존한다.
        self.assertFalse(self.soft('r13_pw_origin',primary=True))

    def test_unrelated_shared_controls_are_unchanged(self):
        for control in (None,'r13_control_지도','r13_confirm_yes','r13_map_travel','r13_ev_present','r13_fire_unknown_future'):
            with self.subTest(control=control):self.assertFalse(self.soft(control))


if __name__=='__main__':unittest.main()
