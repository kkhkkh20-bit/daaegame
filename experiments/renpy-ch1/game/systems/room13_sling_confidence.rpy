# Delayed requester disclosure is a new authored difficulty revision, not old canon.
# Own the final Sling-specific presentation/topic gates without replacing other routes.
init 206 python:
    def r13_sling_knows_requester():
        return any(r13_has(key) for key in ("H9","know_granny_reads","sling_confession_heard"))

    def r13_sling_papers_shown():
        state=store.room13 or {}
        owned=set(state.get("evidence",[]))
        shown={entry.split(":",1)[0] for entry in state.get("resident_knowledge",{}).get("resident_sling",[])}
        # Possession, portrait recognition, and this NPC's prior testimony are not
        # permission to read Dad's other papers. Each record must actually be shown.
        if "J06" in owned and "J06" in shown:return "J06"
        if {"E18","J08"}<=owned and {"E18","J08"}<=shown:return "E18+J08"
        return None

    def r13_sling_nonpaid_trust():
        return (r13_has("sling_nonpaid_trust") or r13_has("sling_reconciled")) and not r13_grudge_open("sling")

    def r13_sling_confront_ready():
        if r13_has("H9"):return False
        # A legacy save that actually heard the requester may restore its missing
        # written record through a new completed conversation, never from viewing.
        if r13_sling_knows_requester():return True
        return bool(r13_sling_papers_shown()) and r13_sling_nonpaid_trust()

    def r13_sling_protect_ready():
        return r13_has("sling_job_pressure_heard") and not r13_sling_nonpaid_trust() and not r13_grudge_open("sling")

    def r13_sling_fake_letter_ready():
        state=store.room13 or {}
        return (r13_sling_knows_requester() and state.get("case_state")=="pending"
            and 2<=state.get("day",1)<=R13_CASE_DAY and not r13_has("fake_letter_planted")
            and not r13_grudge_open("sling"))

    def r13_sling_confront_lines():
        # Pure final dialogue provider: the NPC sees only papers explicitly shown
        # to Sling. The known-save route never pretends those papers were presented.
        if not r13_sling_confront_ready():return []
        if r13_sling_knows_requester():
            opening=[("dad","전에 말씀하신 편지 일을 정확히 적어 두려고 합니다. 누구의 부탁이었습니까?")]
        elif r13_sling_papers_shown()=="J06":
            opening=[("dad","보여 드린 기록은 할머니가 아내 이름으로 온 편지를 썼다고 한 말입니다. 슬링 씨가 맡았던 편지 일과 관계가 있습니까?")]
        else:
            opening=[("dad","보여 드린 글에서 아내는 여관에 행선지를 알리지 말라고 했습니다. 슬링 씨는 그분의 편지를 보셨다고 했고요. 그때 어떤 일을 맡으셨습니까?")]
        return opening+[
            ("resident_sling","……여관 할머니가 시켰어요. 손님 편지 중에 ‘부인’이 보낸 게 있으면 베껴 오라고요. 안 하면 일자리를 잃는대요."),
            ("dad","그 지시를 받았다는 말씀만 적겠습니다. 왜 모으라고 했는지도 들으셨습니까?"),
            ("resident_sling","아뇨. 왜 필요한지는 말씀 안 하셨어요.")]

    ROOM13["topics"]["sling:protect_confidence"]=dict(npc="resident_sling",title="들은 사정을 퍼뜨리지 않겠다고 한다",
        day=[2,14],need=["sling_job_pressure_heard"],not_flags=[],give=[],flags=[],lines=[],
        discover_any=["sling_job_pressure_heard"])
    ROOM13["topics"]["sling:letter_requester"]=dict(npc="resident_sling",title="편지를 베끼라던 부탁을 확인한다",
        day=[2,14],need=[],not_flags=["H9"],give=[],flags=[],lines=[],
        discover_any=["sling_job_pressure_heard","know_granny_reads","sling_confession_heard"])
    ROOM13["topics"]["sling:fake_letter"]=dict(npc="resident_sling",title="가짜 약속 쪽지를 맡긴다",
        day=[2,14],need=[],not_flags=["fake_letter_planted"],give=[],flags=[],lines=[],
        discover_any=["H9","know_granny_reads","sling_confession_heard"])
    R13_TOPIC_LABELS.update({"sling:protect_confidence":"r13_sling_protect_confidence",
        "sling:letter_requester":"r13_sling_earned_confront", "sling:fake_letter":"r13_sling_fake_followup"})
    R13_CONTACT_RECORDS["resident_sling"]=tuple(dict.fromkeys(R13_CONTACT_RECORDS.get("resident_sling",())+("E18","J08","J06")))

    _r13_sling_confidence_topics=r13_topics
    def r13_topics(person):
        rows=_r13_sling_confidence_topics(person)
        if person!="resident_sling":return rows
        gates={"sling:protect_confidence":r13_sling_protect_ready,
               "sling:letter_requester":r13_sling_confront_ready,
               "sling:fake_letter":r13_sling_fake_letter_ready}
        return [(key,spec) for key,spec in rows if key not in gates or gates[key]()]

    _r13_sling_confidence_present=r13_present
    def r13_present(person,key,identity=False):
        if person!="resident_sling" or key not in ("E18","J08","J06") or not r13_has(key):
            return pb01_present_lines(key,identity) if person=="guard" and key.startswith("PB01:") and pb01_active() and r13_has(key) else _r13_sling_confidence_present(person,key,identity)
        # Preserve the actual presentation history and all unrelated lower-layer
        # effects. Merely computing an available-record list never calls this.
        _r13_sling_confidence_present(person,key,identity)
        if r13_sling_knows_requester():
            return [("resident_sling","전에 말씀드린 편지 일도 다시 확인하실 건가요?")]
        if r13_grudge_open("sling"):
            return [("resident_sling","그 기록은 봤어요. 하지만 저를 경비에게 알리셨잖아요. 지금은 더 말하고 싶지 않아요.")]
        first_pressure=not r13_has("sling_job_pressure_heard")
        pressure=[("resident_sling","편지 내용을 베껴 오라는 부탁은 받았어요. 하지만 누구 부탁인지는 말 못 해요. 일자리를 잃을까 봐요.")] if first_pressure else []
        r13_flag("sling_job_pressure_heard")
        if r13_sling_confront_ready():
            return pressure+[("resident_sling","……보여 주신 기록은 읽었어요. 제 사정도 들어 주셨으니, 편지 일도 이야기해 볼게요.")]
        if key=="J08":
            return pressure+[("resident_sling","제가 그분의 편지를 봤다는 말은 맞아요. 하지만 그 기록만으로 다른 일까지 말할 수는 없어요.")]
        return pressure+[("resident_sling","그 글은 읽었어요. 하지만 누구 부탁으로 일을 했는지는 아직 말 못 해요. 일자리를 잃을 수도 있어서요.")]

