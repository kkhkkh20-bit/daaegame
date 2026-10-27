screen r13_hud():
    style_prefix "r13"
    zorder 20
    # Carriage skip shares the compact dialogue footer; no duplicate top button.







    if not r13_cg_active and place!="마차 안" and not r13_meeting_active:
        frame:
            xpos (940 if renpy.get_screen("r13_hub") else R13_CONCEPT_RIGHT-238) ypos 20 xsize 238 ysize 72 padding (0,0) background r13_field_paper()
            fixed:
                xysize (238,72)
                # 2026-10-27 타이포 시안: 큰 숫자 title, 작은 글자 small. 「일째」는 small(22~28)이 48px 에 안 들어가
                # 두 줄로 꺾이므로 켜진 동안만 칸을 60(시계 글자 시작 76 앞)까지 넓힌다.
                # 2026-10-27 소유자 「날짜 네모칸에 글씨 삐져나옴」: 72px 칸에 두 줄이 들어야 한다. 큰 글씨·휴대폰에서
                # title 34~36(줄 42~44)+small 26~28(줄 32~34)=74~78 로 넘쳤고 「늦은 저녁」 28px 는 104px 칸과 같은 폭.
                # Pretendard 실측(진행폭·ascent+descent)으로 상한을 둔다 — 숫자 32(줄 39, 「14」 36px)·일째 24(줄 29, 42px)
                # ·요일 26(줄 33, 67px)·시간대 24(줄 29, 「늦은 저녁」 89px). 왼쪽 열 3+39, 41+29=70 / 오른쪽 열 10+33, 42+29=71.
                # 칸을 키우지 않는 것은 이름표 충돌 판정(r13_field_ui_rects)이 이 칸을 기준으로 해서다.
                text ("%02d"%room13.get("day",1)) xpos 14 ypos (1 if R13_TYPE_V2 else 8) xsize (60 if R13_TYPE_V2 else 48) text_align .5 size (min(r13_type("title") if R13_TYPE_V2 else 28,32)) color (r13_type_color("ink") if R13_TYPE_V2 else "#493b30") font R13_UI_BOLD_FONT
                text "일째" xpos 14 ypos (37 if R13_TYPE_V2 else 42) xsize (60 if R13_TYPE_V2 else 48) text_align .5 size (min(r13_type("small") if R13_TYPE_V2 else 14,24)) color (r13_type_color("muted") if R13_TYPE_V2 else "#796044") font r13_ui_font()
                text r13_clock().split(" · ")[1] xpos 76 ypos (6 if R13_TYPE_V2 else 12) xsize (104 if R13_TYPE_V2 else 92) size (min(r13_type("body") if R13_TYPE_V2 else 20,26)) color (r13_type_color("ink") if R13_TYPE_V2 else "#493b30") font R13_UI_BOLD_FONT
                text r13_clock().split(" · ")[-1] xpos 76 ypos (37 if R13_TYPE_V2 else 40) xsize (104 if R13_TYPE_V2 else 92) size (min(r13_type("small") if R13_TYPE_V2 else 18,24)) color (r13_type_color("muted") if R13_TYPE_V2 else "#65503b") font r13_ui_font()
                add R13TimeDial() xpos 182 ypos 16
        frame:
            xpos 24 ypos 20 padding (12,8) background r13_field_paper(tape=True)
            hbox:
                spacing 1
                add Transform(Crop((16,16,32,32),r13_asset_path("file:assets/ui-b-field/b_icon_pin.png")),xysize=(28,28)) yalign .5
                text r13_hud_place() size (r13_type("title") if R13_TYPE_V2 else r13_read_size(20,23)) color (r13_type_color("ink") if R13_TYPE_V2 else "#493b30") font R13_UI_BOLD_FONT yalign .5

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
        use r13_notebook_topic_tools(ready,person,present_action)
    elif mode!="field":
        use r13_playback_footer(show_record=True,ready=ready)
    else:
        use r13_field_view_controls(ready)
        fixed:
            area (180,84,144,88 if r13_touch_ui() else 64)
            use r13_field_top_button("기록","record",Show("r13_records"),ready)
        use r13_options_control(ready)

