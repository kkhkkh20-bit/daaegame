"""B 마을 지도 QA가 실제 확대율과 뷰포트를 사용하고 선택을 대신하지 않는지 검증한다."""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest


GAME = Path(__file__).resolve().parents[1] / "game"


class Adjustment:
    def __init__(self, limit):
        self.range = limit
        self.value = 0

    def change(self, value):
        self.value = value


class MapRevealTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (GAME / "qa_tests/helpers.rpy").read_text()
        block = source.split("init 999 python:\n", 1)[1].split("\nlabel ", 1)[0]
        tree = ast.parse(textwrap.dedent(block))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "r13_qa_map_reveal")
        cls.code = compile(ast.Module(body=[node], type_ignores=[]), "<qa-map>", "exec")
        cls.layout = json.loads((GAME / "assets/map-village-b/layout.json").read_text())
        cls.places = {row["id"]: row for row in cls.layout["locations"]}
        map_source = (GAME / "room13_map_village_b.rpy").read_text()
        map_block = map_source.split("init 65 python:\n", 1)[1].split("\nscreen ", 1)[0]
        assignments = ast.parse(textwrap.dedent(map_block)).body
        cls.viewport = ast.literal_eval(next(n.value for n in assignments if isinstance(n, ast.Assign)
                                             and any(isinstance(t, ast.Name) and t.id == "R13_VILLAGE_B_VIEW" for t in n.targets)))

    def setUp(self):
        self.scope = dict(region="village", selected="gate", village_zoom=1.15, ready=True)
        self.refreshes = []
        self.view = None
        self.make_view(1.15)

        def get_widget(screen, widget):
            self.assertEqual((screen, widget), ("r13_map", "r13_map_view"))
            return self.view

        def get_screen(name):
            self.assertEqual(name, "r13_map")
            return SimpleNamespace(scope=self.scope)

        ns = dict(renpy=SimpleNamespace(get_widget=get_widget, get_screen=get_screen,
                                       restart_interaction=lambda: self.refreshes.append("refresh")),
                  R13_VILLAGE_B_VIEW=self.viewport, R13_VILLAGE_B_LAYOUT=self.layout,
                  R13_VILLAGE_B_PLACES=self.places)
        exec(self.code, ns)
        self.reveal = ns["r13_qa_map_reveal"]

    def make_view(self, zoom):
        self.scope["village_zoom"] = zoom
        vw, vh = self.viewport[2:]
        self.zoom = max(zoom, vw / 1642.0, vh / 958.0)
        self.view = SimpleNamespace(xadjustment=Adjustment(max(0, int(1642 * self.zoom) - vw)),
                                    yadjustment=Adjustment(max(0, int(958 * self.zoom) - vh)))

    def test_current_map_centers_and_clamps_without_selecting(self):
        before = copy.deepcopy(self.scope)
        for key, expected in (("market", (340.5, 140.3)), ("forest", (0, 0)), ("river", (752, 522.1))):
            self.reveal(key)
            self.assertAlmostEqual(self.view.xadjustment.value, expected[0])
            self.assertAlmostEqual(self.view.yadjustment.value, expected[1])
            self.assertEqual(self.scope, before)
        self.assertEqual(self.refreshes, ["refresh"] * 3)

    def test_all_delivered_name_centers_remain_inside_actual_viewport_at_each_zoom(self):
        for zoom in (0.1, 0.7, 1.15, 1.6):
            self.make_view(zoom)
            for key, row in self.places.items():
                with self.subTest(zoom=zoom, place=key):
                    self.reveal(key)
                    x = row["label_center"][0] * self.zoom - self.view.xadjustment.value
                    y = row["label_center"][1] * self.zoom - self.view.yadjustment.value
                    self.assertGreaterEqual(x, 0)
                    self.assertLessEqual(x, self.viewport[2])
                    self.assertGreaterEqual(y, 0)
                    self.assertLessEqual(y, self.viewport[3])

    def test_wrong_region_fails_without_changing_map(self):
        self.scope["region"] = "inn"
        with self.assertRaises(ValueError):
            self.reveal("inn")
        self.assertEqual((self.view.xadjustment.value, self.view.yadjustment.value), (0, 0))
        self.assertEqual(self.refreshes, [])

    def test_missing_widget_fails_before_adjustment(self):
        self.view = None
        with self.assertRaises(ValueError):
            self.reveal("market")
        self.assertEqual(self.refreshes, [])

    def test_non_canvas_place_is_not_silently_replaced_by_an_alias(self):
        with self.assertRaises(KeyError):
            self.reveal("v111_custody")
        self.assertEqual((self.view.xadjustment.value, self.view.yadjustment.value), (0, 0))
        self.assertEqual(self.scope["selected"], "gate")
        self.assertEqual(self.refreshes, [])


if __name__ == "__main__":
    unittest.main()
