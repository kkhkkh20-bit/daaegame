screen r13_hud():
    style_prefix "r13"
    zorder 20
    if place == "마차 안":
        textbutton ("읽은 대사만 ●" if r13_fast_read else "읽은 대사만 ›"):
            style "r13_action_button"
            xpos 988 ypos 24 xsize 184 ysize 54
            text_size r13_read_size(20,24)
            action Function(r13_toggle_read_skip)
            tooltip "이미 읽은 대사만 넘기고, 새 대사와 선택지에서 멈춥니다"
    if not any(renpy.get_screen(k) for k in ("say","r13_topics","choice","r13_entry_topics","r13_entry_karo_topics")):
        frame:
            xpos 24 ypos 20 xsize 410 ysize 82 padding (16,10)
            background R13ActionPanel()
            vbox:
                spacing 5
                text r13_clock() size r13_read_size(19,22) color "#c6b88e"
                text place size r13_read_size(20,24) color "#fff2cf" xsize 378

init 80:
    style r13_toolbar_button is r13_action_button:
        xsize 128
        ysize 44
        padding (10,6)
        background Solid("#102b35ed")
        hover_background Solid("#29434ed9")
        insensitive_background Solid("#1c303bea")
    style r13_toolbar_button_text is r13_action_button_text:
        color "#edf0e5"
        hover_color "#ffffff"
        insensitive_color "#91a6ae"
        outlines [(1,"#14232a99",0,1)]
        xalign .5
        yalign .5

screen r13_toolbar(investigate_action=None,present_action=None,person=None,mode="line",ready=True):
    style_prefix "r13"
    if mode!="field":
        frame:
            area (640,676,640,40) padding (8,0) background Solid("#edf1e9")
            hbox:
                spacing 8
                if investigate_action is not None:
                    textbutton "돌아가기" style "r13_footer_button" action investigate_action sensitive ready
                if present_action is not None:
                    textbutton "보여주기" style "r13_footer_button" action present_action sensitive ready
                textbutton "기록" style "r13_footer_button" action Show("r13_records") sensitive ready
                textbutton "백로그" style "r13_footer_button" action Show("r13_backlog") sensitive ready
                textbutton ("자동 ●" if _preferences.afm_enable else "자동"):
                    style "r13_footer_button"
                    action Preference("auto-forward","toggle")
                    sensitive ready and mode=="line" and renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
                textbutton "옵션" style "r13_footer_button" action ShowMenu("pause_menu") sensitive ready
    else:
        # Three independent controls leave the rest of the scene visible/clickable.
        hbox:
            xalign .5 ypos 670 spacing 8
            if mode=="field":
                frame:
                    xsize 128 ysize 44 padding (10,6)
                    background Solid("#244239ed")
                    text "조사":
                        size r13_read_size(20,24) color "#e2ebdf"
                        outlines [(1,"#14232a99",0,1)]
                        xalign .5 yalign .5
            else:
                textbutton "조사":
                    style "r13_toolbar_button"
                    text_size r13_read_size(20,24)
                    action (investigate_action or NullAction())
                    sensitive ready and investigate_action is not None
                    tooltip "대화를 마치고 현장을 살핍니다"
            textbutton "보여주기":
                style "r13_toolbar_button"
                text_size r13_read_size(20,24)
                action (present_action or NullAction()) sensitive ready and present_action is not None
                tooltip ((R13_NAMES.get(person,"")+"에게 자료를 보여줍니다") if person else "인물을 눌러 대화를 시작하세요")
            textbutton "기록":
                style "r13_toolbar_button"
                text_size r13_read_size(20,24)
                action Show("r13_records") sensitive ready
        use r13_options_control(ready)

screen r13_options_control(ready=True):
    # Owned by the active modal screen, so options remain clickable in dialogue.
    button:
        id "r13_options_gear"
        area (1190,20,64,64) padding (0,0)
        background Solid("#152e3866") hover_background Solid("#29434ee0")
        insensitive_background Solid("#1c303bea")
        action ShowMenu("pause_menu") sensitive ready
        tooltip "옵션" alt "옵션"
        fixed:
            xsize 64 ysize 64
            # Stepped eight-tooth pixel gear; no extra bitmap or font glyph.
            add Solid("#e0e8dc",xsize=24,ysize=24) xpos 20 ypos 12
            add Solid("#e0e8dc",xsize=8,ysize=36) xpos 28 ypos 6
            add Solid("#e0e8dc",xsize=36,ysize=8) xpos 14 ypos 20
            add Solid("#e0e8dc",xsize=8,ysize=8) xpos 18 ypos 10
            add Solid("#e0e8dc",xsize=8,ysize=8) xpos 38 ypos 10
            add Solid("#e0e8dc",xsize=8,ysize=8) xpos 18 ypos 30
            add Solid("#e0e8dc",xsize=8,ysize=8) xpos 38 ypos 30
            add Solid("#203942",xsize=10,ysize=10) xpos 27 ypos 19
            text "옵션" size 14 color "#e6ece2" xalign .5 ypos 45

