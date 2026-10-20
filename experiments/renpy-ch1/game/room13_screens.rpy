screen r13_hud():
    style_prefix "r13"
    zorder 20
    if place == "마차 안" and not pb01_active():
        # The opening carriage can always be skipped straight to the village gate.
        textbutton "씬 건너뛰기":
            style "r13_action_button"
            xpos 948 ypos 24 xsize 224 ysize 54
            text_size r13_read_size(20,24)
            action [SetVariable("r13_carriage_skip", True), Function(renpy.end_interaction, True)]
            tooltip "마차 이야기를 건너뛰고 마을 입구에 도착합니다"
    if not r13_cg_active and place!="마차 안" and not r13_meeting_active:
        frame:
            xpos (940 if renpy.get_screen("r13_hub") else R13_CONCEPT_RIGHT-238) ypos 20 xsize 238 ysize 68 padding (10,8) background R13PaperFrame()
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
            text r13_hud_place() size r13_read_size(18,22) color "#493b30"

init 80:
    style r13_toolbar_button is r13_action_button:
        xsize 128
        ysize 44
        padding (10,6)
        background R13ControlSurface()
        hover_background R13ControlSurface(hovered=True)
        insensitive_background R13ControlSurface(disabled=True)
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
        use r13_concept_dock(ready=ready,show_record=True,person=person,present_action=present_action,reserve_return=True)
    elif mode!="field":
        use r13_playback_footer(show_record=True,ready=ready)
    else:
        use r13_field_view_controls(ready)
        use r13_footer_control(4,"기록","record",Show("r13_records"),enabled=ready)
        use r13_options_control(ready)

screen r13_options_control(ready=True):
    # A compact instance of the same component, not a separate vertical icon layout.
    fixed:
        area (1190,20,64,64)
        use r13_control("","settings",Show("r13_more_tools"),enabled=ready,width=64,height=64,control_id="r13_options_gear")

screen r13_hub(entry=False):
    style_prefix "r13"
    modal True
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
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
        use r13_world_camera_controls(world_adjustment)
    else:
        use r13_world_contents(entry,ready)
    if entry:
        use r13_waiting_window(ready)
    else:
        fixed:
            area (1020,104,232,r13_control_height())
            use r13_antique_button("지도 · 이동","map",Return(("menu","map")),enabled=ready,width=232,height=r13_control_height())
    if not entry and r13_bed_available("bed"):
        fixed:
            area (1020,264,232,64)
            use r13_control("자기","auto",Return(("sleep","bed")),enabled=ready,height=64)
    if not entry and r13_evening_missions():
        fixed:
            area (772,104,232,64)
            use r13_control("저녁 할 일","auto",Return(("menu","evening")),enabled=ready,height=64)
    if not entry and r13_has("livelihood_open"):
        # 0.18.56 (owner): no work/shop board at the top. Work is asked for from the person who
        # gives it, goods are bought from the seller in person; only the purse is shown.
        frame:
            xpos 24 ypos 74 padding (12,6) background R13InkPanel(alpha="b8")
            text ("가진 돈 %d냥"%r13_wallet(room13)["cash"]) size r13_read_size(18,21) color "#fff2cf"
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
                text hint size 20 color "#fff2cf" yalign .5

screen r13_world_contents(entry=False,ready=False):
    style_prefix "r13"
    button:
        area (0,0,r13_world_width(),720) padding (0,0) background None hover_background None
        action Function(r13_empty_tap_feedback) sensitive ready alt "배경"
    # Background targets stay behind the visible residents.
    for key,spec in ROOM13["objects"].get(room13["location"],{}).items():
        if r13_object_visible(spec):
            button:
                area tuple(spec["rect"])
                background None hover_background None insensitive_background None padding (0,0)
                action [Function(r13_click_feedback,key),Return(("object",key))] sensitive ready
                tooltip r13_object_name(key) alt r13_object_name(key)
    # 0.18.50 (owner): where a person and an object overlap, the person is pressed. Objects drawn
    # in front of a resident stay pressable around the resident's silhouette.
    for key,rect,mask in r13_objects_over_actors(entry):
        button:
            area rect focus_mask mask
            background None hover_background None insensitive_background None padding (0,0)
            action [Function(r13_click_feedback,key),Return(("object",key))] sensitive ready
            tooltip r13_object_name(key) alt r13_object_name(key)
    # 0.18.63: separate prop layers (systems/room13_map_actions.rpy), behind the residents.
    for prop,px,py in r13_world_props(entry):
        add prop xpos px ypos py
    use r13_resident_stage(entry,ready)
    # Inspection ticks sit under the name tags, never on top of a name.
    for key,point in room13["checks"].items():
        $ point=r13_check_point(key,point)
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
            padding (12,7) background R13ActionPanel() hover_background R13ActionPanel(True) text_size 20 text_color "#fff2cf" text_xalign .5 text_yalign .5
            action r13_person_action(nameplate["person"],entry) sensitive ready
        if not entry and r13_offer_for_person(nameplate["person"]):
            # 0.18.53: something is happening with this person; press them to see it.
            frame:
                xpos nameplate["rect"][0]-38 ypos nameplate["rect"][1]+4 xsize 34 ysize 40 padding (0,0)
                background Solid("#d9a441")
                text "!" size 28 color "#2a1d10" xalign .5 yalign .5

    use r13_life_group_labels(entry,ready)

