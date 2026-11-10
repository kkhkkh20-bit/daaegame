"""3일 피코 사건에서 관찰·판단·돌봄 약속의 정보 경계를 확인한다."""
import copy
import re
from test_newworld_text import Layer, ROOT


class PikoCaseDeduction(Layer):
    def test_early_record_keeps_location_without_answering_the_later_claim(self):
        env=self.load()
        text=env['R13_V111']['evidence']['E32']['variants']['observed']
        self.assertIn('안쪽 틈',text)
        self.assertIn('방향',text)
        self.assertIn('그림',text)
        self.assertNotIn('닿지 않는다',text)
        src=(ROOT/'game/room13_v111_days123.rpy').read_text()
        scene=src.split('label r13_v111_lamp_fragment3:',1)[1].split('\nlabel ',1)[0]
        self.assertLess(scene.index('MS14_D03_S02_L0018'),scene.index('MS14_D03_S02_L9102'))
        self.assertIn("['E17', 'E32', 'E33']",src.split('label r13_v111_trial_latch:',1)[1].split('\nlabel ',1)[0])

    def test_morning_discovery_does_not_claim_to_know_death_time(self):
        env=self.load()
        env['r13_v111_set']('piko_alive',False)
        lines=env['r13_v111_lines'](['MS14_D03_S01_L0020','MS14_D03_S05_L0038'])
        text=' '.join(r[1] for r in lines)
        self.assertIn('아침에',text)
        self.assertIn('발견',text)
        self.assertIn('언제 숨졌는지는 아직 모릅니다',text)
        self.assertNotIn('없어진 뒤에도',text)

    def test_viewing_new_reactions_does_not_finish_care_or_change_custody(self):
        for status in ('reporting_obligation','detained_work_waiting_station'):
            env=self.load()
            self.state.room13.update(day=3,location='workshop',period=1)
            env['r13_v111_set']('silluk_status',status)
            env['r13_v111_set']('silluk.children.location','workshop_with_buri')
            before=copy.deepcopy(self.state.room13)
            for block in ('piko_latch_shape3','piko_latch_time3','piko_children_report3','piko_children_transfer3'):
                rows=env['r13_nw_block'](block)
                self.assertTrue(rows)
            self.assertEqual(self.state.room13,before)
            self.assertEqual(env['r13_v111_value']('silluk.children.location'),'workshop_with_buri')
