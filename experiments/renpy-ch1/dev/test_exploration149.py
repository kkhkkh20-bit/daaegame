"""돈을 쓰지 않는 선택 탐색의 수령·대여·사용 모델을 SDK 없이 검증한다."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'game/systems/room13_exploration149_model.rpy'


def environment():
    state = SimpleNamespace(
        room13=dict(day=2, period=0, location='market', evidence=['V111:E01'], flags=['lodging'], case_state='pending',
                    v111=dict(gate='morning_finish2', scene='MS14_D02_S01', values={'piko_alive': True},
                              world148={'postal': {'observed': True}}, sidequests={'seam': {'status': 'accepted'}})),
        calm=True, hidden=set(), unready=set(), where={'resident_eunho': 'market', 'karo': 'gate'})
    def value(key): return state.room13.get('v111', {}).get('values', {}).get(key)
    def calm():
        room = state.room13
        return state.calm and room['v111'].get('gate') != 'travel' and not value('DARAM_DETAINED') and room.get('case_state') != 'occurred'
    env = dict(store=state, winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),
               r13_v111_active=lambda: bool(state.room13 and state.room13.get('v111')),
               r13_sidequest_calm=calm, r13_v111_value=value,
               r13_v111_actor_ready=lambda p: p not in state.unready and state.where.get(p) == state.room13['location'],
               r13_v111_person_alive=lambda p: value('alive:' + p) is not False,
               r13_visible_people=lambda: [p for p, place in state.where.items() if place == state.room13['location'] and p not in state.hidden],
               R13_V111_BINDINGS=json.loads((ROOT / 'game/v111/field-bindings.json').read_text()))
    legacy = (ROOT / 'game/systems/room13_livelihood_model.rpy').read_text().split('init 91 python:\n', 1)[1]
    exec(textwrap.dedent(legacy), env)
    exec(textwrap.dedent(SOURCE.read_text().split('init 389 python:\n', 1)[1]), env)
    return env, state


def main_state(state, *, allow_lamp_supply=False):
    room = copy.deepcopy(state.room13)
    room.pop('livelihood', None)
    room['v111'].pop('exploration149', None)
    if allow_lamp_supply: room['v111']['values'].pop('lamp_cord2', None)
    return room


def own(state, *items, cash=None):
    state.room13['livelihood'] = dict(items=list(items), used=[], ledger=[], borrowed={})
    if cash is not None: state.room13['livelihood']['cash'] = cash


def delivery(env, state):
    state.room13['location'] = 'gate'
    own(state, 'cord')
    for part in ('delivery_large_tag', 'delivery_small_tag', 'delivery_box'):
        assert env['r13_ex149_observe'](part)


class Exploration149(unittest.TestCase):
    def test_queries_never_create_money_inventory_or_progress(self):
        env, state = environment();before = copy.deepcopy(state.room13)
        for _ in range(3):
            self.assertEqual(env['r13_ex149_state'](), {})
            self.assertTrue(env['r13_ex149_available']());self.assertFalse(env['r13_ex149_owned']('cord'))
            env['r13_ex149_person_ready']('resident_eunho');env['r13_ex149_delivery_ready']();env['r13_ex149_lamp_ready']('lamp')
        self.assertEqual(state.room13, before)
        for key in ('r13_ex149_price', 'r13_ex149_buy', 'r13_ex149_wallet_open'): self.assertNotIn(key, env)

    def test_receiving_items_uses_real_seller_and_no_money(self):
        for place in ('market', 'store'):
            env, state = environment();state.room13['location'] = state.where['resident_eunho'] = place
            before = main_state(state)
            self.assertTrue(env['r13_ex149_receive']('cord'));self.assertTrue(env['r13_ex149_receive']('weight'))
            items = state.room13['livelihood']
            self.assertEqual(items['items'], ['cord', 'weight'])
            self.assertEqual(items['borrowed']['weight']['owner'], 'resident_eunho')
            self.assertEqual([row['amount'] for row in items['ledger']], [0, 0])
            self.assertNotIn('cash', items);self.assertNotIn('debt', items);self.assertEqual(main_state(state), before)
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_receive']('cord'));self.assertFalse(env['r13_ex149_receive']('weight'))
            self.assertEqual(state.room13, before)

    def test_old_cash_and_debt_are_preserved_and_never_determine_eligibility(self):
        for cash in (0, 99, -10, 'old-format', None):
            env, state = environment();own(state)
            state.room13['livelihood'].update(cash=cash, debt=100)
            self.assertTrue(env['r13_ex149_available']());self.assertTrue(env['r13_ex149_receive']('weight'))
            self.assertTrue(env['r13_ex149_return_weight']())
            self.assertEqual(state.room13['livelihood']['cash'], cash);self.assertEqual(state.room13['livelihood']['debt'], 100)
            self.assertNotIn('travel_money', state.room13['flags']);self.assertNotIn('livelihood_open', state.room13['flags'])

    def test_absent_busy_dead_departed_hidden_seller_cannot_supply_or_receive(self):
        for action in ('receive', 'return'):
            for reason in ('wrong_place', 'hidden', 'unready', 'busy', 'dead', 'departed', 'absent', 'unsafe'):
                env, state = environment()
                if action == 'return': self.assertTrue(env['r13_ex149_receive']('weight'))
                person = 'resident_eunho'
                if reason == 'wrong_place': state.room13['location'] = state.where[person] = 'square'
                elif reason == 'hidden': state.hidden.add(person)
                elif reason == 'unready': state.unready.add(person)
                elif reason == 'busy': state.room13['v111']['values']['busy:' + person] = 'school_transport'
                elif reason == 'dead': state.room13['v111']['values']['alive:' + person] = False
                elif reason == 'departed': state.room13['v111']['values']['departed:' + person] = True
                elif reason == 'absent': state.where[person] = 'store'
                elif reason == 'unsafe': state.calm = False
                before = copy.deepcopy(state.room13)
                result = env['r13_ex149_receive']('cord') if action == 'receive' else env['r13_ex149_return_weight']()
                self.assertFalse(result, (action, reason));self.assertEqual(state.room13, before)

    def test_used_cord_is_not_reissued_but_returned_weight_can_be_borrowed_again(self):
        env, state = environment();own(state);state.room13['livelihood']['used'] = ['cord']
        self.assertFalse(env['r13_ex149_receive']('cord'));self.assertTrue(env['r13_ex149_receive']('weight'))
        self.assertTrue(env['r13_ex149_return_weight']())
        for field in ('items', 'borrowed', 'used'): self.assertNotIn('weight', state.room13['livelihood'][field])
        self.assertFalse(env['r13_ex149_return_weight']());self.assertTrue(env['r13_ex149_receive']('weight'))

    def test_old_owned_weight_is_not_retroactively_treated_as_a_loan(self):
        env, state = environment();own(state, 'weight', cash=12)
        before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_ex149_weight_borrowed']());self.assertFalse(env['r13_ex149_return_weight']())
        self.assertEqual(state.room13, before)
        state.room13['location'] = 'store'
        self.assertTrue(env['r13_ex149_scale_place'](), '직접 소유한 추는 기존대로 쓸 수 있다')

    def test_unknown_items_cannot_be_received(self):
        for item in ('knife', [], None):
            env, state = environment();before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_receive'](item));self.assertEqual(state.room13, before)

    def test_both_labels_and_slipping_box_are_required_before_tying(self):
        parts = ('delivery_large_tag', 'delivery_small_tag', 'delivery_box')
        for missing in parts:
            env, state = environment();state.room13['location'] = 'gate';own(state, 'cord')
            for part in parts:
                if part != missing: self.assertTrue(env['r13_ex149_observe'](part))
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_delivery_ready'](), missing);self.assertFalse(env['r13_ex149_delivery_tie'](), missing)
            self.assertEqual(state.room13, before)

    def test_cargo_observation_requires_actual_scene_and_driver(self):
        for reason in ('wrong_place', 'hidden', 'unready', 'busy'):
            env, state = environment();state.room13['location'] = 'gate'
            if reason == 'wrong_place': state.room13['location'] = 'post'
            elif reason == 'hidden': state.hidden.add('karo')
            elif reason == 'unready': state.unready.add('karo')
            elif reason == 'busy': state.room13['v111']['values']['busy:karo'] = 'family_walk'
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_observe']('delivery_large_tag'));self.assertEqual(state.room13, before)

    def test_tying_and_reporting_are_separate_and_award_only_actual_method(self):
        env, state = environment();delivery(env, state);before = main_state(state);items = copy.deepcopy(state.room13['livelihood'])
        self.assertFalse(env['r13_ex149_delivery_report']());self.assertTrue(env['r13_ex149_delivery_tie']())
        self.assertEqual(state.room13['livelihood'], items);self.assertNotIn('knot_method', env['r13_ex149_state']())
        self.assertTrue(env['r13_ex149_delivery_report']());self.assertTrue(env['r13_ex149_state']()['knot_method'])
        self.assertEqual(state.room13['livelihood'], items);self.assertEqual(main_state(state), before)
        before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_ex149_delivery_tie']());self.assertFalse(env['r13_ex149_delivery_report']());self.assertEqual(state.room13, before)

    def test_tying_needs_cord_and_reporting_needs_karo_present_again(self):
        env, state = environment();delivery(env, state);state.room13['livelihood']['items'] = []
        self.assertFalse(env['r13_ex149_delivery_tie']());state.room13['livelihood']['items'] = ['cord']
        self.assertTrue(env['r13_ex149_delivery_tie']());state.where['karo'] = 'inn';before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_ex149_delivery_report']());self.assertEqual(state.room13, before)

    def test_scale_visible_before_borrowing_but_not_testable_without_weight(self):
        env, state = environment();state.room13['location'] = 'store'
        self.assertTrue(env['r13_ex149_observe']('scale_reference'));before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_ex149_scale_place']());self.assertFalse(env['r13_ex149_observe']('scale_placed'))
        self.assertFalse(env['r13_ex149_observe']('scale_pivot'));self.assertFalse(env['r13_ex149_scale_correct']());self.assertEqual(state.room13, before)

    def test_scale_recheck_records_experience_without_payment_or_discount(self):
        env, state = environment();state.room13['location'] = 'store';own(state, 'weight', cash=11)
        before = main_state(state);items = copy.deepcopy(state.room13['livelihood'])
        self.assertFalse(env['r13_ex149_observe']('scale_pivot'));self.assertTrue(env['r13_ex149_scale_place']())
        self.assertFalse(env['r13_ex149_scale_correct']());self.assertTrue(env['r13_ex149_observe']('scale_pivot'))
        self.assertFalse(env['r13_ex149_scale_correct']());state.where['resident_eunho'] = 'store'
        self.assertTrue(env['r13_ex149_scale_correct']());self.assertTrue(env['r13_ex149_state']()['scale_corrected'])
        self.assertEqual(state.room13['livelihood'], items);self.assertEqual(main_state(state), before)
        self.assertNotIn('scale_rigged', state.room13['flags']);self.assertNotIn('shop_discount', state.room13['flags'])
        before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_ex149_scale_place']());self.assertFalse(env['r13_ex149_scale_correct']());self.assertEqual(state.room13, before)

    def prep_lamp(self, env, state):
        delivery(env, state);self.assertTrue(env['r13_ex149_delivery_tie']());self.assertTrue(env['r13_ex149_delivery_report']())
        state.room13.update(location='square', period=2);state.room13['v111']['gate'] = 'lamp_prep2'
        state.room13['v111']['values']['lamp_latch_seen2'] = True

    def test_method_and_cord_connect_only_to_existing_lamp_supply(self):
        env, state = environment();self.prep_lamp(env, state);before = main_state(state, allow_lamp_supply=True)
        self.assertTrue(env['r13_ex149_lamp_ready']('lamp'));self.assertTrue(env['r13_ex149_lamp_supply']('lamp'))
        self.assertTrue(state.room13['v111']['values']['lamp_cord2']);self.assertNotIn('lamp_bound2', state.room13['v111']['values'])
        items = state.room13['livelihood']
        self.assertNotIn('cord', items['items']);self.assertEqual(items['used'], ['cord']);self.assertNotIn('cash', items)
        self.assertEqual(items['ledger'][-1]['amount'], 0);self.assertEqual(main_state(state, allow_lamp_supply=True), before)
        before = copy.deepcopy(state.room13);self.assertFalse(env['r13_ex149_lamp_supply']('lamp'));self.assertEqual(state.room13, before)

    def test_lamp_rejects_missing_physical_or_authored_requirement(self):
        for reason in ('day3', 'wrong_gate', 'wrong_place', 'wrong_object', 'no_latch', 'no_knot', 'no_cord', 'already_bound', 'already_supplied', 'unsafe', 'missing_binding'):
            env, state = environment();self.prep_lamp(env, state);obj = 'lamp'
            if reason == 'day3': state.room13['day'] = 3
            elif reason == 'wrong_gate': state.room13['v111']['gate'] = 'sleep2'
            elif reason == 'wrong_place': state.room13['location'] = 'gate'
            elif reason == 'wrong_object': obj = 'stone'
            elif reason == 'no_latch': state.room13['v111']['values']['lamp_latch_seen2'] = False
            elif reason == 'no_knot': state.room13['v111']['exploration149']['knot_method'] = False
            elif reason == 'no_cord': state.room13['livelihood']['items'] = []
            elif reason == 'already_bound': state.room13['v111']['values']['lamp_bound2'] = True
            elif reason == 'already_supplied': state.room13['v111']['values']['lamp_cord2'] = True
            elif reason == 'unsafe': state.calm = False
            elif reason == 'missing_binding': env['R13_V111_BINDINGS'] = {}
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_lamp_ready'](obj), reason);self.assertFalse(env['r13_ex149_lamp_supply'](obj), reason)
            self.assertEqual(state.room13, before)

    def test_regular_old_cord_route_remains_unchanged(self):
        env, state = environment();state.room13.update(location='square', period=2);state.room13['v111']['gate'] = 'lamp_prep2'
        state.room13['v111']['values'].update(lamp_cord2=True, lamp_latch_seen2=True);before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_ex149_lamp_ready']('lamp'));self.assertEqual(state.room13, before)
        option = env['R13_V111_BINDINGS']['lamp_prep2']['options'][3]
        self.assertTrue(all(state.room13['v111']['values'].get(key) == value for kind, key, value in option['guard']))

    def test_correct_material_without_method_is_distinguished_without_mutation(self):
        env, state = environment();self.prep_lamp(env, state)
        for method in (None, False, True):
            state.room13['v111']['exploration149']['knot_method'] = method
            before = copy.deepcopy(state.room13)
            self.assertEqual(env['r13_ex149_lamp_needs_method']('lamp'), method is not True)
            self.assertEqual(env['r13_ex149_lamp_ready']('lamp'), method is True)
            self.assertEqual(state.room13, before)
        state.room13['v111']['exploration149'].pop('knot_method')
        self.assertTrue(env['r13_ex149_lamp_needs_method']('lamp'))
        before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_ex149_lamp_supply']('lamp'))
        self.assertEqual(state.room13, before, '방법 안내는 끈·시간·본편 상태를 바꾸지 않는다')

    def test_method_hint_only_for_observed_unfixed_lamp_and_owned_cord(self):
        for reason in ('day3', 'wrong_gate', 'wrong_place', 'wrong_object', 'no_latch', 'no_cord', 'bound', 'supplied', 'unsafe', 'missing_binding'):
            env, state = environment();self.prep_lamp(env, state)
            state.room13['v111']['exploration149'].pop('knot_method');obj = 'lamp'
            if reason == 'day3': state.room13['day'] = 3
            elif reason == 'wrong_gate': state.room13['v111']['gate'] = 'sleep2'
            elif reason == 'wrong_place': state.room13['location'] = 'gate'
            elif reason == 'wrong_object': obj = 'stone'
            elif reason == 'no_latch': state.room13['v111']['values']['lamp_latch_seen2'] = False
            elif reason == 'no_cord': state.room13['livelihood']['items'] = []
            elif reason == 'bound': state.room13['v111']['values']['lamp_bound2'] = True
            elif reason == 'supplied': state.room13['v111']['values']['lamp_cord2'] = True
            elif reason == 'unsafe': state.calm = False
            elif reason == 'missing_binding': env['R13_V111_BINDINGS'] = {}
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_lamp_needs_method'](obj), reason)
            self.assertEqual(state.room13, before)

    def test_days_and_crises_disable_mutations(self):
        for reason in ('day1', 'day8', 'travel', 'unsafe', 'detained', 'incident'):
            env, state = environment()
            if reason == 'day1': state.room13['day'] = 1
            elif reason == 'day8': state.room13['day'] = 8
            elif reason == 'travel': state.room13['v111']['gate'] = 'travel'
            elif reason == 'unsafe': state.calm = False
            elif reason == 'detained': state.room13['v111']['values']['DARAM_DETAINED'] = True
            elif reason == 'incident': state.room13['case_state'] = 'occurred'
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_available']());self.assertFalse(env['r13_ex149_mark']('scale_reference'))
            self.assertFalse(env['r13_ex149_receive']('cord'));self.assertFalse(env['r13_ex149_return_weight']());self.assertEqual(state.room13, before)

    def test_marks_optional_only_and_state_reads_are_copies(self):
        env, state = environment();before = main_state(state)
        self.assertFalse(env['r13_ex149_mark']('piko_alive', False));self.assertFalse(env['r13_ex149_mark']('unknown'))
        self.assertTrue(env['r13_ex149_mark']('scale_reference'));self.assertFalse(env['r13_ex149_mark']('scale_reference'))
        result = env['r13_ex149_state']();result['scale_reference'] = False
        self.assertTrue(env['r13_ex149_state']()['scale_reference']);self.assertEqual(main_state(state), before)

    def test_malformed_item_storage_fails_without_repair_or_write(self):
        for field, value in (('exploration149', None), ('exploration149', []), ('values', [])):
            env, state = environment();state.room13['v111'][field] = value;before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_available']());self.assertFalse(env['r13_ex149_mark']('scale_reference'));self.assertEqual(state.room13, before)
        for items in (None, [], {'items': None}, {'used': 'cord'}, {'items': [{}]}, {'ledger': None}, {'borrowed': []}):
            env, state = environment();state.room13['livelihood'] = items;before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_ex149_owned']('cord'));self.assertFalse(env['r13_ex149_receive']('cord'))
            self.assertFalse(env['r13_ex149_return_weight']());self.assertEqual(state.room13, before)

    def test_store_list_alias_accepts_both_python_and_revertable_style_saved_lists(self):
        class SimulatedRevertableList(list):
            pass
        env, state = environment()
        env['list'] = SimulatedRevertableList
        own(state, 'cord')
        state.room13['livelihood']['used'] = SimulatedRevertableList()
        state.room13['livelihood']['ledger'] = SimulatedRevertableList()
        state.room13['location'] = 'gate'
        before = copy.deepcopy(state.room13)
        self.assertTrue(env['r13_ex149_available']())
        self.assertTrue(env['r13_ex149_owned']('cord'))
        self.assertTrue(env['r13_ex149_person_ready']('karo'))
        self.assertEqual(state.room13, before)
        state.room13['livelihood']['items'] = SimulatedRevertableList(['cord'])
        self.assertTrue(env['r13_ex149_available']())
        state.room13['livelihood']['used'] = 'invalid'
        self.assertFalse(env['r13_ex149_available'](), '기본 list 수용이 잘못된 저장 형태까지 허용하지 않는다')

    def test_missing_campaign_state_does_not_crash_entry_points(self):
        for room in (None, [], {}, {'v111': []}, {'day': True, 'v111': {'values': {}}}):
            env, state = environment();state.room13 = room;before = copy.deepcopy(room)
            self.assertEqual(env['r13_ex149_state'](), {});self.assertFalse(env['r13_ex149_available']())
            self.assertFalse(env['r13_ex149_owned']('cord'));self.assertFalse(env['r13_ex149_receive']('cord'))
            self.assertFalse(env['r13_ex149_observe']('scale_reference'));self.assertFalse(env['r13_ex149_delivery_tie']())
            self.assertFalse(env['r13_ex149_delivery_report']());self.assertFalse(env['r13_ex149_scale_place']())
            self.assertFalse(env['r13_ex149_scale_correct']());self.assertFalse(env['r13_ex149_lamp_supply']('lamp'))
            self.assertFalse(env['r13_ex149_return_weight']());self.assertEqual(state.room13, before)


if __name__ == '__main__': unittest.main()
