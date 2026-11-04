"""초회 정보와 질문·제출 이력에 맞는 1일 대사·진행의 회귀시험."""
import itertools
import copy
import unittest

from engine_sim import EngineSim


def submissions(evidence):
    for count in range(1, len(evidence) + 1):
        yield from itertools.combinations(evidence, count)


class Day01Logic(unittest.TestCase):
    def test_gate_resolves_only_the_missing_companion_name(self):
        sim = EngineSim()
        sim.investigate()
        evidence = sim.ns["V2_EVIDENCE"]
        self.assertNotIn("다람", evidence["E02"]["text"])
        self.assertIn("다람", evidence["E03"]["text"])
        claim = sim.ns["V2_PROOFS"]["gate"]["quote"]["t"]
        self.assertIn("다람", claim)
        self.assertRegex(claim, r"이름.*없")
        # 다른 직업 문제를 함께 내지 않고, 빠진 이름을 확인해 추가하는 결과로 닫는다.
        for line in sim.lines:
            self.assertNotRegex(line["t"], r"일꾼|장작 운반")
        sim.lines.clear()
        sim.call("v2_present_to", "guard", "E01")
        self.assertEqual(sim.drain(), "ui")
        replies = " ".join(line["t"] for line in sim.lines if line["who"] == "guard")
        self.assertIn("다람", replies)
        self.assertNotRegex(replies, r"묵을 곳|숙소|일꾼")
        sim.dismiss_topics()
        self.assertFalse(sim.store.v2_vals.get("gate_daram_listed"))
        self.assertEqual(sim.submit_gate(("E02", "E03")), "wait")
        self.assertTrue(sim.store.v2_vals.get("gate_daram_listed"))
        self.assertIn("E05", sim.store.v2_ev)
        self.assertRegex(evidence["E05"]["text"], r"다람.*추가")

    def test_pilot3_saved_frames_still_point_to_the_same_dialogue(self):
        # 이전 공개판 저장에 들어가는 실제 묶음·순번이다. 조건 문구를 넣어도 순번을 밀지 않는다.
        positions = (
            ("n:registered", 18, "MS14_D01_S04_L0012"),
            ("n:room_compare/8/then", 0, "NW_D01_SR01"),
            ("g:gate_investigate/0/4/then", 4, "NW_D01_S03_B01"),
            ("g:note_pick/0", 5, "MS14_D01_S05_L0020"),
            ("p:gate/o0/0/then", 5, "MS14_D01_S03_L0017"),
            ("p:gate/o1", 1, "MS14_D01_S03_L0024"),
            ("p:letters/spot:head", 1, "NW_D01_OB05"),
        )
        sim = EngineSim()
        sim.store.v2_vals["purpose_difference_known"] = True
        for block, index, ident in positions:
            with self.subTest(block=block, index=index):
                sim.store.v2_stack = [[block, index, 1]]
                sim.store.v2_line_pages = dict(key=(block, index, "이전 판 문구"),
                                               pages=["저장 당시 쪽"], size="normal")
                frame, step = sim.call("v2_current")
                self.assertEqual(step["id"], ident)
                pages = sim.call("v2_dialogue_pages", frame, step)
                self.assertEqual(frame[2], 0)
                self.assertNotEqual(pages, ["저장 당시 쪽"])

    def registered(self):
        sim = EngineSim()
        sim.investigate()
        self.assertEqual(sim.submit_gate(("E02", "E03")), "wait")
        self.assertTrue(sim.store.v2_vals.get("gate_registered"))
        return sim

    def test_gate_answer_is_unchanged_for_all_fifteen_submissions(self):
        for rules in (False, True):
            sim = EngineSim()
            sim.investigate(rules)
            proof = sim.ns["V2_PROOFS"]["gate"]
            for chosen in submissions(("E01", "E02", "E03", "E04")):
                with self.subTest(rules=rules, chosen=chosen):
                    self.assertEqual(sim.call("v2_proof_won", proof, chosen),
                                     {"E02", "E03"} <= set(chosen))

    def test_every_owned_submission_reaches_the_expected_gate_result(self):
        for rules in (False, True):
            available = ("E01", "E02", "E03", "E04") if rules else ("E01", "E02", "E03")
            for chosen in submissions(available):
                with self.subTest(rules=rules, chosen=chosen):
                    sim = EngineSim()
                    sim.investigate(rules)
                    self.assertEqual(sim.submit_gate(chosen), "wait")
                    won = {"E02", "E03"} <= set(chosen)
                    self.assertEqual(bool(sim.store.v2_vals.get("gate_basis_proven")), won)
                    self.assertEqual(bool(sim.store.v2_vals.get("gate_registered")), won)
                    self.assertEqual(sim.store.v2_gate, "registered_menu" if won else "gate_investigate")

    def test_wrong_submission_without_rules_does_not_claim_missing_documents(self):
        sim = EngineSim()
        sim.investigate()
        self.assertEqual(set(sim.store.v2_ev), {"E01", "E02", "E03"})
        for _ in range(3):
            sim.lines.clear()
            self.assertEqual(sim.submit_gate(("E03",)), "wait")
            hint = " ".join(line["t"] for line in sim.lines if line["who"] == "dad")
            self.assertTrue(hint)
            self.assertNotRegex(hint, r"확인하지 않은 서류|서류가 더|아직.*(?:읽지|안 읽)|자료.*부족")
            self.assertNotIn("E04", sim.store.v2_ev)
            self.assertFalse(sim.store.v2_vals.get("gate_basis_proven"))

    def test_acknowledged_difference_is_remembered_in_partial_submission_reply(self):
        for rules, chosen in ((False, ("E03",)), (True, ("E03",)), (True, ("E03", "E04"))):
            with self.subTest(rules=rules, chosen=chosen):
                sim = EngineSim()
                sim.investigate(rules)
                self.assertEqual(sim.option("gate_investigate", 3), "ui")
                sim.dismiss_topics()
                self.assertTrue(sim.store.v2_vals.get("purpose_difference_known"))
                sim.lines.clear()
                before = copy.deepcopy(sim.ns["V2_DAY"])
                self.assertEqual(sim.submit_gate(chosen), "wait")
                replies = [line for line in sim.lines if line.get("id") in
                           ("MS14_D01_S03_L0024", "MS14_D01_S03_L0025") and line["who"] == "guard"]
                self.assertTrue(replies)
                self.assertRegex(" ".join(line["t"] for line in replies), r"(?:말한|말씀한).*차이|차이.*(?:알겠|알고|확인)")
                self.assertNotRegex(" ".join(line["t"] for line in replies), r"어디가.*다르")
                # 조건 대사를 읽어도 원문과 등록된 단계 목록 자체를 덮어쓰지 않는다.
                self.assertEqual(sim.ns["V2_DAY"], before)

    def test_registered_guard_acknowledges_completed_registration_for_old_documents(self):
        for evidence in ("E01", "E02", "E03", "E05"):
            with self.subTest(evidence=evidence):
                sim = self.registered()
                sim.lines.clear()
                sim.call("v2_click_person", "guard")
                sim.call("v2_present_to", "guard", evidence)
                sim.drain()
                reply = " ".join(line["t"] for line in sim.lines if line["who"] == "guard")
                self.assertTrue(reply)
                self.assertRegex(reply, r"등록|정정|고쳤|고친|마쳤|들어가|올렸|추가")
                self.assertNotRegex(reply, r"확인이 안|원본도 마저|묵을 곳도 봐야")
                self.assertTrue(sim.store.v2_vals.get("gate_registered"))

    def test_reason_followup_starts_unread_and_disappears_after_reason_is_known(self):
        sim = EngineSim()
        sim.investigate()
        row = next(row for row in sim.call("v2_topics", "guard") if row["key"] == ("follow", "F002"))
        self.assertFalse(row["read"])
        self.assertEqual(sim.option("gate_investigate", 3), "ui")
        sim.dismiss_topics()
        self.assertEqual(sim.option("gate_investigate", 5), "ui")
        sim.dismiss_topics()
        self.assertTrue(sim.store.v2_vals.get("reason_heard"))
        self.assertNotIn(("follow", "F002"), [row["key"] for row in sim.call("v2_topics", "guard")])

    def test_registration_alone_hides_old_reason_followup(self):
        sim = self.registered()
        self.assertFalse(sim.store.v2_vals.get("reason_heard"))
        self.assertNotIn(("follow", "F002"), [row["key"] for row in sim.call("v2_topics", "guard")])

    def test_granny_does_not_send_player_to_search_the_room_again(self):
        sim = self.registered()
        self.assertEqual(sim.option("registered_menu", 1), "wait")
        self.assertEqual(sim.option("to_room13", 0), "wait")
        self.assertEqual(sim.option("note_pick", 0), "wait")
        self.assertEqual(sim.option("bundle_open", 0), "proof")
        self.assertTrue(sim.store.v2_vals.get("under_desk_checked"))
        sim.call("v2_proof_prepare", "letters")
        sim.call("v2_proof_result", ("submit", ["E01", "E06"]))
        self.assertEqual(sim.drain(), "menu")
        sim.call("v2_menu_choose", 1)
        self.assertEqual(sim.drain(), "wait")
        self.assertEqual(sim.option("to_inn", 0), "wait")
        self.assertEqual(sim.store.v2_loc, "inn")
        sim.lines.clear()
        sim.call("v2_click_person", "granny")
        sim.call("v2_present_to", "granny", "E01")
        sim.drain()
        reply = " ".join(line["t"] for line in sim.lines if line["who"] == "granny")
        self.assertTrue(reply)
        self.assertNotRegex(reply, r"우선 올라가|다시.*(?:찾아|뒤져|살펴)")
        self.assertRegex(reply, r"방.*그대로")
        self.assertTrue(sim.store.v2_vals.get("under_desk_checked"))

    def test_acorn_habit_is_known_before_comparison_and_both_night_routes_finish(self):
        for observe_tail, night_path in itertools.product((False, True), (0, 1)):
            with self.subTest(observe_tail=observe_tail, night_path=night_path):
                sim = self.registered()
                self.assertEqual(sim.option("registered_menu", 1), "wait")
                self.assertEqual(sim.option("to_room13", 0), "wait")
                self.assertEqual(sim.option("note_pick", 0), "wait")
                habit = next(line for line in sim.lines if line.get("id") == "MS14_D01_S05_L0020")
                self.assertIn("도토리", habit["t"])
                self.assertRegex(habit["t"], r"엄마|아내")
                self.assertRegex(habit["t"], r"마다|늘|언제나|항상|맨날|습관")
                self.assertNotIn("NW_D01_OB04", sim.line_ids())
                self.assertEqual(sim.option("bundle_open", 0), "proof")
                self.assertTrue(sim.store.v2_vals.get("under_desk_checked"))
                sim.call("v2_proof_prepare", "letters")
                if observe_tail:
                    sim.call("v2_toggle_pick", "E01")
                    sim.call("v2_toggle_pick", "E06")
                    self.assertTrue(sim.call("v2_pair_ready", "letters"))
                    sim.store.v2_pair = True
                    sim.call("v2_proof_result", ("observe", "tail"))
                    self.assertEqual(sim.drain(), "proof")
                    self.assertTrue(sim.store.v2_vals.get("letter_tail_observed"))
                    sim.store.v2_pair = False
                sim.call("v2_proof_result", ("submit", ["E01", "E06"]))
                self.assertEqual(sim.drain(), "menu")
                self.assertEqual(bool(sim.store.v2_vals.get("letter_tail_observed")), observe_tail)
                self.assertEqual("NW_D01_SR01" in sim.line_ids(), not observe_tail)
                sim.call("v2_menu_choose", night_path)
                if night_path == 1:
                    self.assertEqual(sim.drain(), "wait")
                    self.assertEqual(sim.store.v2_gate, "to_inn")
                    self.assertEqual(sim.option("to_inn", 0), "wait")
                    self.assertEqual(sim.store.v2_gate, "to_room13_night")
                    self.assertEqual(sim.option("to_room13_night", 0), "wait")
                else:
                    self.assertEqual(sim.drain(), "wait")
                self.assertEqual(sim.store.v2_gate, "sleep1")
                self.assertLess(sim.line_ids().index("MS14_D01_S05_L0037"),
                                sim.line_ids().index("MS14_D01_S05_L0042"))
                self.assertIsNone(sim.option("sleep1", 0))
                self.assertEqual(sim.persistent.v2_last_end["vals"]["day"], 2)


if __name__ == "__main__":
    unittest.main()
