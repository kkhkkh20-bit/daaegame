# 대사 쪽 경계: 읽는 도중 글자 크기를 바꾸거나 저장을 복원해도 원문을 빠뜨리지 않는다.
import ast
import copy
import os
import pickle
import re
import textwrap
import types
import unittest

from v2data import DAY, GAME, all_steps


class DialoguePages(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(GAME, "engine/engine.rpy"), encoding="utf-8") as f:
            source = f.read().split("init python:\n", 1)[1].split("\ntransform ", 1)[0]
        tree = ast.parse(textwrap.dedent(source))
        names = {"v2_plain_len", "v2_wrap", "v2_pages", "v2_dialogue_pages", "v2_steps",
                 "v2_current", "v2_line_kind", "v2_do_line", "v2_new_game"}
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
        self.line = next(copy.deepcopy(st) for st, _ in all_steps() if st.get("id") == "MS14_D01_S02_L0015")
        self.shown = []
        self.shown_sizes = []
        self.preference = types.SimpleNamespace(v2_text_size="large")
        self.store = types.SimpleNamespace(v2_stack=[["test", 0, 0]], v2_line_pages=None,
                                          v2_trace=[], v2_met=[], v2_fig="guard", v2_loc="gate")
        self.ns = dict(re=re, store=self.store, persistent=self.preference, V2_DAY=DAY,
                       V2_BLOCKS={"test": [self.line]}, V2_DRAWN=(),
                       v2_stage_band=lambda: None, v2_char=lambda who: who,
                       renpy=types.SimpleNamespace(say=self.say, hide=lambda tag: None))
        exec(compile(ast.Module(body=functions, type_ignores=[]), "engine.rpy", "exec"), self.ns)
        with open(os.path.join(GAME, "screens/style.rpy"), encoding="utf-8") as f:
            source = f.read().split("init python:\n", 1)[1].split("\nstyle ", 1)[0]
        tree = ast.parse(textwrap.dedent(source))
        type_nodes = [node for node in tree.body if
                      (isinstance(node, ast.FunctionDef) and node.name == "v2_type") or
                      (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "V2_TYPE_SCALE" for t in node.targets))]
        exec(compile(ast.Module(body=type_nodes, type_ignores=[]), "style.rpy", "exec"), self.ns)

    def say(self, who, text):
        self.shown.append(text)
        self.shown_sizes.append(self.ns["v2_type"]("display", self.store.v2_line_pages.get("size")))

    def play_rest(self):
        while self.store.v2_stack[0][1] == 0:
            self.ns["v2_do_line"]()

    def test_changing_size_during_first_page_keeps_every_word(self):
        for before, after in (("large", "small"), ("small", "large")):
            with self.subTest(before=before, after=after):
                self.setUp()
                self.preference.v2_text_size = before
                expected = self.ns["v2_pages"](self.line["t"])

                def change_size(who, text):
                    self.say(who, text)
                    self.preference.v2_text_size = after

                self.ns["renpy"].say = change_size
                self.play_rest()
                self.assertEqual(self.shown, expected)
                self.assertEqual(self.shown_sizes, [self.ns["v2_type"]("display", before)] * len(expected))
                self.assertIn("뒤에 기다리는", " ".join(self.shown).replace("\n", " "))
                self.assertIsNone(self.store.v2_line_pages)

    def test_saved_page_bundle_survives_changed_persistent_preference(self):
        expected = self.ns["v2_pages"](self.line["t"])
        self.ns["v2_do_line"]()
        self.assertEqual(self.store.v2_stack[0][2], 1)
        self.store = pickle.loads(pickle.dumps(self.store))
        self.ns["store"] = self.store
        self.preference.v2_text_size = "small"
        self.play_rest()
        self.assertEqual(self.shown, expected)

    def test_old_save_without_bundle_restarts_current_line_without_omission(self):
        del self.store.v2_line_pages
        self.store.v2_stack[0][2] = 1
        self.preference.v2_text_size = "small"
        expected = self.ns["v2_pages"](self.line["t"])
        self.play_rest()
        self.assertEqual(self.shown, expected)

    def test_next_line_uses_new_size(self):
        self.ns["V2_BLOCKS"]["test"].append(copy.deepcopy(self.line))
        self.ns["v2_do_line"]()
        self.preference.v2_text_size = "small"
        self.play_rest()
        self.shown.clear()
        expected = self.ns["v2_pages"](self.line["t"])
        while self.store.v2_stack[0][1] == 1:
            self.ns["v2_do_line"]()
        self.assertEqual(self.shown, expected)

    def test_size_freezes_only_dialogue_until_next_line(self):
        self.preference.v2_text_size = "small"
        self.ns["V2_BLOCKS"]["test"].append(copy.deepcopy(self.line))

        def enlarge(who, text):
            self.say(who, text)
            self.preference.v2_text_size = "large"

        self.ns["renpy"].say = enlarge
        self.play_rest()
        self.assertEqual(set(self.shown_sizes), {28})
        # 설정 등 인자 없는 기존 호출은 새 설정이 바로 적용된다.
        self.assertEqual(self.ns["v2_type"]("body"), 26)
        self.shown_sizes.clear()
        while self.store.v2_stack[0][1] == 1:
            self.ns["v2_do_line"]()
        self.assertEqual(set(self.shown_sizes), {34})

    def test_bundle_without_size_uses_current_preference(self):
        self.ns["v2_dialogue_pages"](self.store.v2_stack[0], self.line)
        del self.store.v2_line_pages["size"]
        self.preference.v2_text_size = "small"
        self.play_rest()
        self.assertEqual(set(self.shown_sizes), {28})

    def test_different_line_cannot_reuse_previous_bundle(self):
        self.ns["v2_dialogue_pages"](self.store.v2_stack[0], self.line)
        other = dict(who="dad", t="다른 줄을 읽는다.")
        self.assertEqual(self.ns["v2_dialogue_pages"]([None, 0, 1, [other]], other), [other["t"]])

    def test_new_game_clears_page_bundle(self):
        self.ns["v2_dialogue_pages"](self.store.v2_stack[0], self.line)
        self.ns["v2_new_game"]()
        self.assertIsNone(self.store.v2_line_pages)


if __name__ == "__main__":
    unittest.main()
