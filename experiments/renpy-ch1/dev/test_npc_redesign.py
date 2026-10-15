"""2026-10-15 NPC redesigns: art-only replacement, originals preserved.

Real placement and dialogue framing run in Ren'Py:
dev/run_renpy_tests.sh redesign_world redesign_dialogue
"""
import hashlib, json, unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/npc-redesign-20261015"
REG = json.loads((ART / "redesign.json").read_text(encoding="utf-8"))
BACKUP = json.loads((ART / "original-entries.json").read_text(encoding="utf-8"))
CAST = json.loads((GAME / "assets/cast.json").read_text(encoding="utf-8"))
ACTING = json.loads((GAME / "assets/room13-pixel-acting.json").read_text(encoding="utf-8"))
PORTRAITS = json.loads((GAME / "assets/room13-portraits.json").read_text(encoding="utf-8"))
FULLBODY = json.loads((GAME / "assets/room13-fullbody-dialogue.json").read_text(encoding="utf-8"))["people"]
CONTENT = json.loads((GAME / "room13-content.json").read_text(encoding="utf-8"))


def files(entry):
    out = set()
    if isinstance(entry, dict):
        for k, v in entry.items():
            out |= {v} if k == "file" else files(v)
    elif isinstance(entry, list):
        for v in entry:
            out |= files(v)
    return out


class NpcRedesign(unittest.TestCase):
    def test_one_design_per_existing_npc(self):
        npcs = [d["npc"] for d in REG["designs"]]
        # 0.18.58 (owner, 07:39 PDT): only the two elders join the first eight; nobody else.
        self.assertEqual(sorted(npcs), sorted({"resident_yeoni", "resident_momo", "resident_librarian", "resident_nubi",
                                               "resident_seol", "resident_siluk", "resident_nero", "resident_bori",
                                               "resident_owlgp", "granny"}))
        self.assertEqual(len({d["sha256"] for d in REG["designs"]}), len(npcs))  # no picture used twice
        sources = {d["npc"]: d["sha256"] for d in REG["designs"]}
        self.assertEqual(sources["resident_owlgp"], "8ad9353427e3b32e74b886436d4fe8cde897a88e925a2f16c82370d9d2b56941")
        self.assertEqual(sources["granny"], "91a35c0e5ee83260fdf9fbfa98ca92ff0bc0333ec7ffe670a18cb25560c750d6")
        # Everyone else keeps the original game art.
        for npc, states in CAST.items():
            if npc not in sources:
                self.assertNotIn("redesign", json.dumps(states), npc)
        for d in REG["designs"]:
            src = (ART / d["source"]).read_bytes()
            self.assertEqual(hashlib.sha256(src).hexdigest(), d["sha256"], d["source"])
            # ID and name stay the story's own
            self.assertEqual(CONTENT["residents"][d["npc"]]["runtime_id"], d["npc"])
            self.assertEqual(FULLBODY[d["npc"]]["name_ko"], d["name_ko"])

    def test_every_art_entry_uses_the_new_file(self):
        for d in REG["designs"]:
            npc, new = d["npc"], "assets/room13-redesign-%s.webp" % d["npc"]
            for data in (CAST, ACTING, PORTRAITS):
                self.assertEqual(files(data[npc]), {new}, npc)
            self.assertEqual(files(FULLBODY[npc]), {new}, npc)
            # Old seated / living poses would show the old body: removed.
            self.assertEqual(set(ACTING[npc]), {"neutral", "thinking", "distressed", "expressive",
                                                "avatar_neutral", "avatar_thinking", "avatar_distressed", "avatar_expressive"})

    def test_geometry_fits_the_image_and_feet_touch_the_bottom(self):
        for d in REG["designs"]:
            npc = d["npc"]
            spec = ACTING[npc]["neutral"]
            with Image.open(GAME / spec["file"]) as im:
                self.assertEqual(im.mode, "RGBA")
                alpha = np.asarray(im)[..., 3]
                w, h = im.size
            x, y, cw, ch = spec["crop"]
            self.assertTrue(0 <= x and 0 <= y and x + cw <= w and y + ch <= h, npc)
            fx, fy = spec["foot"]
            self.assertTrue(0 < fx < cw and ch - 8 <= fy <= ch, npc)
            visible = np.where((alpha[y:y + ch, x:x + cw] >= 32).any(1))[0]
            self.assertEqual(visible.max() + 1, fy, npc)          # foot = lowest visible row
            self.assertLessEqual(visible.min(), 6, npc)            # nothing cut at the top
            # Transparent outside the figure (no background box).
            self.assertEqual(int(alpha[0, 0]) + int(alpha[0, -1]) + int(alpha[-1, 0]) + int(alpha[-1, -1]), 0)
            hx, hy, hw, hh = spec["head"]
            self.assertTrue(hx + hw <= cw and hy + hh <= ch and hh > 0, npc)
            ax, ay, aw, ah = ACTING[npc]["avatar_neutral"]["crop"]
            self.assertTrue(ax + aw <= w and ay + ah <= h, npc)

    def test_originals_are_backed_up_and_kept_on_disk(self):
        for d in REG["designs"]:
            saved = BACKUP["npcs"][d["npc"]]
            self.assertEqual(set(saved), {"cast", "acting", "portraits", "fullbody"})
            self.assertFalse(any("redesign" in json.dumps(v) for v in saved.values()))
            for f in files(saved):
                self.assertTrue((GAME / f).exists(), f)


if __name__ == "__main__":
    unittest.main()
