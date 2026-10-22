"""2026-10-22 expression intake (dev/import_expr_intake_20261022.py): originals kept byte-exact,
each slot connected with its character's convention, feet on the neutral's foot row."""
import hashlib, json, unittest
from pathlib import Path

import numpy as np
from PIL import Image
from import_expr_intake_20261022 import ART, GAME, PLAN, TAG, HAZE

REPORT = json.loads((ART / "connection-report.json").read_text(encoding="utf-8"))
BEFORE = json.loads((ART / "original-entries.json").read_text(encoding="utf-8"))
FB = json.loads((GAME / "assets/room13-fullbody-dialogue.json").read_text(encoding="utf-8"))["people"]
ROOT = ART.parents[1]


def rgba(path):
    return np.asarray(Image.open(path).convert("RGBA"))


def lowest(alpha):
    return int(np.where((alpha >= 32).any(1))[0].max()) + 1


class ExprIntake(unittest.TestCase):
    def test_plan_report_and_registry_agree(self):
        self.assertEqual([(r["person"], r["key"]) for r in REPORT["expressions"]], [(p, e) for _, p, e, _ in PLAN])
        for row in REPORT["expressions"]:
            image = FB[row["person"]]["images"][row["key"]]
            self.assertEqual(image, row["image"])
            self.assertEqual(image["review_batch"], TAG)
            self.assertNotIn("fallback", image)
            self.assertNotEqual(image["file"], FB[row["person"]]["images"]["neutral"]["file"])
            self.assertEqual(hashlib.sha256((ROOT / row["source"]).read_bytes()).hexdigest(), image["source_sha256"])
            self.assertEqual(hashlib.sha256((GAME / image["file"]).read_bytes()).hexdigest(), row["runtime_sha256"])
            self.assertIn(row["person"] + "/" + row["key"], BEFORE)
        files = [r["image"]["file"] for r in REPORT["expressions"]]
        self.assertEqual(len(set(files)), len(files))

    def test_pixels_geometry_and_feet(self):
        for row in REPORT["expressions"]:
            with self.subTest(slot=row["person"] + "/" + row["key"]):
                entry, image = FB[row["person"]], row["image"]
                shown = rgba(GAME / image["file"])
                self.assertEqual(list(shown.shape[1::-1]), image["size"])
                alpha = shown[..., 3]
                for edge in (alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]):
                    self.assertFalse((edge >= 32).any())
                u, ox, oy = image["map"]
                foot = oy + u * lowest(alpha)
                figure_bottom = entry["figure"][1] + entry["figure"][3]
                if row["method"] == "batch":
                    src = rgba(ROOT / row["source"]).copy()
                    src[src[..., 3] < HAZE] = 0
                    self.assertTrue(np.array_equal(src, shown))      # generator pixels, haze only
                    self.assertTrue(image["native_detail"])
                    self.assertAlmostEqual(foot, figure_bottom, places=3)
                elif row["method"] == "acting":
                    neutral = entry["images"]["neutral"]
                    self.assertEqual(image["cell"], 2)
                    self.assertEqual(u, entry["pixel"]["u"])
                    self.assertTrue((shown[0::2, 0::2] == shown[1::2, 1::2]).all())
                    self.assertEqual(set(np.unique(alpha)) - {0, 255}, set())
                    self.assertEqual([v % 2 for v in image["crop"]], [0, 0, 0, 0])
                    n_alpha = rgba(GAME / neutral["file"])[..., 3]
                    self.assertAlmostEqual(foot, neutral["map"][2] + u * lowest(n_alpha), places=3)
                else:
                    self.assertEqual(image["size"], [512, 768])
                    self.assertEqual(u, 1.0)
                    self.assertEqual(foot, figure_bottom)
                x, y, w, h = image["crop"]
                self.assertLessEqual(x + w, image["size"][0]); self.assertLessEqual(y + h, image["size"][1])
                self.assertEqual(int(alpha[y:y + h, x:x + w].astype(np.int64).sum()), int(alpha.astype(np.int64).sum()))

    def test_untouched_slots_and_skips(self):
        planned = {(p, e) for _, p, e, _ in PLAN}
        for person, entry in FB.items():
            for emotion, image in entry["images"].items():
                if (person, emotion) not in planned:
                    self.assertNotEqual(image.get("review_batch"), TAG, (person, emotion))
        # Skipped on purpose (README.txt): Piko's palette set is incomplete; granny already has scarf art.
        self.assertEqual(FB["resident_piko"]["images"]["joy"].get("fallback"), "neutral")
        self.assertIn("scarf", FB["granny"]["images"]["joy"]["file"])


if __name__ == "__main__":
    unittest.main()
