"""Host-side regression tests of authored Room13 Python state functions.

Loads the actual init blocks with UI/audio stubs. This is not browser play or
Ren'Py save serialization; those are covered by the separate live QA driver.
"""
import copy
import ast
import hashlib
import json
import io
from pathlib import Path
import textwrap
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_rules():
    persistent = SimpleNamespace(room13_read=[], room13_knowledge=[],
        room13_knowledge_revision=None, room13_previous_knowledge={},
        room13_opening_seen=False, room13_endings=[], room13_ending_notes={})
    store = SimpleNamespace(room13=None)
    config = SimpleNamespace(interact_callbacks=[], skipping=None)
    renpy = SimpleNamespace(file=lambda p: io.StringIO((ROOT / 'game' / p).read_text()),
        notify=lambda text: None, save_persistent=lambda: None, config=config,
        get_showing_tags=lambda *args, **kwargs: [])
    ns = dict(json=json, renpy=renpy, persistent=persistent, store=store,
        winter_copy=copy, WINTER_NAMES={}, CAST={}, Character=lambda *a, **k: None,
        source_fx=lambda *a: None, config=config, R13_RESIDENTS={},
        R13_CORE_PEOPLE={'granny','buri','bami','nabi','karo','neoul','seryeon','doto'},
        r13_resident_where=lambda person: None)
    for filename in ('room13_rules.rpy', 'room13_week2_rules.rpy'):
        source=(ROOT / 'game' / filename).read_text()
        block=source.split(' python:\n',1)[1]
        exec(compile(textwrap.dedent(block),filename,'exec'),ns)
    # Calendar-aware topic completion records the actual encounter key.
    calendar_source=(ROOT / 'game/room13_dialogue_openings_20261013.rpy').read_text().split('init 75 python:\n',1)[1]
    calendar_tree=ast.parse(textwrap.dedent(calendar_source))
    calendar_tree.body=[n for n in calendar_tree.body if isinstance(n,ast.FunctionDef) and n.name in ('r13_calendar_phase','r13_calendar_key')]
    ns.update(R13_OPENING_SCENES=json.loads((ROOT/'game/room13-dialogue-openings.json').read_text()), r13_hashlib=hashlib, r13_opening_json=json)
    exec(compile(calendar_tree,'actual calendar helpers','exec'),ns)
    store.room13=ns['r13_new']()
    ns['r13_upgrade']()
    return ns