screen r13_resident_stage(entry=False,ready=False):
    for actor in r13_stage_people(entry):
        add r13_staged_visible_art(actor):
            id ("r13_world_"+actor["person"])
            xpos actor["x"] ypos actor["y"]
            at r13_actor_appear(r13_appearance_duration())
        button:
            area tuple(actor["rect"]) background None hover_background None insensitive_background None padding (0,0)
            focus_mask r13_actor_hit_mask(actor)
            action r13_person_action(actor["person"],entry) sensitive ready
            tooltip (R13_EVENT_OFFERS[r13_offer_for_person(actor["person"])][0] if not entry and r13_offer_for_person(actor["person"]) else r13_person_caption(actor["person"])+" · 말 걸기")


screen r13_question_list(person,pose,title,entries,ready,actor_x=220,list_left=420,list_width=760,animate=True,return_action=None,caption=""):
    style_prefix "r13"
    if person and title!="선택":
        use r13_side_question_list(person,pose,entries,ready,return_action,caption)
    elif person:
        $ list_width=min(900,max(760,list_width))
        $ list_left=(1280-list_width)//2
        # Face to face: retain the existing actor, centred behind the choices.
        # The person stands large
        # on the left, the scene is dimmed, and plain-text options name what
        # Dad will ask; the question itself is then spoken in dialogue.
        # 0.18.39 (owner): same size and place as in dialogue, so the person does not jump.
        add Solid("#00000030")
        add r13_close_art(person,pose,840):
            xpos r13_close_x(person,pose) xanchor .5 ypos r13_close_y(person,840,110,pose)
        if title=="선택":
            $ context=r13_choice_context()
            if context:
                # 0.18.93 (owner review of the question screen): the line just spoken sits on an ink
                # panel above the head, never as bare white text over the face or a bright background.
                frame:
                    xpos list_left ypos 18 xsize list_width padding (18,8,18,10)
                    background R13InkPanel(alpha="d9",slim=True)
                    text context[1]:
                        xsize list_width-36 text_align .5
                        size r13_read_size(20,24) color "#fff4df" line_spacing 3 font r13_ui_font()
                        outlines [(1,"#101515",0,0)]
        # Questions sit around the centre, clear of dialogue advancement and bottom tools.
        $ row_h=(80 if persistent.room13_large_text else 72)
        $ list_top,list_bottom=r13_question_bounds(entries,list_width)
        if caption:
            text caption:
                xpos list_left ypos list_top-44 xsize list_width text_align .5
                size r13_read_size(22,27) color "#f6d18a" outlines [(1,"#101515",0,0)]
        if title!="선택":
            text title.replace(R13_NAMES.get(person, ""), r13_display_name(person)):
                xpos list_left ypos max(34,list_top-78) xsize list_width text_align .5
                size r13_read_size(27,32) color "#fff0cc" outlines [(1,"#101515",0,0)]
            if R13_NAMES.get(person) and R13_NAMES[person] in title:
                text r13_display_role(person):
                    xpos list_left ypos max(76,list_top-38) xsize list_width text_align .5
                    size r13_read_size(18,20) color "#f3e7ce" outlines [(1,"#101515",0,0)]
        viewport:
            area (list_left,list_top,list_width,list_bottom-list_top)
            mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
            vbox:
                spacing 16
                for index,(title,action,was_read) in enumerate(entries):
                    button:
                        xsize list_width-23 yminimum row_h padding (18,17)
                        background R13ControlSurface() hover_background R13ControlSurface(hovered=True)
                        action r13_safe_question_action(action) sensitive ready
                        text (("%d  "%(index+1) if index<9 else "")+r13_question_caption(title,was_read,mark_unread=True)):
                            xsize list_width-59 text_align .5 xalign .5 yalign .5
                            size r13_read_size(24,30) font r13_ui_font()
                            color (r13_role_color("subdued") if was_read else r13_role_color("speech"))
                            outlines [(1,"#101515",0,0)]
                if not entries:
                    # 0.18.93: on a panel like the question rows (bare text sat on the person's face).
                    frame:
                        xsize list_width-23 padding (16,10) background R13InkPanel(alpha="d9",slim=True)
                        text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.":
                            xsize list_width-55 text_align .5 xalign .5 size r13_read_size(24,30) color "#eee5d5"
                            outlines [(1,"#101515",0,0)]
        if ready:
            for index,(title,action,was_read) in enumerate(entries[:9]):
                key ("K_%d"%(index+1)) action r13_safe_question_action(action)
                key ("K_KP%d"%(index+1)) action r13_safe_question_action(action)
        if return_action is not None:
            # Return to the scene sits at the right; topic tools reserve this slot.
            use r13_concept_action(R13_CONCEPT_RIGHT-232,232,"돌아가기","dialogue",return_action,enabled=ready)
    else:
        add Solid("#00000020")
        $ compact_width=min(list_width,940)
        $ choice_size=r13_read_size(23,28)
        $ list_left=(1280-compact_width)//2
        # Choices (owner, 0.18.4): the line just spoken stays above the options,
        # each option carries a number (keys 1-9). Captions are kept short (about
        # 20 characters) so a 940px row holds them on one line.
        $ context=r13_choice_context() if title=="선택" else None
        $ list_floor=(190 if context else 100)
        $ question_height=r13_reference_list_height(entries,compact_width,16,(470 if context else 430 if return_action is not None else 520),72,choice_size,vertical_padding=32)
        $ question_top=max(list_floor,int((690-question_height+list_floor-100)//2) if return_action is None else min(int((680-question_height)//2),534-question_height))
        if context:
            frame:
                xalign .5 ypos 34 xsize compact_width padding (22,14,22,16)
                background R13InkPanel(alpha="d9",slim=True)
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
                spacing 16
                for index,(title,action,was_read) in enumerate(entries):
                    button:
                        # Left padding clears the gold number tab drawn by R13ReferenceChoice.
                        xsize compact_width-23 yminimum 72 padding (72,16,20,16)
                        background R13ReferenceChoice(False,index+1 if index<9 else None) hover_background R13ReferenceChoice(True,index+1 if index<9 else None)
                        action r13_safe_question_action(action) sensitive ready
                        text r13_question_caption(title,was_read,False):
                            xsize compact_width-115 text_align .5 xalign .5 yalign .5
                            size choice_size font r13_ui_font()
                            color ("#d3e3e7" if was_read else "#ffffff")
                if not entries:
                    frame:
                        xsize compact_width-23 padding (16,10) background R13InkPanel(alpha="d9",slim=True)
                        text "지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.":
                            xsize compact_width-55 text_align .5 xalign .5 size r13_read_size(22,28) color "#eee5d5"
        if ready:
            for index,(title,action,was_read) in enumerate(entries[:9]):
                key ("K_%d"%(index+1)) action r13_safe_question_action(action)
                key ("K_KP%d"%(index+1)) action r13_safe_question_action(action)
        if return_action is not None:
            use r13_concept_action(R13_CONCEPT_RIGHT-232,232,"돌아가기","dialogue",return_action,enabled=ready)

screen r13_entry_topics():
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    $ questions=pb01_entry_questions() if pb01_active() else [("신청한 것과 이름 목록이 다른 이유가 뭡니까?",Return(("entry","explain")),r13_has("question_read:entry:explain")),("원본 담당자를 기다리겠습니다.",Return(("entry","wait")),r13_has("question_read:entry:wait"))]
    use r13_question_list("guard","interview_neutral","돌목에게 묻기",questions,ready,return_action=Return(("entry","back")))
    use r13_toolbar(investigate_action=Return(("entry","back")),present_action=Return(("entry","argue")),person="guard",mode="talk",ready=ready)

screen r13_entry_karo_topics():
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
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
    timer .15 action SetScreenVariable("ready",True)
    $ actor_pose=r13_conversation_pose(person)
    $ questions=[(r13_calendar_topic_title(key,spec),Return(key),r13_calendar_topic_seen(key,spec)) for key,spec in r13_topics_in_order(person)]
    use r13_question_list(person,actor_pose,R13_NAMES[person]+"에게 묻기",questions,ready,return_action=Return("back"))
    use r13_toolbar(investigate_action=Return("back"),present_action=Return("present"),person=person,mode="talk",ready=ready)

screen r13_confirm(message,yes="진행한다",no="돌아간다"):
    style_prefix "r13"
    modal True
    zorder 65
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    use r13_confirmation_card(message,yes,no,ready)
    # 0.18.99 PC: Enter = yes, Esc = no.
    if ready:
        key "K_RETURN" action Return(True)
        key "K_KP_ENTER" action Return(True)
        key "game_menu" action Return(False)

screen r13_activities():
    style_prefix "r13"
    modal True
    zorder 45
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
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
    on "show" action Function(r13_unread_hold.clear)
    modal True
    zorder 50
    on "show" action Function(source_fx,"note_open")
    $ view_context=r13_book_context(target,hearing)
    $ remembered=r13_book_views.get(view_context,{})
    default detail=remembered.get("detail")
    default ready=False
    default archive=False
    default category="all"
    $ category="all"
    default page=remembered.get("page",0)
    default material_filter=remembered.get("material_filter","all")
    on "hide" action Function(r13_book_remember,view_context,detail,page,material_filter)
    default order="recent"
    $ chip_person=r13_book_person(target,hearing) if present else None
    timer .15 action SetScreenVariable("ready",True)
    if r13_meeting_active and r13_meeting_claim in R13_DEBATE:
        use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
    use r13_reference_record_shell("보여주기" if present else "자료 기록")
    use r13_reference_record_categories("r13_book",category,True,archive and not present)
    if not present and r13_learning_archive_keys():
        textbutton ("이번 여정" if not archive else "지난 플레이"):
            style "r13_paper_tab_button" xpos 66 ypos 326 xsize 176 ysize 40 text_size 18
            action [SetScreenVariable("archive",not archive),SetScreenVariable("detail",None),SetScreenVariable("page",0)]
    if present:
        $ statement=r13_book_statement() if hearing else None
        text (statement[0]+"의 발언" if statement else R13_NAMES.get(target,"상대")+"에게") xpos 66 ypos 214 xsize 176 size 19 color "#6c512a"
        if statement:
            viewport:
                area (66,252,176,298) mousewheel True draggable True scrollbars "vertical"
                text statement[1] xsize 156 size r13_read_size(17,21) color "#493b30"
        else:
            text "먼저 보여주고, 건넬지는 대화 후 결정합니다." xpos 66 ypos 252 xsize 176 size 17 color "#625738"
    $ entries=r13_catalog_entries(archive and not present,hearing)
    $ entries=r13_present_entries(entries,target) if present else entries
    $ material_filter="all" if material_filter=="unread" or ((hearing or archive) and material_filter=="transfer") else material_filter
    $ entries=r13_material_subset(entries,material_filter)
    # 0.19.2: 보여줄 때는 단추 없이, 지금 상대(발언자)와 이어진 자료를 앞에 놓는다.
    if chip_person:
        $ entries=r13_record_related_first(entries,chip_person)
    $ selected_record=r13_present_selection(entries,detail,page) if present else r13_record_selected(entries,detail,page)
    text ("자료 %d개"%len(entries)) xpos 284 ypos 72 size 20 color "#65503b"
    use r13_material_filters("r13_book",material_filter,not hearing and not archive,unread=len(r13_material_subset(r13_catalog_entries(archive and not present,hearing),"unread")))
    use r13_material_grid(entries,selected_record,page,"r13_book",archive and not present,filters=r13_material_filters_visible(material_filter,not hearing and not archive))
    use r13_material_detail(selected_record,archive and not present,view_context) id (view_context,selected_record,archive,persistent.room13_large_text)
    if present and not selected_record:
        text "보여줄 자료를 직접 고르세요." xpos 842 ypos 320 xsize 362 text_align .5 size 18 color "#796044"
    if present:
        textbutton ("이 주장에 근거로 낸다" if hearing else R13_NAMES.get(target,"상대")+"에게 보여주기"):
            style "r13_compact_button" xpos 824 ypos r13_record_footer_y() xsize 398 ysize r13_record_footer_height() text_size r13_read_size(20,24)
            background R13ControlSurface(primary=True) hover_background R13ControlSurface(primary=True,hovered=True) insensitive_background R13ControlSurface(disabled=True)
            action Return(selected_record)
            sensitive ready and detail==selected_record and r13_catalog_can_present(selected_record,hearing) and not archive
    textbutton ("그만두기" if present else "닫기"):
        style "r13_compact_button" xpos 66 ypos r13_record_footer_y() xsize 176 ysize r13_record_footer_height() text_size 20
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
    for i in range(7):
        text r13_weekday(week*7+1+i) xpos 302+i*128 ypos 128 size 22 color "#493b30"
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
    timer .15 action SetScreenVariable("ready",True)
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

# Approved fixed evidence action, shared by conversation toolbars.
screen r13_present_button(command,ready,x,y,w=332,h=72):
    fixed:
        area (x,y,w,h)
        use r13_control("자료 보여주기","present",command,enabled=ready,primary=True,width=w,height=h,control_id="r13_present_button")
