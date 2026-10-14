"""Camera coordinate invariants for authored panorama widths."""
import copy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest


class WorldCamera(unittest.TestCase):
    def setUp(self):
        source = (Path(__file__).resolve().parents[1] / "game/room13_world_camera.rpy").read_text()
        code = source.split("init 58 python:\n", 1)[1].split("\ninit 62 python:", 1)[0]
        self.store = SimpleNamespace(room13={"location": "inn", "day": 3, "period": 1}, r13_world_cameras={})
        self.ns = {"store": self.store, "json": json, "r13_hashlib": hashlib,
                   "renpy": SimpleNamespace(loadable=lambda _: False, retain_after_load=lambda: None)}
        exec(textwrap.dedent(code), self.ns)
        self.ns["R13_WORLD_LAYOUTS"] = {"inn": {"width": 1920, "initial_x": 640},
                                        "school": {"width": 1800, "initial_x": 0}}

    def test_initial_world_and_screen_coordinate(self):
        self.assertEqual(self.ns["r13_world_offset"](), 640)
        self.assertEqual(self.ns["r13_world_to_screen"]((1540, 430)), (900, 430))
        self.assertEqual(self.ns["r13_world_to_screen"]((100, 430)), (-540, 430))

    def test_camera_clamps_and_preserves_pixel_grid(self):
        callback = self.ns["R13WorldCameraChanged"]("school")
        callback(157.3)
        self.assertEqual(self.ns["r13_world_offset"]("school"), 158)
        callback(99999)
        self.assertEqual(self.ns["r13_world_offset"]("school"), 520)
        callback(-50)
        self.assertEqual(self.ns["r13_world_offset"]("school"), 0)

    def test_location_cameras_do_not_change_story_or_other_locations(self):
        before = copy.deepcopy(self.store.room13)
        self.ns["R13WorldCameraChanged"]("school")(400)
        self.assertEqual(self.ns["r13_world_offset"]("inn"), 640)
        self.assertEqual(self.store.room13, before)
        self.assertEqual(self.ns["r13_world_offset"]("dining"), 0)

    def test_saved_old_offset_clamps_after_layout_change(self):
        self.store.r13_world_cameras["school"] = 1280
        self.assertEqual(self.ns["r13_world_offset"]("school"), 520)


if __name__ == "__main__":
    unittest.main()
