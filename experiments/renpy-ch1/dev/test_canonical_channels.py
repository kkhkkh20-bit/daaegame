"""Canonical defaults, approved exceptions and missing-expression fallback."""
import ast
import hashlib
import json
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
A = GAME / "assets"
load = lambda p: json.loads(p.read_text())
REPORT = load(ROOT / "art/canonical-channel-alignment-20261017/report.json")


class CanonicalChannels(unittest.TestCase):
    def test_sources_channels_and_preserved_actions(self):
        fb = load(A / "room13-fullbody-dialogue.json")["people"]
        tables = [load(A / name) for name in ("cast.json", "room13-pixel-acting.json", "room13-portraits.json")]
        for rid, row in REPORT["roles"].items():
            self.assertEqual(hashlib.sha256((ROOT / row["source"]).read_bytes()).hexdigest(), row["sha256"])
            expected = fb[rid]["images"]["neutral"]["file"]
            for table in tables:
                self.assertEqual(table[rid]["neutral"]["file"], expected, rid)
            for action in row["preserved_approved_actions"]:
                self.assertIn(action, tables[1][rid])
        self.assertIn("living_thermos", tables[1]["resident_tosil"])
        self.assertIn("hold_storybook", tables[1]["resident_tosil"])

    def test_all_channel_paths_exist_and_pending_is_explicit(self):
        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key == "file" and isinstance(item, str) and item.startswith("assets/"):
                        self.assertTrue((GAME / item).is_file(), item)
                    else:
                        walk(item)
            elif isinstance(value, list):
                for item in value: walk(item)
        for name in ("cast.json", "room13-pixel-acting.json", "room13-portraits.json", "room13-fullbody-dialogue.json", "room13-meeting-seated.json"):
            walk(load(A / name))
        fb = load(A / "room13-fullbody-dialogue.json")["people"]
        for rid, missing in REPORT["pending_expressions"].items():
            if rid=="resident_solbang":
                self.assertEqual(fb[rid]["role_connect"],"approved-chinchilla-20261017")
                continue # Six approved chinchilla sources supersede this historical pending list.
            for emotion in missing:
                image = fb[rid]["images"][emotion]
                self.assertEqual(image["fallback"], "neutral")
                self.assertEqual(image["production_status"], "pending")
        layout = load(A / "room13-world-layout.json")
        for row in REPORT["pending_layout_actions"]:
            self.assertNotIn(row["person"], layout[row["place"]][row["field"]])

    def test_missing_expression_uses_current_neutral_before_old_bust(self):
        source = (GAME / "room13_fullbody_dialogue.rpy").read_text().split("init 58 python:\n", 1)[1]
        tree = ast.parse(textwrap.dedent(source))
        wanted = {"r13_fullbody_key", "r13_fullbody_emotion", "r13_fullbody_spec"}
        module = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted], type_ignores=[])
        env = dict(R13_FULLBODY_DIALOGUE=True, R13_FULLBODY_EMOTIONS=("neutral", "angry"),
                   R13_FULLBODY_LEGACY={}, R13_FULLBODY_FILES={"current.webp"},
                   R13_FULLBODY={"people": {"test": {"crop": [0, 0, 20, 30], "figure": [0, 0, 20, 30],
                       "images": {"neutral": {"file": "current.webp"}, "angry": {"file": "missing.webp"}}}}})
        exec(compile(module, "fullbody-spec", "exec"), env)
        spec = env["r13_fullbody_spec"]("test", "angry")
        self.assertEqual(spec["file"], "current.webp")
        self.assertEqual(spec["emotion"], "neutral")


if __name__ == "__main__":
    unittest.main()
