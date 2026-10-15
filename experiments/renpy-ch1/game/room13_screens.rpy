screen r13_hud():
    style_prefix "r13"
    zorder 20
    if place == "마차 안":
        # The opening carriage can always be skipped straight to the village gate.
        textbutton "건너뛰기 ›":
            style "r13_action_button"
            xpos 988 ypos 24 xsize 184 ysize 54
            text_size r13_read_size(20,24)
            action [SetVariable("r13_carriage_skip", True), Function(renpy.end_interaction, True)]
            tooltip "마차 이야기를 건너뛰고 마을 입구에 도착합니다"
    if not r13_cg_active and place!="마차 안":
        frame:
            xpos 940 ypos 20 xsize 238 ysize 68 padding (10,8) background R13PaperFrame()
            hbox:
                spacing 10
                vbox:
                    xsize 42 spacing 2
                    text ("%02d"%room13.get("day",1)) size 25 color "#493b30" xalign .5
                    text "일째" size 12 color "#796044" xalign .5
                vbox:
                    xsize 112 spacing 7
                    text r13_clock().split(" · ")[1] size 17 color "#493b30"
                    text r13_clock().split(" · ")[-1] size 17 color "#65503b"
                add R13TimeDial() yalign .5
        frame:
            xpos 24 ypos 20 padding (14,8) background R13PaperFrame()
            text (r13_location_path().replace("마을 › ","",1) if place != "마차 안" else place) size r13_read_size(18,22) color "#493b30"

init 80:
    style r13_toolbar_button is r13_action_button:
        xsize 128
        ysize 44
        padding (10,6)
        background R13InkPanel()
        hover_background R13InkPanel(focused=True)
        insensitive_background R13InkPanel(disabled=True)
    style r13_toolbar_button_text is r13_action_button_text:
        color "#edf0e5"
        hover_color "#ffffff"
        insensitive_color "#91a6ae"
        outlines []
        xalign .5
        yalign .5

screen r13_toolbar(investigate_action=None,present_action=None,person=None,mode="line",ready=True):
    style_prefix "r13"
    if mode=="talk":
        # Question screens: "돌아가기" sits at the bottom left (0.18.42); only the tools
        # used while choosing a question stay here.
        frame:
            area (1168,664,112,56) padding (0,0) background None
            use r13_antique_button("기록","record",Show("r13_records",target=person,present_action=present_action),enabled=ready,compact=True,width=112)
        if present_action is not None:
            fixed:
                xpos 260 ypos 628 xsize 220 ysize 64
                use r13_antique_button("보여주기","present",present_action,enabled=ready,width=220)
    elif mode!="field":
        use r13_playback_footer(show_record=True,ready=ready)
    else:
        # The investigation badge is a state, not a dead action button.
        frame:
            xpos 24 ypos 676 xsize 156 ysize 40 padding (8,4) background None
            hbox:
                spacing 6
                add R13AntiqueIcon("investigate",size=24) yalign .5
                text "조사 중" size 20 color "#efe2c2" outlines [(1,"#302b25",0,0)] font r13_ui_font() yalign .5
        frame:
            area (1168,664,112,56) padding (0,0) background None
            use r13_antique_button("기록","record",Show("r13_records"),enabled=ready,compact=True,width=112)
        use r13_options_control(ready)

screen r13_options_control(ready=True):
    # Owned by the active modal screen, so options remain clickable in dialogue.
    button:
        id "r13_options_gear"
        area (1190,20,64,64) padding (0,0)
        background R13InkPanel(alpha="b8") hover_background R13InkPanel(focused=True)
        insensitive_background R13InkPanel(disabled=True)
        action ShowMenu("pause_menu") sensitive ready
        tooltip "옵션" alt "옵션"
        fixed:
            xsize 64 ysize 64
            add R13AntiqueIcon("settings",size=34) xpos 15 ypos 6
            text "옵션" size 14 color "#e6ece2" xalign .5 ypos 45

