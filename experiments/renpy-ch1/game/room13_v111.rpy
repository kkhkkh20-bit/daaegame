# V1.1.1 story data in the existing Room13 state and native Ren'Py labels.
# No alternate controller, natural-language evaluator, or separate save state.
init 301 python:
    R13_V111=json.load(renpy.file("v111/records.json"))
    R13_V111_BINDINGS=json.load(renpy.file("v111/field-bindings.json"))
    def r13_v111_active():
        return bool(getattr(store,"room13",None) and store.room13.get("v111"))
    def r13_v111_value(key):
        return store.room13.get("v111",{}).get("values",{}).get(key,R13_V111["initial"].get(key))
    def r13_v111_set(key,value):
        n=winter_copy.deepcopy(store.room13)
        n["v111"]["values"][key]=value
        if key=="day":n["day"]=value;n["period"]=0;n["v111"]["values"]["elapsed_minutes"]=0
        if key=="piko_alive" and not value and "piko_dead" not in n["flags"]:n["flags"].append("piko_dead")
        store.room13=n
    def r13_v111_owned(key):
        return "V111:"+key in store.room13["evidence"]
    def r13_v111_apply(event,operations):
        if r13_has("v111:applied:"+event):return
        for op in operations:
            if op["op"]=="set":r13_v111_set(op["field"],op["value"])
            elif op["op"]=="acquire":
                key="V111:"+op["key"]
                r13_grant([key],event)
                r13_v111_set(op["key"]+".variant",op["variant"])
            else:raise Exception("Unreviewed V1.1.1 operation: "+str(op))
        r13_flag("v111:applied:"+event)
    def r13_v111_commit(rid):
        r13_v111_apply(rid,R13_V111["records"][rid]["operations"])
    def r13_v111_line(rid):
        r=R13_V111["records"][rid]
        if r.get("requires"):raise Exception("Unbound record condition: "+rid)
        who=MS14_SPEAKERS.get(r.get("speaker"))
        if who=="resident_piko" and r13_v111_value("piko_alive") is False:raise Exception("Absent/dead Piko line: "+rid)
        slot=r.get("direction",{}).get("slot") or "neutral"
        return (who,r["text"],dict(no_lead=True,expression=slot,pose=slot,**({"carriage_jolt":True} if rid=="MS14_D01_S01_L0002" else {})))
    def r13_v111_binding():
        v=store.room13.get("v111",{})
        if v.get("gate")=="travel":
            target=v["travel_to"]
            return dict(people=v.get("people",["daram"]),options=[dict(title=R13_PLACES[target][0],location=target,move=target)])
        b=dict(R13_V111_BINDINGS.get(v.get("gate"),{}))
        b["options"]=[dict(o,index=i) for i,o in enumerate(b.get("options",[])) if all((r13_v111_owned(k)==expected if kind=="evidence" else r13_v111_value(k)==expected) for kind,k,expected in o.get("guard",[]))]
        b.setdefault("people",v.get("people",["daram"]))
        return b
    def r13_v111_context(key):
        n=winter_copy.deepcopy(store.room13);n["v111"]["gate"]=key;store.room13=n
    def r13_v111_questions(person):
        b=r13_v111_binding()
        return [(o["title"],Return(o.get("index",i)),False) for i,o in enumerate(b.get("options",[])) if o.get("person")==person]
    for title in R13_V111["proof_claims"]:R13_CLAIMS["v111:"+title]=dict(assertion=title)
    for key,spec in R13_V111["evidence"].items():
        rid="V111:"+key
        ROOM13["evidence"][rid]=dict(id=rid,name=spec["name"],kind=spec["kind"],establishes=next(iter(spec["variants"].values())),does_not_establish="",current_run_only=True,retained_on_show=True,scenes=[])
        R13_RECORD_SHORT[rid]=spec["name"]
    _r13_v111_visible_people=r13_visible_people
    def r13_visible_people():
        if not r13_v111_active():return _r13_v111_visible_people()
        return [p for p in r13_v111_binding().get("people",["daram"]) if p!="resident_piko" or r13_v111_value("piko_alive")]
    _r13_v111_stage_people=r13_stage_people
    def r13_stage_people(entry=False):
        rows=_r13_v111_stage_people(entry)
        return [a for a in rows if a["person"] in r13_visible_people()] if r13_v111_active() else rows
    _r13_v111_person_action=r13_person_action
    def r13_person_action(person,entry=False):
        return Return(("person",person)) if r13_v111_active() else _r13_v111_person_action(person,entry)
    _r13_v111_object_visible=r13_object_visible
    def r13_object_visible(spec):
        if not r13_v111_active():return _r13_v111_object_visible(spec)
        objects=ROOM13["objects"].get(store.room13["location"],{})
        return any(spec is objects.get(o.get("object")) for o in r13_v111_binding().get("options",[]) if o.get("location")==store.room13["location"])
    ROOM13["objects"].setdefault("forest",{})["v111_box"]=dict(rect=[1150,548,220,152],need=[],give=[],flags=[],text="북쪽 물자 길 교환함")
    R13_OBJECT_NAMES["v111_box"]="교환함"
    _r13_v111_props=r13_world_props
    def r13_world_props(entry=False):
        if r13_v111_active() and store.room13["location"]=="forest":
            return [(Transform("assets/ms14/box.png",xysize=(220,152),fit="contain",nearest=True),1150,548)]
        return _r13_v111_props(entry)
    _r13_v111_places=r13_places
    def r13_places():
        if not r13_v111_active():return _r13_v111_places()
        return list(dict.fromkeys([store.room13["location"]]+[o["location"] for o in r13_v111_binding().get("options",[]) if o.get("location")]))
    _r13_v111_bed=r13_bed_available
    def r13_bed_available(key):
        return False if r13_v111_active() else _r13_v111_bed(key)

