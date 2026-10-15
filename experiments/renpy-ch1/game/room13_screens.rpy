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
            xpos 940 ypos 20 xsize 238 ysize 68 padding (10,8) background R13StonePanel(alpha="ff")
            hbox:
                spacing 10
                vbox:
                    xsize 42 spacing 2
                    text ("%02d"%room13.get("day",1)) size 25 color "#f1e9cf" xalign .5
                    text "일째" size 12 color "#c9ccba" xalign .5
                vbox:
                    xsize 112 spacing 7
                    text r13_clock().split(" · ")[1] size 17 color "#f1e9cf"
                    text r13_clock().split(" · ")[-1] size 17 color "#d2d4bf"
                add R13TimeDial() yalign .5
        frame:
            xpos 24 ypos 20 padding (14,8) background R13StonePanel(alpha="d4")
            text (r13_location_path().replace("마을 › ","",1) if place != "마차 안" else place) size r13_read_size(18,22) color "#f3ecd5"

init 80:
    style r13_toolbar_button is r13_action_button:
        xsize 128
        ysize 44
        padding (10,6)
        background Solid("#102b35ed")
        hover_background Solid("#29434ed9")
        insensitive_background R13StonePanel(disabled=True)
    style r13_toolbar_button_text is r13_action_button_text:
        color "#edf0e5"
        hover_color "#ffffff"
        insensitive_color "#91a6ae"
        outlines [(1,"#14232a99",0,1)]
        xalign .5
        yalign .5

screen r13_toolbar(investigate_action=None,present_action=None,person=None,mode="line",ready=True):
    style_prefix "r13"
    if mode=="talk":
        # Question screens: the large "돌아가기" button returns; only the tools
        # used while choosing a question stay here.
        $ footer_width=r13_footer_width(2 if present_action is not None else 1)
        add R13StonePanel(alpha="d4") xpos (1280-footer_width) ypos 676 xsize footer_width ysize 44
        frame:
            area (1280-footer_width,664,footer_width,56) padding (8,0) background None
            hbox:
                spacing 8
                if present_action is not None:
                    textbutton "보여주기" style "r13_footer_button" action present_action sensitive ready
                textbutton "기록" style "r13_footer_button" action Show("r13_records") sensitive ready
    elif mode!="field":
        $ line_tools=(3 if mode=="line" else 0)
        $ footer_width=r13_footer_width(4+line_tools+(1 if investigate_action is not None else 0)+(1 if present_action is not None else 0))
        add R13StonePanel(alpha="d4") xpos (1280-footer_width) ypos 676 xsize footer_width ysize 44
        frame:
            area (1280-footer_width,664,footer_width,56) padding (8,0) background None
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
                if mode=="line":
                    $ line_active=ready and renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
                    # Player requests (0.18.4): skip read lines / everything to the next
                    # choice, and hide the dialogue window to see the picture.
                    textbutton "건너뛰기":
                        style "r13_footer_button" selected r13_fast_read
                        text_selected_color "#f6d18a" selected_background R13StonePanel(focused=True)
                        action Function(r13_toggle_read_skip) sensitive line_active
                        tooltip "읽은 대사를 다음 선택지까지 넘깁니다"
                    textbutton "빠르게":
                        style "r13_footer_button" selected r13_fast_all
                        text_selected_color "#f6d18a" selected_background R13StonePanel(focused=True)
                        action Function(r13_toggle_fast_all) sensitive line_active
                        tooltip "처음 보는 대사도 다음 선택지까지 넘깁니다"
                    textbutton "숨기기" style "r13_footer_button" action HideInterface() sensitive line_active
                textbutton "옵션" style "r13_footer_button" action ShowMenu("pause_menu") sensitive ready
    else:
        text "조사·대화·이동 · 시간 소모 없음":
            xalign .5 ypos 646 size r13_read_size(16,19) color "#f2f3e6"
            outlines [(1,"#14232a",0,1)]
        # Three independent controls leave the rest of the scene visible/clickable.
        hbox:
            xalign .5 ypos 650 spacing 8
            if mode=="field":
                frame:
                    xsize 128 ysize 44 yoffset 20 padding (10,6)
                    background R13StonePanel(focused=True)
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
        background R13StonePanel(alpha="b8") hover_background R13StonePanel(focused=True)
        insensitive_background R13StonePanel(disabled=True)
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
            add Solid("#3a3e3d",xsize=10,ysize=10) xpos 27 ypos 19
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
        textbutton "지도 · 이동":
            style "r13_action_button" xpos 1070 ypos 102 xsize 180 ysize 44
            text_size 23 action Return(("menu","map")) sensitive ready
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


