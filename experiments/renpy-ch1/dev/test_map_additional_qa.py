"""A03/A05: stage-bound names, no knowledge/travel expansion, separate keyboard panning."""
import ast
import copy
import textwrap
import types
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


def helpers(state, allowed=("forest", "square"), touch=False):
    source = (GAME / "room13_navigation.rpy").read_text()
    start = source.index(" python:\n") + len(" python:\n")
    tree = ast.parse(textwrap.dedent(source[start:source.index("\nscreen ", start)]))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name in ("r13_map_label", "r13_map_input_hint")]
    ns = dict(store=types.SimpleNamespace(room13=state),
              R13_MAP_LABELS=dict(forest="깊은 숲", square="광장", greenhouse="폐온실"),
              r13_v111_active=lambda: bool(state.get("v111")),
              r13_places=lambda: list(allowed), r13_touch_ui=lambda: touch)
    exec(compile(ast.Module(body=functions, type_ignores=[]), "<map-helper>", "exec"), ns)
    return ns


class MapAdditionalQA(unittest.TestCase):
    def state(self, gate="go_box", **story):
        return dict(day=2, location="square", v111=dict(gate=gate, **story))

    def test_named_trip_then_inspect_note_post_and_later_visits(self):
        state = self.state()
        ns = helpers(state)
        before = copy.deepcopy(state)
        self.assertEqual(ns["r13_map_label"]("forest"), "깊은 숲 · 교환함")
        self.assertEqual(ns["r13_map_label"]("square"), "광장")
        self.assertEqual(state, before)
        for gate in ("box_inspect", "box_note", "envelope_show", "lamp_rope"):
            state["v111"]["gate"] = gate
            self.assertEqual(ns["r13_map_label"]("forest"), "깊은 숲", gate)
        state["v111"]["gate"] = "go_box"
        state["day"] = 3
        self.assertEqual(ns["r13_map_label"]("forest"), "깊은 숲")

    def test_travel_context_and_completed_box_are_distinguished(self):
        state = self.state("travel", scene="MS14_D02_S01", travel_to="forest", values={})
        ns = helpers(state)
        self.assertEqual(ns["r13_map_label"]("forest"), "깊은 숲 · 교환함")
        for key, value in (("scene", "MS14_D02_S02"), ("travel_to", "post")):
            previous = state["v111"][key]
            state["v111"][key] = value
            self.assertEqual(ns["r13_map_label"]("forest"), "깊은 숲")
            state["v111"][key] = previous
        state["v111"]["values"]["mother_box_checked_day2"] = True
        self.assertEqual(ns["r13_map_label"]("forest"), "깊은 숲")

    def test_restore_or_unavailable_destination_has_no_old_hint(self):
        state = self.state()
        self.assertEqual(helpers(state, allowed=("square",))["r13_map_label"]("forest"), "깊은 숲")
        state["v111"] = dict(gate="travel", travel_to="gate", scene="MS14_D02_S01")
        self.assertEqual(helpers(state)["r13_map_label"]("forest"), "깊은 숲")
        state.pop("v111")
        self.assertEqual(helpers(state)["r13_map_label"]("forest"), "깊은 숲")
        self.assertEqual(helpers(state)["r13_map_label"]("greenhouse"), "폐온실")

    def test_visible_input_hints_match_available_modes(self):
        for touch in (False, True):
            hint = helpers(self.state(), touch=touch)["r13_map_input_hint"]("village")
            self.assertIn("이동", hint)
            self.assertIn("손가락" if touch else "Shift+방향키", hint)
        self.assertNotIn("드래그", helpers(self.state())["r13_map_input_hint"]("mountain"))

    # 2026-10-27: shift+화살표 지도 이동 시험은 어디서도 쓰지 않던 r13_cartography 화면을 지우면서 뺐다.

if __name__ == "__main__":
    unittest.main()
