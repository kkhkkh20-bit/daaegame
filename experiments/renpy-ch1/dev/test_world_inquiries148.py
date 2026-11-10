"""현장 관찰·주민별 지식·선택 생활 분기의 독립 상태 계약을 검증한다.

Ren'Py SDK 대신 init Python 블록만 실행한다. 본편 상태와 증거를 바꾸지
않으면서 실제 현장에 있는 사람에게만 새 질문이 생기는지 확인한다.
"""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'game/systems/room13_world_inquiries148.rpy'
DATA = json.loads((ROOT / 'game/v111/world-inquiries148.json').read_text())['threads']


def environment():
    owners = {row['owner'] for row in DATA.values()}
    state = SimpleNamespace(
        room13=dict(day=2, period=1, location='square', coins=17,
                    evidence=['V111:E01'], flags=['entry_corrected'],
                    case_state='pending',
                    v111=dict(gate='morning_finish2', scene='MS14_D02_S01',
                              values={}, sidequests={'seam': {'status': 'accepted'}},
                              village_visits={'postcard': {'status': 'noticed'}})),
        calm=True, companion=True, options=[], hidden=set(), unready=set(),
        where={row['owner']: row['sources'][0]['location'] for row in DATA.values()},
        questions=[],
    )
    speakers = {'아빠': 'dad', '다람': 'daram', **{
        row['owner_name']: row['owner'] for row in DATA.values()}}
    def value(key):
        return state.room13['v111']['values'].get(key)
    def calm():
        return (state.calm and 2 <= state.room13['day'] <= 7
                and state.room13['v111']['gate'] != 'travel')
    env = dict(
        store=state, json=json, winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),
        renpy=SimpleNamespace(file=lambda path: open(ROOT / 'game' / path, encoding='utf-8')),
        ROOM13=json.loads((ROOT / 'game/room13-content.json').read_text()),
        CAST={p: {} for p in owners | {'dad', 'daram'}}, MS14_SPEAKERS=speakers,
        R13_NAMES={row['owner']: row['owner_name'] for row in DATA.values()},
        R13_PLACES={place: (place, '') for place in json.loads((ROOT / 'game/room13-content.json').read_text())['objects']},
        r13_v111_active=lambda: bool(state.room13.get('v111')),
        r13_v111_value=value,
        r13_v111_owned=lambda key: 'V111:' + key in state.room13['evidence'],
        r13_sidequest_calm=calm,
        r13_v111_binding=lambda: dict(options=state.options),
        r13_v111_actor_ready=lambda p: p not in state.unready and state.where.get(p) == state.room13['location'],
        r13_v111_person_alive=lambda p: value('alive:' + p) is not False,
        r13_visible_people=lambda: [p for p, place in state.where.items()
                                   if place == state.room13['location'] and p not in state.hidden],
        r13_where=lambda p: state.where.get(p),
        r13_nw_added_line=lambda row: row,
        r13_v111_resident_companion_ok=lambda p: state.companion,
        r13_v111_questions=lambda p: list(state.questions),
        r13_v111_has_business=lambda p: False,
        r13_population146_side_people=lambda: {'resident_yeoni'},
        r13_sidequest_tasks146=lambda: [],
        Return=lambda value: SimpleNamespace(value=value),
    )
    block = SOURCE.read_text().split('init 387 python:\n', 1)[1].split('\nlabel ', 1)[0]
    exec(textwrap.dedent(block), env)
    return env, state


def main_state(state):
    result = copy.deepcopy(state.room13)
    result['v111'].pop('world148', None)
    return result


