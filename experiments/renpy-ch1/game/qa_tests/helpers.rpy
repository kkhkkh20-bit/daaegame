# Helpers for game/qa_tests/tests.rpy (state setup and result dumps). Not shipped.

init 999:
    screen r13_book(target=None,present=False,hearing=False):
        modal True
        zorder 60
        add Solid("#000c")
        vbox:
            xpos 40 ypos 40 spacing 4
            for k in room13["evidence"]:
                textbutton ("QA "+k) action Return(k)
            textbutton "QA 닫기" action Return(None)

init 999 python:
    def r13_qa_dump():
        d=dict(result=room13.get("trial_result"),daram=room13.get("daram_state"),granny=room13.get("granny_state"),
            props=list(room13["propositions"]),closed=dict(room13.get("debate",{}).get("closed",{})),
            ending=room13.get("ending"),open={c:r13_debate_open(c) for c in ("F1","F2","F3","F4")} if room13.get("finale_started") else None)
        open(renpy.config.basedir+"/qa_result.txt","w").write(repr(d))

label r13_qa_setup(day,ev,flags=()):
    $ room13_mode=True
    $ winter_mode=True
    $ winter=winter_new()
    $ source_mode=False
    $ room13=r13_new()
    $ r13_world_cameras={}
    $ r13_inspection_location=None
    $ r13_prepare_history()
    $ r13_scene_key=None
    $ r13_upgrade()
    $ typing_allowed=True
    hide screen winter_hud
    hide screen hud
    $ room13.update(day=day,period=0,case_state="occurred",victim_state="dead",location="inn",life_poc=True)
    $ room13["evidence"]=list(ev)
    # Older trial tests assume the episode gates are open (systems/room13_episodes.rpy);
    # "-gates" in flags removes them.
    $ _qa_gates=set() if "-gates" in flags else {"witness:nabi","witness:tok","fair_hearing"}
    $ room13["flags"]=list(set(room13["flags"])|{"lodging","entry_corrected","livelihood_open"}|_qa_gates|(set(flags)-{"-gates"}))
    return

label r13_qa_trial(ev,flags=()):
    call r13_qa_setup(7,ev,flags)
    $ room13["daram_state"]="held"
    jump r13_trial

label r13_qa_finale(ev,flags=()):
    call r13_qa_setup(14,ev,flags)
    $ room13.update(daram_state="with_dad",trial_ended=True,trial_result="cleared",finale_started=True,location="altar",mom_state="reunited",week2_started=True)
    $ room13["flags"]=list(set(room13["flags"])|{"mom_reunited"})
    call r13_scene("r13_altar","북쪽 산길 끝 · 숲속 제단","hearing")
    jump r13_final_hub

label r13_qa_view:
    $ room13_mode=True
    $ winter_mode=True
    $ winter=winter_new()
    $ source_mode=False
    $ room13=r13_new()
    $ r13_world_cameras={}
    $ r13_inspection_location=None
    $ r13_prepare_history()
    $ r13_scene_key=None
    $ r13_upgrade()
    $ typing_allowed=True
    hide screen winter_hud
    hide screen hud
    $ room13.update(r13_qa_state)
    $ room13["flags"]=list(set(room13.get("flags",[]))|{"livelihood_open","lodging"})
    $ room13["checks"]=dict(r13_qa_checks)
    $ place=R13_PLACES[room13["location"]][0]
    call r13_scene(R13_PLACES[room13["location"]][1],place,"calm")
    call screen r13_hub
    return
init 999 python:
    R13_QA_ORIG_PEOPLE=r13_people
    r13_qa_state={}
    r13_qa_checks={}


label r13_qa_shop:
    $ room13_mode=True
    $ winter_mode=True
    $ winter=winter_new()
    $ source_mode=False
    $ room13=r13_new()
    $ r13_world_cameras={}
    $ r13_prepare_history()
    $ r13_scene_key=None
    $ r13_upgrade()
    $ room13.update(location="market",day=5,period=0,life_poc=True,case_state="occurred")
    $ room13["flags"]=list(set(room13["flags"])|{"lodging","entry_corrected","livelihood_open"})
    $ room13["livelihood"]=dict(cash=40,debt=0)
    call r13_scene(R13_PLACES["store"][1],R13_PLACES["store"][0],"calm")
    call screen r13_topics("resident_eunho")
    $ room13["livelihood"]=dict(cash=40,debt=0)
    call screen r13_shop
    return

init 999 python:
    def r13_qa_items_chain():
        import json
        st=store.room13;log={}
        st.update(day=5,period=0,case_state="occurred",location="workshop",life_poc=True,secret_route_unlocked=False)
        st["flags"]=list(set(st["flags"])|{"lodging","entry_corrected","livelihood_open","life:buri_honest","lamplighter_trust"})
        st["livelihood"]=dict(cash=30,debt=0)
        log["buri_topics"]=[k for k,s in r13_topics("buri")]
        r13_finish_topic("borrow:knife");r13_finish_topic("borrow:lantern")
        log["after_borrow"]=r13_wallet(store.room13)
        def acts(loc,obj):
            store.room13["location"]=loc
            return [a for a,s in r13_object_actions(obj)]
        log["room13_books_visible_before"]=r13_object_visible(ROOM13["objects"]["room13"]["books"])
        log["under"]=acts("room13","under")
        r13_finish_action("use_knife_under")
        log["kitchen_rear"]=acts("kitchen","rear")
        r13_finish_action("use_lantern_rear")
        log["room13_books_visible_after"]=r13_object_visible(ROOM13["objects"]["room13"]["books"])
        log["books"]=acts("room13","books")
        log["route_before"]=r13_secret_route_available()
        r13_finish_action("use_knife_books")
        log["route_after"]=r13_secret_route_available()
        log["kitchen_shelf_visible"]=r13_object_visible(ROOM13["objects"]["kitchen"]["shelf"])
        log["workshop_plans_visible"]=r13_object_visible(ROOM13["objects"]["workshop"]["plans"])
        store.room13["location"]="workshop"
        log["map_activity_spec_secret"]=ROOM13["activities"]["map"].get("secret_route_only")
        log["passage_place"]="passage" in r13_places() if "r13_places" in globals() else None
        store.room13["livelihood"]=dict(r13_wallet(store.room13),cash=store.room13["livelihood"].get("cash",0)+20)
        r13_life_apply_purchase("rubbing");r13_life_apply_purchase("weight")
        log["square_stone"]=acts("square","stone")
        r13_finish_action("use_rubbing_stone")
        log["store_scale"]=acts("store","scale");log["store_burlap"]=acts("store","burlap")
        r13_finish_action("use_weight_scale");r13_finish_action("use_knife_burlap")
        log["eunho_topics"]=[k for k,s in r13_topics("resident_eunho")]
        r13_finish_topic("eunho_scale");r13_finish_topic("eunho_hidden")
        log["price_snack"]=r13_shop_price(store.room13,"snack");log["price_herbs"]=r13_shop_price(store.room13,"herbs")
        log["ppul_topics"]=[k for k,s in r13_topics("resident_ppul")]
        store.room13["location"]="workshop"
        log["buri_after"]=[k for k,s in r13_topics("buri")]
        r13_finish_topic("return:knife")
        log["final_wallet"]=r13_wallet(store.room13)
        log["evidence"]=[e for e in store.room13["evidence"] if e in ("M02","R01","R02")]
        log["flags"]=[f for f in store.room13["flags"] if f in ("soot_trail","passage_found","hidden_stock","scale_rigged","shop_discount","supply_terms","eunho_exposed")]
        open(renpy.config.basedir+"/qa_items.json","w").write(json.dumps(log,ensure_ascii=False,indent=1,default=str))

