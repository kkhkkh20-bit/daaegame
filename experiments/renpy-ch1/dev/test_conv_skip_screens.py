"""「건너뛰기」가 고르는 화면에서 멈추는지(2026-10-30 눈가림 플레이: 한 줄씩만 넘어갔다).

건너뛰기는 누른 뒤 플레이어가 고르는 화면이 뜰 때까지 대사 묶음을 넘긴다(systems/room13_conv_skip_run.rpy).
고르는 화면 목록에 빠진 call screen 이 있으면 그 화면을 지난 뒤의 대사까지 넘겨 버린다. 새 화면을 부르면 목록에도 넣는다.
"""
import re
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / 'game'


class ConvSkipScreens(unittest.TestCase):
    def test_every_called_screen_stops_skip(self):
        src = (GAME / 'systems/room13_conv_skip_run.rpy').read_text()
        m = re.search(r'R13_CONV_SKIP_STOP_SCREENS=\((.*?)\)\n', src, re.S)
        self.assertIsNotNone(m)
        listed = set(re.findall(r'"([a-z0-9_]+)"', m.group(1)))
        called = set()
        for f in GAME.rglob('*.rpy'):
            if 'qa_tests' in f.parts:
                continue
            text = f.read_text()
            called.update(re.findall(r'^\s*call screen ([a-z0-9_]+)', text, re.M))
            called.update(re.findall(r'renpy\.call_screen\(["\']([a-z0-9_]+)', text))
        missing = sorted(called - listed - {'save'})
        self.assertEqual(missing, [], '건너뛰기 멈춤 목록에 없는 call screen')


if __name__ == '__main__':
    unittest.main()