screen r13_question_list(person,pose,title,entries,ready,actor_x=220,list_left=420,list_width=760,animate=True,return_action=None):
    style_prefix "r13"
    if person:
        $ list_width=min(900,max(760,list_width))
        $ list_left=(1280-list_width)//2
        # Face to face: retain the existing actor, centred behind the choices.
        # The person stands large
        # on the left, the scene is dimmed, and plain-text options name what
        # Dad will ask; the question itself is then spoken in dialogue.
        add r13_close_art(person,pose,760):
            xpos 640 xanchor .5 ypos r13_close_y(person,760,110,pose)
        add Solid("#000000a0")
        text r13_person_caption(person):
            xalign .5 ypos 24 xsize 940 text_align .5
            size r13_read_size(23,28) color "#f6d18a"
        if title=="선택":
            $ context=r13_choice_context()
            if context:
                text context[1]:
                    xpos list_left ypos 66 xsize list_width text_align .5
                    size r13_read_size(20,24) color "#e5ece6" line_spacing 3
        else:
            text "질문·자료 보여주기 · 시간 소모 없음":
                xalign .5 ypos 63 size r13_read_size(17,21) color "#e5ece6"
        if title!="선택":
            text title:
                xpos list_left ypos 146 xsize list_width text_align .5
                size r13_read_size(27,32) color "#f6d18a"
        viewport:
            area (list_left,204,list_width,342 if return_action is not None else 416)
            mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
            vbox:
                spacing 12
                for index,(title,action,was_read) in enumerate(entries):
                    button:
                        xsize list_width-23 yminimum r13_read_row_height() padding (18,15)
                        background R13StonePanel() hover_background R13StonePanel(focused=True)
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
            textbutton "돌아가기":
                xpos list_left+list_width//2 xanchor .5 ypos 558 xsize 220 ysize 64
                padding (18,12) background R13StonePanel() hover_background R13StonePanel(focused=True)
                text_size r13_read_size(23,28) text_color "#fff4df" text_xalign .5
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
                background R13StonePanel()
                vbox:
                    spacing 6
                    if context[0]:
                        text context[0] size r13_read_size(20,24) color "#f6d18a" font r13_ui_font()
                    text context[1]:
                        size r13_read_size(22,27) color "#fff4df" font r13_ui_font() line_spacing 4
                        xsize compact_width-44
            text ("어떻게 할까?" if renpy.variant("touch") else "어떻게 할까? · 숫자 키로도 고를 수 있다"):
                xalign .5 ypos list_floor-34 size r13_read_size(17,20) color "#e8d9b0"
                outlines [(1,"#101515",0,0)]
        else:
            text title:
                xalign .5 ypos 50 xsize compact_width text_align .5
                size r13_read_size(27,32) color "#f6d18a"
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
                        xsize compact_width-23 padding (16,10) background R13StonePanel()
                        text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.":
                            xsize compact_width-55 text_align .5 xalign .5 size r13_read_size(22,28) color "#eee5d5"
        if ready:
            for index,(title,action,was_read) in enumerate(entries[:9]):
                key ("K_%d"%(index+1)) action action
                key ("K_KP%d"%(index+1)) action action
        if return_action is not None:
            textbutton "돌아가기":
                xpos list_left+compact_width//2 xanchor .5 ypos 544 xsize 150 ysize 44
                padding (12,6) background R13StonePanel() hover_background R13StonePanel(focused=True)
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
    use r13_reference_record_shell("제시" if present else "자료 기록")
    use r13_reference_record_categories("r13_book",category,True,archive and not present)
    if not present and r13_learning_archive_keys():
        textbutton ("이번 여정" if not archive else "지난 플레이"):
            style "r13_paper_tab_button" xpos 66 ypos 326 xsize 176 ysize 40 text_size 18
            action [SetScreenVariable("archive",not archive),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
    $ entries=r13_record_entries(category,archive,present,order,favorite_only)
    $ selected_record=r13_record_selected(entries,detail,page)
    use r13_record_filters("r13_book",order,favorite_only,archive and not present)
    use r13_material_grid(entries,selected_record,page,"r13_book",archive and not present)
    use r13_material_detail(selected_record,archive and not present)
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