screen r13_hub(entry=False):
    style_prefix "r13"
    modal True
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    default world_adjustment=r13_world_adjustment(room13["location"])

    if r13_world_width()>1280:
        viewport:
            id "r13_world_viewport"
            area (0,0,1280,720)
            xadjustment world_adjustment
            draggable True mousewheel "horizontal" arrowkeys False
            fixed:
                xsize r13_world_width() ysize 720
                add r13_world_background()
                use r13_world_contents(entry,ready)
                if not entry:
                    use r13_inn_v4_world_chips(ready)
        use r13_world_camera_controls(world_adjustment)
    else:
        use r13_world_contents(entry,ready)
    if not entry:
        hbox:
            xpos 1250 xanchor 1.0 ypos 158 spacing 8
            for destination,title in r13_local_connections():
              if destination not in r13_inn_v4_handled(room13["location"]):
                textbutton (title+" ›"):
                    style "r13_action_button" padding (16,10) ysize 64
                    text_size 21 action Return(("travel",destination)) sensitive ready
    if not entry:
        use r13_inn_v4_screen_chips(ready)
    if not entry and r13_inn_guide_available():
        textbutton "안내도":
            id "r13_inn_guide_button"
            style "r13_action_button" xpos 1058 xanchor 1.0 ypos 102 xsize 112 ysize 54
            text_size 22 action Show("r13_inn_guide") sensitive ready
            alt "여관 안내도 열기"
    if entry:
        use r13_waiting_window(ready)
    else:
        fixed:
            xpos 1070 ypos 82 xsize 180 ysize 64
            use r13_antique_button("지도 · 이동","map",Return(("menu","map")),enabled=ready,width=180)
    if not entry and r13_bed_available("bed"):
        textbutton "자기":
            style "r13_action_button" area (1010,584,220,56)
            action Return(("sleep","bed"))
    if not entry and r13_evening_missions():
        textbutton "저녁 할 일":
            style "r13_action_button" area (730,30,194,56) text_size 21
            action Return(("menu","evening")) sensitive ready
            tooltip "오늘 저녁에만 할 수 있는 일"
    if not entry and r13_has("livelihood_open"):
        textbutton ("일거리 · 상점  %d냥"%r13_wallet(room13)["cash"]):
            style "r13_action_button" area (448,30,270,56) text_size 21
            action Return(("livelihood",None)) sensitive ready
    if not entry:
        use r13_event_offers(ready)
    use r13_admin_key()
    if not entry and room13.get("life_poc") and room13["day"]<=2:
        use r13_goal_fold(r13_intro_goal(),ready)
    elif not entry and room13.get("life_poc") and r13_campaign_goal():
        use r13_goal_fold(r13_campaign_goal(),ready)
    use r13_toolbar(mode="field",ready=ready)
    $ hint=GetTooltip()
    if hint:
        frame:
            xpos max(12,min(980,renpy.get_mouse_pos()[0]+18)) ypos max(90,min(594,renpy.get_mouse_pos()[1]+22)) padding (14,9) background R13ActionPanel()
            hbox:
                spacing 6
                if hint in [r13_object_name(k) for k,spec in ROOM13["objects"].get(room13["location"],{}).items() if r13_object_visible(spec)]:
                    add R13AntiqueIcon("investigate",size=22) yalign .5
                text hint size 20 color "#fff2cf" yalign .5

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
    for key,rect,mask in r13_objects_over_actors(entry):
        button:
            area rect focus_mask mask
            background None hover_background None insensitive_background None padding (0,0)
            action [Function(r13_click_feedback,key),Return(("object",key))] sensitive ready
            tooltip r13_object_name(key)
    # Inspection ticks sit under the name tags, never on top of a name.
    for key,point in room13["checks"].items():
        if key.startswith(room13["location"]+":") and r13_visible_check(key,point) and not r13_point_on_face(point,entry):
            add TopicTick() xpos point[0]-13 ypos point[1]-13
    $ bundle_point=r13_gate_bundle_check_point()
    if bundle_point:
        add TopicTick() xpos bundle_point[0]-13 ypos bundle_point[1]-13
    use r13_admin_hitboxes()
    for nameplate in r13_actor_nameplates(r13_stage_people(entry)):
        if nameplate["leader"]:
            $ leader=R13NameLeader(nameplate["leader"])
            add leader xpos leader.left ypos leader.top
        textbutton R13_NAMES[nameplate["person"]]:
            area nameplate["rect"]
            padding (12,7) background R13ActionPanel() text_size 18 text_color "#fff2cf"
            action Return(("person",nameplate["person"])) sensitive ready

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
            tooltip (r13_person_caption(actor["person"])+" · 말 걸기")


