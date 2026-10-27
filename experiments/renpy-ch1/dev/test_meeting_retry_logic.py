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
            # 2026-10-27 외부 리뷰 R08: 조사로 얻은 자료는 남고, 회의 상태(기회·논증·applied 깃발)만 되돌아간다.
            restored=copy.deepcopy(self.store.room13)
            self.assertIn('during',restored.pop('evidence'))
            expected=copy.deepcopy(original);expected.pop('evidence')
            self.assertEqual(expected,restored)
    def test_restore_keeps_investigation_results_but_resets_meeting(self):
        self.store.room13.update(records={'before':{'day':1}},read_topics=['t0'],checks={},observations={})
        self.ns['r13_meeting_checkpoint']('lamp')
        r=self.store.room13
        r['evidence'].append('V111:E03');r['records']['V111:E03']={'day':1,'source':'gate'}
        r['read_topics'].append('t1');r['checks']['gate:rules']=(1,2);r['observations']['first']={'x':1}
        r['flags']+=['observed:gate:rules','v111:applied:MS14_D01_S03_L0002','v111:applied:meeting_line']
        r['v111']['values'].update({'E03.variant':'observed','tries:lamp':3,'proof_given:x':['a']})
        r['arguments']['claim']=['V111:E03']
        self.assertTrue(self.ns['r13_meeting_restore']('lamp'))
        r=self.store.room13
        self.assertEqual(r['evidence'],['before','V111:E03'])
        self.assertEqual(r['records'],{'before':{'day':1},'V111:E03':{'day':1,'source':'gate'}})
        self.assertEqual(r['read_topics'],['t0','t1'])
        self.assertEqual(r['checks'],{'gate:rules':(1,2)})
        self.assertEqual(r['observations'],{'first':{'x':1}})
        self.assertEqual(r['flags'],['before','observed:gate:rules'])
        self.assertEqual(r['v111']['values'].get('E03.variant'),'observed')
        self.assertNotIn('tries:lamp',r['v111']['values']);self.assertNotIn('proof_given:x',r['v111']['values'])
        self.assertEqual(r['arguments'],{})
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
