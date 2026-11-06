"""6일 주민 반응: 허락/실제 인수와 잔류/빈 창고 경로를 분리한다."""
import copy
import json
import re
import unittest

import test_newworld_text as layer


SOURCE = layer.ROOT / 'game/room13_v111_days610.rpy'
MATCHING = layer.ROOT / 'docs/design/resident-reactions-day456-20261106/day6_매칭.json'


class ResidentDay6(layer.Layer):
    def setUp(self):
        self.load()
        self.rows = []
        part = json.loads((layer.ROOT / 'game/v111/newworld/d06.json').read_text())
        # 추가행은 실행 패킷에 line_id를 싣지 않으므로 실제 출력 문장으로 대조한다.
        self.rr_by_text = {row['text']: row['id']
                           for group in ('after', 'blocks')
                           for block in part.get(group, {}).values() for row in block
                           if row.get('id', '').startswith('NW_RR6_')}
        self.env.update(
            r13_lines=lambda rows, tag=None: self.rows.extend(rows),
            r13_v111_scene=lambda *args: None,
            r13_v111_travel=lambda *args, **kwargs: None,
            r13_v111_arrive=lambda *args: None,
            r13_v111_join=lambda *args: None,
            r13_fork_set_fate=lambda *args: None,
        )

    def run_label(self, name):
        """기존 라벨의 입력 없는 부분을 실행한다. 이동 표시는 스텁으로 둔다."""
        match = re.search(r'^label ' + re.escape(name) + r':\n(.*?)(?=^label |^init |\Z)',
                          SOURCE.read_text(), re.M | re.S)
        self.assertIsNotNone(match, name)
        code = []
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
            code.append(line)
        function_name = '_run_' + name
        exec('def ' + function_name + '():\n' + '\n'.join(code), self.env)
        return self.env[function_name]()

    def setv(self, **values):
        for key, value in values.items():
            self.env['r13_v111_set'](key, value)

    def rr_ids(self):
        return [self.rr_by_text[row[1]] for row in self.rows if row[1] in self.rr_by_text]

    def test_permission_and_prepared_blankets_are_not_handover(self):
        self.setv(FIRE_EVACUATED=False, warehouse_children_school_handover=0,
                  D06_P01_handover_completed=False, school_blankets_prepared6=False)
        self.assertEqual(self.run_label('r13_v111_seat6'), 'r13_v111_afternoon6')
        self.assertTrue(self.env['r13_v111_value']('school_permission'))
        self.assertTrue(self.env['r13_v111_value']('kkomi_seat6'))
        self.run_label('r13_v111_school_blanket_loan6')
        self.assertTrue(self.env['r13_v111_value']('school_blankets_prepared6'))
        self.assertFalse(self.env['r13_v111_value']('FIRE_EVACUATED'))
        self.assertFalse(self.env['r13_v111_value']('D06_P01_handover_completed'))
        self.assertEqual(self.env['r13_v111_value']('warehouse_children_school_handover'), 0)
        self.assertEqual(self.rr_ids(), [])

    def test_actual_receipt_reaction_requires_current_loan_and_precedes_commit(self):
        self.setv(kkomi_seat6=True, school_blankets_prepared6=True,
                  FIRE_EVACUATED=False, D06_P01_handover_completed=False,
                  carried_dry_blankets=2)
        receipt_state = []
        real_lines = self.env['r13_lines']

        def observe(rows, tag=None):
            if any(self.rr_by_text.get(row[1]) == 'NW_RR6_01_02' for row in rows):
                receipt_state.append(self.env['r13_v111_value']('D06_P01_handover_completed'))
            real_lines(rows, tag)

        self.env['r13_lines'] = observe
        self.assertEqual(self.run_label('r13_v111_handoff_done6'), 'r13_v111_empty_fire6')
        self.assertEqual(self.rr_ids(), ['NW_RR6_01_01', 'NW_RR6_01_02', 'NW_RR6_01_03'])
        self.assertEqual(receipt_state, [False])
        self.assertTrue(self.env['r13_v111_value']('FIRE_EVACUATED'))
        self.assertTrue(self.env['r13_v111_value']('KKOMI_ALIVE'))
        self.assertEqual(self.env['r13_v111_value']('warehouse_children_school_handover'), 4)
        self.assertEqual(self.env['r13_v111_value']('carried_dry_blankets'), 2)

    def test_legacy_handover_does_not_invent_loan_memory(self):
        self.setv(kkomi_seat6=False, school_blankets_prepared6=False)
        self.run_label('r13_v111_handoff_done6')
        self.assertEqual(self.rr_ids(), [])
        self.assertTrue(self.env['r13_v111_value']('D06_P01_handover_completed'))
        self.assertEqual(self.env['r13_v111_value']('warehouse_children_school_handover'), 4)

    def test_three_child_rescue_does_not_save_kkomi(self):
        # 이미 밖으로 나온 세 아이에 대한 반응은 자료·생사를 바꾸지 않는다.
        self.setv(FIRE_EVACUATED=False, KKOMI_ALIVE=True)
        before = copy.deepcopy(self.state.room13)
        self.rows.extend(self.env['r13_v111_lines'](['MS14_D06_S03_L0005']))
        self.assertEqual(self.state.room13, before)
        self.assertEqual(self.rr_ids(), ['NW_RR6_02_01', 'NW_RR6_02_02', 'NW_RR6_02_03'])
        self.assertEqual(self.run_label('r13_v111_rescue_done6'), 'r13_v111_after_fire6')
        self.assertFalse(self.env['r13_v111_value']('KKOMI_ALIVE'))
        self.assertEqual(self.env['r13_v111_value']('warehouse_children_rescued'), 3)
        self.assertEqual(self.env['r13_v111_value']('DARAM_location'), 'school')
        self.assertEqual(self.env['r13_v111_value']('BORI_hands'), 'burned')

    def test_school_reactions_do_not_cross_between_fire_outcomes(self):
        self.env.update(
            room13=self.state.room13,
            r13_edit=lambda **kwargs: None,
            r13_v111_score=lambda: None,
        )
        for name in ('r13_v111_bori_burned6', 'r13_v111_bori_unhurt6',
                     'r13_v111_empty_testimony6', 'r13_v111_rescue_testimony6'):
            self.env[name] = lambda label=name: self.run_label(label)
        self.setv(FIRE_EVACUATED=False, KKOMI_ALIVE=False)
        self.assertEqual(self.run_label('r13_v111_after_fire6'), 'r13_v111_fire_evidence6')
        self.assertEqual(self.rr_ids(), ['NW_RR6_03_01', 'NW_RR6_03_02', 'NW_RR6_03_03'])
        self.assertFalse(self.env['r13_v111_value']('KKOMI_ALIVE'))
        self.assertEqual(self.env['r13_v111_value']('BORI_hands'), 'burned')
        self.rows.clear()
        self.setv(FIRE_EVACUATED=True, KKOMI_ALIVE=True)
        self.assertEqual(self.run_label('r13_v111_after_fire6'), 'r13_v111_fire_evidence6')
        self.assertEqual(self.rr_ids(), ['NW_RR6_04_01', 'NW_RR6_04_02'])
        self.assertTrue(self.env['r13_v111_value']('KKOMI_ALIVE'))
        self.assertEqual(self.env['r13_v111_value']('BORI_hands'), 'not_rescue_burned')

    def test_all_new_reactions_are_pure_display_and_catalog_is_valid(self):
        part = json.loads((layer.ROOT / 'game/v111/newworld/d06.json').read_text())
        rows = [row for group in ('before', 'after', 'blocks')
                for block in part.get(group, {}).values() for row in block
                if row.get('id', '').startswith('NW_RR6_')]
        self.assertEqual(len(rows), 11)
        self.assertEqual(len({row['id'] for row in rows}), 11)
        for row in rows:
            self.assertLessEqual(set(row), {'id', 'speaker', 'kind', 'text', 'expression'})
        before = copy.deepcopy(self.state.room13)
        for anchor in ('MS14_D06_S03_L0005', 'MS14_D06_S04_L0013', 'MS14_D06_S04_L0017'):
            self.env['r13_v111_lines']([anchor])
        self.env['r13_nw_block']('school_blanket_receipt6')
        self.assertEqual(self.state.room13, before)
        self.assertEqual(self.env['r13_nw_text_problems'](), [])
        matching = json.loads(MATCHING.read_text())
        matched = [rid for scene in matching['scenes'] for rid in scene['game_addition']['row_ids']]
        self.assertEqual(set(matched), {row['id'] for row in rows})
        catalog = set(self.env['R13_V111']['records'])
        for group in ('before', 'after', 'blocks'):
            for block in self.env['R13_NW_TEXT'][group].values():
                catalog.update(row['id'] for row in block)
        for scene in matching['scenes']:
            for anchor in scene['anchors']:
                self.assertRegex(SOURCE.read_text(),
                                 r'(?m)^label ' + re.escape(anchor['label']) + r':$')
                self.assertLessEqual(set(anchor['dialogue_ids']), catalog)


if __name__ == '__main__':
    unittest.main()
