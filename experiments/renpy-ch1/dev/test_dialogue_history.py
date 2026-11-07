"""백로그는 실제 표시 순서와 발화 안 페이지 순서를 보존하며 앞 대사를 만들지 않는다."""
import ast
import copy
import json
from pathlib import Path
import textwrap
from types import SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/room13_notebook.rpy"


class DialogueHistory(unittest.TestCase):
    def setUp(self):
        self.room = dict(day=1, location="inn", evidence=["V111:E01"], flags=["before"])
        self.store = SimpleNamespace(room13=self.room, room13_mode=True, r13_thought_active=False,
                                     dialogue_speaker="daram", _history_list=[])
        self.retained = []
        self.ns = dict(store=self.store, R13_PLACES={"inn": ("여관",)},
                       renpy=SimpleNamespace(filter_text_tags=lambda text, **kw: text,
                                             retain_after_load=lambda: self.retained.append(True)))
        body = SOURCE.read_text().split("init 68 python:\n", 1)[1].split("\ninit 71:", 1)[0]
        tree = ast.parse(textwrap.dedent(body))
        names = {"r13_history_stamp", "r13_history_rows", "r13_backlog_scroll_state", "r13_backlog_remember_scroll"}
        nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), "exec"), self.ns)

    def entry(self, what, who="다람", key=None, page=None, line_id="SOURCE1", thought=False):
        self.store.r13_read_id = key
        self.store.r13_page_i = page
        self.store.r13_pages = ["앞", "중간", "끝"]
        self.store.r13_packet = ("daram", "아직 보지 않은 나중 페이지", dict(line_id=line_id))
        self.store.r13_thought_active = thought
        entry = SimpleNamespace(what=what, who=who)
        self.ns["r13_history_stamp"](entry)
        self.store._history_list.append(entry)
        return entry

    def test_exchange_and_split_pages_are_in_reading_order(self):
        self.entry("아흔일곱 번째거든? 방 번호만 확인하는 거야.", "아빠", "dad", 0)
        self.entry("아빠도 아는 게 있어.", key="kid1", page=0)
        self.entry("십삼 호! 하나, 둘…… 열셋.", key="kid2", page=0)
        self.entry("외웠어.", key="kid3", page=0)
        self.entry("아빠는 짐 들어.", key="kid3", page=1)
        rows = self.ns["r13_history_rows"]()
        self.assertEqual([row["what"] for row in rows], [
            "아흔일곱 번째거든? 방 번호만 확인하는 거야.", "아빠도 아는 게 있어.",
            "십삼 호! 하나, 둘…… 열셋.", "외웠어.\n아빠는 짐 들어."])
        self.assertEqual((rows[-1]["first_page"], rows[-1]["last_page"]), (0, 1))
        self.assertEqual((rows[-1]["line_key"], rows[-1]["line_id"], rows[-1]["stamp"]),
                         ("kid3", "SOURCE1", "1일 · 여관"))

    def test_viewed_pages_only_and_history_query_has_no_mutation(self):
        self.entry("지금 본 앞부분.", key="partial", page=0)
        before = copy.deepcopy((self.room, self.store._history_list))
        rows = self.ns["r13_history_rows"]()
        self.assertEqual(rows[0]["what"], "지금 본 앞부분.")
        self.assertNotIn("아직 보지 않은", repr(rows))
        self.assertEqual((self.room, self.store._history_list), before)
        self.assertEqual(self.retained, [])

    def test_repeat_visit_missing_page_and_different_source_do_not_get_fused(self):
        self.entry("첫 방문.", key="repeat", page=0)
        self.entry("다시 방문.", key="repeat", page=0)
        self.entry("다음 페이지.", key="repeat", page=1)
        self.entry("새 출처.", key="repeat", page=2, line_id="SOURCE2")
        self.entry("보지 못한 앞쪽은 없음.", key="partial", page=2)
        rows = self.ns["r13_history_rows"]()
        self.assertEqual([row["what"] for row in rows], [
            "첫 방문.", "다시 방문.\n다음 페이지.", "새 출처.", "보지 못한 앞쪽은 없음."])

    def test_different_speaker_thought_and_place_remain_separate(self):
        self.entry("말.", key="x", page=0)
        self.entry("생각.", key="x", page=1, thought=True)
        self.entry("답.", who="아빠", key="x", page=2)
        self.store.place = "마차 안"
        self.entry("이동 뒤 말.", who="아빠", key="x", page=2)
        rows = self.ns["r13_history_rows"]()
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[1]["kind"], "독백")
        self.assertEqual(rows[-1]["stamp"], "1일 · 마차 안")

    def test_legacy_entries_keep_unknown_source_and_actual_chronology(self):
        self.store._history_list = [SimpleNamespace(who="다람", what="먼저 한 말."),
                                    SimpleNamespace(who="다람", what="그 다음 말.")]
        rows = self.ns["r13_history_rows"]()
        self.assertEqual([row["what"] for row in rows], ["먼저 한 말.", "그 다음 말."])
        self.assertTrue(all(row["stamp"] == "이전 저장의 대화" and row["line_key"] is None for row in rows))

    def test_stale_page_counter_outside_dialogue_is_not_given_current_line_source(self):
        entry = self.entry("별도 안내.", key="stale", page=3)
        self.assertFalse(hasattr(entry, "r13_line_key"))
        self.assertIsNone(self.ns["r13_history_rows"]()[0]["line_id"])

    def test_scroll_starts_at_latest_and_preserves_earlier_reading_position(self):
        state = self.ns["r13_backlog_scroll_state"]
        remember = self.ns["r13_backlog_remember_scroll"]
        self.assertEqual(state(), dict(value=0, range=0, tail=True))
        before = copy.deepcopy(self.room)
        remember(SimpleNamespace(value=240, range=1600))
        self.assertEqual(state(), dict(value=240, range=1600, tail=False))
        self.store.r13_backlog_position = json.loads(json.dumps(self.store.r13_backlog_position))
        self.assertEqual(state()["value"], 240)
        remember(SimpleNamespace(value=1598, range=1600))
        self.assertTrue(state()["tail"])
        self.assertEqual(self.room, before)
        self.assertEqual(len(self.retained), 2)


if __name__ == "__main__":
    unittest.main()
