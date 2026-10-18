"""Actual cross-layer dialogue-state helpers; no Ren'Py UI/playthrough claim.

The old discovery fixture remains isolated. Here the production topic helpers,
base finish function, Daram finish wrapper, and contact decision share one store.
"""
import copy
import json
import textwrap
import types
import unittest
from pathlib import Path
import test_daram_home as home_fixture

ROOT = Path(__file__).resolve().parents[1]


def load_function(ns, relative, name):
    lines = (ROOT / "game" / relative).read_text().splitlines(True)
    start = next(i for i, line in enumerate(lines)
                 if line.startswith("    def " + name + "("))
    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line.strip() and not line.startswith("        "):
            break
        end += 1
    exec(compile(textwrap.dedent("".join(lines[start:end])), relative, "exec"), ns)


class DialogueStateIntegration(unittest.TestCase):
    def setUp(self):
        fixture = home_fixture.HomeTest()
        fixture.setUp()
        self.n = fixture.ns
        self.store = self.n["store"]
        self.n["R13_WEEK2_DAY"] = 11
        self.n["R13_NAMES"] = {}
        self.n["r13_has"] = lambda key: key in self.s["flags"] + self.s["evidence"]
        self.n["r13_calendar_key"] = lambda person: "test-calendar"
        self.n["r13_grant"] = self.grant
        self.n["r13_flag"] = self.flag
        # Replace only the fixture's bottom finish stub with the real production
        # function; retain the real init101 wrapper already installed by fixture.
        home_finish = self.n["r13_finish_topic"]
        load_function(self.n, "room13_rules.rpy", "r13_finish_topic")
        self.n["_r13_daram_home_finish"] = self.n["r13_finish_topic"]
        self.n["r13_finish_topic"] = home_finish
        record = (ROOT / "game/systems/room13_topic_record.rpy").read_text()
        block = record.split("init 130 python:\n", 1)[1].split("\nlabel ", 1)[0]
        exec(compile(textwrap.dedent(block), "topic_record", "exec"), self.n)
        # Actual contact decision, with unrelated first-meeting/presentation routes
        # inert so a fresh live topic is the only possible entry reason.
        load_function(self.n, "systems/room13_question_discovery.rpy", "r13_contact_has_content")
        self.n["r13_contact_presentations"] = lambda person: []
        self.n["r13_met_people"] = lambda: ["daram", "granny", "nabi"]
        content = json.loads((ROOT / "game/room13-content.json").read_text())
        for key in ("nabi_alibi", "nabi_gap"):
            self.n["ROOM13"]["topics"][key] = copy.deepcopy(content["topics"][key])
        self.n["ROOM13"]["topics"]["mystery:door"] = dict(
            npc="granny", give=[], flags=[], lines=[("granny", "문은 하나뿐이에요.")])
        self.store.r13_topic_shown = None

    @property
    def s(self):
        return self.store.room13

    def grant(self, keys, source):
        for key in keys:
            if key not in self.s["evidence"]:
                self.s["evidence"].append(key)

    def flag(self, *keys):
        for key in keys:
            if key not in self.s["flags"]:
                self.s["flags"].append(key)

    def rows(self, key):
        if self.n["r13_topic_current_context"](key) is not None:
            return self.n["r13_topic_current_lines"](key)
        return self.n["ROOM13"]["topics"][key]["lines"]

    def finish(self, key):
        self.store.r13_topic_shown = self.rows(key)
        self.n["r13_finish_topic"](key)

    def text(self, rows):
        return "\n".join(row[1] for row in rows)

    def test_daram_current_dispatch_and_period_contact(self):
        key = "home:daram:rest"
        self.finish(key)
        first = copy.deepcopy(self.s["topic_transcripts"][key])
        date = copy.deepcopy(self.s["dialogue_dates"][key])
        self.assertFalse(self.n["r13_contact_has_content"]("daram"))
        self.s["period"] = 1
        before = copy.deepcopy(self.s)
        self.assertTrue(self.n["r13_contact_has_content"]("daram"))
        rows = self.rows(key)
        self.assertIn("마차", self.text(rows))
        self.assertEqual(before, self.s)  # query and preview cannot mark read
        self.finish(key)
        self.assertFalse(self.n["r13_topic_current_fresh"](key))
        self.assertEqual(first, self.s["topic_transcripts"][key])
        self.assertEqual(date, self.s["dialogue_dates"][key])
        self.assertEqual([], self.s["evidence"])
        self.assertEqual((2, 1), (self.s["day"], self.s["period"]))
        script = (ROOT / "game/room13.rpy").read_text()
        self.assertIn('r13_topic in room13["read_topics"] and r13_topic_current_context(r13_topic) is None', script)
        self.assertIn('r13_topic_rows=r13_topic_current_lines(r13_topic)', script)

    def test_daram_new_evidence_and_reunion_are_not_archived_answers(self):
        self.s["evidence"] = ["J04"]
        self.finish("home:daram:packet")
        self.s["evidence"].append("J05")
        self.assertTrue(self.n["r13_topic_current_fresh"]("home:daram:packet"))
        self.assertIn("까로", self.text(self.rows("home:daram:packet")))
        self.s["evidence"].append("M01")
        self.finish("home:daram:mother")
        old = copy.deepcopy(self.s["topic_transcripts"]["home:daram:mother"])
        self.s.update(day=11, mom_state="reunited")
        self.assertIn("엄마 얼굴을 봤으니까", self.text(self.rows("home:daram:mother")))
        self.finish("home:daram:mother")
        self.assertEqual(old, self.s["topic_transcripts"]["home:daram:mother"])

    def test_granny_acknowledgement_preserves_original_not_current_denial(self):
        key = "mystery:door"
        self.finish(key)
        first = copy.deepcopy(self.s["topic_transcripts"][key])
        self.flag("inn_claim_retracted")
        before = copy.deepcopy(self.s)
        self.assertTrue(self.n["r13_topic_current_fresh"](key))
        self.assertTrue(self.n["r13_contact_has_content"]("granny"))
        self.assertIn("세탁물", self.text(self.rows(key)))
        self.assertEqual(before, self.s)
        self.finish(key)
        self.assertFalse(self.n["r13_topic_current_fresh"](key))
        self.assertEqual(first, self.s["topic_transcripts"][key])
        self.assertIn("세탁물", self.text(self.rows(key)))

    def test_nabi_gap_first_never_fabricates_j09(self):
        self.s["case_state"] = "occurred"
        self.finish("nabi_gap")
        self.assertIn("E12", self.s["evidence"])
        self.assertIn("그때부터는 못 봤어요", self.text(self.rows("nabi_alibi")))
        self.finish("nabi_alibi")
        self.assertIn("E15", self.s["evidence"])
        self.assertNotIn("J09", self.s["evidence"])
        self.finish("nabi_alibi")  # first repeat legitimately changes dialogue_views to followup
        before = copy.deepcopy(self.s)
        self.finish("nabi_alibi")
        self.assertEqual(before, self.s)

    def test_nabi_first_statement_kept_after_correction_and_save_copy(self):
        self.s["case_state"] = "occurred"
        self.finish("nabi_alibi")
        first = copy.deepcopy(self.s["topic_transcripts"]["nabi_alibi"])
        self.assertIn("J09", self.s["evidence"])
        self.finish("nabi_gap")
        self.assertTrue(self.n["r13_topic_current_fresh"]("nabi_alibi"))
        self.finish("nabi_alibi")
        self.store.room13 = json.loads(json.dumps(self.s))
        self.assertFalse(self.n["r13_topic_current_fresh"]("nabi_alibi"))
        self.assertEqual(first, self.s["topic_transcripts"]["nabi_alibi"])
        self.assertIn("J09", self.s["evidence"])
        self.s.pop("current_topic_contexts")
        before = copy.deepcopy(self.s)
        self.assertTrue(self.n["r13_topic_current_fresh"]("nabi_alibi"))
        self.assertEqual(before, self.s)  # old save query does not migrate facts

    def test_doto_case_guard_owned_records_and_repeat(self):
        self.n["_r13_tm_present"] = lambda *args: [("doto", "기본 답변")]
        load_function(self.n, "systems/room13_testimony.rpy", "r13_present")
        for state in ("pending", "prevented", "occurred"):
            for key in ("E04", "E05", "E37"):
                self.s.update(case_state=state, evidence=[key], flags=[])
                self.n["r13_present"]("doto", key)
                self.assertEqual(state == "occurred", "J10" in self.s["evidence"])
                before = copy.deepcopy(self.s)
                self.n["r13_present"]("doto", key)
                self.assertEqual(before, self.s)
        self.s.update(case_state="occurred", evidence=[], flags=[])
        self.n["r13_present"]("doto", "E37")
        self.assertNotIn("J10", self.s["evidence"])


