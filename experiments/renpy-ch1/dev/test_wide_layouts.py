"""World layout data (game/assets/room13-world-layout.json): pictures exist, crops sit
inside their pictures, scaling is uniform (never x only), and every rect/slot is
inside the world. Runtime clicks and staging: dev/run_renpy_tests.sh wide_*."""
import json
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
LAYOUT = json.loads((GAME / "assets/room13-world-layout.json").read_text())
DAYLIGHT = ("morning", "afternoon", "evening")


def pictures(spec):
    """(daylight, state or None, path) for every picture the layout can show."""
    if "state_files" in spec:
        for state, files in spec["state_files"].items():
            for daylight, path in files.items():
                yield daylight, state, path
    for daylight, path in spec.get("files", {}).items():
        yield daylight, None, path


class WideLayouts(unittest.TestCase):
    def test_pictures_and_uniform_scale(self):
        for location, spec in LAYOUT.items():
            width = int(spec["width"])
            for daylight, state, path in pictures(spec):
                with self.subTest(location=location, daylight=daylight, state=state):
                    file = GAME / path
                    self.assertTrue(file.exists(), path)
                    with Image.open(file) as im:
                        size = im.size
                    crop = spec.get("crops", {}).get(daylight, [0, 0, size[0], size[1]])
                    x, y, w, h = crop
                    self.assertTrue(x >= 0 and y >= 0 and x + w <= size[0] and y + h <= size[1], (crop, size))
                    # Uniform scale: crop aspect equals the world aspect (within one source pixel).
                    self.assertLess(abs(w * 720.0 / h - width), width / float(w) + 1e-6, (crop, width))

    def test_periods_have_pictures(self):
        for location, spec in LAYOUT.items():
            periods = spec.get("periods", DAYLIGHT)
            for daylight in periods:
                with self.subTest(location=location, daylight=daylight):
                    if "state_files" in spec:
                        for state, files in spec["state_files"].items():
                            self.assertIn(daylight, files, state)
                    else:
                        self.assertIn(daylight, spec["files"])

    def test_rects_and_slots_inside_world(self):
        for location, spec in LAYOUT.items():
            width = int(spec["width"])
            for key, (x, y, w, h) in spec.get("objects", {}).items():
                with self.subTest(location=location, key=key):
                    self.assertTrue(0 <= x and 0 <= y and x + w <= width and y + h <= 720 and w > 0 and h > 0)
            for slot in spec.get("slots", []) + [f + ["floor"] for f in spec.get("floors", [])]:
                with self.subTest(location=location, slot=slot):
                    cx, feet, height = slot[:3]
                    self.assertTrue(0 < cx < width and 0 < feet <= 720 and 0 < height < feet, slot)

    def test_scope(self):
        # 0.18.58: post wide in the morning only; guestroom stays the old room.
        self.assertEqual(LAYOUT["post"]["periods"], ["morning"])
        self.assertNotIn("guestroom", LAYOUT)
        # The post slot in front of the scarf was replaced (it hid the scarf).
        self.assertNotIn([675, 635, 205], [s[:3] for s in LAYOUT["post"]["slots"]])
        # 13호/hall: every state x daylight picture exists (no fallback to morning).
        for location in ("hall", "room13"):
            for state in ("before", "after"):
                self.assertEqual(sorted(LAYOUT[location]["state_files"][state]), sorted(DAYLIGHT))

if __name__ == "__main__":
    unittest.main()
