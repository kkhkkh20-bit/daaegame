"""읽기 쌍과 제출 선택을 분리하고 현재 자료의 사실만 분류한다.

Ren'Py 없이 실제 함수와 자료를 읽는다. 화면 배치·입력은 동명의 native QA가 맡는다.
"""
import copy
import json
import textwrap
import unittest
from collections.abc import Mapping, Sequence
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "game/systems/room13_proof_workspace.rpy"
EVIDENCE_VIEW = ROOT / "game/systems/room13_evidence_view.rpy"
FACTS = json.loads((ROOT / "game/v111/evidence-facts.json").read_text())
RECORDS = json.loads((ROOT / "game/v111/records.json").read_text())


def load_function(path, name, namespace):
    """init 블록 전체를 실행하지 않고 요청한 기존 함수만 가져온다."""
    lines = path.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("    def " + name + "("))
    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line.strip() and not line.startswith("        "):
            break
        end += 1
    exec(compile(textwrap.dedent("\n".join(lines[start:end])), str(path), "exec"), namespace)
    return namespace[name]


class ProofReadingPair(unittest.TestCase):
    def setUp(self):
        self.ns = {}
        self.read_pair = load_function(WORKSPACE, "r13_pw_read_pair", self.ns)
        load_function(WORKSPACE, "r13_pw_pair_live", self.ns)
        self.open_pair = load_function(WORKSPACE, "r13_pw_pair_on_open", self.ns)

    def test_empty_slots_fill_without_touching_submit_selection(self):
        pair = [None, None]
        submitted = ["V111:E32"]
        before = copy.deepcopy((pair, submitted))
        result = self.read_pair(pair, "V111:E11", 0)
        self.assertEqual(result, ("V111:E11", None))
        self.assertEqual(self.read_pair(result, "V111:E13", 1), ("V111:E11", "V111:E13"))
        self.assertEqual((pair, submitted), before)

    def test_replace_one_slot_preserves_other_and_original(self):
        pair = ["V111:E11", "V111:E13"]
        self.assertEqual(self.read_pair(pair, "V111:E32", 0), ("V111:E32", "V111:E13"))
        self.assertEqual(pair, ["V111:E11", "V111:E13"])

    def test_moving_same_record_empties_its_previous_slot(self):
        pair = ("V111:E11", "V111:E13")
        self.assertEqual(self.read_pair(pair, "V111:E13", 0), ("V111:E13", None))
        self.assertEqual(self.read_pair(pair, "V111:E11", 1), (None, "V111:E11"))
        self.assertEqual(self.read_pair(pair, "V111:E11", 0), pair)

    def test_invalid_slot_does_not_replace_or_mutate(self):
        pair = ["V111:E11", "V111:E13"]
        for slot in (None, -1, 2):
            self.assertEqual(self.read_pair(pair, "V111:E32", slot), tuple(pair))
        self.assertEqual(pair, ["V111:E11", "V111:E13"])

    def test_open_reads_the_two_explicit_checks_without_submitting(self):
        checked = ["V111:E11", "V111:E13"]
        old_pair = ["V111:E01", None]
        before = copy.deepcopy((checked, old_pair))
        self.assertEqual(self.open_pair(checked, old_pair, "V111:E01", checked + ["V111:E01"]), tuple(checked))
        self.assertEqual((checked, old_pair), before)

    def test_open_does_not_guess_which_two_of_three_to_read(self):
        owned = ["V111:E01", "V111:E11", "V111:E13"]
        self.assertEqual(self.open_pair(owned, (owned[0], owned[1]), owned[2], owned), (owned[0], owned[1]))
        self.assertEqual(self.open_pair(owned, None, owned[2], owned), (owned[2], None))

    def test_open_drops_missing_records_and_keeps_one_check_independent(self):
        owned = ["V111:E11", "V111:E13"]
        self.assertEqual(self.open_pair([owned[0]], (owned[1], "missing"), owned[0], owned), (owned[1], None))
        self.assertEqual(self.open_pair([owned[0], "missing"], None, "missing", owned), (None, None))

    def test_compare_starts_with_past_and_current_documents_visible(self):
        initial = load_function(WORKSPACE, "r13_pw_initial_tab", {})
        owned = [str(i) for i in range(20)]
        self.assertEqual(initial("compare", True, owned, owned[:2]), "all")
        self.assertEqual(initial("proof", True, owned, owned[:2]), "now")
        self.assertEqual(initial("proof", True, owned, []), "all")


