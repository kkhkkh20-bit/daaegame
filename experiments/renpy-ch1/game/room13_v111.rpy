default r13_field_reading = False
default r13_v111_talk_person = None
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
        if key=="DARAM_DETAINED":n["daram_state"]="held" if value else "with_dad"
        if key=="OWL_ALIVE":
            n["victim_state"]="alive" if value else "dead"
            if not value:n["case_state"]="occurred"
            elif n["v111"]["values"].get("route7")=="prevented":n["case_state"]="prevented"
        if key=="grandmother_custody":n["granny_state"]="detained" if value=="detained" else "trusted"
        if key=="family_reunited" and value:n["mom_state"]="reunited"
        store.room13=n
        # 0.20.5 (Codex T02): an ending is recorded when its story is finished, not when it is chosen.
        if key=="story14_completed" and value and "r13_fork_ending" in globals():r13_fork_ending(n["v111"]["values"].get("ending14"))
        death={"piko_alive":"piko_dead","KKOMI_ALIVE":"kkomi_dead","alive:kid_dodam":"dodam_dead","nero_alive":"nero_dead","TOK_ALIVE":"tok_dead","OWL_ALIVE":"v111:owl_dead"}
        if key in death and value is False:r13_flag(death[key])
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
    # Owner-requested opening dialogue revision, 2026-10-20.
    # Keep uploaded source records intact; only these reviewed spoken/action lines differ.
    R13_V111_CARRIAGE_TEXT = {
        "MS14_D13_S04_L0037": "오늘 밤은 넘겨도, 내일은 어쩌겠소?",
        "MS14_D06_S04_L0046": "다람이 도토리는 내가 꺼내 왔어.",
        "MS14_D01_S01_L0001": "마차가 덜컹 기울었다. 다람이 과자 봉지를 두 손으로 감쌌다.",
        "MS14_D01_S01_L0002": "과자는 꼭 잡고, 아빠는?",
        "MS14_D01_S01_L0004": "넘어지면 아프거든.",
        "MS14_D01_S01_L0005": "다람이 한 손으로 내 소매를 잡았다. 다른 손에는 과자 봉지를 꼭 안은 채였다.",
        "MS14_D01_S01_L0006": "과자는 몇 개 남았어?",
        "MS14_D01_S01_L0008": "제일 큰 걸 남겼네.",
    }
    def r13_v111_person_alive(person):
        life={"resident_nero":"nero_alive","resident_owlgp":"OWL_ALIVE","kid_kkomi":"KKOMI_ALIVE","resident_tok":"TOK_ALIVE","resident_piko":"piko_alive","resident_musoe":"musoe_alive","kid_dodam":"alive:kid_dodam"}
        return r13_v111_value(life.get(person,"alive:"+person)) is not False
    def r13_v111_line(rid):
        r=R13_V111["records"][rid]
        if r.get("requires") and not r13_v111_record_allowed(rid):raise Exception("Unmet authored record condition: "+rid)
        who=MS14_SPEAKERS.get(r.get("speaker"))
        if r.get("speaker") and who is None:raise Exception("Unmapped authored speaker: "+r["speaker"])
        if who=="resident_piko" and r13_v111_value("piko_alive") is False:raise Exception("Absent/dead Piko line: "+rid)
        if who and not r13_v111_person_alive(who):raise Exception("Absent/dead authored speaker: "+rid)
        slot=r.get("direction",{}).get("slot") or "neutral"
        art_options={}
        if rid in ("MS14_D13_S01_L0005","MS14_D13_S01_L0007","MS14_D13_S01_L0008","MS14_D13_S01_L0009"):
            art_options["cut"]="v111_blanket_before"
        elif rid in ("MS14_D13_S01_L0011","MS14_D13_S01_L0012","MS14_D13_S01_L0013","MS14_D13_S01_L0014","MS14_D13_S01_L0016","MS14_D13_S01_L0017","MS14_D13_S01_L0018"):
            art_options["cut"]="v111_blanket_after"
        return (who,R13_V111_CARRIAGE_TEXT.get(rid,r["text"]),dict(no_lead=True,expression=slot,pose=slot,**dict(art_options,**({"carriage_jolt":True,"show":"daram"} if rid=="MS14_D01_S01_L0001" else {}))))
    def r13_v111_binding():
        v=store.room13.get("v111",{})
        if v.get("gate")=="travel":
            target=v["travel_to"]
            return dict(people=v.get("people",["daram"]),options=[dict(title=R13_PLACES[target][0],location=target,move=target)])
        b=dict(R13_V111_BINDINGS.get(v.get("gate"),{}))
        b["options"]=[dict(o,index=o.get("index",i)) for i,o in enumerate(b.get("options",[])) if all((r13_v111_owned(k)==expected if kind=="evidence" else r13_v111_value(k)==expected) for kind,k,expected in o.get("guard",[]))]
        if v.get("gate")=="free_day7" and not r13_owl_tok_available7():
            b["options"]=[o for o in b["options"] if o.get("index") not in (111,112)]
        if v.get("gate")=="transport_cleanup13":
            guard_place=r13_v111_value("location:guard") if r13_v111_value("busy:guard")=="silluk_supervision" else "square"
            for option in b["options"]:
                if option.get("person")=="guard":option["location"]=guard_place
            square_people=["karo","resident_badook"]+([] if guard_place!="square" else ["guard"])
            # 0.20.12 (후반 기획서 C안): 다섯 확인을 바둑이·돌목·까로 세 대화로 묶는다. 마친 확인은 목록에서 빼고,
            # 이어지는 두 번째 확인(수레 반환, 사본 전달)은 앞 대화 뒤에 남은 경우에만 따로 보인다.
            _done={0:r13_v111_value("actual_stop_actor_refuses_transport"),
                   1:r13_v111_value("current_order_execution_stopped"),
                   2:r13_v111_value("Kkaro_forced_transport_refused"),
                   3:r13_v111_value("cart_returned") or not r13_v111_value("Kkaro_forced_transport_refused"),
                   4:r13_v111_value("relay_stopped") or not r13_v111_value("current_order_execution_stopped")}
            b["options"]=[o for o in b["options"] if not _done.get(o["index"])]
            b["people_by_location"]={"square":square_people,"school":["nabi","mom","daram"],"v111_labor":["guard","resident_siluk"],"v111_supervised":["neoul","resident_teacher"],"workshop":["buri"]}
        if v.get("gate")=="device_detach14" and r13_v111_value("buri_device_present"):b["people"]=["mom","daram","buri","resident_ppul","resident_badook","karo"]
        if v.get("gate")=="guard_relief_check14":b["people"]=["guard","resident_siluk",r13_v111_value("guard_relief_person") or "v111_patrol"]
        b.setdefault("people",v.get("people",["daram"]))
        if v.get("scene") in ("MS14_D14_S02","MS14_D14_S04") and r13_v111_value("madam_observer_consent") and r13_v111_value("location:resident_madam")==store.room13["location"] and r13_v111_person_alive("resident_madam"):
            b["people"]=list(dict.fromkeys(b["people"]+["resident_madam"]))
        if v.get("gate")=="partial_receipt14" and getattr(store,"v111_pending_patient",None):b["people"]=list(dict.fromkeys(b["people"]+[store.v111_pending_patient]))
        if v.get("gate")=="crowd_prepare13" and not r13_crowd_guard_available13(True):
            b["people"]=[p for p in b.get("people",[]) if p!="guard"]
            b["options"]=[o for o in b["options"] if o.get("person")!="guard"]
        if b.get("daram_if_free") and r13_v111_value("DARAM_DETAINED"):b["people"]=[p for p in b["people"] if p!="daram"]
        if b.get("people_by_location") is not None:b["people"]=b["people_by_location"].get(store.room13["location"],[])
        return b
    def r13_v111_present_index(binding,person,shown):
        if not shown or shown not in store.room13["evidence"]:return None
        for i,option in enumerate(binding.get("options",[])):
            if option.get("present")==shown and option.get("person")==person and option.get("location")==store.room13["location"]:
                return option.get("index",i)
        return None
    def r13_v111_context(key):
        n=winter_copy.deepcopy(store.room13);n["v111"]["gate"]=key
        # 2026-10-24 행동 검수 4(소유자 승인 「구조 수정」): 이동 말고 다른 대기에 닿으면 지금 장면의
        # 「생각」을 보인 것이므로, 이동 중에 붙들어 두던 직전 장면 문구를 놓는다.
        if key!="travel":n["v111"]["thought_pending"]=False
        store.room13=n
    def r13_v111_questions(person):
        b=r13_v111_binding()
        # 0.20.10 (4~14일 리뷰): 제목이 보일 자료를 이미 말하므로, 가진 자료면 목록에서 다시 찾지 않는다.
        return [(o["title"],Return("present") if o.get("present") and o["present"] not in store.room13["evidence"] else Return(o.get("index",i)),bool(o.get("remember_read") and r13_v111_value("ui_topic_read:%s:%s"%(store.room13["v111"].get("gate"),o.get("index",i))))) for i,o in enumerate(b.get("options",[])) if o.get("person")==person and o.get("location")==store.room13["location"]]
    for title in R13_V111["proof_claims"]:R13_CLAIMS["v111:"+title]=dict(assertion=title)
    for key,spec in R13_V111["evidence"].items():
        rid="V111:"+key
        ROOM13["evidence"][rid]=dict(id=rid,name=spec["name"],kind=spec["kind"],establishes=next(iter(spec["variants"].values())),does_not_establish="",current_run_only=True,retained_on_show=True,scenes=[])
        R13_RECORD_SHORT[rid]=spec["name"]
    _r13_v111_visible_people=r13_visible_people
    def r13_visible_people():
        if not r13_v111_active():return _r13_v111_visible_people()
        authored=r13_v111_binding().get("people",["daram"])
        # Preserve the existing residents and their scheduled staging. Explicit
        # V1.1.1 survival, relocation and custody results still take precedence.
        people=[] if r13_v111_value("wild_night14") or store.room13["location"] in ("hidden_pandol","hidden_base14") else list(_r13_v111_visible_people())
        if store.room13["v111"].get("gate")=="crowd_prepare13" and not r13_crowd_guard_available13(True):people=[p for p in people if p!="guard"]
        people=[p for p in people if not r13_v111_value("busy:"+p) or r13_v111_value("location:"+p) in (None,store.room13["location"])]
        if r13_v111_value("piko.location") and r13_v111_value("piko.location")!=store.room13["location"]:
            people=[p for p in people if p!="resident_piko"]
        if r13_v111_value("silluk_status") in ("detained_work_waiting_station","supervised_compulsory_labor"):
            people=[p for p in people if p!="resident_siluk"]
        if r13_v111_value("grandmother_custody")=="detained":people=[p for p in people if p!="granny"]
        if r13_v111_value("teacher_custody") in ("guard","neoul"):people=[p for p in people if p!="resident_teacher"]
        people=list(dict.fromkeys(people+list(authored)))
        # 2026-10-27 소유자: "처음에 다람이가 나올 필요가 없어, 초소에서도 아빠랑 같이 있는데". 1일 입구에서는 아빠 곁에
        # 붙어 있으므로 현장에 따로 세우지 않는다. 대사 근접·주고받기(r13_child_is_along)는 상태로 판단해 그대로 나온다.
        if store.room13.get("day")==1 and store.room13.get("location")=="gate":people=[p for p in people if p!="daram"]
        if r13_v111_value("DARAM_DETAINED") and "daram" not in authored:people=[p for p in people if p!="daram"]
        for family_person in ("daram","mom"):
            physical=r13_v111_value("location:"+family_person)
            if physical and physical!=store.room13["location"] and family_person not in authored:people=[p for p in people if p!=family_person]
        # Unnamed off-screen speakers have no authored body in CAST. Keep their
        # location/role state, but do not feed a missing sprite to the stage.
        return [p for p in people if p in CAST and (p!="resident_piko" or r13_v111_value("piko_alive")) and (p!="resident_musoe" or r13_v111_value("musoe_alive")) and r13_v111_person_alive(p)]
    _r13_v111_stage_people=r13_stage_people
    def r13_stage_people(entry=False):
        rows=_r13_v111_stage_people(entry)
        return [a for a in rows if a["person"] in r13_visible_people()] if r13_v111_active() else rows
    _r13_v111_person_action=r13_person_action
    def r13_person_action(person,entry=False):
        return Return(("person",person)) if r13_v111_active() else _r13_v111_person_action(person,entry)
    R13_V111_RECORD_OBJECTS={
        ("gate","ledger"):"E02",("gate","booth"):"E03",("gate","gate_documents"):"E03",("gate","rules"):"E04",
        ("room13","mother_note"):"E06",("room13","family_bundle"):"E30",
        ("clinic","notes"):"E13",("store","ledger"):"E16",
    }
    R13_V111_RECORD_LATER={
        ("room13","mother_note"):"책상 위에 접힌 종이가 있다. 우선 다람이 짐부터 침대에 내려놓고 방을 둘러보자.",
        ("room13","family_bundle"):"책상 아래에 보따리가 보인다. 책상 위 종이부터 보고 열어 보자.",
        # 2026-10-27 플레이 리뷰 P4: 「지금은 먼저 할 일이 있다」는 무엇을 하라는 건지 없다. 조작 순서만 알려 준다(정답은 아님).
        ("gate","booth"):"초소 선반의 서류. 돌목 씨에게 신청서를 찾아 달라고 먼저 부탁하자.",
        ("gate","gate_documents"):"초소 서류. 돌목 씨에게 신청서를 찾아 달라고 먼저 부탁하자.",
        ("gate","rules"):"겨울철 입장 규칙. 돌목 씨가 명단을 어떻게 적었는지부터 확인하자.",
    }
    def r13_v111_object_key(key):
        if store.room13["location"]=="kitchen" and key in ("rear_after","rear_after_known"):return "rear"
        return key
    def r13_v111_ambient_text(key,spec):
        if r13_v111_value("wild_night14"):return "연기가 밀려온다. 오래 들여다볼 틈이 없다."
        location=store.room13["location"]
        key=r13_v111_object_key(key)
        spec=ROOM13["objects"].get(location,{}).get(key,spec)
        record=R13_V111_RECORD_OBJECTS.get((location,key))
        if record:
            if r13_v111_owned(record):return ROOM13["evidence"]["V111:"+record]["establishes"]
            # 0.20.6 (play review P01): a record not yet taken says why, not only its name.
            return R13_V111_RECORD_LATER.get((location,key)) or (ROOM13["evidence"]["V111:"+record]["name"]+". 지금은 먼저 할 일이 있다.")
        # Keep the existing scenery observations, but never run an old case's
        # grants, latch events, deductions or secret-room handlers in this story.
        if (location,key)==("square","lamp"):return "등 받침에 작은 점검함이 있다."
        if spec.get("give") or spec.get("flags") or spec.get("special"):
            return r13_object_name(key) if _r13_v111_object_visible(spec) else None
        return spec.get("text") if _r13_v111_object_visible(spec) else None
    _r13_v111_object_visible=r13_object_visible
    def r13_object_visible(spec):
        if not r13_v111_active():return _r13_v111_object_visible(spec)
        objects=ROOM13["objects"].get(store.room13["location"],{})
        if any(spec is value and r13_v111_object_key(key)!=key for key,value in objects.items()):return False
        return (any(spec is objects.get(o.get("object")) for o in r13_v111_binding().get("options",[]) if o.get("location")==store.room13["location"])
            or any(spec is value and r13_v111_ambient_text(key,value) for key,value in objects.items()))
    ROOM13["objects"].setdefault("forest",{})["v111_box"]=dict(rect=[880,500,220,152],need=[],give=[],flags=[],text="북쪽 물자 길 교환함")
    R13_OBJECT_NAMES["v111_box"]="교환함"
    # 0.20.10 (4~14일 리뷰 D11-02·03): 서술이 가리키는 대상을 그 단계에서만 보이는 조사 지점으로 둔다.
    ROOM13["objects"].setdefault("facility",{})["v111_mural"]=dict(rect=[1690,90,220,400],need=[],give=[],flags=[],text="벽 그림과 떨어진 돌판")
    R13_OBJECT_NAMES["v111_mural"]="벽 그림과 돌판"
    ROOM13["objects"].setdefault("forest",{})["v111_lower_door"]=dict(rect=[1310,360,290,230],need=[],give=[],flags=[],text="눈에 묻힌 아랫길 집 문")
    R13_OBJECT_NAMES["v111_lower_door"]="눈에 묻힌 문"
    _r13_v111_props=r13_world_props
    def r13_world_props(entry=False):
        if r13_v111_active() and store.room13["location"]=="forest" and store.room13["v111"].get("scene") in ("MS14_D02_S01","MS14_D11_S00"):
            # One rect drives both the prop and its click target on days 2 and 11.
            x,y,w,h=ROOM13["objects"]["forest"]["v111_box"]["rect"]
            return [(Transform("assets/ms14/box.png",xysize=(w,h),fit="contain",nearest=True),x,y)]
        if r13_v111_active() and store.room13["location"]=="school" and store.room13["v111"].get("gate")=="blanket_mend13":
            return [(Transform("assets/room13-v111-blanket-before.webp",xysize=(260,180),fit="contain",nearest=True),30,441)]
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
    # 0.20.6 (owner day-1 play: "추가 질문마다 대화를 다시 시작하는 느낌"): after a question, a shown
    # record or a follow-up, the same person's questions open again while they still have
    # something to say and stand here; 「돌아가기」 leaves the conversation.
    if r13_v111_talk_person and r13_v111_talk_person in r13_visible_people() and not r13_v111_idle_ok(r13_v111_talk_person):
        $ v111_pick=("person",r13_v111_talk_person); v111_binding=r13_v111_binding()
    else:
        call screen r13_hub
        $ v111_pick=_return; v111_binding=r13_v111_binding()
    $ r13_v111_talk_person=None
    # 0.19.95: same guard as the older hub (room13.rpy) — a screen that returns
    # something other than a (kind, value) pair shows the hub again instead of crashing.
    if not r13_screen_choice_ok(v111_pick,"r13_v111_hub"):
        jump r13_v111_wait_again
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
        if room13["location"] in ("hidden_pandol","hidden_base14") and not any(o.get("person")==v111_person for o in v111_binding.get("options",[])):
            call r13_hidden_idle
            jump r13_v111_wait_again
        if r13_v111_value("wild_night14") and not any(o.get("person")==v111_person for o in v111_binding.get("options",[])):
            call r13_v111_wild_family_wait14
            jump r13_v111_wait_again
        if key=="gate_request" and v111_person=="guard":
            # 2026-10-27 소유자 플레이: 경비를 눌렀는데 그림도 말도 없이 명단 지문이 흐르고 자료가 생겼다.
            # 명단은 경비에게 보여 달라고 해서 받는 것이므로, 그 주고받기를 먼저 보이고 읽는다.
            call r13_v111_gate_ledger_hand
            $ r13_v111_time("inspect:gate_request:ledger",15)
            return 0
        if v111_person in r13_visible_people() and r13_v111_idle_ok(v111_person):
            # 2026-10-27 소유자: 회의(오답 뒤) 상태의 현장에서 다른 주민의 한가한 한 줄에도 돌목 무대가 떴다. 현장 관찰로 읽는다.
            $ r13_field_reading=True
            call r13_lines(r13_v111_idle_lines(v111_person),"v111:idle:"+v111_person)
            $ r13_field_reading=False
        elif v111_person in r13_visible_people():
            # 0.20.10 (4~14일 리뷰 P07): 물을 것이 없는 다람은 장면마다 처음 한 번 먼저 대답한다.
            if v111_person=="daram" and r13_v111_daram_hello_due():
                call r13_lines(r13_v111_daram_hello(),"v111:daram_hello")
            call screen r13_topics(v111_person)
            if _return!="back":
                $ r13_v111_talk_person=v111_person
                $ r13_v111_set("talked:%s:%s"%(room13["v111"].get("scene"),v111_person),True)
            if room13["location"] in ("hidden_pandol","hidden_base14") and (_return=="present" or isinstance(_return,tuple)):
                $ r13_v111_talk_person=None
                call r13_hidden_idle
                jump r13_v111_wait_again
            if r13_v111_value("wild_night14") and (_return=="present" or isinstance(_return,tuple)):
                $ r13_v111_talk_person=None
                $ renpy.notify("지금은 불길을 피해야 한다.")
                jump r13_v111_wait_again
            if isinstance(_return,int):
                $ r13_v111_set("ui_topic_read:%s:%s"%(key,_return),True)
                $ r13_v111_time("topic:"+key+":"+str(_return),0 if (key=="gate_investigate" and _return in (5,6)) or (key=="post_menu" and _return==1) or key in ("safe_passage9","passage_after9") else 10)
                return _return
            if _return=="present":
                call screen r13_book(v111_person,present=True)
                $ v111_shown=_return if isinstance(_return,str) else None  # 0.20.4: cancel (False/None/True) is not a record
                $ v111_match=r13_v111_present_index(v111_binding,v111_person,v111_shown)
                if v111_match is not None:
                    return v111_match
                if v111_shown:
                    # 0.20.x (owner plan item 3): the resident answers in their own voice.
                    $ v111_react=r13_v111_present_reaction(v111_person,v111_shown)
                    if v111_react:
                        call r13_lines(v111_react,"v111:present_reaction:"+v111_person+":"+v111_shown)
                    else:
                        $ renpy.notify("지금은 이 자료로 더 확인할 내용이 없다.")
            if isinstance(_return,tuple) and len(_return)==2 and _return[0]=="followup":
                $ v111_follow=_return[1]
                call r13_lines(r13_v111_followup_lines(v111_follow),"v111:followup:"+v111_follow)
        jump r13_v111_wait_again
    if v111_pick[0]=="object":
        $ v111_pick=("object",r13_v111_object_key(v111_pick[1]))
        $ v111_matches=[i for i,o in enumerate(v111_binding.get("options",[])) if o.get("object")==v111_pick[1] and o.get("location")==room13["location"]]
        if len(v111_matches)==1:
            $ r13_v111_time("inspect:"+key+":"+v111_pick[1],0 if key=="gate_investigate" and v111_pick[1]=="ledger" else 15)
            return v111_binding["options"][v111_matches[0]].get("index",v111_matches[0])
        if len(v111_matches)>1:
            $ v111_object_options=[(v111_binding["options"][i]["title"],i) for i in v111_matches]
            $ v111_result=renpy.display_menu(v111_object_options)
            return v111_binding["options"][v111_result].get("index",v111_result)
        $ v111_object_spec=ROOM13["objects"].get(room13["location"],{}).get(v111_pick[1],{})
        $ v111_ambient=r13_v111_ambient_text(v111_pick[1],v111_object_spec)
        if v111_ambient:
            $ r13_field_reading=True
            # 2026-10-27 소유자 플레이: 물건을 눌러도 지문 한 줄뿐이고 아빠·다람 주고받기(R13_OBSERVATION_CHAT)가 안 붙었다.
            # 반응 표는 옛 경로(room13.rpy)의 r13_observe 에만 걸려 있었다. 같은 라벨로 돌려 생각 줄과 주고받기를 붙인다.
            call r13_observe([(None,v111_ambient)],"object:"+room13["location"]+":"+v111_pick[1])
            $ r13_field_reading=False
    jump r13_v111_wait_again

