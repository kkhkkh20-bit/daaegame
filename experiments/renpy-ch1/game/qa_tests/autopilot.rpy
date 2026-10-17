# QA only (not shipped): plays the game forward on its own from a new game and logs every line.
# Owner 2026-10-17 ("잔 오류가 많네"): single-scene tests jump straight to a day and place, so
# mistakes that only show in a continuous run (a scene over the wrong background, a speaker who is
# not the one on screen, a dead resident talking) slipped through. testcase walk_days drives this.
#   lines:  $ROOM13_QA_OUT/walk.jsonl   (one row per spoken line)
#   issues: $ROOM13_QA_OUT/walk_issues.txt (+ a screenshot per issue)
default r13_qa_auto = None

init 999 python:
    import json as _qa_json, os as _qa_os, time as _qa_time

    def r13_qa_out(name):
        out=_qa_os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa");_qa_os.makedirs(out,exist_ok=True)
        return _qa_os.path.join(out,name)

    def r13_qa_auto_start(last_day=3):
        store.r13_qa_auto=dict(active=True,last_day=last_day,visited=[],issues=0,lines=0,stall=0.0,
            last_progress=_qa_time.time(),done=False,shots=0,seen_issue=[])
        for n in ("walk.jsonl","walk_issues.txt"):
            p=r13_qa_out(n)
            if _qa_os.path.exists(p):_qa_os.remove(p)

    R13_QA_LOCATION_BG = None
    def r13_qa_location_bgs():
        return {v[1]:k for k,v in R13_PLACES.items()}

    def r13_qa_issue(kind,row):
        a=store.r13_qa_auto
        key=kind+"|"+row.get("what","")[:40]
        if key in a["seen_issue"]:return
        a["seen_issue"].append(key);a["issues"]+=1
        with open(r13_qa_out("walk_issues.txt"),"a") as f:
            f.write("%s\t%s\n"%(kind,_qa_json.dumps(row,ensure_ascii=False)))
        a["shot_next"]="issue_%02d_%s.png"%(a["issues"],kind)

    def r13_qa_line_cb(event,interact=True,**kwargs):
        a=store.r13_qa_auto
        if not a or not a.get("active") or not store.room13_mode or not store.room13:return
        if event=="show_done" and a.get("shot_next"):
            try:renpy.screenshot(r13_qa_out(a["shot_next"]))
            except Exception:pass
            a["shot_next"]=None
        if event!="begin":return
        s=store.room13
        who=kwargs.get("who_id")
        what=getattr(store,"_last_say_what","") or ""
        loc=s.get("location");bg=getattr(store,"r13_scene_bg",None)
        row=dict(day=s.get("day"),period=s.get("period"),loc=loc,bg=bg,place=getattr(store,"place",None),
            who=who,what=what[:80],visitor=getattr(store,"r13_motion_person",None),
            shown="r13_visitor" in renpy.get_showing_tags())
        a["lines"]+=1;a["last_progress"]=_qa_time.time()
        with open(r13_qa_out("walk.jsonl"),"a") as f:f.write(_qa_json.dumps(row,ensure_ascii=False)+"\n")
        # 1. A scene over another place's picture: the background is the plain picture of a
        #    different village place than where the family stands (Piko over the gate).
        bgs=r13_qa_location_bgs()
        here=R13_PLACES.get(loc,(None,None))[1]
        if bg in bgs and bg!=here and bgs[bg]!=loc and getattr(store,"place","")!="마차 안":
            r13_qa_issue("stale_background",row)
        # 2. A resident marked dead speaks.
        if who in R13_REL_DEAD and r13_has(R13_REL_DEAD[who]):
            r13_qa_issue("dead_speaker",row)
        # 3. An on-screen resident who is not the speaker while a resident speaks.
        if who and who in CAST and who not in ("dad",r13_viewpoint()) and row["shown"] and row["visitor"] and row["visitor"]!=who and getattr(store,"place","")!="마차 안":
            r13_qa_issue("speaker_not_shown",row)

    config.all_character_callbacks.append(r13_qa_line_cb)

    # Remember what is about to be said; who comes to the callback as who_id (cb_who_id on R13_CHARS).
    _r13_qa_prev_filter=config.say_menu_text_filter
    def r13_qa_say_filter(what):
        if _r13_qa_prev_filter:what=_r13_qa_prev_filter(what)
        store._last_say_what=what
        return what
    config.say_menu_text_filter=r13_qa_say_filter

    def r13_qa_auto_plan():
        """Next hub step: visit every open place once per time slot, then move the clock on."""
        a=store.r13_qa_auto;s=store.room13
        stamp=(s["day"],s["period"])
        if not r13_has("entry_corrected") or not r13_has("lodging"):
            return ("unlock",None)
        todo=[p for p in r13_places() if (stamp,p) not in [tuple(v) if isinstance(v,list) else v for v in a["visited"]]]
        if s["location"] in todo:
            a["visited"].append((stamp,s["location"]))
            todo=[p for p in todo if p!=s["location"]]
        if todo:return ("go",todo[0])
        if s["day"]>=a["last_day"] and s["period"]>=3:return ("done",None)
        return ("tick",None)

    def r13_qa_auto_hub():
        step,arg=r13_qa_auto_plan()
        a=store.r13_qa_auto
        if step=="done":
            a["done"]=True;a["active"]=False
            return
        if step=="unlock":
            # The day-1 gate paperwork is its own puzzle (covered by the gate tests); open the village.
            r13_flag("entry_corrected","lodging")
            renpy.jump("r13_roam")
        if step=="go":
            a["visited"].append(((store.room13["day"],store.room13["period"]),arg))
            r13_edit(location=arg)
            renpy.jump("r13_roam")
        if step=="tick":
            if store.room13["period"]<3:
                r13_edit(period=store.room13["period"]+1)
                renpy.jump("r13_roam")
            r13_next_day()
            renpy.jump("r13_day")

    def r13_qa_auto_pick():
        """First real option of whatever menu is up (Ren'Py choice or r13_confirm)."""
        scr=renpy.get_screen("choice")
        if scr:
            for item in scr.scope.get("items",[]):
                if item.action is not None:
                    return item.action()
        if renpy.get_screen("r13_confirm"):
            return True
        return None

    def r13_qa_auto_stalled():
        a=store.r13_qa_auto
        if not a or not a.get("active"):return False
        return _qa_time.time()-a["last_progress"]>6.0

    def r13_qa_auto_unstick():
        a=store.r13_qa_auto
        shown=[n for n in ("r13_records","r13_map","r13_book","r13_more_tools","r13_offer_card","r13_evening_board","r13_life_closeup","r13_cinematic_view","r13_arrival_card") if renpy.get_screen(n)]
        with open(r13_qa_out("walk_issues.txt"),"a") as f:
            f.write("stuck\t%s\n"%_qa_json.dumps(dict(day=store.room13.get("day"),period=store.room13.get("period"),loc=store.room13.get("location"),screens=shown),ensure_ascii=False))
        a["last_progress"]=_qa_time.time()
        for n in shown:renpy.hide_screen(n)
        renpy.queue_event("dismiss")

    config.overlay_screens.append("r13_qa_autopilot")