def prepare(env, state, key, *, owner=False, evidence=True):
    spec = DATA[key]
    source = spec['sources'][0]
    state.room13['location'] = source['location']
    state.room13['day'] = max(3 if key in ('seat', 'tools') else 2, spec['days'][0])
    if key == 'aftermath':
        state.room13['day'] = 7
        state.room13['v111']['values'].update(
            D06_S03P_empty_fire_completed=True,
            warehouse_children_school_handover=4, KKOMI_ALIVE=True)
    if evidence and key in ('postal', 'seat', 'tools'):
        state.room13['evidence'].append('V111:' + {'postal': 'E07', 'seat': 'E09', 'tools': 'E12'}[key])
    if key == 'seat':
        state.room13['v111']['values']['piko_alive'] = True
    if owner:
        state.where[spec['owner']] = state.room13['location']
    return source


class WorldInquiries148(unittest.TestCase):
    def observe(self, env, state, key, **kwargs):
        source = prepare(env, state, key, **kwargs)
        self.assertTrue(env['r13_world148_record'](key, 'observe'))
        return source

    def actions(self, env, key):
        return [row['action'] for row in env['r13_world148_person_actions'](DATA[key]['owner'])
                if row['thread'] == key]

    def test_catalogue_uses_existing_background_objects(self):
        content = json.loads((ROOT / 'game/room13-content.json').read_text())
        self.assertEqual(set(DATA), {'light', 'postal', 'seat', 'tools', 'school', 'aftermath'})
        for key, spec in DATA.items():
            with self.subTest(thread=key):
                for source in spec['sources'] + [spec['task']]:
                    self.assertIn(source['object'], content['objects'][source['location']])
                self.assertEqual({choice['result'] for choice in spec['choices']}, {'help', 'listen', 'later'})
        env, _ = environment()
        self.assertEqual(env['r13_world148_problems'](), [])

    def test_observation_journal_does_not_promise_a_question_before_prerequisite(self):
        for key, evidence in (('postal', 'E07'), ('tools', 'E12')):
            env, state = environment()
            source = prepare(env, state, key, owner=True)
            state.room13['evidence'] = ['V111:E01']
            self.assertTrue(env['r13_world148_record'](key, 'observe'))
            before = copy.deepcopy(state.room13)
            entry = next(r for r in env['r13_world148_journal']() if r['title'] == DATA[key]['title'])
            self.assertNotIn('물어볼 수', entry['objective'])
            self.assertEqual(self.actions(env, key), [])
            self.assertEqual(state.room13, before)
            state.room13['evidence'].append('V111:' + evidence)
            entry = next(r for r in env['r13_world148_journal']() if r['title'] == DATA[key]['title'])
            self.assertIn('물어볼 수', entry['objective'])
            self.assertEqual(self.actions(env, key), ['ask'])

    def test_queries_are_pure_and_leave_existing_saved_state_intact(self):
        env, state = environment()
        for key in DATA:
            source = prepare(env, state, key, owner=True)
            before = copy.deepcopy(state.room13)
            for _ in range(3):
                env['r13_world148_state'](key)
                env['r13_world148_variants'](key)
                env['r13_world148_source_allowed'](key, source['object'])
                env['r13_world148_object_actions'](source['object'])
                env['r13_world148_person_actions'](DATA[key]['owner'])
                env['r13_v111_questions'](DATA[key]['owner'])
                env['r13_v111_has_business'](DATA[key]['owner'])
                env['r13_population146_side_people']()
                env['r13_world148_lines'](key, 'intro')
                env['r13_world148_journal']()
            self.assertEqual(state.room13, before)

    def test_observation_does_not_invent_hearing_help_or_new_evidence(self):
        for key in DATA:
            with self.subTest(thread=key):
                env, state = environment()
                source = prepare(env, state, key, evidence=False)
                before = main_state(state)
                self.assertTrue(env['r13_world148_record'](key, 'observe'))
                row = env['r13_world148_state'](key)
                self.assertTrue(row['observed'])
                self.assertEqual(row['source_place'], source['location'])
                self.assertEqual(row['observed_fact'], source['fact'])
                self.assertNotIn('result', row)
                self.assertNotIn('worked', row)
                self.assertEqual(main_state(state), before)
                journal = env['r13_world148_journal']()
                self.assertEqual(len(journal), 1)
                self.assertEqual(journal[0]['status'], '현장에서 본 것')
                self.assertEqual(journal[0]['fact'], source['fact'])

    def test_unobserved_objects_never_add_owner_questions_or_journal_entries(self):
        env, state = environment()
        for key in DATA:
            prepare(env, state, key, owner=True)
            self.assertEqual(self.actions(env, key), [])
        self.assertEqual(env['r13_world148_journal'](), [])

    def test_question_prerequisites_do_not_prevent_reading_visible_objects(self):
        for key, evidence in (('postal', 'E07'), ('seat', 'E09'), ('tools', 'E12')):
            with self.subTest(thread=key):
                env, state = environment()
                self.observe(env, state, key, owner=True, evidence=False)
                self.assertEqual(self.actions(env, key), [])
                snapshot = copy.deepcopy(state.room13)
                self.assertFalse(env['r13_world148_record'](key, 'choose', 'listen'))
                self.assertEqual(state.room13, snapshot)
                state.room13['evidence'].append('V111:' + evidence)
                self.assertEqual(self.actions(env, key), ['ask'])

    def test_empty_lamp_evidence_does_not_imply_knowledge_of_tool_loans(self):
        env, state = environment()
        self.observe(env, state, 'tools', owner=True, evidence=False)
        state.room13['evidence'].append('V111:E10')
        before = copy.deepcopy(state.room13)
        self.assertEqual(self.actions(env, 'tools'), [])
        self.assertFalse(env['r13_world148_record']('tools', 'choose', 'listen'))
        self.assertEqual(state.room13, before)
        state.room13['evidence'].append('V111:E12')
        self.assertEqual(self.actions(env, 'tools'), ['ask'])

    def test_dead_piko_requires_each_owner_to_have_heard_the_news(self):
        env, state = environment()
        self.observe(env, state, 'seat', owner=True)
        values = state.room13['v111']['values']
        values.update(piko_alive=False)
        values['piko_news3:buri'] = True
        before = copy.deepcopy(state.room13)
        self.assertEqual(self.actions(env, 'seat'), [])
        self.assertNotIn('piko_dead', env['r13_world148_variants']('seat'))
        self.assertEqual(state.room13, before)
        values['piko_news3:nabi'] = True
        self.assertEqual(self.actions(env, 'seat'), ['ask'])
        self.assertIn('piko_dead', env['r13_world148_variants']('seat'))
        values['piko_news3:buri'] = False
        self.assertNotIn('piko_dead', env['r13_world148_variants']('tools'))

    def test_surviving_piko_never_uses_the_death_variant(self):
        env, state = environment()
        self.observe(env, state, 'seat', owner=True)
        state.room13['v111']['values'].update(piko_alive=True)
        state.room13['v111']['values']['piko_news3:nabi'] = True
        self.assertEqual(self.actions(env, 'seat'), ['ask'])
        variants = env['r13_world148_variants']('seat')
        self.assertIn('piko_safe', variants)
        self.assertNotIn('piko_dead', variants)

    def test_portrait_without_confirmed_piko_state_cannot_start_seat_conversation(self):
        env, state = environment()
        self.observe(env, state, 'seat', owner=True)
        state.room13['v111']['values'].pop('piko_alive')
        before = copy.deepcopy(state.room13)
        self.assertEqual(self.actions(env, 'seat'), [])
        self.assertFalse(env['r13_world148_record']('seat', 'choose', 'listen'))
        self.assertEqual(state.room13, before)

    def test_help_is_a_promise_until_the_actual_task_object_is_selected(self):
        for key in DATA:
            with self.subTest(thread=key):
                env, state = environment()
                source = self.observe(env, state, key, owner=True)
                before = main_state(state)
                self.assertTrue(env['r13_world148_record'](key, 'choose', 'help'))
                self.assertEqual(main_state(state), before)
                self.assertFalse(env['r13_world148_state'](key).get('worked'))
                self.assertEqual(self.actions(env, key), ['reminder'])
                entry = env['r13_world148_journal']()[0]
                self.assertEqual(entry['status'], '도울 차례')
                self.assertEqual(entry['fact'], source['fact'], '도움 수락은 듣기 전용 설명이나 완료한 일을 기록하지 않는다')
                self.assertNotEqual(entry['fact'], DATA[key]['facts']['learned'])
                self.assertNotEqual(entry['fact'], DATA[key]['facts']['helped'])
                self.assertIn('에서 관찰', entry['source'])
                task = DATA[key]['task']
                state.room13['location'] = task['location']
                work = [row for row in env['r13_world148_object_actions'](task['object'])
                        if row['thread'] == key]
                self.assertEqual([row['action'] for row in work], ['work'])
                before = main_state(state)
                self.assertTrue(env['r13_world148_record'](key, 'work'))
                self.assertEqual(main_state(state), before)
                self.assertTrue(env['r13_world148_state'](key)['worked'])
                entry = env['r13_world148_journal']()[0]
                self.assertEqual(entry['status'], '직접 해본 일')
                self.assertEqual(entry['fact'], DATA[key]['facts']['helped'])
                self.assertIn('직접 확인', entry['source'])
                snapshot = copy.deepcopy(state.room13)
                self.assertFalse(env['r13_world148_record'](key, 'work'))
                self.assertEqual(state.room13, snapshot)

    def test_listening_creates_no_completed_work_and_choices_cannot_be_replaced(self):
        for key in DATA:
            env, state = environment()
            self.observe(env, state, key, owner=True)
            before = main_state(state)
            self.assertTrue(env['r13_world148_record'](key, 'choose', 'listen'))
            self.assertEqual(main_state(state), before)
            snapshot = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_world148_record'](key, 'work'))
            self.assertFalse(env['r13_world148_record'](key, 'choose', 'help'))
            self.assertEqual(state.room13, snapshot)
            row = env['r13_world148_state'](key)
            self.assertEqual(row['result'], 'listen')
            self.assertNotIn('worked', row)
            entry = env['r13_world148_journal']()[0]
            self.assertEqual(entry['fact'], DATA[key]['facts']['learned'])
            self.assertNotEqual(entry['fact'], DATA[key]['facts']['helped'])
            self.assertIn('에게 들음', entry['source'])

    def test_later_and_invalid_actions_consume_no_optional_or_main_state(self):
        for action, result in (('choose', 'later'), ('choose', 'unknown'), ('choose', None),
                               ('work', None), ('memory', None), ('unexpected', None)):
            env, state = environment()
            self.observe(env, state, 'light', owner=True)
            snapshot = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_world148_record']('light', action, result))
            self.assertEqual(state.room13, snapshot)
            self.assertEqual(self.actions(env, 'light'), ['ask'])
        env, state = environment()
        before = copy.deepcopy(state.room13)
        self.assertFalse(env['r13_world148_record']('unknown', 'observe'))
        self.assertEqual(state.room13, before)

    def test_unavailable_owner_pauses_question_without_erasing_observation(self):
        for reason in ('hidden', 'unready', 'elsewhere', 'busy', 'departed', 'dead'):
            with self.subTest(reason=reason):
                env, state = environment()
                self.observe(env, state, 'light', owner=True)
                person = DATA['light']['owner']
                if reason == 'hidden': state.hidden.add(person)
                elif reason == 'unready': state.unready.add(person)
                elif reason == 'elsewhere': state.where[person] = 'post'
                elif reason == 'busy': state.room13['v111']['values']['busy:' + person] = 'medical_call'
                elif reason == 'departed': state.room13['v111']['values']['departed:' + person] = True
                elif reason == 'dead': state.room13['v111']['values']['alive:' + person] = False
                snapshot = copy.deepcopy(state.room13)
                self.assertEqual(self.actions(env, 'light'), [])
                self.assertFalse(env['r13_world148_record']('light', 'choose', 'help'))
                self.assertTrue(env['r13_world148_state']('light')['observed'])
                self.assertEqual(state.room13, snapshot)

    def test_observation_is_possible_without_the_owner_being_present(self):
        env, state = environment()
        source = prepare(env, state, 'school')
        person = DATA['school']['owner']
        state.where[person] = 'inn'
        self.assertTrue(env['r13_world148_source_allowed']('school', source['object']))
        self.assertTrue(env['r13_world148_record']('school', 'observe'))
        self.assertEqual(self.actions(env, 'school'), [])

    def test_main_object_binding_has_priority_over_both_observation_and_work(self):
        for stage in ('observe', 'work'):
            for key in DATA:
                with self.subTest(thread=key, stage=stage):
                    env, state = environment()
                    source = prepare(env, state, key, owner=True)
                    if stage == 'work':
                        self.assertTrue(env['r13_world148_record'](key, 'observe'))
                        self.assertTrue(env['r13_world148_record'](key, 'choose', 'help'))
                    target = DATA[key]['task'] if stage == 'work' else source
                    state.room13['location'] = target['location']
                    state.options = [dict(location=target['location'], object=target['object'], index=0)]
                    snapshot = copy.deepcopy(state.room13)
                    self.assertEqual(env['r13_world148_object_actions'](target['object']), [])
                    self.assertFalse(env['r13_world148_record'](key, stage))
                    self.assertEqual(state.room13, snapshot)
                    state.options[0]['location'] = 'unrelated_place'
                    self.assertTrue(env['r13_world148_object_actions'](target['object']))

    def test_wrong_scene_object_and_unsafe_time_cannot_write_progress(self):
        for reason in ('wrong_place', 'wrong_object', 'unsafe', 'travel', 'day1', 'day8'):
            env, state = environment()
            source = prepare(env, state, 'light', owner=True)
            obj = source['object']
            if reason == 'wrong_place': state.room13['location'] = 'post'
            elif reason == 'wrong_object': obj = 'parcels'
            elif reason == 'unsafe': state.calm = False
            elif reason == 'travel': state.room13['v111']['gate'] = 'travel'
            elif reason == 'day1': state.room13['day'] = 1
            elif reason == 'day8': state.room13['day'] = 8
            snapshot = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_world148_source_allowed']('light', obj), reason)
            if reason != 'wrong_object':
                self.assertFalse(env['r13_world148_record']('light', 'observe'), reason)
            self.assertEqual(state.room13, snapshot)

    def test_listening_waits_for_later_memory_but_completed_help_can_be_reported_now(self):
        for result in ('help', 'listen'):
            env, state = environment()
            self.observe(env, state, 'light', owner=True)
            self.assertTrue(env['r13_world148_record']('light', 'choose', result))
            self.assertNotIn('memory', self.actions(env, 'light'))
            if result == 'help':
                self.assertTrue(env['r13_world148_record']('light', 'work'))
            else:
                self.assertFalse(env['r13_world148_record']('light', 'memory'))
                state.room13['period'] = 2
            before = main_state(state)
            self.assertEqual(self.actions(env, 'light'), ['memory'])
            self.assertTrue(env['r13_world148_record']('light', 'memory'))
            self.assertEqual(main_state(state), before)
            row = env['r13_world148_state']('light')
            self.assertEqual(row['result'], result)
            self.assertEqual(bool(row.get('worked')), result == 'help')
            if result == 'help':
                self.assertTrue(row['report_seen'])
            else:
                entries = env['r13_world148_person_actions'](DATA['light']['owner'])
                self.assertTrue(entries[0]['read'])

    def test_reinspection_never_replaces_first_source_or_choice(self):
        env, state = environment()
        self.observe(env, state, 'light', owner=True)
        env['r13_world148_record']('light', 'choose', 'listen')
        first = env['r13_world148_state']('light')
        state.room13['day'] = 4
        self.assertTrue(env['r13_world148_record']('light', 'observe'))
        self.assertEqual(env['r13_world148_state']('light'), first)
        first['result'] = 'help'
        self.assertEqual(env['r13_world148_state']('light')['result'], 'listen', '상태 조회는 복사본이어야 한다')

    def test_outcome_variants_follow_current_proof_and_actual_fire(self):
        env, state = environment()
        prepare(env, state, 'tools', owner=True)
        values = state.room13['v111']['values']
        self.assertEqual(env['r13_world148_variants']('tools'), [])
        for result in ('win', 'partial', 'lose'):
            values['meeting:lamp'] = result
            values['listed:resident_tok'] = result == 'lose'
            self.assertEqual(env['r13_world148_variants']('tools'), ['lamp_' + result])
        values.update({'meeting:lamp': 'win', 'listed:resident_tok': True})
        self.assertNotIn('lamp_win', env['r13_world148_variants']('tools'))
        values.clear()
        values.update(D06_P01_handover_completed=True, warehouse_children_school_handover=4, KKOMI_ALIVE=True)
        self.assertNotIn('fire_safe', env['r13_world148_variants']('school'), '사전 대피만으로 실제 화재가 끝난 것은 아니다')
        values['D06_S03P_empty_fire_completed'] = True
        self.assertIn('fire_safe', env['r13_world148_variants']('school'))
        values.clear()
        values.update(D06_S03_main_completed=True, warehouse_children_rescued=3, KKOMI_ALIVE=False)
        self.assertIn('fire_lost', env['r13_world148_variants']('school'))
        self.assertNotIn('fire_safe', env['r13_world148_variants']('school'))

    def test_legacy_tok_flags_never_determine_the_new_campaign_result(self):
        env, state = environment()
        prepare(env, state, 'tools', owner=True)
        state.room13['flags'].extend(['tok_cleared', 'tok_detained'])
        self.assertEqual(env['r13_world148_variants']('tools'), [])
        state.room13['v111']['values'].update({'meeting:lamp': 'partial'})
        self.assertEqual(env['r13_world148_variants']('tools'), ['lamp_partial'])

    def test_aftermath_is_unavailable_until_a_consistent_fire_outcome_exists(self):
        for mode in ('none', 'only_handover', 'only_safe_flag', 'only_loss_flag', 'safe', 'lost'):
            env, state = environment()
            state.room13.update(day=7, location='school')
            values = state.room13['v111']['values']
            if mode in ('only_handover', 'safe'):
                values.update(warehouse_children_school_handover=4, KKOMI_ALIVE=True)
            if mode in ('only_safe_flag', 'safe'): values['D06_S03P_empty_fire_completed'] = True
            if mode in ('only_loss_flag', 'lost'): values['D06_S03_main_completed'] = True
            if mode == 'lost': values.update(warehouse_children_rescued=3, KKOMI_ALIVE=False)
            source = DATA['aftermath']['sources'][0]
            before = copy.deepcopy(state.room13)
            self.assertEqual(env['r13_world148_source_allowed']('aftermath', source['object']), mode in ('safe', 'lost'), mode)
            self.assertEqual(state.room13, before)

    def test_story_variants_replace_only_the_phases_they_explicitly_author(self):
        env, state = environment()
        prepare(env, state, 'tools', owner=True)
        values = state.room13['v111']['values']
        state.room13['evidence'].append('V111:E09')
        values.update({'piko_alive': False, 'piko_news3:buri': True, 'meeting:lamp': 'partial',
                       'D06_S03_main_completed': True, 'warehouse_children_rescued': 3, 'KKOMI_ALIVE': False})
        for key, spec in DATA.items():
            for phase, base in spec['blocks'].items():
                expected = base
                for variant in env['r13_world148_variants'](key):
                    expected = spec.get('variants', {}).get(variant, {}).get(phase, expected)
                self.assertEqual(env['r13_world148_lines'](key, phase), expected, (key, phase))

    def test_stale_physical_location_does_not_override_real_scheduled_presence(self):
        env, state = environment()
        self.observe(env, state, 'aftermath')
        state.room13.update(location='square', day=7, period=1)
        person = DATA['aftermath']['owner']
        state.where[person] = 'square'
        state.room13['v111']['values']['location:' + person] = 'school'
        self.assertEqual(self.actions(env, 'aftermath'), ['ask'])
        self.assertTrue(env['r13_world148_record']('aftermath', 'choose', 'help'))
        self.assertIn('school', env['r13_world148_journal']()[0]['objective'])
        self.assertFalse(env['r13_world148_record']('aftermath', 'work'), '광장 대화만으로 학교 작업이 완료되면 안 된다')
        state.room13['location'] = 'school'
        self.assertTrue(env['r13_world148_record']('aftermath', 'work'))

    def test_part_one_last_afternoon_allows_school_work_then_square_report_without_time_advance(self):
        env, state = environment()
        self.observe(env, state, 'aftermath')
        state.room13['v111']['gate'] = 'free_day7'
        state.room13['v111']['scene'] = 'MS14_D07_S02'
        person = DATA['aftermath']['owner']
        state.where[person] = 'square'
        state.room13['location'] = 'square'
        self.assertTrue(env['r13_world148_record']('aftermath', 'choose', 'help'))
        same_time = (state.room13['day'], state.room13['period'])
        state.room13['location'] = 'school'
        self.assertEqual(self.actions(env, 'aftermath'), [], '부재중인 보리에게 현장 작업 보고를 하지 않는다')
        self.assertTrue(env['r13_world148_record']('aftermath', 'work'))
        self.assertFalse(env['r13_world148_record']('aftermath', 'memory'))
        state.room13['location'] = 'square'
        before = main_state(state)
        self.assertEqual(self.actions(env, 'aftermath'), ['memory'])
        self.assertTrue(env['r13_world148_record']('aftermath', 'memory'))
        self.assertEqual(main_state(state), before)
        self.assertEqual((state.room13['day'], state.room13['period']), same_time)
        self.assertEqual(same_time, (7, 1))
        row = env['r13_world148_state']('aftermath')
        self.assertTrue(row['worked'])
        self.assertTrue(row['report_seen'])
        self.assertEqual(row['result'], 'help')

    def test_old_save_without_group_loads_and_malformed_group_cannot_write(self):
        env, state = environment()
        before = copy.deepcopy(state.room13)
        self.assertEqual(env['r13_world148_state']('light'), {})
        self.assertEqual(env['r13_world148_journal'](), [])
        self.assertEqual(state.room13, before)
        for group in (None, [], 'invalid', {'light': 'invalid'}):
            state.room13['v111']['world148'] = group
            before = copy.deepcopy(state.room13)
            self.assertFalse(env['r13_world148_record']('light', 'observe'))
            self.assertEqual(state.room13, before)

    def test_question_wrapper_preserves_main_priority_and_uses_tagged_return(self):
        env, state = environment()
        self.observe(env, state, 'light', owner=True)
        original_main = ('본편 질문', SimpleNamespace(value=3), False)
        original_chat = ('일상 질문', SimpleNamespace(value=('resident_chat', 'work')), False)
        state.questions = [original_main, original_chat]
        rows = env['r13_v111_questions'](DATA['light']['owner'])
        self.assertIs(rows[0], original_main)
        self.assertEqual(rows[1][1].value, ('world148', ('light', 'ask')))
        self.assertIs(rows[-1], original_chat)
        self.assertTrue(env['r13_v111_has_business'](DATA['light']['owner']))
        self.assertEqual(env['r13_population146_side_people'](), {'resident_yeoni', DATA['light']['owner']})


if __name__ == '__main__':
    unittest.main()