init 999 python:
    def r13_qa_override_chains(names):
        """Runtime call chain of each overridden function: [(file, line), ...] outermost first."""
        import json
        out={}
        for name in names:
            fn=getattr(store,name,None);seen=[]
            while fn is not None and hasattr(fn,"__code__") and len(seen)<30:
                code=fn.__code__
                seen.append([code.co_filename.split("/game/")[-1],code.co_firstlineno])
                inner=None
                for ref in code.co_names:
                    cand=getattr(store,ref,None)
                    if ref!=name and callable(cand) and getattr(cand,"__name__","")==name:
                        inner=cand;break
                fn=inner
            out[name]=seen
        open(renpy.config.basedir+"/qa_result.txt","w").write(json.dumps(out))

# Town events: set up a state and enter it through r13_roam (so arrival events run).
label r13_qa_roam(state,flags=(),items=(),cash=0):
    # The owner's admin tool is a persistent toggle; tests always start without it.
    $ persistent.room13_admin=False
    $ r13_admin_hitboxes=False
    $ room13_mode=True
    $ winter_mode=True
    $ winter=winter_new()
    $ source_mode=False
    $ room13=r13_new()
    $ r13_world_cameras={}
    $ r13_inspection_location=None
    $ r13_prepare_history()
    $ r13_scene_key=None
    $ r13_upgrade()
    $ typing_allowed=True
    hide screen winter_hud
    hide screen hud
    show screen r13_hud
    $ room13.update(state)
    # Evening brief (systems/room13_evening.rpy) is skipped unless "+brief" is passed;
    # the week-1 cases G·L·I·S·T (systems/room13_week1_cases.rpy) unless "+w1c" is passed.
    $ room13["flags"]=list(dict.fromkeys(room13["flags"]+["lodging","entry_corrected","livelihood_open"]+([] if "+offers" in flags else ["qa_auto_offer"])+[f for f in flags if f not in ("+brief","+w1c","+offers")]+([] if "+brief" in flags else ["evening_brief:%d"%d for d in range(1,14)])+([] if "+w1c" in flags else ["ev_g_done","ev_l_done","ev_i_done","ev_s_done","ev_t_done","ev_owl_threshold_done","ev_owl_omen_done"])))
    $ room13["livelihood"]=dict(cash=cash,debt=0,items=list(items))
    jump r13_roam

init 999 python:
    def r13_qa_town_dump():
        import json
        s=store.room13;w=r13_wallet(s)
        keep=("ev_","somi_","musoe_","madam_","mungchi_","know_","kongi_","roof_path","room_searched","warning_exposed","goods_recovered","yeoni_","eunho_holds","rumor:","bami_","patrol_","badook_","kids_","nabi_","witness:","fair_hearing","ppul_","tok_","seori_","ubak_","clue_","ep","siluk_","nubi_","lodging_cheap","quarantined","medkit")
        out=dict(day=s["day"],period=s["period"],location=s["location"],cash=w["cash"],items=w["items"],
            flags=sorted(f for f in s["flags"] if f.startswith(keep)),
            evidence=[e for e in s["evidence"] if e[0] in "HW"],town=s.get("town",{}))
        open(renpy.config.basedir+"/qa_result.txt","w").write(json.dumps(out,ensure_ascii=False))

label r13_qa_talk(person):
    # Already met: skip the first-approach choice.
    $ r13_note_encounter(person)
    $ r13_target=person
    call r13_talk
    jump r13_roam

# 0.18.76: run one event label directly from the field and come back through r13_roam.
label r13_qa_event(name):
    call expression name
    jump r13_roam

# 0.18.76: step into a pending event offer from the field and come back through r13_roam.
label r13_qa_offer(key):
    call r13_take_offer(key)
    jump r13_roam

# 0.18.75: press an inspection spot from the field and come back through r13_roam.
label r13_qa_object(key):
    call r13_object(key)
    jump r13_roam

# Move within the same run (keeps state) and arrive through r13_roam.
label r13_qa_goto(day,period,location,flags=()):
    $ r13_edit(day=day,period=period,location=location)
    $ r13_flag(*flags) if flags else None
    jump r13_roam

