# New-world dialogue layer (2026-10-21 rework plan, "새 세계관 대사판").
# The authored V1.1.1 records stay exactly as imported (test_v111 checks them).
# Owner-reviewed revisions live in game/v111/newworld/dNN.json and are applied
# here, by record ID only:
#   replace  {rid: {"text": ..., "when"?: name}}   new sentence for an authored line (only while when holds)
#   before / after  {rid: [line, ...]}             new lines around an authored line
#   drop     [rid | {"id": rid, "when": name}, ...]  authored line not shown (while when holds)
#   evidence {key: {"name": ..., "variants": {variant: text}, "add_variants": {new: text}}}
#   new_evidence {"NW_...": {"name": ..., "kind": "물증|기록|관찰기록|증언", "variants": {variant: text}}}
#            a record that only the new world has; the generators acquire it with r13_nw_acquire
#   blocks   {name: [line, ...]}                     new-world lines with no authored record
#            (new meetings); the generators show them with r13_nw_block(name)
# A new line: {"id": "NW_...", "speaker": name|null, "text": ..., "kind"?: dialogue|narration|thought, "expression"?,
#              (thought: the father's unspoken line; text without brackets, the engine adds them)
#              "when"?: condition name in R13_NW_WHEN, "cut"?: existing ep art name}
# Conditions are named Python predicates, never evaluated strings.
# With every file empty the game shows the same lines in the same order as before.
init 319 python:
    R13_NW_TEXT_DAYS=["d%02d"%n for n in range(1,15)]
    R13_NW_TEXT=dict(replace={},before={},after={},drop=[],evidence={},new_evidence={},blocks={})
    for _nw_day in R13_NW_TEXT_DAYS:
        _nw_path="v111/newworld/%s.json"%_nw_day
        if not renpy.loadable(_nw_path):continue
        with renpy.file(_nw_path) as _nw_file:_nw_part=json.load(_nw_file)
        for _nw_key in ("replace","before","after","evidence","new_evidence","blocks"):
            for _nw_rid,_nw_value in _nw_part.get(_nw_key,{}).items():
                if _nw_rid in R13_NW_TEXT[_nw_key]:raise Exception("Duplicate new-world entry: %s %s"%(_nw_key,_nw_rid))
                R13_NW_TEXT[_nw_key][_nw_rid]=_nw_value
        R13_NW_TEXT["drop"]+=list(_nw_part.get("drop",[]))
    # New-world records join the V1.1.1 catalog before anything checks references.
    for _nw_key,_nw_spec in R13_NW_TEXT["new_evidence"].items():
        if not _nw_key.startswith("NW_") or _nw_key in R13_V111["evidence"]:raise Exception("Bad new-world evidence key: "+_nw_key)
        if _nw_spec.get("kind") not in R13_RECORD_CATEGORIES or not _nw_spec.get("name") or not _nw_spec.get("variants"):raise Exception("Incomplete new-world evidence: "+_nw_key)
        R13_V111["evidence"][_nw_key]=dict(name=_nw_spec["name"],kind=_nw_spec["kind"],variants=dict(_nw_spec["variants"]))
        ROOM13["evidence"]["V111:"+_nw_key]=dict(id="V111:"+_nw_key,name=_nw_spec["name"],kind=_nw_spec["kind"],establishes=next(iter(_nw_spec["variants"].values())),does_not_establish="",current_run_only=True,retained_on_show=True,scenes=[])
        R13_RECORD_SHORT["V111:"+_nw_key]=_nw_spec["name"]
    def r13_nw_acquire(key,variant="observed"):
        """Give a new-world record once (same path as an authored 'acquire')."""
        if key not in R13_NW_TEXT["new_evidence"]:raise Exception("Unknown new-world evidence: "+str(key))
        if variant not in R13_V111["evidence"][key]["variants"]:raise Exception("Unknown new-world evidence variant: %s %s"%(key,variant))
        r13_v111_apply("nw:acquire:"+key,[dict(op="acquire",key=key,variant=variant)])
    # Named conditions for added lines. Add one line here when an event needs it.
    R13_NW_WHEN={
        "always":lambda:True,
        "owl_alive":lambda:r13_v111_value("OWL_ALIVE") is not False,
        "owl_dead":lambda:r13_v111_value("OWL_ALIVE") is False,
        "piko_alive":lambda:r13_v111_value("piko_alive") is not False,
        "piko_dead":lambda:r13_v111_value("piko_alive") is False,
        "kkomi_alive":lambda:r13_v111_value("KKOMI_ALIVE") is not False,
        "kkomi_dead":lambda:r13_v111_value("KKOMI_ALIVE") is False,
        "daram_free":lambda:not r13_v111_value("DARAM_DETAINED"),
        # Event 01: lost gate proof, Daram entered as '외 한 명' (owner plan A, 2026-10-21).
        "gate_daram_unlisted":lambda:r13_v111_value("gate_daram_unlisted") is True,
        "gate_daram_listed":lambda:r13_v111_value("gate_daram_unlisted") is not True,
        # Event 03: the day-3 lamp meeting (win / partial / lose).
        "lamp_win":lambda:r13_v111_value("meeting:lamp")=="win",
        "lamp_partial":lambda:r13_v111_value("meeting:lamp")=="partial",
        "lamp_lose":lambda:r13_v111_value("meeting:lamp")=="lose",
        "lamp_not_win":lambda:r13_v111_value("meeting:lamp") in ("partial","lose"),
        # Event 04: the day-5 gate-post meeting.
        "gate_post_lose":lambda:r13_v111_value("meeting:gate_post")=="lose",
        "gate_post_half":lambda:(r13_v111_value("tries:gate_post") or 0)>0 and r13_v111_value("meeting:gate_post") is None,
        # Event 05: the day-7 fire meeting.
        "fire_win":lambda:r13_v111_value("meeting:fire")=="win",
        "fire_partial":lambda:r13_v111_value("meeting:fire")=="partial",
        "fire_lose":lambda:r13_v111_value("meeting:fire")=="lose",
        "fire_not_lose":lambda:r13_v111_value("meeting:fire")!="lose",
        # Events 06-07: the day-7 room 13 night and the day-10 meetings.
        "prevention_a":lambda:r13_v111_value("prevention")=="A",
        "prevention_b":lambda:r13_v111_value("prevention")=="B",
        "room13_win":lambda:r13_v111_value("meeting:room13")=="win",
        "room13_partial":lambda:r13_v111_value("meeting:room13")=="partial",
        "room13_lose":lambda:r13_v111_value("meeting:room13")=="lose",
        "room13_not_win":lambda:r13_v111_value("meeting:room13") in ("partial","lose"),
        "room13_partial_unknown":lambda:r13_v111_value("meeting:room13")=="partial" and r13_v111_value("room13_partial_kind")=="unknown",
        "room13_partial_accident":lambda:r13_v111_value("meeting:room13")=="partial" and r13_v111_value("room13_partial_kind")=="accident",
        "records_win":lambda:r13_v111_value("meeting:records")=="win",
        "records_partial":lambda:r13_v111_value("meeting:records")=="partial",
        "records_lose":lambda:r13_v111_value("meeting:records")=="lose",
        "records_not_lose":lambda:r13_v111_value("meeting:records")!="lose",
        # Event 08: the day-11 facility and the hypothesis meeting.
        "guldol_ready":lambda:r13_v111_actor_ready("resident_guldol"),
        "guldol_absent":lambda:not r13_v111_actor_ready("resident_guldol"),
        "guldol_listed":lambda:r13_v111_value("listed:resident_guldol") is True,
        "hyp_win":lambda:r13_v111_value("meeting:hypothesis")=="win",
        "hyp_partial":lambda:r13_v111_value("meeting:hypothesis")=="partial",
        "hyp_lose":lambda:r13_v111_value("meeting:hypothesis")=="lose",
        "hyp_not_lose":lambda:r13_v111_value("meeting:hypothesis") in ("win","partial"),
        "hyp_lost1":lambda:r13_v111_value("hyp_issue:1")=="lost",
        "hyp_lost2":lambda:r13_v111_value("hyp_issue:2")=="lost",
        "hyp_lost3":lambda:r13_v111_value("hyp_issue:3")=="lost",
        "hyp_lost4":lambda:r13_v111_value("hyp_issue:4")=="lost",
        # Event 09: the day-12 soup.
        "soup_late":lambda:r13_v111_value("route12")=="late_exposure",
        "soup_lose_stolen":lambda:r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="stolen",
        "soup_lose_nabi":lambda:r13_v111_value("meeting:soup")=="lose" and r13_v111_value("soup_lose_kind")=="nabi",
        # Event 10: the day-13 cart.
        "daram_deal_freed":lambda:r13_v111_value("daram_deal_freed") is True,
        "cart_departed":lambda:r13_v111_value("cart_departed") is True,
        "daram_departed":lambda:r13_v111_value("departed:daram") is True,
        "neoul_held":lambda:r13_v111_value("neoul_held") is True,
        # Event 11: the altar, Bomi, and the endings.
        "has_ledger":lambda:r13_v111_owned("NW_NEOUL_LEDGER"),
        "no_ledger":lambda:not r13_v111_owned("NW_NEOUL_LEDGER"),
        "has_burnt_page":lambda:r13_v111_owned("NW_BURNT_PAGE"),
        "altar_win":lambda:r13_v111_value("meeting:altar")=="win",
        "altar_partial":lambda:r13_v111_value("meeting:altar")=="partial",
        "altar_lose":lambda:r13_v111_value("meeting:altar")=="lose",
        "altar_half1":lambda:r13_v111_value("altar_half1") is True,
        "family_priority":lambda:r13_v111_value("outcome13")=="family_priority",
        "ending_morning":lambda:r13_v111_value("ending14")=="morning",
        "reader_nabi":lambda:not (r13_v111_value("departed:nabi") or not r13_v111_person_alive("nabi")),
        "reader_tosil":lambda:bool(r13_v111_value("departed:nabi") or not r13_v111_person_alive("nabi")),
        "granny_held_win":lambda:r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="win",
        "granny_room13_partial":lambda:r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="partial",
        "granny_room13_lose":lambda:r13_v111_value("OWL_ALIVE") is False and r13_v111_value("meeting:room13")=="lose",
    }
    # One condition per person who can be on the transfer list (same names as R13_NW_LISTABLE).
    R13_NW_LIST_NAMES=("resident_tok","bami","resident_bori","nabi","daram","resident_owlgp","resident_piko","resident_siluk","resident_guldol","resident_teacher","mom","dad")
    for _nw_person in R13_NW_LIST_NAMES:
        R13_NW_WHEN["listed:"+_nw_person]=(lambda p=_nw_person:r13_v111_value("listed:"+p) is True)
    R13_NW_CUT_SPECIAL=("bell","v111_blanket_before","v111_blanket_after")
    def r13_nw_drop_item(item):
        return (item,"always") if isinstance(item,str) else (item.get("id"),item.get("when","always"))
    def r13_nw_dropped(rid):
        return any(r==rid and R13_NW_WHEN[w]() for r,w in (r13_nw_drop_item(i) for i in R13_NW_TEXT["drop"]))
    def r13_nw_text_problems():
        """Every broken reference in the loaded files, as readable strings."""
        out=[];records=R13_V111["records"];seen=set()
        for rid in R13_NW_TEXT["replace"]:
            if rid not in records:out.append("replace: unknown record "+rid)
            elif not R13_NW_TEXT["replace"][rid].get("text"):out.append("replace: empty text "+rid)
            elif R13_NW_TEXT["replace"][rid].get("when","always") not in R13_NW_WHEN:out.append("replace: unknown condition "+rid)
        for item in R13_NW_TEXT["drop"]:
            rid,when=r13_nw_drop_item(item)
            if rid not in records:out.append("drop: unknown record "+str(rid))
            if when not in R13_NW_WHEN:out.append("drop: unknown condition "+str(rid))
        for where in ("before","after","blocks"):
            for rid,rows in R13_NW_TEXT[where].items():
                if where!="blocks" and rid not in records:out.append(where+": unknown record "+rid)
                if where=="blocks" and not rows:out.append("blocks: empty block "+rid)
                for row in rows:
                    nid=row.get("id","")
                    if not nid.startswith("NW_") or nid in seen or nid in records:out.append(where+": bad or repeated id "+repr(nid))
                    seen.add(nid)
                    if not row.get("text"):out.append(where+": empty text "+nid)
                    if row.get("kind","dialogue") not in ("dialogue","narration","thought"):out.append(where+": unknown kind %s %s"%(nid,row.get("kind")))
                    if row.get("kind")=="thought" and (row.get("speaker")!="아빠" or row["text"].startswith("(")):out.append(where+": thought must be the father's, without brackets "+nid)
                    if row.get("speaker") is not None and row["speaker"] not in MS14_SPEAKERS:out.append(where+": unknown speaker %s %s"%(nid,row["speaker"]))
                    if row.get("when","always") not in R13_NW_WHEN:out.append(where+": unknown condition %s %s"%(nid,row.get("when")))
                    cut=row.get("cut")
                    if cut and cut not in R13_NW_CUT_SPECIAL and not renpy.loadable("assets/room13-ep-%s.webp"%cut):out.append(where+": missing cut art %s %s"%(nid,cut))
        for key in R13_NW_TEXT["evidence"]:
            if key not in R13_V111["evidence"]:out.append("evidence: unknown key "+key)
        return out
    _nw_problems=r13_nw_text_problems()
    if _nw_problems:raise Exception("New-world text files are inconsistent: "+"; ".join(_nw_problems[:8]))

    _r13_nw_authored_line=r13_v111_line
    def r13_v111_line(rid):
        packet=_r13_nw_authored_line(rid)
        revised=R13_NW_TEXT["replace"].get(rid)
        if revised and R13_NW_WHEN[revised.get("when","always")]():packet=(packet[0],revised["text"])+tuple(packet[2:])
        return packet
    def r13_nw_added_line(row):
        if row.get("kind")=="thought":
            # The father's unspoken thought, shown like the authored thought lines.
            return ("dad","("+row["text"]+")",dict(no_lead=True,thought=True,expression="thinking",pose="thinking"))
        who=MS14_SPEAKERS.get(row.get("speaker")) if row.get("speaker") is not None else None
        if who and not r13_v111_person_alive(who):raise Exception("Absent/dead new-world speaker: "+row["id"])
        slot=row.get("expression") or "neutral"
        options=dict(no_lead=True,expression=slot,pose=slot)
        if row.get("cut"):options["cut"]=row["cut"]
        return (who,row["text"],options)
    def r13_v111_lines(rids):
        """Authored lines with the reviewed new-world revisions around them."""
        out=[]
        for rid in rids:
            for row in R13_NW_TEXT["before"].get(rid,()):
                if R13_NW_WHEN[row.get("when","always")]():out.append(r13_nw_added_line(row))
            if not r13_nw_dropped(rid):
                packet=r13_v111_line(rid)
                # The authored record rides with its line, so approved per-line art
                # still finds it after lines are added before it or its text changes.
                out.append((packet[0],packet[1],dict(packet[2],line_id=rid))+tuple(packet[3:]))
            for row in R13_NW_TEXT["after"].get(rid,()):
                if R13_NW_WHEN[row.get("when","always")]():out.append(r13_nw_added_line(row))
        return out
    def r13_nw_block(name):
        """Lines of a new-world block (a new meeting) whose conditions hold."""
        if name not in R13_NW_TEXT["blocks"]:raise Exception("Unknown new-world block: "+str(name))
        return [r13_nw_added_line(row) for row in R13_NW_TEXT["blocks"][name] if R13_NW_WHEN[row.get("when","always")]()]
    _r13_nw_context_match=r13_dialogue_context_match
    def r13_dialogue_context_match(identity,index,packet,pose):
        rid=packet[2].get("line_id") if len(packet)>2 and isinstance(packet[2],dict) else None
        if not rid:return _r13_nw_context_match(identity,index,packet,pose)
        if pose not in R13_FULLBODY_PLAIN:return None
        for cue in R13_DIALOGUE_CONTEXT_ART["bindings"]:
            if cue.get("line_id")==rid and cue["identity"]==identity and cue["person"]==packet[0]:
                return cue
        return None
    for _nw_key,_nw_spec in R13_NW_TEXT["evidence"].items():
        _nw_rid="V111:"+_nw_key
        if _nw_spec.get("name"):
            ROOM13["evidence"][_nw_rid]["name"]=_nw_spec["name"]
            R13_RECORD_SHORT[_nw_rid]=_nw_spec["name"]
        for _nw_variant,_nw_text in _nw_spec.get("variants",{}).items():
            if _nw_variant not in R13_V111["evidence"][_nw_key]["variants"]:raise Exception("Unknown evidence variant: %s %s"%(_nw_key,_nw_variant))
            R13_V111["evidence"][_nw_key]["variants"][_nw_variant]=_nw_text
        for _nw_variant,_nw_text in _nw_spec.get("add_variants",{}).items():
            if _nw_variant in R13_V111["evidence"][_nw_key]["variants"]:raise Exception("Evidence variant already exists: %s %s"%(_nw_key,_nw_variant))
            R13_V111["evidence"][_nw_key]["variants"][_nw_variant]=_nw_text
        ROOM13["evidence"][_nw_rid]["establishes"]=next(iter(R13_V111["evidence"][_nw_key]["variants"].values()))