label r13_sling_protect_confidence:
    if not r13_sling_protect_ready():
        return
    call r13_lines([("dad","말씀하신 사정은 함부로 퍼뜨리지 않겠습니다. 말씀하지 않은 이름도 짐작해서 말하지 않겠습니다."),
        ("resident_sling","……그 약속은 지켜 주세요. 편지에 대해 확인할 건 듣겠습니다.")],"sling:confidence:promise")
    $ r13_flag("sling_nonpaid_trust")
    $ r13_finish_topic("sling:protect_confidence")
    return

label r13_sling_earned_confront:
    if not r13_sling_confront_ready():
        return
    menu:
        "편지 일을 끝까지 듣는다":
            $ _sling_confront_rows=r13_sling_confront_lines()
            if not _sling_confront_rows:
                return
            call r13_lines(_sling_confront_rows,"sling:confidence:confront", binding_route="dynamic:857")
            # Normal live return, including the game's explicit conversation skip,
            # completes this chosen encounter. Menu cancellation does not.
            $ r13_flag("sling_confront_completed")
            $ r13_sling_note_confession()
            $ store.r13_topic_shown=_sling_confront_rows
            $ r13_finish_topic("sling:letter_requester")
        "지금은 더 묻지 않는다":
            return
    return

label r13_sling_fake_followup:
    if not r13_sling_fake_letter_ready():
        return
    call r13_w1c_fake_letter
    if r13_has("fake_letter_planted"):
        $ r13_finish_topic("sling:fake_letter")
    return
