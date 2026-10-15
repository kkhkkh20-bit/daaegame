"""0.18.29 dot effects: data file, frames and the two hook lines stay consistent."""
import json
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
META = json.loads((GAME / "assets/room13-dot-fx.json").read_text(encoding="utf-8"))


def size(path):
    with Image.open(GAME / path) as im:
        return im.size


class DotFxTest(unittest.TestCase):
    def test_fire_sheets_match_rect_and_frames(self):
        fire = META["inn_fire"]
        x, y, w, h = fire["rect"]
        self.assertEqual((x % 4, y % 4, w % 4, h % 4), (0, 0, 0, 0))
        layout = json.loads((GAME / "assets/room13-world-layout.json").read_text(encoding="utf-8"))["inn"]
        for period, item in fire["periods"].items():
            self.assertIn(period, layout["files"])
            bw, bh = size(layout["files"][period])
            self.assertLessEqual(x + w, bw)
            self.assertLessEqual(y + h, bh)
            self.assertEqual(size(item["sheet"]), (w * fire["frames"], h))
            self.assertEqual(len(item["light"]), fire["frames"])

    def test_plates_cover_their_backgrounds(self):
        self.assertEqual(size(META["inn_glow"]["file"]), (2048, 768))
        self.assertEqual(size(META["lamp_glow"]["square"]["file"]), (2048, 768))

    def test_snow_only_outdoors_in_the_evening(self):
        snow = META["snow"]
        self.assertEqual(set(snow["locations"]), {"square", "gate", "altar"})
        self.assertEqual(snow["periods"], ["evening"])
        self.assertEqual(size(snow["small"]), (4, 4))
        self.assertEqual(size(snow["big"]), (8, 8))

    def test_blink_pieces_sit_inside_the_fullbody_picture(self):
        daram = META["blink"]["people"]["daram"]
        # joy is drawn with closed eyes; it never blinks.
        self.assertEqual(set(daram), {"neutral", "flustered", "angry", "anxious", "surprise"})
        for emotion, spec in daram.items():
            fw, fh = size("assets/room13-fullbody-daram-%s.webp" % emotion)
            x, y, w, h = spec["rect"]
            self.assertTrue(0 <= x and 0 <= y and x + w <= fw and y + h <= fh, emotion)
            self.assertEqual(size(spec["half"]), (w, h))
            self.assertEqual(size(spec["closed"]), (w, h))

    def test_hooks_are_single_lines_not_override_layers(self):
        camera = (GAME / "room13_world_camera.rpy").read_text(encoding="utf-8")
        fullbody = (GAME / "room13_fullbody_dialogue.rpy").read_text(encoding="utf-8")
        fx = (GAME / "systems/room13_dot_fx.rpy").read_text(encoding="utf-8")
        self.assertIn("r13_dot_fx_scene(location,period,source,path,crop)", camera)
        self.assertIn("r13_blink_art(person,spec[\"emotion\"],spec[\"file\"])", fullbody)
        # Every effect respects the motion option and skipping.
        self.assertIn("persistent.room13_motion", fx)
        self.assertIn("renpy.is_skipping()", fx)


if __name__ == "__main__":
    unittest.main()
