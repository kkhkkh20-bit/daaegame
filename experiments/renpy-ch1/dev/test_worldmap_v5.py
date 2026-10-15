"""Village map v5 (from closed PR #8, ported to 0.18.5): source-level invariants.

Actual mouse/keyboard input and travel are checked in the browser by
dev/qa_worldmap.py and in Ren'Py by dev/run_renpy_tests.sh worldmap_travel.
"""
import ast, copy, hashlib, json, textwrap, types, unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
DESIGN = ROOT.parents[1] / "design/maps/20261014"
DATA = json.loads((GAME / "room13-worldmap-v5.json").read_text(encoding="utf-8"))
SCALE = 860 / 1672


def extract(ns, file, names):
    text = (GAME / file).read_text(encoding="utf-8")
    start = text.index(" python:\n") + len(" python:\n")
    lines = []
    for line in text[start:].splitlines():
        if line and not line.startswith((" ", "#")):
            break
        lines.append(line)
    tree = ast.parse(textwrap.dedent("\n".join(lines)))
    chosen = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names
              or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
    exec(compile(ast.Module(body=chosen, type_ignores=[]), file, "exec"), ns)


def namespace():
    ns = {"store": types.SimpleNamespace(room13={})}
    extract(ns, "room13_rules.rpy", {"r13_places"})
    ns["r13_has"] = lambda f: f in ns["store"].room13["flags"] or f in ns["store"].room13["evidence"]
    ns["_r13_route_places"] = ns["r13_places"]
    extract(ns, "room13_route_knowledge.rpy", {"r13_places", "r13_secret_route_available"})
    extract(ns, "room13_navigation.rpy", {"R13_MAP_NODES", "R13_LOCAL_CONNECTIONS", "r13_map_nodes",
        "r13_map_discovered", "r13_map_selection", "r13_local_connections", "r13_local_destination"})
    return ns


class WorldmapV5(unittest.TestCase):
    def test_destinations_are_the_existing_eight_village_places(self):
        ns = namespace()
        dest = {k for k, v in DATA["layers"].items() if v["node"]}
        self.assertEqual(dest, set(ns["R13_MAP_NODES"]["village"]))
        self.assertEqual(len(dest), 8)
        self.assertEqual(len(DATA["layers"]), 22)
        # Shrine, old quarry and scenery houses are drawn but are not places.
        for scenery in ("shrine", "quarry_home", "quarry_shed"):
            self.assertIsNone(DATA["layers"][scenery]["node"])

    def test_original_art_and_web_copy(self):
        source = DESIGN / "worldmap-winter-shrine-old-quarry-v5.png"
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), DATA["sha256"])
        with Image.open(GAME / "assets/room13-worldmap-v5.webp") as im:
            self.assertEqual(list(im.size), list(DATA["size"]))
        for key, spec in DATA["layers"].items():
            if spec["node"]:
                x, y, w, h = spec["bounds"]
                for suffix in ("", "-outline"):
                    with Image.open(GAME / ("assets/room13-worldmap-v5-%s%s.webp" % (key, suffix))) as im:
                        self.assertEqual(im.size, (w, h), key)
            else:
                self.assertFalse((GAME / ("assets/room13-worldmap-v5-%s.webp" % key)).exists(), key)
            self.assertGreater(len(spec["polygon"]), 4)
            self.assertTrue(all(0 <= x < 1672 and 0 <= y < 941 for x, y in spec["polygon"]))

    def test_labels_inside_map_and_not_overlapping(self):
        boxes = []
        for key, spec in DATA["layers"].items():
            if not spec["node"]:
                continue
            x, y = spec["label"]
            x, y = round(x * SCALE), round(y * SCALE)
            boxes.append((key, x - 57, y - 18, x + 57, y + 18))
        for i, (k, a, b, c, d) in enumerate(boxes):
            self.assertTrue(0 <= a < c <= 860 and 0 <= b < d <= 484, k)
            for j, e, f, g, h in boxes[i + 1:]:
                self.assertTrue(c <= e or g <= a or d <= f or h <= b, (k, j))

    def test_eligibility_and_hidden_places(self):
        ns = namespace()
        count = 0
        for day in (1, 4, 8, 14):
            for lodging in (False, True):
                for discovered in (False, True):
                    for opened in (False, True):
                        for case in ("pending", "occurred"):
                            for current in ("gate", "passage", "greenhouse", "altar"):
                                state = dict(day=day, location=current, flags=["lodging"] if lodging else [],
                                             evidence=[], case_state=case, passage_open=opened,
                                             secret_route_unlocked=discovered)
                                ns["store"].room13 = state
                                before = copy.deepcopy(state)
                                allowed = set(ns["r13_places"]())
                                self.assertEqual("guestroom" in allowed, lodging and case == "occurred")
                                for region in ns["R13_MAP_NODES"]:
                                    visible = {k for k, p in ns["r13_map_nodes"](region)}
                                    self.assertEqual("passage" in visible, region == "inn" and discovered and opened)
                                    self.assertNotIn("greenhouse", visible)
                                    self.assertNotIn("altar", visible)
                                    for stale in ("passage", "greenhouse", "altar", "invalid", None):
                                        selected = ns["r13_map_selection"](region, stale)
                                        self.assertTrue(selected in visible or selected is None)
                                self.assertEqual(before, state)
                                count += 1
        self.assertEqual(count, 256)


if __name__ == "__main__":
    unittest.main()
