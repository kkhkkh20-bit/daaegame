"""Explicit D01 adapter. Authored strings are validated, never evaluated.

Pure, copy-on-write save state; Ren'Py owns statement cursor and rollback.
Only the selected block runs. Presentation sidecars never execute effects.
"""
from copy import deepcopy

VERSION = "DT_STORY_1.1_PRODUCTION_BASIS_01_20261020"
PREFIX = "MS14_D01_"
SPEAKERS = {"아빠": "dad", "다람": "daram", "까로": "karo", "돌목": "guard"}
REQUIRED = frozenset(("family_visit", "two_person_lodging", "family_registration_rule"))
FIELDS = {
    "application_count": ("E03", "신청 2명"),
    "family_visit": ("E03", "가족 방문"),
    "two_person_lodging": ("E03", "여관 13호, 방문 가족 2명 숙박 확인"),
    "family_registration_rule": ("E04", "가족 방문은 숙소가 확인된 동행 인원으로 등록한다"),
    "worker_rule": ("E04", "신규 일꾼은 작업 명단의 본인만 등록한다"),
}


def new_state():
    return dict(version=VERSION, scene="MS14_D01_S01", record=None,
                day=1, location="carriage", father_alive=True, daram_alive=True,
                new_game=True, father_with_daram=True,
                family_cookie=1, invitation_author="unknown", mother_location="unknown",
                K01a=False, K01b=False, K05=False, reason_heard=False,
                purpose_difference_known=False, gate_basis_proven=False,
                gate_registered=False, letter_close_selected=False,
                carriage_stopped=False, village_revealed=False,
                evidence=[], applied=[], completed_inputs=[], elapsed_minutes=0,
                pending_input=None, input=None, selected=[], complete=False)


# These are exact author strings, not a general expression language.
GUARDS = {
    "S01_B001": "always",
    "S01_B002": "always AND input_completed(MS14_D01_S01:2)",
    "S01_B003": "input=inspect_letter_last",
    "S01_B004": "input=inspect_letter_hand",
    "S01_B005": "(K01a=true OR K01b=true) AND letter_close_selected=true",
    "S01_B006": "letter_close_selected=true AND K01a=false AND K01b=false",
    "S01_B007": "always",
    "S02_B001": "always", "S02_B002": "input=show_invitation",
    "S02_B003": "input=request_original", "S02_B004": "always",
    "S03_B001": "always",
    "S03_B002": "input=connect(E03.family_visit,E02.worker) AND gate_basis_proven=false",
    "S03_B003": "input=inspect(E03.lodging) AND gate_basis_proven=false",
    "S03_B004": "input=submit AND E02,E03,E04 acquired AND selected=family_visit+two_person_lodging+family_registration_rule AND purpose_difference_known=true",
    "S03_B005": "input=submit AND E02,E03,E04 acquired AND selected=family_visit+two_person_lodging+family_registration_rule AND purpose_difference_known=false",
    "S03_B006": "input=submit_only_application_count",
    "S03_B007": "input=submit_only_passenger_confirmation",
    "S03_B008": "input=submit_other_house_application",
    "S03_B009": "input=hint",
    "S03_B010": "input=ask_worker_reason AND purpose_difference_known=true AND reason_heard=false",
    "S04_B001": "always",
}
EFFECTS = {
    "acquire(E01)": ("evidence", "E01"), "acquire(E02)": ("evidence", "E02"),
    "acquire(E03)": ("evidence", "E03"), "acquire(E04)": ("evidence", "E04"),
    "acquire(E05)": ("evidence", "E05"),
    **{key + "=true": ("flag", key) for key in
       ("K01a", "K01b", "K05", "reason_heard", "purpose_difference_known",
        "gate_basis_proven", "gate_registered")},
}
ENTRY_GUARDS = {
    "MS14_D01_S01": ["new_game=true", "day=1", "father.alive=true", "daram.alive=true", "father.location=carriage", "daram.location=carriage"],
    "MS14_D01_S02": ["day=1", "carriage_stopped=true", "father_with_daram=true"],
    "MS14_D01_S03": ["day=1", "E02 acquired", "father.location=guardhouse", "daram.location=guardhouse", "gate_registered=false"],
    "MS14_D01_S04": ["day=1", "gate_basis_proven=true", "gate_registered=false"],
}


def validate(data):
    if data["version"] != VERSION:
        raise ValueError("Unsupported production basis")
    seen = set()
    for scene in data["scenes"]:
        if scene["enter_when"] != ENTRY_GUARDS[scene["scene_id"]]:
            raise ValueError("Unmapped scene entry condition")
        for block in scene["blocks"]:
            key = block["id"].removeprefix(PREFIX)
            if GUARDS[key] != block["when"]:
                raise ValueError("Unmapped block condition: " + block["id"])
            seen.add(key)
            for record in block["records"]:
                if record.get("requires"):
                    raise ValueError("Unmapped record requirement: " + record["id"])
                if record["kind"] not in ("action", "dialogue", "narration", "evidence", "choice"):
                    raise ValueError("Unmapped record kind")
                if record["kind"] == "dialogue" and record["speaker"] not in SPEAKERS:
                    raise ValueError("Unmapped speaker")
                for effect in record["effects"]:
                    if effect not in EFFECTS:
                        raise ValueError("Unmapped effect: " + effect)
                for option in record.get("options", []):
                    if option["when"] not in ("always", "E03 acquired", "gate_basis_proven=false", "reason_heard=false",
                                              "purpose_difference_known=true AND reason_heard=false"):
                        raise ValueError("Unmapped option condition")
    if seen != set(GUARDS):
        raise ValueError("Missing D01 blocks")


