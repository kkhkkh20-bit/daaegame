"""9일 주민 반응의 실제 출석·경로·자료 취득 순서를 검증한다."""
import ast
import copy
import json
import re
import textwrap
import unittest

import test_newworld_text as layer


SOURCE = layer.ROOT / 'game/room13_v111_days610.rpy'
MATCHING = layer.ROOT / 'docs/design/resident-reactions-day789-20261106/day9_매칭.json'


class ResidentDay9(layer.Layer):
    def setUp(self):
        self.load()
        self.rows = []
        self.present = set()
        part = json.loads((layer.ROOT / 'game/v111/newworld/d09.json').read_text())
        # 추가행 패킷에는 line_id가 없으므로 등록된 실제 문장으로 출력을 대조한다.
        self.rr_by_text = {row['text']: row['id'] for rows in part['after'].values()
                           for row in rows if row['id'].startswith('NW_RR9_')}
        self.env.update(
            room13=self.state.room13,
            r13_lines=lambda rows, tag=None: self.rows.extend(rows),
            r13_v111_scene=lambda *args: None,
            r13_edit=lambda **kwargs: None,
            r13_v111_travel=lambda *args, **kwargs: None,
            r13_v111_arrive=lambda people: setattr(self, 'present', set(people)),
            r13_v111_join=lambda people: self.present.update(people),
            r13_v111_actor_ready=lambda person: person in self.present,
            r13_v111_score=lambda: None,
            r13_v111_wait=lambda *args: None,
        )
        # 출석 판정은 추정 스텁 대신 현재 실행 파일의 함수를 그대로 사용한다.
        source = (layer.ROOT / 'game/room13_v111_later_bindings.rpy').read_text()
        block = re.search(r'^init 311 python:\n((?:[ \t].*\n|\n)*)', source, re.M).group(1)
        function = next(node for node in ast.parse(textwrap.dedent(block)).body
                        if isinstance(node, ast.FunctionDef) and node.name == 'r13_v111_tok_attends')
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'tok_attends', 'exec'), self.env)

    def setv(self, **values):
        for key, value in values.items():
            self.env['r13_v111_set'](key, value)

    def run_label(self, name):
        """기존 라벨의 Python·호출·분기를 실행한다. 화면과 이동은 스텁이다."""
        match = re.search(r'^label ' + re.escape(name) + r':\n(.*?)(?=^label |^init |\Z)',
                          SOURCE.read_text(), re.M | re.S)
        self.assertIsNotNone(match, name)
        lines = []
        for line in match.group(1).splitlines():
            indent = line[:len(line) - len(line.lstrip())]
            statement = line.lstrip()
            if statement.startswith('$ '):
                line = indent + statement[2:]
            elif statement.startswith('call '):
                call = statement[5:]
                line = indent + call + ('()' if '(' not in call else '')
            elif statement.startswith('jump '):
                line = indent + 'return ' + repr(statement[5:])
            lines.append(line)
        function_name = '_run_' + name
        exec('def ' + function_name + '():\n' + '\n'.join(lines), self.env)
        return self.env[function_name]()

    def rr_ids(self):
        return [self.rr_by_text[row[1]] for row in self.rows if row[1] in self.rr_by_text]

    def test_murder_and_prevention_stage_different_companions(self):
        self.setv(route7='murder', DARAM_DETAINED=True)
        self.assertEqual(self.run_label('r13_v111_day9'), 'r13_v111_passage9')
        self.assertEqual(self.run_label('r13_v111_passage9'), 'r13_v111_safe_passage9')
        self.assertIn('buri', self.present)
        self.assertNotIn('daram', self.present)
        self.assertNotIn('어느 문으로 나가', ' '.join(row[1] for row in self.rows))
        self.assertEqual(self.rr_ids(), [])
        self.setv(route7='prevent', DARAM_DETAINED=False,
                  **{'busy:nabi': 'daram_guard', 'location:daram': 'school'})
        self.assertEqual(self.run_label('r13_v111_day9'), 'r13_v111_prevent_passage9')
        self.assertEqual(self.run_label('r13_v111_prevent_passage9'), 'r13_v111_safe_prevent9')
        self.assertNotIn('buri', self.present)
        self.assertNotIn('daram', self.present)
        self.assertIsNone(self.env['r13_v111_value']('busy:nabi'))
        self.assertEqual(self.rr_ids(), [])

    def test_safety_question_does_not_start_walk_or_acquire_record(self):
        self.env['_return'] = 1
        self.assertEqual(self.run_label('r13_v111_safe_passage9'), 'r13_v111_passage_safety_hint9')
        self.assertEqual(self.run_label('r13_v111_passage_safety_hint9'), 'r13_v111_safe_passage9')
        self.assertEqual(self.rr_ids(), [])
        self.assertFalse(self.env['r13_v111_owned']('E09_PASSAGE'))
        self.env['_return'] = None
        self.assertEqual(self.run_label('r13_v111_safe_passage9'), 'r13_v111_safe_passage9')
        self.assertFalse(self.env['r13_v111_owned']('E09_PASSAGE'))

    def test_buri_reaction_precedes_walk_commit_and_never_enters_prevention(self):
        self.setv(DARAM_DETAINED=True, TTADAK_ALIVE=True)
        observed = []
        output = self.env['r13_lines']

        def inspect(rows, tag=None):
            if any(self.rr_by_text.get(row[1]) == 'NW_RR9_01_02' for row in rows):
                observed.append(self.env['r13_v111_owned']('E09_PASSAGE'))
            output(rows, tag)

        self.env['r13_lines'] = inspect
        self.assertEqual(self.run_label('r13_v111_passage_walk9'), 'r13_v111_passage_after9')
        self.assertEqual(self.rr_ids(), ['NW_RR9_01_01', 'NW_RR9_01_02', 'NW_RR9_01_03'])
        self.assertEqual(observed, [False])
        self.assertTrue(self.env['r13_v111_owned']('E09_PASSAGE'))
        self.assertTrue(self.env['r13_v111_value']('TTADAK_ALIVE'))
        self.assertTrue(self.env['r13_v111_value']('DARAM_DETAINED'))
        self.setUp()
        self.assertEqual(self.run_label('r13_v111_prevent_walk9'), 'r13_v111_papers_check9')
        self.assertEqual(self.rr_ids(), [])
        self.assertTrue(self.env['r13_v111_owned']('E09_PASSAGE'))
        self.assertTrue(self.env['r13_v111_value']('TTADAK_ALIVE'))

    def test_tok_attendance_and_copy_use_workshop_value_independently_of_hearing(self):
        for alive in (False, True):
            for workshop in (False, True):
                for hearing in (False, True):
                    with self.subTest(alive=alive, workshop=workshop, hearing=hearing):
                        self.setUp()
                        self.setv(route7='murder', DARAM_DETAINED=True, TOK_ALIVE=alive,
                                  tok_workshop_present=workshop, tok_hearing_present=hearing)
                        attends = alive and workshop
                        target = self.run_label('r13_v111_tok_route9')
                        self.assertEqual(target, 'r13_v111_tok9' if attends else 'r13_v111_repair_copy9')
                        self.assertEqual(self.run_label(target), 'r13_v111_scarf9')
                        self.assertEqual(bool(self.rr_ids()), attends)
                        self.assertEqual('resident_tok' in self.present, attends)
                        self.assertNotIn('daram', self.present)
                        self.assertTrue(self.env['r13_v111_owned']('E09_PIN_OWNER'))
                        self.assertTrue(self.env['r13_v111_value']('tok_repair_copy_owned'))
                        self.assertEqual(self.env['r13_v111_value']('E09_PIN_OWNER'),
                                         'repair_and_receipt_confirmed' if attends else 'repair_receipt_copy_confirmed')
                        self.assertEqual(self.env['r13_v111_value']('TOK_ALIVE'), alive)
                        self.assertTrue(self.env['r13_v111_value']('DARAM_DETAINED'))

    def test_tok_reaction_adds_no_record_before_existing_repair_commit(self):
        self.setv(TOK_ALIVE=True, tok_workshop_present=True)
        before = copy.deepcopy(self.state.room13)
        self.rows.extend(self.env['r13_v111_lines'](['MS14_D09_S02_L0007']))
        self.assertEqual(self.rr_ids(), ['NW_RR9_02_01', 'NW_RR9_02_02', 'NW_RR9_02_03'])
        self.assertEqual(self.state.room13, before)
        self.assertFalse(self.env['r13_v111_owned']('E09_PIN_OWNER'))
        self.assertNotIn('할머니', ' '.join(row[1] for row in self.rows))

    def test_postal_reaction_is_common_without_private_letter_or_custody_effect(self):
        for route in ('murder', 'prevent'):
            with self.subTest(route=route):
                self.setUp()
                detained = route == 'murder'
                self.setv(route7=route, DARAM_DETAINED=detained,
                          mother_warning_shared9=False, pending_post_search=True)
                before_commit = []
                output = self.env['r13_lines']

                def inspect(rows, tag=None):
                    if any(self.rr_by_text.get(row[1]) == 'NW_RR9_03_02' for row in rows):
                        before_commit.append(self.env['r13_v111_owned']('E09_MAIL'))
                    output(rows, tag)

                self.env['r13_lines'] = inspect
                self.run_label('r13_v111_postal9')
                self.assertEqual(self.rr_ids(), ['NW_RR9_03_01', 'NW_RR9_03_02', 'NW_RR9_03_03'])
                self.assertEqual(before_commit, [False])
                self.assertTrue(self.env['r13_v111_owned']('E09_MAIL'))
                self.assertFalse(self.env['r13_v111_value']('pending_post_search'))
                self.assertEqual(self.present, {'seryeon', 'resident_sling'})
                self.assertEqual(self.env['r13_v111_value']('DARAM_DETAINED'), detained)
                self.assertFalse(self.env['r13_v111_value']('mother_warning_shared9'))

    def test_display_only_rows_matching_and_existing_anchors_are_valid(self):
        part = json.loads((layer.ROOT / 'game/v111/newworld/d09.json').read_text())
        rows = [row for block in part['after'].values() for row in block
                if row['id'].startswith('NW_RR9_')]
        self.assertEqual(len(rows), 9)
        for row in rows:
            self.assertEqual(set(row), {'id', 'speaker', 'kind', 'text', 'expression'})
            self.assertIn(row['expression'], {'neutral', 'anxious', 'angry'})
        self.assertEqual(self.env['r13_nw_text_problems'](), [])
        matching = json.loads(MATCHING.read_text())
        self.assertEqual(matching['day'], 9)
        self.assertEqual({rid for scene in matching['scenes'] for rid in scene['game_added_ids']},
                         {row['id'] for row in rows})
        catalog = set(self.env['R13_V111']['records'])
        for group in ('before', 'after', 'blocks'):
            for block in self.env['R13_NW_TEXT'][group].values():
                catalog.update(row['id'] for row in block)
        for scene in matching['scenes']:
            self.assertRegex(SOURCE.read_text(), r'(?m)^label ' + re.escape(scene['label']) + r':$')
            self.assertEqual(scene['modified_ids'], [])
            for anchor in scene['anchors']:
                if anchor.get('label'):
                    self.assertRegex(SOURCE.read_text(), r'(?m)^label ' + re.escape(anchor['label']) + r':$')
                self.assertLessEqual(set(anchor.get('record_ids', []) + anchor.get('overlay_ids', [])), catalog)


if __name__ == '__main__':
    unittest.main()