screen r13_question_list(person,pose,title,entries,ready,actor_x=220,list_left=420,list_width=760,animate=True,return_action=None,caption=""):
    style_prefix "r13"
    if person:
        $ list_width=min(900,max(760,list_width))
        $ list_left=(1280-list_width)//2
        # Face to face: retain the existing actor, centred behind the choices.
        # The person stands large
        # on the left, the scene is dimmed, and plain-text options name what
        # Dad will ask; the question itself is then spoken in dialogue.
        # 0.18.39 (owner): same size and place as in dialogue, so the person does not jump.
        add Solid("#00000080")
        add r13_close_art(person,pose,840):
            xpos r13_close_x(person,pose) xanchor .5 ypos r13_close_y(person,840,110,pose)
        if title=="선택":
            $ context=r13_choice_context()
            if context:
                text context[1]:
                    xpos list_left ypos 66 xsize list_width text_align .5
                    size r13_read_size(20,24) color "#e5ece6" line_spacing 3
        # 0.18.39 (owner): the list sits where the dialogue window is. Its bottom is the window's
        # bottom edge (632) and it grows upward, so the face stays visible and choices and lines
        # are read at the same height.
        $ list_bottom=632
        # One line per question (owner, 0.18.39): text height plus a small margin, not two lines.
        $ row_h=(58 if persistent.room13_large_text else 48)
        # Measured (0.18.41), so a caption that wraps to two lines still fits without scrolling.
        $ list_h=r13_reference_list_height(entries,list_width-23,12,452,row_h,r13_read_size(24,30))+4
        $ list_top=max(204 if title!="선택" else 150,list_bottom-list_h)
        if caption:
            text caption:
                xpos list_left ypos list_top-44 xsize list_width text_align .5
                size r13_read_size(22,27) color "#f6d18a" outlines [(1,"#101515",0,0)]
        if title!="선택":
            text title:
                xpos list_left ypos list_top-56 xsize list_width text_align .5
                size r13_read_size(27,32) color "#f6d18a"
        viewport:
            area (list_left,list_top,list_width,list_bottom-list_top)
            mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
            vbox:
                spacing 12
                for index,(title,action,was_read) in enumerate(entries):
                    button:
                        xsize list_width-23 yminimum row_h padding (18,9)
                        background R13InkPanel() hover_background R13InkPanel(focused=True)
                        action action sensitive ready
                        text (("%d  "%(index+1) if index<9 else "")+r13_question_caption(title,was_read)):
                            xsize list_width-59 text_align .5 xalign .5
                            size r13_read_size(24,30) font r13_ui_font()
                            color (r13_role_color("subdued") if was_read else r13_role_color("speech"))
                            outlines [(1,"#101515",0,0)]
                if not entries:
                    text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.":
                        xsize list_width-40 text_align .5 size r13_read_size(24,30) color "#eee5d5"
        if ready:
            for index,(title,action,was_read) in enumerate(entries[:9]):
                key ("K_%d"%(index+1)) action action
                key ("K_KP%d"%(index+1)) action action
        if return_action is not None:
            # 0.18.42 (owner): not centred under the list, where it read as another choice.
            # Bottom-left corner, on the same row as the tools at the bottom right.
            textbutton "돌아가기":
                xpos 0 ypos 676 xsize 150 ysize 44
                padding (12,6) background R13InkPanel() hover_background R13InkPanel(focused=True)
                text_size r13_read_size(20,24) text_color "#fff4df" text_xalign .5
                action return_action sensitive ready
    else:
        add Solid("#00000048")
        $ compact_width=min(list_width,940)
        $ choice_size=r13_read_size(23,28)
        $ list_left=(1280-compact_width)//2
        # Choices (owner, 0.18.4): the line just spoken stays above the options,
        # each option carries a number (keys 1-9). Captions are kept short (about
        # 20 characters) so a 940px row holds them on one line.
        $ context=r13_choice_context() if title=="선택" else None
        $ list_floor=(190 if context else 100)
        $ question_height=r13_reference_list_height(entries,compact_width,14,(470 if context else 430 if return_action is not None else 520),56,choice_size)
        $ question_top=max(list_floor,int((690-question_height+list_floor-100)//2) if return_action is None else min(int((680-question_height)//2),534-question_height))
        if context:
            frame:
                xalign .5 ypos 34 xsize compact_width padding (22,14,22,16)
                background R13InkPanel()
                vbox:
                    spacing 6
                    if context[0]:
                        text context[0] size r13_read_size(20,24) color "#f6d18a" font r13_ui_font()
                    text context[1]:
                        size r13_read_size(22,27) color "#fff4df" font r13_ui_font() line_spacing 4
                        xsize compact_width-44
            if not caption:
                text ("어떻게 할까?" if renpy.variant("touch") else "어떻게 할까? · 숫자 키로도 고를 수 있다"):
                    xalign .5 ypos list_floor-34 size r13_read_size(17,20) color "#e8d9b0"
                    outlines [(1,"#101515",0,0)]
        else:
            text title:
                xalign .5 ypos 50 xsize compact_width text_align .5
                size r13_read_size(27,32) color "#f6d18a"
        if caption:
            text caption:
                xalign .5 ypos question_top-40 xsize compact_width text_align .5
                size r13_read_size(22,27) color "#f6d18a" outlines [(1,"#101515",0,0)]
        viewport:
            area (list_left,question_top,compact_width,question_height)
            mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
            vbox:
                spacing 14
                for index,(title,action,was_read) in enumerate(entries):
                    button:
                        # Left padding clears the gold number tab drawn by R13ReferenceChoice.
                        xsize compact_width-23 yminimum 56 padding (72,8,20,8)
                        background R13ReferenceChoice(False,index+1 if index<9 else None) hover_background R13ReferenceChoice(True,index+1 if index<9 else None)
                        action action sensitive ready
                        text r13_question_caption(title,was_read,False):
                            xsize compact_width-115 text_align .5 xalign .5 yalign .5
                            size choice_size font r13_ui_font()
                            color ("#d3e3e7" if was_read else "#ffffff")
                if not entries:
                    frame:
                        xsize compact_width-23 padding (16,10) background R13InkPanel()
                        text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.":
                            xsize compact_width-55 text_align .5 xalign .5 size r13_read_size(22,28) color "#eee5d5"
        if ready:
            for index,(title,action,was_read) in enumerate(entries[:9]):
                key ("K_%d"%(index+1)) action action
                key ("K_KP%d"%(index+1)) action action
        if return_action is not None:
            textbutton "돌아가기":
                xpos 0 ypos 676 xsize 150 ysize 44
                padding (12,6) background R13InkPanel() hover_background R13InkPanel(focused=True)
                text_size r13_read_size(20,24) text_color "#fff4df" text_xalign .5
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
    use r13_evidence_card(key,"보여 준 자료",conversation=True)

# The resident stays on the left; opaque questions never cover the face.
screen r13_topics(person):
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    $ actor_pose=r13_conversation_pose(person)
    $ questions=[(r13_calendar_topic_title(key,spec),Return(key),r13_calendar_topic_seen(key,spec)) for key,spec in r13_topics_in_order(person)]
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
                        textbutton (a["title"]+" · "+r13_learning_time_text(a.get("cost",1),ending=key=="w2_escape")):
                            action Return(key) sensitive ready and (room13["period"]<3 or not a.get("cost",1)) xsize 810 text_size 24
                    if not r13_actions():
                        text "주변을 살피거나 주민과 이야기하며 확인할 일을 찾아보자." size 24 xsize 780
            textbutton "돌아가기" action Return(False) sensitive ready

screen r13_book(target=None,present=False,hearing=False):
    style_prefix "r13"
    modal True
    zorder 50
    on "show" action Function(source_fx,"note_open")
    default detail=None
    default ready=False
    default archive=False
    default category="evidence"
    default page=0
    default order="recent"
    default favorite_only=False
    timer .35 action SetScreenVariable("ready",True)
    use r13_reference_record_shell("보여주기" if present else "자료 기록")
    use r13_reference_record_categories("r13_book",category,True,archive and not present)
    if not present and r13_learning_archive_keys():
        textbutton ("이번 여정" if not archive else "지난 플레이"):
            style "r13_paper_tab_button" xpos 66 ypos 326 xsize 176 ysize 40 text_size 18
            action [SetScreenVariable("archive",not archive),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
    $ entries=r13_record_entries(category,archive,present,order,favorite_only)
    $ entries=r13_present_entries(entries,target) if present else entries
    $ selected_record=r13_present_selection(entries,detail,page) if present else r13_record_selected(entries,detail,page)
    use r13_record_filters("r13_book",order,favorite_only,archive and not present)
    use r13_material_grid(entries,selected_record,page,"r13_book",archive and not present)
    use r13_material_detail(selected_record,archive and not present)
    if present and not selected_record:
        text "보여줄 자료를 직접 고르세요." xpos 842 ypos 320 xsize 362 text_align .5 size 18 color "#796044"
    if present:
        textbutton ("이 주장에 근거로 낸다" if hearing else R13_NAMES.get(target,"상대")+"에게 보여주기"):
            style "r13_compact_button" xpos 824 ypos 592 xsize 398 ysize 48 text_size r13_read_size(20,24)
            action Return(selected_record)
            sensitive ready and detail==selected_record and selected_record in room13.get("evidence",[]) and not archive
    textbutton ("그만두기" if present else "닫기"):
        style "r13_compact_button" xpos 66 ypos 594 xsize 176 ysize 44 text_size 20
        action (Return(False) if present else Hide("r13_book")) sensitive ready
    key "game_menu" action (Return(False) if present else Hide("r13_book"))

screen r13_calendar():
    modal True
    zorder 55
    use r13_records(initial_tab="calendar",close_action=Hide("r13_calendar"))

screen r13_calendar_content():
    default week=min(1,(room13["day"]-1)//7)
    text "달력" xpos 284 ypos 72 size 26 color "#765426"
    text ("%d주째"%(week+1)) xpos 1070 ypos 76 size 22 color "#796044"
    for i,dayname in enumerate(("월","화","수","목","금","토","일")):
        text dayname xpos 302+i*128 ypos 128 size 22 color "#493b30"
    for day in range(week*7+1,week*7+8):
        frame:
            area (284+((day-1)%7)*128,170,120,128)
            background R13PaperPanel(day==room13["day"]) padding (10,12)
            vbox:
                spacing 14
                text (str(day)+"일") size r13_read_size(23,27) color "#493b30"
                if day==room13["day"]:
                    text "오늘" size 18 color "#765426"
                elif day<room13["day"]:
                    text "지난 날" size 16 color "#796044"
    text "확인한 약속" xpos 284 ypos 334 size 23 color "#765426"
    viewport:
        area (284,378,918,194) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 14
            for promise in r13_calendar_promises():
                text promise size r13_read_size(21,25) color "#493b30" xsize 886
            if not r13_calendar_promises():
                text "날짜가 정해진 새 약속은 아직 없다." size 21 color "#796044"
    hbox:
        xpos 864 ypos 596 spacing 12
        textbutton "지난 주" style "r13_compact_button" xsize 158 ysize 44 text_size 19 sensitive week>0 action Function(r13_record_select,_scope,"week",week-1)
        textbutton "다음 주" style "r13_compact_button" xsize 158 ysize 44 text_size 19 sensitive week<1 action Function(r13_record_select,_scope,"week",week+1)

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