class C2BoundedArgument(unittest.TestCase):
    def setUp(self):
        source = (ROOT / "game/systems/room13_debate.rpy").read_text()
        block = source.split("init 98 python:\n", 1)[1].split("\nlabel ", 1)[0]
        self.store = types.SimpleNamespace(room13=dict(
            propositions=[], flags=[], evidence=[], finale_started=False))
        self.n = dict(store=self.store, winter_copy=copy, R13_NAMES={},
                      r13_has=lambda key: key in self.store.room13["flags"] + self.store.room13["evidence"])
        exec(compile(textwrap.dedent(block), "debate", "exec"), self.n)

    def test_original_gates_and_specific_evidence_rewards(self):
        judge = self.n["r13_debate_judge"]
        self.store.room13["evidence"] = ["E06", "E08", "E07", "E35", "E09", "E10"]
        e06 = judge("C2", "s1", "E06")
        e08 = judge("C2", "s1", "E08")
        self.assertEqual("break", e06[0])
        self.assertEqual("break", e08[0])
        self.assertNotEqual(e06[1], e08[1])
        self.assertIn("정할 수 없습니다", str(e08[1]))
        self.assertEqual("soft", judge("C2", "s2", "E07")[0])
        self.assertEqual("break", judge("C2", "s2", "E35")[0])
        self.assertEqual("soft", judge("C2", "s3", "E10")[0])
        self.store.room13["flags"] = ["bami_consent"]
        self.assertEqual("break", judge("C2", "s3", "E10")[0])
        e09 = judge("C2", "s3", "E09")
        self.assertEqual("break", e09[0])
        self.assertNotIn("침대", str(e09[1]))
        self.assertIn("범인을 정하지 않겠습니다", str(e09[1]))
        self.assertIsNone(self.n["r13_debate_counter"]("C2", "s3"))
        self.store.room13["propositions"] = ["C1"]
        counter = self.n["r13_debate_counter"]("C2", "s3")
        self.assertIn("미리 레버", str(counter["correct"]))
        c2 = self.n["R13_DEBATE"]["C2"]
        self.assertEqual(["s1", "s2", "s3"], [s["id"] for s in c2["statements"]])
        self.assertTrue(all(not s.get("hidden") for s in c2["statements"]))
        self.assertEqual(["correct", "over", "weak"], [k for k, _ in c2["conclusion"]["options"]])
        self.assertIn("근거는 무너졌다", c2["conclusion"]["options"][0][1])
        for rows in [e06[1], e08[1], e09[1], counter["correct"], c2["conclusion"]["correct"]]:
            self.assertTrue(all(not (r[0] == "dad" and len(r) > 2 and "expression" in r[2]) for r in rows))


if __name__ == "__main__":
    unittest.main()
