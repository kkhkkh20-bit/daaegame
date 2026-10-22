"""Read-only fork visibility and persistent observation contracts without Ren'Py."""
import ast
import copy
import textwrap
import unittest
from types import SimpleNamespace
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ForkScreen(unittest.TestCase):
    def setUp(self):
        self.values={}
        self.store=SimpleNamespace(room13={'v111':{},'day':1},r13_meeting_active=False)
        self.persistent=SimpleNamespace(r13_fork_runs=0,r13_fork_seen={},r13_fork_endings={})
        self.saves=[]
        def capture(size):
            self.assertEqual(size,(320,180))
            return b'png'
        self.env=dict(store=self.store,persistent=self.persistent,
            renpy=SimpleNamespace(screenshot_to_bytes=capture,save_persistent=lambda:self.saves.append(True)),
            r13_v111_value=lambda key:self.values.get(key))
        source=(ROOT/'game/room13_fork_screen.rpy').read_text().split('init 322 python:\n')[1].split('\nscreen ')[0]
        exec(textwrap.dedent(source),self.env)
    def call(self,name,*args):
        return self.env['r13_fork_'+name](*args)
    def test_future_is_one_opaque_column_even_with_later_discoveries(self):
        self.persistent.r13_fork_seen[('altar','win')]={'png':b'png'}
        columns=self.call('columns')
        self.assertEqual(len(columns),2)
        self.assertEqual(columns[-1],dict(key=None,day='그 너머',rows=[]))
        self.assertEqual(len(columns[0]['rows']),1)
    def test_missed_results_have_no_title_or_result(self):
        self.values['meeting:gate']='win'
        rows=self.call('columns')[0]['rows']
        self.assertEqual(len(rows),3)
        for row in rows[1:]:
            self.assertEqual(row['kind'],'locked')
            self.assertIsNone(row['title'])
            self.assertIsNone(row['result'])
    def test_saved_path_changes_independently_of_persistent(self):
        self.call('record','gate','partial')
        self.values['meeting:gate']='win'
        rows=self.call('columns')[0]['rows']
        self.assertEqual(rows[0]['result'],'win')
        self.assertEqual(rows[1]['kind'],'old')
        self.values.clear()  # load an earlier save
        self.assertEqual(self.call('current'),0)
        self.assertEqual(len(self.call('columns')[0]['rows']),1)
        self.assertIn(('gate','partial'),self.persistent.r13_fork_seen)
    def test_active_stage_wins_and_initial_page_contains_it(self):
        self.store.r13_meeting_active=True
        self.store.r13_meeting_claim='NW:soup'
        self.assertEqual(self.call('current'),7)
        self.assertLessEqual(self.call('initial_page'),7)
        self.assertGreater(self.call('initial_page')+6,7)
    def test_run_number_is_saved_and_reading_does_not_increment(self):
        self.call('start')
        saved=copy.deepcopy(self.store.room13)
        self.call('start')
        self.store.room13=saved
        self.call('columns')
        self.assertEqual(self.store.room13['v111']['fork_run'],1)
        self.assertEqual(self.persistent.r13_fork_runs,2)
    def test_capture_failure_is_recorded_and_latest_replaces_bytes(self):
        self.call('record','gate','win')
        self.assertEqual(self.persistent.r13_fork_seen[('gate','win')]['png'],b'png')
        def fail(size):raise RuntimeError('web')
        self.env['renpy'].screenshot_to_bytes=fail
        self.call('record','gate','win')
        self.assertIsNone(self.persistent.r13_fork_seen[('gate','win')]['png'])
        self.call('ending','true')
        self.assertIn('true',self.persistent.r13_fork_endings)
        self.assertTrue(self.saves)
    def test_meeting_hook_records_only_first_decision(self):
        source=(ROOT/'game/room13_v111_newworld_rules.rpy').read_text()
        code=source.split('init 318 python:\n')[1].split('    R13_NW_LISTABLE=')[0]
        tree=ast.parse(textwrap.dedent(code))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_nw_meeting_end')
        self.env.update(R13_NW_MEETING_RESULTS=('win','partial','lose'),r13_v111_set=lambda k,v:self.values.update({k:v}))
        exec(compile(ast.Module(body=[node],type_ignores=[]),'meeting','exec'),self.env)
        self.env['r13_nw_meeting_end']('gate','win')
        self.env['r13_nw_meeting_end']('gate','lose')
        self.assertEqual(self.values['meeting:gate'],'win')
        self.assertEqual(list(self.persistent.r13_fork_seen),[('gate','win')])
        self.assertEqual(len(self.saves),1)
    def test_capture_fallback_uses_meeting_place(self):
        self.env.update(R13_PLACES={'room13':('13호실','room'),'square':('광장','winter_square')},r13_background=lambda name:'bg:'+name)
        self.assertEqual(self.call('image',{'png':None},'room13'),'bg:room')

    def test_all_completed_has_no_future_and_valid_page(self):
        self.values.update({'meeting:'+m[0]:'win' for m in self.env['R13_FORK_MEETINGS']})
        self.assertEqual(self.call('current'),11)
        self.assertEqual(len(self.call('columns')),11)
        self.assertEqual(self.call('initial_page'),5)

if __name__=='__main__':unittest.main()
