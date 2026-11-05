"""소설 개정의 실제 인계·정보 시점과 구 저장 호환을 함께 검증한다."""
import copy
import unittest
from test_newworld_text import Layer, ROOT

class NovelDays610(Layer):
    def test_corridor_operation_keeps_other_commit_fields_and_source_record(self):
        env=self.load()
        rid='MS14_D07_S03_L0031'
        before=copy.deepcopy(env['R13_V111']['records'][rid]['operations'])
        line=next(l.strip()[2:] for l in (ROOT/'game/room13_v111_days610.rpy').read_text().splitlines() if "$ r13_v111_apply('MS14_D07_S03_L0031'" in l)
        exec(line,env)
        for key,value in [('DOTO_location','hall'),('DARAM_guardian','DOTO'),('father_location','medical_route'),('D07_S03_C_completed',True)]:
            self.assertEqual(env['r13_v111_value'](key),value)
        self.assertEqual(env['R13_V111']['records'][rid]['operations'],before)
        env['r13_v111_set']('DOTO_location','later_place')
        exec(line,env)
        self.assertEqual(env['r13_v111_value']('DOTO_location'),'later_place','재실행한 완료 처리가 이후 위치를 되돌리지 않는다')

    def test_old_room_save_and_new_corridor_dialogue_are_distinct(self):
        env=self.load(); rid='MS14_D07_S03_L0023'
        self.assertIn('침대',env['r13_v111_line'](rid)[1])
        env['r13_v111_set']('corridor_handover7',True)
        self.assertIn('다시 들여보내지',env['r13_v111_line'](rid)[1])
        self.assertNotIn('침대',env['r13_v111_line'](rid)[1])

    def test_blanket_carrier_does_not_reintroduce_himself_after_actual_loan(self):
        env=self.load(); rid='MS14_D06_P01_L0011'
        self.assertIn('도토예요',env['r13_v111_line'](rid)[1])
        env['r13_v111_set']('school_blankets_prepared6',True)
        self.assertNotIn('도토예요',env['r13_v111_line'](rid)[1])
        self.assertIn('담요',env['r13_v111_line'](rid)[1])

    def test_letter_source_date_and_privacy_survive_both_routes(self):
        env=self.load()
        for rid in ('MS14_D08_S04_L0012','MS14_D08_S04_L0020'):
            text=env['r13_v111_line'](rid)[1]
            self.assertIn('날짜는 6일',text)
            self.assertIn('발소리가 와서 자리를 옮겼어',text)
            self.assertNotIn('보호실',text)
            self.assertNotIn('다람이가 붙잡',text)
        raw=env['R13_V111']['records']['MS14_D08_S04_L0033']['operations']
        self.assertIn(dict(op='set',field='mother_secret_shared',value=False),raw)
        self.assertIn(dict(op='set',field='mother_location',value='unknown'),raw)

    def test_confirmed_relay_does_not_undo_the_message_it_just_confirmed(self):
        env=self.load()
        self.assertIn('답이 와 있을지도',env['r13_v111_line']('MS14_D10_S04_L0018')[1])
        env['r13_v111_set']('mother_contact_relay10',True)
        self.assertIn('같이 볼래',env['r13_v111_line']('MS14_D10_S04_L0017')[1])
        self.assertNotIn('답이 와 있을지도',env['r13_v111_line']('MS14_D10_S04_L0018')[1])
        self.assertIn('같이 보자',env['r13_v111_line']('MS14_D10_S04_L0018')[1])

    def test_passage_record_separates_two_different_doors(self):
        env=self.load()
        text=env['R13_V111']['evidence']['E09_PASSAGE']['variants']['observed']
        self.assertIn('수동 손잡이는 주방 레버와 관계없이',text)
        self.assertIn('별도의 판자문',text)
        for rid in ('MS14_D09_S01_L0015','MS14_D09_P01_L0004'):
            self.assertNotIn('잡고 있을게',env['r13_v111_line'](rid)[1])
        self.assertEqual(env['ROOM13']['evidence']['V111:E10_PUMP']['name'],'물자 연락함의 위치')
        self.assertIn('마지막으로 기재된 날짜',env['R13_V111']['evidence']['E10_PUMP']['variants']['observed'])

if __name__=='__main__':unittest.main()
