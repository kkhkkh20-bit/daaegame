"""지도 시험의 화면 이동이 선택 상태를 대신 바꾸지 않는지 확인한다."""
import ast
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest


class MapRevealTest(unittest.TestCase):
    def test_reveal_centers_and_clamps_without_selecting(self):
        source = (Path(__file__).resolve().parents[1] / 'game/qa_tests/helpers.rpy').read_text()
        block = source.split('init 999 python:\n', 1)[1].split('\nlabel ', 1)[0]
        tree = ast.parse(textwrap.dedent(block))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'r13_qa_map_reveal')
        class Adjustment:
            def __init__(self, limit):
                self.range, self.value = limit, 0
            def change(self, value):
                self.value = value
        view = SimpleNamespace(xadjustment=Adjustment(800), yadjustment=Adjustment(600))
        points = {'center': (1000, 700), 'top': (10, 20), 'bottom': (2400, 1600)}
        calls = []
        def get_widget(screen, widget):
            self.assertEqual((screen, widget), ('r13_map', 'r13_map_view'))
            return view
        ns = dict(renpy=SimpleNamespace(get_widget=get_widget, restart_interaction=lambda: calls.append('refresh')),
                  r13_cart_label_point=points.__getitem__)
        exec(compile(ast.Module(body=[node], type_ignores=[]), '<qa-map>', 'exec'), ns)
        for key, expected in [('center', (376, 426)), ('top', (0, 0)), ('bottom', (800, 600))]:
            ns['r13_qa_map_reveal'](key)
            self.assertEqual((view.xadjustment.value, view.yadjustment.value), expected)
        self.assertEqual(calls, ['refresh'] * 3)


if __name__ == '__main__':
    unittest.main()