screen r13_options_control(ready=True):
    # A compact instance of the same component, not a separate vertical icon layout.
    fixed:
        area (1190,20,64,64)
        use r13_field_button("","settings",Show("r13_more_tools"),enabled=ready,width=64,height=64,control_id="r13_options_gear")

screen r13_hub(entry=False):
    style_prefix "r13"
    modal True
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    default world_moving=False
    $ input_ready=ready and not world_moving
    default world_adjustment=r13_world_adjustment(room13["location"])

    if r13_world_width()>1280:
        # 0.20.3 (owner mockup D): a zoomed place draws its world smaller and leaves a strip below.
        if r13_world_height()*r13_field_zoom()<719:
            add Solid("#1d1611") ypos int(r13_world_height()*r13_field_zoom()) xsize 1280 ysize 720-int(r13_world_height()*r13_field_zoom())
            add Solid("#c9a86a88") ypos int(r13_world_height()*r13_field_zoom()) xsize 1280 ysize 1
        fixed:
            at r13_field_zoomed(r13_field_zoom())
            xsize r13_view_width() ysize r13_world_height()
            viewport:
                id "r13_world_viewport"
                area (0,0,r13_view_width(),r13_world_height())
                xadjustment world_adjustment
                draggable False mousewheel False arrowkeys False
                fixed:
                    xsize r13_world_width() ysize r13_world_height()
                    add r13_world_background()
                    use r13_world_contents(entry,input_ready)
        if not world_moving:
            use r13_world_camera_controls(world_adjustment)
    else:
        use r13_world_contents(entry,input_ready)
    if entry:
        use r13_waiting_window(input_ready)
    else:
        fixed:
            area (24,84,144,88 if r13_touch_ui() else 64)
            use r13_field_top_button("지도","map",Return(("menu","map")),input_ready)
    if not entry and r13_bed_available("bed"):
        fixed:
            area (1020,264,232,64)
            use r13_control("자기","auto",Return(("sleep","bed")),enabled=input_ready,height=64)
    if not entry and r13_evening_missions() and not r13_v111_active():  # 0.20.6: the new-world wait has no evening menu (button did nothing)
        fixed:
            area (772,104,232,64)
            use r13_control("저녁 할 일","auto",Return(("menu","evening")),enabled=input_ready,height=64)
    if not entry and r13_has("livelihood_open"):
        # 0.18.56 (owner): no work/shop board at the top. Work is asked for from the person who
        # gives it, goods are bought from the seller in person; only the purse is shown.
        frame:
            xpos 510 ypos 100 padding (12,6) background r13_field_paper(label=True)
            text ("가진 돈 %d냥"%r13_wallet(room13)["cash"]) size (r13_type("small") if R13_TYPE_V2 else r13_read_size(18,21)) color (r13_type_color("ink") if R13_TYPE_V2 else "#664932")
    if not entry and not r13_v111_active():
        use r13_event_offers(input_ready)
    use r13_admin_key()
    if not entry and r13_v111_active() and r13_v111_goal():
        use r13_goal_fold(r13_v111_goal(),input_ready)
    elif not entry and not r13_v111_active() and room13.get("life_poc") and room13["day"]<=2:
        use r13_goal_fold(r13_intro_goal(),input_ready)
    elif not entry and not r13_v111_active() and room13.get("life_poc") and r13_campaign_goal():
        use r13_goal_fold(r13_campaign_goal(),input_ready)
    use r13_toolbar(mode="field",ready=input_ready)
    $ hint=GetTooltip()
    if hint:
        frame:
            xpos max(12,min(980,renpy.get_mouse_pos()[0]+18)) ypos max(90,min(594,renpy.get_mouse_pos()[1]+22)) padding (14,9) background r13_field_paper()
            hbox:
                spacing 6
                text hint size (r13_type("body") if R13_TYPE_V2 else 20) color (r13_type_color("ink") if R13_TYPE_V2 else "#4b3021") yalign .5

    if world_moving:
        timer .05 repeat True action Function(r13_world_pan_finish,world_adjustment,_update_screens=False)
        # Eat pointer presses and releases through the entire slide, including
        # the dock. Disabled field actions alone still permit click-through.
        button:
            area (0,0,1280,720) background None hover_background None
            action NullAction() keyboard_focus False
        key "game_menu" action NullAction()
        key "rollback" action NullAction()
        key "rollforward" action NullAction()

