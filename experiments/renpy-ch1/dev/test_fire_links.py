"""화재의 관찰 연결과 자료 역할은 기존 증명·기회·생사를 보존한다.

순수 모델에 실제 소스의 함수를 연결한다. 화면 입력·저장 파일은 엔진 QA에서 검사한다.
"""
import ast
import copy
import itertools
import json
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SOURCE = GAME / "systems/room13_fire_links.rpy"
ORIGIN = "불이 시작된 곳과 진술을 대조한다"
RESCUE = "불의 원인과 아이 구조를 구분한다"
EMPTY = "불의 원인과 빈 창고 진압을 구분한다"


def proof_rules():
    source = (GAME / "room13_v111_newworld_rules.rpy").read_text()
    tree = ast.parse(textwrap.dedent(source.split("init 318 python:", 1)[1]))
    names = {"R13_PROOF_EXTRAS", "R13_PROOF_ALTERNATES",
             "r13_v111_proof_sets", "r13_v111_proof_accepts"}
    nodes = [node for node in tree.body if
             isinstance(node, ast.FunctionDef) and node.name in names
             or isinstance(node, ast.Assign) and any(
                 isinstance(target, ast.Name) and target.id in names for target in node.targets)]
    namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "기존 증명 규칙", "exec"), namespace)
    return namespace


class FireVerdictCompatibility(unittest.TestCase):
    """추가 조작이 있더라도 기존 자료 정답·대체·덧붙임의 의미가 달라지면 안 된다."""
    def setUp(self):
        self.rules = proof_rules()

    def accepts(self, claim, given):
        correct = ["E06_FIRE"] if claim == ORIGIN else [
            "E06_FIRE", "E06_EMPTY" if claim == EMPTY else "E06_RESCUE", "E07_NUBI"]
        return self.rules["r13_v111_proof_accepts"](
            claim, correct, ["V111:" + key for key in given])

    def test_first_proof_still_uses_only_existing_fire_record(self):
        self.assertTrue(self.accepts(ORIGIN, ["E06_FIRE"]))
        for given in ([], ["E06_RESCUE"], ["E06_FIRE", "E06_RESCUE"], ["E06_FIRE", "E01"]):
            with self.subTest(given=given):
                self.assertFalse(self.accepts(ORIGIN, given))

    def test_confession_and_ticket_are_alternates_and_can_be_submitted_together(self):
        for claim, action in ((RESCUE, "E06_RESCUE"), (EMPTY, "E06_EMPTY")):
            for promise in (["E07_NUBI"], ["NW_NUBI_TICKET"], ["E07_NUBI", "NW_NUBI_TICKET"]):
                for extras in ([], ["NW_LAUNDRY_TALK"], ["E02"], ["NW_LAUNDRY_TALK", "E02"]):
                    with self.subTest(claim=claim, promise=promise, extras=extras):
                        self.assertTrue(self.accepts(claim, ["E06_FIRE", action] + promise + extras))

    def test_action_from_other_branch_and_hearsay_only_do_not_replace_required_proof(self):
        for claim, action, other in ((RESCUE, "E06_RESCUE", "E06_EMPTY"),
                                     (EMPTY, "E06_EMPTY", "E06_RESCUE")):
            for given in (["E06_FIRE", other, "E07_NUBI"],
                          ["E06_FIRE", action, "NW_LAUNDRY_TALK"],
                          ["E06_FIRE", action, "E02"],
                          ["E06_FIRE", action, "E07_NUBI", "E01"],
                          ["E06_FIRE", action, other, "E07_NUBI"]):
                with self.subTest(claim=claim, given=given):
                    self.assertFalse(self.accepts(claim, given))


def load_links():
    source = SOURCE.read_text()
    namespace = {}
    for body in re.findall(r"^init \d+ python:\n((?:[ \t].*\n|\n)*)", source, re.M):
        tree = ast.parse(textwrap.dedent(body))
        exec(compile(tree, str(SOURCE), "exec"), namespace)
    return namespace


