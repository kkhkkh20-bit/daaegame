# Residents with nothing to say right now (owner 2026-10-22: "대화하거나 제시할 게 없으면
# 혼잣말로 넘어가도 괜찮고, 기본 인사말이라도"). Tapping such a resident does not open the
# question sheet: the first tap of the day plays that resident's greeting
# (v111/newworld/greetings.json), later taps a short thought from Dad.
# "Nothing to say" = no option of the current scene for this person here, no unread follow-up
# question, and no specific evidence reaction left to see. Family members always open as before.
init 336 python:
    R13_GREETINGS=json.load(renpy.file("v111/newworld/greetings.json")) if renpy.loadable("v111/newworld/greetings.json") else {}
    R13_IDLE_THOUGHTS=(
        "지금은 더 물어볼 게 없겠지.",
        "바쁜 사람을 자꾸 붙잡지 말자. 물을 게 생기면 다시 오자.",
        "새로 알게 된 게 생기면 그때 다시 말을 걸어 보자.",
    )
    R13_IDLE_FAMILY=("daram","mom","dad")

    def r13_v111_has_business(person):
        here=store.room13["location"]
        if any(o.get("person")==person and o.get("location")==here for o in r13_v111_binding().get("options",[])):return True
        if any(not r13_followup_read(s["id"]) for s in r13_v111_followups(person)):return True
        for spec in R13_REACTIONS.get("present",[]):
            if spec["person"]==person and r13_v111_owned(spec["evidence"]) and r13_reaction_day_ok(spec) and not r13_v111_value("reacted:%s:%s"%(person,spec["evidence"])):
                return True
        return False

    def r13_v111_idle_ok(person):
        return r13_v111_active() and person not in R13_IDLE_FAMILY and not r13_v111_has_business(person)

    _r13_idle_present_reaction=r13_v111_present_reaction
    def r13_v111_present_reaction(person,shown):
        key=shown[5:] if isinstance(shown,str) and shown.startswith("V111:") else shown
        if any(s["person"]==person and s["evidence"]==key for s in R13_REACTIONS.get("present",[])):
            r13_v111_set("reacted:%s:%s"%(person,key),True)
        return _r13_idle_present_reaction(person,shown)

    def r13_v111_idle_lines(person):
        day=(store.room13 or {}).get("day",1)
        name=next((n for n,p in MS14_SPEAKERS.items() if p==person),None)
        rows=R13_GREETINGS.get(person) or []
        if name and rows and not r13_v111_value("greeted:%s:%s"%(day,person)):
            r13_v111_set("greeted:%s:%s"%(day,person),True)
            seen=r13_v111_value("greeted_count:"+person) or 0
            r13_v111_set("greeted_count:"+person,seen+1)
            row=rows[min(seen,len(rows)-1)]
            return [r13_nw_added_line(dict(speaker=name,text=row["text"],expression=row.get("expression","neutral"),kind="dialogue"))]
        count=(r13_v111_value("idle_count") or 0)
        r13_v111_set("idle_count",count+1)
        return [r13_nw_added_line(dict(speaker="아빠",text=R13_IDLE_THOUGHTS[count%len(R13_IDLE_THOUGHTS)],kind="thought"))]
