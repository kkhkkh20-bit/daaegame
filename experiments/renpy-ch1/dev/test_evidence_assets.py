"""Every current story record has authored art or an explicit state/portrait source."""
import json
import ast
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def catalog():
    evidence = json.loads((ROOT / "game/v111/records.json").read_text())["evidence"]
    for path in sorted((ROOT / "game/v111/newworld").glob("d??.json")):
        data = json.loads(path.read_text())
        for key, spec in data.get("evidence", {}).items():
            evidence[key].update(spec)
        evidence.update(data.get("new_evidence", {}))
    return evidence


class EvidenceAssets(unittest.TestCase):
    def test_current_art_precedes_legacy_mapping_but_state_art_survives(self):
        text=(ROOT / "game/room13_notebook.rpy").read_text().split("init 68 python:\n",1)[1].split("\ninit 71:",1)[0]
        tree=ast.parse(textwrap.dedent(text))
        fn=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=="r13_record_icon")
        env=dict(ROOM13={"evidence_sources":{}},r13_record_category=lambda key:"evidence",
            r13_evidence_art_path=lambda key:"authored-letter" if key=="V111:E01" else None,
            r13_material_art=lambda key:"portrait-state" if key=="V111:E09" else "legacy-mapped-paper")
        exec(compile(ast.Module(body=[fn],type_ignores=[]),"icon-priority","exec"),env)
        self.assertEqual(env["r13_record_icon"]("V111:E01"),"authored-letter")
        self.assertEqual(env["r13_record_icon"]("V111:E09"),"portrait-state")
        self.assertEqual(env["r13_record_icon"]("E01"),"legacy-mapped-paper")

    def sources(self):
        source = (ROOT / "game/systems/room13_evidence_sources.rpy").read_text()
        env = {"ROOM13": {"evidence_sources": {"legacy": "existing"}}}
        exec(textwrap.dedent(source.split("init 329 python:\n", 1)[1]), env)
        self.assertEqual(env["ROOM13"]["evidence_sources"]["legacy"], "existing")
        return env["R13_V111_TESTIMONY_SOURCES"]

    def test_every_current_record_has_specific_art(self):
        sources = self.sources()
        state_art = {"E09", "E30", "E13_MENDING"}
        missing = [key for key in catalog() if key not in sources and key not in state_art
                   and not (ROOT / "game/assets/evidence" / (key + ".webp")).is_file()]
        self.assertEqual(missing, [])

    def test_testimony_sources_match_authored_speakers_and_have_faces(self):
        sources = self.sources()
        evidence = catalog()
        cast = json.loads((ROOT / "game/assets/cast.json").read_text())
        names = {"bami": "밤이", "guard": "돌목", "resident_nero": "네로",
                 "resident_nubi": "누비", "resident_madam": "백 부인",
                 "resident_somi": "솜이", "kid_kkomi": "꼬미"}
        self.assertEqual(set(sources), {key for key, spec in evidence.items() if spec["kind"] == "증언"})
        for key, person in sources.items():
            with self.subTest(key=key):
                text = " ".join(evidence[key]["variants"].values())
                self.assertIn(names[person], text)
                self.assertTrue((ROOT / "game" / cast[person]["avatar_neutral"]["file"]).is_file())

    def test_state_art_variants_remain_available(self):
        art = json.loads((ROOT / "game/ms14/art.json").read_text())
        for key in ("bundle", "portrait_complete", "portrait_unfinished", "portrait_child"):
            self.assertTrue((ROOT / "game" / art[key]["file"]).is_file(), key)
        self.assertTrue((ROOT / "game/assets/room13-v111-blanket-after.webp").is_file())


if __name__ == "__main__":
    unittest.main()
