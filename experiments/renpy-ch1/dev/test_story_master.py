"""이야기 총정리 자동 부분(dev/story_master.py)이 오류 없이, 같은 결과로, 주요 회의·결말을 담아 만들어지는지."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('story_master', ROOT / 'dev/story_master.py')
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


class StoryMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = sm.build()
        cls.fails = list(sm.FAIL)

    def test_same_result_every_run(self):
        self.assertEqual(sm.build(), self.text)

    def test_every_meeting_has_a_section_with_its_chances(self):
        for name, key, tries in (('입구 회의', 'gate', 3), ('등 회의', 'lamp', 7), ('초소 회의', 'gate_post', 3),
                                 ('불 회의', 'fire', 4), ('13호실 회의', 'room13', 7), ('기록 회의', 'records', 4),
                                 ('가설 회의', 'hypothesis', 13), ('수프 회의', 'soup', 5), ('담요 회의', 'blanket', 4),
                                 ('피코 회의', 'piko', 4), ('제단 회의', 'altar', 6)):
            self.assertIn('### %s `%s`' % (name, key), self.text)
            self.assertRegex(self.text, r'### %s `%s` · [^\n]* · 기회 %d\n' % (name, key, tries))

    def test_endings_and_judges_are_listed(self):
        for title in ('남겨진 이름', '얼어붙은 마을', '함께 떠난 가족', '남은 사람들', '상처 입은 귀환', '마을의 아침', '새로운 아침'):
            self.assertIn(title, self.text)
        for fn in ('def r13_nw_ending14', 'def r13_nw_true_ending_ready', 'def r13_nw_dead'):
            self.assertIn(fn, self.text)

    def test_days_and_key_values(self):
        for d in range(1, 15):
            self.assertIn('### %d일' % d, self.text)
        for piece in ('`MS14_D07_S04`', 'fate_owl', '`hypothesis`', 'menu:hyp0', 'menu:trial_knife', '`R13_NW_WHEN`'):
            self.assertIn(piece, self.text)

    def test_failures_are_few_and_written_down(self):
        # 못 읽은 곳은 숨기지 않고 적는다. 갑자기 늘면 코드 꼴이 바뀐 것이니 도구를 손본다.
        self.assertLess(len(set(self.fails)), 10)
        self.assertIn('자동 추출 실패: %d곳' % len(set(self.fails)), self.text)


if __name__ == '__main__':
    unittest.main()