class FireLinkModel(unittest.TestCase):
    def setUp(self):
        self.ns = load_links()
        self.owned = ["V111:" + key for key in (
            "E06_FIRE", "E06_RESCUE", "E06_EMPTY", "E07_NUBI",
            "NW_NUBI_TICKET", "NW_LAUNDRY_TALK", "E02", "E01")]

    def check(self, key, row, owned=None, witness=True):
        owned = self.owned if owned is None else owned
        observations = self.ns["r13_fire_link_observations"](owned, witness)
        return self.ns["r13_fire_link_check"](key, row, owned, observations)

    def first(self, facts=("lamp", "door"), question="door", materials=None):
        return dict(observations=list(facts), question=question,
                    materials=["V111:E06_FIRE"] if materials is None else list(materials))

    def second(self, roles, extra=()):
        return dict(roles=list(roles), extra=list(extra))

    def test_observations_require_owned_source_and_actual_witness(self):
        facts = self.ns["r13_fire_link_observations"]
        owned = ["V111:E06_FIRE", "V111:E06_RESCUE"]
        before = copy.deepcopy(owned)
        self.assertEqual(facts([], False), [])
        self.assertEqual([row[0] for row in facts([], True)], ["witness"])
        self.assertEqual([row[0] for row in facts(owned, False)], ["lamp", "door", "bori"])
        self.assertEqual([row[0] for row in facts(owned, True)], ["lamp", "door", "witness", "bori"])
        for _, _, source in facts(owned, True):
            self.assertTrue(source is None or source in owned)
        self.assertEqual(owned, before)
        self.assertEqual(facts(["V111:E06_EMPTY"], False)[0][2], "V111:E06_EMPTY")
        self.assertEqual(facts(["V111:E06_RESCUE"], False)[0][2], "V111:E06_RESCUE")

    def test_site_picture_requires_the_collected_fire_record_without_mutating_sources(self):
        available = self.ns["r13_fire_site_available"]
        for owned in ([], ["V111:E06_RESCUE"], ["V111:E06_FIRE"]):
            before = list(owned)
            self.assertEqual(available("V111:E06_FIRE", owned), "V111:E06_FIRE" in owned)
            self.assertFalse(available("V111:E06", owned))
            self.assertEqual(owned, before)

    def test_sources_are_derived_from_selected_owned_facts_without_assuming_verdict(self):
        sources=self.ns["r13_fire_link_sources"]
        facts=self.ns["r13_fire_link_observations"](self.owned,True)
        for selected,expected in ((["lamp","door"],["V111:E06_FIRE"]),
                                  (["door","witness"],["V111:E06_FIRE"]),
                                  (["bori","door"],["V111:E06_EMPTY","V111:E06_FIRE"]),
                                  (["witness",None],[]),(["missing","lamp"],["V111:E06_FIRE"])):
            row=dict(observations=selected,materials=[],source_manual=False)
            before=copy.deepcopy((row,self.owned,facts))
            self.assertEqual(sources(row,self.owned,facts),expected)
            self.assertEqual((row,self.owned,facts),before)
        self.assertEqual(sources(dict(observations=["lamp","door"]),[],[]),[])

    def test_source_changes_and_legacy_materials_are_not_replaced_with_correct_record(self):
        sources=self.ns["r13_fire_link_sources"]
        facts=self.ns["r13_fire_link_observations"](self.owned,True)
        for row in (dict(observations=["lamp","door"],materials=["V111:E01"]),
                    dict(observations=["door","witness"],materials=["V111:E01"],source_manual=True)):
            self.assertEqual(sources(row,self.owned,facts),["V111:E01"])
        self.assertEqual(sources(dict(observations=["lamp","door"],materials=["V111:E99"],source_manual=True),self.owned,facts),[])

    def test_first_ui_checks_complete_syntax_without_pregrading_available_questions(self):
        # 어느 관찰·질문을 물을지는 상대가 답한다. 화면은 문법이 맞는 질문을 거절하지 않는다.
        for facts in itertools.permutations(("lamp", "door", "witness", "bori"), 2):
            for question in ("door", "lamp_keeper", "wood_owner"):
                with self.subTest(facts=facts, question=question):
                    self.assertEqual(self.check(ORIGIN, self.first(facts, question)), "ready")
        for question in (None, "unknown"):
            self.assertEqual(self.check(ORIGIN, self.first(question=question)), "incomplete")

    def test_actual_question_routes_both_relevant_pairs_and_other_questions(self):
        observations = self.ns["r13_fire_link_observations"](self.owned, True)
        route = self.ns["r13_fire_question_route"]
        for facts in (("lamp", "door"), ("door", "lamp"), ("door", "witness"), ("witness", "door")):
            row = dict(question="door", observations=list(facts))
            before = copy.deepcopy((row, observations))
            self.assertEqual(route(row, observations), "challenge")
            self.assertEqual((row, observations), before)
        for question in ("lamp_keeper", "wood_owner"):
            self.assertEqual(route(dict(question=question, observations=["lamp", "door"]), observations), question)
        self.assertEqual(route(dict(question="door", observations=["lamp", "witness"]), observations), "presence")
        self.assertEqual(route(dict(question="door", observations=["lamp", "bori"]), observations), "action")
        for row in (None, {}, dict(question="door", observations=["door", "door"]),
                    dict(question="door", observations=["door", "unheard"])):
            self.assertEqual(route(row, observations), "incomplete")

    def test_recheck_lists_only_owned_trace_and_exchange_actually_heard(self):
        options = self.ns["r13_fire_recheck_options"]
        self.assertEqual(options([], False), ())
        self.assertEqual(options(["V111:E06_RESCUE"], False), ())
        self.assertEqual(options(["V111:E06_FIRE"], False), ("trace",))
        self.assertEqual(options([], True), ("pot",))
        self.assertEqual(options(["V111:E06_FIRE"], True), ("trace", "pot"))

    def test_missing_duplicate_or_unheard_fact_never_counts_as_complete_link(self):
        for facts in ((None, "door"), ("door", None), ("door", "door"), ("made-up", "door"), ("lamp",)):
            with self.subTest(facts=facts):
                self.assertEqual(self.check(ORIGIN, self.first(facts)), "incomplete")
        self.assertEqual(self.check(ORIGIN, self.first(("witness", "door")), witness=False), "incomplete")
        self.assertEqual(self.check(ORIGIN, self.first(materials=[])), "empty")

    def test_first_wrong_material_is_left_to_existing_verdict_without_revealing_answer(self):
        row = self.first(materials=["V111:E01"])
        before = copy.deepcopy(row)
        self.assertEqual(self.check(ORIGIN, row), "ready")
        self.assertFalse(proof_rules()["r13_v111_proof_accepts"](ORIGIN, ["E06_FIRE"], row["materials"]))
        self.assertEqual(row, before)

    def test_second_role_order_is_required_for_each_valid_document_set(self):
        for key, action in ((RESCUE, "V111:E06_RESCUE"), (EMPTY, "V111:E06_EMPTY")):
            for who in ("V111:E07_NUBI", "V111:NW_NUBI_TICKET"):
                expected_roles = ("V111:E06_FIRE", who, action)
                for roles in itertools.permutations(expected_roles):
                    for extra in ((), ("V111:E02",), ("V111:NW_LAUNDRY_TALK",),
                                  ("V111:E02", "V111:NW_LAUNDRY_TALK")):
                        with self.subTest(key=key, roles=roles, extra=extra):
                            expected = "ready" if roles == expected_roles else "roles"
                            self.assertEqual(self.check(key, self.second(roles, extra)), expected)

    def test_both_confession_and_ticket_can_support_same_role_without_losing_other(self):
        for key, action in ((RESCUE, "V111:E06_RESCUE"), (EMPTY, "V111:E06_EMPTY")):
            for who, extra in (("V111:E07_NUBI", "V111:NW_NUBI_TICKET"),
                               ("V111:NW_NUBI_TICKET", "V111:E07_NUBI")):
                row = self.second(("V111:E06_FIRE", who, action), (extra, "V111:E02"))
                self.assertEqual(self.check(key, row), "ready")
                chosen = self.ns["r13_fire_link_union"](row, self.owned, False)
                self.assertIn(who, chosen)
                self.assertIn(extra, chosen)
                self.assertEqual(len(chosen), 5)

    def test_partial_or_wrong_records_still_reach_original_chance_and_hint_pipeline(self):
        for roles, extra in ((("V111:E06_FIRE", None, None), ()),
                             (("V111:E06_FIRE", "V111:E07_NUBI", None), ()),
                             ((None, None, None), ("V111:E01",)),
                             (("V111:E07_NUBI", "V111:E06_FIRE", "V111:E06_RESCUE"), ("V111:E01",)),
                             (("V111:E06_FIRE", "V111:E07_NUBI", "V111:E06_EMPTY"), ())):
            with self.subTest(roles=roles, extra=extra):
                self.assertEqual(self.check(RESCUE, self.second(roles, extra)), "ready")

    def test_no_owned_material_cannot_be_invented_by_saved_or_foreign_input(self):
        row = self.second(("V111:E06_FIRE", "V111:E07_NUBI", "V111:E06_RESCUE"))
        owned = ["V111:E06_FIRE", "V111:E06_RESCUE"]
        # 구 저장의 미보유 참조는 제거한다. 남은 두 장은 기존 부분 제출 판정으로 보낸다.
        self.assertEqual(self.check(RESCUE, row, owned), "ready")
        chosen = self.ns["r13_fire_link_union"](row, owned, False)
        self.assertEqual(chosen, ["V111:E06_FIRE", "V111:E06_RESCUE"])
        self.assertFalse(proof_rules()["r13_v111_proof_accepts"](
            RESCUE, ["E06_FIRE", "E06_RESCUE", "E07_NUBI"], chosen))
        self.assertEqual(self.check(RESCUE, self.second((None, None, None)), owned), "empty")
        self.assertEqual(self.check(ORIGIN, self.first(materials=["V111:E99"])), "empty")

    def test_union_filters_missing_records_deduplicates_and_never_modifies_input(self):
        union = self.ns["r13_fire_link_union"]
        row = dict(materials=["V111:E06_FIRE", "V111:E99", "V111:E06_FIRE"],
                   roles=["V111:E07_NUBI", "V111:E06_FIRE", "V111:E06_RESCUE"],
                   extra=["V111:E07_NUBI", "V111:E99", "V111:E02"])
        before = copy.deepcopy((row, self.owned))
        self.assertEqual(union(row, self.owned, True), ["V111:E06_FIRE"])
        self.assertEqual(union(row, self.owned, False),
                         ["V111:E07_NUBI", "V111:E06_FIRE", "V111:E06_RESCUE", "V111:E02"])
        self.assertEqual((row, self.owned), before)


