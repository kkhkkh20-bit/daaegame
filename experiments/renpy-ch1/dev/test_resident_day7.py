"""7일 주민 발췌의 공개 순서와 자백·생존 갈래, 조회 무부작용을 확인한다."""
import ast
import copy
import itertools
import json
import re
import unittest

from test_newworld_text import Layer, ROOT


DAY_FILE = ROOT / 'game/v111/newworld/d07.json'
MATCHING = ROOT / 'docs/design/resident-reactions-day789-20261106/day7_매칭.json'


class ResidentDay7(Layer):
    def test_living_child_exchange_is_wholly_absent_when_kkomi_is_dead(self):
        env = self.load()
        env['r13_v111_set']('KKOMI_ALIVE', False)
        before = copy.deepcopy(self.state.room13)
        rows = env['r13_v111_lines'](['MS14_D07_S02_L0036'])
        self.assertFalse(any(r[0] == 'kid_kkomi' or '나르는 거랑 안 깨는 건' in r[1] for r in rows))
        self.assertEqual(before, self.state.room13)
        data = json.loads(DAY_FILE.read_text())
        self.assertTrue(all(r.get('when') == 'kkomi_alive' for r in data['after']['MS14_D07_S02_L0036']))

    def label(self, name):
        source = (ROOT / 'game/room13_v111_days610.rpy').read_text()
        return re.search(r'^label ' + name + r':\n(.*?)(?=^label |\Z)', source, re.M | re.S).group(1)

    def rows(self, env, label):
        result = []
        for call in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)', self.label(label)):
            result.extend(env['r13_v111_lines'](ast.literal_eval(call.group(1))))
        return result

    def excerpt(self, entry):
        data = json.loads(DAY_FILE.read_text())
        section = entry['scene_extent']['game_excerpt']
        return [row for row in data[section['position']][section['anchor']]
                if row['id'] in entry['game_added_ids']]

    def test_viewing_beats_keeps_life_fire_meeting_and_evidence_unchanged(self):
        entries = json.loads(MATCHING.read_text())['scenes']
        for alive, evacuated, result in itertools.product((False, True), (False, True), ('lose', 'partial', 'win')):
            with self.subTest(alive=alive, evacuated=evacuated, meeting=result):
                env = self.load()
                self.state.room13.update(day=7, period=0, location='school')
                for key, value in [('KKOMI_ALIVE', alive), ('FIRE_EVACUATED', evacuated), ('meeting:fire', result)]:
                    env['r13_v111_set'](key, value)
                env['r13_v111_set']('NUBI_intent_to_kill', 'unproven')
                before = copy.deepcopy(self.state.room13)
                intake = env['r13_nw_block']('nubi_children_received7')
                self.assertEqual([r[0] for r in intake], [None, 'resident_teacher', 'nabi', 'resident_teacher', None])
                if result != 'lose':
                    self.rows(env, 'r13_v111_nubi_admission7')
                rows = self.rows(env, 'r13_v111_living_child7' if alive else 'r13_v111_lost_child7')
                texts = [r[1] for r in rows]
                living_excerpt = [r['text'] for r in self.excerpt(entries[2])]
                self.assertEqual([t for t in texts if t in living_excerpt], living_excerpt if alive else [])
                self.assertNotIn('kid_kkomi', [r[0] for r in rows] if not alive else [])
                self.assertEqual(before, self.state.room13, '조회는 인수·자백·생사·승패·자료 획득을 처리하지 않는다')
                self.assertFalse(env['r13_v111_owned']('E07_NUBI'))
                self.assertEqual(env['r13_v111_value']('NUBI_intent_to_kill'), 'unproven')

    def test_nubi_excerpt_is_after_admission_and_never_in_first_loss_path(self):
        env = self.load()
        entries = json.loads(MATCHING.read_text())['scenes']
        rows = self.rows(env, 'r13_v111_nubi_admission7')
        texts = [r[1] for r in rows]
        anchor = next(i for i, row in enumerate(rows) if row[2].get('line_id') == 'MS14_D07_S01_L0044')
        added = [texts.index(r['text']) for r in self.excerpt(entries[1])]
        self.assertEqual(added, list(range(anchor + 1, anchor + 4)))
        admission = self.label('r13_v111_nubi_admission7')
        first_question = self.label('r13_v111_nubi_first_question7')
        first_proof = self.label('r13_v111_nubi_proof7')
        self.assertIn("['E06_FIRE'],'r13_v111_nubi_first_question7'", first_proof)
        for guarded in (admission, first_question):
            self.assertIn('if not r13_v111_value("bori_nubi_door_witness_heard"):', guarded)
            self.assertIn('jump r13_v111_bori_witness7', guarded)
        loss = self.label('r13_v111_nubi_wrong7')
        self.assertNotIn('r13_v111_nubi_admission7', loss)
        self.assertIn('jump r13_v111_responsibility7', loss)
        env['r13_v111_commit']('MS14_D07_S01_L0045')
        self.assertTrue(env['r13_v111_owned']('E07_NUBI'))
        self.assertTrue(env['r13_v111_value']('NUBI_admitted_setting_fire'))
        self.assertEqual(env['r13_v111_value']('NUBI_intent_to_kill'), 'unproven')

    def test_intake_and_living_child_still_use_original_commits_and_separate_counts(self):
        env = self.load()
        intake = self.label('r13_v111_nubi_children_received7')
        self.assertLess(intake.index("r13_v111_commit('MS14_D07_S01_L0024')"),
                        intake.index("r13_nw_block('nubi_children_received7')"))
        self.assertLess(intake.index("r13_nw_block('nubi_children_received7')"), intake.index("r13_v111_travel('laundry'"))
        env['r13_v111_commit']('MS14_D07_S01_L0024')
        self.assertEqual(env['r13_v111_value']('NUBI_CHILDREN_location'), 'school')
        rows = self.rows(env, 'r13_v111_living_child7')
        texts = [r[1] for r in rows]
        entry = json.loads(MATCHING.read_text())['scenes'][2]
        added = [texts.index(row['text']) for row in self.excerpt(entry)]
        original = next(i for i, row in enumerate(rows) if row[2].get('line_id') == 'MS14_D07_S02_L0036')
        later = next(i for i, row in enumerate(rows) if row[2].get('line_id') == 'MS14_D07_S02_L0049')
        self.assertTrue(all(original < i < later for i in added))
        route = self.label('r13_v111_school_names_done7')
        self.assertIn("if r13_v111_value('KKOMI_ALIVE'):", route)
        self.assertIn('call r13_v111_living_child7\n    else:\n        call r13_v111_lost_child7', route)

    def test_matching_distinguishes_complete_scene_from_nine_added_game_rows(self):
        matching = json.loads(MATCHING.read_text())
        self.assertEqual(matching['day'], 7)
        self.assertEqual([e['id'] for e in matching['scenes']], ['RR7_01', 'RR7_02', 'RR7_03'])
        self.assertEqual([e['pov_name'] for e in matching['scenes']], ['사자 선생님', '누비', '보리'])
        self.assertEqual(sum(len(e['game_added_ids']) for e in matching['scenes']), 9)
        data = json.loads(DAY_FILE.read_text())
        for entry in matching['scenes']:
            self.assertEqual(entry['day'], 7)
            self.assertTrue(entry['known'] and entry['unknown'])
            self.assertTrue(entry['scene_extent']['manuscript'])
            self.assertTrue(entry['scene_extent']['release_after'])
            excerpt = entry['scene_extent']['game_excerpt']
            self.assertIn(excerpt['anchor'], self.label(entry['label']))
            rows = self.excerpt(entry)
            self.assertEqual([r['id'] for r in rows], entry['game_added_ids'])
            self.assertFalse(any(set(r) & {'effects', 'operations', 'set', 'acquire'} for r in rows))
        self.assertEqual(data['blocks']['nubi_children_received7'][0]['id'], 'NW_D07_NC01')
        # 주민의 내면은 문서에만 있고, 추가된 게임 지문은 아빠가 볼 수 있는 행동이다.
        self.assertFalse(any(r.get('kind') == 'thought' for e in matching['scenes'] for r in self.excerpt(e)))


if __name__ == '__main__':
    unittest.main()