label r13_v111_wait(key):
    $ r13_v111_context(key)
label r13_v111_wait_again:
    window hide
    hide r13_visitor
    call screen r13_hub
    $ v111_pick=_return; v111_binding=r13_v111_binding()
    if v111_pick[0]=="menu" and v111_pick[1]=="map":
        call screen r13_map
        if _return and _return in r13_places():
            $ r13_edit(location=_return)
            call r13_scene(R13_PLACES[room13["location"]][1],R13_PLACES[room13["location"]][0],"calm")
            $ v111_move=next((i for i,o in enumerate(v111_binding.get("options",[])) if o.get("move")==room13["location"]),None)
            if v111_move is not None:
                $ r13_v111_time("move:"+key+":"+room13["location"],5)
                return v111_binding["options"][v111_move].get("index",v111_move)
        jump r13_v111_wait_again
    if v111_pick[0]=="person":
        $ v111_person=v111_pick[1]
        if r13_v111_questions(v111_person):
            call screen r13_topics(v111_person)
            if isinstance(_return,int):
                $ r13_v111_time("topic:"+key+":"+str(_return),0 if (key=="gate_investigate" and _return in (5,6)) or (key=="post_menu" and _return==1) else 10)
                return _return
            if _return=="present":
                call screen r13_book(v111_person,present=True)
                $ v111_shown=_return
                $ v111_match=next((i for i,o in enumerate(v111_binding.get("options",[])) if o.get("present")==v111_shown),None)
                if v111_match is not None:
                    return v111_binding["options"][v111_match].get("index",v111_match)
        jump r13_v111_wait_again
    if v111_pick[0]=="object":
        $ v111_matches=[i for i,o in enumerate(v111_binding.get("options",[])) if o.get("object")==v111_pick[1] and o.get("location")==room13["location"]]
        if len(v111_matches)==1:
            $ r13_v111_time("inspect:"+key+":"+v111_pick[1],0 if key=="gate_investigate" and v111_pick[1]=="ledger" else 15)
            return v111_binding["options"][v111_matches[0]].get("index",v111_matches[0])
        if len(v111_matches)>1:
            $ v111_object_options=[(v111_binding["options"][i]["title"],i) for i in v111_matches]
            $ v111_result=renpy.display_menu(v111_object_options)
            return v111_binding["options"][v111_result].get("index",v111_result)
    jump r13_v111_wait_again

