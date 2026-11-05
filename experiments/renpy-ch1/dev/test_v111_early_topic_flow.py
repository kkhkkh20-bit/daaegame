"""초반 두 대화의 생략 조건과 기존 자료 수신자 검증을 확인한다."""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EarlyTopicFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (ROOT / 'game/room13_v111.rpy').read_text()
        block = source.split('init 301 python:\n', 1)[1].split('\nlabel ', 1)[0]
        import textwrap
        tree = ast.parse(textwrap.dedent(block))
        names = {'r13_v111_direct_topic', 'r13_v111_present_index'}
        env = {}
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '초반 대화', 'exec'), env)
        cls.choose = staticmethod(env['r13_v111_direct_topic'])
        cls.present = staticmethod(env['r13_v111_present_index'])
        cls.env = env
        cls.bindings = json.loads((ROOT / 'game/v111/field-bindings.json').read_text())

    def options(self, gate):
        return [dict(o, index=o.get('index', i))
                for i, o in enumerate(copy.deepcopy(self.bindings[gate]['options']))]

    def test_empty_post_question_opens_picker_without_choosing_a_record(self):
        options = self.options('envelope_show')
        before = copy.deepcopy(options)
        self.assertEqual(self.choose('envelope_show', 'seryeon', 'post', options, []), 'present')
        self.assertEqual(options, before)

    def test_recipient_location_and_gate_must_all_match(self):
        options = self.options('envelope_show')
        for gate, person, location in [('envelope_show', 'guard', 'post'),
                                       ('envelope_show', 'seryeon', 'square'),
                                       ('post_menu', 'seryeon', 'post')]:
            with self.subTest(gate=gate, person=person, location=location):
                self.assertIsNone(self.choose(gate, person, location, options, []))

    def test_added_post_question_or_world_option_keeps_question_screen(self):
        options = self.options('envelope_show')
        followup = [('새로 열린 질문', SimpleNamespace(value=('followup', 'new')), False)]
        self.assertIsNone(self.choose('envelope_show', 'seryeon', 'post', options, followup))
        self.assertIsNone(self.choose('envelope_show', 'seryeon', 'post', options + [dict(index=7)], []))
        options[0]['present_only'] = False
        self.assertIsNone(self.choose('envelope_show', 'seryeon', 'post', options, []))

    def test_portrait_only_runs_the_original_single_question_zero(self):
        options = self.options('portrait_ask')
        questions = [(options[0]['title'], SimpleNamespace(value=0), False)]
        self.assertEqual(self.choose('portrait_ask', 'resident_piko', 'square', options, questions), 0)
        options[0]['index'] = 9
        self.assertIsNone(self.choose('portrait_ask', 'resident_piko', 'square', options, questions))

    def test_portrait_preserves_followups_and_different_question_actions(self):
        options = self.options('portrait_ask')
        original = (options[0]['title'], SimpleNamespace(value=0), False)
        followup = ('후속 질문', SimpleNamespace(value=('followup', 'new')), False)
        self.assertIsNone(self.choose('portrait_ask', 'resident_piko', 'square', options, [original, followup]))
        for value in [False, None, 'present', 1, ('followup', 'new')]:
            with self.subTest(value=value):
                self.assertIsNone(self.choose('portrait_ask', 'resident_piko', 'square', options,
                                             [('다른 질문', SimpleNamespace(value=value), False)]))

    def test_direct_picker_still_rejects_unowned_wrong_or_wrong_recipient_record(self):
        binding = dict(options=self.options('envelope_show'))
        self.env['store'] = SimpleNamespace(room13=dict(location='post', evidence=['V111:E01', 'V111:E02']))
        self.assertEqual(self.present(binding, 'seryeon', 'V111:E01'), 0)
        self.assertIsNone(self.present(binding, 'seryeon', 'V111:E02'))
        self.assertIsNone(self.present(binding, 'guard', 'V111:E01'))
        self.env['store'].room13['evidence'] = []
        self.assertIsNone(self.present(binding, 'seryeon', 'V111:E01'))


if __name__ == '__main__':
    unittest.main()
