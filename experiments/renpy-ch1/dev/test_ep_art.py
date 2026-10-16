"""0.18.89 episode art (dev/apply_ep_art.py): icons, pictures and scene keys exist and fit."""
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
        # O46 ropes (noose-like loops) and the U22 blank-nose frame stay in art/ only.
        self.assertFalse((GAME / "assets/room13-ep-U22-mother-portrait-blank-nose.webp").exists())
        with Image.open(GAME / "assets/room13-ep-O46-mountain-ropes.webp") as im:
            alpha = im.getchannel("A")
            # left-top tree area (the ropes) is fully transparent; only the cart remains
            self.assertEqual(alpha.crop((0, 0, 400, 380)).getextrema()[1], 0)


if __name__ == "__main__":
    unittest.main()