label r13_v111_proof(key,correct,success,wrong=None,hint=None):
    $ v111_claim="v111:"+key
    $ R13_CLAIMS[v111_claim]=dict(assertion=key)
    $ room13["arguments"].setdefault(v111_claim,[])
label r13_v111_proof_again:
    call screen r13_crisis_proof(v111_claim,heading="기록 · 자료 대조")
    if _return=="present":
        call screen r13_book("dad",present=True)
        if _return and _return in room13["evidence"] and _return not in room13["arguments"][v111_claim]:
            $ v111_copy=winter_copy.deepcopy(room13); v111_copy["arguments"][v111_claim].append(_return); room13=v111_copy
        jump r13_v111_proof_again
    if _return=="argue":
        if set("V111:"+x for x in correct)==set(room13["arguments"][v111_claim]):
            return success
        $ v111_wrong_target="r13_v111_gate_number" if v111_claim=="v111:함께 들어갈 근거를 고른다" and room13["arguments"][v111_claim]==["V111:E03"] else wrong
        $ v111_copy=winter_copy.deepcopy(room13); v111_copy["arguments"][v111_claim]=[]; room13=v111_copy
        if v111_wrong_target:
            return v111_wrong_target
    if _return=="press" and hint:
        return hint
    if _return=="leave":
        call screen r13_book
    jump r13_v111_proof_again

label r13_v111_travel(destination,travel_id):
    if room13["location"]==destination:
        return
    $ room13["v111"]["travel_to"]=destination
    call r13_v111_wait("travel")
    return

init 302 python:
    _r13_v111_material_art=r13_material_art
    def r13_material_art(key):
        if r13_v111_active() and key in ("V111:E09","V111:E30"):
            art=("portrait_"+r13_v111_value("portrait")) if key=="V111:E09" else "bundle"
            if art=="portrait_child_completed":art="portrait_child"
            if art in MS14_ART:return Transform(MS14_ART[art]["file"],xysize=(160,100),fit="contain",nearest=True)
        return _r13_v111_material_art(key)

