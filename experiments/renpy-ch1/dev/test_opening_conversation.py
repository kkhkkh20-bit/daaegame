"""첫날 부녀 문답의 지식 순서와 두 종이 대조의 목적·다음 행동을 확인한다."""
import copy
import unittest

from test_newworld_text import Layer, ROOT


class OpeningConversation(Layer):
    def texts(self, env, ids):
        return [row[1] for row in env['r13_v111_lines'](ids)]

    def test_carriage_keeps_one_snack_request_and_answers_the_reading_question(self):
        env = self.load()
        before = copy.deepcopy(self.state.room13)
        source = (ROOT / 'game/room13_v111_days123.rpy').read_text()
        self.assertIn("r13_nw_block('carriage_snack1'), 'v111:carriage:before-bump'", source)
        snack = [row[1] for row in env['r13_nw_block']('carriage_snack1')]
        self.assertEqual(sum('반씩' in text or '반만' in text for text in snack), 1)
        self.assertLess(next(i for i, text in enumerate(snack) if '엄마는 아직' in text),
                        next(i for i, text in enumerate(snack) if '잘 싸' in text))
        reading = self.texts(env, ['MS14_D01_S01_L0015', 'MS14_D01_S01_L0016'])
        question = next(i for i, text in enumerate(reading) if '멈췄지' in text)
        self.assertIn('엄마가 문 열고', reading[question + 1])
        sleeping = self.texts(env, ['MS14_D01_S01_L0019', 'MS14_D01_S01_L0020', 'MS14_D01_S01_L0021'])
        index = lambda term: next(i for i, text in enumerate(sleeping) if term in text)
        self.assertLess(index('엄마 옆'), index('그럼 내가 가운데'))
        self.assertLess(index('그럼 내가 가운데'), index('코 골면'))
        self.assertEqual(self.state.room13, before, '표시 대사 조회가 이야기 상태를 만들지 않는다')

    def test_inn_child_reacts_after_the_missing_news(self):
        env = self.load()
        before = copy.deepcopy(self.state.room13)
        rows = self.texts(env, ['MS14_D01_S05_L0005', 'MS14_D01_S05_L0006',
                               'MS14_D01_S05_L0007', 'MS14_D01_S05_L0008',
                               'MS14_D01_S05_L0009', 'MS14_D01_S05_L0010',
                               'MS14_D01_S05_L0011', 'MS14_D01_S05_L0012'])
        index = lambda term: next(i for i, text in enumerate(rows) if term in text)
        self.assertLess(index('편지를 펼친다'), index('13호실에 있습니까'))
        self.assertLess(index('며칠째 안 보여'), index('엄마가 여기 없는 거야'))
        self.assertLess(index('엄마가 여기 없는 거야'), index('기다리고 계실 줄'))
        self.assertLess(index('어디 간다는 말'), index('어디로 간다는 말은'))
        self.assertLess(index('어디로 간다는 말은'), index('마지막으로 돌아와서'))
        self.assertNotIn('아빠는 알고 있었어?', ' '.join(rows))
        self.assertEqual(self.state.room13, before)

    def test_letter_comparison_sets_a_question_and_then_a_concrete_lead(self):
        env = self.load()
        setup = self.texts(env, ['MS14_D01_S05_L0029', 'MS14_D01_S05_L0030'])
        self.assertIn('같은 사람이 쓴 건지', ' '.join(setup))
        self.assertNotIn('도토리', ' '.join(setup), '관찰할 위치나 차이를 먼저 알려 주지 않는다')
        for observed in (False, True):
            with self.subTest(tail_observed=observed):
                env['r13_v111_set']('letter_tail_observed', observed)
                before = copy.deepcopy(self.state.room13)
                rows = []
                if observed:
                    rows += [row[1] for row in env['r13_nw_block']('letter_observe_tail')]
                rows += self.texts(env, ['MS14_D01_S05_L0032', 'MS14_D01_S05_L0033',
                                        'MS14_D01_S05_L0034', 'MS14_D01_S05_L0035'])
                index = lambda term: next(i for i, text in enumerate(rows) if term in text)
                self.assertLess(index('도토리'), index('누가 썼는지 모르겠어'))
                self.assertLess(index('누가 썼는지 모르겠어'), index('이 편지를 보낸 것도 엄마인지'))
                self.assertLess(index('이 편지를 보낸 것도 엄마인지'), index('할머니한테 물어보자'))
                self.assertEqual(sum('편지엔 하나도 없어' in text for text in rows), 1)
                self.assertEqual(self.state.room13, before)
        self.assertEqual(env['R13_V111']['evidence']['E01']['variants']['observed'],
                         '다람이를 데리고 와 줘. 여관 13호실에서 기다릴게.')


    def test_comparison_remembers_whether_granny_was_already_asked(self):
        env = self.load()
        env['r13_v111_set']('chorong_whereabouts_asked1', True)
        before = copy.deepcopy(self.state.room13)
        heard = ' '.join(self.texts(env, ['MS14_D01_S05_L0035']))
        self.assertIn('내일 아침', heard)
        self.assertNotIn('할머니한테 물어보자', heard)
        self.assertEqual(self.state.room13, before)
        env['r13_v111_set']('chorong_whereabouts_asked1', False)
        unheard = ' '.join(self.texts(env, ['MS14_D01_S05_L0035']))
        self.assertIn('할머니한테 물어보자', unheard)
        self.assertNotIn('내일 아침', unheard)


if __name__ == '__main__':
    unittest.main()
