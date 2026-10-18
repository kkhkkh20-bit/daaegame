# Topic records (0.18.46, owner review).
#   - What was said on first reading is kept verbatim (r13_finish_topic(key, shown)). A review
#     shows that record, not lines rebuilt from the current state (Daram's presence, case state).
#   - Read historical questions replay the kept record. Live companion/corrected topics
#     use current lines while preserving the original transcript.
#   - Saves from before 0.18.46 have no record; they fall back to the older dated replay.
default r13_topic_shown = None

init 130 python:
    # Pure queries: current dialogue and archived testimony are separate.
    # Contexts are marked only by r13_finish_topic after the rows were displayed.
    def r13_topic_current_context(key):
        if key in R13_DARAM_HOME_KEYS:
            return r13_daram_home_context() if r13_daram_home_allowed(key) else None
        if key=="mystery:door" and r13_has("inn_claim_retracted"):return "door-retracted"
        if key=="nabi_alibi" and r13_has("E12"):return "nabi-gap-known"
        return None

    def r13_topic_current_fresh(key):
        context=r13_topic_current_context(key)
        if context is None:return False
        if key in R13_DARAM_HOME_KEYS:return not r13_daram_home_seen(key)
        return (store.room13 or {}).get("current_topic_contexts",{}).get(key)!=context

    _r13_current_topic_seen=r13_calendar_topic_seen
    def r13_calendar_topic_seen(key,spec):
        if key in ("mystery:door","nabi_alibi") and r13_topic_current_context(key) is not None:
            return not r13_topic_current_fresh(key)
        return _r13_current_topic_seen(key,spec)

    def r13_topic_current_lines(key):
        if key in R13_DARAM_HOME_KEYS:return r13_daram_home_lines(key)
        if key=="mystery:door":
            return [("dad","책장 뒤 문은 예전에 세탁물을 나르던 길이라고 하셨지요?"),
                ("granny","그래요. 손님이 쓰는 문은 아니라고 말씀드렸잖아요."),
                ("dad","손님용이 아니어도 방으로 들어가는 문이지요. 문이 하나뿐이라는 말씀과는 다릅니다."),
                ("granny","……오래 쓰지 않은 문까지 세어 말씀드린 건 아니에요.")]
        if key=="nabi_alibi":
            return [("dad","첫 비명이 났을 때부터 다시 확인할게. 그때는 할머니 곁에 있었지?"),
                ("nabi","네. 목도리 핀이 새것이라 뻑뻑해서 제가 대신 잠가 드렸어요."),
                ("dad","그 뒤, 공구를 가지러 주방에 가신 다음에는?"),
                ("nabi","그때부터는 못 봤어요. 저는 13호 문 앞에 있었고요."),
                ("dad","첫 비명 때 함께 있었다는 것과 그 뒤에도 계속 함께 있었다는 건 나눠 적을게."),
                ("nabi","네. 제가 직접 본 건 거기까지예요.")]
        return r13_conversation_topic_lines(key)

    def r13_topic_record(key):
        return (store.room13 or {}).get("topic_transcripts",{}).get(key)

    def r13_topic_when(key):
        stamp=(store.room13 or {}).get("dialogue_dates",{}).get(key)
        if not stamp:return "이전에"
        return "%d일째 %s"%(stamp["day"],("오전","오후","저녁","늦은 저녁")[min(3,stamp["period"])])

    def r13_topic_key_lines(key,limit=3):
        npc=ROOM13["topics"][key]["npc"]
        rows=[(i,who,text) for i,(who,text,thought) in enumerate(r13_topic_record(key) or []) if who==npc and not thought]
        keep=sorted(sorted(rows,key=lambda r:-len(r[2]))[:limit])
        return [(who,text) for i,who,text in keep]

    def r13_topic_full_record(key):
        return [(who,text,{"thought":True}) if thought else (who,text) for who,text,thought in r13_topic_record(key)]

label r13_topic_review(key):
    if r13_topic_record(key):
        call r13_lines(r13_topic_full_record(key),"topic:record_full:"+key, binding_route="dynamic:664")
    else:
        # Legacy saves keep the existing fallback when no verbatim transcript exists.
        call r13_lines(r13_conversation_topic_lines(key),"topic:review:"+key, binding_route="dynamic:665")
    return
