# Dialogue routing only. Existing encounter records remain the source of truth.
default r13_carriage_snack = False
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
        if not early:
            return spec["late"]
        with_child = state["daram_state"] in ("with_dad", "rescued")
        return spec["early" if with_child else "early_solo"]

    def r13_conversation_topic_lines(key):
        state = store.room13
        # Optional companion speech does not alter topic visibility or evidence.
        with_child = state["daram_state"] in ("with_dad", "rescued")
        variants = R13_OPENING_SCENES["with_daram"]
        if with_child and key in variants:
            return variants[key]
        return ROOM13["topics"][key]["lines"]


    def r13_resident_notice(person):
        spec = R13_OPENING_SCENES["first_meetings"][person]
        state = store.room13
        special = R13_OPENING_SCENES["special_notices"]
        if person == "buri" and state["victim_state"] == "dead":
            return special["buri_bereaved"]
        if person == "bami" and r13_has("bami_pressured"):
            return special["bami_pressured"]
        early = state["day"] <= 3 and state["case_state"] == "pending"
        if not early:
            return spec["notice_late"]
        with_child = state["daram_state"] in ("with_dad", "rescued")
        return spec["notice_child" if with_child else "notice_solo"]

# Seeing a resident does not record a meeting, grant evidence, or advance time.
# Separate return labels keep existing saved call stacks stable.
label r13_notice_before_talk(person):
    if person not in R13_OPENING_SCENES["first_meetings"] or person in r13_met_people():
        return True
    if not r13_has("noticed:" + person):
        $ r13_notice_rows = r13_resident_notice(person)
        call r13_lines(r13_notice_rows, "notice:resident:" + person) from r13_notice_lines_return
        $ r13_flag("noticed:" + person)
    $ r13_notice_approach = R13_OPENING_SCENES["first_meetings"][person]["approach"]
    call screen r13_resident_approach(r13_notice_approach)
    return _return

screen r13_resident_approach(approach):
    modal True
    zorder 40
    style_prefix "r13"
    add Solid("#00000066")
    frame:
        area (320,250,920,220) padding (24,24)
        background R13ActionPanel()
        vbox:
            spacing 18
            textbutton approach:
                action Return(True) xsize 872 yminimum 76 text_size 24
            textbutton "지금은 말을 걸지 않는다":
                action Return(False) xsize 872 yminimum 76 text_size 24