# Sound check (0.18.6): visit every place in each mood and record what plays.
label r13_qa_sound:
    call r13_qa_setup(3,("E01","E05"))
    $ _qa_sound={"title":config.main_menu_music,"places":{},"fx":{}}
    $ _qa_bgs=sorted(R13_PLACE_SOUND)
    $ _qa_i=0
    while _qa_i<len(_qa_bgs):
        $ _qa_bg=_qa_bgs[_qa_i]
        $ _qa_row=[]
        $ _qa_m=0
        while _qa_m<4:
            $ _qa_mood=("calm","search","night","quiet")[_qa_m]
            $ r13_scene_key=None
            call r13_scene(_qa_bg,"QA "+_qa_bg,_qa_mood)
            $ _qa_row.append((_qa_mood,renpy.music.get_playing(),renpy.music.get_playing(channel="ambience")))
            $ _qa_m+=1
        $ _qa_sound["places"][_qa_bg]=_qa_row
        $ _qa_i+=1
    $ r13_scene_key=None
    call r13_scene("hall","여관 2층 · 연기가 새는 문","quiet")
    $ _qa_sound["smoke_door"]=(renpy.music.get_playing(),renpy.music.get_playing(channel="ambience"))
    python:
        for k in R13_FX:
            _qa_sound["fx"][k]=renpy.loadable(r13_fx_path(k))
        _qa_sound["bgm_loadable"]=all(renpy.loadable(p) for p in R13_BGM.values())
        _qa_sound["amb_loadable"]=all(renpy.loadable(p) for p in R13_AMBIENCE.values())
        _qa_sound["click"]=style.button.activate_sound
        _qa_sound["judge"]=r13_debate_judge("C1",r13_debate_statements("C1")[0]["id"],"E05")[0]
        _qa_sound["judge_fx"]=renpy.music.get_playing(channel="scene_fx")
        _qa_sound["moves"]={a+">"+b:r13_sound_move(a,b) for a,b in (("hall","room"),("room","hall"),("front","hall"),("front","winter_square"),("winter_square","winter_post"),("hall","winter_passage"),("winter_passage","room"),("winter_carriage","winter"))}
        open(renpy.config.basedir+"/qa_result.txt","w").write(repr(_qa_sound))
    return

label r13_qa_linebreak:
    call r13_scene("hall","QA 줄바꿈","calm")
    call r13_lines([("resident_seori","부엉이 어르신이 발견된 방은 안에서 잠겨 있었습니다. 안에는 다람 양이 있었습니다."),
        (None,"팔의 상처만으로는 목숨을 앗아 간 머리 상처를 설명할 수 없습니다. 떨어져 나간 촛대 윗부분이 다시 쓰였습니다. 그 사이 아이가 어디 있었는지, 누가 다른 길로 드나들었는지 함께 봐야 합니다.")],"qa:linebreak")
    $ open(renpy.config.basedir+"/qa_result.txt","w").write("linebreak done")
    return

init 999 python:
    def r13_goal_is_question():
        # Field guidance in the first days names an open question, never "show X to Y".
        g=r13_intro_goal()
        return g.rstrip().endswith("?") or "?" in g

    r13_qa_last_present=""
    def r13_qa_present(person,key):
        store.r13_qa_last_present=" ".join(line[1] for line in r13_present(person,key))

label r13_qa_grudge(key):
    $ r13_topic="grudge_fix:"+key
    call r13_grudge_fix
    jump r13_roam

init 999 python:
    def r13_qa_price(*flags):
        st=winter_copy.deepcopy(store.room13);st["flags"]=list(flags)
        return r13_shop_price(st,sorted(R13_SHOP)[0])

label r13_qa_delivery:
    $ r13_job_key="delivery"
    $ r13_job_question=R13_JOBS["delivery"]["choice"]
    call r13_delivery_inspect
    $ store.r13_qa_dv_choice=r13_job_choice
    jump r13_roam

init 999 python:
    def r13_qa_present_deferred(person,key):
        store.r13_defer_grants=True
        store.r13_qa_last_present=" ".join(line[1] for line in r13_present(person,key))
        store.r13_defer_grants=False

label r13_qa_gate_shelf:
    # Same path as clicking the shelf at the gate (0.18.22).
    call r13_object("gate_documents")
    jump r13_entry

label r13_qa_life(name):
    # Runs one life close-up from the field and returns there (0.18.22).
    $ r13_job_question=R13_JOBS["kitchen"]["choice"]
    $ r13_job_choice=None
    call expression name
    $ store.r13_qa_dv_choice=r13_job_choice
    jump r13_roam

label r13_qa_life_door:
    call r13_qa_life("r13_life_door")

label r13_qa_life_meal:
    call r13_qa_life("r13_life_meal")

# 0.18.5 full-body dialogue check: every character x expression in the real
# dialogue layout (normal and large text) and the topic list layout.
default r13_qa_fb_done = False
init 999 python:
    def r13_qa_fullbody_capture(modes=("normal","large","topic"),people=None,emotions=None):
        import os, json as qa_json
        out=os.path.join(os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa"),"fullbody")
        if not os.path.isdir(out):os.makedirs(out)
        preferences.text_cps=0
        report=[]
        people=people or [p for p in sorted(R13_FULLBODY["people"]) if p!="dad"]
        emotions=emotions or list(R13_FULLBODY_EMOTIONS)
        for mode in modes:
            persistent.room13_large_text=(mode=="large")
            for person in people:
                for emotion in (emotions if mode!="topic" else ["neutral"]):
                    if mode=="topic":
                        renpy.hide("r13_visitor")
                        renpy.show_screen("r13_question_list",person,"neutral","선택",[],False,animate=False)
                        renpy.pause(0.35,hard=True)
                    else:
                        r13_speaker(person,R13_FULLBODY_TO_LEGACY[emotion],emotion)
                        renpy.say(R13_CHARS.get(person),"표정 확인 %s — 대사창과 얼굴이 겹치는지 보는 두 줄짜리 시험 문장입니다. 끝까지 읽히는지도 확인합니다."%emotion,interact=False)
                        renpy.pause(0.45,hard=True)
                    name="%s_%s_%s.png"%(mode,person,emotion)
                    renpy.screenshot(os.path.join(out,name))
                    bounds=renpy.get_image_bounds("r13_visitor") if mode!="topic" else None
                    report.append(dict(mode=mode,person=person,emotion=emotion,file=name,bounds=bounds,
                        y=r13_close_y(person,760 if mode=="topic" else 840,126 if mode=="topic" else 110,emotion),
                        scale=r13_fullbody_scale(person,760 if mode=="topic" else 840),
                        spec=(r13_fullbody_spec(person,emotion) or {}).get("file")))
                    if mode=="topic":renpy.hide_screen("r13_question_list")
        persistent.room13_large_text=False
        open(os.path.join(out,"report.json"),"w").write(qa_json.dumps(report,ensure_ascii=False,indent=0))
        store.r13_qa_fb_done=True

label r13_qa_fullbody(modes=("normal","large","topic"),people=None,emotions=None):
    call r13_qa_setup(5,["E01"])
    call r13_scene(R13_PLACES["inn"][1],R13_PLACES["inn"][0],"quiet")
    $ r13_qa_fullbody_capture(modes,people,emotions)
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(done=r13_qa_fb_done)))
    return