default r13_nw_wrong_pending = None
default r13_nw_can_solve = None

label r13_nw_wrong_thought:
    # 2026-10-24 지시서 01 4번: 틀린 뒤 아빠 속말(문구는 room13_v111_newworld_rules.rpy R13_NW_WRONG_THOUGHTS).
    if r13_nw_wrong_pending:
        $ v111_wrong_text=r13_nw_wrong_pending[1]; r13_nw_wrong_pending=None
        call r13_lines([r13_nw_added_line(dict(kind="thought",text=v111_wrong_text))],"v111:wrong_thought")
    return

label r13_v111_proof(key,correct,success,wrong=None,hint=None,review_return=None):
    # 2026-10-27 UX 인계서 D04: review_return 이 있으면 「조사 계속」으로 그 현장 라벨로 돌아간다(기회·선택·판정 불변).
    call r13_nw_wrong_thought
    $ v111_claim="v111:"+key
    $ R13_CLAIMS[v111_claim]=dict(assertion=R13_PROOF_TITLES.get(key,key))
    $ room13["arguments"].setdefault(v111_claim,[])
label r13_v111_proof_again:
    # 2026-10-27 UX 인계서 D01~D03·D06: 시범 쟁점(systems/room13_proof_workspace.rpy R13_PW_CONTEXT)은 통합 화면.
    # 반환값("argue"/"press"/"investigate"/("remove",키)/("toggle",키))은 아래 기존 분기로 그대로 흐른다.
    # 그 밖의 쟁점과 옛 캠페인은 기존 자료 대조 패널 + 자료 고르기 책(r13_v111_proof_pick)이다.
    if r13_pw_active(key):
        call screen r13_proof_workspace(v111_claim,key,can_press=bool(hint) or key in R13_PROOF_RANGE,investigate=bool(review_return),chances=r13_v111_proof_chances(key))
    else:
        call screen r13_crisis_proof(v111_claim,heading="기록 · 자료 대조",can_press=bool(hint) or key in R13_PROOF_RANGE,need_evidence=True,leave_label="자료 다시 보기",chances=r13_v111_proof_chances(key),investigate=bool(review_return))
    if _return=="investigate" and review_return:
        return review_return
    if _return=="present":
        jump r13_v111_proof_pick
    if isinstance(_return,tuple) and len(_return)==2 and _return[0]=="toggle" and _return[1] in room13["evidence"]:
        # 통합 화면의 체크(화면 안에서 r13_pw_toggle_action 이 처리하지만, 반환으로 와도 같은 규칙). 기회를 쓰지 않는다.
        $ v111_copy=winter_copy.deepcopy(room13); v111_copy["arguments"][v111_claim]=r13_pw_toggle(v111_copy["arguments"][v111_claim],_return[1],room13["evidence"],(r13_pw_context(key) or {}).get("mode","proof"))[0]; room13=v111_copy
        jump r13_v111_proof_again
    if isinstance(_return,tuple) and len(_return)==2 and _return[0]=="remove":
        # 0.20.7 (Codex A02): a record taken back before it is argued; no chance is spent.
        $ v111_copy=winter_copy.deepcopy(room13); v111_copy["arguments"][v111_claim]=[k for k in v111_copy["arguments"][v111_claim] if k!=_return[1]]; room13=v111_copy
        jump r13_v111_proof_again
    if _return=="argue" and not room13["arguments"][v111_claim]:
        jump r13_v111_proof_again  # 0.20.5 (Codex A01): an empty submission costs nothing
    if _return=="argue":
        # D04: 오답 안내가 「다 있었다」를 거짓으로 말하지 않도록, 정답 세트 하나를 보유 자료만으로 꾸릴 수 있는지를 지금 적어 둔다.
        $ r13_nw_can_solve=(key,any(need<=set(room13["evidence"]) for need in r13_v111_proof_sets(key,correct)))
        if r13_v111_proof_accepts(key,correct,room13["arguments"][v111_claim]):
            $ r13_v111_set("proof_given:"+key,sorted(room13["arguments"][v111_claim]))
            $ r13_proof_guide_finish()  # 2026-10-27: 첫 제출 성공 뒤에는 단계 안내를 줄인다.
            return success
        $ v111_last_presented=list(room13["arguments"][v111_claim])
        $ v111_wrong_target="r13_v111_gate_number" if v111_claim=="v111:함께 들어갈 근거를 고른다" and room13["arguments"][v111_claim]==["V111:E03"] and not r13_v111_value("gate_hardened") else wrong
        $ v111_copy=winter_copy.deepcopy(room13); v111_copy["arguments"][v111_claim]=r13_v111_proof_kept(key,correct,v111_last_presented); room13=v111_copy
        if v111_wrong_target:
            return v111_wrong_target
    if _return=="press" and hint:
        return hint
    if _return=="press" and key in R13_PROOF_RANGE:
        # 0.20.10 (4~14일 리뷰 D5-02 등): 되묻기는 이 대조가 무엇과 무엇을 맞추는지만 짚는다.
        call r13_lines([r13_nw_added_line(dict(speaker="아빠",kind="thought",text=R13_PROOF_RANGE[key]))],"v111:proof_range")
    if _return=="leave":
        call screen r13_book(called=True)  # 0.20.6: X returns here instead of hiding the called screen
    jump r13_v111_proof_again

