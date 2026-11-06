"""13일 담요 양보·학교 준비·고삐 반환 발췌의 순서와 상태 보존을 확인한다."""
import ast
import copy
import itertools
import json
import re
import unittest

from test_newworld_text import Layer, ROOT


DAY_FILE = ROOT / 'game/v111/newworld/d13.json'
MATCHING = ROOT / 'docs/design/resident-reactions-day1314-20261106/day13_매칭.json'


class ResidentDay13(Layer):
    def label(self, name):
        source = (ROOT / 'game/room13_v111_days1114.rpy').read_text()
        return re.search(r'^label ' + name + r':\n(.*?)(?=^label |\Z)', source, re.M | re.S).group(1)

    def rows(self, env, label):
        result = []
        for call in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)', self.label(label)):
            result.extend(env['r13_v111_lines'](ast.literal_eval(call.group(1))))
        return result

    def excerpts(self):
        data = json.loads(DAY_FILE.read_text())
        result = []
        for entry in json.loads(MATCHING.read_text())['scenes']:
            section = entry['scene_extent']['game_excerpt']
            result.append([r for r in data[section['position']][section['anchor']]
                           if r['id'] in entry['game_added_ids']])
        return result

    def render_excerpt(self, env, rows):
        # 독립 추출에서도 실제 overlay의 조건과 패킷 함수를 쓴다.
        return [env['r13_nw_added_line'](row) for row in rows
                if env['R13_NW_WHEN'][row.get('when', 'always')]()]

    def test_pandol_shares_one_blanket_before_future_deal_or_meeting_without_inventory_change(self):
        for piko, fever in itertools.product((False, True), repeat=2):
            env = self.load()
            self.state.room13.update(day=13, period=0, location='school')
            env['r13_v111_set']('piko_alive', piko)
            env['r13_v111_set']('daram_fever12', fever)
            before = copy.deepcopy(self.state.room13)
            rows = self.rows(env, 'r13_v111_blanket_mended13')
            texts = [r[1] for r in rows]
            start = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D13_S01_L0017')
            end = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D13_S01_L0018')
            added = [texts.index(r['text']) for r in self.excerpts()[0]]
            self.assertEqual(added, list(range(start + 1, end)))
            self.assertEqual([rows[i][0] for i in added], [None, 'dad', 'npc_pandol'])
            self.assertEqual(before, self.state.room13, '담요 공유 반응은 물건 추가·기부·자료 획득·미래 거래를 처리하지 않는다')
            self.assertFalse(env['r13_v111_owned']('E13_MENDING'))
            self.assertFalse(env['r13_v111_value']('pandol_blanket_mended'))
        body = self.label('r13_v111_blanket_mended13')
        self.assertLess(body.index('MS14_D13_S01_L0023'), body.index("r13_v111_set('pandol_blanket_mended',True)"))
        self.assertIn('key=\'E13_MENDING\'', body)
        self.assertIn('jump r13_v111_family_exit13', self.label('r13_v111_offer_accept13'))
        self.assertIn('jump r13_v111_blanket_lie13', self.label('r13_v111_offer_refuse13'))

    def test_nabi_prepares_space_without_receiving_patients_and_entire_response_obeys_guard(self):
        env = self.load()
        before = copy.deepcopy(self.state.room13)
        self.assertEqual(self.excerpts()[1], [])
        rows = env['r13_nw_block']('beds_ready13')
        self.assertEqual([r[0] for r in rows], ['nabi'])
        self.assertIn('데려오기만 하세요', rows[0][1])
        self.assertEqual(before, self.state.room13)
        self.assertFalse(env['r13_v111_value']('handover_prepared13'))
        for person in ('npc_pandol', 'resident_momo', 'resident_guldol'):
            self.assertFalse(env['r13_v111_value']('handed:' + person))
        body = self.label('r13_v111_beds_ready13')
        self.assertIn("if r13_v111_actor_ready('nabi'):", body)
        self.assertLess(body.index("r13_nw_block('beds_ready13')"), body.index("r13_v111_set('handover_prepared13',True)"))
        prep = self.label('r13_v111_school_handover_prep13')
        self.assertLess(prep.index("r13_v111_set('handed:nabi',True)"), prep.index('jump r13_v111_nabi_beds13'))
        failed = self.label('r13_v111_mending_wrong13')
        self.assertIn("r13_v111_set('cart_departed',True)", failed)
        self.assertIn('jump r13_v111_departed_night13', failed)
        self.assertNotIn('r13_v111_school_handover_prep13', failed)

    def test_karo_gives_reins_to_present_owner_before_original_return_completion(self):
        env = self.load()
        rows = self.rows(env, 'r13_v111_cart_return13')
        texts = [r[1] for r in rows]
        owner = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D13_S04_L0084')
        empty = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D13_S04_L0085')
        next_row = next(i for i, r in enumerate(rows) if r[2].get('line_id') == 'MS14_D13_S04_L0086')
        added = [texts.index(r['text']) for r in self.excerpts()[2]]
        self.assertTrue(owner < empty < min(added) < max(added) < next_row)
        self.assertEqual([rows[i][0] for i in added], ['karo', 'resident_eunho', 'karo'])
        body = self.label('r13_v111_cart_return13')
        self.assertIn("r13_v111_arrive(['karo', 'guard', 'resident_badook', 'resident_eunho'])", body)
        self.assertIn("if r13_v111_actor_ready('karo'):", body)
        self.assertLess(body.index('MS14_D13_S04_L0086'), body.index("r13_v111_set('cart_returned',True)"))
        self.assertFalse(env['r13_v111_value']('cart_returned'))
        self.assertFalse(env['r13_v111_value']('escort_gear_returned'))
        self.assertEqual({r.get('when') for r in self.excerpts()[2]}, {'karo_ready'})
        ready = env['r13_v111_actor_ready']
        env['r13_v111_actor_ready'] = lambda person: False if person == 'karo' else ready(person)
        self.assertEqual(self.render_excerpt(env, self.excerpts()[2]), [], '까로 부재 때 주인의 응답만 남기지 않는다')

    def test_return_reaction_does_not_finish_other_transport_steps_or_restore_departed_people(self):
        for family, stopped, relay, refused in itertools.product(('square', 'school'), (False, True), (False, True), (False, True)):
            env = self.load()
            self.state.room13.update(day=13, period=2, location='square')
            for key, value in [('family_location', family), ('current_order_execution_stopped', stopped),
                               ('relay_stopped', relay), ('Kkaro_forced_transport_refused', refused),
                               ('all_cart_handed', True), ('listed:daram', True), ('handed:daram', True),
                               ('departed:resident_owlgp', True), ('cart_returned', False),
                               ('escort_gear_returned', False), ('current_transport_chain_stopped', False)]:
                env['r13_v111_set'](key, value)
            before = copy.deepcopy(self.state.room13)
            env['r13_v111_lines'](['MS14_D13_S04_L0085'])
            self.assertEqual(before, self.state.room13)
        last_cart = self.label('r13_v111_last_cart13')
        self.assertLess(last_cart.index('if not all('), last_cart.index("r13_v111_set('all_cart_handed',True)"))
        self.assertLess(last_cart.index("r13_v111_set('all_cart_handed',True)"), last_cart.index('jump r13_v111_transport_cleanup13'))
        self.assertIn('"relay_stopped"', self.label('r13_v111_night_finish13'))
        self.assertIn('"cart_returned"', self.label('r13_v111_night_finish13'))

    def test_matching_separates_full_prose_from_six_added_beats(self):
        matching = json.loads(MATCHING.read_text())
        self.assertEqual(matching['day'], 13)
        self.assertEqual([e['id'] for e in matching['scenes']], ['RR13_01', 'RR13_02', 'RR13_03'])
        self.assertEqual([e['pov_name'] for e in matching['scenes']], ['판돌', '나비', '까로'])
        self.assertEqual(sum(len(e['game_added_ids']) for e in matching['scenes']), 6)
        self.assertEqual(matching['scenes'][1]['game_existing_ids'], ['NW_D13_BR01'])
        for entry, rows in zip(matching['scenes'], self.excerpts()):
            self.assertTrue(entry['known'] and entry['unknown'])
            self.assertTrue(entry['scene_extent']['manuscript'])
            self.assertTrue(entry['scene_extent']['release_after'])
            self.assertIn(entry['scene_extent']['game_excerpt']['anchor'], self.label(entry['label']))
            self.assertEqual([r['id'] for r in rows], entry['game_added_ids'])
            self.assertFalse(any(set(r) & {'effects', 'operations', 'set', 'acquire', 'cut'} for r in rows))
            self.assertFalse(any(r.get('kind') == 'thought' for r in rows))
        manuscript = (MATCHING.parent / 'day13_원고.md').read_text()
        for index, part in enumerate(manuscript.split('## ')[1:], 1):
            self.assertTrue(part.startswith(f'{index:02d}. '))
            self.assertIn(' — ', part.splitlines()[0])
            self.assertTrue('\n'.join(part.splitlines()[4:]).strip(), '주민 원고 본문이 비어 있다')


if __name__ == '__main__':
    unittest.main()