# 0.18.5: authored per-line emotions reach the real dialogue loop.
default r13_qa_le_log = []
init 999 python:
    R13_QA_LINE_CASES = [('trial:C2:wrong', 'buri', '할아버지도 착한 사람이었어요. 그런 말로 끝내지 말아요.', None, 'angry'), ('entry:daram:waiting', 'daram', '아빠, 이거 안 열려.', None, 'flustered'), ('case:unpreserved:v3', 'buri', '할아버지! 비켜요!', None, 'surprise'), ('topic:buri_records', 'buri', '전날 저녁엔 많이 심했어요. 나를 알아보지 못할 때도 있었고.', None, 'anxious'), ('qa:legacy', 'karo', '기존 expressive 키는 기쁨 표정으로 이어집니다.', 'expressive', 'joy'), ('qa:direct', 'karo', '새 표정 키를 대사에 직접 적을 수 있습니다.', 'surprise', 'surprise'), ('trial:C2:wrong', 'buri', '대사가 바뀌면 지정이 적용되지 않습니다.', 'distressed', 'anxious')]
    def r13_qa_le_record():
        who=store.r13_motion_person
        spec=r13_fullbody_spec(who,store.r13_current_pose) if who else None
        store.r13_qa_le_log.append(dict(who=who,pose=store.r13_current_pose,expression=store.dialogue_expression,file=(spec or {}).get("file"),showing="r13_visitor" in renpy.get_showing_tags()))

label r13_qa_line_emotions:
    call r13_qa_setup(5,["E01"])
    call r13_scene(R13_PLACES["inn"][1],R13_PLACES["inn"][0],"quiet")
    $ preferences.text_cps=0
    $ r13_qa_le_i=0
    while r13_qa_le_i<len(R13_QA_LINE_CASES):
        $ _c=R13_QA_LINE_CASES[r13_qa_le_i]
        call r13_lines([(_c[1],_c[2],_c[3])] if _c[3] else [(_c[1],_c[2])],_c[0])
        $ r13_qa_le_i+=1
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(log=r13_qa_le_log,expected=[c[4] for c in R13_QA_LINE_CASES])))
    return

# 0.18.5 inn lobby/hall v4 chips and the supplementary guide.
default r13_qa_inn_log = []
init 999 python:
    def r13_qa_inn_note(tag):
        st=store.room13
        chips=[(k,l,a) for k,l,r,a in r13_inn_v4_chips(st["location"],True)+r13_inn_v4_chips(st["location"],False)]
        m=renpy.get_screen("r13_map")
        guide=[(i["key"],i["text"],i["target"]) for i in r13_inn_guide_labels()] if renpy.get_screen("r13_inn_guide") else None
        store.r13_qa_inn_log.append(dict(tag=tag,location=st["location"],day=st["day"],period=st["period"],chips=chips,
            row=[k for k,t in r13_local_connections() if k not in r13_inn_v4_handled(st["location"])],
            guide=guide,map=bool(m),
            places=r13_places(),flags=sorted(st["flags"])))
    def r13_qa_inn_dump():
        open(renpy.config.basedir+"/qa_result.txt","w").write(repr(store.r13_qa_inn_log))

label r13_qa_inn_v4(case="pending"):
    call r13_qa_setup(2,["E01"])
    $ room13.update(case_state=case,victim_state="alive" if case=="pending" else "dead",location="inn",period=0)
    $ preferences.text_cps=0
    jump r13_roam

label r13_qa_gm(name):
    # Runs one hand-check close-up (0.18.22) and records whether it finished.
    call expression name
    $ store.r13_qa_dv_choice=_return
    jump r13_roam

label r13_qa_gm_package:
    call r13_qa_gm("r13_gm_package")

label r13_qa_gm_lamp:
    call r13_qa_gm("r13_gm_lamp")

label r13_qa_gm_scale:
    call r13_qa_gm("r13_gm_scale")

label r13_qa_gm_floor:
    call r13_qa_gm("r13_gm_floor")

label r13_qa_gm_stone:
    call r13_qa_gm("r13_gm_stone")

init 999 python:
    def r13_qa_scenario_dump():
        """Static scenario data as the running game sees it (0.18.22 audit)."""
        import json
        def lst(v):return list(v) if isinstance(v,(list,tuple,set)) else ([] if v is None else [v])
        out=dict(evidence={k:dict(name=v.get("name"),kind=v.get("kind"),est=v.get("establishes",""),notest=v.get("does_not_establish","")) for k,v in ROOM13["evidence"].items()},
            sources=dict(ROOM13.get("evidence_sources",{})),
            topics={k:dict(npc=v.get("npc"),title=v.get("title"),day=lst(v.get("day")),need=lst(v.get("need")),not_flags=lst(v.get("not_flags")),give=lst(v.get("give")),flags=lst(v.get("flags")),lines=len(v.get("lines",[]) or []),label=R13_TOPIC_LABELS.get(k),case=v.get("case"),state=v.get("state")) for k,v in ROOM13["topics"].items()},
            objects={loc:{k:dict(need=lst(v.get("need")),give=lst(v.get("give")),flags=lst(v.get("flags")),text=v.get("text","")) for k,v in objs.items()} for loc,objs in ROOM13["objects"].items()},
            activities={k:dict(place=v.get("place"),title=v.get("title"),day=lst(v.get("day")),need=lst(v.get("need")),not_flags=lst(v.get("not_flags")),give=lst(v.get("give")),flags=lst(v.get("flags")),cost=v.get("cost",1),special=bool(v.get("special")),case=v.get("case")) for k,v in ROOM13["activities"].items()},
            presentations=[dict(npc=p.get("npc"),items=lst(p.get("items")),topic=p.get("topic")) for p in ROOM13.get("presentations",[])],
            debate={c:dict(title=d.get("title"),accept=[lst(s.get("accept")) for s in d.get("statements",[])],soft=[list((s.get("soft") or {}).keys()) for s in d.get("statements",[])]) for c,d in R13_DEBATE.items()},
            offers=list(R13_EVENT_OFFERS),
            names=sorted(R13_NAMES),
            gimmicks=dict(R13_GIMMICK_LABELS),
            places=list(R13_PLACES))
        open(renpy.config.basedir+"/scenario_dump.json","w").write(json.dumps(out,ensure_ascii=False,indent=1))