screen r13_hub(entry=False):
    style_prefix "r13"
    modal True
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    default world_adjustment=r13_world_adjustment(room13["location"])

    if r13_world_width()>1280 and not entry:
        viewport:
            id "r13_world_viewport"
            area (0,0,1280,720)
            xadjustment world_adjustment
            draggable True mousewheel "horizontal" arrowkeys False
            fixed:
                xsize r13_world_width() ysize 720
                add r13_world_background()
                use r13_world_contents(entry,ready)
        use r13_world_camera_controls(world_adjustment)
    else:
        use r13_world_contents(entry,ready)
    if not entry:
        hbox:
            xpos 1250 xanchor 1.0 ypos 105 spacing 6
            for destination,title in r13_local_connections():
                textbutton (title+" ›"):
                    style "r13_action_button" padding (13,10) ysize 43
                    text_size 18 action Return(("travel",destination)) sensitive ready
    if entry:
        use r13_waiting_window(ready)
    else:
        textbutton "지도 · 이동":
            style "r13_action_button" xpos 970 ypos 23 xsize 180 ysize 62
            text_size 23 action Return(("menu","map")) sensitive ready
    if not entry and r13_bed_available("bed"):
        textbutton "자기":
            style "r13_action_button" area (1010,584,220,56)
            action Return(("sleep","bed"))
    if not entry and r13_has("livelihood_open"):
        textbutton ("일거리 · 상점  %d냥"%r13_wallet(room13)["cash"]):
            style "r13_action_button" area (24,515,290,52) text_size 21
            action Return(("livelihood",None)) sensitive ready
    if not entry and room13.get("life_poc") and room13["day"]<=2:
        $ life_goal=(("접수대의 할머니에게 아내 소식을 묻자" if room13.get("location")=="inn" else "여관에 가서 편지를 보낸 할머니를 만나자") if room13["day"]==1 and not r13_has("lodging") else "2층 13호실에 가서 엄마가 남긴 물건을 살펴보자" if room13["day"]==1 and room13.get("location")!="room13" and not (r13_has("M01") and r13_has("E03")) else "책상에 남은 메모와 이불을 살펴보자" if room13["day"]==1 and not r13_bed_available("bed") else "다람이와 이야기를 나누고 쉬자" if room13["day"]==1 else "입구의 까로에게 돌아갈 마차를 물어보자" if not r13_has("livelihood_open") else "등불을 돌보는 초롱을 찾아 엄마의 메모를 보여 주자" if (r13_has("mother_lamplighter_lead") or r13_has("J01")) else "엄마의 메모를 보여주고 등불을 돌보는 사람을 찾자")
        frame:
            xpos 24 ypos 178 padding (12,8) background Solid("#102725b0")
            text life_goal size 20 color "#eee5d5"
    elif not entry and room13.get("life_poc") and r13_campaign_goal():
        frame:
            xpos 24 ypos 178 padding (12,8) background Solid("#102725b0")
            text r13_campaign_goal() size r13_read_size(20,24) color "#eee5d5"
    use r13_toolbar(mode="field",ready=ready)
    $ hint=GetTooltip()
    if hint:
        frame:
            xpos 24 ypos 580 padding (14,9) background R13ActionPanel()
            text hint size 20 color "#fff2cf"

screen r13_world_contents(entry=False,ready=False):
    style_prefix "r13"
    # Background targets stay behind the visible residents.
    for key,spec in ROOM13["objects"].get(room13["location"],{}).items():
        if r13_object_visible(spec):
            button:
                area tuple(spec["rect"])
                background None hover_background None insensitive_background None padding (0,0)
                action [Function(r13_click_feedback,key),Return(("object",key))] sensitive ready
                tooltip r13_object_name(key)
    use r13_resident_stage(entry,ready)
    for nameplate in r13_actor_nameplates(r13_stage_people(entry)):
        if nameplate["leader"]:
            $ leader=R13NameLeader(nameplate["leader"])
            add leader xpos leader.left ypos leader.top
        textbutton R13_NAMES[nameplate["person"]]:
            area nameplate["rect"]
            padding (12,7) background R13ActionPanel() text_size 18 text_color "#fff2cf"
            action Return(("person",nameplate["person"])) sensitive ready
    for key,point in room13["checks"].items():
        if key.startswith(room13["location"]+":") and r13_visible_check(key,point):
            add TopicTick() xpos point[0]-13 ypos point[1]-13
    $ bundle_point=r13_gate_bundle_check_point()
    if bundle_point:
        add TopicTick() xpos bundle_point[0]-13 ypos bundle_point[1]-13