label r13_v111_proof_pick:
    # 0.20.7 (Codex A05, owner "다 해줘"): the book stays open while records are added; picking a
    # record already on the table takes it back; 「선택 마치기」 returns to the proof without submitting.
    call screen r13_book("dad",present=True,purpose=("compare" if key in R13_SELF_COMPARE_PROOFS else "proof"),chosen=list(room13["arguments"][v111_claim]))
    if _return and _return in room13["evidence"]:
        $ v111_copy=winter_copy.deepcopy(room13)
        if _return in v111_copy["arguments"][v111_claim]:
            $ v111_copy["arguments"][v111_claim]=[k for k in v111_copy["arguments"][v111_claim] if k!=_return]
        else:
            $ v111_copy["arguments"][v111_claim].append(_return)
        $ room13=v111_copy
        jump r13_v111_proof_pick
    jump r13_v111_proof_again

label r13_v111_travel(destination,travel_id,companions=None,direct=False):
    if room13["location"]==destination:
        return
    $ v111_travel_origin=room13["location"]
    if companions is None:
        $ companions=[]
        if not r13_v111_value("DARAM_DETAINED") and r13_v111_value("location:daram") in (None,v111_travel_origin) and not (r13_v111_value("busy:mom")=="daram_guard") and not (r13_v111_value("DARAM_location")=="school" and r13_v111_value("busy:nabi")=="daram_guard") and not (r13_v111_value("DARAM_location")=="room13" and room13["v111"].get("scene")=="MS14_D07_S04"):
            $ companions.append("daram")
        if r13_v111_value("family_reunited") and r13_v111_value("location:mom")==v111_travel_origin and not r13_v111_value("busy:mom"):
            $ companions.append("mom")
    $ room13["v111"]["travel_to"]=destination
    if direct:
        # 0.20.6 (owner day-1 play): a chosen purpose ("할머니에게 묻는다") goes straight there.
        $ r13_edit(location=destination)
        call r13_scene(R13_PLACES[destination][1],R13_PLACES[destination][0],"calm")
    else:
        call r13_v111_wait("travel")
    # 2026-10-24 행동 검수 4: 도착했으니 「생각」은 이 장면 문구로 바뀐다(이어서 또 이동해도 앞 장면으로 돌아가지 않는다).
    $ room13["v111"]["thought_pending"]=False
    $ r13_v111_arrive(companions)
    return

