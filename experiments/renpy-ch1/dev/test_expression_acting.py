"""0.18.92 dialogue expression package (dev/apply_expression_acting.py): one key = one picture,
pixels exact, maps consistent, held characters untouched, rollback data present."""
import csv, hashlib, json, unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/expression-acting-20261016"
REG = json.loads((ART / "registry.json").read_text(encoding="utf-8"))
ROWS = list(csv.DictReader((ART / "pack68/current-selection-map.csv").open(encoding="utf-8")))
FULLBODY = json.loads((GAME / "assets/room13-fullbody-dialogue.json").read_text(encoding="utf-8"))["people"]
BEFORE = json.loads((ART / "original-files/room13-fullbody-dialogue.json").read_text(encoding="utf-8"))["people"]
EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")


def rgba(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(int)


class ExpressionActing(unittest.TestCase):
    def test_package_is_complete_and_byte_exact(self):
        self.assertEqual(len(ROWS), 68)
        self.assertEqual(len({(r["character"], r["expression"]) for r in ROWS}), 68)   # one picture per key
        for r in ROWS:
            self.assertEqual(hashlib.sha256((ART / "pack68" / r["file"]).read_bytes()).hexdigest(), r["sha256"], r["file"])
        # the 2nd art-fix delivery's lion/Neoul pictures are the same bytes (not applied twice)
        manifest = json.loads((ART / "second-fixes/manifest.json").read_text(encoding="utf-8"))
        same = {r["sha256"] for r in ROWS if r["character"] in ("neoul", "resident_teacher")}
        self.assertEqual({f["sha256"] for f in manifest["files"] if f.get("sha256")}, same)

    def test_every_package_key_is_shown_exactly(self):
        for r in ROWS:
            person, emotion = r["character"], r["expression"]
            if person in REG["held"]:
                continue
            image = FULLBODY[person]["images"][emotion]
            self.assertEqual(image.get("source_sha256"), r["sha256"], (person, emotion))
            shown = rgba(GAME / image["file"])
            src = rgba(ART / "pack68" / r["file"])
            if REG["apply"][person]["kind"] == "hires":
                src = src[0::2, 0::2]                       # one sample per 2x2 cell
            self.assertEqual(shown.shape, src.shape)
            visible = src[..., 3] > 0
            self.assertTrue((shown[..., 3] == src[..., 3]).all(), (person, emotion))
            self.assertTrue((shown[visible][:, :3] == src[visible][:, :3]).all(), (person, emotion))

    def test_missing_keys_and_maps(self):
        for person, spec in REG["apply"].items():
            entry = FULLBODY[person]
            keys = {r["expression"] for r in ROWS if r["character"] == person}
            self.assertEqual(entry["acting_package"], "expression-acting-20261016")
            for e in EMOTIONS:
                image = entry["images"][e]
                if e in keys:
                    continue
                if spec.get("package_only"):
                    self.assertEqual(image["file"], entry["images"]["neutral"]["file"], (person, e))
                else:
                    self.assertEqual(image["file"], BEFORE[person]["images"][e]["file"], (person, e))
            maps = {tuple(i["map"]) for i in entry["images"].values() if "map" in i and i.get("cell")}
            if spec["kind"] == "pixel":
                self.assertEqual(entry["pixel"]["cell"], 2)
                # one scale for every package picture of the character
                self.assertEqual({m[0] for m in maps}, {entry["pixel"]["u"]}, person)
            self.assertEqual(entry.get("poses"), BEFORE[person].get("poses"), person)

    def test_whole_screen_pixels_per_cell(self):
        # mirror of r13_fullbody_scale: k screen pixels per 2x2 cell, near the usual size
        for person, entry in FULLBODY.items():
            if "pixel" not in entry:
                continue
            for height in (840, 760, 560):
                scale = height * 1.05 * {"bami": .88, "doto": .92}.get(person, 1.0) / entry["figure"][3]
                unit = entry["pixel"]["u"] * entry["pixel"]["cell"]
                k = max(1, round(scale * unit))
                s = k / unit
                self.assertLess(abs(s / scale - 1), .2, (person, height))
                for image in entry["images"].values():
                    if image.get("cell"):
                        u = image["map"][0]
                        self.assertAlmostEqual(s * u * 2, k, places=6)
                        self.assertEqual(image["crop"][2] % 2, 0)

    def test_held_characters_are_untouched(self):
        for person in REG["held"]:
            self.assertEqual(FULLBODY[person], BEFORE[person], person)


if __name__ == "__main__":
    unittest.main()
