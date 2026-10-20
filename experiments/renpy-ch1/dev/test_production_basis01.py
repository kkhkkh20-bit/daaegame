"""D01 data and integration tests using the existing state functions verbatim.
Not a replacement for native save files, clicks, or screenshot inspection.
"""
import ast
import copy
import io
import json
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace
import validate_production_basis01 as authored

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
DATA = json.loads((GAME / 'production-basis01-d01.json').read_text())


def init_python(path, priority):
    lines = path.read_text().splitlines()
    begin = lines.index('init %s python:' % priority) + 1
    end = next((i for i in range(begin, len(lines)) if lines[i] and not lines[i].startswith((' ', '#'))), len(lines))
    return textwrap.dedent('\n'.join(lines[begin:end]))


def existing_functions(path, priority, names, env):
    tree = ast.parse(init_python(path, priority))
    chosen = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if len(chosen) != len(names): raise AssertionError('Missing real state function')
    exec(compile(ast.Module(body=chosen, type_ignores=[]), str(path), 'exec'), env)


class ExistingEngineD01(unittest.TestCase):
    def setUp(self):
        self.store = SimpleNamespace(room13=None, r13_present_priority=None)
        self.present_calls = []
        self.env = dict(store=self.store, json=json, winter_copy=copy,
                        persistent=SimpleNamespace(room13_knowledge=[]), R13_TRIAL_DAY=7,
                        ROOM13=dict(story_revision='baseline', evidence={}), R13_RECORD_SHORT={},
                        source_fx=lambda *a: None, Return=lambda value:value,
                        renpy=SimpleNamespace(file=lambda p:io.StringIO((GAME/p).read_text()), notify=lambda *a:None),
                        _r13_sling_confidence_present=lambda *args:self.present_calls.append(args))
        existing_functions(GAME/'room13_rules.rpy', 55,
                           {'r13_new','r13_edit','r13_flag','r13_has','r13_grant','r13_available'}, self.env)
        self.store.room13 = self.env['r13_new']()
        self.env['r13_edit'](campaign_id='production_basis01')
        existing_functions(GAME/'room13_record_compare.rpy',78,{'r13_compare_result'},self.env)
        self.env['_r13_tm_compare']=self.env['r13_compare_result']
        exec(compile(init_python(GAME/'production_basis01.rpy',210),'story_init','exec'),self.env)

    def grant(self,*keys):
        self.env['r13_grant'](['PB01:'+key for key in keys], 'source-record')

    def test_source_guards_and_ids_validate_without_runtime_interpreter(self):
        authored.validate(DATA)
        self.assertFalse((GAME/'python-packages/production_basis01.py').exists())
        source=(GAME/'production_basis01.rpy').read_text()
        for forbidden in ('r13_basis01_state','elapsed_minutes','new_state(', 'commit_record(', 'def allowed(', 'eval('):
            self.assertNotIn(forbidden,source)

    def test_unknown_conditions_and_effects_fail_authoring_validation(self):
        for field,value in [('when','unknown=true')]:
            data=copy.deepcopy(DATA);data['scenes'][0]['blocks'][0][field]=value
            with self.assertRaises((ValueError,KeyError)):authored.validate(data)
        data=copy.deepcopy(DATA);data['scenes'][0]['blocks'][0]['records'][0]['effects']=['unknown=true']
        with self.assertRaises((ValueError,KeyError)):authored.validate(data)

    def test_data_projection_preserves_visible_record_ids_and_never_grants(self):
        before=copy.deepcopy(self.store.room13)
        lines=self.env['pb01_lines']('MS14_D01_S01_B002')
        self.assertEqual(lines[0][2]['source_record_id'],'MS14_D01_S01_L9101')
        self.assertFalse(any('조작:' in row[1] for row in lines))
        self.assertEqual(self.store.room13,before)

    def test_actual_existing_grant_and_flag_functions_are_idempotent(self):
        for _ in range(5):
            self.grant('E01','E02','E03')
            self.env['r13_flag']('pb01:K01a')
        self.assertEqual(self.store.room13['evidence'],['PB01:E01','PB01:E02','PB01:E03'])
        self.assertEqual(self.store.room13['flags'].count('pb01:K01a'),1)
        self.assertEqual(set(self.store.room13['records']),set(self.store.room13['evidence']))

    def test_gate_entry_does_not_grant_uninspected_documents(self):
        self.grant('E01','E02')
        self.env['pb01_entry_questions']()
        self.assertNotIn('PB01:E03',self.store.room13['evidence'])
        self.assertNotIn('PB01:E04',self.store.room13['evidence'])

    def test_real_availability_filters_questions_and_optional_reason(self):
        questions=self.env['pb01_entry_questions']()
        self.assertNotIn(('entry','compare'),[q[1] for q in questions])
        self.grant('E03')
        self.assertIn(('entry','compare'),[q[1] for q in self.env['pb01_entry_questions']()])
        self.env['r13_flag']('pb01:purpose_difference_known')
        self.assertIn(('entry','reason'),[q[1] for q in self.env['pb01_entry_questions']()])
        self.env['r13_flag']('pb01:reason_heard')
        self.assertNotIn(('entry','reason'),[q[1] for q in self.env['pb01_entry_questions']()])

    def test_existing_compare_uses_owned_documents_without_auto_registration(self):
        self.env['pb01_compare_feedback'](['PB01:E02','PB01:E03'])
        self.assertNotIn('pb01:purpose_difference_known',self.store.room13['flags'])
        self.grant('E02','E03')
        text=self.env['pb01_compare_feedback'](['PB01:E02','PB01:E03'])
        self.assertIn('가족 방문',text)
        self.assertIn('pb01:purpose_difference_known',self.store.room13['flags'])
        self.assertNotIn('entry_corrected',self.store.room13['flags'])

    def test_three_grounds_direct_and_regular_branches(self):
        self.grant('E02','E03','E04')
        self.store.r13_present_priority=('guard',('PB01:E03','PB01:E04'))
        self.assertEqual(self.env['pb01_gate_block']('PB01:E03'),'MS14_D01_S03_B005')
        self.assertNotIn('pb01:reason_heard',self.store.room13['flags'])
        self.env['r13_flag']('pb01:purpose_difference_known')
        self.assertEqual(self.env['pb01_gate_block']('PB01:E03'),'MS14_D01_S03_B004')

    def test_missing_evidence_and_extra_or_wrong_grounds_do_not_succeed(self):
        for evidence in [('E02',),('E02','E03'),('E02','E04')]:
            self.store.room13=self.env['r13_new']();self.grant(*evidence)
            self.store.r13_present_priority=('guard',('PB01:E03','PB01:E04'))
            self.assertEqual(self.env['pb01_gate_block']('PB01:E03'),'MS14_D01_S03_B006')
        self.grant('E02','E03','E04');self.store.r13_present_priority=('guard',('PB01:E03','PB01:E04','PB01:E02'))
        self.assertEqual(self.env['pb01_gate_block']('PB01:E03'),'MS14_D01_S03_B006')
        self.store.r13_present_priority=('guard',('PB01:E03',))
        self.assertEqual(self.env['pb01_gate_block']('PB01:E03'),'MS14_D01_S03_B006')

    def test_presentation_reuses_existing_chain_without_awarding_success(self):
        self.grant('E02','E03','E04')
        lines=self.env['pb01_present_lines']('PB01:E03')
        self.assertEqual(self.present_calls,[('guard','PB01:E03',False)])
        self.assertEqual(lines[0][2]['source_record_id'],'MS14_D01_S03_L0024')
        self.assertNotIn('entry_corrected',self.store.room13['flags'])
        self.assertNotIn('PB01:E05',self.store.room13['evidence'])

    def test_registration_and_roundtrip_use_only_existing_room13_state(self):
        self.grant('E02','E03','E04')
        need=dict(need=['pb01:gate_basis_proven','PB01:E02','PB01:E03','PB01:E04'])
        self.assertFalse(self.env['r13_available'](need))
        self.env['r13_flag']('pb01:gate_basis_proven')
        self.assertTrue(self.env['r13_available'](need))
        self.grant('E05');self.env['r13_flag']('entry_corrected','pb01:gate_registered')
        self.store.room13=json.loads(json.dumps(self.store.room13))
        self.grant('E05');self.env['r13_flag']('entry_corrected','pb01:gate_registered')
        self.assertEqual(self.store.room13['evidence'].count('PB01:E05'),1)
        self.assertEqual(self.store.room13['flags'].count('entry_corrected'),1)
        self.assertFalse(any(k in self.store.room13 for k in ('elapsed_minutes','applied','completed_inputs')))

    def test_source_hooks_use_existing_entry_object_and_final_present_layer(self):
        root=(GAME/'room13.rpy').read_text()
        self.assertIn('renpy.jump("r13_pb01_entry_dispatch") if pb01_active()',root)
        self.assertIn('call r13_object(r13_choice[1])',(GAME/'production_basis01.rpy').read_text())
        self.assertIn('renpy.jump("r13_pb01_documents") if pb01_active()', (GAME/'room13_gate_inspection.rpy').read_text())
        self.assertIn('key.startswith("PB01:") and pb01_active()' , (GAME/'systems/room13_sling_confidence.rpy').read_text())
        self.assertEqual(self.store.room13['day'],1)
        self.assertEqual(self.store.room13['period'],0)


if __name__=='__main__':unittest.main()
