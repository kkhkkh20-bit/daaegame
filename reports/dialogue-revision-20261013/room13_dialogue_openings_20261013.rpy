# Dialogue routing only. Existing encounter records remain the source of truth.
default r13_first_encounter = False
default r13_opening_lines = []

init 58 python:
    import json as r13_opening_json
    R13_OPENING_SCENES = r13_opening_json.load(renpy.file("room13-dialogue-openings.json"))

    def r13_conversation_opening(person, first):
        spec = R13_OPENING_SCENES["first_meetings"].get(person)
        if spec is None:
            return []
        if not first:
            return spec["revisit"]
        state = store.room13
        early = state["day"] <= 3 and state["case_state"] == "pending"
        return spec["early" if early else "late"]

    def r13_conversation_topic_lines(key):
        state = store.room13
        # Optional companion speech does not alter topic visibility or evidence.
        with_child = state["daram_state"] in ("with_dad", "rescued")
        variants = R13_OPENING_SCENES["with_daram"]
        if with_child and key in variants:
            return variants[key]
        return ROOM13["topics"][key]["lines"]
