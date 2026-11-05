"""등록 뒤 너울의 첫 등장과 초소에서 듣는 문답을 확인한다."""
import copy
import unittest
from types import SimpleNamespace

from test_newworld_text import Layer, ROOT
from test_play_review_field import load_function


class OpeningDeparture(Layer):
    def departure(self, origin, unlisted):
        env = self.load()
        self.state.room13['location'] = origin
        env['r13_v111_set']('gate_daram_unlisted', unlisted)
        env['r13_v111_set']('gate_registered', True)
        env['r13_v111_set']('location:daram', origin)
        env['r13_v111_set']('location:guard', 'gate')
        env['r13_v111_set']('location:karo', 'gate')
        calls = []
        env.update(
            r13_edit=lambda **values: self.state.room13.update(values),
            R13_PLACES={'gate': ('마을 초소', 'gate_background')},
            renpy=SimpleNamespace(call=lambda *args: calls.append((args, copy.deepcopy(self.state.room13)))),
        )
        # 실제 현재 배우 등록 함수를 써 위치와 사람 목록을 함께 확인한다.
        load_function('game/room13_v111_later_bindings.rpy', 'r13_v111_arrive', env)
        fn = load_function('game/systems/room13_depart_booth.rpy', 'r13_v111_depart_from_booth', env)
        before_evidence = copy.deepcopy(self.state.room13['evidence'])
        fn()
        self.assertEqual(self.state.room13['location'], 'gate')
        self.assertEqual(self.state.room13['v111']['people'], ['guard', 'daram', 'karo', 'neoul'])
        for person in self.state.room13['v111']['people']:
            self.assertEqual(env['r13_v111_value']('location:' + person), 'gate')
        self.assertEqual(before_evidence, self.state.room13['evidence'])
        self.assertEqual(env['r13_v111_value']('gate_daram_unlisted'), unlisted)
        self.assertTrue(env['r13_v111_value']('gate_registered'))
        self.assertEqual(self.state.v111_depart_direct, origin != 'gate')
        self.assertEqual(len(calls), int(origin != 'gate'))
        for args, scene_state in calls:
            self.assertEqual(args, ('r13_scene', 'gate_background', '마을 초소', 'calm'))
            self.assertEqual(scene_state['location'], 'gate')
            self.assertIn('neoul', scene_state['v111']['people'])
        return env

    def test_normal_and_map_departure_stage_the_same_actual_people(self):
        for origin in ('gate', 'inn'):
            for unlisted in (False, True):
                with self.subTest(origin=origin, unlisted=unlisted):
                    self.departure(origin, unlisted)

    def test_greeting_and_father_reply_precede_the_rule_on_both_registration_paths(self):
        for unlisted in (False, True):
            with self.subTest(unlisted=unlisted):
                env = self.departure('inn', unlisted)
                env['r13_v111_actor_ready'] = lambda person: person in self.state.room13['v111']['people']
                rows = env['r13_v111_lines'](['MS14_D01_S04_L0018', 'MS14_D01_S04_L0019', 'MS14_D01_S04_L0020', 'MS14_D01_S04_L0021'])
                texts = [row[1] for row in rows]
                index = lambda term: next(i for i, text in enumerate(texts) if term in text)
                self.assertLess(index('초소 안쪽에서 다가온다'), index('너울 씨, 이 두 분'))
                self.assertLess(index('마을 장부를 맡은 너울이오'), index('아내가 13호실에서 기다린다고'))
                self.assertLess(index('아내가 13호실에서 기다린다고'), index('그 방이 당신 주소요'))
                self.assertLess(index('돌목 쪽으로 돌아선다'), index('돌목 씨,'))
                self.assertLess(index('누가 그런 부탁을'), index('묵는 사람 소식은 여관에'))
                self.assertLess(index('묵는 사람 소식은 여관에'), index('엄마 어디 갔대'))
                joined = ' '.join(texts)
                self.assertNotIn('인사 대신', joined)
                self.assertNotIn('며칠째 안 보여', joined)
                self.assertEqual('정정한 표를 접으며' in joined, not unlisted)


if __name__ == '__main__':
    unittest.main()