label r13_qa_type_lines:
    # 0.18.24 typography: narration, Dad's thought (no parentheses in source), speech with an item.
    call r13_lines([(None,"책상 아래에 접힌 종이가 끼어 있다."),("dad","원본과 옮겨 쓴 명부가 다르다. 어디서 빠진 거지?",{"thought":True}),("dad","「예약 원본」에는 다람이 이름도 적혀 있습니다.")],"qa:typography")
    jump r13_roam

# 2026-10-15 NPC redesigns (dev/apply_npc_redesign.py): find a real slot where
# each redesigned NPC is scheduled, stand there and record the staging.
init 999 python:
    R13_QA_REDESIGNED = ("resident_yeoni","resident_momo","resident_librarian","resident_nubi","resident_seol","resident_siluk","resident_nero","resident_bori")
    def r13_qa_redesign_slot(person):
        saved=winter_copy.deepcopy(store.room13)
        try:
            for day in range(2,8):
                for period in (0,1):
                    store.room13.update(day=day,period=period)
                    where=r13_where(person)
                    if where in R13_MAP_NODES["village"]:
                        return (day,period,where)
        finally:
            store.room13=saved
        raise Exception("no slot for "+person)
    def r13_qa_redesign_record(person):
        import os, json as qa_json
        actors=[a for a in r13_stage_people(False) if a["person"]==person]
        path=renpy.config.basedir+"/qa_result.txt"
        log=qa_json.loads(open(path).read()) if os.path.exists(path) and open(path).read().startswith("{") else {}
        spec=r13_acting_spec(person,actors[0]["pose"]) if actors else None
        log[person]=dict(location=store.room13["location"],day=store.room13["day"],period=store.room13["period"],
            present=person in r13_people(),actor={k:actors[0][k] for k in ("pose","x","y","width","height","contact")} if actors else None,
            file=spec["file"] if spec else None,crop=spec["crop"] if spec else None,foot=spec.get("foot") if spec else None)
        open(path,"w").write(qa_json.dumps(log,ensure_ascii=False))

# 0.18.29: dot effects (systems/room13_dot_fx.rpy) captured in the real engine.
default r13_qa_fx_done = False
init 999 python:
    def r13_qa_fx_capture():
        import os, json as qa_json
        out=os.path.join(os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa"),"dot_fx")
        if not os.path.isdir(out):os.makedirs(out)
        report=dict(scenes={},blink={})
        for location,period in (("inn","evening"),("inn","morning"),("square","evening"),("gate","evening"),("altar","evening"),("square","morning")):
            renpy.scene()
            renpy.show("r13_qa_fx_bg",what=r13_world_background(location,period))
            shots=[]
            for i in range(3):
                renpy.pause(0.37,hard=True)
                name="%s_%s_%d.png"%(location,period,i)
                renpy.screenshot(os.path.join(out,name));shots.append(name)
            persistent.room13_motion=False
            renpy.pause(0.4,hard=True)
            name="%s_%s_off.png"%(location,period)
            renpy.screenshot(os.path.join(out,name));shots.append(name)
            persistent.room13_motion=True
            report["scenes"]["%s_%s"%(location,period)]=shots
        # 0.18.31: impact lines, evidence sparkle (and its card), dither transition plate.
        renpy.scene()
        renpy.show("r13_qa_fx_bg",what=r13_world_background("square","morning"))
        renpy.pause(1.2,hard=True)
        renpy.screenshot(os.path.join(out,"square_morning_smoke.png"))
        r13_fx_cue("present")
        renpy.pause(0.03,hard=True)
        renpy.screenshot(os.path.join(out,"impact.png"))
        renpy.pause(0.4,hard=True)
        renpy.hide_screen("r13_fx_impact")
        renpy.show_screen("r13_evidence_found",keys=["E01"],conversation=False)
        renpy.pause(0.22,hard=True)
        renpy.screenshot(os.path.join(out,"evidence_sparkle.png"))
        renpy.pause(0.5,hard=True)
        renpy.hide_screen("r13_evidence_found")
        report["dither"]=renpy.loadable(R13_DOT_FX["dither"]["file"])
        renpy.scene()
        renpy.show("r13_qa_fx_bg",what=r13_world_background("inn","evening"))
        preferences.text_cps=0
        for emotion in ("neutral","angry","joy"):
            spec=R13_DOT_FX["blink"]["people"]["daram"].get(emotion)
            r13_speaker("daram",R13_FULLBODY_TO_LEGACY[emotion],emotion)
            renpy.say(R13_CHARS.get("daram"),"눈 깜빡임 확인 문장입니다.",interact=False)
            shots=[]
            if spec:
                probe=R13Blink(spec["half"],"daram",emotion,spec)
                start=0.7+probe.gap(0)
                renpy.pause(start+0.09,hard=True)       # 감은 눈(반쯤 50ms 뒤 90ms)
                renpy.screenshot(os.path.join(out,"blink_%s_closed.png"%emotion));shots.append("closed")
                renpy.pause(0.6,hard=True)
            else:
                renpy.pause(1.0,hard=True)
            renpy.screenshot(os.path.join(out,"blink_%s_open.png"%emotion));shots.append("open")
            report["blink"][emotion]=dict(spec=bool(spec),shots=shots)
            renpy.hide("r13_visitor")
        # 0.18.33: Daram's body reacts when her expression changes (neutral -> each emotion).
        report["react"]={}
        store.place="여관 접수대"
        for emotion in ("surprise","joy","angry","anxious","flustered","thinking"):
            r13_speaker("daram","neutral","neutral")
            renpy.say(R13_CHARS.get("daram"),"반응 확인 문장입니다.",interact=False)
            renpy.pause(0.5,hard=True)
            r13_speaker("daram",R13_FULLBODY_TO_LEGACY.get(emotion,"thinking"),emotion)
            renpy.say(R13_CHARS.get("daram"),"반응 확인 문장입니다.",interact=False)
            shots=[]
            last=0.0
            for t in (0.04,0.10,0.16,0.22,0.30,0.40,0.70):
                renpy.pause(t-last,hard=True);last=t
                name="react_%s_%03d.png"%(emotion,int(t*1000))
                renpy.screenshot(os.path.join(out,name));shots.append(name)
            report["react"][emotion]=shots
            renpy.hide("r13_visitor")
            store.r13_motion_person=None
        # 0.18.37: indoor lamps, inn window snow, cinematic effects, other people's reactions and blinks.
        for location in ("school","workshop","clinic","store","inn"):
            renpy.scene()
            renpy.show("r13_qa_fx_bg",what=r13_world_background(location,"evening"))
            for i in range(2):
                renpy.pause(0.37,hard=True)
                renpy.screenshot(os.path.join(out,"lamp_%s_%d.png"%(location,i)))
        for key in ("mountain","E3","proof"):
            renpy.scene()
            renpy.show("r13_qa_fx_bg",what=r13_cinematic_art(key))
            for i in range(2):
                renpy.pause(0.5,hard=True)
                renpy.screenshot(os.path.join(out,"cine_%s_%d.png"%(key,i)))
        renpy.scene()
        renpy.show("r13_qa_fx_bg",what=r13_world_background("inn","evening"))
        report["react_more"]={}
        store.place="여관 접수대"   # setup leaves the carriage, where only Daram is drawn
        for person in ("buri","nabi","bami","mom","karo"):
            r13_speaker(person,"neutral","neutral")
            renpy.say(R13_CHARS.get(person),"반응 확인 문장입니다.",interact=False)
            renpy.pause(0.5,hard=True)
            r13_speaker(person,"expressive","surprise")
            renpy.say(R13_CHARS.get(person),"반응 확인 문장입니다.",interact=False)
            renpy.pause(0.16,hard=True)
            renpy.screenshot(os.path.join(out,"react2_%s_jump.png"%person))
            spec=R13_DOT_FX["blink"]["people"].get(person,{}).get("surprise")
            if spec:
                r13_speaker(person,"neutral","neutral")
                renpy.say(R13_CHARS.get(person),"반응 확인 문장입니다.",interact=False)
                spec=R13_DOT_FX["blink"]["people"][person]["neutral"]
                probe=R13Blink(spec["half"],person,"neutral",spec)
                renpy.pause(0.7+probe.gap(0)+0.09,hard=True)
                renpy.screenshot(os.path.join(out,"blink2_%s_closed.png"%person))
            report["react_more"][person]=bool(spec)
            renpy.hide("r13_visitor")
            store.r13_motion_person=None
        open(os.path.join(out,"report.json"),"w").write(qa_json.dumps(report,ensure_ascii=False,indent=0))
        store.r13_qa_fx_done=True

label r13_qa_dot_fx:
    call r13_qa_setup(5,["E01"])
    $ r13_qa_fx_capture()
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(done=r13_qa_fx_done)))
    return


