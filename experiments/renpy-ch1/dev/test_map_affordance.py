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
        self.assertEqual(self.source.count('action [SetScreenVariable("selected",key),SetScreenVariable("map_notice",None)]'), 2)
        self.assertEqual(self.source.count('hovered (None if r13_touch_ui() else SetScreenVariable("map_hover",key))'), 2)
        self.assertIn("focus_mask r13_cart_layer(region,key)", self.source)
        self.assertNotIn("Return(", self.source)
        self.assertNotIn("r13_tick(", self.source)

    def test_touch_selection_does_not_restart_for_hover(self):
        self.assertEqual(self.source.count('hovered (None if r13_touch_ui() else SetScreenVariable("map_hover",key))'),2)
        self.assertEqual(self.source.count('unhovered (None if r13_touch_ui() else SetScreenVariable("map_hover",None))'),2)
        self.assertIn('outlined_focus=key==selected or key==map_hover',self.source)
        self.assertIn('if outlined_focus and r13_cart_pops(region,key):',self.source)

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

    def test_closed_public_places_explain_without_unlocking_or_secret_aliases(self):
        source = (GAME / "room13_navigation.rpy").read_text()
        start = source.index(" python:\n") + len(" python:\n")
        tree = ast.parse(textwrap.dedent(source[start:source.index("\nscreen ", start)]))
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name == "r13_map_locked_nodes"]
        state = {"location": "gate", "day": 1}
        ns = {"store": types.SimpleNamespace(room13=state),
              "R13_MAP_NODES": {"village": dict(gate=(0,0), workshop=(1,1), school=(2,2), fire=(2,2), secret=(3,3)),
                                "mountain": dict(forest=(0,0), facility=(1,1), greenhouse=(2,2), altar=(3,3))},
              "R13_V111_MAP_ALIASES": {"fire": "school"},
              "r13_map_nodes": lambda region: [("gate",(0,0)),("fire",(2,2))] if region=="village" else [("forest",(0,0))],
              "r13_map_discovered": lambda key: key != "secret"}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "<map>", "exec"), ns)
        self.assertEqual(ns["r13_map_locked_nodes"]("village"), [("workshop",(1,1))])
        self.assertEqual(ns["r13_map_locked_nodes"]("mountain"), [("facility",(1,1))])
        self.assertEqual(ns["r13_map_locked_nodes"]("inn"), [])
        self.assertEqual(state, {"location": "gate", "day": 1})
        locked = self.source.split("for key,point in r13_map_locked_nodes(region):",1)[1].split("for key,point in r13_map_nodes(region):",1)[0]
        self.assertIn('SetScreenVariable("map_notice",', locked)
        self.assertNotIn('SetScreenVariable("selected",', locked)
        self.assertNotIn('Return(', locked)

    def test_footer_row_centers_both_responsive_heights(self):
        source=(GAME/'room13_map_village_b.rpy').read_text()
        self.assertIn('by-((88 if r13_touch_ui() else 44)-bh)//2',source)
        for height in (44,88):
            top=643-(height-40)//2
            self.assertEqual(top+height/2,663)
            self.assertLessEqual(top+height,708)

    def test_mobile_map_controls_meet_css_target(self):
        source = (GAME / "room13_navigation.rpy").read_text()
        start = source.index("    def r13_map_control_height():")
        end = source.index("    def r13_map_region", start)
        for touch,base,expected in ((False,64,64),(False,80,80),(True,80,88),(True,96,96)):
            ns={"r13_touch_ui":lambda:touch,"r13_control_height":lambda:base}
            exec(textwrap.dedent(source[start:end]),ns)
            self.assertEqual(ns["r13_map_control_height"](),expected)
            if touch:
                for height in (390,360):self.assertGreaterEqual(expected*height/720,44)

    def test_tabs_and_actions_share_centered_row(self):
        source=(GAME/'room13_map_village_b.rpy').read_text()
        footer=source.split('screen r13_map_diary_footer(',1)[1]
        self.assertIn('use r13_village_b_control("이곳으로 이동",(704,643,184,40)',footer)
        self.assertIn('use r13_village_b_control("현장으로",(902,643,142,40)',footer)
        self.assertIn('chosen=key==region',footer)
        nav=(GAME/'room13_navigation.rpy').read_text()
        self.assertIn('use r13_map_diary_footer(region,selected,ready,local_guide,close_action)',nav)
        self.assertIn('use r13_map_diary_footer("village",selected,ready,local_guide,close_action)',source)

    def test_travel_and_local_guide_gates_remain(self):
        source=(GAME/'room13_map_village_b.rpy').read_text().split('screen r13_map_diary_footer(',1)[1]
        self.assertIn('selected!=room13["location"]',source)
        self.assertIn('selected in dict(r13_local_connections()) if local_guide else selected in r13_places()',source)
        self.assertIn('[Hide("r13_inn_guide"),Return(("travel",selected))] if local_guide else Return(selected)',source)
        self.assertIn('enabled=ready and can_travel',source)
        self.assertIn('if not local_guide:',source)

    def test_geometry_and_discovery_layer_unchanged(self):
        self.assertIn("if r13_cart_cover_visible(secret):", self.source)
        self.assertIn("xpos (ox+lx) ypos (oy+ly)", self.source)
        self.assertIn('area (ox+lx,oy+ly,lw,lh) padding (0,0)', self.source)


if __name__ == "__main__":
    unittest.main()