def can_enter(state, scene_id):
    common = state["day"] == 1 and state["father_alive"] and state["daram_alive"]
    if scene_id == PREFIX + "S01":
        return common and state["new_game"] and state["location"] == "carriage"
    if scene_id == PREFIX + "S02":
        return common and state["carriage_stopped"] and state["father_with_daram"] and "E01" in state["evidence"]
    if scene_id == PREFIX + "S03":
        return common and state["location"] == "guardhouse" and "E02" in state["evidence"] and not state["gate_registered"]
    if scene_id == PREFIX + "S04":
        return common and state["gate_basis_proven"] and not state["gate_registered"] and state["location"] == "guardhouse"
    raise ValueError("Unmapped scene: " + scene_id)


def correct_submission(state):
    return set(state["selected"]) == REQUIRED and {"E02", "E03", "E04"} <= set(state["evidence"])


def allowed(state, block_id):
    key = block_id.removeprefix(PREFIX)
    if key not in GUARDS:
        raise ValueError("Unmapped block: " + block_id)
    # Scene entry is checked once by enter(). Its entry-only conditions may be
    # changed by that same scene (registration), so do not reapply them per line.
    if state["scene"] != block_id.rsplit("_", 1)[0]:
        return False
    action = state["input"]
    if key in ("S01_B001", "S01_B007", "S02_B001", "S02_B004", "S03_B001", "S04_B001"):
        return True
    if key == "S01_B002": return "open_letter" in state["completed_inputs"]
    if key == "S01_B003": return action == "inspect_letter_last"
    if key == "S01_B004": return action == "inspect_letter_hand"
    if key == "S01_B005": return state["letter_close_selected"] and (state["K01a"] or state["K01b"])
    if key == "S01_B006": return state["letter_close_selected"] and not (state["K01a"] or state["K01b"])
    if key == "S02_B002": return action == "show_invitation"
    if key == "S02_B003": return action == "request_original"
    if key == "S03_B004": return action == "submit" and correct_submission(state) and state["purpose_difference_known"]
    if key == "S03_B005": return action == "submit" and correct_submission(state) and not state["purpose_difference_known"]
    if key == "S03_B010":
        return action == "ask_worker_reason" and state["purpose_difference_known"] and not state["reason_heard"]
    inputs = {"S03_B002": "connect", "S03_B003": "lodging", "S03_B006": "count",
              "S03_B007": "passenger", "S03_B008": "other", "S03_B009": "hint"}
    return action == inputs[key] and not state["gate_basis_proven"] and (
        key not in ("S03_B002", "S03_B003") or {"E02", "E03"} <= set(state["evidence"]))


def enter(state, scene_id):
    if not can_enter(state, scene_id):
        raise ValueError("Scene entry rejected: " + scene_id)
    result = deepcopy(state)
    result.update(scene=scene_id, record=None, input=None)
    return result


def accept_input(state, action):
    result = deepcopy(state)
    scene = state["scene"].removeprefix(PREFIX)
    choices = {
        "S01": {"open_letter", "inspect_letter_last", "inspect_letter_hand", "close_letter", "dismount"},
        "S02": {"show_invitation", "request_original", "to_documents"},
        "S03": {"inspect_original", "inspect_rules", "connect", "lodging", "hint", "ask_worker_reason",
                "submit", "count", "passenger", "other", "read_processing"},
        "S04": set(),
    }
    if action not in choices[scene]: raise ValueError("Unexpected input: " + action)
    if action in ("connect", "lodging") and not {"E02", "E03"} <= set(state["evidence"]):
        raise ValueError("Read the original before comparing")
    if action == "ask_worker_reason" and (not state["purpose_difference_known"] or state["reason_heard"]):
        raise ValueError("Reason question is not available")
    if action == "dismount" and not state["letter_close_selected"]:
        raise ValueError("Letter input is incomplete")
    result.update(input=action, pending_input=None)
    if action not in result["completed_inputs"]:
        result["completed_inputs"].append(action)
        # Authored unique movement/detail inspection costs; retries/reviews cost 0.
        result["elapsed_minutes"] += {"dismount": 5, "inspect_original": 15, "inspect_rules": 15}.get(action, 0)
    if action == "close_letter": result["letter_close_selected"] = True
    if action == "dismount": result.update(carriage_stopped=True, location="gate")
    if action == "to_documents": result["location"] = "guardhouse"
    return result


def submission_block(state):
    if correct_submission(state):
        return PREFIX + ("S03_B004" if state["purpose_difference_known"] else "S03_B005")
    if set(state["selected"]) == {"passenger"}: return PREFIX + "S03_B007"
    # Any insufficient application/unsupported combination receives the existing
    # insufficiency response; never fall through to success or fabricate evidence.
    return PREFIX + "S03_B006"


def commit_record(state, block, record):
    if not allowed(state, block["id"]):
        raise ValueError("Block guard rejected: " + block["id"])
    if record not in block["records"]:
        raise ValueError("Record does not belong to block")
    # Author contract overrides always-block placement with actual document clicks.
    gates = {"MS14_D01_S03_L0002": "inspect_original", "MS14_D01_S03_L0007": "inspect_rules"}
    if record["id"] in gates and gates[record["id"]] not in state["completed_inputs"]:
        raise ValueError("Document must be inspected before acquiring")
    result = deepcopy(state)
    result["record"] = record["id"]
    for index, effect in enumerate(record["effects"]):
        kind, key = EFFECTS[effect]  # unknown effects fail closed
        token = record["id"] + ":" + str(index)
        if token in result["applied"]: continue
        if kind == "evidence":
            if key not in result["evidence"]: result["evidence"].append(key)
        else:
            result[key] = True
        result["applied"].append(token)
    return result
