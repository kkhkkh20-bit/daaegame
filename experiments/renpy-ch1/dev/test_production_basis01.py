"""D01 input/branch and save-state tests; these do not claim Ren'Py execution."""
import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("production_basis01_test", ROOT / "game/python-packages/production_basis01.py")
pb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pb)
DATA = json.loads((ROOT / "game/production-basis01-d01.json").read_text())
BLOCKS = {b["id"]: b for s in DATA["scenes"] for b in s["blocks"]}


def run_block(state, key, ids=None):
    block = BLOCKS[pb.PREFIX + key]
    if not pb.allowed(state, block["id"]): raise ValueError("Guard rejected")
    for record in block["records"]:
        if record["kind"] != "choice" and (ids is None or record["id"] in ids):
            state = pb.commit_record(state, block, record)
    return state


def arrive(letter="close_letter", invitation="request_original"):
    state = pb.new_state()
    state = run_block(state, "S01_B001")
    state = pb.accept_input(state, "open_letter")
    state = run_block(state, "S01_B002")
    if letter != "close_letter":
        state = pb.accept_input(state, letter)
        state = run_block(state, "S01_B003" if letter == "inspect_letter_last" else "S01_B004")
    state = pb.accept_input(state, "close_letter")
    state = run_block(state, "S01_B005" if state["K01a"] or state["K01b"] else "S01_B006")
    state = run_block(state, "S01_B007")
    state = pb.accept_input(state, "dismount")
    state = pb.enter(state, "MS14_D01_S02")
    state = run_block(state, "S02_B001")
    state = pb.accept_input(state, invitation)
    state = run_block(state, "S02_B002" if invitation == "show_invitation" else "S02_B003")
    state = run_block(state, "S02_B004")
    return pb.enter(pb.accept_input(state, "to_documents"), "MS14_D01_S03")


def inspect(state, key):
    state = pb.accept_input(state, "inspect_original" if key == "E03" else "inspect_rules")
    return run_block(state, "S03_B001", ["MS14_D01_S03_L0002" if key == "E03" else "MS14_D01_S03_L0007"])


def submit(state, fields):
    state = deepcopy(state)
    state["selected"] = list(fields)
    action = "submit" if pb.correct_submission(state) else "passenger" if set(fields) == {"passenger"} else "count"
    state = pb.accept_input(state, action)
    return run_block(state, pb.submission_block(state).removeprefix(pb.PREFIX))