label r13_qa_granny_ask:
    call r13_granny_letter_ask
    jump r13_roam


# 0.18.43: a short reel of Daram's 1:1 reactions for review (screen recording; not in the default set).
default r13_qa_reel_done = False
label r13_qa_reel:
    call r13_qa_setup(5,["E01"])
    $ place="여관 접수대"
    $ preferences.text_cps=0
    hide screen r13_hud
    scene expression r13_world_background("inn","evening")
    python:
        reel=[("neutral","neutral","(기본) 눈만 깜빡여요.",2.6),("expressive","surprise","(놀람) 움찔했다가 확!",2.4),
              ("neutral","neutral","(기본)",1.6),("expressive","joy","(기쁨) 통통 두 번!",2.2),
              ("neutral","neutral","(기본)",1.6),("distressed","angry","(화남) 움찔, 그리고 부르르.",2.2),
              ("neutral","neutral","(기본)",1.6),("distressed","anxious","(불안) 움츠렸다가 천천히.",2.6),
              ("neutral","neutral","(기본)",1.6),("distressed","flustered","(당황) 좌우로 허둥지둥.",2.2),
              ("neutral","neutral","(기본)",1.6),("thinking","thinking","(생각) 기울여서 잠깐.",2.8)]
        renpy.pause(1.0,hard=True)
        for legacy,pose,line,dur in reel:
            r13_speaker("daram",legacy,pose)
            renpy.say(R13_CHARS.get("daram"),line,interact=False)
            renpy.pause(dur,hard=True)
        store.r13_qa_reel_done=True
    return

label r13_qa_topic_review:
    call r13_topic_review("karo_road")
    jump r13_roam

label r13_qa_inspect_desk:
    call r13_inspect_desk
    jump r13_roam

label r13_qa_talk_menu:
    $ r13_target=r13_qa_person
    $ r13_note_encounter(r13_qa_person)
    jump r13_talk_menu