screen r13_resident_stage(entry=False,ready=False):
    for actor in r13_stage_people(entry):
        add r13_staged_visible_art(actor):
            id ("r13_world_"+actor["person"])
            xpos actor["x"] ypos actor["y"]
            at r13_actor_appear(r13_appearance_duration())
        button:
            area tuple(actor["rect"]) background None hover_background None insensitive_background None padding (0,0)
            focus_mask r13_actor_hit_mask(actor)
            action Return(("person",actor["person"])) sensitive ready
            tooltip (R13_NAMES[actor["person"]]+"에게 말 걸기")


screen r13_question_list(person,pose,title,entries,ready,actor_x=220,list_left=420,list_width=760,animate=True,return_action=None):
    style_prefix "r13"
    # Shade the scenery first. The face remains at its authored brightness.
    add Solid("#00000048")
    $ compact_width=min(list_width,470)
    $ list_left=(1280-compact_width)//2
    $ question_height=r13_reference_list_height(entries,compact_width)
    $ question_top=int((680-question_height)//2)
    if person:
        add r13_close_art(person,pose,840):
            id ("r13_topics_"+person)
            xpos 640 xanchor .5 ypos r13_close_y(person,840,110,pose)
    if not person:
        text title:
            xpos list_left ypos 50 xsize compact_width text_align .5
            size r13_read_size(27,32) color "#f6d18a"
    viewport:
        area (list_left,question_top,compact_width,question_height)
        mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
        vbox:
            spacing 24
            for title,action,was_read in entries:
                button:
                    # Left padding clears the white diagonal drawn by R13ReferenceChoice.
                    xsize compact_width-23 yminimum 42 padding (60,6,16,6)
                    background R13ReferenceChoice(False) hover_background R13ReferenceChoice(True)
                    action action sensitive ready
                    text (("{font=assets/Room13Sans.ttf}✓{/font}  "+title) if was_read else title):
                        xsize compact_width-99 text_align .5 xalign .5
                        size r13_read_size(22,28) font r13_ui_font()
                        color ("#d3e3e7" if was_read else "#ffffff")
            if not entries:
                frame:
                    xsize compact_width-23 padding (16,10) background Solid("#102b2bd8")
                    text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.":
                        xsize compact_width-55 text_align .5 xalign .5 size r13_read_size(22,28) color "#eee5d5"
    if return_action is not None and not person:
        textbutton "돌아가기":
            xpos list_left+compact_width//2 xanchor .5 ypos 544 xsize 150 ysize 44
            padding (12,6) background Solid("#102b2bb0") hover_background Solid("#42615ed0")
            text_size r13_read_size(20,25) text_color "#fff4df" text_xalign .5
            action return_action sensitive ready

screen r13_entry_topics():
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    $ questions=[("신청한 것과 이름 목록이 다른 이유가 뭡니까?",Return(("entry","explain")),r13_has("question_read:entry:explain")),("원본과 다시 맞춰 봐 주시겠습니까?",Return(("entry","wait")),r13_has("question_read:entry:wait"))]
    use r13_question_list("guard","interview_neutral","돌목에게 묻기",questions,ready,return_action=Return(("entry","back")))
    use r13_toolbar(investigate_action=Return(("entry","back")),present_action=Return(("entry","argue")),person="guard",mode="talk",ready=ready)

screen r13_entry_karo_topics():
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    $ questions=[("마차는 괜찮습니까?",Return("road"),r13_has("question_read:entry:karo:road")),("함께 왔다고 말해 주시겠어요?",Return("witness"),r13_has("question_read:entry:karo:witness")),("짐을 잠시 맡아 주시겠습니까?",Return("bags"),r13_has("question_read:entry:karo:bags"))]
    use r13_question_list("karo","interview_neutral","까로에게 묻기",questions,ready,return_action=Return("back"))
    use r13_toolbar(investigate_action=Return("back"),present_action=Return("present"),person="karo",mode="talk",ready=ready)

# Kept as a save-compatible screen name; people open their topics directly.
screen r13_interaction(person):
    use r13_topics(person)

screen r13_material_corner(key):
    zorder 85
    # The card's reveal owns one paper whoosh; prediction/redraw/replace stay silent.
    on "show" action Function(source_fx,"page")
    use r13_evidence_card(key,"보여 준 자료")

# The resident stays on the left; opaque questions never cover the face.
screen r13_topics(person):
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    $ actor_pose=r13_conversation_pose(person)
    $ questions=[(r13_calendar_topic_title(key,spec),Return(key),r13_calendar_topic_seen(key,spec)) for key,spec in r13_topics(person)]
    use r13_question_list(person,actor_pose,R13_NAMES[person]+"에게 묻기",questions,ready,return_action=Return("back"))
    use r13_toolbar(investigate_action=Return("back"),present_action=Return("present"),person=person,mode="talk",ready=ready)

screen r13_confirm(message,yes="진행한다",no="돌아간다"):
    style_prefix "r13"
    modal True
    zorder 65
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    frame:
        xpos 165 ypos 210 xsize 950 padding (32,28)
        vbox:
            spacing 25
            text message size 26 xsize 880
            hbox:
                spacing 25
                textbutton yes action Return(True) sensitive ready text_size 25
                textbutton no action Return(False) sensitive ready text_size 25

screen r13_activities():
    style_prefix "r13"
    modal True
    zorder 45
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    frame:
        area (180,160,920,495) padding (26,25)
        vbox:
            spacing 20
            text "이곳에서 할 수 있는 일" size 32 color "#765426"
            viewport:
                xsize 850 ysize 305 draggable True mousewheel True scrollbars "vertical"
                vbox:
                    spacing 16
                    for key,a in r13_actions():
                        textbutton (a["title"]+(" · "+r13_time_target() if a.get("cost",1) else "")):
                            action Return(key) sensitive ready and (room13["period"]<3 or not a.get("cost",1)) xsize 810 text_size 24
                    if not r13_actions():
                        text "주변을 살피거나 주민과 이야기하며 확인할 일을 찾아보자." size 24 xsize 780
            textbutton "돌아가기" action Return(False) sensitive ready

screen r13_book(target=None,present=False,hearing=False):
    style_prefix "r13"
    modal True
    zorder 50
    default detail=None
    default ready=False
    default archive=False
    default category="evidence"
    default page=0
    default order="recent"
    default favorite_only=False
    timer .35 action SetScreenVariable("ready",True)
    add Solid("#0c172a99")
    fixed:
        xsize 1280 ysize 720
        at Transform(zoom=(.96 if persistent.room13_large_text else .90),xalign=.5,yalign=.5)
        add Solid("#eee7d6")
        text ("자료 보여 주기 · "+R13_NAMES.get(target,"재판") if present else "자료 기록") style "r13_title_text" xpos 32 ypos 29
        if target:
            add Transform(r13_art(target,"avatar_neutral"),xysize=(64,66),fit="contain",nearest=True) xpos 1180 ypos 14
        hbox:
            xpos 32 ypos 98 spacing 10
            for key,title in (("evidence","증거"),("testimony","들은 말")):
                textbutton title:
                    style "r13_paper_tab_button" xsize 168 ysize 48 background R13PaperPanel(category==key)
                    sensitive ready
                    action [SetScreenVariable("category",key),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
        text ("자료를 눌러 선택한 뒤 보여주세요" if present else "조사로 확인한 물건과 문서" if category=="evidence" else "인물에게 직접 들은 말") style "r13_secondary_text" xpos 400 ypos 112
        if not present:
            hbox:
                xpos 816 ypos 98 spacing 8
                textbutton "이번 여정" style "r13_paper_tab_button" xsize 206 ysize 48 background R13PaperPanel(not archive) sensitive ready action [SetScreenVariable("archive",False),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
                textbutton "이전 발견" style "r13_paper_tab_button" xsize 206 ysize 48 background R13PaperPanel(archive) sensitive ready action [SetScreenVariable("archive",True),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
        $ entries=r13_record_entries(category,archive,present,order,favorite_only)
        use r13_record_filters("r13_book",order,favorite_only,archive and not present)
        $ selected_record=r13_record_selected(entries,detail,page)
        use r13_material_detail(selected_record,archive and not present)
        use r13_material_grid(entries,selected_record,page,"r13_book",archive and not present)
        if present:
            textbutton ("이 주장에 근거로 낸다" if hearing else R13_NAMES.get(target,"상대")+"에게 보여주기"):
                style "r13_compact_button" xpos 872 ypos 644 xsize 376 ysize 64 text_size r13_read_size(22,27)
                action Return(selected_record)
                sensitive ready and detail==selected_record and selected_record in room13.get("evidence",[]) and not archive
        else:
            text ("%d개 · 이전 여정의 기록"%len(entries) if archive else "%d개 · 이번 여정에서 모음"%len(entries)) style "r13_secondary_text" xpos 880 ypos 661
        textbutton ("그만두기" if present else "닫기"):
            style "r13_compact_button" xpos 32 ypos 644 xsize 220 ysize 64 text_size r13_read_size(22,27)
            action (Return(False) if present else Hide("r13_book")) sensitive ready
        key "game_menu" action (Return(False) if present else Hide("r13_book"))

screen r13_calendar():
    style_prefix "r13"
    modal True
    zorder 55
    default week=(room13["day"]-1)//7
    add Solid("#243732b0")
    add R13PaperPanel() xpos 30 ypos 20 xsize 1220 ysize 685
    text "여행 수첩 · 달력" xpos 60 ypos 35 size 35 color "#765426"
    for i,dayname in enumerate(("월","화","수","목","금","토","일")):
        text dayname xpos 80+i*170 ypos 106 size 24
    for day in range(week*7+1,week*7+8):
        frame:
            area (55+((day-1)%7)*170,155,155,150)
            background R13PaperPanel(day==room13["day"]) padding (14,14)
            vbox:
                spacing 17
                text (str(day)+"일") size 25
                if day==room13["day"]:
                    text "오늘" size 20 color "#765426"
                elif day<room13["day"]:
                    text "지난 날" size 18
    text "확인한 약속" xpos 60 ypos 420 size 26 color "#765426"
    viewport:
        area (60,462,1140,176) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 18
            for promise in r13_calendar_promises():
                text promise size r13_read_size(23,29) color "#342a23" xsize 1100
            if not r13_calendar_promises():
                text "날짜가 정해진 새 약속은 아직 없다." size r13_read_size(23,29) color "#536158" xsize 1100

    textbutton "닫기" xpos 60 ypos 650 action Hide("r13_calendar")
    if week>0:
        textbutton "지난 주" xpos 700 ypos 650 action SetScreenVariable("week",week-1)
    textbutton "다음 주" xpos 970 ypos 650 action SetScreenVariable("week",week+1)

screen r13_debate(claim):
    style_prefix "r13"
    modal True
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    frame:
        area (50,155,1180,425) padding (26,22) background R13PaperPanel()
        vbox:
            spacing 22
            text R13_CLAIMS[claim]["assertion"] size 32 color "#765426"
            text "내가 내놓은 근거" size 23
            viewport:
                xsize 1110 ysize 180 draggable True mousewheel True scrollbars "vertical"
                vbox:
                    spacing 7
                    for key in room13["arguments"].get(claim,[]):
                        text ("· "+ROOM13["evidence"][key]["name"]) size 22
                    if not room13["arguments"].get(claim):
                        text "아직 내놓지 않았다." size 22 color "#817e70"
            hbox:
                spacing 18
                textbutton "근거 내놓기" action Return("present") sensitive ready
                textbutton "되묻기" action Return("press") sensitive ready
                textbutton "논리를 연결한다" action Return("argue") sensitive ready
                textbutton "이 문제는 남겨 둔다" action Return("leave") sensitive ready text_size 22

screen r13_handoff():
    style_prefix "r13"
    modal True
    zorder 40
    add Solid("#172a2aa6")
    frame:
        area (175,135,930,465) padding (35,30)
        vbox:
            spacing 25
            text "13호 사건 · 둘째 주 이어가기" size 35 color "#765426"
            text "이전 개발본의 끝에 도착했습니다.\n이번에 내려진 결정과, 갇혔는지 풀려났는지를 그대로 이어 갑니다." size 27 xsize 840
            text ("다람이: "+("아빠와 동행" if room13["daram_state"]=="with_dad" else "보호시설에 갇힘")+"\n할머니: "+("갇힘" if room13["granny_state"]=="detained" else "자유 상태")) size 25
            text "이 화면은 이야기 속 엔딩이 아닙니다." size 22 color "#717367"
            hbox:
                spacing 18
                textbutton "저장하기" action ShowMenu("save")
                textbutton "이어서 진행" action [Hide("r13_handoff"),Jump("r13_week2_opening")]
                textbutton "제목으로" action MainMenu(confirm=False)
