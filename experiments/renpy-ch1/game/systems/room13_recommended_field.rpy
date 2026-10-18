# Scene-level navigation. Only recommended-state subjects are staged.
default r13_rec_admin_harness = False

init 905 python:
    r13_rec_card_art = {}
    r13_rec_card_people = {"piko_nabi_defense":"nabi"}
    def r13_rec_location_info(location, state=None):
        state = state or store.r13_recommended or {}
        callback = r13_rec_location_overrides.get(state.get("episode",1))
        override = callback(state,location) if callback else None
        if override: return override
        return r13_rec_backgrounds.get(location, R13_PLACES.get(location, (location,"front")))
    def r13_rec_local_targets(state):
        groups = {}
        for key, title in r13_rec_available(state):
            spec = r13_rec_actions[key]
            if spec["place"] != state.get("location", "inn"):
                continue
            person = spec.get("target_person")
            target = ("person", person) if person else ("object", spec.get("target_object") or title)
            groups.setdefault(target, []).append((key,title))
        return [(kind, subject, rows) for (kind,subject), rows in groups.items()]
    def r13_rec_field_actor(person, cx):
        if person not in CAST: return None
        w,h = r13_actor_geometry(person,"neutral")
        height = 230
        width = max(1,int(round(w*float(height)/max(h,1))))
        x,y = cx-width//2,590-height
        return dict(person=person,pose="neutral",x=x,y=y,width=width,height=height,rect=(x,y,width,height),depth=590,occlusion=None,contact=None,slot=None)
    def r13_rec_art_spec(key):
        spec=r13_rec_card_art.get(key)
        if key=="piko_portrait" and not spec:
            art=r13_evidence_art("P01")
            if art is not None:return dict(icon=Transform(art,xysize=(64,64),fit="contain",nearest=True),detail=Transform(art,xysize=(240,240),fit="contain",nearest=True))
        if not isinstance(spec,dict):return {"icon":spec,"detail":spec} if spec else {}
        if key=="e5_card_pots" and spec.get("variants"):
            state=getattr(store,"r13_recommended",None) or {}
            contaminated=state.get("episodes",{}).get("5",{}).get("event")=="contaminated"
            return spec["variants"]["swapped" if contaminated and not state.get("e5_poison_blocked") else "original"]
        return spec
    def r13_rec_identity_person(state, ident):
        for key in r13_rec_identity_facts(state,ident):
            if r13_rec_card_people.get(key): return r13_rec_card_people[key]
        return None
    def r13_rec_identity_art(state, ident):
        for key in r13_rec_identity_facts(state,ident):
            if r13_rec_art_spec(key).get("icon"): return r13_rec_art_spec(key)["icon"]
        return None
    def r13_rec_target_art(rows):
        for key,title in rows:
            for card in r13_rec_actions[key].get("give",()):
                if r13_rec_art_spec(card).get("icon"):return r13_rec_art_spec(card)["icon"]
        return None
    def r13_rec_map_places(state):
        locations = list(dict.fromkeys([state.get("location","inn")]+[r13_rec_actions[key]["place"] for key,title in r13_rec_available(state)]))
        return [(loc,r13_rec_location_info(loc)[0]) for loc in locations]

