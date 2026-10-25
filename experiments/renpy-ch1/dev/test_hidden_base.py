"""고대 기지는 진엔딩 자격을 바꾸지 않는 현재 판의 선택 조사다."""
import ast
import copy
import itertools
from pathlib import Path
import re
import textwrap
import types
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'game/room13_hidden_base.rpy').read_text()

class HiddenBase(unittest.TestCase):
    def setUp(self):
        source=SOURCE.split('init 324 python:',1)[1].split('\nlabel ',1)[0]
        tree=ast.parse(textwrap.dedent(source))
        functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
        self.values={}
        self.store=types.SimpleNamespace(room13=dict(location='school',period=2,v111=dict(people=['mom','daram'],gate='cookie14')))
        self.env=dict(r13_v111_value=self.values.get,r13_v111_set=self.values.__setitem__,store=self.store)
        self.env['r13_edit']=lambda **kw:self.store.room13.update(kw)
        self.env['r13_v111_arrive']=lambda people:self.store.room13['v111'].update(people=list(people))
        self.env['r13_v111_context']=lambda gate:self.store.room13['v111'].update(gate=gate)
        exec(compile(ast.Module(body=functions,type_ignores=[]),'<hidden_base>','exec'),self.env)

    def test_only_completed_parts_in_true_ending_enter(self):
        for ending in ('morning','true','wild_night','family','partial','violence','frozen','left_name',None):
            for bits in itertools.product((None,False,True),repeat=3):
                self.values.clear();self.values['ending14']=ending
                self.values.update(('hidden_base:'+k,v) for k,v in zip(('paper','plate','marks_copied'),bits))
                self.assertEqual(self.env['r13_hidden_base_ready'](),ending=='true' and bits==(True,True,True))

    def test_finished_episode_does_not_reopen(self):
        self.values.update({'ending14':'true',**{'hidden_base:'+k:True for k in ('paper','plate','marks_copied','finished')}})
        self.assertFalse(self.env['r13_hidden_base_ready']())

    def test_return_context_survives_save_copy_and_is_not_replaced(self):
        self.values['elapsed_minutes']=43
        self.env['r13_hidden_base_remember_return']()
        self.store.room13.update(location='hidden_base14',period=2)
        self.store.room13['v111'].update(people=['mom'],gate='hidden_base_room14')
        self.values['elapsed_minutes']=88
        self.env['r13_hidden_base_remember_return']()
        saved=copy.deepcopy(self.values)
        self.values.clear();self.values.update(saved)
        self.env['r13_hidden_base_restore_return']()
        self.assertEqual(self.store.room13,dict(location='school',period=2,v111=dict(people=['mom','daram'],gate='cookie14')))
        self.assertEqual(self.values['elapsed_minutes'],43)
        self.assertIsNone(self.values['hidden_base:return_context'])
        self.env['r13_hidden_base_restore_return']()
        self.assertEqual(self.store.room13['location'],'school')

    def test_only_own_state_is_written(self):
        keys=re.findall(r"r13_v111_set\(['\"]([^'\"]+)",SOURCE)
        self.assertTrue(keys)
        self.assertTrue(all(k.startswith('hidden_base:') or k=='elapsed_minutes' for k in keys))
        self.assertNotIn('persistent.',SOURCE)
        self.assertNotIn('r13_nw_acquire(',SOURCE)
        self.assertNotIn('r13_nw_true_ending_ready()',SOURCE)

    def test_wrong_orientation_preserves_parts_and_exit_has_no_read_gate(self):
        wrong=SOURCE.split("elif _return==3:",1)[1].split('elif _return==4:',1)[0]
        self.assertIn("r13_v111_set('hidden_base:aligned',False)",wrong)
        self.assertNotIn("hidden_base:paper',False",wrong)
        exit_block=SOURCE.split('label r13_hidden_base_return14:',1)[1]
        self.assertNotIn('read_section',exit_block)
        self.assertNotIn('read_incident',exit_block)
        self.assertIn("r13_hidden_base_restore_return()",exit_block)

if __name__=='__main__':unittest.main()
