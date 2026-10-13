screen r13_hud():
    style_prefix "r13"
    zorder 20
    frame:
        xpos 24 ypos 20 xsize 654 ysize 70 padding (18,12)
        background R13ActionPanel()
        hbox:
            spacing 22
            text r13_clock() size 19 color "#d6b779" yalign .5
            add Solid("#8a7958",xsize=2,ysize=36) yalign .5
            text place size 22 color "#fff2cf" xsize 310 yalign .5

screen r13_toolbar(investigate_action=None,present_action=None,person=None,mode="line",ready=True):
    style_prefix "r13"
    if mode in ("field","talk"):
        button:
            area (0,642,1280,78) padding (0,0)
            background Solid("#102322e8") hover_background Solid("#102322e8")
            action NullAction() keyboard_focus False
    hbox:
        xpos 310 ypos 654 spacing 10
        textbutton "조사":
            style "r13_action_button" xsize 225 ysize 58
            action (investigate_action or NullAction())
            selected mode=="field" sensitive ready and (mode=="field" or investigate_action is not None)
            tooltip ("대화를 마치고 현장을 살핍니다" if mode=="talk" else "대화가 끝나면 현장을 살필 수 있습니다")
        textbutton "제시":
            style "r13_action_button" xsize 225 ysize 58
            action (present_action or NullAction()) sensitive ready and present_action is not None
            tooltip ((R13_NAMES.get(person,"")+"에게 자료를 보여줍니다") if person else "인물을 눌러 대화를 시작하세요")
        textbutton "기록":
            style "r13_action_button" xsize 225 ysize 58
            action Show("r13_records") sensitive ready
        textbutton "옵션":
            style "r13_action_button" xsize 225 ysize 58
            action ShowMenu("pause_menu") sensitive ready
    if mode=="field":
        text "제시하려면 인물을 눌러\n대화를 시작하세요":
            xpos 35 ypos 660 xsize 252 size 18 color "#ced9d4"

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
            style "r13_action_button" xpos 1075 ypos 23 xsize 180 ysize 62
            text_size 23 action Return(("menu","map")) sensitive ready
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


screen r13_question_list(person,pose,title,entries,ready):
    style_prefix "r13"
    add r13_close_art(person,pose,760):
        id ("r13_topics_"+person)
        xpos 220 xanchor .5 ypos r13_close_y(person,760,126,pose)
        at r13_actor_appear(r13_appearance_duration())
    add Solid("#00000088")
    text title:
        xpos 420 ypos 150 xsize 760 text_align .5 size 29 color "#f6d18a"
    viewport:
        area (420,210,760,402)
        mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 14
            for title,action,was_read in entries:
                button:
                    xsize 737 yminimum 76 padding (18,15)
                    background None hover_background Solid("#ffffff18")
                    action action sensitive ready
                    text (("{s}"+title+"{/s}") if was_read else title):
                        xsize 701 text_align .5 xalign .5 size 24
                        color ("#898b88" if was_read else "#fff4df")
                        outlines [(1,"#101515",0,0)]
            if not entries:
                text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.":
                    xsize 720 text_align .5 size 24 color "#eee5d5"

screen r13_entry_topics():
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    $ questions=[("신청과 명부가 다른 이유가 뭡니까?",Return(("entry","explain")),r13_has("question_read:entry:explain")),("원본과 다시 대조해 주시겠습니까?",Return(("entry","wait")),r13_has("question_read:entry:wait"))]
    use r13_question_list("guard","interview_neutral","돌목에게 묻기",questions,ready)
    use r13_toolbar(investigate_action=Return(("entry","back")),present_action=Return(("entry","argue")),person="guard",mode="talk",ready=ready)

screen r13_entry_karo_topics():
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    $ questions=[("마차는 괜찮습니까?",Return("road"),r13_has("question_read:entry:karo:road")),("함께 왔다고 말해 주시겠어요?",Return("witness"),r13_has("question_read:entry:karo:witness")),("짐을 잠시 맡아 주시겠습니까?",Return("bags"),r13_has("question_read:entry:karo:bags"))]
    use r13_question_list("karo","interview_neutral","까로에게 묻기",questions,ready)
    use r13_toolbar(investigate_action=Return("back"),present_action=Return("present"),person="karo",mode="talk",ready=ready)

# Kept as a save-compatible screen name; people open their topics directly.
screen r13_interaction(person):
    use r13_topics(person)

screen r13_material_corner(key):
    zorder 85
    on "show" action Function(source_fx,"found")
    use r13_evidence_card(key,"제시한 자료")

