"""0.19.0 role connection (dev/apply_role_connect.py): approved / confirmed designs in every art
channel, no picture of the old design left, rollback data present."""
import csv, hashlib, json, unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/role-connect-20261016"
REG = json.loads((ART / "registry.json").read_text(encoding="utf-8"))
BACKUP = json.loads((ART / "original-entries.json").read_text(encoding="utf-8"))["roles"]
A = lambda n: json.loads((GAME / "assets" / n).read_text(encoding="utf-8"))
CAST, ACTING, PORTRAITS = A("cast.json"), A("room13-pixel-acting.json"), A("room13-portraits.json")
FULLBODY, MEETING, DOTFX = A("room13-fullbody-dialogue.json")["people"], A("room13-meeting-seated.json"), A("room13-dot-fx.json")
MAP = json.loads((ROOT / "art/map-actions-20261015/registry.json").read_text(encoding="utf-8"))
CANON = {r["roleId"]: r for r in csv.DictReader((ROOT / "art/canonical48-rev45/canonical48.csv").open(encoding="utf-8-sig"))}
EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")


def files(entry):
    out = set()
    if isinstance(entry, dict):
        for k, v in entry.items():
            out |= {v} if k == "file" else files(v)
    elif isinstance(entry, list):
        for v in entry:
            out |= files(v)
    return out


class RoleConnect(unittest.TestCase):
    def test_sources_are_the_approved_bytes(self):
        approved = {}
        for name in ("approved-change.csv", "three-approved-changes.csv"):
            for r in csv.DictReader((ART / "sources/approved" / name).open(encoding="utf-8-sig")):
                approved[r["roleId"]] = r["sha256"]
        for rid, spec in REG["roles"].items():
            if spec["mode"] == "canon":
                self.assertEqual(spec["sha256"], CANON[rid]["sha256"], rid)
            elif spec["mode"] == "native_single":
                self.assertEqual(rid, "resident_kkwak")
                self.assertEqual(spec["sha256"], "dced0d974c10cc81fe0f72fdcbb884067ee54e3511e2cbf4f43d3f0b1674f2a9")
            elif spec["mode"] == "pixel_set":
                self.assertEqual(spec["dialogue"]["neutral"]["sha256"], approved[rid])
            else:
                self.assertEqual(spec["sha256"], approved[rid], rid)
            for s in ([spec] if "source" in spec else list(spec["dialogue"].values())):
                self.assertEqual(hashlib.sha256((ART / s["source"]).read_bytes()).hexdigest(), s["sha256"])
        # not part of this change: 너울·사자 선생님 (outfit decision pending), 네로 (grey cloak kept)
        self.assertFalse({"neoul", "resident_teacher", "resident_nero"} & set(REG["roles"]))

    def test_no_old_design_picture_left(self):
        live = {(e["person"], e["sha256"]) for e in MAP["poses"] if not (e.get("withdrawn") or e.get("hold"))}
        for rid, spec in REG["roles"].items():
            if spec["mode"] == "dialogue_neutral":
                continue
            new = {f for f in files([CAST[rid], ACTING[rid], PORTRAITS[rid], FULLBODY[rid]])}
            allowed = {f for f in new if f.startswith("assets/room13-role-%s" % rid)}
            for k, v in ACTING[rid].items():
                if v.get("map_action"):
                    self.assertIn((rid, v["source_sha256"]), live, (rid, k))
                    allowed.add(v["file"])
            self.assertEqual(new, allowed, rid)
            self.assertNotIn(rid, MEETING)                       # old seated picture gone
            self.assertNotIn(rid, DOTFX["blink"]["people"])      # old eye pieces gone
            self.assertEqual(set(FULLBODY[rid]["images"]), set(EMOTIONS))
            self.assertFalse(FULLBODY[rid].get("poses"))

    def test_pixel_pictures_are_exact(self):
        for rid, spec in REG["roles"].items():
            if spec["mode"] not in ("pixel_set", "pixel_single", "dialogue_neutral"):
                continue
            sources = spec["dialogue"] if spec["mode"] == "pixel_set" else {"neutral": spec}
            for e, s in sources.items():
                img = FULLBODY[rid]["images"][e]
                self.assertEqual(img["cell"], 2)
                shown = np.asarray(Image.open(GAME / img["file"]).convert("RGBA")).astype(int)
                src = np.asarray(Image.open(ART / s["source"]).convert("RGBA")).astype(int)
                self.assertEqual(shown.shape, src.shape)
                vis = src[..., 3] > 0
                self.assertTrue((shown[..., 3] == src[..., 3]).all(), (rid, e))
                self.assertTrue((shown[vis][:, :3] == src[vis][:, :3]).all(), (rid, e))
                self.assertEqual(img["crop"][0] % 2 + img["crop"][1] % 2 + img["crop"][2] % 2 + img["crop"][3] % 2, 0)

    def test_buri_v7_six_faces_and_actions(self):
        fb = FULLBODY["buri"]
        self.assertEqual(len({fb["images"][e]["file"] for e in EMOTIONS}), 6)
        self.assertEqual(fb["pixel"], {"u": 1.0, "cell": 2})
        for pose in ("action_1", "action_2", "event_toolbox"):
            self.assertTrue(ACTING["buri"][pose]["file"].startswith("assets/room13-action-buri-"), pose)
            self.assertIn("buri-v7", [e for e in MAP["poses"] if e["person"] == "buri" and e["pose"] == pose
                                      and not e.get("withdrawn")][0]["source"])
        self.assertIn("hand", ACTING["buri"]["action_1"])

    def test_guard_keeps_its_other_faces_and_poses(self):
        before = BACKUP["guard"]
        for e in EMOTIONS[1:]:
            self.assertEqual(FULLBODY["guard"]["images"][e], before["fullbody"]["images"][e])
        for key, value in before["acting"].items():
            if key != "neutral" and not key.startswith("avatar_"):
                self.assertEqual(ACTING["guard"][key], value)
        self.assertEqual(ACTING["guard"]["neutral"]["file"], FULLBODY["guard"]["images"]["neutral"]["file"])
        self.assertEqual(PORTRAITS["guard"]["neutral"]["file"], FULLBODY["guard"]["images"]["neutral"]["file"])
        self.assertTrue(FULLBODY["guard"]["images"]["neutral"]["file"].startswith("assets/room13-role-guard"))

    def test_new_residents_no_longer_borrow(self):
        src = (GAME / "systems/room13_new_cast.rpy").read_text(encoding="utf-8")
        self.assertIn("if _r13_nc_id in CAST:continue", src)
        for rid in ("resident_solbang", "resident_guldol", "resident_mulgyeol", "resident_dalgeurak",
                    "resident_jongjong", "resident_hyeoni", "resident_kalbaram"):
            self.assertIn(rid, CAST)
            self.assertIn(rid, FULLBODY)

    def test_backup_has_every_role(self):
        self.assertEqual(set(BACKUP), set(REG["roles"]))
        self.assertIsNotNone(BACKUP["buri"]["meeting"])
        self.assertIsNone(BACKUP["resident_mulgyeol"]["cast"])


if __name__ == "__main__":
    unittest.main()