screen r13_world_contents(entry=False,ready=False):
    style_prefix "r13"
    button:
        area (0,0,r13_world_width(),r13_world_height()) padding (0,0) background None hover_background None
        action Function(r13_empty_tap_feedback) sensitive ready alt "배경"
    # Background targets stay behind the visible residents.
    for key,spec in ROOM13["objects"].get(room13["location"],{}).items():
        if r13_object_visible(spec):
            button:
                area r13_object_target_rect(key,spec)
                background None hover_background None insensitive_background None padding (0,0)
                action [Function(r13_click_feedback,key),Return(("object",key))] sensitive ready
                tooltip r13_object_name(key) alt r13_object_name(key)
    # 0.18.63: separate prop layers (systems/room13_map_actions.rpy), behind the residents.
    for prop,px,py in r13_world_props(entry):
        add prop xpos px ypos py
    use r13_resident_stage(entry,ready)
    # Re-add masked object targets AFTER resident buttons. The existing mask
    # excludes faces and later small props; transparent sprite padding already
    # passes through via r13_actor_hit_mask. Drawing order must match this policy.
    for key,rect,mask in r13_objects_over_actors(entry):
        button:
            area rect focus_mask mask
            background None hover_background None insensitive_background None padding (0,0)
            action [Function(r13_click_feedback,key),Return(("object",key))] sensitive ready
            tooltip r13_object_name(key) alt r13_object_name(key)
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
        textbutton (R13_NAMES[nameplate["person"]]+(" !" if not entry and nameplate["person"]=="resident_piko" and r13_offer_for_person("resident_piko")=="r13_w1c_portrait" else "")):
            area nameplate["rect"]
            padding (7,2) background r13_field_paper(label=True) hover_background r13_field_paper(label=True,hover=True) text_size int((18 if r13_touch_ui() else 16)/r13_field_zoom()) text_color "#4b3021" text_hover_color "#9c3c2b" text_font R13_UI_BOLD_FONT text_xalign .5 text_yalign .5
            action r13_person_action(nameplate["person"],entry) sensitive ready
        if not entry and r13_offer_for_person(nameplate["person"]) and not (nameplate["person"]=="resident_piko" and r13_offer_for_person("resident_piko")=="r13_w1c_portrait"):
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
    if title=="선택" and place=="마차 안":
        use r13_carriage_choice_list(entries,ready,caption)
    elif person and title!="선택":
        use r13_side_question_list(person,pose,entries,ready,return_action,caption)
    else:
        use r13_notebook_choice_list(person,pose,title,entries,ready,return_action,caption)


screen r13_entry_topics():
    style_prefix "r13"
    modal True
    zorder 30
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    $ questions=[("제가 낸 신청서와 초소 명단을 보겠습니다.",Return(("entry","explain")),r13_has("question_read:entry:explain")),("원본 담당자를 기다리겠습니다.",Return(("entry","wait")),r13_has("question_read:entry:wait"))]
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
    $ questions=r13_v111_questions(person) if r13_v111_active() else [(r13_calendar_topic_title(key,spec),Return(key),r13_calendar_topic_seen(key,spec)) for key,spec in r13_topics_in_order(person)]
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

