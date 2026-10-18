"""Source/helper regression for Momo's non-prop curator conversation.

Pure Python only. Does not run Ren'Py, render art, or establish visual QA.
"""
import copy
import hashlib
import io
import json
import textwrap
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = "ep6:st_momo_glasses"  # Legacy save/flag identity deliberately retained.
OLD_TITLE = "늘 안경을 품에 넣고 다니시네요"
OLD_REPLY = "제 안경이 아니에요. 첫 겨울에 보호소로 간 동생 거예요."
TITLE = "옛 마을 물건을 모으는 이유가 있나요?"
REPLY = "첫 겨울에 동생이 보호소로 갔어요. 그 애가 살던 마을까지 잊고 싶지는 않았어요."
TAIL = [
    ("resident_momo", "옛 마을 물건이라면 뭐든 산다고들 흉보죠. 사람은 가도 물건은 남으니까, 그거라도 붙잡아 두는 거예요."),
    ("resident_momo", "언젠가 누가 ‘이건 누구 것이었소’ 하고 물어봐 주면 좋겠어요. 그럼 그 이름을 한 번 더 말할 수 있으니까요."),
]
SOURCE = "game/systems/room13_ep_story.rpy"


def load_function(namespace, relative, name):
    lines = (ROOT / "game" / relative).read_text().splitlines(True)
    start = next(i for i, line in enumerate(lines) if line.startswith("    def " + name + "("))
    end = start + 1
    while end < len(lines):
        if lines[end].strip() and not lines[end].startswith("        "):
            break
        end += 1
    exec(compile(textwrap.dedent("".join(lines[start:end])), relative, "exec"), namespace)


def topic_namespace():
    source = (ROOT / SOURCE).read_text()
    block = source.split("init 158 python:\n", 1)[1].split("\nlabel ", 1)[0]
    namespace = dict(ROOM13={"topics": {}}, R13_EVENT_OFFERS={}, R13_OFFER_ACTORS={})
    exec(compile(textwrap.dedent(block), SOURCE, "exec"), namespace)
    return namespace