class StoreProxy:
    """Ren’Py store 속성과 init 전역이 같은 공간을 보도록 모사한다."""
    def __init__(self, namespace):
        object.__setattr__(self, "namespace", namespace)

    def __getattr__(self, name):
        return self.namespace[name]

    def __setattr__(self, name, value):
        self.namespace[name] = value


class FireLinkRuntime(unittest.TestCase):
    def setUp(self):
        self.ns = load_links()
        self.owned = ["V111:E06_FIRE", "V111:E06_RESCUE", "V111:E07_NUBI", "V111:E01"]
        self.values = {"bori_nubi_door_witness_heard": True, "fire_lamp_defense_heard": True,
                       "tries:fire": 2, "KKOMI_ALIVE": False, "FIRE_EVACUATED": False}
        self.room = dict(evidence=self.owned, arguments={}, v111=dict(values=self.values))
        self.ended = []
        self.retained = []
        self.ns.update(room13=self.room, r13_fire_link_views={},
                       r13_pw_entries=lambda: list(self.owned),
                       r13_v111_active=lambda: True,
                       r13_v111_value=lambda key: self.values.get(key),
                       r13_catalog_title=lambda key: key,
                       renpy=SimpleNamespace(retain_after_load=lambda: self.retained.append(True),
                                             restart_interaction=lambda: None, end_interaction=self.ended.append))
        self.ns["store"] = StoreProxy(self.ns)
        self.ns["r13_pw_set_arguments"] = lambda claim, chosen: self.room["arguments"].__setitem__(claim, list(chosen))
        self.claim = "v111:" + ORIGIN

    def test_old_completed_hypothesis_uses_existing_screen_without_mutating_story(self):
        active = self.ns["r13_fire_links_active"]
        before = copy.deepcopy(self.room)
        self.assertTrue(active(ORIGIN))
        self.assertFalse(active("다른 사건"))
        self.values["fire_origin_hypothesis"] = True
        self.assertFalse(active(ORIGIN))
        self.assertTrue(active(RESCUE))
        self.assertTrue(active(EMPTY))
        self.values.pop("fire_origin_hypothesis")
        self.assertEqual(self.room, before)

    def test_direct_admission_requires_formally_accepted_owned_proof_or_completed_old_save(self):
        self.ns["r13_v111_owned"] = lambda key: "V111:" + key in self.owned
        self.ns["r13_v111_proof_accepts"] = proof_rules()["r13_v111_proof_accepts"]
        ready = self.ns["r13_fire_admission_ready"]
        before = copy.deepcopy(self.room)
        self.assertFalse(ready())  # 현장 기록을 가진 것만으로 자백하지 않는다.
        self.assertEqual(self.room, before)
        key = "proof_given:" + ORIGIN
        for given, expected in ((["V111:E06_RESCUE"], False),
                                (["V111:E06_FIRE", "V111:E01"], False),
                                (["V111:E06_FIRE"], True)):
            self.values[key] = given
            before = copy.deepcopy(self.room)
            self.assertEqual(ready(), expected)
            self.assertEqual(self.room, before)
        self.owned.remove("V111:E06_FIRE")
        self.assertFalse(ready())
        self.values["NUBI_admitted_setting_fire"] = True
        before = copy.deepcopy(self.room)
        self.assertTrue(ready())  # 완료한 옛 저장은 재제출하지 않는다.
        self.assertEqual(self.room, before)

    def test_query_and_caller_edits_do_not_alias_saved_lists_or_arguments(self):
        row = dict(observations=["lamp", "door"], question="door",
                   materials=["V111:E06_FIRE"], roles=[None, None, None], extra=[])
        self.ns["r13_fire_links_write"](self.claim, row)
        saved = copy.deepcopy(self.ns["r13_fire_link_views"])
        row["observations"][0] = "bori"
        row["materials"].append("V111:E01")
        self.assertEqual(self.ns["r13_fire_link_views"], saved)
        queried = self.ns["r13_fire_links_state"](self.claim)
        queried["roles"][0] = "V111:E01"
        queried["extra"].append("V111:E01")
        self.assertEqual(self.ns["r13_fire_link_views"], saved)
        self.assertEqual(self.room["arguments"], {})

    def test_other_questions_reach_actual_reply_without_story_or_argument_changes(self):
        before = copy.deepcopy(self.room)
        for facts, question, route in ((["lamp", "door"], "wood_owner", "wood_owner"),
                                       (["lamp", "door"], "lamp_keeper", "lamp_keeper"),
                                       (["lamp", "witness"], "door", "presence")):
            self.ns["r13_fire_links_write"](self.claim, dict(
                materials=["V111:E06_FIRE"], observations=facts, question=question))
            self.ns["r13_fire_links_submit"](self.claim, ORIGIN)
            action, payload = self.ended[-1]
            self.assertEqual(action, "fire_question")
            self.assertEqual(self.ns["r13_fire_question_validate"](payload), route)
            self.assertFalse(self.ns["r13_fire_question_finish"](payload, argue=True))
            self.assertTrue(self.ns["r13_fire_question_finish"](payload))
            self.assertEqual(self.ns["r13_fire_links_state"](self.claim)["view"], "board")
            self.assertFalse(self.ns["r13_fire_links_state"](self.claim)["notice"])
            self.assertEqual(self.room, before)

    def test_actual_valid_reply_alone_commits_materials_for_unchanged_original_verdict(self):
        before = copy.deepcopy(self.values)
        for material in ("V111:E06_FIRE", "V111:E01"):
            self.ns["r13_fire_links_write"](self.claim, dict(
                materials=[material], observations=["lamp", "door"], question="door"))
            arguments = copy.deepcopy(self.room["arguments"])
            self.ns["r13_fire_links_submit"](self.claim, ORIGIN)
            action, payload = self.ended[-1]
            self.assertEqual(action, "fire_question")
            self.assertEqual(self.room["arguments"], arguments)
            self.assertTrue(self.ns["r13_fire_question_finish"](payload, argue=True))
            self.assertEqual(self.room["arguments"][self.claim], [material])
            self.assertEqual(proof_rules()["r13_v111_proof_accepts"](ORIGIN, ["E06_FIRE"], [material]),
                             material == "V111:E06_FIRE")
        self.assertEqual(self.values, before)
        self.assertNotIn("NUBI_admitted_setting_fire", self.values)

    def test_question_payload_is_a_copy_and_stale_or_unowned_payload_cannot_commit(self):
        self.ns["r13_fire_links_write"](self.claim, dict(
            materials=["V111:E06_FIRE"], observations=["lamp", "door"], question="door"))
        self.ns["r13_fire_links_submit"](self.claim, ORIGIN)
        _, payload = self.ended[-1]
        self.assertTrue(self.ns["r13_fire_links_state"](self.claim)["source_pending"])
        saved = copy.deepcopy(self.ns["r13_fire_link_views"])
        changed = copy.deepcopy(payload)
        changed["observations"][0] = "witness"
        self.assertEqual(self.ns["r13_fire_question_validate"](changed), "incomplete")
        changed = copy.deepcopy(payload)
        changed["materials"].append("V111:E99")
        self.assertFalse(self.ns["r13_fire_question_finish"](changed, argue=True))
        self.assertEqual(self.ns["r13_fire_link_views"], saved)
        self.assertEqual(self.room["arguments"], {})
        payload["observations"].append("bori")
        payload["materials"].append("V111:E01")
        self.assertEqual(self.ns["r13_fire_link_views"], saved)

    def test_pick_rejects_unowned_record_and_unheard_witness(self):
        self.values["bori_nubi_door_witness_heard"] = False
        self.ns["r13_fire_links_write"](self.claim, dict(observations=[None, None]))
        before = copy.deepcopy((self.ns["r13_fire_link_views"], self.room))
        self.ns["r13_fire_links_pick"](self.claim, ORIGIN, "obs0", "witness")
        self.ns["r13_fire_links_pick"](self.claim, ORIGIN, "materials", "V111:E99")
        self.assertEqual((self.ns["r13_fire_link_views"], self.room), before)

    def test_board_question_can_submit_without_opening_source_preview(self):
        before=copy.deepcopy((self.values,self.owned))
        for field,value in (("obs0","lamp"),("obs1","door"),("question","door")):
            self.ns["r13_fire_links_pick"](self.claim,ORIGIN,field,value)
        row=self.ns["r13_fire_links_state"](self.claim)
        self.assertEqual(row["materials"],[])
        self.assertFalse(row["source_manual"])
        self.assertEqual(self.room["arguments"].get(self.claim,[]),[])
        self.assertEqual(row["view"],"board")
        self.assertEqual(self.ended,[])
        self.ns["r13_fire_links_submit"](self.claim,ORIGIN)
        self.assertEqual(self.room["arguments"].get(self.claim,[]),[])
        self.assertEqual(self.ended[0][0],"fire_question")
        self.assertTrue(self.ns["r13_fire_question_finish"](self.ended[0][1],argue=True))
        self.assertEqual(self.room["arguments"][self.claim],["V111:E06_FIRE"])
        self.assertEqual((self.values,self.owned),before)

    def test_source_editor_preserves_explicit_wrong_selection_for_original_verdict(self):
        for field,value in (("obs0","door"),("obs1","witness"),("question","door")):
            self.ns["r13_fire_links_pick"](self.claim,ORIGIN,field,value)
        self.ns["r13_fire_links_edit_sources"](self.claim)
        row=self.ns["r13_fire_links_state"](self.claim)
        self.assertEqual(row["materials"],["V111:E06_FIRE"])
        self.assertTrue(row["source_manual"])
        self.assertEqual(self.room["arguments"].get(self.claim,[]),[])
        self.ns["r13_fire_links_pick"](self.claim,ORIGIN,"materials","V111:E06_FIRE")
        self.ns["r13_fire_links_pick"](self.claim,ORIGIN,"materials","V111:E01")
        self.ns["r13_fire_links_submit"](self.claim,ORIGIN)
        self.assertEqual(self.room["arguments"].get(self.claim,[]),[])
        self.assertEqual(self.ended[0][0],"fire_question")
        self.assertTrue(self.ns["r13_fire_question_finish"](self.ended[0][1],argue=True))
        self.assertEqual(self.room["arguments"][self.claim],["V111:E01"])

    def test_source_preview_save_round_trip_has_no_story_or_argument_mutation(self):
        for field,value in (("obs0","door"),("obs1","witness"),("question","door")):
            self.ns["r13_fire_links_pick"](self.claim,ORIGIN,field,value)
        self.ns["r13_fire_links_change"](self.claim,view="sources")
        saved=copy.deepcopy(self.ns["r13_fire_links_state"](self.claim))
        domain=copy.deepcopy(self.room)
        self.ns["r13_fire_link_views"]=json.loads(json.dumps(self.ns["r13_fire_link_views"]))
        self.ns["r13_fire_links_enter"](self.claim,ORIGIN)
        self.assertEqual(self.ns["r13_fire_links_state"](self.claim),saved)
        self.assertEqual(self.room,domain)
        self.assertEqual(self.ended,[])

    def test_pending_manual_source_survives_save_before_any_submission(self):
        for field,value in (("obs0","lamp"),("obs1","door"),("question","door")):
            self.ns["r13_fire_links_pick"](self.claim,ORIGIN,field,value)
        self.ns["r13_fire_links_edit_sources"](self.claim)
        self.ns["r13_fire_links_pick"](self.claim,ORIGIN,"materials","V111:E06_FIRE")
        self.ns["r13_fire_links_pick"](self.claim,ORIGIN,"materials","V111:E01")
        draft=copy.deepcopy(self.ns["r13_fire_links_state"](self.claim))
        self.assertTrue(draft["source_pending"])
        self.assertEqual(draft["materials"],["V111:E01"])
        domain=copy.deepcopy(self.room)
        self.ns["r13_fire_link_views"]=json.loads(json.dumps(self.ns["r13_fire_link_views"]))
        self.ns["r13_fire_links_enter"](self.claim,ORIGIN)
        self.assertEqual(self.ns["r13_fire_links_state"](self.claim),draft)
        self.assertEqual(self.room,domain)
        self.assertEqual(self.ended,[])

    def test_saved_partial_connection_restores_without_granting_story_progress(self):
        row = dict(view="choices", field="obs1", observations=["door", None],
                   question=None, materials=["V111:E06_FIRE"], roles=[None, None, None], extra=[])
        self.ns["r13_fire_links_write"](self.claim, row)
        self.room["arguments"][self.claim] = ["V111:E06_FIRE"]
        before = copy.deepcopy(self.values)
        serialized = json.dumps(self.ns["r13_fire_link_views"])
        self.ns["r13_fire_link_views"] = json.loads(serialized)
        self.ns["r13_fire_links_enter"](self.claim, ORIGIN)
        restored = self.ns["r13_fire_links_state"](self.claim)
        for key, expected in row.items():
            self.assertEqual(restored[key], expected, key)
        self.assertEqual(self.values, before)
        self.assertEqual(self.ended, [])

    def test_clear_removes_only_chosen_role_without_mutating_prior_lists_or_story(self):
        claim = "v111:" + RESCUE
        original = dict(roles=["V111:E06_FIRE", "V111:E07_NUBI", "V111:E06_RESCUE"],
                        extra=["V111:E01"], observations=["lamp", "door"], question="door")
        before = copy.deepcopy((original, self.values, self.owned))
        for slot in range(3):
            with self.subTest(slot=slot):
                self.ns["r13_fire_links_write"](claim, original)
                previous = self.ns["r13_fire_link_views"][claim]
                self.ns["r13_fire_links_clear"](claim, RESCUE, "role" + str(slot))
                current = self.ns["r13_fire_links_state"](claim)
                expected = list(original["roles"])
                expected[slot] = None
                self.assertEqual(current["roles"], expected)
                self.assertEqual(current["extra"], ["V111:E01"])
                self.assertEqual(current["observations"], ["lamp", "door"])
                self.assertEqual(current["question"], "door")
                self.assertEqual(self.room["arguments"][claim],
                                 [key for key in expected if key] + ["V111:E01"])
                self.assertEqual(previous["roles"], original["roles"])
                self.assertIsNot(current["roles"], previous["roles"])
                self.assertEqual((original, self.values, self.owned), before)
        untouched = copy.deepcopy((self.ns["r13_fire_link_views"], self.room))
        retained = len(self.retained)
        for field in ("obs0", "question", "materials", "role3", None):
            self.ns["r13_fire_links_clear"](claim, RESCUE, field)
        self.assertEqual((self.ns["r13_fire_link_views"], self.room), untouched)
        self.assertEqual(len(self.retained), retained)
        self.assertEqual(self.ended, [])

    def test_ui_write_retains_save_state_and_queries_have_no_checkpoint_side_effect(self):
        before = copy.deepcopy(self.room)
        self.assertEqual(self.retained, [])
        self.ns["r13_fire_links_write"](self.claim, dict(observations=["lamp", None]))
        self.assertTrue(self.retained)
        retained = len(self.retained)
        saved = copy.deepcopy(self.ns["r13_fire_link_views"])
        self.ns["r13_fire_links_state"](self.claim)
        self.assertEqual(len(self.retained), retained)
        self.assertEqual(self.ns["r13_fire_link_views"], saved)
        self.assertEqual(self.room, before)


if __name__ == "__main__":
    unittest.main()
