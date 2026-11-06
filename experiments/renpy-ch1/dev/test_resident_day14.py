"""14일 생활 반응의 결말 줄기·현재 출석·미완료 조건을 보존한다."""
import copy
import json
import re
import unittest

import test_newworld_text as layer


SOURCE = layer.ROOT / 'game/room13_v111_days1114.rpy'
MATCHING = layer.ROOT / 'docs/design/resident-reactions-day1314-20261106/day14_매칭.json'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError('중복 JSON 키: ' + key)
        result[key] = value
    return result


class ResidentDay14(layer.Layer):
    def setUp(self):
        self.load()
        self.rows = []
        self.present = {'dad', 'mom', 'daram', 'resident_tosil', 'resident_madam', 'nabi', 'guard'}
        self.unavailable = set()
        part = json.loads((layer.ROOT / 'game/v111/newworld/d14.json').read_text(),
                          object_pairs_hook=unique_object)
        self.rr_by_text = {row['text']: row['id'] for block in part['after'].values()
                           for row in block if row['id'].startswith('NW_RR14_')}
        self.env.update(
            room13=self.state.room13,
            r13_lines=lambda rows, tag=None: self.rows.extend(rows),
            r13_v111_scene=lambda *args: None,
            r13_edit=lambda **kwargs: None,
            r13_v111_travel=lambda *args, **kwargs: None,
            r13_v111_arrive=lambda people: setattr(self, 'present', set(people)),
            r13_v111_actor_ready=lambda person: person in self.present and person not in self.unavailable,
        )
        for label in ('r13_v111_madam_inventory14', 'r13_v111_chorong_lamps14',
                      'r13_v111_mother_lamps14', 'r13_v111_owl_alive14', 'r13_v111_unfinished_operation14'):
            self.env[label] = lambda name=label: self.run_label(name)

    def setv(self, **values):
        for key, value in values.items():
            self.env['r13_v111_set'](key, value)

    def run_label(self, name):
        """대상 라벨의 실제 Python·호출·분기를 실행하고 다음 라벨을 돌려준다."""
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

    def test_ending_dispatch_does_not_send_other_endings_into_morning_life(self):
        for ending, label in (
            ('left_name', 'r13_v111_left_name_ending14'),
            ('frozen', 'r13_v111_frozen_ending14'),
            ('family', 'r13_v111_family_ending14'),
            ('partial', 'r13_v111_partial_ending14'),
            ('violence', 'r13_v111_violence_ending14'),
            ('morning', 'r13_v111_morning_safe14'),
        ):
            with self.subTest(ending=ending):
                self.env['r13_nw_ending14'] = lambda result=ending: result
                self.assertEqual(self.run_label('r13_v111_ending_dispatch14'), label)
                self.assertEqual(self.rr_ids(), [])

    def test_name_writing_reaction_preserves_inside_outside_knowledge(self):
        for listening in ('inside', 'outside'):
            with self.subTest(listening=listening):
                self.rows.clear()
                self.setv(tosil_listen=listening, bomi_death_confirmed=True, ending14='morning')
                before = copy.deepcopy(self.state.room13)
                self.assertEqual(self.run_label('r13_v111_tosil_name14'), 'r13_v111_pandol_news14')
                self.assertEqual(self.rr_ids(), ['NW_RR14_01_01', 'NW_RR14_01_02', 'NW_RR14_01_03'])
                self.assertEqual(self.state.room13, before)
                self.assertEqual(self.env['r13_v111_value']('tosil_listen'), listening)

    def test_not_writing_is_not_replaced_by_ink_reaction(self):
        for listening in ('inside', 'outside'):
            self.rows.clear()
            self.setv(tosil_listen=listening)
            self.assertEqual(self.run_label('r13_v111_tosil_no_name14'), 'r13_v111_pandol_news14')
            self.assertEqual(self.rr_ids(), [])

    def test_whole_madam_bundle_is_hidden_when_she_is_not_ready(self):
        for ready in (False, True):
            with self.subTest(ready=ready):
                self.rows.clear()
                self.unavailable = set() if ready else {'resident_madam'}
                before = copy.deepcopy(self.state.room13)
                self.run_label('r13_v111_madam_inventory14')
                self.assertEqual(self.rr_ids(),
                                 ['NW_RR14_02_01', 'NW_RR14_02_02', 'NW_RR14_02_03'] if ready else [])
                self.assertEqual(self.state.room13, before)

    def test_school_receipt_keeps_transport_and_joint_control_requirements(self):
        for stopped in (False, True):
            for controlled in (False, True):
                with self.subTest(stopped=stopped, controlled=controlled):
                    self.setUp()
                    self.setv(school_inventory_checked=False, current_transport_chain_stopped=stopped,
                              device_joint_control=controlled, current_sacrifice_operation_closed=False)
                    observed = []
                    output = self.env['r13_lines']

                    def inspect(rows, tag=None):
                        if any(self.rr_by_text.get(row[1]) == 'NW_RR14_02_02' for row in rows):
                            observed.append(self.env['r13_v111_value']('school_inventory_checked'))
                        output(rows, tag)

                    self.env['r13_lines'] = inspect
                    self.assertEqual(self.run_label('r13_v111_supply_inventory_done14'), 'r13_v111_lamp_assignment14')
                    self.assertEqual(observed, [False])
                    self.assertTrue(self.env['r13_v111_value']('school_inventory_checked'))
                    self.assertTrue(self.env['r13_v111_value']('school_supply_handed'))
                    self.assertEqual(self.env['r13_v111_value']('current_sacrifice_operation_closed'), stopped and controlled)
                    self.assertEqual(self.env['r13_v111_value']('current_transport_chain_stopped'), stopped)
                    self.assertEqual(self.env['r13_v111_value']('device_joint_control'), controlled)

    def test_lamp_reaction_keeps_absent_replacement_and_unfinished_operation(self):
        for ready in (False, True):
            for complete in (False, True):
                with self.subTest(ready=ready, complete=complete):
                    self.setUp()
                    self.unavailable = set() if ready else {'resident_lamplighter'}
                    self.setv(OWL_ALIVE=False, current_transport_chain_stopped=complete,
                              device_joint_control=complete, current_sacrifice_operation_closed=complete)
                    self.assertEqual(self.run_label('r13_v111_lamp_assignment14'), 'r13_v111_cookie14')
                    self.assertEqual(self.rr_ids(),
                                     ['NW_RR14_03_01', 'NW_RR14_03_02', 'NW_RR14_03_03'] if ready else [])
                    self.assertEqual(self.env['r13_v111_value']('lamp_manager'),
                                     'resident_lamplighter' if ready else 'mom')
                    self.assertEqual(self.env['r13_v111_value']('current_sacrifice_operation_closed'), complete)
                    self.assertFalse(self.env['r13_v111_value']('OWL_ALIVE'))
                    text = ' '.join(row[1] for row in self.rows)
                    self.assertEqual('아직 확인 못 한 분들은 빈칸' in text, not complete)

    def test_nine_display_only_rows_match_existing_anchors_and_expressions(self):
        part = json.loads((layer.ROOT / 'game/v111/newworld/d14.json').read_text(),
                          object_pairs_hook=unique_object)
        rows = [row for block in part['after'].values() for row in block
                if row['id'].startswith('NW_RR14_')]
        self.assertEqual(len(rows), 9)
        for row in rows:
            self.assertEqual(set(row), {'id', 'speaker', 'kind', 'text', 'expression'})
            self.assertIn(row['expression'], {'neutral', 'anxious'})
        self.assertEqual(self.env['r13_nw_text_problems'](), [])
        matching = json.loads(MATCHING.read_text(), object_pairs_hook=unique_object)
        self.assertEqual({rid for scene in matching['scenes'] for rid in scene['game_added_ids']},
                         {row['id'] for row in rows})
        catalog = set(self.env['R13_V111']['records'])
        for group in ('before', 'after', 'blocks'):
            for block in self.env['R13_NW_TEXT'][group].values():
                catalog.update(row['id'] for row in block)
        for scene in matching['scenes']:
            self.assertEqual(scene['day'], 14)
            self.assertEqual(scene['modified_ids'], [])
            self.assertRegex(SOURCE.read_text(), r'(?m)^label ' + scene['label'] + r':$')
            for anchor in scene['anchors']:
                self.assertLessEqual(set(anchor.get('record_ids', []) + anchor.get('overlay_ids', [])), catalog)


if __name__ == '__main__':
    unittest.main()