init 302 python:
    # Reuse by meaning, not by the old campaign's numeric evidence ID.
    R13_V111_MATERIAL_ART={
        "E01":"E01","E02":"G3","E03":"G1","E04":"G2","E05":"E02",
        "E06":"tool:paper","E07":"G3","E08":"bag:lantern","E11":"E17",
        "E12":"tool:paper","E13":"E20","E14":"G3","E16":"E17",
        "E31":"E29","E33":"bag:knife","E34":"G3","E35":"bag:blanket",
        "E27":"E01","E28":"bag:postcard",
    }
    _r13_v111_material_art=r13_material_art
    def r13_material_art(key):
        if r13_v111_active() and key=="V111:E13_MENDING" and r13_v111_owned("E13_MENDING"):
            return Transform("assets/room13-v111-blanket-after.webp",xysize=(160,100),fit="contain",nearest=True)
        if r13_v111_active() and key in ("V111:E09","V111:E30"):
            art=("portrait_"+r13_v111_value("portrait")) if key=="V111:E09" else "bundle"
            if art=="portrait_child_completed":art="portrait_child"
            if art in MS14_ART:return Transform(MS14_ART[art]["file"],xysize=(160,100),fit="contain",nearest=True)
        if r13_v111_active() and isinstance(key,str) and key.startswith("V111:"):
            original=R13_V111_MATERIAL_ART.get(key[5:])
            if original:return _r13_v111_material_art(original)
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
        # 2026-10-24 지시서 01 1번: 칼 대조 동의는 회의 진입 조건에서 뺐다. 동의가 없어도 회의는 열리고 칼 쟁점은 이길 수 있다.
        "MS14_D03_S05":(["E11","E12","E13","E14","E15","E16","E32"],{"silluk.children.location":"workshop_with_buri"}),
        "MS14_D03_S06":([],{"lamp_theft_supported":True,"stone_choice_completed":True}),
    }
    def r13_v111_thought_hold(scene):
        """2026-10-24 행동 검수 4: 장면은 이동 「전에」 지정된다. 그래서 지도 화면의 「생각」이 도착할 장면의
        일(아직 일어나지 않은 비명, 만나지 않은 사람)을 먼저 말했다. 장면이 실제로 바뀌는 순간 마지막으로 보인
        장면을 적어 두고, 이동 대기 동안에는 그 장면의 문구를 보인다(r13_v111_goal). 도착 뒤 첫 대기에서 놓는다.
        진입이 거절된 장면은 값을 바꾸지 않으므로 이 함수는 거절 검사를 다 지난 뒤에만 부른다."""
        v=store.room13["v111"]
        if v.get("scene")!=scene and not v.get("thought_pending"):
            v["thought_scene"]=v.get("scene");v["thought_pending"]=True
    def r13_v111_scene(scene):
        marker="v111:entered:"+scene
        if r13_has(marker):
            r13_v111_thought_hold(scene)
            store.room13["v111"]["scene"]=scene
            return
        if store.room13["day"]!=R13_V111["scene_days"][scene]:raise Exception("Wrong authored day: "+scene)
        if scene=="MS14_D02_S04" and r13_v111_value("D02_afternoon") not in (None,"uncommitted"):raise Exception("Afternoon already committed")
        if scene=="MS14_D02_S05" and r13_v111_value("D02_afternoon") not in ("shelter","nero"):raise Exception("Missing afternoon decision")
        if scene=="MS14_D03_S06" and r13_v111_value("silluk_status") not in ("reporting_obligation","detained_work_waiting_station","released"):raise Exception("Missing custody decision")
        check=globals().get("R13_V111_SCENE_CHECKS",{}).get(scene)
        if check and not check():raise Exception("Unmet authored scene state: "+scene)
        items,values=R13_V111_ENTRY.get(scene,([],{}))
        if scene=="MS14_D03_S05" and r13_v111_value("lamp_bound2"):
            items,values=(["NW_LA_CHECK","NW_LA_FIELD","NW_LA_KNIFE","NW_LA_OFFER"],{"silluk.children.location":"workshop_with_buri"})
        if not all(r13_v111_owned(x) for x in items) or not all(r13_v111_value(k)==v for k,v in values.items()):raise Exception("Unmet authored scene entry: "+scene)
        if scene=="MS14_D02_S01" and not r13_has("v111:applied:option:sleep1:0"):raise Exception("Missing actual first-night sleep")
        if scene=="MS14_D03_S01" and not r13_has("v111:applied:option:sleep2:0"):raise Exception("Missing actual second-night sleep")
        r13_v111_thought_hold(scene)
        store.room13["v111"]["scene"]=scene
        r13_flag(marker)