class ProofReadingGroups(unittest.TestCase):
    def build(self, values=None):
        values = dict(values or {})
        ns = {
            "_R13EvMapping": Mapping, "_R13EvSequence": Sequence,
            "R13_EVIDENCE_FACT_LIMIT": 3, "R13_EVIDENCE_FACTS": copy.deepcopy(FACTS),
            "R13_V111": RECORDS, "r13_v111_active": lambda: True,
            "r13_v111_value": lambda key: values.get(key),
            "r13_catalog_record": lambda key: None,
        }
        for name in ("_r13_ev_is_lines", "r13_evidence_base_key", "r13_evidence_variant", "r13_evidence_split", "r13_evidence_facts", "r13_evidence_read_groups"):
            load_function(EVIDENCE_VIEW, name, ns)
        return load_function(WORKSPACE, "r13_pw_read_groups", ns), ns

    def test_e11_has_only_existing_document_facts(self):
        groups, ns = self.build({"E11.variant": "observed"})
        before = copy.deepcopy(ns["R13_EVIDENCE_FACTS"])
        result = groups("V111:E11")
        self.assertEqual(result, [("점검장에 적힌 내용", FACTS["E11"]["observed"])])
        self.assertNotIn("청소", repr(result))
        self.assertNotIn("파편", repr(result))
        self.assertEqual(ns["R13_EVIDENCE_FACTS"], before)

    def test_e13_separates_only_the_existing_reported_statement(self):
        groups, ns = self.build({"E13.variant": "observed"})
        original = copy.deepcopy(ns["R13_EVIDENCE_FACTS"])
        self.assertEqual(groups("V111:E13"), [
            ("측정지에 적힌 내용", FACTS["E13"]["observed"][:2]),
            ("함께 들은 말", FACTS["E13"]["observed"][2:]),
        ])
        self.assertEqual([line for _, lines in groups("V111:E13") for line in lines], FACTS["E13"]["observed"])
        self.assertEqual(ns["R13_EVIDENCE_FACTS"], original)

    def test_other_portrait_variants_and_later_status_remain_current(self):
        for values, key, variant in (
            ({"E09.variant": "unfinished"}, "E09", "unfinished"),
            ({"E09.variant": "complete"}, "E09", "complete"),
            ({"E09.variant": "unfinished", "portrait": "child_completed"}, "E09", "child_completed"),
            ({"E35.variant": "reserved", "E35.status": "received"}, "E35", "received"),
        ):
            with self.subTest(values=values):
                groups, _ = self.build(values)
                self.assertEqual(groups("V111:" + key), [("확인한 내용", FACTS[key][variant])])

    def test_unrecognized_e13_variant_is_not_given_old_testimony(self):
        groups, ns = self.build({"E13.variant": "other"})
        ns["R13_EVIDENCE_FACTS"]["E13"]["other"] = ["다른 변형에서 확보한 내용만 남는다."]
        self.assertEqual(groups("V111:E13"), [("확인한 내용", ["다른 변형에서 확보한 내용만 남는다."])])
        ns["R13_EVIDENCE_FACTS"]["E13"]["other"] = ["첫 관찰", "둘째 관찰", "새 관찰"]
        self.assertEqual(groups("V111:E13"), [("확인한 내용", ["첫 관찰", "둘째 관찰", "새 관찰"])])


class SmallFinishGeometry(unittest.TestCase):
    def test_mobile_settings_thumbnail_fits_inside_existing_slot(self):
        thumb = load_function(ROOT / "game/screens.rpy", "r13_settings_save_thumb", {})
        for touch, area, controls in ((False, 460, 52), (True, 436, 88)):
            slot_h = (area - 24 - controls - 12 - 28) // 3
            width, height = thumb(slot_h)
            self.assertLessEqual(height, slot_h - 20)
            self.assertLessEqual(width, 160)
            self.assertLess(abs(width / height - 16 / 9), .02)
            self.assertEqual((width, height), (131, 74) if touch else (160, 90))


if __name__ == "__main__":
    unittest.main()
