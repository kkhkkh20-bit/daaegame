"""초반 증명은 확보한 진술과 관찰을 잇고, 같은 사실의 기록을 중복 제출하도록 강요하지 않는다."""
import ast
import json
from pathlib import Path
import textwrap
import unittest


GAME = Path(__file__).resolve().parents[1] / "game"
REPAIR = "수리와 반출을 가릴 자료를 낸다"
SALE = "돌과 매입 기록을 낸다"
STONE = "마지막 점검과 인수한 돌을 연결한다"
GATE_POST = "밤이 혐의의 근거를 확인한다"


class DayThreeProofRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (GAME / "room13_v111_newworld_rules.rpy").read_text()
        tree = ast.parse(textwrap.dedent(source.split("init 318 python:", 1)[1]))
        names = {
            "R13_PROOF_EXTRAS", "R13_PROOF_ALTERNATES",
            "r13_v111_proof_sets", "r13_v111_proof_accepts",
            "R13_NW_WRONG_MISSING", "R13_NW_WRONG_THOUGHTS", "r13_nw_wrong_text",
        }
        nodes = [
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name in names
            or isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id in names
                for target in node.targets
            )
        ]
        cls.env = {}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "<실행 증명 규칙>", "exec"), cls.env)
        cls.correct = {}
        for filename in ("room13_v111_days123.rpy", "room13_v111_days45.rpy", "room13_lamp_attempt.rpy"):
            for line in (GAME / filename).read_text().splitlines():
                if line.strip().startswith("call r13_v111_proof("):
                    call = ast.parse(line.strip()[5:], mode="eval").body
                    cls.correct[ast.literal_eval(call.args[0])] = ast.literal_eval(call.args[1])

    def accepts(self, claim, evidence):
        return self.env["r13_v111_proof_accepts"](
            claim, self.correct[claim], ["V111:" + key for key in evidence]
        )

    def test_measurement_and_later_check_work_with_or_without_loan_note(self):
        # 우박의 개봉·반환 진술은 진료소에서 이미 듣는다. E13 문서 자체는 측정 시각 기록이다.
        for evidence in (
            ("E11", "E13"), ("E11", "E12", "E13"),
            ("E10", "E11", "E13"), ("E10", "E11", "E12", "E13"),
        ):
            with self.subTest(evidence=evidence):
                self.assertTrue(self.accepts(REPAIR, evidence))
        for evidence in (("E11",), ("E13",), ("E11", "E12"), ("E12", "E13")):
            with self.subTest(evidence=evidence):
                self.assertFalse(self.accepts(REPAIR, evidence))

    def test_transport_note_supports_but_cannot_replace_sale_and_stone(self):
        self.assertTrue(self.accepts(SALE, ("E15", "E16")))
        self.assertTrue(self.accepts(SALE, ("E14", "E15", "E16")))
        for evidence in (("E14",), ("E14", "E15"), ("E14", "E16")):
            with self.subTest(evidence=evidence):
                self.assertFalse(self.accepts(SALE, evidence))
        self.assertFalse(self.accepts(SALE, ("E09", "E14", "E15", "E16")))

    def test_stone_identity_links_check_and_mark_without_repeating_sale(self):
        # 실룩의 판매는 직전 매입 쟁점에서 입증된다. 새벽의 돌과 창고에서 구별한 돌을 잇는다.
        self.assertTrue(self.accepts(STONE, ("E11", "E15")))
        self.assertTrue(self.accepts(STONE, ("E11", "E14", "E15")))
        self.assertTrue(self.accepts(STONE, ("E11", "E15", "E16")))
        for evidence in (
            ("E11",), ("E15",), ("E11", "E13"),
            ("E15", "E16"), ("E11", "E14", "E16"),
        ):
            with self.subTest(evidence=evidence):
                self.assertFalse(self.accepts(STONE, evidence))

    def test_new_stolen_lamp_alternate_does_not_prove_prevented_attempt(self):
        for claim in ("수리 뒤 새로 생긴 파손을 가린다", "남아 있는 돌과 칼의 사용을 연결한다"):
            with self.subTest(claim=claim):
                self.assertTrue(self.accepts(claim, self.correct[claim]))
                self.assertFalse(self.accepts(claim, ("E11", "E13")))

    def test_gate_post_cloth_comparison_already_carries_fence_origin(self):
        # E23은 수거한 울타리 천과 겉옷의 실제 대조다. E22를 다시 내지 않아도 그 연결은 남는다.
        for evidence in (
            ("E20", "E23", "E24"),
            ("E20", "E22", "E23", "E24"),
            ("E20", "E21", "E23", "E24"),
        ):
            with self.subTest(evidence=evidence):
                self.assertTrue(self.accepts(GATE_POST, evidence))

    def test_gate_post_still_needs_identification_comparison_and_wearer(self):
        # 최초 진술, 천의 식별, 그날 착용자 중 빠진 축을 단순 현장 천이나 다른 목격으로 메우지 않는다.
        for evidence in (
            ("E23", "E24"), ("E20", "E24"), ("E20", "E23"),
            ("E21", "E22", "E23", "E24"),
            ("E20", "E21", "E22", "E24"),
            ("E20", "E21", "E22", "E23"),
        ):
            with self.subTest(evidence=evidence):
                self.assertFalse(self.accepts(GATE_POST, evidence))

    def test_gate_post_keeps_existing_portrait_alternates(self):
        for evidence in (
            ("E20", "E22", "NW_PIKO_SKETCH4"),
            ("E20", "E22", "E23", "NW_PIKO_SKETCH4"),
            ("E20", "E22", "E24", "NW_PIKO_SKETCH4"),
            ("E20", "E21", "E22", "E23", "E24", "NW_PIKO_SKETCH4"),
        ):
            with self.subTest(evidence=evidence):
                self.assertTrue(self.accepts(GATE_POST, evidence))
        self.assertFalse(self.accepts(GATE_POST, ("E22", "NW_PIKO_SKETCH4")))

    def test_gate_post_combines_actual_cloth_comparison_and_portrait(self):
        # E23이 천의 현장 출처를 잇고 그림이 착용자의 차림을 보인다. 어느 한 축도 생략하지 않는다.
        self.assertTrue(self.accepts(GATE_POST, ("E20", "E23", "NW_PIKO_SKETCH4")))
        self.assertFalse(self.accepts(GATE_POST, ("E20", "NW_PIKO_SKETCH4")))
        self.assertFalse(self.accepts(GATE_POST, ("E23", "NW_PIKO_SKETCH4")))

    def test_gate_post_partial_alternate_asks_for_actual_missing_link(self):
        # 세 장 경로에서 빠진 축을 물어야 한다. E23이 이미 연결한 울타리 출처를 다시 묻지 않는다.
        source = (GAME / "room13_v111_newworld_text.rpy").read_text()
        tree = ast.parse(textwrap.dedent(source.split("init 319 python:", 1)[1]))
        table = next(
            node.value for node in tree.body
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "R13_NW_WHEN"
                for target in node.targets
            )
        )
        presented = set()
        env = {"r13_gp_half": lambda: True, "r13_gp_given": lambda: presented}
        conditions = {
            key.value: eval(compile(ast.Expression(body=value), "<일부 제출 조건>", "eval"), env)
            for key, value in zip(table.keys, table.values)
            if isinstance(key, ast.Constant) and key.value.startswith("gate_post_half_")
        }
        variants = json.loads((GAME / "v111/newworld/d05.json").read_text())["replace"]["MS14_D05_S03_L0038"]
        for evidence, expected in (
            (("E23", "E24"), "gate_post_half_height"),
            (("E20", "E23"), "gate_post_half_wearer"),
            (("E20", "E24"), "gate_post_half_match"),
            (("E23", "NW_PIKO_SKETCH4"), "gate_post_half_height"),
            (("E20", "NW_PIKO_SKETCH4"), "gate_post_half_fence"),
        ):
            with self.subTest(evidence=evidence):
                presented.clear()
                presented.update("V111:" + key for key in evidence)
                actual = next(
                    row.get("when") for row in variants
                    if not row.get("when") or conditions[row["when"]]()
                )
                self.assertEqual(actual, expected)


    def test_gate_does_not_require_optional_rule_to_give_combination_feedback(self):
        claim = "함께 들어갈 근거를 고른다"
        self.env["r13_nw_cannot_solve"] = lambda issue: False
        self.env["r13_v111_owned"] = lambda key: key in {"E02", "E03"}
        self.assertEqual(self.env["r13_nw_wrong_text"](claim, 1),
                         self.env["R13_NW_WRONG_THOUGHTS"][claim][1])
        self.env["r13_v111_owned"] = lambda key: key == "E02"
        self.assertEqual(self.env["r13_nw_wrong_text"](claim, 1),
                         self.env["R13_NW_WRONG_MISSING"][claim][1])


if __name__ == "__main__":
    unittest.main()
