# 근접 다람이는 본편에서 승인한 원본을 같은 크기로 보여 준다.
import hashlib
import json
import unittest
from pathlib import Path

from v2data import LAYOUT, GAME


class ApprovedPortrait(unittest.TestCase):
    def test_daram_expressions_preserve_approved_source_and_display_size(self):
        old = Path(GAME).parents[1] / "renpy-ch1/game"
        table = json.loads((old / "assets/room13-closeup-smooth.json").read_text())
        profile = LAYOUT["figure"]["portraits"]["daram"]
        for face in ("neutral", "joy", "angry", "anxious", "flustered", "surprise_talk"):
            with self.subTest(face=face):
                approved = table["assets/dialogue-dot-v2/daram/760/%s.webp" % face]
                runtime = Path(GAME) / "assets" / profile["file"].format(face=face)
                self.assertEqual(runtime.relative_to(GAME).as_posix(), approved["master"])
                self.assertEqual(profile["size"], approved["dot"])
                self.assertEqual(hashlib.sha256(runtime.read_bytes()).digest(),
                                 hashlib.sha256((old / approved["master"]).read_bytes()).digest())


if __name__ == "__main__":
    unittest.main()
