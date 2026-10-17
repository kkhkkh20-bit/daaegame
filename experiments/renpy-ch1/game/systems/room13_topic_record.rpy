# Topic records (0.18.46, owner review).
#   - What was said on first reading is kept verbatim (r13_finish_topic(key, shown)). A review
#     shows that record, not lines rebuilt from the current state (Daram's presence, case state).
#   - Clicking a read question immediately replays the kept record, without a summary or extra menu.
#   - Saves from before 0.18.46 have no record; they fall back to the older dated replay.
default r13_topic_shown = None

init 130 python:
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