screen r13_book(target=None,present=False,hearing=False,called=False,purpose=None,chosen=()):
    # 0.20.6 (owner review): `called` - opened with `call screen`, so closing must return (a bare Hide
    # left the caller waiting: background only, no buttons). `purpose` names what the pick is for:
    # "proof" = a record added to Dad's own argument, "use" = a record Dad takes out himself.
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
    default page_restored=False
    default material_filter=remembered.get("material_filter","all")
    on "hide" action Function(r13_book_remember,view_context,detail,page,material_filter)
    default order="recent"
    $ chip_person=r13_book_person(target,hearing) if present else None
    timer .15 action SetScreenVariable("ready",True)
    if r13_meeting_active and r13_meeting_claim in R13_DEBATE:
        use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
    # 0.20.x 증거 비교 창 (plan5 m2a/m2b): the same brown 자료 view as 기록. Presenting keeps the
    # single big-picture view with the primary 「~에게 보여주기」; comparing is for reading only.
    default pair=None
    default pair_slot=1
    # 2026-10-24 증거 서랍(v111): 회의·대화의 보여주기도 「이번 사건」이 먼저 열리고 「지난 사건」·「사람별」을 열 수 있다.
    # 어느 자료가 다시 쓰이는지는 표시하지 않는다. 옛 이야기는 예전대로 「지난 사건」 묶음이 목록에서 빠진다.
    default drawer="now"
    default drawer_case=None
    default drawer_gpage=0
    default drawer_ipage=0
    $ drawer_on=r13_drawer_active(archive)
    $ entries=r13_catalog_entries(archive and not present,hearing)
    if drawer_on:
        $ drawer_all=entries
        $ drawer_view=r13_drawer_view(drawer,drawer_all,detail,drawer_case)
        $ drawer_back=[k for k in (drawer_view[1] or ()) if k in R13_DRAWER_BACK]
        $ entries=[k for k in (drawer_view[1] or ()) if k not in R13_DRAWER_BACK]
    $ entries=r13_present_entries(entries,target) if present else entries
    $ material_filter="all" if material_filter=="unread" or ((hearing or archive) and material_filter=="transfer") else material_filter
    $ entries=entries if drawer_on else r13_material_subset(entries,material_filter)
    # 0.19.2: 보여줄 때는 단추 없이, 지금 상대(발언자)와 이어진 자료를 앞에 놓는다.
    if chip_person:
        $ entries=r13_record_related_first(entries,chip_person)
    if drawer_on:
        $ entries=drawer_back+entries
    if not page_restored and not (drawer_on and drawer_view[0]=="groups"):
        $ page=r13_record_restore_page(entries,detail,page)
        $ page_restored=True
    $ selected_record=(r13_drawer_selected(entries,detail,page,present) if drawer_on else
        (r13_present_selection(entries,detail,page) if present else r13_record_selected(entries,detail,page)))
    $ statement=r13_book_statement() if present and hearing else None
    $ day_span=r13_evidence_day_span(entries)
    $ purpose_text=R13_BOOK_PURPOSE.get(purpose)
    $ book_copy=r13_book_ui_copy(purpose,chosen,hearing,target)
    $ present_label=("이 주장에 근거로 낸다" if hearing else ((("비교에서 빼기" if purpose=="compare" else "근거에서 빼기") if purpose in ("proof","compare") and detail in chosen else purpose_text[0]) if purpose_text else R13_NAMES.get(target,"상대")+"에게 보여주기"))
    $ present_ok=bool(present and ready and detail==selected_record and selected_record and r13_catalog_can_present(selected_record,hearing) and not archive)
    use r13_ink_record_shell((book_copy["title"] if present else "자료 기록"),r13_ev_record_tabs("r13_book",present),"all",
        (Return(False) if present or called else Hide("r13_book")),
        note=((statement[0]+"의 발언에 낼 자료" if statement else book_copy["note"]) if present else None))
    if drawer_on:
        use r13_ink_chips(r13_drawer_chips("r13_book",drawer,(False if not present and r13_learning_archive_keys() else None)))
    else:
        use r13_ink_chips(r13_ev_filter_chips("r13_book",material_filter,not hearing and not archive,None,0,(archive if not present and (archive or r13_learning_archive_keys()) else None)))
    if drawer_on and drawer_view[0]=="groups":
        use r13_drawer_groups_view(drawer,drawer_all,drawer_case,drawer_gpage,drawer_ipage,"r13_book",r13_drawer_header(drawer,drawer_all,drawer_view,drawer_case))
        # 묶음을 고르는 동안에도 회의·대화를 그만둘 수 있게 「돌아가기」(또는 「선택 마치기」)는 늘 같은 자리에 둔다.
        $ stop_h=r13_ev_button_height()
        fixed:
            xpos R13_EV_RIGHT_X ypos (R13_EV_BOTTOM-stop_h) xysize (R13_EV_RIGHT_W,stop_h)
            use r13_control(book_copy["stop"],None,(Return(False) if present or called else Hide("r13_book")),enabled=ready,width=R13_EV_RIGHT_W,height=stop_h,label_size=r13_ev_label_size(book_copy["stop"],R13_EV_RIGHT_W),control_id="r13_ev_stop")
    else:
        use r13_evidence_browser(entries,selected_record,page,"r13_book",pair,pair_slot,archive and not present,view_context,
            (r13_drawer_header(drawer,drawer_all,(drawer_view[0],entries),drawer_case) if drawer_on else ("자료 %d개"%len(entries))+((" · "+day_span) if day_span else "")),
            present,present_label,present_ok,Return(selected_record),(Return(False) if present or called else Hide("r13_book")),ready,statement,
            (R13_NAMES.get(target,"상대")+"에게" if present and not statement and not purpose_text else None),
            stop_label=book_copy["stop"],present_help=book_copy["help"])

