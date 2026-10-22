# Residents react to what the player has found (owner-approved plan 2026-10-22, item 3:
# "알아낸 만큼 주민의 말이 달라지게"). Data: game/v111/newworld/reactions.json
#   present   [{person, evidence, days:[from,to], lines:[row]}]   shown evidence -> reaction lines
#   followups [{id, person, after, days, title, lines:[row]}]      a new question once `after` is owned
#   generic   {person: [{text, expression}]}                       unrelated evidence, in their own voice
# Rows use the new-world line format (speaker Korean name or null, text, expression, fx).
# Presentation and dialogue only: no story values change except the follow-up "read" marks.
init 335 python:
    R13_REACTIONS=json.load(renpy.file("v111/newworld/reactions.json")) if renpy.loadable("v111/newworld/reactions.json") else dict(present=[],followups=[],generic={})
    R13_REACTION_EXPRESSIONS=("neutral","joy","angry","anxious","surprise","flustered")

    def r13_reaction_problems():
        out=[];people=set(MS14_SPEAKERS.values())
        def rows(where,lines):
            for row in lines:
                if row.get("speaker") is not None and row["speaker"] not in MS14_SPEAKERS:out.append(where+": unknown speaker "+str(row.get("speaker")))
                if not row.get("text"):out.append(where+": empty line")
                if row.get("expression","neutral") not in R13_REACTION_EXPRESSIONS:out.append(where+": bad expression")
                if row.get("fx") and row["fx"] not in R13_NW_FX:out.append(where+": bad fx")
        for spec in R13_REACTIONS.get("present",[]):
            where="present %s %s"%(spec.get("person"),spec.get("evidence"))
            if spec.get("person") not in people:out.append(where+": unknown person")
            if spec.get("evidence") not in R13_V111["evidence"]:out.append(where+": unknown evidence")
            rows(where,spec.get("lines",[]))
        seen=set()
        for spec in R13_REACTIONS.get("followups",[]):
            where="followup "+str(spec.get("id"))
            if spec.get("id") in seen:out.append(where+": repeated id")
            seen.add(spec.get("id"))
            if spec.get("person") not in people:out.append(where+": unknown person")
            if spec.get("after") not in R13_V111["evidence"]:out.append(where+": unknown evidence")
            if not spec.get("title"):out.append(where+": no title")
            rows(where,spec.get("lines",[]))
        for person,lines in R13_REACTIONS.get("generic",{}).items():
            if person not in people:out.append("generic: unknown person "+person)
        return out
    _r13_reaction_issues=r13_reaction_problems()
    if _r13_reaction_issues:raise Exception("reactions.json is inconsistent: "+"; ".join(_r13_reaction_issues[:8]))

    def r13_reaction_day_ok(spec):
        days=spec.get("days") or [1,14]
        day=(store.room13 or {}).get("day",1)
        return days[0]<=day<=days[-1]

    def r13_reaction_packets(lines):
        out=[]
        for row in lines:
            who=MS14_SPEAKERS.get(row["speaker"]) if row.get("speaker") is not None else None
            if who and who not in ("dad",) and not r13_v111_person_alive(who):return []
            out.append(r13_nw_added_line(dict(row,kind="dialogue")))
        return out

    def r13_v111_present_reaction(person,shown):
        """Lines for showing `shown` (a "V111:" record id) to `person`, or None."""
        key=shown[5:] if isinstance(shown,str) and shown.startswith("V111:") else shown
        for spec in R13_REACTIONS.get("present",[]):
            if spec["person"]==person and spec["evidence"]==key and r13_reaction_day_ok(spec):
                packets=r13_reaction_packets(spec["lines"])
                if packets:return packets
        generic=R13_REACTIONS.get("generic",{}).get(person) or []
        if generic:
            # Same evidence, same person -> same answer (stable, no random reroll on reload).
            row=generic[sum(ord(ch) for ch in str(key)) % len(generic)]
            return [r13_nw_added_line(dict(speaker=next(n for n,p in MS14_SPEAKERS.items() if p==person),text=row["text"],expression=row.get("expression","neutral"),kind="dialogue"))]
        return None

    def r13_followup_read(fid):
        return bool(r13_v111_value("followup_read:"+fid))

    def r13_v111_followups(person):
        return [spec for spec in R13_REACTIONS.get("followups",[])
                if spec["person"]==person and r13_v111_owned(spec["after"]) and r13_reaction_day_ok(spec)]

    _r13_reaction_questions=r13_v111_questions
    def r13_v111_questions(person):
        rows=list(_r13_reaction_questions(person))
        for spec in r13_v111_followups(person):
            read=r13_followup_read(spec["id"])
            title=spec["title"] if read else "{color=#e0707a}새{/color}  "+spec["title"]
            rows.append((title,Return(("followup",spec["id"])),read))
        return rows

    def r13_v111_followup_lines(fid):
        spec=next((s for s in R13_REACTIONS.get("followups",[]) if s["id"]==fid),None)
        if spec is None:return []
        r13_v111_set("followup_read:"+fid,True)
        return r13_reaction_packets(spec["lines"])
