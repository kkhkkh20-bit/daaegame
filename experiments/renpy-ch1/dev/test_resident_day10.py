"""10일 주민 발췌의 살인·예방·톡 출석 경계와 기존 결과 보존을 확인한다."""
import ast
import copy
import itertools
import json
import re
import textwrap
import unittest

from test_newworld_text import Layer, ROOT


DAY_FILE = ROOT / 'game/v111/newworld/d10.json'
MATCHING = ROOT / 'docs/design/resident-reactions-day101112-20261106/day10_매칭.json'


class ResidentDay10(Layer):
    def label(self, name):
        source = (ROOT / 'game/room13_v111_days610.rpy').read_text()
        return re.search(r'^label ' + name + r':\n(.*?)(?=^label |\Z)', source, re.M | re.S).group(1)

    def rows(self, env, label):
        result = []
        for call in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)', self.label(label)):
            result.extend(env['r13_v111_lines'](ast.literal_eval(call.group(1))))
        return result

    def excerpts(self):
        data = json.loads(DAY_FILE.read_text())
        return [[row for row in data['after'][entry['scene_extent']['game_excerpt']['anchor']]
                 if row['id'] in entry['game_added_ids']]
                for entry in json.loads(MATCHING.read_text())['scenes']]

    def attendance(self, env):
        source = (ROOT / 'game/room13_v111_later_bindings.rpy').read_text()
        block = re.search(r'^init 311 python:\n((?:[ \t].*\n|\n)*)', source, re.M).group(1)
        tree = ast.parse(textwrap.dedent(block))
        function = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'r13_v111_tok_attends']
        exec(compile(ast.Module(body=function, type_ignores=[]), 'tok_attendance', 'exec'), env)
        return env['r13_v111_tok_attends']

    def test_buri_leaves_after_notebook_return_before_trial_without_releasing_daram(self):
        env = self.load()
        env['r13_v111_set']('route7', 'murder')
        env['r13_v111_set']('OWL_ALIVE', False)
        env['r13_v111_set']('DARAM_DETAINED', True)
        before = copy.deepcopy(self.state.room13)
        rows = self.rows(env, 'r13_v111_waiting10')
        texts = [r[1] for r in rows]
        data = json.loads(DAY_FILE.read_text())
        returned = next(r['text'] for r in data['after']['MS14_D10_S01_L0014'] if r['id'] == 'NW_AUD_D10_05')
        added = [texts.index(r['text']) for r in self.excerpts()[0]]
        next_line = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D10_S01_L0016')
        self.assertTrue(all(texts.index(returned) < i < next_line for i in added))
        self.assertEqual(before, self.state.room13)
        self.assertTrue(env['r13_v111_value']('DARAM_DETAINED'))
        self.assertFalse(env['r13_v111_value']('forgery_confirmed'))
        day = self.label('r13_v111_day10')
        self.assertIn("if r13_v111_value('route7')=='murder':", day)
        self.assertIn('jump r13_v111_waiting10', day)
        self.assertIn('jump r13_v111_prevent_hearing10', day)

    def test_tok_uses_actual_hearing_attendance_and_copy_path_has_no_excerpt(self):
        for alive, workshop, hearing in itertools.product((False, True), repeat=3):
            with self.subTest(alive=alive, workshop=workshop, hearing=hearing):
                env = self.load()
                for key, value in [('route7', 'murder'), ('OWL_ALIVE', False), ('TOK_ALIVE', alive),
                                   ('tok_workshop_present', workshop), ('tok_hearing_present', hearing)]:
                    env['r13_v111_set'](key, value)
                attends = self.attendance(env)
                before = copy.deepcopy(self.state.room13)
                label = 'r13_v111_owner_tok10' if attends('hearing') else 'r13_v111_owner_copy10'
                rows = self.rows(env, label)
                texts = [r[1] for r in rows]
                expected = [r['text'] for r in self.excerpts()[1]] if alive and hearing else []
                added_texts = {r['text'] for r in self.excerpts()[1]}
                self.assertEqual([t for t in texts if t in added_texts], expected)
                self.assertEqual(before, self.state.room13, '조회가 증거를 수선하거나 출석·주인·접촉 판정을 완료하지 않는다')
                self.assertFalse(env['r13_v111_value']('D10_S03_owner_tok_completed'))
        gate = self.label('r13_v111_owner_answer10')
        self.assertIn('if r13_v111_tok_attends("hearing"):', gate)
        self.assertIn('jump r13_v111_owner_copy10', gate)
        self.assertIn("['E08_WOUND_WIRE', 'E09_PIN_OWNER'],'r13_v111_owner_answer10'", self.label('r13_v111_owner_proof10'))
        env = self.load()
        rows = self.rows(env, 'r13_v111_owner_tok10')
        texts = [r[1] for r in rows]
        earlier = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D10_S03_L0008')
        later = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D10_S03_L0010')
        self.assertTrue(all(earlier < texts.index(r['text']) < later for r in self.excerpts()[1]))

    def test_owl_whole_exchange_disappears_when_dead_and_does_not_acquire_private_record(self):
        excerpt = self.excerpts()[2]
        self.assertEqual({r.get('when') for r in excerpt}, {'owl_alive'})
        for alive, prevention, result in itertools.product((False, True), ('stone', 'repair'), ('partial', 'win')):
            with self.subTest(alive=alive, prevention=prevention, result=result):
                env = self.load()
                for key, value in [('OWL_ALIVE', alive), ('prevention', prevention), ('meeting:records', result),
                                   ('route7', 'prevented'), ('DARAM_DETAINED', False)]:
                    env['r13_v111_set'](key, value)
                before = copy.deepcopy(self.state.room13)
                rows = env['r13_v111_lines'](['MS14_D10_P01_L0073'])
                texts = [r[1] for r in rows]
                expected = [r['text'] for r in excerpt] if alive else []
                self.assertEqual([t for t in texts if t in {r['text'] for r in excerpt}], expected)
                self.assertEqual(before, self.state.room13)
                self.assertFalse(env['r13_v111_owned']('E10_PUMP'))
                self.assertFalse(env['r13_v111_value']('D10_P01_family_delivery_completed'))
        body = self.label('r13_v111_public_paper10')
        self.assertLess(body.index('MS14_D10_P01_L0073'), body.index('MS14_D10_P01_L0078'))
        self.assertLess(body.index('MS14_D10_P01_L0078'), body.index("r13_v111_commit('MS14_D10_P01_L0083')"))

    def test_viewing_does_not_change_murder_results_suspicion_or_unproven_intent(self):
        for result in ('lose', 'partial', 'win'):
            env = self.load()
            for key, value in [('route7', 'murder'), ('OWL_ALIVE', False), ('meeting:room13', result),
                               ('DARAM_DETAINED', False), ('listed:daram', result == 'lose'),
                               ('grandmother_custody', 'detained' if result == 'win' else 'none'),
                               ('forgery_confirmed', result == 'win'), ('premeditation', 'unproven'),
                               ('interpretation.intentional_strike_vs_struggle_collision', 'not_proven')]:
                env['r13_v111_set'](key, value)
            before = copy.deepcopy(self.state.room13)
            self.rows(env, 'r13_v111_waiting10')
            env['r13_v111_lines'](['MS14_D10_S03_L0008'])
            self.assertEqual(before, self.state.room13)

    def test_matching_separates_full_resident_prose_and_nine_visible_beats(self):
        data = json.loads(DAY_FILE.read_text())
        matching = json.loads(MATCHING.read_text())
        self.assertEqual(matching['day'], 10)
        self.assertEqual([e['id'] for e in matching['scenes']], ['RR10_01', 'RR10_02', 'RR10_03'])
        self.assertEqual([e['pov_name'] for e in matching['scenes']], ['부리', '톡', '부엉이'])
        self.assertEqual(sum(len(e['game_added_ids']) for e in matching['scenes']), 9)
        for entry, excerpt in zip(matching['scenes'], self.excerpts()):
            self.assertTrue(entry['known'] and entry['unknown'])
            self.assertTrue(entry['scene_extent']['manuscript'])
            self.assertTrue(entry['scene_extent']['release_after'])
            self.assertIn(entry['scene_extent']['game_excerpt']['anchor'], self.label(entry['label']))
            self.assertEqual([r['id'] for r in excerpt], entry['game_added_ids'])
            self.assertFalse(any(set(r) & {'effects', 'operations', 'set', 'acquire', 'cut'} for r in excerpt))
            self.assertFalse(any(r.get('kind') == 'thought' for r in excerpt))
        self.assertFalse(any('NW_RR10_' in r['id'] for rows in data['before'].values() for r in rows))
        manuscript = (MATCHING.parent / 'day10_원고.md').read_text()
        for index, part in enumerate(manuscript.split('## ')[1:], 1):
            self.assertTrue(part.startswith(f'{index:02d}. '))
            self.assertIn(' — ', part.splitlines()[0])
            self.assertTrue(900 <= len('\n'.join(part.splitlines()[4:])) <= 1400)


if __name__ == '__main__':
    unittest.main()