screen r13_calendar_content():
    default week=min(1,(room13["day"]-1)//7)
    # 2026-10-27 수첩 공통 틀: 달력 한 주(7칸 x 128)는 틀 안쪽 132 부터, 지난 주·다음 주는 하단 버튼 줄로.
    $ body_size=(r13_type("body") if R13_TYPE_V2 else r13_read_size(21,25))
    $ small_size=(r13_type("small") if R13_TYPE_V2 else 18)
    $ ink=(r13_type_color("ink") if R13_TYPE_V2 else "#493b30")
    $ muted=(r13_type_color("muted") if R13_TYPE_V2 else "#796044")
    $ accent=(r13_type_color("accent") if R13_TYPE_V2 else "#765426")
    text "달력" xpos (R13_NB_LEFT+4) ypos R13_NB_TOP size (r13_type("subtitle") if R13_TYPE_V2 else 26) color ink font R13_UI_BOLD_FONT
    text ("%d주째"%(week+1)) xpos R13_NB_RIGHT xanchor 1.0 ypos (R13_NB_TOP+6) size (r13_type("body") if R13_TYPE_V2 else 22) color muted font R13_UI_BOLD_FONT
    for i in range(7):
        text r13_weekday(week*7+1+i) xpos (R13_NB_LEFT+18+i*128) ypos (R13_NB_TOP+52) size (r13_type("body") if R13_TYPE_V2 else 22) color ink
    for day in range(week*7+1,week*7+8):
        frame:
            area (R13_NB_LEFT+((day-1)%7)*128,R13_NB_TOP+86,120,116)
            background R13PaperPanel(day==room13["day"]) padding (10,12)
            vbox:
                spacing 10
                text (str(day)+"일") size (r13_type("emphasis") if R13_TYPE_V2 else r13_read_size(23,27)) color ink
                if day==room13["day"]:
                    text "오늘" size small_size color accent
                elif day<room13["day"]:
                    text "지난 날" size small_size color muted
    text "확인한 약속" xpos (R13_NB_LEFT+4) ypos (R13_NB_TOP+220) size (r13_type("body") if R13_TYPE_V2 else 23) color accent font R13_UI_BOLD_FONT
    viewport:
        area (R13_NB_LEFT,R13_NB_TOP+256,R13_NB_WIDTH,max(60,r13_nb_body_bottom()-(R13_NB_TOP+256))) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 14
            for promise in r13_calendar_promises():
                text promise size body_size color ink xsize (R13_NB_WIDTH-40)
            if not r13_calendar_promises():
                text "날짜가 정해진 새 약속은 아직 없다." size body_size color muted xsize (R13_NB_WIDTH-40)
    use r13_nb_footer_button(2,"지난 주",Function(r13_record_select,_scope,"week",week-1),enabled=week>0,control_id="r13_cal_prev")
    use r13_nb_footer_button(1,"다음 주",Function(r13_record_select,_scope,"week",week+1),enabled=week<1,control_id="r13_cal_next")

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
                textbutton "선택한 근거 제출" action Return("argue") sensitive ready
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
