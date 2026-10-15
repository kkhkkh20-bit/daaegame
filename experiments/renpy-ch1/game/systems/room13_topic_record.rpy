# Topic records (0.18.46, owner review).
#   - What was said on first reading is kept verbatim (r13_finish_topic(key, shown)). A review
#     shows that record, not lines rebuilt from the current state (Daram's presence, case state).
#   - A review opens short: when it was heard and the other person's own words (quoted, up to
#     three lines, longest first in their original order). No summary or inference is added.
#     "전체 대화 다시 보기" plays the whole kept record.
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
    if not r13_topic_record(key):
        call r13_lines(r13_conversation_topic_lines(key),"topic:review:"+key)
        return
    $ r13_review_npc=ROOM13["topics"][key]["npc"]
    call r13_lines([(None,r13_topic_when(key)+", "+R13_NAMES.get(r13_review_npc,r13_review_npc)+"에게 들은 이야기를 수첩에서 다시 본다.")]+
        [(None,R13_NAMES.get(who,who)+" · “"+text+"”") for who,text in r13_topic_key_lines(key)],"topic:record:"+key)
    menu:
        "전체 대화 다시 보기":
            call r13_lines(r13_topic_full_record(key),"topic:record_full:"+key)
        "그만 본다":
            pass
    return
