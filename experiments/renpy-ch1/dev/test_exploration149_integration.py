"""149 모델과 화면용 Python API를 함께 로드해 본편과의 접점을 검증한다.

Ren'Py 화면·라벨을 실행하지 않는다. 실제 대사 등록·모델·통합 함수를
그대로 읽고, 배치·화면 Action만 대역으로 제공한다.
"""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

from dev.test_exploration149 import environment as model_environment, delivery, own


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'game/systems/room13_exploration149.rpy'
HUB = ROOT / 'game/room13_v111.rpy'


def environment():
    env, state = model_environment()
    state.r13_ex149_scale_on_pan = False
    state.r13_ex149_held = None
    state.questions = []
    state.base_places = ['inn', 'square', 'post', 'store', 'gate']
    env.update(
        json=json,
        renpy=SimpleNamespace(file=lambda path: open(ROOT / 'game' / path, encoding='utf-8')),
        r13_nw_added_line=lambda row: dict(row),
        r13_v111_questions=lambda person: list(state.questions),
        r13_v111_has_business=lambda person: False,
        r13_v111_public_revisit_places=lambda: list(state.base_places),
        Return=lambda value: SimpleNamespace(value=value),
        R13_LIFE_SCENES={
            'delivery': {'before': 'delivery-before', 'after': 'delivery-after'},
            'scale_base': {'before': 'scale-before'},
            'scale_loaded': {'before': 'scale-loaded'},
        },
    )
    block = SOURCE.read_text().split('init 390 python:\n', 1)[1].split('\nscreen ', 1)[0]
    exec(textwrap.dedent(block), env)
    return env, state


def held_guard(env, state, kind, *, target='lamp', options=()):
    """현재 허브의 실제 선택 물품 해제 조건을 모델 상태에 대입한다."""
    prefix = 'if r13_ex149_held and not r13_ex149_lamp_ready' if kind == 'object' else 'if r13_ex149_held and any('
    line = next(row.strip() for row in HUB.read_text().splitlines() if row.strip().startswith(prefix))
    condition = line[3:-1]
    return eval(condition, dict(env, r13_ex149_held=state.r13_ex149_held,
                               room13=state.room13, v111_person=target,
                               v111_pick=(kind, target), v111_binding={'options': list(options)}))


