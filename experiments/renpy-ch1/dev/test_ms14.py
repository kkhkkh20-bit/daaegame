"""Route/effect checks. These do not claim to test the Ren'Py save UI or mobile."""
import copy
import itertools
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'game/python-packages'))
import ms14_runtime as rt
DATA = json.loads((ROOT/'game/ms14/route.json').read_text())


def advance(state):
    node = DATA['nodes'][state['node']]
    if node['kind']=='block':
        for rid in node['records'][state['cursor']:]:
            state = rt.finish_record(state,DATA['records'][rid])
        return rt.enter(state,node['next'])
    if node['kind']=='branch':
        return rt.enter(state,node['yes'] if state['values'][node['field']]==node['value'] else node['no'])
    if node['kind']=='mark':
        return rt.enter(rt.apply(state,state['node'],node['operations']),node['next'])
    if node['kind']=='read':return rt.enter(state,node['next'])
    raise ValueError('Interaction needed: '+state['node'])


def play(afternoon='shelter',stone=0,custody=0,early=True):
    state=rt.new_state(DATA)
    path=[]
    for _ in range(1000):
        key=state['node'];node=DATA['nodes'][key];path.append(key)
        if node['kind']=='end':return state,path
        if node['kind']=='proof':
            for evidence in node['correct']:state=rt.select(state,evidence)
            state=rt.submit(state,node)
        elif node['kind']=='choice':
            index=0
            if key=='letter_menu':index=2
            elif key=='gate_choice':index=1
            elif key=='gate_investigate':
                if 'E03' not in state['evidence']:index=0
                elif 'E04' not in state['evidence']:index=1
                elif not early and not state['values']['purpose_difference_known']:index=3
                else:index=5
            elif key=='registered_menu':index=1
            elif key=='post_menu':index=1
            elif key=='lamp_observe':
                index=next((i for i in range(4) if not state['values']['lamp_part_'+str(i)]),4)
            elif key=='afternoon':index=0 if afternoon=='shelter' else 1
            elif key=='stone_choice':index=stone
            elif key=='custody_choice':index=custody
            state=rt.choose(state,node,index)
        else:state=advance(state)
        # Every acquired variant is readable; catches swapped/missing authored cards.
        for evidence in state['evidence']:rt.observed(DATA,state,evidence)
    raise AssertionError('Route did not finish: '+str(path[-10:]))


class MS14Tests(unittest.TestCase):
    def test_all_eight_outcomes_and_both_gate_routes(self):
        for afternoon,stone,custody,early in itertools.product(('shelter','nero'),range(2),range(2),(False,True)):
            with self.subTest(afternoon=afternoon,stone=stone,custody=custody,early=early):
                state,path=play(afternoon,stone,custody,early)
                v=state['values']
                self.assertEqual(v['day'],4)
                self.assertEqual(v['piko_alive'],afternoon=='shelter')
                self.assertEqual(v['portrait'],'complete' if afternoon=='shelter' else 'child_completed')
                self.assertEqual(v['public_stones'],'restored' if stone==0 else 'with_baek')
                self.assertEqual(v['unverified_stones_status'],'with_baek')
                self.assertEqual(v['carried_dry_blankets'],0 if afternoon=='shelter' else 2)
                self.assertEqual(v['silluk_status'],'reporting_obligation' if custody==0 else 'supervised_compulsory_labor')
                self.assertEqual('labor4' in path,custody==1)
                self.assertEqual('nero4_work' in path,afternoon=='shelter')
                self.assertTrue(v['lamp_theft_supported'])
                self.assertEqual('gate_early' in path,early)

    def test_observation_is_required(self):
        state=rt.enter(rt.new_state(DATA),'gate_investigate')
        self.assertNotIn('E03',state['evidence'])
        self.assertNotIn('E04',state['evidence'])
        self.assertFalse(rt.allowed(state,[['evidence','E03',True]]))
        self.assertIsNone(rt.observed(DATA,state,'E03'))
        with self.assertRaises(ValueError):rt.select(state,'E03')

    def test_wrong_and_hint_have_no_effects(self):
        state=rt.new_state(DATA)
        state=rt.apply(state,'test', [dict(op='acquire',key='E03',variant='observed')])
        state=rt.enter(state,'gate_proof');state=rt.select(state,'E03')
        result=rt.submit(state,DATA['nodes']['gate_proof'])
        self.assertEqual(result['node'],'gate_number')
        before=copy.deepcopy(result['values']);after=advance(result)
        self.assertEqual(before,after['values'])
        self.assertFalse(after['values']['gate_basis_proven'])

    def test_effects_once_across_serialized_resume(self):
        state=rt.new_state(DATA)
        record=DATA['records']['MS14_D03_S06_L0041']
        state=rt.finish_record(state,record)
        restored=json.loads(json.dumps(state))
        repeated=rt.apply(restored,record['id'],record['operations'])
        self.assertEqual(restored,repeated)
        self.assertEqual(repeated['values']['carried_dry_blankets'],2)
        self.assertEqual(repeated['applied'].count(record['id']),1)
        self.assertEqual(rt.new_state(DATA)['values']['carried_dry_blankets'],0)

    def test_knife_is_not_theft_verdict(self):
        state=rt.enter(rt.new_state(DATA),'knife_fit')
        state=advance(state)
        self.assertFalse(state['values']['lamp_theft_supported'])
        self.assertEqual(state['node'],'trial_latch')
        self.assertIn('E17',state['evidence'])
        self.assertIn('E33',state['evidence'])
        self.assertNotEqual(rt.observed(DATA,state,'E17')['establishes'],rt.observed(DATA,state,'E33')['establishes'])

    def test_source_text_and_ids_preserved(self):
        source=json.loads(next((ROOT/'docs/story-ms14/source').glob('*대사연출조건.json')).read_text())
        authored={r['id']:r for s in source['scenes'] for b in s['blocks'] for r in b['records']}
        for key,r in DATA['records'].items():
            self.assertEqual(r['text'],authored[key]['text'])
            self.assertEqual(r['effects'],authored[key]['effects'])
        self.assertTrue(rt.validate(DATA))

    def test_unknown_guards_and_operations_fail_closed(self):
        state=rt.new_state(DATA)
        with self.assertRaises(ValueError):rt.allowed(state,[['prose','always',True]])
        with self.assertRaises(ValueError):rt.allowed(state,[['state','unknown',True]])
        with self.assertRaises(ValueError):rt.apply(state,'unknown',[dict(op='eval')])

    def test_asset_hashes_and_no_dev_evidence(self):
        import hashlib
        art=json.loads((ROOT/'game/ms14/art.json').read_text())
        for key,spec in art.items():
            file=ROOT/'game'/spec['file']
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(),spec['sha256'])
            self.assertNotIn('developer_review',spec['source'])
            self.assertNotIn('pixel2x_candidates',spec['source'])
            self.assertNotIn('/audio/',spec['source'])


if __name__=='__main__':unittest.main()
