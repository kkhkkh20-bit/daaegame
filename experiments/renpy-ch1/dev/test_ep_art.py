"""0.18.89 episode art (dev/apply_ep_art.py): icons, pictures and scene keys exist and fit."""
import numpy as np
import json, re, unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
REG = json.loads((ROOT / "art/ep-art-20261016/registry.json").read_text(encoding="utf-8"))
ICONS = json.loads((GAME / "assets/room13-evidence-icons.json").read_text(encoding="utf-8"))
ART = (GAME / "systems/room13_ep_art.rpy").read_text(encoding="utf-8")


class EpArt(unittest.TestCase):
    def test_every_episode_icon_is_a_300px_transparent_picture(self):
        for key in REG["icons"]:
            spec = ICONS[key]
            with Image.open(GAME / spec["file"]) as im:
                self.assertEqual(im.size, (300, 300), key)
                self.assertEqual(im.mode, "RGBA", key)
            self.assertEqual(spec["crop"], [0, 0, 300, 300])

    def test_pictures_have_the_planned_size(self):
        for name, spec in REG["pictures"].items():
            with Image.open(GAME / "assets" / name) as im:
                if spec.get("size"):
                    self.assertEqual(list(im.size), spec["size"], name)

    def test_scene_keys_and_overlays_point_at_shipped_files(self):
        for name in set(re.findall(r'"(room13-[a-z0-9-]+\.webp)"', ART)):
            self.assertTrue((GAME / "assets" / name).exists(), name)
        used = set(re.findall(r'call r13_scene\("(ep_[a-z_]+)"', "".join(p.read_text(encoding="utf-8") for p in (GAME / "systems").glob("room13_ep*.rpy"))))
        keys = set(re.findall(r'"(ep_[a-z_]+)":', ART))
        self.assertTrue(used and used <= keys, used - keys)

    def test_held_items_are_not_shipped(self):
        # The U22 blank-nose frame stays in art/ only.
        self.assertFalse((GAME / "assets/room13-ep-U22-mother-portrait-blank-nose.webp").exists())
        # O46: the noose-like ropes were never shipped; 0.18.90 adds the redrawn short ropes
        # (manual extraction, dev/extract_o46_ropes.py) only inside their hand-drawn region.
        with Image.open(GAME / "assets/room13-ep-O46-mountain-ropes.webp") as im:
            alpha = np.asarray(im.getchannel("A"))
        with Image.open(ROOT / "art/ep-art-20261016/derived/ep-O46-mountain-ropes-cart.webp") as im:
            cart = np.asarray(im.getchannel("A"))
        outside = np.ones_like(alpha, bool)
        outside[70:240, 60:410] = False
        self.assertTrue(((alpha > 0) == (cart > 0))[outside].all())        # cart and the rest unchanged
        self.assertGreater(int((alpha[70:240, 60:410] > 0).sum()), 800)     # the four ropes are there


if __name__ == "__main__":
    unittest.main()