# The resident stays on the left; opaque questions never cover the face.
screen r13_topics(person):
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    $ actor_pose=r13_conversation_pose(person)
    $ questions=[(spec["title"],Return(key),key in room13["read_topics"]) for key,spec in r13_topics(person)]
    use r13_question_list(person,actor_pose,R13_NAMES[person]+"에게 묻기",questions,ready)
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
    timer .35 action SetScreenVariable("ready",True)
    add Solid("#eee7d6")
    text ("자료 제시 · "+R13_NAMES.get(target,"재판") if present else "자료 기록") style "r13_title_text" xpos 32 ypos 29
    if target:
        add Transform(r13_art(target,"avatar_neutral"),xysize=(64,66),fit="contain",nearest=True) xpos 1180 ypos 14
    hbox:
        xpos 32 ypos 98 spacing 10
        for key,title in (("evidence","증거"),("testimony","증언")):
            textbutton title:
                style "r13_paper_tab_button" xsize 168 ysize 48 background R13PaperPanel(category==key)
                sensitive ready
                action [SetScreenVariable("category",key),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
    text ("조사로 확인한 물건과 문서" if category=="evidence" else "인물에게 직접 들은 말") style "r13_secondary_text" xpos 400 ypos 112
    if not present:
        hbox:
            xpos 816 ypos 98 spacing 8
            textbutton "이번 여정" style "r13_paper_tab_button" xsize 206 ysize 48 background R13PaperPanel(not archive) sensitive ready action [SetScreenVariable("archive",False),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
            textbutton "이전 발견" style "r13_paper_tab_button" xsize 206 ysize 48 background R13PaperPanel(archive) sensitive ready action [SetScreenVariable("archive",True),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
    $ entries=r13_record_entries(category,archive,present)
    $ selected_record=r13_record_selected(entries,detail,page)
    use r13_material_detail(selected_record,archive and not present)
    use r13_material_grid(entries,selected_record,page,"r13_book")
    if present:
        textbutton ("이 주장에 근거로 낸다" if hearing else R13_NAMES.get(target,"상대")+"에게 보여주기"):
            style "r13_compact_button" xpos 872 ypos 648 xsize 376 ysize 48
            action Return(selected_record)
            sensitive ready and selected_record in room13.get("evidence",[]) and not archive
    else:
        text ("%d개 · 이전 여정의 기록"%len(entries) if archive else "%d개 · 이번 여정에서 확보"%len(entries)) style "r13_secondary_text" xpos 880 ypos 661
    textbutton ("제시 취소" if present else "닫기"):
        style "r13_compact_button" xpos 32 ypos 648 xsize 220 ysize 48
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
    text ("내일 동틀 무렵 · 제단으로 호송한다는 통보를 받았다." if room13["day"]==13 and "day13_warning" in room13.get("events",[]) else "목요일 저녁 · 어르신과 만나기로 했다." if room13["day"]<=4 and r13_has("elder_appointment") else "일요일 · 다람이의 사건을 주민 앞에서 다룬다." if room13["day"]<=7 and r13_has("trial_notice") else "날짜가 정해진 새 약속은 아직 없다.") xpos 60 ypos 467 size 23 xsize 1110
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
            text "내가 제시한 근거" size 23
            viewport:
                xsize 1110 ysize 180 draggable True mousewheel True scrollbars "vertical"
                vbox:
                    spacing 7
                    for key in room13["arguments"].get(claim,[]):
                        text ("· "+ROOM13["evidence"][key]["name"]) size 22
                    if not room13["arguments"].get(claim):
                        text "아직 제시하지 않았다." size 22 color "#817e70"
            hbox:
                spacing 18
                textbutton "근거 제시" action Return("present") sensitive ready
                textbutton "되묻기" action Return("press") sensitive ready
                textbutton "논리를 연결한다" action Return("argue") sensitive ready
                textbutton "이 논점은 남겨 둔다" action Return("leave") sensitive ready text_size 22

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
            text "이전 개발본의 끝에 도착했습니다.\n이번 판결과 구금 상태를 유지하며 계속합니다." size 27 xsize 840
            text ("다람이: "+("아빠와 동행" if room13["daram_state"]=="with_dad" else "보호시설에 구금")+"\n할머니: "+("구금" if room13["granny_state"]=="detained" else "자유 상태")) size 25
            text "이 화면은 이야기 속 엔딩이 아닙니다." size 22 color "#717367"
            hbox:
                spacing 18
                textbutton "저장하기" action ShowMenu("save")
                textbutton "이어서 진행" action [Hide("r13_handoff"),Jump("r13_week2_opening")]
                textbutton "제목으로" action MainMenu(confirm=False)
