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
            row=rows[-1]  # the working line; greetings (row 0) read as if meeting anew
            return [r13_nw_added_line(dict(speaker=name,text=row["text"],expression=row.get("expression","neutral"),kind="dialogue"))]
        count=(r13_v111_value("idle_count") or 0)
        r13_v111_set("idle_count",count+1)
        return [r13_nw_added_line(dict(speaker="아빠",text=R13_IDLE_THOUGHTS[count%len(R13_IDLE_THOUGHTS)],kind="thought"))]

# First meeting (owner 2026-10-22: "다들 나를 본것처럼 이야기하는데?"): a resident who has not yet
# spoken with Dad in this run greets him as a stranger; their own greeting starts after that.
# Everyone who speaks a line is remembered in r13_met_people (saved with the game).
default r13_met_people = set()
init 346 python:
    _r13_met_line_art=r13_ep_line_art
    def r13_ep_line_art(packet):
        who=packet[0] if packet else None
        if isinstance(who,str) and who not in ("dad",):
            met=set(store.r13_met_people or ())
            if who not in met:
                met.add(who);store.r13_met_people=met
        return _r13_met_line_art(packet)
    _r13_met_idle_lines=r13_v111_idle_lines
    def r13_v111_idle_lines(person):
        if person not in (store.r13_met_people or ()) and person in R13_GREETINGS:
            name=next((n for n,p in MS14_SPEAKERS.items() if p==person),None)
            if name:
                # Owner 2026-10-22: "처음에 다 인사하는것도 웃기고". A stranger does not greet; they
                # glance over and keep working. Their own lines start once they have spoken with Dad.
                day=(store.room13 or {}).get("day",1)
                r13_v111_set("greeted:%s:%s"%(day,person),True)
                josa="은" if (ord(name[-1])-0xAC00)%28 else "는"
                if not (0xAC00<=ord(name[-1])<=0xD7A3):josa="은"
                return [r13_nw_added_line(dict(speaker=None,text="%s%s 이쪽을 힐끗 보고는 하던 일을 계속한다."%(name,josa),kind="narration"))]
        return _r13_met_idle_lines(person)

# Evidence with no fitting reaction (owner 2026-10-22: "다람이에게 편지 보내주기했는데 아무반응 없이
# 조사하기 화면으로 이동함"): Daram answers in her own voice; anyone else without a reply gets a short
# thought from Dad instead of a passing notification.
init 347 python:
    R13_DARAM_PRESENT={
        "E01":("엄마 편지잖아. 나 벌써 다 외웠어!","anxious"),
    }
    R13_DARAM_GENERIC=(
        ("그거 왜 나한테 보여 줘? 난 다 봤는데.","flustered"),
        ("음…… 그건 아빠가 더 잘 알잖아.","neutral"),
        ("그거 아빠 수첩에 적어 둬. 나중에 같이 보자.","neutral"),
    )
    R13_PRESENT_NOTHING=("지금 이걸 보여 줘도 더 들을 말은 없겠다.","이건 다른 사람에게 물어봐야겠다.")
    _r13_present_fallback=r13_v111_present_reaction
    def r13_v111_present_reaction(person,shown):
        lines=_r13_present_fallback(person,shown)
        if lines:return lines
        key=shown[5:] if isinstance(shown,str) and shown.startswith("V111:") else shown
        if person=="daram":
            text,exp=R13_DARAM_PRESENT.get(key) or R13_DARAM_GENERIC[sum(ord(c) for c in str(key))%len(R13_DARAM_GENERIC)]
            return [r13_nw_added_line(dict(speaker="다람",text=text,expression=exp,kind="dialogue"))]
        text=R13_PRESENT_NOTHING[sum(ord(c) for c in str(key))%len(R13_PRESENT_NOTHING)]
        return [r13_nw_added_line(dict(speaker="아빠",text=text,kind="thought"))]