# 0.18.59 wide maps: click log, hit maps and capacity checks.
init 999 python:
    R13_QA_WIDE_LOG = []
    def r13_qa_wide_write():
        import json as qa_json
        open(renpy.config.basedir+"/qa_result.txt","w").write(qa_json.dumps(R13_QA_WIDE_LOG,ensure_ascii=False))
    def r13_qa_wide_log(tag,expect=None):
        choice=getattr(store,"r13_choice",None)
        actors=[dict(person=a["person"],pose=a["pose"],feet=a["y"]+a["height"],x=a["x"],w=a["width"],h=a["height"],slot=list(a["slot"]) if a.get("slot") else None) for a in r13_stage_people(False)]
        row=dict(tag=tag,expect=expect,choice=list(choice) if isinstance(choice,tuple) else choice,location=store.room13["location"],
            day=store.room13["day"],period=store.room13["period"],daylight=r13_daylight(),width=r13_world_width(),camera=r13_world_offset(),
            background=r13_world_file(store.room13["location"],r13_daylight()) if r13_layout() else None,actors=actors,
            rects={k:list(v["rect"]) for k,v in ROOM13["objects"].get(store.room13["location"],{}).items()})
        R13_QA_WIDE_LOG.append(row)
        r13_qa_wide_write()
    def r13_qa_wide_reset_choice():
        store.r13_choice=None
    def r13_qa_hit(x,y):
        """What a click at screen (x,y) presses: the Return value of the topmost focusable."""
        f=renpy.display.render.focus_at_point(x,y)
        if f is None:return None
        actions=getattr(f.widget,"action",None)
        for a in (actions if isinstance(actions,list) else [actions]):
            if a.__class__.__name__=="Return":
                v=a.value
                return list(v) if isinstance(v,tuple) else v
            if a.__class__.__name__ in ("Show","ShowMenu"):return ["show",getattr(a,"screen","?")]
        return ["other",type(f.widget).__name__]
    R13_QA_PICK={}
    def r13_qa_hitmap(tag):
        """Sample every visible object rect and every actor on a 1280x720 viewport
        (screen = world - camera) through Ren'Py's own focus lookup."""
        location=store.room13["location"];camera=r13_world_offset()
        objects={};R13_QA_PICK.clear()
        for key,spec in ROOM13["objects"].get(location,{}).items():
            if not r13_object_visible(spec):continue
            x,y,w,h=spec["rect"]
            counts={};best=None
            for i in range(16):
                for j in range(12):
                    wx=x+w*(i+.5)/16.0;wy=y+h*(j+.5)/12.0;sx=int(wx-camera);sy=int(wy)
                    if not (0<=sx<1280 and 0<=sy<720):continue
                    hit=r13_qa_hit(sx,sy)
                    label="self" if hit==["object",key] else (hit[0]+":"+str(hit[1])) if isinstance(hit,list) else str(hit)
                    counts[label]=counts.get(label,0)+1
                    if label=="self":
                        d=(i-7.5)**2+(j-5.5)**2
                        if best is None or d<best[0]:best=(d,sx,sy)
            visible=sum(counts.values())
            objects[key]=dict(rect=[x,y,w,h],visible=visible,hits=counts.get("self",0),other={k:v for k,v in counts.items() if k!="self"},
                pick=[best[1],best[2]] if best else None)
            if best:R13_QA_PICK[key]=(best[1],best[2])
        actors=[]
        for a in r13_stage_people(False):
            x,y,w,h=a["rect"];counts={}
            for i in range(10):
                for j in range(14):
                    sx=int(x+w*(i+.5)/10.0-camera);sy=int(y+h*(j+.5)/14.0)
                    if not (0<=sx<1280 and 0<=sy<720):continue
                    hit=r13_qa_hit(sx,sy)
                    if hit==["person",a["person"]]:counts["self"]=counts.get("self",0)+1
            face=r13_actor_face(a,0)
            head=r13_acting_head(a["person"],a["pose"])
            nw,nh=r13_actor_geometry(a["person"],a["pose"])
            fx=int(face[0]+face[2]/2-camera);fy=int(face[1]+face[3]/2)
            actors.append(dict(person=a["person"],pose=a["pose"],rect=list(a["rect"]),feet=a["y"]+a["height"],slot=list(a["slot"]) if a.get("slot") else None,
                head_px=round(a["height"]*head[3]/float(nh),1) if head else None,display_h=a["height"],native_h=nh,
                person_hits=counts.get("self",0),face_hit=r13_qa_hit(fx,fy) if 0<=fx<1280 else "offscreen"))
        R13_QA_WIDE_LOG.append(dict(tag=tag,kind="hitmap",location=location,day=store.room13["day"],period=store.room13["period"],
            daylight=r13_daylight(),width=r13_world_width(),camera=camera,background=r13_world_file(store.room13["location"],r13_daylight()) if r13_layout() else None,
            objects=objects,actors=actors,travel=[list(c) for c in r13_local_connections()]))
        r13_qa_wide_write()
    def r13_qa_pick(key):
        return R13_QA_PICK.get(key,(640,40))
    def r13_qa_wide_capacity(locations=("post","kitchen","dining","passage","inn","hall","room13","river","forest","market")):
        """Residents at each wide location for every day/period and the states that
        move people (case, victim, granny, shelter, protection, detention)."""
        import itertools
        saved=store.room13
        rows=[]
        flag_sets=[(),("shelter_ready",),("bami_protected","nubi_protected"),("tok_detained",),("mom_reunited","patient_transport","shelter_ready")]
        for day in range(1,15):
            for period in range(4):
                for case,victim,granny,flags in itertools.product(("pending","occurred"),("alive","dead"),("free","detained"),flag_sets):
                    n=winter_copy.deepcopy(saved)
                    n.update(day=day,period=period,case_state=case,victim_state=victim,granny_state=granny)
                    n["flags"]=list(set(n.get("flags",[]))|set(flags))
                    for location in locations:
                        n["location"]=location;store.room13=n
                        layout=r13_layout(location)
                        people=r13_people()
                        # Pinned people (authored positions, ceiling hooks) do not take a slot;
                        # in the dining room everyone stands on the floor list directly.
                        if location=="dining":need=len(people);cap=len(layout.get("floors",[]))
                        else:
                            need=len([p for p in people if p not in layout.get("pinned",[]) and p not in layout.get("hooks",{})])
                            cap=len(layout.get("slots",[]))
                        rows.append(dict(day=day,period=period,case=case,victim=victim,granny=granny,flags=list(flags),location=location,
                            wide=bool(layout),slots=cap if layout else None,need=need,people=people))
        store.room13=saved
        over=[r for r in rows if r["wide"] and r["need"]>r["slots"]]
        peak={}
        for r in rows:
            k="%s/%d"%(r["location"],min(r["period"],2))
            peak[k]=max(peak.get(k,0),len(r["people"]))
        groups={}
        for r in over:
            k="%s/%d %s"%(r["location"],min(r["period"],2),",".join(r["people"]))
            g=groups.setdefault(k,dict(slots=r["slots"],count=0,days=set(),states=set()))
            g["count"]+=1;g["days"].add(r["day"]);g["states"].add("%s/%s/%s/%s"%(r["case"],r["victim"],r["granny"],"+".join(r["flags"])))
        groups={k:dict(slots=g["slots"],count=g["count"],days=sorted(g["days"]),states=sorted(g["states"])[:6]) for k,g in groups.items()}
        R13_QA_WIDE_LOG.append(dict(tag="capacity",kind="capacity",rows=len(rows),over_groups=groups,over_count=len(over),peak=peak))
        r13_qa_wide_write()
        return not over

