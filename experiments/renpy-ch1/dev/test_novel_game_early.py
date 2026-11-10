"""소설 개정의 초반 감정·연락 출처가 기존 플레이 경로를 보존하는지 검증한다."""
import copy
import json
import re
import unittest
from test_newworld_text import Layer, ROOT


class EarlyNovelAdaptation(Layer):
    def test_family_reactions_require_present_child_without_granting_records(self):
        env = self.load()
        env["r13_v111_actor_ready"] = lambda who: who == "daram"
        anchors = ["MS14_D01_S04_L0020", "MS14_D01_S05_L0007", "MS14_D01_S05_L0017", "MS14_D01_S05_L0040"]
        before = copy.deepcopy(self.state.room13)
        rows = env["r13_v111_lines"](anchors)
        data = json.loads((ROOT / "game/v111/newworld/d01.json").read_text())
        added = [row["text"] for anchor in anchors for row in data["after"].get(anchor, []) if row["id"].startswith("NW_NOV_D01_")]
        self.assertTrue(set(added) <= {row[1] for row in rows})
        self.assertEqual(before, self.state.room13)
        env["r13_v111_actor_ready"] = lambda who: False
        rows = env["r13_v111_lines"](anchors)
        self.assertFalse(set(added) & {row[1] for row in rows})
        self.assertEqual(before, self.state.room13)

    def test_written_note_supplies_reply_context_only_after_player_writing(self):
        env = self.load()
        rows = env["r13_nw_block"]("box_note_written2")
        note = " ".join(row[1] for row in rows)
        self.assertIn("편지를 받고 다람이랑 왔어", note)
        self.assertNotIn("당신이 보낸", note)
        self.assertIn("13호실", note)
        self.assertIn("초롱 씨에게 답", note)
        source = (ROOT / "game/room13_v111_days123.rpy").read_text()
        label = lambda name: re.search(r"^label " + name + r":\n(.*?)(?=^label |\Z)", source, re.M | re.S).group(1)
        gate = label("r13_v111_box_note")
        written = label("r13_v111_box_written")
        self.assertIn("call r13_v111_wait('box_note')", gate)
        self.assertIn("if v111_answer==0:", gate)
        self.assertLess(written.index("r13_nw_block('box_note_written2')"), written.index("r13_v111_commit('MS14_D02_S01_L0039')"))
        self.assertEqual(source.count("r13_v111_commit('MS14_D02_S01_L0039')"), 1)
        # 작성 뒤 원래 L0040 앞에 또 종이를 꺼내고 넣는 장면이 붙지 않는다.
        after_writing = " ".join(row[1] for row in env["r13_v111_lines"](["MS14_D02_S01_L0040"]))
        self.assertIn("함에 넣었습니다", after_writing)
        self.assertIn("오후에 답이 왔는지 다시", after_writing)
        self.assertNotIn("쪽지 남기자", after_writing)
        self.assertNotIn("쪽지를 함 안쪽", after_writing)
        data = json.loads((ROOT / "game/v111/newworld/d02.json").read_text())
        self.assertFalse({"NW_D02_SR01", "NW_D02_SR02", "NW_D02_SR03", "NW_D02_SR04"} & {row.get("id") for rows in data["before"].values() for row in rows})



    def test_memorial_keeps_completion_marker_but_leaves_nose_for_reunion(self):
        env = self.load()
        env["r13_v111_set"]("piko_alive", False)
        source = (ROOT / "game/room13_v111_days123.rpy").read_text()
        block = re.search(r"^label r13_v111_piko_memorial:\n(.*?)(?=^label )", source, re.M | re.S).group(1)
        tail = block[block.index("    $ r13_v111_commit('MS14_D03_S06_L0022')"):]
        before_evidence = copy.deepcopy(self.state.room13["evidence"])
        for line in tail.splitlines():
            if line.strip().startswith("$ "):
                exec(line.strip()[2:], env)
        self.assertEqual(env["r13_v111_value"]("portrait"), "unfinished")
        self.assertTrue(env["r13_v111_value"]("portrait_waiting_for_mom"))
        self.assertFalse(env["r13_v111_value"]("piko_alive"))
        self.assertEqual(before_evidence, self.state.room13["evidence"])
        saved = copy.deepcopy(self.state.room13)
        env["r13_v111_commit"]("MS14_D03_S06_L0022")
        self.assertEqual(saved, self.state.room13, "기존 완료 표시가 이중 커밋을 막는다")


if __name__ == "__main__":
    unittest.main()