class Rules(unittest.TestCase):
    def setUp(self):
        self.n=load_rules();self.s=self.n['store'];self.p=self.n['persistent']
    def call(self,name,*args,**kwargs):return self.n['r13_'+name](*args,**kwargs)
    def edit(self,**kw):self.call('edit',**kw)
    def grant(self,*keys):self.call('grant',keys,'QA fixture')
    def flags(self,*keys):self.call('flag',*keys)
    def state(self):return copy.deepcopy(self.s.room13)
    def owned(self):self.grant(*self.n['ROOM13']['evidence'])

    def test_sleep_applies_leak_consequence_once(self):
        self.flags('bami_identity_leaked')
        self.call('next_day');self.call('next_day')
        self.assertEqual(3,self.s.room13['day'])
        self.assertEqual(1,self.s.room13['flags'].count('bami_pressured'))
        self.assertEqual(2,len(self.s.room13['log']))

    def test_protection_blocks_pressure_for_wait_and_sleep(self):
        self.flags('bami_identity_leaked','bami_protected')
        self.call('tick');self.call('next_day')
        self.assertNotIn('bami_pressured',self.s.room13['flags'])

    def test_afternoon_measurement_allows_same_evening_recheck(self):
        self.edit(day=10,period=1)
        self.call('finish_action','w2_measure1')
        self.assertEqual(2,self.s.room13['period'])
        self.assertEqual(37,self.s.room13['observations']['first']['time'])
        self.assertTrue(self.call('w2_actions_allowed','w2_measure2'))
        self.call('finish_action','w2_measure2')
        self.assertEqual(3,self.s.room13['period'])
        first=self.s.room13['observations']['first'];second=self.s.room13['observations']['second']
        self.assertEqual(38,second['time']);self.assertNotEqual(first['load'],second['load'])

    def test_repeat_activity_does_not_add_time_or_reward(self):
        self.call('finish_action','map');before=self.state()
        self.call('finish_action','map');self.assertEqual(before,self.state())

    def test_past_knowledge_is_not_presentable(self):
        self.p.room13_knowledge=['E19','E27']
        before=self.state();self.call('present','granny','E19')
        self.assertEqual(before,self.state())
        self.call('submit','C1','E05');self.assertEqual(before,self.state())

    def test_present_preserves_original_and_deduplicates(self):
        self.grant('E09');before=self.state()
        self.call('present','granny','E09');once=self.state()
        self.call('present','granny','E09')
        self.assertEqual(once,self.state())
        self.assertEqual(before['evidence'],self.s.room13['evidence'])
        self.assertEqual(before['records'],self.s.room13['records'])
        self.assertEqual(before['period'],self.s.room13['period'])

    def test_anonymous_then_named_witness_is_distinct_disclosure(self):
        self.grant('E10');self.call('present','granny','E10',False)
        self.assertFalse(self.call('has','bami_identity_leaked'))
        self.call('present','granny','E10',True)
        self.assertTrue(self.call('has','bami_identity_leaked'))
        self.assertEqual(2,len(self.s.room13['resident_knowledge']['granny']))
        self.assertNotIn('neoul',self.s.room13['resident_knowledge'])

    def test_topic_unlock_does_not_grant_testimony(self):
        self.grant('E11');self.call('present','nabi','E11')
        self.assertTrue(self.call('has','topic:nabi_gap'))
        self.assertFalse(self.call('has','E12'))
        self.call('finish_topic','nabi_gap')
        self.assertTrue(self.call('has','E12'))
        before=self.state();self.call('finish_topic','nabi_gap')
        after=self.state()
        # Replays now track followup mode, but grant no duplicate evidence or time.
        for state in (before, after):
            for item in state.get('dialogue_views', {}).values():
                item.pop('mode', None)
        self.assertEqual(before,after)

    def test_buri_requires_both_sources_and_consent(self):
        self.grant('E06','E08');self.call('present','buri','E06');self.call('present','buri','E08')
        self.assertFalse(self.call('has','topic:buri_records'))
        self.flags('medical_consent');self.call('present','buri','E08')
        self.assertTrue(self.call('has','topic:buri_records'))

    def test_different_convoy_revision_can_be_disclosed_again(self):
        self.edit(day=9,daram_state='held')
        self.call('finish_action','w2_scout');self.flags('injunction_support')
        self.assertIn('order',self.call('rescue_routes'))
        self.call('present','granny','E27')
        self.assertEqual(1,self.s.room13['convoy_revision'])
        self.assertEqual([],self.call('rescue_routes'))
        self.call('present','granny','E27')
        self.assertEqual(1,self.s.room13['convoy_revision'])
        self.call('finish_action','w2_scout')
        self.assertIn('order',self.call('rescue_routes'))
        self.call('present','granny','E27')
        self.assertEqual(2,self.s.room13['convoy_revision'])
        self.assertEqual([],self.call('rescue_routes'))

    def test_all_rescue_routes_require_current_scout(self):
        self.grant('E27','E28');self.flags('injunction_support','laundry_support',
            'shelter_ready','maintenance_support','operators_ready')
        self.assertEqual([],self.call('rescue_routes'))
        self.edit(scout_revision=0)
        self.assertEqual(['order','laundry','maintenance'],self.call('rescue_routes'))

    def test_legacy_convoy_disclosure_does_not_repeat_consequence(self):
        self.edit(day=9,convoy_revision=1,resident_knowledge={'granny':['E27:anonymous']})
        self.grant('E27');self.call('present','granny','E27')
        self.assertEqual(1,self.s.room13['convoy_revision'])

    def test_leaked_contact_reopens_safety_work_not_reunion(self):
        self.edit(day=9,mom_state='contacted');self.grant('E19')
        self.call('finish_action','w2_secure_contact')
        self.call('present','granny','E19')
        self.assertEqual('relocated',self.s.room13['mom_state'])
        self.assertFalse(self.call('has','contact_safe'))
        self.assertNotIn('w2_secure_contact',self.s.room13['done'])
        before=self.state();self.call('present','granny','E19');self.assertEqual(before,self.state())
        self.flags('mom_reunited');self.edit(mom_state='reunited')
        self.call('present','neoul','E19')
        self.assertEqual('reunited',self.s.room13['mom_state'])

    def test_all_claim_paths_use_actual_submitted_evidence(self):
        self.owned();self.flags('bami_consent','shelter_ready','supplies_ready','operators_ready','patient_transport')
        for claim,spec in self.n['R13_CLAIMS'].items():
            for path in spec['support_sets']:
                with self.subTest(claim=claim,path=path):
                    self.edit(arguments={claim:path[:-1]})
                    self.assertFalse(self.call('argument_ready',claim))
                    self.call('submit',claim,path[-1])
                    self.assertTrue(self.call('argument_ready',claim))

    def test_anonymous_witness_cannot_complete_c2(self):
        path=self.n['R13_CLAIMS']['C2']['support_sets'][0]
        self.owned();self.edit(arguments={'C2':path})
        self.assertFalse(self.call('argument_ready','C2'))
        self.flags('bami_consent');self.assertTrue(self.call('argument_ready','C2'))

    def test_f3_requires_real_preparations(self):
        self.edit(arguments={'F3':['E25','E26']})
        self.assertFalse(self.call('argument_ready','F3'))
        self.flags('shelter_ready','supplies_ready','operators_ready','patient_transport')
        self.assertTrue(self.call('argument_ready','F3'))

    def test_survival_branch_outcomes(self):
        self.edit(daram_state='lost');self.assertEqual('E1',self.call('resolve_ending'))
        self.edit(daram_state='rescued');self.assertEqual('E3',self.call('resolve_ending'))
        self.call('prove','F2');self.assertEqual('E4',self.call('resolve_ending'))
        self.call('prove','F1');self.call('prove','F3')
        self.flags('shelter_ready','supplies_ready','operators_ready','patient_transport')
        self.assertEqual('E5',self.call('resolve_ending'))
        self.call('prove','F4');self.call('prove','C4')
        self.flags('mother_original_safe','bami_protected')
        self.edit(observations={'first':{'time':37,'load':'day_low'},'second':{'time':38,'load':'evening_high'}})
        self.assertEqual('E6',self.call('resolve_ending'))

    def test_prevention_can_reach_true_ending_without_murder_proof(self):
        self.edit(case_state='prevented',victim_state='protected',propositions=['F4'],
            observations={'first':{'time':37,'load':'day_low'},'second':{'time':38,'load':'evening_high'}})
        self.flags('mother_original_safe','witness_protected','premeditation_prevented_proven')
        self.assertTrue(self.call('true_ending_ready'))
        self.edit(day=8);self.assertEqual('school',self.call('where','resident_owlgp'))
        self.edit(victim_state='dead');self.assertIsNone(self.call('where','resident_owlgp'))

    def test_detained_granny_stays_absent_after_day_transition(self):
        self.edit(day=7,granny_state='detained');self.call('next_day')
        self.assertIsNone(self.call('where','granny'))
        self.call('upgrade');self.assertEqual('detained',self.s.room13['granny_state'])

    def test_all_seven_endings_and_fresh_run_history(self):
        self.assertEqual({f'E{i}' for i in range(7)},set(self.n['R13_ENDINGS']))
        for key in self.n['R13_ENDINGS']:
            self.call('finish_ending',key);self.call('finish_ending',key)
        self.assertEqual(7,len(self.p.room13_endings))
        self.grant('E09');self.call('present','granny','E09')
        self.p.room13_read=['old-read'];self.edit(daram_state='held')
        self.s.room13=self.call('new');self.call('upgrade')
        self.assertEqual(1,self.s.room13['day']);self.assertEqual([],self.s.room13['evidence'])
        self.assertEqual({},self.s.room13['resident_knowledge']);self.assertEqual('with_dad',self.s.room13['daram_state'])
        self.assertEqual(['E09'],self.p.room13_knowledge);self.assertEqual(['old-read'],self.p.room13_read)
        self.assertEqual(7,len(self.p.room13_endings))

    def test_read_skip_stops_on_new_or_changed_line(self):
        self.n['store'].r13_fast_read=True
        key=self.call('before_line','scene',0,'old');self.call('remember_line',key)
        self.call('before_line','scene',0,'old');self.assertEqual('slow',self.n['config'].skipping)
        self.call('before_line','scene',0,'changed');self.assertIsNone(self.n['config'].skipping)

    def test_evidence_and_unlock_references_exist(self):
        data=self.n['ROOM13'];evidence=set(data['evidence'])
        for section in ('topics','activities'):
            for key,spec in data[section].items():
                self.assertTrue(set(spec['give'])<=evidence,key)
        for spec in data['presentations']:
            self.assertIn(spec['topic'],data['topics']);self.assertTrue(set(spec['items'])<=evidence)

if __name__=='__main__':unittest.main(verbosity=2)
