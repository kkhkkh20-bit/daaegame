"""부분 정답의 일반 알림은 정답 조합을 먼저 설명하지 않는다."""
import ast
import copy
from pathlib import Path
import textwrap
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RetryHintPrivacy(unittest.TestCase):
    def test_partial_submission_preserves_progress_without_revealing_note(self):
        source = (ROOT/'game/room13_v111_newworld_rules.rpy').read_text()
        block = source.split('    def r13_nw_retry(', 1)[1].split('\n    #', 1)[0]
        function = ast.parse(textwrap.dedent('    def r13_nw_retry('+block))
        for kept in (False, True):
            with self.subTest(kept=kept):
                values = {'tries:room13': 1}
                args = {'v111:상처': ['V111:E08_CHILD_ACCOUNT']} if kept else {}
                before = copy.deepcopy(args)
                messages, queued = [], []
                env = dict(
                    store=types.SimpleNamespace(room13={'arguments': args},v111_claim='v111:상처',v111_last_presented=['V111:E08_CHILD_ACCOUNT']),
                    r13_v111_value=values.get, r13_v111_set=values.__setitem__,
                    r13_nw_tries_max=lambda meeting: 7, r13_nw_half=lambda correct: True,
                    r13_nw_wrong_queue=lambda *item: queued.append(item),
                    renpy=types.SimpleNamespace(notify=messages.append))
                exec(compile(function,'retry_hint','exec'),env)
                result=env['r13_nw_retry']('room13',['E08_CHILD_ACCOUNT','E08_TOOL'],'아이의 말과 촛대 조각을 함께 놓아야 한다.')
                self.assertTrue(result)
                self.assertEqual(values['tries:room13'],2)
                self.assertEqual(args,before)
                self.assertEqual(queued,[('room13',False)])
                self.assertEqual(messages,['기회 1회 사용 · 남은 기회 5번. '+('맞는 근거는 남겨 두었다.' if kept else '맞지 않는다.')])

if __name__ == '__main__': unittest.main()
