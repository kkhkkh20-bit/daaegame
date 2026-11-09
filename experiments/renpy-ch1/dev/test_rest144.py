"""잠자기 진입 조건과 옛 자동 수면 예약의 호환을 확인한다."""
import copy
import unittest
from types import SimpleNamespace
from test_play_review_field import load_function,ROOT

class Rest144(unittest.TestCase):
    def env(self,gate='sleep1',location='room13'):
        state=SimpleNamespace(room13=dict(day=1,location=location,v111=dict(gate=gate)),r13_v111_bed_pending=None)
        binding=dict(options=[dict(index=0,object='bed',location='room13')])
        env=dict(store=state,r13_v111_active=lambda:True,r13_v111_binding=lambda:binding)
        # 선언과 함수만 읽고 Ren'Py는 실행하지 않는다.
        import ast,textwrap
        source=(ROOT/'game/systems/room13_rest144.rpy').read_text().split('init 353 python:\n')[1].split('\nlabel ')[0]
        exec(textwrap.dedent(source),env)
        load_function('game/room13_v111.rpy','r13_v111_auto_index',env)
        return env,state,binding

    def test_only_actual_rest_stage_and_current_sleeping_place_offer_sleep(self):
        env,state,b=self.env();before=copy.deepcopy(state.room13)
        self.assertEqual(env['r13_v111_rest_option']()['index'],0)
        self.assertEqual(state.room13,before)
        for gate,place in [('note_pick','room13'),('room_observe','room13'),('sleep1','inn'),('handoff6','school')]:
            state.room13.update(location=place);state.room13['v111']['gate']=gate
            self.assertIsNone(env['r13_v111_rest_option']())

    def test_old_string_pending_does_not_skip_new_confirmation(self):
        env,state,b=self.env('sleep2');state.r13_v111_bed_pending='sleep2'
        self.assertIsNone(env['r13_v111_auto_index']('sleep2'))
        self.assertIsNone(state.r13_v111_bed_pending)

    def test_confirmed_chain_is_same_day_and_consumed_once(self):
        env,state,b=self.env('sleep2');state.r13_v111_bed_pending=('sleep2',1)
        self.assertEqual(env['r13_v111_auto_index']('sleep2'),0)
        self.assertIsNone(env['r13_v111_auto_index']('sleep2'))
        state.r13_v111_bed_pending=('sleep2',2)
        self.assertIsNone(env['r13_v111_auto_index']('sleep2'))

    def test_bed_placeholder_cannot_fall_through_to_dad_noun_dialogue(self):
        source=(ROOT/'game/room13_v111.rpy').read_text()
        self.assertIn('if v111_pick[1]=="bed" and room13["location"] in ("room13","guestroom"):',source)
        self.assertIn('call r13_v111_rest_confirm',source)
        self.assertIn('if not _return:\n                    jump r13_v111_wait_again',source)
        self.assertIn('control_id="r13_rest_sleep"',(ROOT/'game/room13_screens.rpy').read_text())

if __name__=='__main__':unittest.main()
