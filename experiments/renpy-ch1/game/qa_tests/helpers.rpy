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
    $ room13.update(location="store",day=5,period=0,life_poc=True,case_state="occurred")
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
    # 0.18.23 typography: narration, Dad's thought (no parentheses in source), speech with an item.
    call r13_lines([(None,"책상 아래에 접힌 종이가 끼어 있다."),("dad","원본과 옮겨 쓴 명부가 다르다. 어디서 빠진 거지?",{"thought":True}),("dad","「예약 원본」에는 다람이 이름도 적혀 있습니다.")],"qa:typography")
    jump r13_roam
