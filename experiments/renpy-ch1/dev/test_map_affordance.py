"""Persistent travel outlines; native input/visual QA is still required."""
import ast
import textwrap
import types
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / "game"


class MapAffordance(unittest.TestCase):
    def setUp(self):
        self.source = (GAME / "room13_worldmap_v5.rpy").read_text()

    def test_outline_uses_authoritative_eligibility(self):
        self.assertIn("for key,point in r13_map_nodes(region):", self.source)
        self.assertIn("if key in r13_places():", self.source)
        self.assertIn("r13_cart_layer(region,key,outline=True)", self.source)

    def test_outline_persists_without_hover(self):
        start = self.source.index("if key in r13_places():")
        end = self.source.index("        button:", start)
        block = self.source[start:end]
        self.assertNotIn("if key==selected", block)
        self.assertIn("outlined_focus=key==selected or key==map_hover", block)
        self.assertIn('alpha=(1.0 if outlined_focus else .85)', block)
        self.assertIn('TintMatrix("#694425" if outlined_focus else "#a18b6c")', block)

    def test_selection_only_and_existing_hit_targets(self):
        self.assertEqual(self.source.count('action SetScreenVariable("selected",key)'), 2)
        self.assertEqual(self.source.count('hovered SetScreenVariable("map_hover",key)'), 2)
        self.assertIn("focus_mask r13_cart_layer(region,key)", self.source)
        self.assertNotIn("Return(", self.source)
        self.assertNotIn("r13_tick(", self.source)

    def test_discovery_and_unavailable_current_location(self):
        source = (GAME / "room13_navigation.rpy").read_text()
        start = source.index(" python:\n") + len(" python:\n")
        end = source.index("\nscreen ", start)
        tree = ast.parse(textwrap.dedent(source[start:end]))
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name == "r13_map_nodes"]
        state = {"location": "closed"}
        ns = {"store": types.SimpleNamespace(room13=state),
              "R13_MAP_NODES": {"village": dict(open=(1, 1), closed=(2, 2), secret=(3, 3))},
              "r13_places": lambda: ["open", "secret"],
              "r13_map_discovered": lambda key: key != "secret"}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "<map>", "exec"), ns)
        visible = [k for k, _ in ns["r13_map_nodes"]("village")]
        outlined = [k for k in visible if k in ns["r13_places"]()]
        self.assertEqual(visible, ["open", "closed"])
        self.assertEqual(outlined, ["open"])
        self.assertEqual(state, {"location": "closed"})

    def test_footer_row_centers_both_responsive_heights(self):
        source = (GAME / "room13_navigation.rpy").read_text()
        expression = next(line.split("=", 1)[1] for line in source.splitlines()
                          if "$ map_controls_y=" in line)
        for height, expected_y in ((64, 625), (80, 617)):
            y = eval(expression, {"r13_control_height": lambda: height})
            self.assertEqual(y, expected_y)
            self.assertEqual(y - 602, 712 - (y + height))
            self.assertGreaterEqual(720 - (y + height), 16)
            self.assertLess(y, 704 - height)

    def test_tabs_and_actions_share_centered_row(self):
        source = (GAME / "room13_navigation.rpy").read_text()
        self.assertIn('xpos 366 ypos map_controls_y spacing 8', source)
        for column in (3, 4):
            self.assertIn('area (r13_control_x(%d)-24,map_controls_y,R13_CONTROL["width"],r13_control_height())' % column, source)
        self.assertIn('text_xalign .5 text_yalign .5', source)
        self.assertIn('use r13_control("이곳으로 이동","map",', source)
        self.assertIn('use r13_control("현장으로","dialogue",close_action,enabled=ready)', source)

    def test_travel_and_local_guide_gates_remain(self):
        source = (GAME / "room13_navigation.rpy").read_text()
        self.assertIn('can_travel=selected!=room13["location"] and (selected in dict(r13_local_connections()) if local_guide else selected in r13_places())', source)
        self.assertIn('[Hide("r13_inn_guide"),Return(("travel",selected))] if local_guide else Return(selected),enabled=ready and can_travel,primary=True)', source)
        self.assertIn('if not local_guide:', source)

    def test_geometry_and_discovery_layer_unchanged(self):
        self.assertIn("if r13_cart_cover_visible(secret):", self.source)
        self.assertIn("xpos (ox+lx) ypos (oy+ly)", self.source)
        self.assertIn('area (ox+lx,oy+ly,lw,lh) padding (0,0)', self.source)


if __name__ == "__main__":
    unittest.main()