screen r13_qa_autopilot():
    zorder 300
    if r13_qa_auto and r13_qa_auto.get("active"):
        if renpy.get_screen("choice") or renpy.get_screen("r13_confirm"):
            timer .15 action Function(r13_qa_auto_pick_and_return)
        elif renpy.get_screen("say"):
            timer .06 repeat True action Function(renpy.queue_event,"dismiss")
        elif renpy.get_screen("r13_hub") and not any(renpy.get_screen(n) for n in ("r13_records","r13_map","r13_more_tools","r13_confirm","r13_book")):
            timer .1 action Function(r13_qa_auto_hub_mark)
        elif renpy.get_screen("r13_cinematic_view") or renpy.get_screen("r13_arrival_card"):
            timer .2 repeat True action Function(renpy.queue_event,"dismiss")
        timer 1.0 repeat True action If(r13_qa_auto_stalled(),Function(r13_qa_auto_unstick),NullAction())

init 999 python:
    def r13_qa_auto_hub_mark():
        store.r13_qa_auto["last_progress"]=_qa_time.time()
        r13_qa_auto_hub()

    def r13_qa_auto_pick_and_return():
        store.r13_qa_auto["last_progress"]=_qa_time.time()
        if renpy.get_screen("r13_confirm"):
            renpy.end_interaction(True)
        scr=renpy.get_screen("choice")
        if scr:
            for item in scr.scope.get("items",[]):
                if item.action is not None:
                    renpy.run(item.action)
                    return
