style default:
    font R13_UI_FONT
    size 25
    color "#f3e7ce"
    # Break Korean at spaces, never inside a word (비/켜).
    language "korean-with-spaces"
style button:
    background Solid("#30261fed")
    hover_background Solid("#65503d")
    insensitive_background Solid("#282421")
    padding (18,12)
style button_text:
    color "#f3e7ce"
    hover_color "#ffdc91"
    insensitive_color "#91877a"
    size 24
style frame:
    background Solid("#201b18ef")
    padding (24,20)
style say_dialogue:
    size 29
    line_spacing 9
style say_label:
    size 25
    bold True
style bar:
    left_bar Solid("#b39060")
    right_bar Solid("#4f4034")
    thumb Solid("#f5e8cf",xsize=14,ysize=30)
    thumb_shadow None
style slider is bar
style scrollbar:
    base_bar Solid("#4f4034")
    thumb Solid("#b39060",xsize=14,ysize=42)

# A vertical scrollbar without its own width can consume the complete Side,
# leaving the evidence viewport at zero width even though its rows exist.
style vscrollbar:
    xsize 10
    base_bar Solid("#4f4034")
    thumb Solid("#b39060",xsize=10,ysize=42)
    bar_vertical True

# One topic style shared by town residents and the investigation interviews.
screen topic_banner(caption, topic_action, done=False, enabled=True):
    button:
        xsize 560 ysize 58 padding (3,3)
        background Solid("#bca579") hover_background Solid("#f0d391")
        action topic_action
        sensitive enabled
        fixed:
            add Solid("#293c39" if done else "#385952")
            add Solid("#dfd2af",xsize=10)
            text (("{s}"+caption+"{/s}") if done else caption) size 23 xalign .5 yalign .5 color ("#bbcbd0" if done else "#fff4d9")
            if done:
                add TopicTick() xpos 514 yalign .5

screen main_menu():
    tag menu
    style_prefix "r13"
    $ title_continue = r13_continue_slot()
    $ title_has_save = bool(r13_save_slots())
    default title_focus = ("continue" if r13_continue_slot() else "new")
    # 승인된 B 메인 납품 좌표. 배경에 합쳐진 조명에는 구판 title light rig를 얹지 않는다.
    add Transform(r13_asset_path("file:assets/ui-b-main/b_main_background_postcard.png"), zoom=1280.0/1672)
    add Transform(r13_asset_path("file:assets/ui-b-main/b_logo.png"), zoom=.85) xpos -18 ypos 10
    # Approved single transparent ensemble sticker; preserve its original ratio.
    add Transform(r13_asset_path("file:assets/ui-b-main/b_main_cast_poster_plain.png"),zoom=610.0/1402) xpos 754 ypos 80
    fixed:
        at r13_title_menu_in
        hbox:
            xpos 44 ypos 616 spacing 14
            use r13_cover_button("이어하기","continue","acorn",184,(r13_load_action(title_continue) if title_continue is not None else NullAction()),title_focus,title_continue is not None,title_continue is not None)
            use r13_cover_button("처음부터","new","book",184,Start(),title_focus,True,title_continue is None)
            use r13_cover_button("불러오기","load","record",184,ShowMenu("load"),title_focus,title_has_save)
            use r13_cover_button("설정","settings","settings",184,ShowMenu("pause_menu"),title_focus)
    textbutton "음악 출처":
        xpos 44 ypos 696 padding (4,2) background None
        text_font R13_UI_FONT text_size 14 text_color "#c5c6d2" text_hover_color "#fff0ce"
        action Show("r13_music_credits")
    text config.version xpos 1172 ypos 674 font r13_ui_font() size 13 color "#b2b8b8"

