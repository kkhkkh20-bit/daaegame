import copy
from pathlib import Path
import textwrap
import types
import unittest

ROOT=Path(__file__).resolve().parents[1]
class RetryLogic(unittest.TestCase):
    def setUp(self):
        self.store=types.SimpleNamespace(room13={'v111':{'values':{'alive:piko':False,'meeting:fire':'win'}},'evidence':['before'],'arguments':{},'flags':['before']},r13_meeting_checkpoint_state=None)
        source=(ROOT/'game/room13_meeting_retry_logic.rpy').read_text().split('init 324 python:\n',1)[1]
        self.ns=dict(store=self.store,winter_copy=copy)
        exec(textwrap.dedent(source),self.ns)
    def test_repeated_restore_preserves_pre_meeting_and_removes_partial_progress(self):
        original=copy.deepcopy(self.store.room13)
        self.ns['r13_meeting_checkpoint']('lamp')
        for _ in range(2):
            self.store.room13['v111']['values'].update({'tries:lamp':7,'proof_given:test':['before'],'OWL_ALIVE':False})
            self.store.room13['evidence'].append('during')
            self.store.room13['flags'].append('v111:applied:test')
            self.store.room13['arguments']['test']=['before']
            self.ns['r13_meeting_checkpoint']('lamp')
            self.assertTrue(self.ns['r13_meeting_restore']('lamp'))
            self.assertEqual(original,self.store.room13)
    def test_missing_checkpoint_does_not_invent_past(self):
        before=copy.deepcopy(self.store.room13)
        self.assertFalse(self.ns['r13_meeting_restore']('room13'))
        self.assertEqual(before,self.store.room13)
    def test_old_save_with_spent_chances_cannot_create_partial_checkpoint(self):
        self.store.room13['v111']['values']['tries:lamp']=2
        self.ns['r13_meeting_checkpoint']('lamp')
        self.assertIsNone(self.store.r13_meeting_checkpoint_state)

    def test_all_meetings_have_real_start_hooks(self):
        files='\n'.join(p.read_text() for p in (ROOT/'game').glob('room13_v111_days*.rpy'))
        self.assertEqual(len(self.ns['R13_MEETING_RESTART_LABELS']),11)
        for meeting,label in self.ns['R13_MEETING_RESTART_LABELS'].items():
            self.assertIn('label '+label+':\n    $ r13_meeting_checkpoint("'+meeting+'")',files)
