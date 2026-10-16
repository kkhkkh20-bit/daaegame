"""TEST BRANCH ONLY: board revision13 appearance test (dev/apply_rev13_test.py).

Checks the 31 byte-exact sources, what each person got (incoming / selected / unchanged),
that the old-species poses are gone only for incoming mappings, that kept poses are the
original entries, that everyone else is untouched, and that the rollback copy exists.
"""
import hashlib, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/rev13-test-20261016"
REG = json.loads((ART / "rev13.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ART / "manifest.json").read_text(encoding="utf-8"))
BACKUP = json.loads((ART / "original-entries.json").read_text(encoding="utf-8"))
load = lambda p: json.loads(p.read_text(encoding="utf-8"))
CAST = load(GAME / "assets/cast.json")
ACTING = load(GAME / "assets/room13-pixel-acting.json")
FULLBODY = load(GAME / "assets/room13-fullbody-dialogue.json")["people"]
SEATED = load(GAME / "assets/room13-meeting-seated.json")
GALLERY = load(GAME / "assets/room13-rev13-gallery.json")
BODY = {"neutral", "thinking", "distressed", "expressive"}


class Rev13Test(unittest.TestCase):
    def test_sources_byte_exact_and_counts(self):
        self.assertEqual(MANIFEST["revision"], 13)
        self.assertEqual(len(REG["designs"]), 31)
        for d in REG["designs"]:
            self.assertEqual(hashlib.sha256((ART / d["source"]).read_bytes()).hexdigest(), d["sha256"], d["source"])
        modes = [d["apply"] for d in REG["designs"]]
        self.assertEqual((modes.count("incoming"), modes.count("selected"), modes.count("life_action_only"), modes.count("gallery_only")), (11, 16, 1, 3))
        incoming = {d["npc"] for d in REG["designs"] if d["apply"] == "incoming"}
        self.assertEqual(incoming, {e["gameId"] for e in MANIFEST["existing"] if e["decision"] == "incoming_mapping"})

    def test_applied_people(self):
        for d in REG["designs"]:
            npc, mode = d.get("npc"), d["apply"]
            if mode not in ("incoming", "selected"):
                continue
            new = "assets/room13-rev13-%s.webp" % npc
            self.assertTrue((GAME / new).exists(), new)
            for state in BODY:
                self.assertEqual(ACTING[npc][state]["file"], new, (npc, state))
                self.assertEqual(CAST[npc][state]["file"], new, (npc, state))
            self.assertEqual({i["file"] for i in FULLBODY[npc]["images"].values()}, {new}, npc)
            old_acting = BACKUP["npcs"][npc]["acting"]
            extra = {k for k in ACTING[npc] if k not in BODY and not k.startswith("avatar_")}
            if mode == "incoming":
                self.assertEqual(extra, set(), npc)                    # no old-species pose left
                self.assertNotIn(npc, SEATED)                           # no old seated picture
            else:
                info = next(e for e in GALLERY["applied"] if e["npc"] == npc)
                self.assertEqual(extra, set(info["kept_poses"]), npc)
                for k in extra:
                    self.assertEqual(ACTING[npc][k], old_acting[k], (npc, k))   # kept verbatim
                old_extra = {k for k in old_acting if k not in BODY and not k.startswith("avatar_")}
                self.assertEqual(extra | set(info["dropped_poses"]), old_extra, npc)
                # kept poses share the new figure's proportions (never the old chibi sheets)
                base = ACTING[npc]["neutral"]["head"][3] / ACTING[npc]["neutral"]["foot"][1]
                for k in extra:
                    spec = ACTING[npc][k]
                    share = spec["head"][3] / spec.get("foot", [0, spec["crop"][3]])[1]
                    self.assertLess(abs(share * spec.get("stature_ratio", 1.0) / base - 1), .36, (npc, k))

    def test_others_untouched_and_rollback_available(self):
        touched = {d["npc"] for d in REG["designs"] if d["apply"] in ("incoming", "selected")}
        originals = ART / "original-files"
        for name, current in (("cast.json", CAST), ("room13-pixel-acting.json", ACTING)):
            before = load(originals / name)
            for npc in before:
                if npc not in touched:
                    self.assertEqual(current.get(npc), before[npc], (name, npc))
        self.assertNotIn("resident_seol", touched)
        self.assertEqual(len(GALLERY["designs"]), 3)
        for g in GALLERY["designs"]:
            self.assertTrue((GAME / g["file"]).exists())


if __name__ == "__main__":
    unittest.main()
