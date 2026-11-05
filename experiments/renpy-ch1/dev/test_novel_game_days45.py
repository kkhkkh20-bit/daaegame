"""소설 개정의 편지 전달·정보 취득과 기존 분기 보존 회귀 검사."""
import copy
import re
import unittest

from test_newworld_text import Layer


def plain(text):
    return re.sub(r'\s+|\{image=[^}]+\}', '', text)


class NovelGameDays45(Layer):
    def test_letter_on_screen_and_in_record_say_the_same_thing(self):
        env = self.load()
        onscreen = ''.join(row[1] for name in ('warning_first5', 'warning_rest5')
                           for row in env['r13_nw_block'](name))
        record = env['R13_V111']['evidence']['E27']['variants']['observed']
        self.assertEqual(plain(onscreen), plain(record))
        for fact in ('첫날', '마차', '너울', '돌목', '여관', '길목', '교환함', '발자국'):
            self.assertIn(fact, onscreen)
        self.assertNotIn('13호에서', onscreen, '첫 답장이 7일 사건을 미리 알면 안 된다')

    def test_envelope_or_legacy_record_is_not_new_contact_read_or_proof(self):
        env = self.load()
        env['r13_v111_commit']('MS14_D05_S04_L0005')
        self.assertTrue(env['r13_v111_owned']('E27'))
        self.assertTrue(env['r13_v111_value']('mother_warning_received'))
        self.assertIsNot(env['r13_v111_value']('mother_first_contact_read5'), True)
        self.assertIsNot(env['r13_v111_value']('mother_denies_invitation'), True)
        before = copy.deepcopy(self.state.room13)
        env['r13_nw_block']('warning_first5')
        env['r13_nw_block']('warning_rest5')
        self.assertEqual(before, self.state.room13, '문장 생성만으로 청취·제출 상태를 설정하지 않는다')
        env['r13_v111_commit']('MS14_D05_S04_L0014')
        self.assertTrue(env['r13_v111_value']('mother_denies_invitation'))

    def test_child_absence_hides_whole_parent_child_correction(self):
        env = self.load()
        env['r13_v111_actor_ready'] = lambda who: False
        absent = env['r13_v111_lines'](['MS14_D04_S04_L0015'])
        self.assertFalse(any('작은 그림자' in row[1] for row in absent))
        self.assertFalse(any('내가 더한 말' in row[1] for row in absent))
        env['r13_v111_actor_ready'] = lambda who: who == 'daram'
        present = env['r13_v111_lines'](['MS14_D04_S04_L0015'])
        self.assertEqual([row[0] for row in present[:3]], ['dad', 'daram', 'dad'])

    def test_retry_feeling_does_not_mutate_meeting_or_grant_materials(self):
        env = self.load()
        for outcome in (None, 'lose', 'win'):
            env['r13_v111_set']('meeting:gate_post', outcome)
            env['r13_v111_set']('tries:gate_post', 2)
            before = copy.deepcopy(self.state.room13)
            env['r13_nw_block']('gate_post_retry_feeling5')
            self.assertEqual(before, self.state.room13)


if __name__ == '__main__':
    unittest.main()
