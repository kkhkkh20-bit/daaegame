"""12일 주민 반응의 실제 도착·입증 뒤 노출·기존 효과 경계를 확인한다."""
import copy
import json
import re
import unittest

import test_newworld_text as layer


SOURCE = layer.ROOT / 'game/room13_v111_days1114.rpy'
MATCHING = layer.ROOT / 'docs/design/resident-reactions-day101112-20261106/day12_매칭.json'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError('중복 JSON 키: ' + key)
        result[key] = value
    return result


class ResidentDay12(layer.Layer):
    def setUp(self):
        self.load()
        self.rows = []
        self.present = set()
        self.grand = False
        self.choice = '약장 밖에 맡긴 약도 있는지 묻는다'
        part = json.loads((layer.ROOT / 'game/v111/newworld/d12.json').read_text(),
                          object_pairs_hook=unique_object)
        self.rr_by_text = {row['text']: row['id'] for group in ('after', 'blocks')
                           for rows in part[group].values() for row in rows
                           if row['id'].startswith('NW_RR12_')}
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
            r13_fork_set_fate=lambda *args: None,
            r13_nw_meeting_end=lambda key, result: self.env['r13_v111_set']('meeting:' + key, result),
            r13_nw_grand=lambda *args: self.grand,
            r13_nw_retry=lambda *args: False,
            r13_nw_list=lambda person, reason: self.env['r13_v111_set']('listed:' + person, True),
        )

    def setv(self, **values):
        for key, value in values.items():
            self.env['r13_v111_set'](key, value)

    def run_label(self, name):
        """현재 소스의 호출·효과·분기를 실행한다. 화면과 이동만 스텁이다."""
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
            elif statement == 'menu:':
                line = indent + 'if True:'
            elif re.fullmatch(r"'.*':", statement):
                line = indent + 'if _rr_choice == ' + statement[:-1] + ':'
            lines.append(line)
        self.env['_rr_choice'] = self.choice
        function_name = '_run_' + name
        exec('def ' + function_name + '():\n' + '\n'.join(lines), self.env)
        return self.env[function_name]()

    def rr_ids(self):
        return [self.rr_by_text[row[1]] for row in self.rows if row[1] in self.rr_by_text]

    def test_seori_reacts_after_actual_return_and_before_handling_record(self):
        self.present = {'daram', 'nabi', 'resident_teacher'}
        self.setv(route12='premeal_stopped', medical_arrived=False,
                  KKOMI_ALIVE=True, **{'alive:kid_dodam': True, 'busy:resident_bori': 'medical_call'})
        seen = []
        output = self.env['r13_lines']

        def observe(rows, tag=None):
            if any(self.rr_by_text.get(row[1]) == 'NW_RR12_01_02' for row in rows):
                seen.append(('resident_seori' in self.present,
                             self.env['r13_v111_owned']('E12_HANDLING')))
            output(rows, tag)

        self.env['r13_lines'] = observe
        self.assertEqual(self.run_label('r13_v111_medical_arrival12'), 'r13_v111_soup_final12')
        self.assertEqual(self.rr_ids(), ['NW_RR12_01_01', 'NW_RR12_01_02', 'NW_RR12_01_03'])
        self.assertEqual(seen, [(True, False)])
        self.assertTrue(self.env['r13_v111_owned']('E12_HANDLING'))
        self.assertTrue(self.env['r13_v111_value']('medical_arrived'))
        self.assertTrue(self.env['r13_v111_value']('KKOMI_ALIVE'))
        self.assertTrue(self.env['r13_v111_value']('alive:kid_dodam'))

    def test_late_medical_visit_does_not_reuse_premeal_reaction_or_confirm_death_early(self):
        self.setv(route12='late_exposure', KKOMI_ALIVE=False,
                  **{'alive:kid_dodam': True, 'busy:resident_bori': 'medical_call'})
        self.run_label('r13_v111_medical_arrival12')
        self.assertEqual(self.rr_ids(), [])
        self.assertFalse(self.env['r13_v111_value']('KKOMI_ALIVE'))
        self.assertTrue(self.env['r13_v111_value']('alive:kid_dodam'))

    def test_nabi_book_reaction_follows_partial_plain_or_grand_results(self):
        for result, grand in (('partial', False), ('win', False), ('win', True)):
            with self.subTest(result=result, grand=grand):
                self.setUp()
                self.present = {'nabi', 'daram', 'resident_teacher', 'guard', 'neoul'}
                self.setv(route12='premeal_stopped', teacher_confessed=True,
                          transfer_list_secured=result == 'win', transfer_list_voided=grand,
                          **{'meeting:soup': result, 'grand:soup': grand})
                self.choice = '돌목에게 감독을 맡긴다'
                self.assertEqual(self.run_label('r13_v111_soup_after_route12'), 'r13_v111_aftermath_pre12')
                self.assertEqual(self.run_label('r13_v111_aftermath_pre12'), 'r13_v111_teacher_guard_pre12')
                self.assertEqual(self.rr_ids(), ['NW_RR12_02_01', 'NW_RR12_02_02', 'NW_RR12_02_03'])
                self.assertTrue(self.env['r13_v111_value']('book_promise12'))
                self.assertEqual(self.env['r13_v111_value']('transfer_list_secured'), result == 'win')
                self.assertEqual(self.env['r13_v111_value']('transfer_list_voided'), grand)

    def test_failure_and_early_prevention_do_not_get_book_or_medical_reactions(self):
        self.setv(route12='premeal_stopped', soup_lose_kind='nabi', **{'meeting:soup': 'lose'})
        self.assertEqual(self.run_label('r13_v111_soup_lost12'), 'r13_v111_sleep12')
        self.assertEqual(self.rr_ids(), [])
        self.rows.clear()
        self.setv(grand_bowl_pocket=False, KKOMI_ALIVE=False, **{'alive:kid_dodam': True})
        self.assertEqual(self.run_label('r13_v111_early12'), 'r13_v111_sleep12')
        self.assertEqual(self.rr_ids(), [])
        self.assertEqual(self.env['r13_v111_value']('route12'), 'early_prevented')
        self.assertFalse(self.env['r13_v111_value']('KKOMI_ALIVE'))

    def test_guard_reaction_requires_grand_win_and_actual_presence_on_both_routes(self):
        for route in ('premeal_stopped', 'late_exposure'):
            for grand, guard in ((False, True), (True, False), (True, True)):
                with self.subTest(route=route, grand=grand, guard=guard):
                    self.setUp()
                    self.grand = grand
                    self.present = {'guard', 'neoul'} if guard else {'neoul'}
                    self.setv(route12=route, transfer_list_voided=False, KKOMI_ALIVE=False,
                              **{'alive:kid_dodam': route != 'late_exposure'})
                    self.run_label('r13_v111_list_won12')
                    self.assertEqual(bool(self.rr_ids()), grand and guard)
                    self.assertTrue(self.env['r13_v111_value']('transfer_list_secured'))
                    self.assertEqual(self.env['r13_v111_value']('transfer_list_voided'), grand)
                    self.assertFalse(self.env['r13_v111_value']('KKOMI_ALIVE'))
                    self.assertEqual(self.env['r13_v111_value']('alive:kid_dodam'), route != 'late_exposure')
                    if grand and guard:
                        texts = [row[1] for row in self.rows]
                        before = next(i for i, text in enumerate(texts) if '그 옆에 ‘무효’라고 적는다' in text)
                        after = next(i for i, text in enumerate(texts) if self.rr_by_text.get(text) == 'NW_RR12_03_01')
                        self.assertLess(before, after)

    def test_all_nine_rows_are_display_only_and_match_valid_anchors(self):
        part = json.loads((layer.ROOT / 'game/v111/newworld/d12.json').read_text(),
                          object_pairs_hook=unique_object)
        rows = [row for group in ('after', 'blocks') for block in part[group].values()
                for row in block if row['id'].startswith('NW_RR12_')]
        self.assertEqual(len(rows), 9)
        for row in rows:
            self.assertLessEqual(set(row), {'id', 'speaker', 'kind', 'text', 'expression', 'when'})
            self.assertIn(row.get('expression'), {'neutral', 'anxious', 'angry'})
            self.assertIn(row.get('when'), {None, 'route12_premeal', 'grand_soup_guard'})
        self.present = {'resident_seori', 'guard'}
        self.setv(route12='premeal_stopped', **{'grand:soup': True})
        before = copy.deepcopy(self.state.room13)
        for anchor in ('MS14_D12_S04_L0045', 'MS14_D12_S04_L0100'):
            self.env['r13_v111_lines']([anchor])
        self.env['r13_nw_block']('soup_list_won12')
        self.assertEqual(self.state.room13, before)
        self.assertEqual(self.env['r13_nw_text_problems'](), [])
        matching = json.loads(MATCHING.read_text(), object_pairs_hook=unique_object)
        self.assertEqual({rid for scene in matching['scenes'] for rid in scene['game_added_ids']},
                         {row['id'] for row in rows})
        catalog = set(self.env['R13_V111']['records'])
        for group in ('before', 'after', 'blocks'):
            for block in self.env['R13_NW_TEXT'][group].values():
                catalog.update(row['id'] for row in block)
        for scene in matching['scenes']:
            self.assertEqual(scene['day'], 12)
            self.assertEqual(scene['modified_ids'], [])
            self.assertRegex(SOURCE.read_text(), r'(?m)^label ' + scene['label'] + r':$')
            for anchor in scene['anchors']:
                self.assertLessEqual(set(anchor.get('record_ids', []) + anchor.get('overlay_ids', [])), catalog)


if __name__ == '__main__':
    unittest.main()
