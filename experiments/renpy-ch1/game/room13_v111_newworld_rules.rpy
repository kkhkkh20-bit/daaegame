# New-world event rules that need more than text (owner-approved per event).
# Text for these paths lives in game/v111/newworld/dNN.json.
init 318 python:
    # Event 01 gate (plan A, 2026-10-21): one presentation. A half presentation
    # (application only) gets one more try; any other wrong answer is final and
    # Daram enters as '외 한 명' with no name on the record.
    R13_V111_ENTRY["MS14_D01_S04"]=([],{"gate_registered":False})
    def r13_nw_gate_entry_decided(previous=globals().get("R13_V111_SCENE_CHECKS",{}).get("MS14_D01_S04")):
        decided=r13_v111_value("gate_basis_proven") is True or r13_v111_value("gate_daram_unlisted") is True
        return decided and (previous is None or previous())
    if "R13_V111_SCENE_CHECKS" not in globals():R13_V111_SCENE_CHECKS={}
    R13_V111_SCENE_CHECKS["MS14_D01_S04"]=r13_nw_gate_entry_decided
    _r13_nw_rules_catalog_record=r13_catalog_record
    def r13_catalog_record(key):
        record=_r13_nw_rules_catalog_record(key)
        if record and r13_v111_active() and key=="V111:E05" and r13_v111_value("gate_daram_unlisted") is True:
            record=dict(record);record["establishes"]=R13_V111["evidence"]["E05"]["variants"]["unlisted"]
        return record

    # Meetings and the transfer list (plan 7). A meeting is decided once.
    R13_NW_MEETING_RESULTS=("win","partial","lose")
    def r13_nw_meeting_end(meeting,result):
        if result not in R13_NW_MEETING_RESULTS:raise Exception("Unknown meeting result: "+str(result))
        if r13_v111_value("meeting:"+meeting) is None:r13_v111_set("meeting:"+meeting,result)
        return r13_v111_value("meeting:"+meeting)
    R13_NW_LISTABLE=("resident_tok","bami","resident_bori","nabi","daram","resident_owlgp","resident_piko","resident_siluk","resident_guldol","resident_teacher","mom","dad")
    def r13_nw_list(person,reason):
        """Write a name on the school transfer list (the 13th cart takes them)."""
        if person not in R13_NW_LISTABLE:raise Exception("Person cannot be listed: "+str(person))
        if r13_v111_value("listed:"+person):return False
        r13_v111_set("listed:"+person,True)
        r13_v111_set("listed_reason:"+person,reason)
        r13_v111_set("listed_order",list(r13_v111_value("listed_order") or [])+[person])
        return True
    def r13_nw_listed():
        return [p for p in (r13_v111_value("listed_order") or []) if r13_v111_value("listed:"+p)]

    # Event 03 lamp meeting: evening scene opens after a partial or lost meeting too.
    R13_V111_ENTRY["MS14_D03_S06"]=([],{"stone_choice_completed":True})
    def r13_nw_lamp_evening_ready(previous=R13_V111_SCENE_CHECKS.get("MS14_D03_S06")):
        decided=r13_v111_value("lamp_theft_supported") is True or r13_v111_value("meeting:lamp") in ("partial","lose")
        return decided and (previous is None or previous())
    R13_V111_SCENE_CHECKS["MS14_D03_S06"]=r13_nw_lamp_evening_ready
