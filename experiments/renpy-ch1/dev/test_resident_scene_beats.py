"""3일의 짧은 주민 행동은 해당 실제 대사 경로에서만 보이고 획득·상태를 대신하지 않는다."""
import ast
import copy
import re
import unittest

from test_newworld_text import Layer, ROOT


class ResidentSceneBeats(Layer):
    def label(self, name):
        source = (ROOT / "game/room13_v111_days123.rpy").read_text()
        return re.search(r"^label " + name + r":\n(.*?)(?=^label |\Z)", source, re.M | re.S).group(1)

    def rows(self, env, label):
        rows = []
        for found in re.finditer(r"r13_v111_lines\((\[[^\]]*\])\)", self.label(label)):
            rows.extend(env["r13_v111_lines"](ast.literal_eval(found.group(1))))
        return rows

    def test_death_handover_runs_before_death_commit_without_touching_e09(self):
        env = self.load()
        # 원래 사망 발견 대화를 읽는 동안에는 아직 piko_alive의 초기값이 True다.
        self.assertTrue(env["r13_v111_value"]("piko_alive"))
        before = copy.deepcopy(self.state.room13)
        rows = self.rows(env, "r13_v111_piko_dead3")
        texts = [r[1] for r in rows]
        self.assertTrue(any("아빠가 여기 있는댔잖아" in t for t in texts))
        self.assertLess(next(i for i, t in enumerate(texts) if "아빠 여기 있을게" in t),
                        next(i for i, t in enumerate(texts) if "아빠가 여기 있는댔잖아" in t))
        self.assertEqual(self.state.room13, before, "행동 대사가 생사나 초상을 획득하지 않는다")
        env["r13_v111_commit"]("MS14_D03_S01_L0021")
        self.assertFalse(env["r13_v111_value"]("piko_alive"))
        self.assertTrue(env["r13_v111_owned"]("E09"))
        self.assertEqual(env["r13_v111_value"]("E09.variant"), "unfinished")

    def test_shelter_cleanup_resolves_the_chosen_work_before_complete_portrait(self):
        env = self.load()
        clean = self.label("r13_v111_piko_clean")
        self.assertIn("call r13_v111_wait('piko_clean')", clean)
        self.assertIn("if v111_answer==0:", clean)
        self.assertIn("jump r13_v111_piko_receive", clean)
        before = copy.deepcopy(self.state.room13)
        # 아침 재회만 읽어서는 실제 정리나 그림 인수 행동이 앞당겨 나오지 않는다.
        morning = self.rows(env, "r13_v111_piko_alive3")
        self.assertFalse(any("포대 양끝" in r[1] for r in morning))
        received = self.rows(env, "r13_v111_piko_receive")
        texts = [r[1] for r in received]
        cleanup = next(i for i, t in enumerate(texts) if "포대 양끝" in t)
        handover = next(i for i, r in enumerate(received) if r[2].get("line_id") == "MS14_D03_S01_L0036")
        self.assertLess(cleanup, handover)
        self.assertFalse(any("아빠가 여기 있는댔잖아" in t for t in texts))
        self.assertEqual(self.state.room13, before)
        env["r13_v111_commit"]("MS14_D03_S01_L0039")
        self.assertTrue(env["r13_v111_value"]("piko_alive"))
        self.assertEqual(env["r13_v111_value"]("E09.variant"), "complete")
        self.assertEqual(env["r13_v111_value"]("piko.location"), "clinic")

    def test_tool_and_loan_replies_keep_collected_fragment_and_note_on_both_routes(self):
        for alive in (False, True):
            with self.subTest(piko_alive=alive):
                env = self.load()
                env["r13_v111_set"]("piko_alive", alive)
                env["r13_v111_commit"]("MS14_D03_S02_L0016")
                env["r13_v111_commit"]("MS14_D03_S03_L0008")
                before = copy.deepcopy(self.state.room13)
                rows = self.rows(env, "r13_v111_lamp_fragment3") + self.rows(env, "r13_v111_loan3")
                texts = [r[1] for r in rows]
                self.assertTrue(any("톡이 자기 공구를 자루에 넣고" in t for t in texts))
                self.assertTrue(any("집게 돌려 달라고도" in t for t in texts))
                self.assertTrue(env["r13_v111_owned"]("E32"))
                self.assertTrue(env["r13_v111_owned"]("E12"))
                self.assertEqual(before, self.state.room13)
                self.assertFalse(any(r[0] == "resident_piko" for r in rows))
                # 사용 여부는 아직 확인할 문제다. 기존 가능성 질문을 범행 입증으로 바꾸지 않는다.
                self.assertTrue(any("아직은 모릅니다" in t and "누가 언제 썼는지" in t for t in texts))
                first = self.rows(env, "r13_v111_workshop3")
                self.assertFalse(any("뭐라고 적었어요" in r[1] for r in first))

    def test_attempt_has_no_death_or_shelter_work_and_keeps_its_complete_portrait(self):
        for sheltered in (False, True):
            with self.subTest(sheltered=sheltered):
                env = self.load()
                env["r13_v111_set"]("lamp_bound2", True)
                env["r13_v111_set"]("piko_sheltered", sheltered)
                before = copy.deepcopy(self.state.room13)
                rows = env["r13_nw_block"]("la_morning3")
                self.assertFalse(any("아빠가 여기 있는댔잖아" in r[1] or "포대 양끝" in r[1] for r in rows))
                self.assertEqual(self.state.room13, before)
                env["r13_v111_apply"]("lamp_attempt:portrait3", [
                    dict(op="set", field="portrait", value="complete"),
                    dict(op="acquire", key="E09", variant="complete"),
                ])
                self.assertEqual(env["r13_v111_value"]("E09.variant"), "complete")
                self.assertTrue(env["r13_v111_value"]("piko_alive"))


if __name__ == "__main__":
    unittest.main()
