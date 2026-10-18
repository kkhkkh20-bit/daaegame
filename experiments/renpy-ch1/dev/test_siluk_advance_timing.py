"""Production helpers + authored branch packets. Not a Ren'Py UI/playthrough test.

Pure unittest passed after explicit parent authorization; integrated CI and Ren'Py QA remain required.
"""
import collections.abc
import copy
import json
import textwrap
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = "systems/room13_town_events2.rpy"


def load_function(ns, relative, name):
    lines = (ROOT / "game" / relative).read_text().splitlines(True)
    start = next(i for i, line in enumerate(lines) if line.startswith("    def " + name + "("))
    end = start + 1
    while end < len(lines):
        if lines[end].strip() and not lines[end].startswith("        "):
            break
        end += 1
    exec(compile(textwrap.dedent("".join(lines[start:end])), relative, "exec"), ns)


class SilukAdvanceIntegration(unittest.TestCase):
    def setUp(self):
        self.store = types.SimpleNamespace(room13=dict(day=3, period=0, location="square",
            flags=[], evidence=[], log=[], town={}, read_topics=[], encounters=[],
            case_state="pending", daram_state="with_dad", livelihood=dict(cash=20, ledger=[])))
        self.people = set()
        self.heard = []
        self.n = dict(store=self.store, winter_copy=copy, r13_siluk_abc=collections.abc,
            ROOM13={"topics": {}}, R13_TOPIC_LABELS={}, R13_TRIAL_DAY=10,
            R13_GREETING={"resident_kongi": "", "resident_siluk": ""},
            R13_QUESTION_LEADS={}, R13_OPENING_SCENES={"first_meetings": {}},
            r13_where=lambda who: self.s["location"] if who in self.people else None,
            r13_lines=lambda rows, identity, **kw: self.heard.append((identity, rows)),
            r13_topic_current_fresh=lambda key: False,
            r13_contact_presentations=lambda person: [], r13_met_people=lambda: ["resident_siluk"])
        for file, names in {
            "room13_rules.rpy": ("r13_flag", "r13_has", "r13_time_consequences", "r13_tick", "r13_next_day", "r13_available", "r13_topics", "r13_people"),
            "room13_week2_rules.rpy": ("r13_abs_time",),
            "systems/room13_livelihood_model.rpy": ("r13_wallet",),
            "systems/room13_town_events.rpy": ("r13_cash", "r13_town_set"),
            FILE: ("_ev2_topic", "r13_siluk_advance_record", "r13_siluk_pay_advance", "r13_siluk_advance_notice", "r13_siluk_commit_notice", "r13_siluk_witness_ready", "r13_siluk_commit_witness", "r13_siluk_sync_advance", "r13_siluk_advance_phase", "r13_siluk_record_request"),
            "room13_dialogue_openings_20261013.rpy": ("r13_siluk_advance_greeting", "r13_conversation_opening",),
            "systems/room13_question_discovery.rpy": ("r13_question_discovered", "r13_contact_has_content"),
        }.items():
            for name in names:
                load_function(self.n, file, name)
        self.source = (ROOT / "game" / FILE).read_text()
        # Execute only the actual two production registration lines, not a replica.
        for line in self.source.splitlines():
            if line.strip().startswith(('ROOM13["topics"]["siluk_advance_followup"]=', 'R13_TOPIC_LABELS["siluk_advance_followup"]=')):
                exec(line.strip(), self.n)

    @property
    def s(self):
        return self.store.room13

    def f(self, name, *args, **kwargs):
        return self.n[name](*args, **kwargs)

    def branch(self, label, choice):
        """Run the exact simple authored payment/follow-up branch using real helpers.

        Only Ren'Py's $ and call syntax are translated; there is no replacement
        implementation of money, deadlines, knowledge, or request state.
        """
        region = self.source.split("label " + label + ":\n", 1)[1].split("\nlabel ", 1)[0]
        lines = region.splitlines(True)
        start = next(i for i, line in enumerate(lines) if line.strip().startswith('"' + choice + '"'))
        indent = len(lines[start]) - len(lines[start].lstrip())
        end = start + 1
        while end < len(lines):
            line = lines[end]
            if line.strip() and len(line) - len(line.lstrip()) <= indent:
                break
            end += 1
        body = textwrap.dedent("".join(lines[start + 1:end]))
        py = []
        for line in body.splitlines(True):
            lead = line[:len(line) - len(line.lstrip())]
            plain = line.lstrip()
            if plain.startswith("$ "):
                line = lead + plain[2:]
            elif plain.startswith("call r13_lines("):
                line = lead + plain[5:]
            py.append(line)
        self.n["room13"] = self.s
        self.n["_siluk_phase"] = self.f("r13_siluk_advance_phase")
        exec(compile("".join(py), "authored:" + choice, "exec"), self.n)

    def pay(self, branch="paid"):
        choices = {"paid": "선금 다섯 냥을 준다", "paid_all": "가진 돈을 모두 준다", "follow": "돈을 주고 몰래 뒤를 밟는다"}
        self.branch("r13_ev_a_siluk", choices[branch])

    def test_paid_packet_is_present_tense_and_atomic(self):
        self.pay()
        self.assertEqual((3, 0), (self.s["day"], self.s["period"]))
        self.assertEqual(15, self.f("r13_wallet", self.s)["cash"])
        self.assertEqual([dict(day=3, text="실룩에게 선금", amount=-5)], self.f("r13_wallet", self.s)["ledger"])
        rec = self.f("r13_siluk_advance_record")
        self.assertEqual((3, 0, 3, "sunset", 10, "pending"), tuple(rec[k] for k in ("payment_day", "payment_period", "due_day", "due_kind", "due_abs", "status")))
        self.assertEqual("ev:a:paid", self.heard[-1][0])
        self.assertEqual([("resident_siluk", "해 지기 전에 짐 가지고 올게요. 걱정 마세요."), (None, "실룩은 선금을 챙겨 자리를 떠났다.")], self.heard[-1][1])
        self.assertNotIn("siluk_scammed", self.s["flags"])
        self.assertNotIn("know_siluk_debt", self.s["flags"])
        self.assertIsNone(self.f("r13_siluk_advance_notice"))

    def test_duplicate_payment_and_reload_do_not_charge_again(self):
        self.pay()
        self.store.room13 = json.loads(json.dumps(self.s))
        before = copy.deepcopy(self.s)
        for branch in ("paid", "follow", "paid_all"):
            self.assertFalse(self.f("r13_siluk_pay_advance", branch))
        self.pay()
        self.assertEqual(before, self.s)

    def test_real_clock_helpers_reach_sunset_then_next_day(self):
        self.pay()
        self.f("r13_tick")
        self.assertIsNone(self.f("r13_siluk_advance_notice"))
        self.f("r13_tick")
        self.assertEqual("sunset", self.f("r13_siluk_advance_notice"))
        self.assertTrue(self.f("r13_siluk_commit_notice", "sunset"))
        self.assertEqual("overdue", self.f("r13_siluk_advance_record")["status"])
        self.assertFalse(self.f("r13_siluk_commit_notice", None))
        self.assertIsNone(self.f("r13_siluk_advance_notice"))
        self.f("r13_next_day")
        self.assertEqual("next_day", self.f("r13_siluk_advance_notice"))
        self.f("r13_siluk_commit_notice", "next_day")
        before = copy.deepcopy(self.s)
        self.assertIsNone(self.f("r13_siluk_advance_notice"))
        self.assertEqual(before, self.s)

    def test_paid_all_preserves_amount_and_end_of_day(self):
        self.s["livelihood"]["cash"] = 3
        self.pay("paid_all")
        self.assertEqual(0, self.f("r13_wallet", self.s)["cash"])
        self.assertEqual(3, self.f("r13_siluk_advance_record")["amount"])
        self.s["period"] = 3
        self.assertIsNone(self.f("r13_siluk_advance_notice"))
        self.f("r13_next_day")
        self.assertEqual("late", self.f("r13_siluk_advance_notice"))
        self.assertNotIn("know_siluk_debt", self.s["flags"])

    def test_payment_bounds_and_query_purity(self):
        self.s["livelihood"]["cash"] = 4
        for branch in ("paid", "follow"):
            before = copy.deepcopy(self.s)
            self.assertFalse(self.f("r13_siluk_pay_advance", branch))
            self.assertEqual(before, self.s)
        self.pay("paid_all")
        before = copy.deepcopy(self.s)
        for name in ("r13_siluk_advance_record", "r13_siluk_advance_phase", "r13_siluk_advance_notice", "r13_siluk_witness_ready", "r13_siluk_advance_greeting"):
            self.f(name)
        self.assertEqual(before, self.s)

    def test_skipped_days_do_not_claim_yesterday_or_duplicate_notices(self):
        self.pay()
        self.s.update(day=6, period=0)
        self.assertEqual("late", self.f("r13_siluk_advance_notice"))
        self.f("r13_siluk_commit_notice", "late")
        self.assertIsNone(self.f("r13_siluk_advance_notice"))
        self.people.add("resident_kongi")
        self.assertTrue(self.f("r13_siluk_witness_ready"))
        self.assertNotEqual(self.s["day"], self.f("r13_siluk_advance_record")["payment_day"] + 1)
        self.assertIn('"ev:a:witness:later"', self.source)

    def test_follow_immediate_observation_not_early_non_delivery(self):
        self.pay("follow")
        self.assertEqual("end_of_day", self.f("r13_siluk_advance_record")["due_kind"])
        self.assertIn("know_siluk_debt", self.s["flags"])
        self.assertIn("know_madam_hoard", self.s["flags"])
        self.assertNotIn("siluk_scammed", self.s["flags"])
        self.assertIn("이번 주 이자", self.heard[-1][1][1][1])

    def test_legacy_same_text_cannot_distinguish_paid_and_follow(self):
        self.f("r13_cash", -5, "실룩에게 선금")
        self.s["flags"].append("siluk_scammed")  # legacy buggy flag is not a clock
        before = copy.deepcopy(self.s)
        self.assertEqual("unknown", self.f("r13_siluk_advance_phase"))
        self.assertEqual("unknown", self.f("r13_siluk_advance_notice"))
        self.assertIsNone(self.f("r13_siluk_advance_record")["due_abs"])
        self.assertEqual(before, self.s)
        self.f("r13_siluk_sync_advance")
        self.assertIn("siluk_advance_paid", self.s["flags"])
        self.assertFalse(self.f("r13_siluk_pay_advance", "paid"))
        self.f("r13_siluk_commit_notice", "unknown")
        self.s["day"] = 9
        self.assertIsNone(self.f("r13_siluk_advance_notice"))
        self.assertEqual("unknown", self.f("r13_siluk_advance_phase"))

    def test_legacy_paid_all_unique_day_can_restore_end_of_day(self):
        self.f("r13_cash", -3, "실룩에게 선금(가진 돈 전부)")
        self.assertEqual("pending", self.f("r13_siluk_advance_phase"))
        self.s.update(day=4, period=0)
        self.assertEqual("late", self.f("r13_siluk_advance_notice"))
        self.assertIsNone(self.f("r13_siluk_advance_record")["payment_period"])

    def test_legacy_refusal_missing_duplicate_or_future_dates(self):
        self.s["flags"] = ["ev_a_done"]
        self.assertIsNone(self.f("r13_siluk_advance_record"))
        self.s["flags"].append("siluk_scammed")
        self.assertEqual("unknown", self.f("r13_siluk_advance_phase"))
        for ledger in ([dict(day=9,text="실룩에게 선금(가진 돈 전부)",amount=-3)],
                       [dict(day=3,text="실룩에게 선금(가진 돈 전부)",amount=-3)] * 2):
            self.s["livelihood"]["ledger"] = ledger
            self.assertEqual("unknown", self.f("r13_siluk_advance_phase"))

    def test_witness_requires_next_day_and_actual_colocation(self):
        self.pay()
        self.people.add("resident_kongi")
        self.assertFalse(self.f("r13_siluk_witness_ready"))
        self.f("r13_next_day")
        self.people.clear()
        self.assertFalse(self.f("r13_siluk_witness_ready"))
        self.people.add("resident_kongi")
        self.assertTrue(self.f("r13_siluk_witness_ready"))
        self.assertTrue(self.f("r13_siluk_commit_witness"))
        self.assertFalse(self.f("r13_siluk_witness_ready"))
        self.assertNotIn("know_siluk_debt", self.s["flags"])
        self.assertIn('if room13["day"]==r13_siluk_advance_record()["payment_day"]+1:', self.source)
        self.assertNotIn('선금을 주신 날', self.source)

    def test_recontact_menu_and_greeting_use_paid_state(self):
        self.pay()
        topics = dict(self.f("r13_topics", "resident_siluk"))
        self.assertIn("siluk_advance_followup", topics)
        self.assertTrue(self.f("r13_question_discovered", "siluk_advance_followup", topics["siluk_advance_followup"]))
        self.assertTrue(self.f("r13_contact_has_content", "resident_siluk"))
        before = copy.deepcopy(self.s)
        greeting = self.f("r13_conversation_opening", "resident_siluk", True)
        self.assertIn("선금은 받았습니다", greeting[0][1])
        self.assertEqual(before, self.s)
        self.branch("r13_siluk_advance_followup", "맡긴 짐은 어디까지 확인하셨습니까?")
        self.assertEqual("pending", self.f("r13_siluk_advance_record")["status"])
        self.assertTrue(self.f("r13_contact_has_content", "resident_siluk"))
        self.assertEqual([], self.s["read_topics"])
        self.s["period"] = 2
        self.assertIn("아직 가져오지 못했어요", self.f("r13_conversation_opening", "resident_siluk", False)[0][1])

    def test_confront_refund_delivery_are_live_no_money_or_evidence_duplication(self):
        self.pay()
        self.assertFalse(self.f("r13_siluk_record_request", "refund"))
        self.s["period"] = 2
        wallet = copy.deepcopy(self.f("r13_wallet", self.s))
        for choice, request in (("약속한 때가 지났습니다. 어떻게 된 겁니까?", "explain"),
                                ("짐을 못 가져오셨으면 선금을 돌려주세요.", "refund"),
                                ("선금은 드렸으니 부탁한 짐을 가져와 주세요", "deliver")):
            self.assertLessEqual(len(choice), 24)
            for _ in range(2):
                self.branch("r13_siluk_advance_followup", choice)
                rec = self.f("r13_siluk_advance_record")
                self.assertEqual(("confronted", request), (rec["status"], rec["last_request"]))
                self.assertEqual(wallet, self.f("r13_wallet", self.s))
                self.assertEqual([], self.s["evidence"])
        self.assertEqual(1, self.s["flags"].count("know_siluk_debt"))
        self.assertNotEqual("resolved", self.f("r13_siluk_advance_record")["status"])
        self.f("r13_siluk_commit_notice", "sunset")
        self.assertEqual("confronted", self.f("r13_siluk_advance_record")["status"])

    def test_debt_alternatives_remain_reachable_before_payment(self):
        for choice in ("짐을 받아 오면 돈을 주겠다고 한다", "바둑이를 불러 증인으로 세운다"):
            self.s["flags"] = ["badook_doubt"] if choice.startswith("바둑이") else []
            if choice.startswith("바둑이"):
                self.assertIn('"바둑이를 불러 증인으로 세운다" if r13_has("badook_doubt") or r13_has("badook_ally"):', self.source)
                self.assertTrue(self.f("r13_has", "badook_doubt"))
            before = copy.deepcopy(self.f("r13_wallet", self.s))
            self.branch("r13_ev_a_siluk", choice)
            self.assertIn("know_siluk_debt", self.s["flags"])
            self.assertEqual(before, self.f("r13_wallet", self.s))
            self.assertTrue(self.n["_ep_loop"])
        self.assertIn('if r13_has("know_siluk_debt") or r13_has("know_madam_hoard"):', self.source)

    def test_resolved_state_never_resets_to_unfamiliar_or_recharges(self):
        self.pay()
        rec = self.f("r13_siluk_advance_record")
        rec.update(status="resolved", resolution="externally_verified")
        self.f("r13_town_set", siluk_advance=rec)
        self.s["day"] = 5
        self.assertIsNone(self.f("r13_siluk_advance_notice"))
        self.assertFalse(self.f("r13_siluk_record_request", "refund"))
        self.assertFalse(self.f("r13_siluk_pay_advance", "paid"))
        self.assertIn("그때 맡기신 짐", self.f("r13_conversation_opening", "resident_siluk", True)[0][1])
        self.assertEqual(15, self.f("r13_wallet", self.s)["cash"])

    def test_authored_routes_are_wired_before_one_time_offer(self):
        label = self.source.split("label r13_town_events2:\n", 1)[1].split("\nlabel ", 1)[0]
        self.assertLess(label.index("call r13_siluk_advance_events"), label.index('room13["day"]==3'))
        self.assertEqual("r13_siluk_advance_followup", self.n["R13_TOPIC_LABELS"]["siluk_advance_followup"])
        followup = self.source.split("label r13_siluk_advance_followup:", 1)[1].split("\nlabel ", 1)[0]
        self.assertNotIn("r13_cash(", followup)
        self.assertNotIn("r13_finish_topic", followup)
        self.assertNotIn("r13_grant(", followup)
        self.assertIn('$ r13_note_encounter("resident_siluk")', self.source)


if __name__ == "__main__":
    unittest.main()