class MomoPropDialogue(unittest.TestCase):
    def setUp(self):
        self.n = topic_namespace()
        self.topic = self.n["ROOM13"]["topics"][KEY]
        self.rows = self.topic["lines"]

    def test_authored_text_has_no_visible_prop_premise(self):
        self.assertEqual(TITLE, self.topic["title"])
        self.assertEqual([("resident_momo", REPLY)] + TAIL, self.rows)
        self.assertNotIn("안경", self.topic["title"] + "".join(row[1] for row in self.rows))
        self.assertEqual("resident_momo", self.topic["npc"])
        self.assertEqual([2, 12], self.topic["day"])
        self.assertEqual(["st_momo_glasses"], self.topic["flags"])
        for field in ("need", "not_flags", "give"):
            self.assertEqual([], self.topic[field])

    def test_no_expanded_static_or_companion_shadow_variant(self):
        expand = json.loads((ROOT / "game/room13-dialogue-expand.json").read_text())
        self.assertFalse(any(key == KEY or key.startswith(KEY + "#") for key in expand))
        content = json.loads((ROOT / "game/room13-content.json").read_text())
        self.assertNotIn(KEY, content["topics"])
        for relative in ("game/room13-content.json", "game/room13-dialogue-expand.json", "game/room13-dialogue-openings.json", "game/assets/room13-dialogue-beats.json", "game/assets/room13-line-direction.json"):
            text = (ROOT / relative).read_text()
            self.assertNotIn(OLD_TITLE, text)
            self.assertNotIn(OLD_REPLY, text)
        self.n.update(json=json, renpy=types.SimpleNamespace(file=lambda path: io.StringIO((ROOT / "game" / path).read_text()), loadable=lambda path: (ROOT / "game" / path).exists()), r13_conversation_topic_lines=lambda key: self.n["ROOM13"]["topics"][key]["lines"])
        block = (ROOT / "game/systems/room13_dialogue_expand.rpy").read_text().split("init 140 python:\n", 1)[1]
        exec(compile(textwrap.dedent(block), "dialogue_expand", "exec"), self.n)
        self.assertEqual(self.rows, self.n["r13_conversation_topic_lines"](KEY))

    def install_state_helpers(self):
        self.store = types.SimpleNamespace(room13=dict(day=2, period=1, case_state="pending", evidence=["E06"], flags=["existing_flag"], read_topics=[]))
        self.n.update(store=self.store, winter_copy=copy, R13_NAMES={}, R13_TRIAL_DAY=14,
                      r13_has=lambda key: key in self.store.room13["flags"] + self.store.room13["evidence"],
                      r13_topic_current_context=lambda key: None,
                      r13_calendar_key=lambda npc: "momo-regression-calendar")
        def grant(items, source):
            for item in items:
                if item not in self.store.room13["evidence"]:
                    self.store.room13["evidence"].append(item)
        def flag(*items):
            for item in items:
                if item not in self.store.room13["flags"]:
                    self.store.room13["flags"].append(item)
        self.n.update(r13_grant=grant, r13_flag=flag)
        for name in ("r13_available", "r13_finish_topic"):
            load_function(self.n, "room13_rules.rpy", name)
        for name in ("r13_topic_record", "r13_topic_full_record"):
            load_function(self.n, "systems/room13_topic_record.rpy", name)

    def test_availability_boundary_and_case_state_unchanged(self):
        self.install_state_helpers()
        for case_state in ("pending", "occurred", "prevented"):
            for day, expected in ((1, False), (2, True), (12, True), (13, False)):
                self.store.room13.update(day=day, case_state=case_state)
                before = copy.deepcopy(self.store.room13)
                self.assertEqual(expected, self.n["r13_available"](self.topic))
                self.assertEqual(before, self.store.room13)

    def test_finish_repeat_save_roundtrip_preserve_progression(self):
        self.install_state_helpers()
        self.store.r13_topic_shown = self.rows
        self.n["r13_finish_topic"](KEY)
        first = copy.deepcopy(self.store.room13["topic_transcripts"][KEY])
        date = copy.deepcopy(self.store.room13["dialogue_dates"][KEY])
        self.assertEqual(["E06"], self.store.room13["evidence"])
        self.assertEqual(["existing_flag", "st_momo_glasses"], self.store.room13["flags"])
        self.assertEqual([KEY], self.store.room13["read_topics"])
        self.assertEqual((2, 1, "pending"), (self.store.room13["day"], self.store.room13["period"], self.store.room13["case_state"]))
        self.store.room13 = json.loads(json.dumps(self.store.room13))
        for _ in range(2):
            self.store.r13_topic_shown = self.rows
            self.n["r13_finish_topic"](KEY)
        self.assertEqual(first, self.n["r13_topic_record"](KEY))
        self.assertEqual(self.rows, self.n["r13_topic_full_record"](KEY))
        self.assertEqual(date, self.store.room13["dialogue_dates"][KEY])
        before = copy.deepcopy(self.store.room13)
        self.store.r13_topic_shown = self.rows
        self.n["r13_finish_topic"](KEY)
        self.assertEqual(before, self.store.room13)

    def test_legacy_verbatim_record_is_not_silently_rewritten(self):
        self.install_state_helpers()
        old_rows = [("resident_momo", OLD_REPLY)] + TAIL
        old_record = [[who, text, False] for who, text in old_rows]
        self.store.room13.update(read_topics=[KEY], topic_transcripts={KEY: old_record}, dialogue_dates={KEY: {"day": 2, "period": 0}})
        self.store.r13_topic_shown = self.rows
        self.n["r13_finish_topic"](KEY)
        self.assertEqual(old_record, self.n["r13_topic_record"](KEY))
        self.assertEqual(old_rows, self.n["r13_topic_full_record"](KEY))

    def test_review_inventory_and_hash_match_exact_text(self):
        review = json.loads((ROOT / "docs/reviews/dialogue-beats/dynamic-context-review.json").read_text())["rows"]
        inventory = json.loads((ROOT / "docs/reviews/dialogue-beats/dynamic-literal-inventory.json").read_text())
        source_lines = (ROOT / SOURCE).read_text().splitlines()
        for index, (person, text) in enumerate(self.rows):
            matching_reviews = [r for r in review.values() if r["source"] == SOURCE and r["person"] == person and r["text"] == text]
            self.assertEqual(1, len(matching_reviews))
            row = matching_reviews[0]
            self.assertEqual((SOURCE, 22 + index, person, text), (row["source"], row["line"], row["person"], row["text"]))
            self.assertEqual([person, text], row["packet"])
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), row["text_sha256"])
            self.assertIn(text, source_lines[row["line"] - 1])
            self.assertEqual(("anxious", False), (row["emotion"], row["reaction"]))
            matches = [r for r in inventory if r["source"] == SOURCE and r["line"] == row["line"]]
            self.assertEqual(1, len(matches))
            for key in ("source", "line", "person", "text", "packet"):
                self.assertEqual(row[key], matches[0][key])

    def test_exact_context_binding_live_review_record_and_other_routes(self):
        registry = json.loads((ROOT / "game/assets/room13-dialogue-bindings.json").read_text())
        load_function(self.n, "systems/room13_dialogue_bindings.rpy", "r13_bind_dialogue_rows")
        bind = self.n["r13_bind_dialogue_rows"]
        affected = [route for route, spec in registry["routes"].items() if any(registry["cues"][key]["text"] == REPLY for key in spec["cues"])]
        self.assertEqual(11, len(affected))
        for route in affected:
            identity = ("topic:record_full:" if route == "dynamic:664" else "topic:review:" if route == "dynamic:665" else "topic:") + KEY
            result = bind(self.rows, identity, route, registry)
            self.assertEqual([], result["unresolved"], (route, result))
            self.assertEqual({"0", "1", "2"}, set(result["rows"]))
            self.assertTrue(all((row["emotion"], row["reaction"]) == ("anxious", False) for row in result["rows"].values()))
        self.assertFalse(any(row["text"] == OLD_REPLY for row in registry["cues"].values()))

    def test_emotion_already_exists_in_approved_runtime_manifest(self):
        art = json.loads((ROOT / "game/assets/room13-dialogue-talk-art.json").read_text())["people"]["resident_momo"]
        self.assertEqual("approved_runtime", art["status"])
        self.assertTrue(art["profiles"])
        for profile in art["profiles"].values():
            self.assertIn("anxious", profile["frames"])

    def test_registry_is_reproducible_from_review_metadata(self):
        import build_dialogue_bindings
        expected = json.loads((ROOT / "game/assets/room13-dialogue-bindings.json").read_text())
        self.assertEqual(expected, build_dialogue_bindings.compile_registry())


if __name__ == "__main__":
    unittest.main(verbosity=2)
