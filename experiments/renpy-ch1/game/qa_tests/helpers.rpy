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
    $ room13["flags"]=list(dict.fromkeys(room13["flags"]+["lodging","entry_corrected","livelihood_open"]+[f for f in flags if f not in ("+brief","+w1c")]+([] if "+brief" in flags else ["evening_brief:%d"%d for d in range(1,14)])+([] if "+w1c" in flags else ["ev_g_done","ev_l_done","ev_i_done","ev_s_done","ev_t_done"])))
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
