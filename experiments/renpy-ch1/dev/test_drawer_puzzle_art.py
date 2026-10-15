"""0.18.63 drawer puzzle art (ART_REQUEST_01822 section 1): sources match the handoff
MANIFEST, imported files are current, both papers share one rect, the ruler tip lands
on the groove. Clicks and layer switching: dev/run_renpy_tests.sh drawer_puzzle_art."""
import hashlib, json, subprocess, sys, unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "art/drawer-puzzle4-20261015"
LAYOUT = json.loads((ROOT / "game/room13-inspection-layout.json").read_text(encoding="utf-8"))


class DrawerPuzzleArt(unittest.TestCase):
    def test_sources_match_manifest(self):
        manifest = json.loads((ART / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["assets"]), 4)
        for item in manifest["assets"]:
            self.assertEqual(hashlib.sha256((ART / item["name"]).read_bytes()).hexdigest(), item["sha256"], item["name"])

    def test_import_is_current(self):
        r = subprocess.run([sys.executable, str(ROOT / "dev/import_drawer_puzzle.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_geometry(self):
        states = LAYOUT["drawer_states"]
        self.assertEqual(states["open"]["rect"], [0, 0, 1280, 720])
        self.assertEqual(states["paper"]["rect"], [435, 385, 305, 150])
        self.assertEqual(states["rubbing"]["rect"], states["paper"]["rect"])
        # Same stored size for both papers (one common canvas).
        sizes = {Image.open(ROOT / "game" / states[k]["file"]).size for k in ("paper", "rubbing")}
        self.assertEqual(sizes, {(610, 300)})
        x, y, w, h = states["held"]["rect"]
        self.assertEqual((w, h), (120, 120))
        tip = (x + 365 * 120 / 1254.0, y + 955 * 120 / 1254.0)
        gx, gy, gw, gh = LAYOUT["drawer"]["targets"]["divider"]
        self.assertAlmostEqual(tip[0], gx + gw / 2.0, delta=0.6)
        self.assertAlmostEqual(tip[1], gy + gh / 2.0, delta=0.6)
        # The paper sits on the tag target; click targets are unchanged.
        tx, ty, tw, th = LAYOUT["drawer"]["targets"]["tag"]
        px, py, pw, ph = states["paper"]["rect"]
        self.assertTrue(tx <= px and ty <= py and px + pw <= tx + tw and py + ph <= ty + th)
        with Image.open(ROOT / "game" / states["open"]["file"]) as im:
            self.assertEqual(im.size, (1672, 941))


if __name__ == "__main__":
    unittest.main()