class Exploration149Integration(unittest.TestCase):
    def test_opening_world_map_and_inspecting_notes_never_grants_money_or_facts(self):
        env, state = environment()
        before = copy.deepcopy(state.room13)
        for _ in range(4):
            self.assertIn('market', env['r13_v111_public_revisit_places']())
            env['r13_ex149_topics']('resident_eunho')
            env['r13_v111_questions']('resident_eunho')
            env['r13_v111_has_business']('resident_eunho')
            self.assertEqual(env['r13_ex149_notes'](), [])
            env['r13_ex149_object']('market_cloth')
            env['r13_ex149_lines']('market_intro')
        self.assertEqual(state.room13, before)
        self.assertNotIn('livelihood', state.room13)
        self.assertNotIn('exploration149', state.room13['v111'])

    def test_market_public_visit_never_bypasses_unsafe_main_state(self):
        for reason in ('day1', 'day8', 'travel', 'detained', 'incident', 'unsafe'):
            env, state = environment()
            if reason == 'day1': state.room13['day'] = 1
            elif reason == 'day8': state.room13['day'] = 8
            elif reason == 'travel': state.room13['v111']['gate'] = 'travel'
            elif reason == 'detained': state.room13['v111']['values']['DARAM_DETAINED'] = True
            elif reason == 'incident': state.room13['case_state'] = 'occurred'
            elif reason == 'unsafe': state.calm = False
            before = copy.deepcopy(state.room13)
            self.assertNotIn('market', env['r13_v111_public_revisit_places'](), reason)
            self.assertEqual(env['r13_ex149_topics']('resident_eunho'), [], reason)
            self.assertFalse(env['r13_ex149_object']('market_cloth'), reason)
            self.assertEqual(state.room13, before)

    def test_corrupt_wallet_disables_screen_entry_functions_without_writes(self):
        for wallet in (None, [], {'cash': 20, 'items': None}, {'borrowed': []}):
            env, state = environment()
            state.room13['livelihood'] = wallet
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_available']())
            self.assertEqual(env['r13_ex149_topics']('resident_eunho'), [])
            self.assertNotIn('market', env['r13_v111_public_revisit_places']())
            self.assertEqual(state.room13, before)

    def test_extra_questions_keep_original_main_returns_before_optional_choices(self):
        env, state = environment()
        main = ('기존 본편 질문', SimpleNamespace(value=3), False)
        other = ('기존 주민 질문', SimpleNamespace(value=('resident_chat', 'work')), False)
        state.questions = [main, other]
        rows = env['r13_v111_questions']('resident_eunho')
        self.assertIs(rows[0], main)
        self.assertEqual(rows[1][1].value, ('exploration149', 'shop'))
        self.assertIs(rows[2], other)
        self.assertTrue(env['r13_v111_has_business']('resident_eunho'))

    def test_owner_questions_follow_actual_location_and_read_history(self):
        env, state = environment()
        self.assertEqual([row[1] for row in env['r13_ex149_topics']('resident_eunho')], ['shop'])
        self.assertFalse(env['r13_ex149_topics']('resident_eunho')[0][2])
        env['r13_ex149_mark']('intro_seen')
        self.assertTrue(env['r13_ex149_topics']('resident_eunho')[0][2])
        state.room13['location'] = 'store'
        self.assertEqual(env['r13_ex149_topics']('resident_eunho'), [], '시장에 있는 사람을 창고에 복제하지 않는다')
        state.where['resident_eunho'] = 'store'
        own(state, 'weight')
        env['r13_ex149_scale_place']()
        self.assertEqual([row[1] for row in env['r13_ex149_topics']('resident_eunho')], ['shop'])
        env['r13_ex149_observe']('scale_pivot')
        self.assertEqual([row[1] for row in env['r13_ex149_topics']('resident_eunho')], ['shop', 'scale_report'])

    def test_picture_switches_only_for_actual_tied_cargo_and_current_pan_state(self):
        env, state = environment()
        self.assertEqual(env['r13_ex149_picture']('delivery'), 'delivery-before')
        delivery(env, state)
        self.assertTrue(env['r13_ex149_delivery_tie']())
        self.assertEqual(env['r13_ex149_picture']('delivery'), 'delivery-after')
        env['r13_ex149_delivery_report']()
        self.assertEqual(env['r13_ex149_picture']('scale'), 'scale-before')
        state.r13_ex149_scale_on_pan = True
        self.assertEqual(env['r13_ex149_picture']('scale'), 'scale-loaded')
        state.r13_ex149_scale_on_pan = False
        self.assertEqual(env['r13_ex149_picture']('scale'), 'scale-before')

    def test_recorded_methods_require_completed_actions_not_ownership_alone(self):
        env, state = environment()
        own(state, 'cord', 'weight')
        self.assertEqual(env['r13_ex149_notes'](), [])
        delivery(env, state)
        self.assertFalse(any('배웠다' in note for note in env['r13_ex149_notes']()))
        env['r13_ex149_delivery_tie']()
        self.assertFalse(any('배웠다' in note for note in env['r13_ex149_notes']()))
        env['r13_ex149_delivery_report']()
        self.assertTrue(any('배웠다' in note for note in env['r13_ex149_notes']()))
        state.room13['location'] = state.where['resident_eunho'] = 'store'
        own(state, 'cord', 'weight')
        env['r13_ex149_scale_place']()
        self.assertFalse(any('눈금을 맞췄다' in note for note in env['r13_ex149_notes']()))
        env['r13_ex149_observe']('scale_pivot')
        env['r13_ex149_scale_correct']()
        self.assertTrue(any('눈금을 맞췄다' in note for note in env['r13_ex149_notes']()))
        self.assertFalse(any('한 냥' in note or '할인' in note or '깎아' in note
                             for note in env['r13_ex149_notes']()))

    def test_held_items_yield_to_both_main_person_and_main_object(self):
        env, state = environment()
        state.room13['location'] = 'square'
        state.r13_ex149_held = 'weight'
        self.assertTrue(held_guard(env, state, 'person', target='resident_lamplighter',
                                   options=[{'person': 'resident_lamplighter', 'location': 'square', 'index': 1}]))
        self.assertTrue(held_guard(env, state, 'object', target='lamp',
                                   options=[{'object': 'lamp', 'location': 'square', 'index': 2}]))
        self.assertFalse(held_guard(env, state, 'object', target='lamp',
                                    options=[{'object': 'lamp', 'location': 'gate', 'index': 2}]))

    def test_only_the_valid_new_lamp_method_keeps_cord_selection_before_main_dispatch(self):
        env, state = environment()
        delivery(env, state)
        env['r13_ex149_delivery_tie']()
        env['r13_ex149_delivery_report']()
        state.room13.update(location='square', period=2)
        state.room13['v111']['gate'] = 'lamp_prep2'
        state.room13['v111']['values']['lamp_latch_seen2'] = True
        state.r13_ex149_held = 'cord'
        options = [{'object': 'lamp', 'location': 'square', 'index': 3}]
        self.assertFalse(held_guard(env, state, 'object', options=options))
        state.room13['v111']['values']['lamp_bound2'] = True
        self.assertTrue(held_guard(env, state, 'object', options=options))

    def test_optional_object_handler_is_restricted_to_the_two_existing_objects(self):
        env, state = environment()
        for place, obj, expected in (('market', 'market_cloth', True), ('market', 'market_cheese', False),
                                     ('store', 'scale', True), ('store', 'ledger', False),
                                     ('room13', 'desk', False), ('square', 'lamp', False)):
            state.room13['location'] = place
            self.assertEqual(env['r13_ex149_object'](obj), expected, (place, obj))

    def test_actual_loan_can_be_returned_and_requested_again_without_dead_report_question(self):
        env, state = environment()
        self.assertTrue(env['r13_ex149_receive']('weight'))
        self.assertTrue(env['r13_ex149_weight_borrowed']())
        self.assertIn('return_weight', [row[1] for row in env['r13_ex149_topics']('resident_eunho')])
        state.room13['location'] = state.where['resident_eunho'] = 'store'
        env['r13_ex149_scale_place']();env['r13_ex149_observe']('scale_pivot')
        self.assertIn('scale_report', [row[1] for row in env['r13_ex149_topics']('resident_eunho')])
        self.assertTrue(env['r13_ex149_return_weight']())
        actions = [row[1] for row in env['r13_ex149_topics']('resident_eunho')]
        self.assertNotIn('return_weight', actions)
        self.assertNotIn('scale_report', actions)
        self.assertTrue(env['r13_ex149_receive']('weight'))
        self.assertIn('scale_report', [row[1] for row in env['r13_ex149_topics']('resident_eunho')])
        self.assertNotIn('cash', state.room13['livelihood'])


if __name__ == '__main__':
    unittest.main()