init 303 python:
    def r13_v111_option(option_id):
        # Input effects are consumed by their explicit callback label, not stored
        # as a lasting 'input' flag that could activate unrelated blocks later.
        r13_v111_apply(option_id,R13_V111["options"][option_id]["operations"])
    R13_V111_ENTRY={
        "MS14_D01_S02":(["E01"],{"carriage_stopped":True}),
        "MS14_D01_S03":(["E02"],{"gate_registered":False}),
        "MS14_D01_S04":([],{"gate_basis_proven":True,"gate_registered":False}),
        "MS14_D01_S05":([],{"gate_registered":True}),
        "MS14_D02_S01":([],{"day":2}),
        "MS14_D02_S02":([],{"mother_box_checked_day2":True,"arrival_note_sent":True}),
        "MS14_D02_S03":(["E07"],{}),
        "MS14_D02_S04":(["E08"],{"portrait_commissioned":True,"nero_contact_lead":True}),
        "MS14_D02_S05":([],{"selected_afternoon_work_completed":True}),
        "MS14_D03_S01":([],{"day":3}),
        "MS14_D03_S02":(["E09"],{}),
        "MS14_D03_S03":(["E10","E11","E32"],{}),
        "MS14_D03_S04":([],{"measurement_separated_from_theft":True}),
        "MS14_D03_S05":(["E11","E12","E13","E14","E15","E16","E32"],{"silluk_knife_comparison_consent":True,"silluk.children.location":"workshop_with_buri"}),
        "MS14_D03_S06":([],{"lamp_theft_supported":True,"stone_choice_completed":True}),
    }
    def r13_v111_scene(scene):
        marker="v111:entered:"+scene
        if r13_has(marker):
            store.room13["v111"]["scene"]=scene
            return
        if store.room13["day"]!=R13_V111["scene_days"][scene]:raise Exception("Wrong authored day: "+scene)
        if scene=="MS14_D02_S04" and r13_v111_value("D02_afternoon") not in (None,"uncommitted"):raise Exception("Afternoon already committed")
        if scene=="MS14_D02_S05" and r13_v111_value("D02_afternoon") not in ("shelter","nero"):raise Exception("Missing afternoon decision")
        if scene=="MS14_D03_S06" and r13_v111_value("silluk_status") not in ("reporting_obligation","detained_work_waiting_station"):raise Exception("Missing custody decision")
        items,values=R13_V111_ENTRY.get(scene,([],{}))
        if not all(r13_v111_owned(x) for x in items) or not all(r13_v111_value(k)==v for k,v in values.items()):raise Exception("Unmet authored scene entry: "+scene)
        if scene=="MS14_D02_S01" and not r13_has("v111:applied:option:sleep1:0"):raise Exception("Missing actual first-night sleep")
        if scene=="MS14_D03_S01" and not r13_has("v111:applied:option:sleep2:0"):raise Exception("Missing actual second-night sleep")
        store.room13["v111"]["scene"]=scene
        r13_flag(marker)

init 304 python:
    def r13_v111_score():
        scene=store.room13.get("v111",{}).get("scene")
        track=R13_V111.get("audio",{}).get(scene)
        if track and renpy.music.get_playing()!=track:
            renpy.music.play(track,fadeout=.2,fadein=.2)

init 305 python:
    def r13_v111_time(event,minutes):
        marker="v111:time:%d:%s"%(store.room13["day"],event)
        if r13_has(marker):return
        r13_v111_set("elapsed_minutes",(r13_v111_value("elapsed_minutes") or 0)+minutes)
        r13_flag(marker)

init 306 python:
    _r13_v111_catalog_record=r13_catalog_record
    def r13_catalog_record(key):
        record=_r13_v111_catalog_record(key)
        if not r13_v111_active() or not record:return record
        if key=="V111:E09":
            record=dict(record)
            variant=r13_v111_value("E09.variant")
            portrait=r13_v111_value("portrait")
            if portrait=="child_completed":
                record["name"]="다람이 이어 그린 엄마의 초상"
                record["establishes"]="다람이 빈 코를 이어 그렸다. 피코가 완성한 초상이나 목격 증언은 아니다."
            elif variant=="unfinished":
                record["name"]="엄마의 초상 · 미완성"
                record["establishes"]="눈과 입이 그려져 있고, 코가 있어야 할 자리는 비어 있다."
            else:
                record["name"]="엄마의 초상 · 완성"
                record["establishes"]="피코가 완성해 건네준 엄마의 초상. 등 절도 순간은 피코가 식당 안에 있었으므로 보지 못했다."
        elif key=="V111:E35":
            record=dict(record)
            received=r13_v111_value("E35.status")=="received"
            record["name"]="가족 침구 · "+("수령 완료" if received else "예약")
            record["establishes"]="마른 담요 두 장을 실제로 받았다." if received else "마른 담요 두 장을 예약했다. 아직 받지 않았다."
        return record

init 307 python:
    _r13_v111_scene_music=r13_sound_scene_music
    def r13_sound_scene_music(bg,title,mood="calm"):
        if r13_v111_active():
            track=R13_V111.get("audio",{}).get(store.room13["v111"].get("scene"))
            if track:return track
        return _r13_v111_scene_music(bg,title,mood)
