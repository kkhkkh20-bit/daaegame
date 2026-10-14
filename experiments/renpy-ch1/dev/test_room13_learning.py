"""Protect no-spoiler/read-only boundaries and displayed time/settlement truth."""
import copy
import textwrap
import types
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class LearningTest(unittest.TestCase):
    def setUp(self):
        self.store=types.SimpleNamespace(room13=dict(day=2,period=0,life_poc=True,evidence=[],flags=[],read_topics=[]))
        self.persistent=types.SimpleNamespace(room13_knowledge=[])
        evidence={k:dict(kind="증언" if k=="E10" else "기록") for k in ("G1","G3","E01","M01","E10","E20","E21","E22","E23","E24","E30")}
        self.ns=dict(store=self.store,persistent=self.persistent,R13_NAMES=dict(karo="까로",resident_lamplighter="초롱"),
                     ROOM13=dict(evidence=evidence,evidence_sources={}),winter_copy=copy,
                     r13_first_mystery_notes=lambda:[dict(title="엄마의 행적",keys=[])])
        model=(ROOT/'game/systems/room13_livelihood_model.rpy').read_text().split('init 91 python:\n')[1]
        exec(textwrap.dedent(model),self.ns)
        def entries(category="evidence",archive=False,present=False,order="acquired",favorite_only=False):
            return list(self.persistent.room13_knowledge if archive and not present else self.store.room13['evidence'])
        self.ns['r13_record_entries']=entries
        source=(ROOT/'game/systems/room13_learning.rpy').read_text().split('init 98 python:\n')[1].split('\nscreen r13_learning_notes():')[0]
        exec(textwrap.dedent(source),self.ns)

    def test_first_run_current_records_do_not_create_previous_play(self):
        s=self.store.room13;s['learning_archive']=self.ns['r13_learning_archive_seed']()
        s['evidence']=['E01','M01'];self.persistent.room13_knowledge=['E01','M01']
        self.assertEqual(self.ns['r13_learning_archive_keys'](),[])
        self.assertEqual(self.ns['r13_record_entries'](archive=True),[])
        # No carryover (owner's rule): a new run shows no earlier-run records,
        # even when the save holds a snapshot.
        s['learning_archive']=self.ns['r13_learning_archive_seed']();s['evidence']=[]
        before=copy.deepcopy(s)
        self.assertEqual(self.ns['r13_record_entries'](archive=True),[])
        self.assertEqual(self.ns['r13_record_entries'](archive=True,present=True),[])
        self.assertEqual(s,before)

    def test_legacy_archive_never_lists_previous_play(self):
        self.persistent.room13_knowledge=['E01','M01'];self.store.room13['evidence']=['E01']
        self.assertEqual(self.ns['r13_learning_archive_keys'](),[])

    def test_world_notes_require_current_owned_evidence_not_day_or_persistent(self):
        s=self.store.room13;s['day']=14
        self.persistent.room13_knowledge=['E20','E21','E22','E23','E24','E30']
        self.assertEqual(self.ns['r13_learning_terms'](),[])
        s['evidence']=['E23'];before=copy.deepcopy(s)
        rows=self.ns['r13_learning_terms']()
        self.assertEqual([r['title'] for r in rows],['힘을 옮긴다는 것'])
        self.assertEqual(s,before)

    def test_preview_matches_real_lodging_settlement_without_writes(self):
        for day,cash,debt,settled in ((1,0,0,[]),(2,4,3,[]),(2,10,0,[]),(2,12,2,[]),(2,7,0,[2])):
            s=dict(day=day,period=0,livelihood=dict(cash=cash,debt=debt,settled=settled))
            original=copy.deepcopy(s);p=self.ns['r13_learning_lodging_preview'](s)
            actual=self.ns['r13_wallet'](self.ns['r13_settle_lodging'](s))
            self.assertEqual((p['left'],p['debt']),(actual['cash'],actual['debt']))
            self.assertEqual(s,original)
        s=dict(day=2,period=0,livelihood=dict(cash=1,debt=2,settled=[]))
        p=self.ns['r13_learning_lodging_preview'](s,6)
        self.assertEqual((p['paid'],p['added_debt'],p['left']),(7,3,0))

    def test_action_time_never_promises_automatic_next_day(self):
        f=self.ns['r13_learning_time_text']
        self.assertIn('오후',f(1,dict(period=0)))
        self.assertIn('저녁',f(1,dict(period=1)))
        self.assertIn('늦은 저녁',f(1,dict(period=2)))
        self.assertIn('없음',f(1,dict(period=3)))
        self.assertEqual(f(0,dict(period=3)),'시간 소모 없음')
        self.assertIn('여정이 끝날',f(0,ending=True))

    def test_sleep_preview_handles_event_night_and_old_no_economy_save(self):
        s=self.store.room13;s.update(day=4,case_state='pending')
        text=self.ns['r13_learning_sleep_text']();self.assertIn('저녁을',text);self.assertNotIn('다음 날',text)
        s.update(day=2,case_state='occurred',life_poc=False)
        text=self.ns['r13_learning_sleep_text']();self.assertNotIn('숙식',text);self.assertIn('남은 낮',text)
        s.update(life_poc=True,period=2)
        text=self.ns['r13_learning_sleep_text']();self.assertIn('외상',text);self.assertNotIn('남은 낮',text)

    def test_witness_permission_uses_consent_not_merely_protection(self):
        s=self.store.room13;s['flags']=['bami_protected']
        self.assertIn('허락 필요',self.ns['r13_learning_record_status']('E10'))
        s['flags'].append('bami_consent')
        self.assertIn('사용 가능',self.ns['r13_learning_record_status']('E10'))

    def test_gate_question_precedes_mother_notes_and_no_hidden_job_secrets(self):
        s=self.store.room13;s.update(evidence=['G1'])
        rows=self.ns['r13_first_mystery_notes']()
        self.assertIn('한 명',rows[0]['title']);self.assertEqual(rows[0]['keys'],['G1'])
        s['flags'].append('entry_corrected')
        self.assertEqual(self.ns['r13_first_mystery_notes']()[0]['title'],'엄마의 행적')
        self.assertEqual(self.ns['r13_person_caption']('karo'),'까로 · 마부')
        self.assertNotIn('비밀',str(self.ns['R13_PUBLIC_ROLES']))
        self.assertNotIn('초롱',self.ns['r13_learning_job_context']('kitchen',dict(flags=[],read_topics=[])))

if __name__=='__main__':unittest.main()
