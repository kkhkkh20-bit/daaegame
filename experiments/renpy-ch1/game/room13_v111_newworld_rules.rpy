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

    # Half presentation (plan 7-2): some of the right records, none wrong.
    def r13_nw_half(correct):
        given=set(getattr(store,"v111_last_presented",None) or [])
        want=set("V111:"+k for k in correct)
        return bool(given) and given<want

    # Event 04 gate-post meeting: day 5 afternoon also follows a lost meeting.
    R13_V111_ENTRY["MS14_D05_S04"]=([],{})
    def r13_nw_gate_post_after(previous=R13_V111_SCENE_CHECKS.get("MS14_D05_S04")):
        return r13_v111_value("bami_status") in ("cleared","listed") and (previous is None or previous())
    R13_V111_SCENE_CHECKS["MS14_D05_S04"]=r13_nw_gate_post_after

    # Event 05 fire meeting: the school scene also follows a lost meeting (Bori blamed).
    def r13_nw_fire_school_ready(previous=R13_V111_SCENE_CHECKS.get("MS14_D07_S02")):
        return (previous is not None and previous()) or r13_v111_value("meeting:fire")=="lose"
    R13_V111_SCENE_CHECKS["MS14_D07_S02"]=r13_nw_fire_school_ready

    # Endings (plan 11-1). Checked on the 14th morning before the kept endings.
    # The five lives the frozen-village ending counts.
    R13_NW_LIVES=(("resident_piko","piko_alive"),("kid_kkomi","KKOMI_ALIVE"),("resident_owlgp","OWL_ALIVE"),("resident_nero","nero_alive"),("kid_dodam","alive:kid_dodam"))
    R13_NW_FROZEN_AT=4
    def r13_nw_is_dead(who,key):
        if r13_v111_value(key) is False:return True
        return who=="kid_dodam" and r13_v111_value("route12")=="late_exposure"
    def r13_nw_dead():
        return [who for who,key in R13_NW_LIVES if r13_nw_is_dead(who,key)]
    def r13_nw_loss_count():
        return len(r13_nw_dead())
    def r13_nw_ending14():
        if r13_v111_value("departed:daram"):return "left_name"
        if r13_nw_loss_count()>=R13_NW_FROZEN_AT:return "frozen"
        outcome=r13_v111_value("outcome13")
        if outcome=="family_priority":return "family"
        if outcome=="partial_rescue":return "partial"
        if r13_v111_value("crowd_injury"):return "violence"
        return "morning"
    def r13_nw_true_ending_ready():
        """Plan 11-1 #6: all five alive, records/hypothesis/blanket/altar won, Neoul's ledger held."""
        if r13_v111_value("ending14")!="morning" or r13_nw_loss_count():return False
        if not r13_v111_owned("NW_NEOUL_LEDGER"):return False
        return all(r13_v111_value("meeting:"+m)=="win" for m in ("records","hypothesis","blanket","altar"))

    # Three chances per meeting (owner decision 2026-10-22, replaces "one presentation").
    # A wrong answer shows the rebuttal and costs a chance; the third wrong answer stands.
    R13_NW_TRIES=3
    def r13_nw_tries_left(meeting):
        return max(0,R13_NW_TRIES-(r13_v111_value("tries:"+meeting) or 0))
    def r13_nw_retry(meeting,correct=None,note=None):
        """True (and one chance used) when this wrong answer may be tried again."""
        if r13_v111_value("meeting:"+meeting) is not None:return False
        used=(r13_v111_value("tries:"+meeting) or 0)+1
        r13_v111_set("tries:"+meeting,used)
        left=R13_NW_TRIES-used
        if left<=0:return False
        hint=note if (note and correct and r13_nw_half(correct)) else "맞지 않는다."
        renpy.notify("%s 남은 기회 %d번."%(hint,left))
        return True

    # Review 2026-10-22: a person who left on the cart (departed:<p>) is never placed again.
    _r13_nw_arrive=r13_v111_arrive
    def r13_v111_arrive(people):
        return _r13_nw_arrive([p for p in people if not r13_v111_value("departed:"+p)])
    _r13_nw_binding=r13_v111_binding
    def r13_v111_binding():
        b=_r13_nw_binding()
        if b.get("people"):b=dict(b,people=[p for p in b["people"] if not r13_v111_value("departed:"+p)])
        return b
