"""0.18.5 inn lobby/hall v4 chips and the supplementary guide: data contract.

Real clicks, travel, guest-room gating and the guide modal (Escape) run in
Ren'Py: dev/run_renpy_tests.sh inn_v4_travel inn_v4_guestroom.
"""
import ast, json, textwrap, unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
NAV = json.loads((GAME / "assets/room13-inn-navigation-v4.json").read_text(encoding="utf-8"))


def connections():
    text = (GAME / "room13_navigation.rpy").read_text(encoding="utf-8")
    start = text.index("    R13_LOCAL_CONNECTIONS=")
    end = text.index("\n\n", start)
    ns = {}
    exec(textwrap.dedent(text[start:end]), ns)
    return {k: {d for d, t in v} for k, v in ns["R13_LOCAL_CONNECTIONS"].items()}


class InnNavigationV4(unittest.TestCase):
    def test_chips_cover_exactly_the_existing_links(self):
        links = connections()
        for location in ("inn", "hall"):
            targets = {c["to"] for c in NAV[location]["chips"]}
            self.assertEqual(targets, links[location], location)
        self.assertIn("outside", links["inn"])  # existing exit, no new ID

    def test_no_secret_place_and_sources_match_backgrounds(self):
        for location, art in (("inn", "room13-pixel-panorama-inn-morning.webp"), ("hall", "room13-pixel-hall-before-morning.webp")):
            self.assertNotIn("passage", {c["to"] for c in NAV[location]["chips"]})
            with Image.open(GAME / "assets" / art) as im:
                self.assertEqual(list(im.size), NAV[location]["source"])
            for chip in NAV[location]["chips"]:
                x0, y0, x1, y1 = chip["bounds"]
                self.assertTrue(0 <= x0 < x1 <= NAV[location]["source"][0] and 0 <= y0 < y1 <= NAV[location]["source"][1])

    def test_guide_labels_are_known_places_only(self):
        guide = json.loads((GAME / "assets/room13-inn-guide.json").read_text(encoding="utf-8"))
        allowed = {"title", "floor", "reception", "entrance", "inn", "dining", "kitchen", "hall", "room13", "guestroom"}
        self.assertEqual({l["locationId"] for l in guide["labels"]} - allowed, set())
        self.assertNotIn("passage", json.dumps(guide["labels"]))
        with Image.open(GAME / guide["base"]) as im:
            self.assertEqual(im.size, (guide["width"], guide["height"]))
        hub = (GAME / "room13_screens.rpy").read_text(encoding="utf-8")
        self.assertIn('Show("r13_inn_guide")', hub[hub.index('textbutton "안내도":'):][:400])

if __name__ == "__main__":
    unittest.main()