init 999 python:
    def r13_qa_note(text):
        import os
        out=os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa");os.makedirs(out,exist_ok=True)
        with open(os.path.join(out,"notes.txt"),"a") as f:f.write(text+"\n")

    def r13_qa_crowd_dump():
        # 0.18.53: who stands where, per day and time slot, with the present flag state.
        import os,json
        saved=winter_copy.deepcopy(store.room13);rows=[]
        for day in range(1,15):
            for period in range(3):
                for loc in sorted(R13_PLACES):
                    n=winter_copy.deepcopy(saved);n.update(day=day,period=period,location=loc);store.room13=n
                    try:people=list(r13_people())
                    except Exception as e:people=["ERR:"+str(e)]
                    rows.append(dict(day=day,period=period,location=loc,people=people))
        store.room13=saved
        out=os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa");os.makedirs(out,exist_ok=True)
        json.dump(rows,open(os.path.join(out,"crowd.json"),"w"),ensure_ascii=False,indent=0)

# Motion audit reel (screen-recorded for review; not in the default set).
default r13_qa_audit_done = False
label r13_qa_audit:
    call r13_qa_setup(5,["E01"])
    $ place="여관 접수대"
    $ preferences.text_cps=0
    hide screen r13_hud
    python:
        for location,period in (("inn","evening"),("inn","afternoon"),("square","evening"),("workshop","evening"),("clinic","evening"),("store","evening"),("school","evening")):
            renpy.scene()
            renpy.show("r13_qa_fx_bg",what=r13_world_background(location,period))
            renpy.with_statement(r13_bleed(.8))
            renpy.pause(3.2,hard=True)
        for key in ("E3","proof"):
            renpy.scene();renpy.show("r13_qa_fx_bg",what=r13_cinematic_art(key));renpy.with_statement(r13_bleed(.6))
            renpy.pause(2.6,hard=True)
        renpy.scene();renpy.show("r13_qa_fx_bg",what=r13_world_background("inn","evening"))
        for legacy,pose in (("neutral","neutral"),("expressive","surprise"),("neutral","neutral"),("distressed","angry")):
            r13_speaker("daram",legacy,pose)
            renpy.say(R13_CHARS.get("daram"),"움직임 점검 문장입니다.",interact=False)
            renpy.pause(1.8,hard=True)
        renpy.hide("r13_visitor");store.r13_motion_person=None
        renpy.show_screen("r13_evidence_found",keys=["E01"],conversation=False)
        renpy.pause(2.6,hard=True)
        r13_fx_cue("present")
        renpy.pause(1.4,hard=True)
        store.r13_qa_audit_done=True
    return

init 999 python:
    def r13_qa_overlap_dump():
        # 0.18.56: inspection targets covered by people, and targets crowding each other.
        import os,json
        saved=winter_copy.deepcopy(store.room13);rows=[]
        def inter(a,b):
            w=min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]);h=min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1])
            return max(0,w)*max(0,h)
        for day in (2,3,5,9):
            for period in range(3):
                for loc in sorted(ROOM13["objects"]):
                    if loc not in R13_PLACES:continue
                    n=winter_copy.deepcopy(saved);n.update(day=day,period=period,location=loc);store.room13=n
                    R13_STAGE_CACHE.clear()
                    try:actors=r13_stage_people()
                    except Exception as e:rows.append(dict(loc=loc,err=str(e)));continue
                    objs=[(k,tuple(spec["rect"])) for k,spec in ROOM13["objects"][loc].items() if r13_object_visible(spec)]
                    for k,r in objs:
                        area=float(r[2]*r[3]) or 1
                        for a in actors:
                            face=r13_actor_face_target(a) or tuple(a["rect"])
                            fb=inter(r,tuple(a["rect"]))/area;ff=inter(r,face)/area
                            if fb>.3 or ff>.05:rows.append(dict(day=day,period=period,loc=loc,obj=k,name=r13_object_name(k),rect=r,person=a["person"],body=round(fb,2),face=round(ff,2)))
                    for i,(k,r) in enumerate(objs):
                        for k2,r2 in objs[i+1:]:
                            o=inter(r,r2)/float(min(r[2]*r[3],r2[2]*r2[3]) or 1)
                            if o>.25:rows.append(dict(day=day,period=period,loc=loc,obj=k,other=k2,overlap=round(o,2)))
        store.room13=saved;R13_STAGE_CACHE.clear()
        out=os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa");os.makedirs(out,exist_ok=True)
        json.dump(rows,open(os.path.join(out,"overlap.json"),"w"),ensure_ascii=False,indent=0)

init 999 python:
    def r13_qa_depth_dump():
        # 0.18.56: feet depth vs drawn height of every staged actor.
        import os,json
        saved=winter_copy.deepcopy(store.room13);rows=[]
        for day in (2,3,5,9):
            for period in range(3):
                for loc in sorted(R13_PLACES):
                    n=winter_copy.deepcopy(saved);n.update(day=day,period=period,location=loc);store.room13=n
                    R13_STAGE_CACHE.clear()
                    try:actors=r13_stage_people()
                    except Exception as e:continue
                    for a in actors:
                        spec=r13_acting_spec(a["person"],a["pose"]) or {}
                        pw,ph=r13_actor_geometry(a["person"],a["pose"])
                        foot=spec.get("foot",[pw/2.0,ph]);sc=float(a["height"])/ph
                        rows.append(dict(loc=loc,day=day,period=period,person=a["person"],pose=a["pose"],contact=a["contact"],
                            feet=round(a["y"]+foot[1]*sc),h=a["height"],std=round(r13_qa_standing_equiv(a,loc))))
        store.room13=saved;R13_STAGE_CACHE.clear()
        out=os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa");os.makedirs(out,exist_ok=True)
        json.dump(rows,open(os.path.join(out,"depth.json"),"w"),ensure_ascii=False)

    def r13_qa_standing_equiv(a,loc):
        layout=getattr(store,"R13_WORLD_LAYOUTS",{}).get(loc,{})
        probe=r13_world_display_height(a["person"],a["pose"],1000.0,dict(layout,standing_height_reference=layout.get("standing_height_reference",1000)))
        return a["height"]*1000.0/probe if probe else a["height"]

init 999 python:
    def r13_qa_find_slot(person,place):
        # First week-1 day/period when person stands at place (new places, 0.18.61).
        saved=winter_copy.deepcopy(store.room13)
        found=None
        for day in range(2,8):
            for period in (0,1):
                n=winter_copy.deepcopy(saved);n.update(day=day,period=period,life_poc=True)
                n["flags"]=list(set(n["flags"])|{"lodging","entry_corrected","livelihood_open"})
                store.room13=n
                if r13_where(person)==place:
                    found=dict(day=day,period=period,location=place,life_poc=True);break
            if found:break
        store.room13=saved
        return found