class ProductionBasis01(unittest.TestCase):
    def test_source_contract_is_exhaustively_mapped(self):
        pb.validate(DATA)

    def test_unknown_conditions_effects_and_entry_fail_closed(self):
        for mutate in (
            lambda d: d["scenes"][0]["blocks"][0].update(when="unknown=true"),
            lambda d: d["scenes"][0]["blocks"][0]["records"][0].update(effects=["rescue_everyone=true"]),
            lambda d: d["scenes"][0]["blocks"][0]["records"][0].update(requires=["unmapped"]),
            lambda d: d["scenes"][0].update(enter_when=["unknown=true"]),
        ):
            data = deepcopy(DATA); mutate(data)
            with self.assertRaises((ValueError, KeyError)): pb.validate(data)

    def test_letter_requires_actual_open_input(self):
        with self.assertRaises(ValueError): run_block(pb.new_state(), "S01_B002")
        with self.assertRaises(ValueError): pb.accept_input(pb.new_state(), "dismount")

    def test_letter_routes_and_arrival_choices_preserve_unknown_author(self):
        for letter in ("close_letter", "inspect_letter_last", "inspect_letter_hand"):
            for invitation in ("show_invitation", "request_original"):
                state = arrive(letter, invitation)
                self.assertEqual(state["K01a"], letter == "inspect_letter_last")
                self.assertEqual(state["K01b"], letter == "inspect_letter_hand")
                self.assertEqual(state["invitation_author"], "unknown")
                self.assertEqual(state["evidence"], ["E01", "E02"])

    def test_scene_entry_rejects_missing_evidence_and_separation(self):
        with self.assertRaises(ValueError): pb.enter(pb.new_state(), "MS14_D01_S03")
        state = arrive();state["father_with_daram"] = False
        self.assertFalse(pb.can_enter(state, "MS14_D01_S02"))

    def test_entry_does_not_auto_grant_application_or_rules(self):
        state = arrive()
        with self.assertRaises(ValueError): run_block(state, "S03_B001")
        self.assertEqual(state["evidence"], ["E01", "E02"])

    def test_document_order_and_reinspection_do_not_repeat_cost_or_effects(self):
        for order in (("E03", "E04"), ("E04", "E03")):
            state = arrive()
            for key in order: state = inspect(state, key)
            expected = deepcopy(state)
            for _ in range(5):
                state = inspect(inspect(state, "E03"), "E04")
            self.assertEqual(state["elapsed_minutes"], 35)
            self.assertEqual(state["applied"], expected["applied"])
            self.assertEqual(set(state["evidence"]), {"E01", "E02", "E03", "E04"})

    def test_early_correct_submission_skips_reason_question(self):
        state = inspect(inspect(arrive(), "E03"), "E04")
        state = submit(state, pb.REQUIRED)
        self.assertTrue(state["gate_basis_proven"])
        self.assertTrue(state["purpose_difference_known"])
        self.assertFalse(state["reason_heard"])
        self.assertFalse(state["gate_registered"])

    def test_regular_route_optional_reason_then_registration(self):
        for ask in (False, True):
            state = inspect(inspect(arrive(), "E03"), "E04")
            state = run_block(pb.accept_input(state, "connect"), "S03_B002")
            if ask: state = run_block(pb.accept_input(state, "ask_worker_reason"), "S03_B010")
            state = submit(state, pb.REQUIRED)
            self.assertEqual(state["reason_heard"], ask)
            state = pb.enter(state, "MS14_D01_S04")
            state = run_block(state, "S04_B001")
            self.assertTrue(state["gate_registered"])
            self.assertEqual(state["evidence"].count("E05"), 1)
            self.assertEqual(state["family_cookie"], 1)
            self.assertEqual(state["mother_location"], "unknown")

    def test_missing_or_extra_basis_never_succeeds(self):
        for fields in ([], ["application_count"], ["passenger"], list(pb.REQUIRED), list(pb.REQUIRED) + ["worker_rule"]):
            state = arrive()
            result = submit(state, fields)
            self.assertFalse(result["gate_basis_proven"])
            self.assertEqual(result["elapsed_minutes"], state["elapsed_minutes"])

    def test_wrong_hint_retry_and_direct_success(self):
        state = inspect(inspect(arrive(), "E03"), "E04")
        state = submit(state, ["application_count"])
        state = run_block(pb.accept_input(state, "hint"), "S03_B009")
        self.assertFalse(state["gate_basis_proven"])
        self.assertTrue(submit(state, pb.REQUIRED)["gate_basis_proven"])
        self.assertEqual(state["elapsed_minutes"], 35)

    def test_save_roundtrip_effect_boundaries_and_reentry_are_idempotent(self):
        state = pb.enter(submit(inspect(inspect(arrive(), "E03"), "E04"), pb.REQUIRED), "MS14_D01_S04")
        block = BLOCKS["MS14_D01_S04_B001"]
        for record in block["records"]:
            before = json.loads(json.dumps(state))
            state = pb.commit_record(before, block, record)
            restored = json.loads(json.dumps(state))
            self.assertEqual(pb.commit_record(restored, block, record), state)
            self.assertEqual(before["elapsed_minutes"], state["elapsed_minutes"])
        self.assertEqual(state["evidence"].count("E05"), 1)

    def test_block_dispatch_does_not_execute_unselected_letter_branch(self):
        state = arrive()
        with self.assertRaises(ValueError): run_block(state, "S03_B010")
        with self.assertRaises(ValueError): pb.allowed(state, "MS14_D01_S03_B999")

    def test_copy_on_write_preserves_rollback_snapshot(self):
        original = arrive();snapshot = deepcopy(original)
        inspect(original, "E03")
        self.assertEqual(original, snapshot)

    def test_new_entry_routes_to_adapter_and_uses_existing_ui(self):
        source = (ROOT / "game/room13.rpy").read_text()
        self.assertIn("jump pb01_start", source.split("label room13_start:")[1].split("label r13_entry:")[0])
        adapter = (ROOT / "game/production_basis01.rpy").read_text()
        self.assertIn("renpy.display_menu", adapter)
        self.assertIn('call screen r13_book("guard", present=True)', adapter)
        self.assertNotIn("eval(", adapter)
        self.assertNotIn("source_effects", adapter)


if __name__ == "__main__": unittest.main()