# Two-line panels end 16px above the unchanged shared gameplay footer.
# Tops are expressed against the historical bottom=632 coordinate.
define R13_SAY_TOP_NORMAL = 528
define R13_SAY_TOP_LARGE = 520
init python:
    def _r13_say_size():
        return 31 if r13_touch_ui() else r13_read_size(28,31)

    def _r13_say_top(what=None):
        large=bool(persistent.room13_large_text) or r13_touch_ui()
        top=R13_SAY_TOP_LARGE if large else R13_SAY_TOP_NORMAL
        size=_r13_say_size()
        # r13_lines paginates two lines per click. Keep a safety expansion for
        # direct say / old-save notices outside that path; never crop their text.
        lines=_r13_say_lines(what,size,1028) if isinstance(what,str) else 1
        if lines>2:
            top-=(lines-2)*(size+7)
        if getattr(store,"r13_field_reading",False):return max(300,top+72)
        return max(300,top+r13_control_y()-16-632)

    import re as _r13_say_re
    def _r13_say_lines(what,size,width=756):
        """Rendered lines of a dialogue text: each written line wraps at the window width (Hangul
        and other wide glyphs count one em, Latin, digits and spaces half)."""
        per=width/float(size)
        total=0
        for line in _r13_say_re.sub(r"\{[^{}]*\}","",what).split("\n"):
            em=sum(1.0 if ord(ch)>0x2e7f else 0.55 for ch in line)
            total+=max(1,int(-(-em//per)))
        return total

screen say(who,what):
    if room13_mode:
        $ who = r13_speaker_label(who)
    # 0.19.97: the opening narration on black (room13_coach_cut.rpy) — white text, no panel.
    if room13_mode and r13_black_card:
        add Solid("#000")
        r13_dialogue_text what id "what" style "say_dialogue" xalign .5 yalign .46 xmaximum 980 text_align .5 layout "subtitle" size r13_read_size(26,30) line_spacing 8 font r13_ui_font() color "#e9e1d2"
        timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
        use r13_toolbar(mode="line")
    elif room13_mode and r13_meeting_active and r13_meeting_claim in R13_DEBATE and not r13_nw_meeting_claim(r13_meeting_claim):
        use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
        use r13_meeting_chrome(r13_meeting_claim)
        window:
            id "window"
            area (80,r13_control_y()-148,1120,132) background Frame(Crop((16,16,1168,128),r13_asset_path("file:assets/ui-b-dialogue/b_panel_dialogue.png")),48,24,64,24) padding (56,50,28,14)
            r13_dialogue_text what id "what" style "say_dialogue" size r13_read_size(23,29) line_spacing 5 xsize 1036 font R13_UI_BOLD_FONT color "#4b3420"
        if who:
            frame:
                xpos 104 ypos (r13_control_y()-158) padding (16,5,24,7)
                background Frame(Crop((16,12,168,32),r13_asset_path("file:assets/ui-b-dialogue/b_ribbon_name.png")),16,6,32,6)
                text who id "who" size r13_read_size(24,26) color "#fff3df" font R13_UI_BOLD_FONT xmaximum 1000 outlines []
        text "▸" xpos 1160 ypos (r13_control_y()-48) size 24 color "#4b3420"
        timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
        if r13_nw_meeting_claim(r13_meeting_claim):
            use r13_toolbar(mode="line")
        else:
            use r13_meeting_tools(r13_meeting_claim,r13_meeting_live_target())
        key "K_h" action Show("r13_backlog")
    elif not room13_mode:
        if room13_mode:
            key "K_h" action Show("r13_backlog")
        $ has_portrait = not room13_mode and dialogue_speaker in CAST
        window:
            id "window"
            xalign .5 ypos (454 if room13_mode and persistent.room13_large_text else 498 if room13_mode else 551) xsize (1008 if room13_mode else 1200) ysize (226 if room13_mode and persistent.room13_large_text else 166 if room13_mode else 169)
            background (r13_dialogue_frame() if room13_mode else Solid("#10262de8" if winter_mode else "#211a16f2"))
            padding (0,0)
            fixed:
                if not room13_mode:
                    add Solid("#b39060",xsize=1200,ysize=2)
                vbox:
                    xpos (32 if room13_mode else 240 if has_portrait else 32) ypos 18
                    spacing 10
                    if who and not room13_mode:
                        text who id "who" color "#ebcd8a" font (r13_ui_font() if room13_mode else R13_UI_FONT)
                    if room13_mode:
                        r13_dialogue_text what id "what" style "say_dialogue" size r13_read_size(26,32) line_spacing 7 xsize 930 text_align .0 font r13_ui_font() color r13_say_color()
                    else:
                        text what id "what" xsize (910 if has_portrait else 1120) font R13_UI_FONT color "#fff5df"
        if who and room13_mode:
            frame:
                xpos 160 xanchor 0.0 ypos (428 if persistent.room13_large_text else 474) padding R13_UI_PADDING["name"]
                background R13InkPanel()
                text who id "who" color R13_SPEAKER_COLOR font r13_ui_font() size r13_read_size(20,24)
        # No speaker profile beside the dialogue (owner's decision); the person is on stage.
        if has_portrait:
            frame:
                id "dialogue_portrait_frame"
                xpos 59 ypos 492 xsize 202 ysize 210
                padding (3,3) background Solid("#b39060")
                fixed:
                    add Solid("#30261f")
                    add Transform(dialogue_speaker + " avatar_"+dialogue_expression,size=(196,204),fit="contain") id "dialogue_portrait"
        text "▸" xpos (1092 if room13_mode else 1190) ypos (610 if room13_mode else 682) size 30 color "#e8c75c"
        if room13_mode:
            timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
            if r13_field_reading:
                pass
            elif place != "마차 안" and not r13_cg_active:
                use r13_toolbar(mode="line")
            else:
                use r13_playback_footer()
    else:
        # Approved B notebook dialogue; retain existing controls and story state.
        key "K_h" action Show("r13_backlog")
        if r13_meeting_active and r13_nw_meeting_claim(r13_meeting_claim):
            use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
            use r13_meeting_chrome(r13_meeting_claim)
        $ b_face = r13_bdialogue_face(r13_packet[0],r13_fullbody_emotion(r13_directed_pose)) if who and r13_packet and not r13_thought_active and "r13_visitor" not in renpy.get_showing_tags() else None
        $ b_text_x = 222 if b_face else 120
        $ b_text_width = 988 if b_face else 1090
        $ b_text_top = r13_night_say_top(what)
        add Transform(Frame(Crop((16,16,1168,128),r13_asset_path("file:assets/ui-b-dialogue/b_panel_dialogue.png")),48,24,64,24),xysize=(1220,714-(b_text_top-38)),alpha=r13_night_shade_alpha()) xpos 30 ypos (b_text_top-38)
        if b_face:
            add Transform(b_face,xysize=(112,112)) xpos 70 ypos (b_text_top-10)
        window:
            id "window"
            xpos b_text_x ypos b_text_top xsize b_text_width yminimum 40
            background None padding (0,0)
            r13_dialogue_text what id "what" style "say_dialogue" size r13_night_say_size() line_spacing 4 xsize b_text_width font R13_UI_BOLD_FONT color r13_night_text_color() outlines []
        if who:
            $ r13_name_track(who)
            hbox:
                xpos b_text_x ypos (r13_night_say_top(what)-60) spacing 12
                # 2026-10-26 소유자: 이름표가 스르륵 생기면 이상하다. 화자가 바뀌면 바로 보인다(r13_name_fade 는 쓰지 않음).
                frame:
                    background Frame(Crop((16,12,168,32),r13_asset_path("file:assets/ui-b-dialogue/b_ribbon_name.png")),16,6,32,6) padding (22,8,36,10) yalign .5
                    text who id "who" color "#fff3df" font R13_UI_BOLD_FONT size r13_read_size(27,30) xmaximum 640 outlines []
                if r13_offscreen_voice(who):
                    text r13_offscreen_voice(who) yalign .5 size r13_read_size(20,22) color "#fff3df" font r13_ui_font() outlines [(1,"#30261f",0,0)]
        # Next-line mark at the end of the controls row (mockup: "더보기 ▸").
        if r13_fx_active():
            text "▸" xanchor 1.0 xpos R13_CONCEPT_RIGHT yanchor .5 ypos r13_night_control_y() size 22 color "#4b3420" at r13_next_glow
        else:
            text "▸" xanchor 1.0 xpos R13_CONCEPT_RIGHT yanchor .5 ypos r13_night_control_y() size 22 color "#4b3420"
        timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
        if r13_field_reading:
            pass
        elif place != "마차 안" and not r13_cg_active:
            use r13_toolbar(mode="line")
        else:
            use r13_playback_footer()

style legacy_choice_frame is frame
style legacy_choice_vbox is vbox
style legacy_choice_button is button
style legacy_choice_button_text is button_text:
    font R13_UI_FONT

screen choice(items):
    style_prefix ("r13" if room13_mode else "legacy_choice")
    modal True
    default choice_ready = not winter_mode
    timer .35 action SetScreenVariable("choice_ready", True)
    # Talking with someone: the person stands on the left and the choices sit on
    # the right, like the question screen (owner, 0.18.6).
    default choice_visitor = room13_mode and "r13_visitor" in renpy.get_showing_tags()
    default choice_actor = (r13_motion_person if choice_visitor else (r13_last_partner if room13_mode and r13_last_partner in CAST else None))
    default choice_pose = (r13_directed_pose if choice_visitor and r13_directed_pose else r13_current_pose if choice_visitor else "interview_neutral") if room13_mode else "neutral"
    if room13_mode and r13_meeting_active:
        use r13_meeting_choices(items,choice_ready)
        if r13_nw_meeting_claim(r13_meeting_claim):
            use r13_toolbar(mode="line",ready=choice_ready)
    elif room13_mode:
        on "show" action Function(r13_choice_layout,choice_actor,choice_pose,True)
        on "hide" action Function(r13_choice_layout,choice_actor,choice_pose,False)
        # A menu caption (no action) is the question being asked: shown as a heading, never as
        # a numbered choice (0.18.41).
        $ choice_entries=[(item.caption,item.action,False) for item in items if item.action is not None]
        $ choice_caption=" ".join(item.caption for item in items if item.action is None)
        use r13_question_list(choice_actor,choice_pose,"선택",choice_entries,choice_ready,caption=choice_caption,actor_x=272,list_left=(500 if choice_actor else 190),list_width=(744 if choice_actor else 940),animate=False)
        use r13_toolbar(mode="line",ready=choice_ready)

    else:
        frame:
            xpos 165 ypos 200 xsize 950
            vbox:
                spacing 17
                for item in items:
                    textbutton item.caption action item.action xfill True ysize 72 sensitive choice_ready

screen hud():
    zorder 20
    if not renpy.get_screen("source_map") and not renpy.get_screen("arrival_map"):
        frame:
            xpos 24 ypos 18 padding (16,10)
            vbox:
                spacing 4
                text place size 23 color "#f8d994"
                text clock_text size 18 color "#c6b699"
    hbox:
        xpos 997 ypos 9 spacing 0
        imagebutton:
            xsize 82 ysize 74 padding (15,11)
            background None hover_background None
            idle Transform(r13_asset_path("file:assets/evidence.png"),size=(52,52))
            hover Transform(r13_asset_path("file:assets/evidence.png"),size=(52,52),alpha=0.75)
            action If(source_mode,Show("source_evidence"),Show("evidence_book"))
            tooltip "수첩"
        imagebutton:
            xsize 82 ysize 74 padding (15,11)
            background None hover_background None
            idle Transform(r13_asset_path("file:assets/save.png"),size=(52,52))
            hover Transform(r13_asset_path("file:assets/save.png"),size=(52,52),alpha=0.75)
            action ShowMenu("save")
            tooltip "저장"
        imagebutton:
            xsize 82 ysize 74 padding (15,11)
            background None hover_background None
            idle Transform(r13_asset_path("file:assets/menu.png"),size=(52,52))
            hover Transform(r13_asset_path("file:assets/menu.png"),size=(52,52),alpha=0.75)
            action ShowMenu("pause_menu")
            tooltip "설정"
    if GetTooltip():
        text GetTooltip() xalign 0.93 ypos 80 size 19

screen explore(location):
    modal True
    default input_ready = False
    timer 0.35 action SetScreenVariable("input_ready",True)
    # No hotspot tint, labels, cursor change or clue-location tooltip.
    if location == "room":
        add Transform(r13_asset_path("file:assets/pouch-world.png"),size=(60,64)) xpos 880 ypos 270
        add Transform(r13_asset_path("file:assets/flour-world.png"),size=(64,53)) xpos 590 ypos 337
        if archive_open:
            add Transform(Crop((832,565,404,164),r13_asset_path("file:assets/chest-open.png")),size=(150,80)) xpos 659 ypos 425
        else:
            add Transform(Crop((880,550,365,150),r13_asset_path("file:assets/chest.png")),size=(150,62)) xpos 659 ypos 443
        if lamp_ready and not somsom_found:
            add Transform(Crop((802,490,110,80),r13_asset_path("file:assets/somsom.png")),size=(27,19),alpha=0.23) xpos 828 ypos 480
        for key,rect in (("pouch",(680,215,310,115)),("flour",(563,331,150,97)),("under",(550,500,345,87)),("head",(620,170,325,62)),("chest",(655,406,158,93))):
            button:
                xpos rect[0] ypos rect[1] xsize rect[2] ysize rect[3]
                background None hover_background None insensitive_background None padding (0,0)
                sensitive input_ready
                action Return(key)
    else:
        $ spec = LOCATIONS[location]
        if spec[2]:
            imagebutton:
                idle Transform(spec[2] + " world",zoom=0.68)
                hover Transform(spec[2] + " world",zoom=0.68)
                xpos spec[3] ypos spec[4]
                yanchor (0.0 if spec[2] == "bami" else 1.0)
                sensitive input_ready
                action Return("talk")
        if location == "hall":
            add Transform(r13_asset_path("file:assets/clock-base.png"),size=(115,115)) xpos 410 ypos 170
            add Transform(r13_asset_path("file:assets/clock-hands.png"),size=(115,115)) xpos 410 ypos 170
            button:
                xpos 405 ypos 165 xsize 125 ysize 125
                background None hover_background None insensitive_background None padding (0,0)
                action Return("clock") sensitive input_ready
        if location == "doto":
            add Transform(r13_asset_path("file:assets/notebook.png"),size=(128,83)) xpos 850 ypos 324
            button:
                xpos 835 ypos 305 xsize 150 ysize 108
                background None hover_background None insensitive_background None padding (0,0)
                action Return("notebook") sensitive input_ready
    frame:
        xpos 25 ypos 604 xsize 760
        text current_goal() size 22 color "#dacba9"
    hbox:
        xpos 852 ypos 609 spacing 12
        imagebutton:
            idle Transform(r13_asset_path("file:assets/move.png"),size=(64,64))
            action Return("map") sensitive input_ready
            tooltip "이동"
        if location != "room":
            imagebutton:
                idle Transform(r13_asset_path("file:assets/talk.png"),size=(64,64))
                action Return("talk") sensitive input_ready
                tooltip "대화"
        if stage == "arrival" and "granny_arrival" in inspected:
            textbutton "방으로" action Return("rest") sensitive input_ready
        elif stage == "investigation":
            textbutton "원탁으로" action Return("meeting") sensitive input_ready
        elif stage == "aftermath":
            textbutton "마무리" action Return("finish") sensitive input_ready

screen village_map():
    modal True
    add Transform(r13_asset_path("file:assets/map.png"),size=(1280,720))
    add Solid("#140f0a88")
    frame:
        xpos 25 ypos 110
        vbox:
            spacing 8
            text "마을과 여관" size 32 color "#ffdc91"
            text "[current_goal()]" size 21
    for key in available_locations():
        $ pos = MAP_POINTS[key]
        button:
            xpos pos[0] ypos pos[1] xsize 224 ysize 91
            padding (10,12)
            background Solid("#211b17f5")
            action Return(key)
            hbox:
                spacing 8
                add Transform(r13_asset_path("file:assets/move.png"),size=(36,36))
                vbox:
                    spacing 6
                    text LOCATIONS[key][0] size 22
                    text ("현재 위치" if key == current_location else "다녀온 곳" if key in visited else "") size 17 color "#c6b699"
    textbutton "돌아가기" xpos 45 ypos 625 action Return(current_location)

screen chest_lock():
    modal True
    add Solid("#130f0be5")
    frame:
        xalign 0.5 ypos 145 xsize 910
        vbox:
            xfill True
            spacing 18
            text "오래된 숫자 자물쇠" size 34 color "#ffdc91"
            text "머리판의 첫 손님 날짜는 무엇이었지?" size 23
            hbox:
                spacing 24 xsize 552 xalign 0.5
                for i in range(4):
                    vbox:
                        spacing 10
                        textbutton "▲" action [SetVariable("digit_code",digit_code[:i]+[(digit_code[i]+1)%10]+digit_code[i+1:]),SetVariable("code_error",False)] xsize 120
                        text str(digit_code[i]) size 56 xalign 0.5
                        textbutton "▼" action [SetVariable("digit_code",digit_code[:i]+[(digit_code[i]-1)%10]+digit_code[i+1:]),SetVariable("code_error",False)] xsize 120
            if code_error:
                text "찰칵. 아직 잠겨 있다." size 23 color "#ffbd76"
            else:
                text "월 두 자리, 날 두 자리." size 23 color "#c6b699"
            hbox:
                spacing 30
                textbutton "열기" action (Return("opened") if digit_code == [1,1,0,2] else SetVariable("code_error",True))
                textbutton "뒤로" action Return("cancel")

screen evidence_book(present=False):
    modal True
    zorder 60
    default detail = (inventory[0] if inventory else None)
    default page_index = 0
    add Solid("#100c09d9")
    frame:
        xpos 65 ypos 105 xsize 1150 ysize 535
        fixed:
            text ("증거 제시" if present else "증거 수첩") size 32 color "#ffdc91"
            for i,key in enumerate(inventory[page_index*6:page_index*6+6]):
                button:
                    xpos (i%2)*230 ypos 65+(i//2)*110
                    xsize 220 ysize 100 padding (8,5)
                    action (Return(key) if present else SetScreenVariable("detail",key))
                    vbox:
                        spacing 5
                        add Transform(EVIDENCE[key][2],size=(74,47),fit="contain") xalign 0.5
                        text EVIDENCE[key][0] size 18 xalign 0.5 text_align 0.5 xsize 204
            if detail:
                add Transform(EVIDENCE[detail][2],size=(224,144),fit="contain") xpos 520 ypos 65
                text EVIDENCE[detail][0] xpos 520 ypos 235 color "#ffdc91" size 25
                text evidence_text(detail) xpos 520 ypos 290 size 23 xsize 535
            else:
                text "아직 모은 증거가 없다." xpos 520 ypos 80 size 24
            textbutton "◀":
                xpos 0 ypos 425 xsize 64
                action SetScreenVariable("page_index",page_index-1)
                sensitive page_index>0
            text "[page_index+1] / [max(1,(len(inventory)+5)//6)]" xpos 85 ypos 440 size 23
            textbutton "▶":
                xpos 165 ypos 425 xsize 64
                action SetScreenVariable("page_index",page_index+1)
                sensitive (page_index+1)*6<len(inventory)
            textbutton ("취소" if present else "닫기"):
                xpos 280 ypos 425
                action (Return("cancel") if present else Hide("evidence_book"))

screen round_table():
    zorder -1
    # A resident who steps forward is absent from the distant row for this shot.
    # Evidence overlays and a full-table view retain every resident.
    $ foreground = None
    if source_mode and renpy.get_screen("source_debate") and not renpy.get_screen("source_evidence") and not renpy.get_screen("source_proof"):
        $ debate = SOURCE_EP["MEET" if source_group=="meet" else "FINAL"]["phases"][source_phase]
        $ foreground = SOURCE_ALIAS.get(debate["stms"][source_statement]["w"],debate["stms"][source_statement]["w"])
    elif source_mode and renpy.showing("visitor") and not renpy.get_screen("source_evidence") and not renpy.get_screen("source_proof"):
        $ foreground = source_stage_person
    for key,x,y in (("granny",170,405),("nabi",340,378),("buri",515,370),("doto",710,370),("seryeon",870,405),("neoul",1040,445),("karo",1160,460)):
        if key != foreground:
            add key + " world" at resident_world xpos x ypos y id ("table_"+key)
        # The full-body source is a distant resident, never reused as the close-up.
    if foreground != "bami":
        add Transform("bami world",zoom=0.47) xpos 1120 ypos 83 id "table_bami"
    add r13_asset("file:assets/table.png") at table_world

screen council():
    modal True
    default input_ready = False
    timer 0.3 action SetScreenVariable("input_ready",True)
    add speaker + " neutral" at portrait_close
    frame:
        xpos 30 ypos 135 xsize 625 ysize 325
        vbox:
            spacing 17
            text NAMES[speaker] size 27 color "#ffdc91"
            text council_quote(speaker) size 28 xsize 565
            if meeting_first:
                text "한쪽 흔적만으로는 부족하다. 비교해 보자." size 21 color "#d8b568"
    hbox:
        xpos 54 ypos 390 spacing 16
        textbutton "되묻기" action Return(("press",speaker)) sensitive input_ready
        textbutton "증거" action Return(("evidence",speaker)) sensitive input_ready
    hbox:
        xpos 25 ypos 540 spacing 8
        for key in ("granny","nabi","buri","bami","doto","karo","neoul","seryeon"):
            button:
                xsize 145 ysize 115 padding (7,5)
                background Solid("#765938f5" if key == speaker else "#211b17f5")
                action Return(("speaker",key)) sensitive input_ready
                vbox:
                    spacing 4
                    add Transform(key + " neutral",size=(60,68)) xalign 0.5
                    text NAMES[key] size 21 xalign 0.5
    text "시각: [ '확인' if 'clock' in resolved_topics else '미확인' ]    주머니 접촉: [ '확인' if 'contact' in resolved_topics else '미확인' ]" xpos 30 ypos 677 size 21 color "#d5c29e"
    textbutton "다시 추궁하기":
        xpos 1000 ypos 665 xsize 250 text_size 23
        action Return(("duel",None))
        sensitive input_ready and "clock" in resolved_topics and "contact" in resolved_topics

screen clock_compare():
    modal True
    add Solid("#160f0be8")
    frame:
        xpos 155 ypos 125 xsize 970 ysize 475
        vbox:
            spacing 20
            text "밤이가 본 시계" size 33 color "#ffdc91"
            hbox:
                spacing 80
                fixed:
                    xsize 270 ysize 270
                    add Transform(r13_asset_path("file:assets/clock-base.png"),size=(270,270))
                    add Transform(r13_asset_path("file:assets/clock-hands.png"),size=(270,270),rotate=(180 if clock_rotated else 0),rotate_pad=False)
                vbox:
                    spacing 20 xsize 500
                    text ("거꾸로 매달린 시선" if clock_rotated else "바닥에 선 우리의 시선") size 25
                    text "밤이는 새벽 다섯 시에 잠든다.\n첫눈이 내릴 때 종은 열두 번 울렸다." size 23
                    textbutton "시선을 뒤집기" action [ToggleVariable("clock_rotated"),SetVariable("clock_demonstrated",True)]
                    textbutton "시각을 판단하기" action Return("choose") sensitive clock_demonstrated

screen duel():
    modal True
    default input_ready = False
    timer 0.3 action SetScreenVariable("input_ready",True)
    add "seryeon distressed" at portrait_close
    frame:
        xpos 40 ypos 155 xsize 650
        vbox:
            spacing 22
            text "세련의 반격" size 28 color "#ffbd76"
            if showdown_issue == "place":
                text "침대 밑 상자 뒤에 있던 쥐 때문에\n제 돈 이야기를 피하시는군요." size 29
            elif showdown_issue == "movement":
                text "방엔 갔습니다. 하지만 주머니를\n놓고 왔다고는 안 했어요." size 29
            else:
                text "봉하기 전엔 삼백 냥이었습니다.\n이백 냥은 할머니가 빼낸 거죠." size 29
    hbox:
        xpos 64 ypos 395 spacing 18
        textbutton "되묻기" action Return("press") sensitive input_ready
        textbutton "증거 제시" action Return("evidence") sensitive input_ready

# Options: three tabs (소리 / 화면 / 게임), one page each, no scrolling,
# large touch targets in the game's own panel style (dark green, gold edge).
default persistent.room13_text_small = False
default persistent.room13_window_alpha = "d4"
default persistent.room13_option_tab = "sound"

init python:
    def r13_set_text_size(size):
        persistent.room13_text_small=(size=="small")
        persistent.room13_large_text=(size=="large")
        renpy.save_persistent()
        renpy.restart_interaction()

    def r13_text_size():
        return "large" if persistent.room13_large_text else "small" if persistent.room13_text_small else "normal"

    def r13_toggle_fullscreen():
        # Web only: Android browsers allow it; iOS Safari ignores the request.
        if renpy.emscripten:
            import emscripten
            emscripten.run_script("(function(){var d=document;if(d.fullscreenElement){d.exitFullscreen&&d.exitFullscreen();}else{var e=d.documentElement;(e.requestFullscreen||e.webkitRequestFullscreen||function(){}).call(e);}})();")
        else:
            renpy.run(Preference("display","toggle"))

# The same folio and left index as the records. Settings apply immediately.
init python:
    def r13_opt_size():
        # 0.20.7 (UI review: phone text about 11px): +4 on a touch screen.
        return r13_read_size(22,26)+(4 if globals().get("r13_touch_ui",lambda:False)() else 0)

    def r13_opt_title_size():
        return r13_read_size(30,34)

    def r13_opt_row_height():
        return max(96 if globals().get("r13_touch_ui",lambda:False)() else 76,112 if persistent.room13_large_text else 76)

style r13opt_text is text:
    font r13_ui_font() color "#4b3420" line_spacing 2
# Approved B options artwork; crops remove only the transparent delivery margin.
style r13opt_button is button:
    background r13_sticker_button() hover_background r13_sticker_button(focused=True)
    selected_background r13_sticker_button(primary=True)
    selected_hover_background r13_sticker_button(primary=True,focused=True)
    insensitive_background r13_sticker_button(disabled=True)
    selected_foreground None
    padding (10,4) ysize 52
style r13opt_button variant "touch":
    ysize 88
style r13opt_button_text is text:
    font R13_UI_BOLD_FONT color "#4b3420" hover_color "#4b3420" selected_color "#fff6e2" insensitive_color "#8f8778"
    xalign .5 yalign .5 text_align .5 line_spacing 2
style r13opt_bar is bar:
    ysize 36
    left_bar Frame(Crop((16,8,280,36),r13_asset_path("file:assets/ui-b-options/b_opt_bar_fill.png")),10,0)
    right_bar Frame(Crop((16,8,280,36),r13_asset_path("file:assets/ui-b-options/b_opt_bar_track.png")),10,0)
    thumb Crop((16,16,36,36),r13_asset_path("file:assets/ui-b-options/b_opt_bar_thumb.png")) thumb_offset 0
style r13opt_tab_button is button:
    background None hover_background None selected_background None padding (0,0)
style r13opt_tab_button_text is text:
    font R13_UI_BOLD_FONT color "#4b3420" hover_color "#4b3420" selected_color "#4b3420" xpos 62 yalign .5

style r13opt_footer_button is r13opt_button:
    padding (10,4)
style r13opt_footer_button_text is r13opt_button_text:
    hover_color "#4b3420"
style r13opt_close_button is r13opt_footer_button:
    background r13_sticker_button(primary=True)
    hover_background r13_sticker_button(primary=True,focused=True)
style r13opt_close_button_text is r13opt_footer_button_text:
    color "#fff6e2" hover_color "#fff6e2"

init -1 python:
    def r13_opt_marks():
        # The two small gold diamonds on a chosen option (mockup).
        d=r13_asset_path("file:assets/ui-night/diamond.png")
        return Fixed(Transform(d,xpos=8,yalign=.5),Transform(d,xalign=1.0,xoffset=-8,yalign=.5))

init python:
    # 2026-10-27 소유자: "옵션창 버튼 크기가 뒤죽박죽". 폭을 줄마다 손으로 적어 132~300px 아홉 가지가 섞였다.
    # 시안(승인 전, 꺼짐): 선택 버튼 한 칸 136, 단독 버튼 두 칸(136x2+12), 아래 줄 다섯은 같은 폭 206.
    R13_OPT_UNIFIED = False
    R13_OPT_CELL = 136
    R13_OPT_FOOT = 206
    def r13_opt_w(legacy,cells=1):
        return (R13_OPT_CELL*cells+12*(cells-1)) if R13_OPT_UNIFIED else legacy
    def r13_opt_foot(legacy_x,legacy_w,slot):
        return (112+slot*(R13_OPT_FOOT+12),R13_OPT_FOOT) if R13_OPT_UNIFIED else (legacy_x,legacy_w)

    def r13_opt_button_height():
        # Match the rendered button in both native touch and short browser windows.
        return 88 if r13_touch_ui() else 52

screen r13_opt_row(label,description=""):
    fixed:
        xsize 844 ysize r13_opt_row_height()
        vbox:
            xpos 0 yalign .5 xsize 232 spacing 4
            text label font R13_UI_TYPE["button"]["font"] size (r13_opt_size()+2) color "#4b3420"
            if description:
                text description size (r13_opt_size()-4) color "#765b3e" xsize 232
        hbox:
            xpos 248 ypos ((r13_opt_row_height()-r13_opt_button_height())//2) spacing 12
            transclude
        add Solid("#c9a86a40") xpos 0 ypos (r13_opt_row_height()-1) xsize 844 ysize 1

screen r13_opt_rule(width,y,x=0):
    add Crop((0,0,width,9),r13_asset_path("file:assets/ui-night/gold_rule.png")) xpos x ypos y

screen pause_menu():
    tag menu
    modal True
    zorder 50
    style_prefix "r13opt"
    default typing_preview = R13TypingPreview()
    default tab=(persistent.room13_option_tab if persistent.room13_option_tab in ("sound","screen","reading") else "reading")
    add Solid("#05070fa6")
    # Unscaled full panel: preserve the three rings and all border pixels.
    add r13_asset("file:assets/ui-b-options/b_opt_panel.png") xpos -4 ypos -4
    # Supplied diary stickers: uniform scales, decorative only, clear of controls.
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_gingham_tape.png"),zoom=120.0/464,rotate=-7) xpos 850 ypos 38
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_star.png"),zoom=44.0/368,rotate=10) xpos 1014 ypos 58
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_emphasis.png"),zoom=40.0/432,rotate=12) xpos 1070 ypos 72
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_acorn.png"),zoom=84.0/437,rotate=-9) xpos 116 ypos 410
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_letter.png"),zoom=64.0/408,rotate=8) xpos 216 ypos 406
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_magnifier.png"),zoom=64.0/422,rotate=-10) xpos 216 ypos 460
    # Keep the index clear of the unscaled binder rings.
    add Crop((16,16,150,44),r13_asset_path("file:assets/ui-b-options/b_opt_title_tape.png")) xpos 96 ypos 42
    text "설정" xpos 120 ypos 42 font R13_UI_BOLD_FONT size (r13_opt_title_size()+8) color "#4b3420"
    vbox:
        xpos 96 ypos 136 spacing 0
        for key,name in (("reading","읽기"),("sound","소리"),("screen","화면")):
            fixed:
                xsize 200 ysize (88 if r13_touch_ui() else 76)
                add Frame(Crop((16,16,206,62),r13_asset_path("file:assets/ui-b-options/b_opt_tab_selected.png") if tab==key else r13_asset_path("file:assets/ui-b-options/b_opt_tab.png")),32,20) xpos 0 yalign .5 xysize (200,62)
                add Crop((18,18,28,28),r13_asset_path("file:"+("assets/ui-b-options/b_icon_opt_%s.png"%key))) xpos 28 yalign .5
                textbutton name style "r13opt_tab_button":
                    xsize 200 ysize (88 if r13_touch_ui() else 76) text_size (r13_opt_title_size()-2)
                    text_style "r13opt_tab_button_text"
                    selected tab==key
                    action [SetScreenVariable("tab",key),SetField(persistent,"room13_option_tab",key),Function(renpy.save_persistent)]
    add Solid("#c9a86a66") xpos 305 ypos 56 xsize 1 ysize (472 if r13_touch_ui() else 496)
    text "변경한 설정은 바로 적용됩니다." xpos 347 ypos 52 size (r13_opt_size()-3) color "#765b3e"
    imagebutton:
        idle r13_asset("file:assets/ui-b-options/b_opt_close.png") hover Transform(r13_asset_path("file:assets/ui-b-options/b_opt_close.png"),matrixcolor=BrightnessMatrix(.15))
        xpos 1130 ypos 48 xysize (64,64) padding (0,0) action Return() alt "닫기"
    viewport:
        id "r13_settings_body"
        area (347,92,854,(436 if r13_touch_ui() else 460)) mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
        vbox:
            spacing 0
            if tab=="sound":
                use r13_opt_row("배경음", "음악의 크기"):
                    bar value Preference("music volume") style "r13opt_bar" xsize 280 ysize 36 yalign .5 id "music_volume"
                    text ("%d%%"%r13_mixer_percent("music")) id "music_volume_percent" size r13_opt_size() xsize 64 yalign .5
                    textbutton ("음소거 중" if _preferences.get_mute("music") else "소리 켜짐"):
                        ysize r13_opt_button_height()
                        xsize r13_opt_w(150) selected not _preferences.get_mute("music") action Preference("music mute","toggle") text_size r13_opt_size()
                use r13_opt_row("효과음", "문·버튼·조사 소리"):
                    bar value Preference("sound volume") style "r13opt_bar" xsize 280 ysize 36 yalign .5 id "fx_volume"
                    text ("%d%%"%r13_mixer_percent("sfx")) id "fx_volume_percent" size r13_opt_size() xsize 64 yalign .5
                    textbutton ("음소거 중" if _preferences.get_mute("sfx") else "소리 켜짐"):
                        ysize r13_opt_button_height()
                        xsize r13_opt_w(150) selected not _preferences.get_mute("sfx") action Preference("sound mute","toggle") text_size r13_opt_size()
                use r13_opt_row("대사 타이핑 소리", "글자가 나타날 때 나는 소리"):
                    for value,name in ((True,"켜기"),(False,"끄기")):
                        textbutton name xsize r13_opt_w(150) selected persistent.room13_typing_sound==value action Function(r13_set_option,"room13_typing_sound",value) text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("소리 확인", "효과음 음량을 적용해 재생"):
                    textbutton "효과음 듣기" xsize r13_opt_w(190,2) action Function(r13_test_option_sound) text_size r13_opt_size() ysize r13_opt_button_height()
                    textbutton "음악 출처" xsize r13_opt_w(160,2) action Show("r13_music_credits") text_size r13_opt_size() ysize r13_opt_button_height()
                null height 12
                text "음소거 중이거나 음량이 0%이면 소리가 나지 않습니다." xpos 248 size (r13_opt_size()-3) color "#765b3e"
            elif tab=="reading":
                use r13_opt_row("글자 크기", "대사와 메뉴에 함께 적용"):
                    for key,name in (("small","작게"),("normal","보통"),("large","크게")):
                        textbutton name id ("r13_text_size_"+key) xsize r13_opt_w(176) selected r13_text_size()==key action Function(r13_set_text_size,key) text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("대사 표시 속도", "글자가 나타나는 빠르기"):
                    for speed_title,speed_value in (("느리게",24),("보통",34),("빠르게",55),("즉시",0)):
                        textbutton speed_title id ("r13_text_speed_%d"%speed_value) xsize r13_opt_w(132) action [Preference("text speed",speed_value),Function(typing_preview.restart)] selected _preferences.text_cps==speed_value text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("자동 넘김 대기", "다음 대사까지 대기"):
                    for value,name in ((0,"수동"),(5,"짧게"),(15,"보통"),(25,"길게")):
                        textbutton name xsize r13_opt_w(132) action Preference("auto-forward time",value) selected (_preferences.afm_time==0 if value==0 else (0<_preferences.afm_time<10) if value==5 else (10<=_preferences.afm_time<20) if value==15 else _preferences.afm_time>=20) text_size r13_opt_size() ysize r13_opt_button_height()
                hbox:
                    spacing 12
                    textbutton "다시 보기" id "r13_preview_replay" xsize r13_opt_w(150,2) text_size r13_opt_size() action Function(typing_preview.restart) ysize r13_opt_button_height()
                    frame:
                        xsize (844-12-r13_opt_w(150,2)) ysize 88 padding (18,12) background r13_sticker_button()
                        add typing_preview
            else:
                null height 0
                frame:
                    xsize 824 ysize 76 padding (26,16) background Frame(Crop((16,16,860,110),r13_asset_path("file:assets/ui-b-options/b_opt_preview_box.png")),26,16)
                    text "대사창 미리보기 · 바꾼 진하기가 적용됩니다." font R13_UI_BOLD_FONT size r13_opt_size() color "#4b3420" xsize 772
                use r13_opt_row("대사창 진하기", "배경이 비쳐 보이는 정도"):
                    for value,name in (("99","연하게"),("d4","보통"),("f5","진하게")):
                        textbutton name xsize r13_opt_w(176) selected persistent.room13_window_alpha==value action [SetField(persistent,"room13_window_alpha",value),Function(renpy.save_persistent)] text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("화면 움직임", "눈·불빛·인물의 짧은 반응"):
                    for value,name in ((True,"켜기"),(False,"끄기")):
                        textbutton name xsize r13_opt_w(176) selected persistent.room13_motion==value action Function(r13_set_option,"room13_motion",value) text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("전체 화면", "지원 기기에서 전환"):
                    textbutton "전체 화면 전환" xsize r13_opt_w(300,2) action Function(r13_toggle_fullscreen) text_size r13_opt_size() ysize r13_opt_button_height()
                # 0.18.50 (owner): test tool behind a PIN (systems/room13_admin.rpy).
                use r13_opt_row("관리자 도구", "핀 번호를 넣으면 켜짐"):
                    if persistent.room13_admin:
                        text "켜짐 · 마을 화면 위쪽 ‘관리자’" xsize 330 size r13_opt_size() color "#765b3e" yalign .5
                        textbutton "끄기" xsize r13_opt_w(132) action Function(r13_admin_toggle) text_size r13_opt_size() ysize r13_opt_button_height()
                    else:
                        textbutton "핀 번호로 켜기" xsize r13_opt_w(220,2) action Show("r13_admin_pin") text_size r13_opt_size() ysize r13_opt_button_height()
    text ("v"+config.version) xpos 120 ypos (516 if r13_touch_ui() else 540) size (r13_opt_size()-6) color "#8f8778"
    add Crop((16,16,1080,6),r13_asset_path("file:assets/ui-b-options/b_opt_divider.png")) xpos 112 ypos (536 if r13_touch_ui() else 560)
    textbutton "설정 초기화" style "r13opt_footer_button":
        ysize r13_opt_button_height()
        xpos r13_opt_foot(112,184,0)[0] ypos (552 if r13_touch_ui() else 576) xsize r13_opt_foot(112,184,0)[1] text_size r13_opt_size()
        action Confirm("읽기·소리·화면 설정을 기본값으로 돌릴까요? 게임 진행과 저장은 유지됩니다.",Function(r13_reset_options))
    if not main_menu:
        textbutton "메인화면" style "r13opt_footer_button":
            ysize r13_opt_button_height()
            xpos r13_opt_foot(308,170,1)[0] ypos (552 if r13_touch_ui() else 576) xsize r13_opt_foot(308,170,1)[1] text_size r13_opt_size()
            action Confirm("메인화면으로 돌아가시겠습니까?\n저장하지 않은 게임 진행은 사라집니다.",MainMenu(confirm=False))
    # 0.19.2: 단축키 안내는 「더보기」에서 설정 안으로 옮겼다.
    textbutton "단축키 PC" style "r13opt_footer_button":
        ysize r13_opt_button_height()
        xpos r13_opt_foot(490,170,2)[0] ypos (552 if r13_touch_ui() else 576) xsize r13_opt_foot(490,170,2)[1] text_size r13_opt_size() action Show("r13_shortcut_help")
    # 0.20.3 (owner 2026-10-22: "저장버튼이 어차피 빈번한 게임이 아니니 옵션에 넣어줘도 되고").
    if not main_menu:
        textbutton "저장 · 불러오기" style "r13opt_footer_button":
            ysize r13_opt_button_height()
            xpos r13_opt_foot(672,260,3)[0] ypos (552 if r13_touch_ui() else 576) xsize r13_opt_foot(672,260,3)[1] text_size r13_opt_size() action ShowMenu("save")  # 0.20.7: wider so it stays on one line on a phone
    textbutton "닫기" style "r13opt_close_button":
        ysize r13_opt_button_height()
        xpos r13_opt_foot(1040,150,4)[0] ypos (552 if r13_touch_ui() else 576) xsize r13_opt_foot(1040,150,4)[1] text_size r13_opt_size() action Return()
    key "game_menu" action Return()

screen save():
    tag menu
    zorder 50
    use file_slots("저장",True)

screen load():
    tag menu
    zorder 50
    use file_slots("불러오기",False)

init python:
    # Each save remembers where the story stood, shown on the slot instead of
    # only the real-world clock.
    def r13_save_json(d):
        try:
            if getattr(store,"room13_mode",False) and getattr(store,"room13",None):
                d["r13_where"]=r13_clock()+" · "+R13_PLACES[store.room13["location"]][0]
                # 0.18.46: which point of the story, and the last line shown, so a slot can be
                # told apart from the one saved just before a choice.
                d["r13_stage"]=r13_save_stage()
                d["r13_last"]=r13_save_last_line()
        except Exception:
            pass
    config.save_json_callbacks.append(r13_save_json)

    def r13_save_stage():
        s=store.room13 or {}
        if s.get("ending"):return "결말"
        if s.get("finale_started"):return "14일째 제단"
        goal=r13_campaign_goal() if s.get("day",1)>=2 else None
        return goal or ("재판 뒤" if s.get("trial_ended") else "")

    def r13_save_last_line(limit=34):
        for entry in reversed(getattr(store,"_history_list",[]) or []):
            what=getattr(entry,"what",None)
            if what:
                text=renpy.filter_text_tags(what,allow=[]).replace("\n"," ")
                who=getattr(entry,"who",None)
                text=(who+": "+text) if who else text
                return text if len(text)<=limit else text[:limit-1]+"…"
        return ""

    def r13_slot_info(slot,key):
        return (renpy.slot_json(slot) or {}).get(key,"")

    def r13_load_confirm(slot):
        """Same path for every slot, autosave included: a running game asks before losing progress."""
        load=r13_load_action(slot)
        if main_menu or r13_save_status(renpy.slot_json(slot))!="compatible":return load
        return Confirm("저장하지 않은 진행은 사라진다. 불러올까?",load)

    def r13_slot_where(slot):
        json=renpy.slot_json(slot)
        return (json or {}).get("r13_where","")

    def r13_slot_action(page,number,saving):
        slot="%s-%s"%(page,number)
        if saving:
            save=[FileSave(number,confirm=False,page=str(page)),Function(source_fx,"save")]
            return Confirm("이 칸에는 이미 저장이 있다. 덮어쓸까?",save) if renpy.can_load(slot) else save
        # Compatibility review (r13_load_action) decides how a save opens;
        # in a running game a compatible load also asks before losing progress.
        return r13_load_confirm(slot)

screen file_slots(title,saving):
    modal True
    style_prefix ("r13" if room13_mode or main_menu else "trial")
    default page=persistent.r13_save_page or 1
    add Solid("#0b151bf2" if room13_mode or main_menu else "#110d0af5")
    frame:
        xpos 60 ypos 40 xsize 1160 ysize 640
        vbox:
            spacing 14
            hbox:
                spacing 24
                text title size 34 color ("#765426" if room13_mode or main_menu else "#ffdc91") yalign .5
                for p in (1,2,3):
                    textbutton ("%d쪽"%p):
                        action [SetLocalVariable("page",p),SetField(persistent,"r13_save_page",p)]
                        selected page==p text_size 21 padding (14,6)
                # 0.19.2: 「더보기 → 저장 · 불러오기」 하나로 들어와 여기서 바꾼다.
                if not main_menu:
                    textbutton ("불러오기로 ›" if saving else "저장으로 ›"):
                        action ShowMenu("load" if saving else "save") text_size 21
                if not saving:
                    textbutton "최근 자동저장":
                        action r13_load_confirm("auto-1")
                        sensitive FileLoadable(1,page="auto")
                        text_size 21
            grid 2 3:
                spacing 14
                for i in range(6):
                    $ slot="%d-%d"%(page,i+1)
                    button:
                        xsize 556 ysize 150 padding (10,10)
                        action r13_slot_action(page,i+1,saving)
                        sensitive (saving or renpy.can_load(slot))
                        hbox:
                            spacing 14
                            add FileScreenshot(i+1,page=str(page)) xsize 192 ysize 108 yalign .5
                            # 0.18.46: read the story point first (day, time, place), then where in
                            # the story and the last line; slot number and real time come last.
                            vbox:
                                spacing 3 yalign .5
                                if renpy.can_load(slot):
                                    text (r13_slot_where(slot) or "%d쪽 %d번"%(page,i+1)) size r13_read_size(21,25) color ("#765426" if room13_mode or main_menu else "#ffdc91") xsize 320
                                    if r13_slot_info(slot,"r13_stage"):
                                        text r13_slot_info(slot,"r13_stage") size r13_read_size(17,21) xsize 320
                                    if r13_slot_info(slot,"r13_last"):
                                        text ("“"+r13_slot_info(slot,"r13_last")+"”") size r13_read_size(16,20) color "#5d6a66" xsize 320
                                    text ("%d쪽 %d번 · "%(page,i+1)+FileTime(i+1,format="%m-%d %H:%M",page=str(page))+" · "+r13_save_caption(renpy.slot_json(slot))) size r13_read_size(14,17) color "#7d8c90" xsize 320
                                else:
                                    text ("%d쪽 %d번 · 비어 있음"%(page,i+1)) size r13_read_size(20,24)
            hbox:
                spacing 18
                textbutton "돌아가기" action Return()
                if not saving:
                    textbutton "이전 저장 정리" action Show("r13_save_cleanup",scope="old") text_size 20
                    textbutton "모든 진행 저장 정리" action Show("r13_save_cleanup",scope="all") text_size 20

screen trial_complete():
    modal True
    zorder 50
    add Solid("#120e0aeb")
    frame:
        xpos 140 ypos 180 xsize 1000
        vbox:
            spacing 23
            text "열세 번째 침대" size 44 color "#ffdc91"
            text (SOURCE_EP["THE_END"]["notice"]["text"] if source_mode else "할머니의 누명은 벗겼다.\n하지만 그 침대에서 엄마가 누구를 기다렸는지는 남았다.") size 28
            text ("1장 마을 탐색 시험판 끝" if source_mode else "작은 1장 끝") size 24 color "#c6b699"
            textbutton "다시 플레이" action Start()
            textbutton "처음 화면으로" action MainMenu(confirm=False)

screen notify(message):
    style_prefix ("r13" if room13_mode else "")
    zorder 100
    if room13_mode:
        # One notice spot (0.18.33): top right under the date plate, like the new-record card.
        # The top-left corner holds the place tag; the top centre holds titles and the work button.
        frame:
            xanchor 1.0 xpos 1256 ypos 92 xmaximum 424 padding (18,12)
            background R13ActionPanel()
            text message size 21 color "#fff2d9" xmaximum 388
    else:
        frame:
            xalign 0.5 ypos 98
            text message size 21
    timer 2.2 action Hide("notify")

screen confirm(message,yes_action,no_action):
    style_prefix ("r13" if room13_mode else "")
    modal True
    zorder 100
    add Solid("#000000bb")
    frame:
        xalign 0.5 yalign 0.5 xsize 900
        vbox:
            spacing 20
            text message
            hbox:
                spacing 30
                textbutton "예" action yes_action
                textbutton "아니요" action no_action

style trial_frame is frame
style trial_button is button
style trial_button_text is button_text
style trial_bar is bar
style trial_slider is slider