init 304 python:
    def r13_v111_score():
        scene=store.room13.get("v111",{}).get("scene")
        r13_sound_ambience(R13_V111.get("ambience",{}).get(scene))
        if store.room13["v111"].get("music_hold")==scene:return
        override=store.room13["v111"].get("music_override",{})
        track=override.get("path") if override.get("scene")==scene else R13_V111.get("audio",{}).get(scene)
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
        elif key=="V111:E14_SUPPLY":
            record=dict(record)
            record["establishes"]=("아빠와 까로가 운반한 장작 묶음을 선생님이 인수했고, 학교에서 실제로 때고 있다. 쓴 양과 남은 양을 확인했다." if r13_v111_value("school_heat_connected") else "아빠와 까로가 운반한 장작 묶음을 선생님이 인수했다. 오늘 밤 쓸 양은 따로 확인한다.")  # 0.20.5 Codex B01
        elif key=="V111:E35":
            record=dict(record)
            received=r13_v111_value("E35.status")=="received"
            record["name"]="가족 침구 · "+("수령 완료" if received else "예약")
            record["establishes"]="마른 담요 두 장을 실제로 받았다." if received else "마른 담요 두 장을 예약했다. 아직 받지 않았다."
        return record

init 307 python:
    R13_BOOK_PURPOSE=dict(proof=("근거에 추가","근거로 낼 자료"),use=("이 기록을 꺼낸다","꺼낼 기록"))
    _r13_v111_scene_music=r13_sound_scene_music
    def r13_sound_scene_music(bg,title,mood="calm"):
        if r13_v111_active():
            scene=store.room13["v111"].get("scene")
            r13_sound_ambience(R13_V111.get("ambience",{}).get(scene))
            if store.room13["v111"].get("music_hold")==scene:return None
            override=store.room13["v111"].get("music_override",{})
            if override.get("scene")==scene:return override["path"]
            if scene in R13_V111.get("audio",{}):return R13_V111["audio"][scene]
        return _r13_v111_scene_music(bg,title,mood)

init 304 python:
    # 0.19.95: in the new-world flow, someone who speaks or comes on screen in a
    # conversation counts as met, so they appear on the relations chart (older flows
    # recorded this through the topic screen, which v111 conversations skip).
    _r13_v111_speaker_base=r13_speaker
    def r13_speaker(who,expression="neutral",pose=None):
        if (r13_v111_active() and who in R13_NAMES and who not in ("dad","daram")
                and who!=r13_viewpoint() and who not in r13_met_people()):
            r13_note_encounter(who)
        return _r13_v111_speaker_base(who,expression,pose)
