"""NPC redesigns (dev/apply_npc_redesign.py): art-only replacement, originals preserved.

Registries: art/npc-redesign-20261015/redesign.json (first 8, history) and
art/character-remodel-20261015/remodel.json (remodel 31 + kept 7; later wins).
Real placement and dialogue framing run in Ren'Py:
dev/run_renpy_tests.sh redesign_world redesign_dialogue redesign_poses
"""
import hashlib, json, sys, unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
sys.path.insert(0, str(ROOT / "dev"))
import apply_npc_redesign as tool  # noqa: E402

DESIGNS = tool.designs()
BY_NPC = {d["npc"]: (d, folder) for d, folder, _ in DESIGNS}
INDEX = json.loads((ROOT / "art/character-remodel-20261015/source/FINAL_CANDIDATE_INDEX.json").read_text(encoding="utf-8"))
BACKUP = json.loads(tool.BACKUP.read_text(encoding="utf-8"))
CAST = json.loads((GAME / "assets/cast.json").read_text(encoding="utf-8"))
ACTING = json.loads((GAME / "assets/room13-pixel-acting.json").read_text(encoding="utf-8"))
PORTRAITS = json.loads((GAME / "assets/room13-portraits.json").read_text(encoding="utf-8"))
FULLBODY = json.loads((GAME / "assets/room13-fullbody-dialogue.json").read_text(encoding="utf-8"))["people"]


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
    def test_exactly_the_index_new_31_and_kept_7(self):
        rows = {r["id"]: r for r in INDEX["rows"]}
        wanted = {k for k, r in rows.items() if r["category"] in ("new_remodel_candidate", "preserve_previous")}
        # nabi keeps her original picture (already in the game): no entry.
        # Excluded (momo, seol: being revised): the game keeps its current picture.
        self.assertEqual(tool.excluded(), {"resident_momo", "resident_seol"})
        self.assertEqual(set(BY_NPC), wanted - {"nabi"} - tool.excluded())
        for held in ("daram", "dad", "nabi"):
            self.assertNotIn("redesign", json.dumps(CAST[held]))
        for npc, (design, folder) in BY_NPC.items():
            self.assertEqual(design["sha256"], rows[npc]["sha256"], npc)  # the index file, no other candidate
            self.assertEqual(hashlib.sha256((folder / design["source"]).read_bytes()).hexdigest(), design["sha256"], npc)
        self.assertEqual(len({d["sha256"] for d, _ in BY_NPC.values()}), len(BY_NPC))  # no picture used twice

    def test_names_and_ids_are_the_game_ones(self):
        for npc, (design, _) in BY_NPC.items():
            saved = BACKUP["npcs"][npc]["fullbody"]["name_ko"]
            self.assertEqual(FULLBODY[npc]["name_ko"], saved, npc)

    def test_every_art_entry_uses_the_new_files(self):
        for npc, (design, _) in BY_NPC.items():
            pose_files = {"assets/room13-redesign-%s-%s.webp" % (npc, k) for k in design.get("poses", {})}
            new = {"assets/room13-redesign-%s.webp" % npc}
            self.assertEqual(files(CAST[npc]), new | pose_files, npc)
            self.assertEqual(files(ACTING[npc]), new | pose_files, npc)
            self.assertEqual(files(PORTRAITS[npc]), new, npc)
            self.assertEqual(files(FULLBODY[npc]), new, npc)  # dialogue never uses a field pose
            expected = {"neutral", "thinking", "distressed", "expressive",
                        "avatar_neutral", "avatar_thinking", "avatar_distressed", "avatar_expressive"} | set(design.get("poses", {}))
            self.assertEqual(set(ACTING[npc]), expected, npc)  # old design poses removed

    def test_investigation_poses_scale_by_head(self):
        poses = {npc: d["poses"] for npc, (d, _) in BY_NPC.items() if d.get("poses")}
        self.assertEqual(set(poses), {"resident_bori", "resident_nero", "resident_yeoni"})
        for npc, items in poses.items():
            for key, spec in items.items():
                entry = ACTING[npc][key]
                self.assertTrue(entry["scale_by_head"] and key.startswith("living_"), npc)
                self.assertGreater(entry["head"][3], 0)

    def test_geometry_fits_the_image_and_feet_touch_the_bottom(self):
        for npc in BY_NPC:
            for key, spec in ACTING[npc].items():
                if key.startswith("avatar_"):
                    continue
                with Image.open(GAME / spec["file"]) as im:
                    self.assertEqual(im.mode, "RGBA")
                    alpha = np.asarray(im)[..., 3]
                    w, h = im.size
                x, y, cw, ch = spec["crop"]
                self.assertTrue(0 <= x and 0 <= y and x + cw <= w and y + ch <= h, (npc, key))
                fx, fy = spec["foot"]
                self.assertTrue(0 < fx < cw and ch - 8 <= fy <= ch, (npc, key))
                visible = np.where((alpha[y:y + ch, x:x + cw] >= 32).any(1))[0]
                self.assertEqual(visible.max() + 1, fy, (npc, key))   # foot = lowest visible row
                self.assertLessEqual(visible.min(), 6, (npc, key))     # nothing cut at the top
                self.assertEqual(int(alpha[0, 0]) + int(alpha[0, -1]) + int(alpha[-1, 0]) + int(alpha[-1, -1]), 0)
                hx, hy, hw, hh = spec["head"]
                self.assertTrue(hx + hw <= cw and hy + hh <= ch and hh > 0, (npc, key))

    def test_originals_are_backed_up_and_kept_on_disk(self):
        for npc in BY_NPC:
            saved = BACKUP["npcs"][npc]
            self.assertEqual(set(saved), {"cast", "acting", "portraits", "fullbody"})
            self.assertFalse(any("redesign" in json.dumps(v) for v in saved.values()))
            for f in files(saved):
                self.assertTrue((GAME / f).exists(), f)


if __name__ == "__main__":
    unittest.main()