screen r13_recommended_field():
    modal True
    default target_page = 0
    $ targets = r13_rec_local_targets(r13_recommended)
    frame:
        xpos 24 ypos 20 background R13PaperFrame() padding (14,8)
        text ("%d일 · %s" % (r13_recommended["day"],r13_rec_location_info(r13_recommended["location"])[0])) size 24 color "#493b30"
    $ page_start = min(target_page*4,max(0,((len(targets)-1)//4)*4))
    for slot, (kind, subject, rows) in enumerate(targets[page_start:page_start+4]):
        $ index = page_start+slot
        $ cx = 190+slot*290
        if kind == "person":
            $ actor = r13_rec_field_actor(subject,cx)
            if actor:
                add r13_staged_visible_art(actor) xpos actor["x"] ypos actor["y"]
                button:
                    area actor["rect"] padding (0,0) background None hover_background None
                    focus_mask r13_actor_hit_mask(actor)
                    action Return("target:"+str(index))
                    tooltip R13_NAMES.get(subject,subject)
            textbutton R13_NAMES.get(subject,subject):
                xpos cx-110 ypos 600 xsize 230 text_size 21
                background R13ActionPanel() hover_background R13ActionPanel(True)
                action Return("target:"+str(index))
        else:
            frame:
                xpos cx-105 ypos 400 xsize 230 ysize 170 background R13PaperFrame() padding (8,8)
                button:
                    xfill True yfill True background None hover_background R13ActionPanel(True)
                    action Return("target:"+str(index))
                    vbox:
                        xalign .5 yalign .5 spacing 8
                        $ target_art = r13_rec_target_art(rows)
                        if target_art:
                            add target_art xalign .5
                        else:
                            text "조사" size 20 color "#493b30" xalign .5
                        text subject size 23 color "#493b30" text_align .5 xalign .5
    if len(targets)>4:
        hbox:
            xpos 760 ypos 80 spacing 16
            textbutton "앞쪽 보기" sensitive page_start>0 action SetScreenVariable("target_page",max(0,target_page-1))
            textbutton "다른 쪽 보기" sensitive page_start+4<len(targets) action SetScreenVariable("target_page",target_page+1)
    if not targets:
        frame:
            xpos 280 ypos 110 xsize 650 background R13InkPanel()
            text "지금 여기서 새로 확인할 일은 없다. 지도에서 다음 장소를 고르자." size 22
    hbox:
        xpos 24 ypos 666 spacing 8
        textbutton "지도 · 이동" action Return("map") text_size 20
        textbutton "수첩 · 카드" action Return("notebook") text_size 20
        if r13_recommended.get("period",0) < 2:
            textbutton "저녁까지 기다린다" action Return("evening") text_size 20
        if r13_recommended["day"] < r13_rec_episodes[r13_recommended["episode"]]["end_day"]:
            textbutton "오늘을 마친다" action Return("advance") text_size 20
        if r13_recommended["day"] == r13_rec_episodes[r13_recommended["episode"]]["end_day"] and not r13_rec_episode_done.get(r13_recommended["episode"],lambda s:False)(r13_recommended):
            textbutton "약속한 회의에 간다" action Return("hearing") text_size 20
        if r13_rec_next_available(r13_recommended):
            textbutton "다음 사건" action Return("next_episode") text_size 20
        textbutton "저장" action ShowMenu("save") text_size 20
        textbutton "제목" action MainMenu(confirm=True) text_size 20
    if r13_recommended.get("qa_fixture"):
        text "미검증 QA 전용 · 최종 단계 시험 허용" xpos 30 ypos 80 size 20 color "#ffb76b"
    if persistent.room13_admin:
        textbutton "상태검증 허브" xpos 1050 ypos 20 text_size 18 action [SetVariable("r13_rec_admin_harness",True),Return("refresh")]
    $ tip = GetTooltip()
    if tip:
        text tip xpos 30 ypos 100 size 24 outlines [(2,"#000",0,0)]

screen r13_recommended_map():
    modal True
    add Solid("#172421ed")
    frame:
        xalign .5 yalign .5 xsize 1000 ysize 610
        vbox:
            spacing 18
            text "마을 · 지금 찾아갈 곳" size 30
            text "이미 들은 행적과 현재 가능한 방문만 표시합니다." size 21
            viewport:
                ysize 430 mousewheel True draggable True scrollbars "vertical"
                vbox:
                    spacing 8
                    for loc, title in r13_rec_map_places(r13_recommended):
                        textbutton title action Return(loc) xsize 900 text_size 24
            textbutton "돌아가기" action Return(None)

screen r13_recommended_subject(kind, subject, rows):
    modal True
    if kind == "person":
        use r13_question_list(subject,"neutral",R13_NAMES.get(subject,subject),[(title,Return(key),False) for key,title in rows],True,return_action=Return(None),caption="직접 확인한 일에서 묻기")
    else:
        frame:
            xalign .5 yalign .5 xsize 980
            vbox:
                spacing 14
                text subject size 28
                for key,title in rows:
                    textbutton title action Return(key) xsize 900 text_size 24
                textbutton "돌아가기" action Return(None)

screen r13_recommended_notebook():
    use r13_recommended_catalog()

label r13_recommended_pick:
    if r13_rec_admin_harness:
        call screen r13_recommended_actions
        return _return
    $ room13["day"] = r13_recommended["day"]
    $ room13["period"] = r13_recommended.get("period",0)
    $ room13["location"] = "post" if r13_recommended["location"] == "library" else r13_recommended["location"]
    $ r13_rec_info = r13_rec_location_info(r13_recommended["location"])
    call r13_scene(r13_rec_info[1],r13_rec_info[0],"calm")
    call screen r13_recommended_field
    $ r13_rec_pick = _return
    if r13_rec_pick == "refresh":
        jump r13_recommended_pick
    if r13_rec_pick == "map":
        call screen r13_recommended_map
        if _return is not None:
            $ r13_recommended = copy.deepcopy(r13_recommended)
            $ r13_recommended["location"] = _return
        jump r13_recommended_pick
    if r13_rec_pick == "notebook":
        call screen r13_recommended_notebook
        if _return is None:
            jump r13_recommended_pick
        return _return
    if r13_rec_pick.startswith("target:"):
        $ r13_rec_target = r13_rec_local_targets(r13_recommended)[int(r13_rec_pick.split(":")[1])]
        call screen r13_recommended_subject(r13_rec_target[0],r13_rec_target[1],r13_rec_target[2])
        if _return is None:
            jump r13_recommended_pick
        return _return
    return r13_rec_pick


screen r13_recommended_card_detail(key):
    modal True
    add Solid("#172421ed")
    frame:
        xalign .5 yalign .5 xsize 1100 ysize 610
        vbox:
            spacing 24
            text r13_rec_cards[key][0] size 30
            hbox:
                spacing 28
                if r13_rec_art_spec(key).get("detail"):
                    add r13_rec_art_spec(key)["detail"]
                elif r13_rec_card_people.get(key):
                    add r13_close_art(r13_rec_card_people[key],"neutral",240)
                vbox:
                    xsize (680 if r13_rec_art_spec(key).get("detail") or r13_rec_card_people.get(key) else 1000) spacing 18
                    text ("확인한 날: %s일" % r13_recommended.get("observed",{}).get(key,"?")) size 21
                    text r13_rec_cards[key][1] size 24 line_spacing 8
            if r13_rec_art_spec(key).get("examination"):
                textbutton "같은 물건 크게 보기" action Show("r13_rec_evidence_enlarged",key=key)
            if key == "child" and "piko_cloth_intact_at_loan" in r13_recommended["done"]:
                textbutton "빌려줄 때의 온전한 천 보기" action Show("r13_rec_piko_intact_cloth",as_overlay=True)
            textbutton "수첩으로 돌아간다" action Return(True)

screen r13_recommended_catalog(question=None):
    modal True
    default folder = (0 if r13_recommended['day']==1 else r13_recommended['episode'])
    default category = "material"
    default selected_identity = None
    add Solid("#172421f5")
    frame:
        xpos 30 ypos 25 xsize 1220 ysize 660
        vbox:
            spacing 10
            text (question or "다람탐정 수첩") size 26
            hbox:
                spacing 10
                for section in range(7):
                    textbutton ("메인" if section==0 else "사건 %d" % section) selected folder==section action [SetScreenVariable("folder",section),SetScreenVariable("selected_identity",None)] text_size 20
            if folder==0:
                text r13_rec_main_objective(r13_recommended) size 19 xsize 1150
            hbox:
                spacing 20
                textbutton "자료 · 현장" selected category=="material" action [SetScreenVariable("category","material"),SetScreenVariable("selected_identity",None)]
                textbutton "인물" selected category=="person" action [SetScreenVariable("category","person"),SetScreenVariable("selected_identity",None)]
            hbox:
                spacing 20
                viewport:
                    xsize 390 ysize (370 if folder==0 else 430) mousewheel True draggable True scrollbars "vertical"
                    vbox:
                        spacing 8
                        for ident,title,held,kind in r13_rec_catalog_entries(r13_recommended,folder,category):
                            button:
                                xsize 355 action SetScreenVariable("selected_identity",ident)
                                vbox:
                                    hbox:
                                        spacing 10
                                        $ preview_art=r13_rec_identity_art(r13_recommended,ident)
                                        if preview_art:
                                            add preview_art
                                        text title size 23
                                    text ("확인 사실 %d개 · %s" % (len(held),"인물" if kind=="person" else "현장" if kind=="scene" else "물건")) size 17
                viewport:
                    xsize 750 ysize (370 if folder==0 else 430) mousewheel True draggable True scrollbars "vertical"
                    vbox:
                        spacing 12
                        if selected_identity:
                            hbox:
                                spacing 18
                                $ profile_person=r13_rec_identity_person(r13_recommended,selected_identity)
                                if profile_person:
                                    add r13_close_art(profile_person,"neutral",110)
                                text (r13_rec_identity_groups[selected_identity][1]+" · 지금까지 직접 확인한 사실") size 24 yalign .5
                            text "같은 인물·물건의 다른 회차 관찰도 함께 연결됩니다." size 18
                            for key in r13_rec_identity_facts(r13_recommended,selected_identity):
                                button:
                                    xsize 710 action Return(key if question else "card:"+key)
                                    vbox:
                                        text ("%s · %s일 확인" % ("메인" if r13_rec_card_episode(key)==0 else "사건 %d" % r13_rec_card_episode(key),r13_recommended.get("observed",{}).get(key,"?"))) size 17
                                        text r13_rec_cards[key][0] size 22
                        else:
                            text "폴더에서 자료나 인물을 고르면, 확인한 사실을 날짜별로 볼 수 있습니다." size 23
            textbutton ("조사로 돌아간다" if question else "현장으로") action Return(None)


screen r13_rec_evidence_enlarged(key):
    modal True
    zorder 150
    add Solid("#172421ed")
    frame:
        align (.5,.5) xsize 930 padding (28,24)
        vbox:
            spacing 20
            text r13_rec_cards[key][0] size 28
            add r13_rec_art_spec(key)["examination"] xalign .5
            text "같은 자료의 확대 관찰 · 추가 수집품이 아님" size 18
            textbutton "수첩으로 돌아간다" action Hide("r13_rec_evidence_enlarged")
    key "game_menu" action Hide("r13_rec_evidence_enlarged")
