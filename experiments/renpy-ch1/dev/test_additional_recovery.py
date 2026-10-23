"""Additional QA: morning checkpoints preserve and replace the right timeline."""
import copy
import random
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'game/systems/room13_polish3.rpy').read_text()
CODE = textwrap.dedent(SOURCE[SOURCE.index('    def r13_morning_slot('):SOURCE.index('    config.overlay_screens.append("r13_morning_watch")')])
DAY1 = ['V111:' + key for key in ('E01','E02','E03','E04','E05','E06','E30')]

class MorningRecovery(unittest.TestCase):
    def setUp(self):
        self.store = SimpleNamespace(room13_mode=True, r13_meeting_active=False, room13={
            'day':2,'period':0,'location':'room13','evidence':list(DAY1),
            'records':{key:{'day':1} for key in DAY1},
            'v111':{'gate':'travel','travel_to':'gate','values':{'mother_box_checked_day2':False,'elapsed_minutes':0}},
            'checks':{},'arguments':{},'record_ui':{'seen':['V111:E01']}})
        self.persistent = SimpleNamespace(r13_mornings={})
        self.saved = {}
        self.loaded = []
        def save(slot, **kwargs): self.saved[slot] = copy.deepcopy(self.store.room13)
        def load(slot):
            self.loaded.append(slot)
            self.store.room13 = copy.deepcopy(self.saved[slot])
        self.env = {'store':self.store,'persistent':self.persistent,'_r13_random':random.Random(25),
                    'r13_edit':lambda **kw:self.store.room13.update(copy.deepcopy(kw)),
                    'r13_shortcut_field':lambda:True,
                    'renpy':SimpleNamespace(save=save,load=load,save_persistent=lambda:None,
                        retain_after_load=lambda:None,can_load=lambda slot:slot in self.saved)}
        exec(CODE,self.env)

    def complete_box(self):
        self.store.room13['location']='forest'
        self.store.room13['v111']['travel_to']='post'
        self.store.room13['v111']['values'].update(mother_box_checked_day2=True,arrival_note_sent=True,elapsed_minutes=60)
        self.store.room13['checks']['box']={'day':2}

    def test_restore_replaces_complete_state_and_retains_day1_records(self):
        self.env['r13_morning_snapshot']()
        morning=copy.deepcopy(self.store.room13)
        self.complete_box()
        self.env['r13_morning_restore'](2)
        self.assertEqual(self.store.room13,morning)
        self.assertEqual(self.store.room13['evidence'],DAY1)
        self.assertNotIn('arrival_note_sent',self.store.room13['v111']['values'])
        self.assertEqual(self.loaded,['r13morning-2'])

    def test_selection_queries_are_read_only(self):
        self.env['r13_morning_snapshot']();self.complete_box()
        before=copy.deepcopy((self.store.room13,self.persistent.r13_mornings,self.saved))
        self.assertEqual(self.env['r13_morning_days'](),[2])
        self.assertFalse(self.env['r13_morning_due']())
        self.assertEqual((self.store.room13,self.persistent.r13_mornings,self.saved),before)
        self.assertFalse(self.loaded)

    def test_replaying_day_does_not_overwrite_the_morning(self):
        self.env['r13_morning_snapshot']();morning=copy.deepcopy(self.saved['r13morning-2'])
        self.complete_box();self.env['r13_morning_snapshot']()
        self.assertEqual(self.saved['r13morning-2'],morning)
        self.env['r13_morning_restore'](2);self.complete_box();self.env['r13_morning_snapshot']()
        self.assertEqual(self.saved['r13morning-2'],morning)

    def test_manual_save_restores_its_own_time_after_morning_restart(self):
        self.env['r13_morning_snapshot']();self.complete_box()
        manual=copy.deepcopy(self.store.room13);self.env['renpy'].save('1-2')
        self.env['r13_morning_restore'](2)
        self.assertNotEqual(self.store.room13,manual)
        self.env['renpy'].load('1-2')
        self.assertEqual(self.store.room13,manual)
        self.assertEqual(self.env['r13_morning_days'](),[2])

    def test_other_run_and_abandoned_branch_mornings_are_not_offered(self):
        self.env['r13_morning_snapshot']()
        self.store.room13['morning_ids']['2']='different-path'
        self.assertEqual(self.env['r13_morning_days'](),[])
        self.assertTrue(self.env['r13_morning_due']())
        self.store.room13['run_token']='another-run'
        self.assertEqual(self.env['r13_morning_days'](),[])

if __name__=='__main__':unittest.main()
