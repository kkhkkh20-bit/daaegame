style default:
    font "assets/Galmuri11.ttf"
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
    add Transform("assets/room13-title-winter020.webp",size=(1280,720),nearest=False)
    add r13_title_fx()
    add r13_title_menu_shade()
    hbox:
        xpos 62 ypos 584 spacing 5
        at r13_title_menu_in
        textbutton "이어하기":
            style "r13_title_button" selected title_focus=="continue"
            sensitive title_continue is not None
            default_focus title_continue is not None hovered SetScreenVariable("title_focus","continue")
            action (r13_load_action(title_continue) if title_continue is not None else NullAction())
        add Solid("#b6bbcb70",xsize=1,ysize=39) yalign .35
        textbutton "처음부터":
            style "r13_title_button" selected title_focus=="new"
            default_focus title_continue is None hovered SetScreenVariable("title_focus","new") action Start()
        add Solid("#b6bbcb70",xsize=1,ysize=39) yalign .35
        textbutton "불러오기":
            style "r13_title_button" selected title_focus=="load"
            sensitive title_has_save
            hovered SetScreenVariable("title_focus","load") action ShowMenu("load")
        add Solid("#b6bbcb70",xsize=1,ysize=39) yalign .35
        textbutton "설정":
            style "r13_title_button" selected title_focus=="settings"
            hovered SetScreenVariable("title_focus","settings") action ShowMenu("pause_menu")
    textbutton "음악 출처":
        xpos 28 ypos 680 padding (8,5) background None
        text_font "assets/Room13TitleSerif.otf" text_size 14 text_color "#c5c6d2" text_hover_color "#fff0ce"
        action Show("r13_music_credits")
    text config.version xpos 1172 ypos 674 font r13_ui_font() size 13 color "#b2b8b8"

# Top of the two-line dialogue window (bottom edge 632): 23px text + padding, or 29px large text.
define R13_SAY_TOP_NORMAL = 532
define R13_SAY_TOP_LARGE = 516
init python:
    def _r13_say_top(what=None):
        # 0.18.93: conversations show two lines per click (systems/room13_linebreak.rpy), but a line
        # spoken outside r13_lines (an old-save notice, a QA line) can wrap to three or more; the
        # window then grows upward by whole lines so the last line never runs past the frame.
        large=bool(persistent.room13_large_text)
        top=R13_SAY_TOP_LARGE if large else R13_SAY_TOP_NORMAL
        lines=_r13_say_lines(what,29 if large else 23) if isinstance(what,str) else 1
        if lines>2:
            top-=(lines-2)*(34 if large else 28)
        return max(300,top)

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
    if room13_mode and r13_meeting_active and r13_meeting_claim in R13_DEBATE:
        use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
        use r13_meeting_chrome(r13_meeting_claim)
        window:
            id "window"
            area (80,500,1120,132) background R13PaperFrame() padding (22,36,22,14)
            r13_dialogue_text what id "what" style "say_dialogue" size r13_read_size(23,29) line_spacing 5 xsize 1076 font r13_ui_font() color r13_say_color()
        if who:
            text who id "who" xpos 104 ypos 510 size r13_read_size(18,22) color "#795d40"
        text "▸" xpos 1160 ypos 600 size 24 color "#795d40"
        timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
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
                        text who id "who" color "#ebcd8a" font (r13_ui_font() if room13_mode else "assets/Galmuri11.ttf")
                    if room13_mode:
                        r13_dialogue_text what id "what" style "say_dialogue" size r13_read_size(26,32) line_spacing 7 xsize 930 text_align .0 font r13_ui_font() color r13_say_color()
                    else:
                        text what id "what" xsize (910 if has_portrait else 1120) font "assets/Galmuri11.ttf" color "#fff5df"
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
            if place != "마차 안" and not r13_cg_active:
                use r13_toolbar(mode="line")
            else:
                use r13_playback_footer()
    else:
        if room13_mode:
            key "K_h" action Show("r13_backlog")
        window:
            id "window"
            # 0.18.39 (owner): two lines tall in both text sizes; the bottom edge stays at 632.
            xpos (240 if room13_mode else 40)
            ypos (_r13_say_top(what) if room13_mode else 551)
            xsize (800 if room13_mode else 1200)
            ysize (632-_r13_say_top(what) if room13_mode else 169)
            background (r13_dialogue_frame() if room13_mode else Solid("#211a16f2")) padding (22,16)
            if room13_mode:
                r13_dialogue_text what id "what" style "say_dialogue" size r13_read_size(23,29) line_spacing 5 xsize 756 font r13_ui_font() color r13_say_color()
            else:
                text what id "what" xsize 1120 font "assets/Galmuri11.ttf" color "#fff5df"
        if who:
            $ r13_name_track(who)
            frame:
                xpos 254 ypos (_r13_say_top(what)-22 if room13_mode else 522)
                padding (14,5) background R13InkPanel(alpha="ff")
                at r13_name_fade
                text who id "who" color R13_SPEAKER_COLOR font r13_ui_font() size 18
        # Next-line mark breathes slowly like a firefly (0.18.47 storybook tone).
        if r13_fx_active():
            text "▸" xpos 1002 ypos 600 size 24 color "#d9d4ab" at r13_next_glow
        else:
            text "▸" xpos 1002 ypos 600 size 24 color "#d9d4ab"
        if room13_mode:
            timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
            if place != "마차 안" and not r13_cg_active:
                use r13_toolbar(mode="line")
            else:
                use r13_playback_footer()

style legacy_choice_frame is frame
style legacy_choice_vbox is vbox
style legacy_choice_button is button
style legacy_choice_button_text is button_text:
    font "assets/Galmuri11.ttf"

screen choice(items):
    style_prefix ("r13" if room13_mode else "legacy_choice")
    modal True
    default choice_ready = not winter_mode
    timer .35 action SetScreenVariable("choice_ready", True)
    # Talking with someone: the person stands on the left and the choices sit on
    # the right, like the question screen (owner, 0.18.6).
    default choice_visitor = room13_mode and "r13_visitor" in renpy.get_showing_tags()
    default choice_actor = (r13_motion_person if choice_visitor else (r13_last_partner if room13_mode and r13_last_partner in CAST else None))
    default choice_pose = (r13_current_pose if choice_visitor else "interview_neutral") if room13_mode else "neutral"
    if room13_mode and r13_meeting_active:
        use r13_meeting_choices(items,choice_ready)
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
            idle Transform("assets/evidence.png",size=(52,52))
            hover Transform("assets/evidence.png",size=(52,52),alpha=0.75)
            action If(source_mode,Show("source_evidence"),Show("evidence_book"))
            tooltip "수첩"
        imagebutton:
            xsize 82 ysize 74 padding (15,11)
            background None hover_background None
            idle Transform("assets/save.png",size=(52,52))
            hover Transform("assets/save.png",size=(52,52),alpha=0.75)
            action ShowMenu("save")
            tooltip "저장"
        imagebutton:
            xsize 82 ysize 74 padding (15,11)
            background None hover_background None
            idle Transform("assets/menu.png",size=(52,52))
            hover Transform("assets/menu.png",size=(52,52),alpha=0.75)
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
        add Transform("assets/pouch-world.png",size=(60,64)) xpos 880 ypos 270
        add Transform("assets/flour-world.png",size=(64,53)) xpos 590 ypos 337
        if archive_open:
            add Transform(Crop((832,565,404,164),"assets/chest-open.png"),size=(150,80)) xpos 659 ypos 425
        else:
            add Transform(Crop((880,550,365,150),"assets/chest.png"),size=(150,62)) xpos 659 ypos 443
        if lamp_ready and not somsom_found:
            add Transform(Crop((802,490,110,80),"assets/somsom.png"),size=(27,19),alpha=0.23) xpos 828 ypos 480
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
            add Transform("assets/clock-base.png",size=(115,115)) xpos 410 ypos 170
            add Transform("assets/clock-hands.png",size=(115,115)) xpos 410 ypos 170
            button:
                xpos 405 ypos 165 xsize 125 ysize 125
                background None hover_background None insensitive_background None padding (0,0)
                action Return("clock") sensitive input_ready
        if location == "doto":
            add Transform("assets/notebook.png",size=(128,83)) xpos 850 ypos 324
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
            idle Transform("assets/move.png",size=(64,64))
            action Return("map") sensitive input_ready
            tooltip "이동"
        if location != "room":
            imagebutton:
                idle Transform("assets/talk.png",size=(64,64))
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
    add Transform("assets/map.png",size=(1280,720))
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
                add Transform("assets/move.png",size=(36,36))
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
    add "assets/table.png" at table_world

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
                    add Transform("assets/clock-base.png",size=(270,270))
                    add Transform("assets/clock-hands.png",size=(270,270),rotate=(180 if clock_rotated else 0),rotate_pad=False)
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
style r13opt_text is text:
    font r13_ui_font() color "#493b30"
style r13opt_button is button:
    background R13PaperFrame() hover_background R13InkPanel(focused=True) selected_background R13InkPanel(focused=True)
    insensitive_background R13InkPanel(disabled=True)
    padding (10,8) ysize 56
style r13opt_button_text is text:
    font r13_ui_font() color "#65503b" hover_color "#fff0ce" selected_color "#fff0ce" insensitive_color "#9b917e"
    xalign .5 yalign .5 text_align .5
style r13opt_bar is bar:
    ysize 40
    left_bar Solid("#ad8550",ysize=40) right_bar Solid("#d0b88e",ysize=40)
    thumb Solid("#574331",xsize=22,ysize=40) thumb_offset 11

screen r13_opt_row(label,description=""):
    fixed:
        xsize 904 ysize 102
        vbox:
            xpos 0 ypos 12 xsize 250 spacing 8
            text label size r13_read_size(22,26) color "#493b30"
            if description:
                text description size r13_read_size(16,18) color "#796a52" xsize 250
        hbox:
            xpos 270 ypos 18 spacing 8
            transclude
        add Solid("#b99b7560") xpos 0 ypos 100 xsize 904 ysize 1

screen pause_menu():
    tag menu
    modal True
    zorder 50
    style_prefix "r13opt"
    default tab=(persistent.room13_option_tab if persistent.room13_option_tab in ("sound","screen","reading") else "reading")
    add Solid("#211b18b8")
    add R13TravelSheet() xpos 12 ypos 8 xsize 1256 ysize 704
    text "설정" xpos 50 ypos 48 size 32 color "#493b30"
    text "변경한 설정은 바로 적용됩니다." xpos 292 ypos 52 size 22 color "#65503b"
    vbox:
        xpos 44 ypos 132 spacing 14
        for key,name in (("reading","읽기"),("sound","소리"),("screen","화면")):
            textbutton name:
                xsize 184 ysize 62 text_size r13_read_size(23,27)
                selected tab==key
                action [SetScreenVariable("tab",key),SetField(persistent,"room13_option_tab",key),Function(renpy.save_persistent)]
    fixed:
        xpos 292 ypos 124 xsize 914 ysize 484
        vbox:
            spacing 0
            if tab=="sound":
                use r13_opt_row("배경음", "음악의 크기"):
                    bar value Preference("music volume") style "r13opt_bar" xsize 300 ysize 48 id "music_volume"
                    text ("%d%%"%round(_preferences.get_volume("music")*100)) size 22 xsize 70 yalign .5
                    textbutton ("음소거 중" if _preferences.get_mute("music") else "소리 켜짐"):
                        xsize 164 selected not _preferences.get_mute("music") action Preference("music mute","toggle") text_size 21
                use r13_opt_row("효과음", "문·버튼·조사 소리"):
                    bar value Preference("sound volume") style "r13opt_bar" xsize 300 ysize 48 id "fx_volume"
                    text ("%d%%"%round(_preferences.get_volume("sfx")*100)) size 22 xsize 70 yalign .5
                    textbutton ("음소거 중" if _preferences.get_mute("sfx") else "소리 켜짐"):
                        xsize 164 selected not _preferences.get_mute("sfx") action Preference("sound mute","toggle") text_size 21
                use r13_opt_row("대사 타이핑 소리", "글자가 나타날 때 나는 소리"):
                    for value,name in ((True,"켜기"),(False,"끄기")):
                        textbutton name xsize 164 selected persistent.room13_typing_sound==value action Function(r13_set_option,"room13_typing_sound",value) text_size 22
                use r13_opt_row("소리 확인", "효과음 음량을 적용해 재생"):
                    textbutton "효과음 듣기" xsize 224 action Function(r13_test_option_sound) text_size 22
                    textbutton "음악 출처" xsize 180 action Show("r13_music_credits") text_size 22
                text "음소거 중이거나 음량이 0%이면 소리가 나지 않습니다." size 18 color "#796a52"
            elif tab=="reading":
                use r13_opt_row("글자 크기", "대사와 메뉴에 함께 적용"):
                    for key,name in (("small","작게"),("normal","보통"),("large","크게")):
                        textbutton name xsize 164 selected r13_text_size()==key action Function(r13_set_text_size,key) text_size 22
                use r13_opt_row("대사 표시 속도", "글자가 나타나는 빠르기"):
                    for speed_title,speed_value in (("느리게",24),("보통",34),("빠르게",55),("즉시",0)):
                        textbutton speed_title xsize 132 action Preference("text speed",speed_value) selected _preferences.text_cps==speed_value text_size 22
                use r13_opt_row("자동 넘김 대기", "자동 재생 중 다음 대사까지"):
                    for value,name in ((0,"수동"),(5,"짧게"),(15,"보통"),(25,"길게")):
                        textbutton name xsize 132 action Preference("auto-forward time",value) selected (_preferences.afm_time==0 if value==0 else (0<_preferences.afm_time<10) if value==5 else (10<=_preferences.afm_time<20) if value==15 else _preferences.afm_time>=20) text_size 22
                text "자동 재생은 대화 중 하단의 ‘자동’에서 켜고 끕니다." size 18 color "#796a52"
                frame:
                    xsize 904 ysize 116 padding (18,14) background r13_dialogue_frame()
                    text "창밖에는 눈이 내리고 있다.\n아직 확인하지 못한 이야기가 남아 있다." size r13_read_size(24,30) color "#efe2c2" xsize 860
            else:
                use r13_opt_row("대사창 진하기", "배경이 비쳐 보이는 정도"):
                    for value,name in (("99","연하게"),("d4","보통"),("f5","진하게")):
                        textbutton name xsize 164 selected persistent.room13_window_alpha==value action [SetField(persistent,"room13_window_alpha",value),Function(renpy.save_persistent)] text_size 22
                use r13_opt_row("화면 움직임", "눈·불빛·인물의 짧은 반응"):
                    for value,name in ((True,"켜기"),(False,"끄기")):
                        textbutton name xsize 164 selected persistent.room13_motion==value action Function(r13_set_option,"room13_motion",value) text_size 22
                use r13_opt_row("전체 화면", "기기·브라우저 지원 시 전환"):
                    textbutton "전체 화면 전환" xsize 300 action Function(r13_toggle_fullscreen) text_size 22
                # 0.18.50 (owner): test tool behind a PIN (systems/room13_admin.rpy).
                use r13_opt_row("관리자 도구", "핀 번호를 넣으면 켜짐"):
                    if persistent.room13_admin:
                        text "켜짐 · 마을 화면 위쪽 ‘관리자’" size 20 color "#796a52" yalign .5
                        textbutton "끄기" xsize 132 action Function(r13_admin_toggle) text_size 22
                    else:
                        textbutton "핀 번호로 켜기" xsize 224 action Show("r13_admin_pin") text_size 22
                frame:
                    xsize 904 ysize 116 padding (18,14) background r13_dialogue_frame()
                    text "대사창 미리보기\n바꾼 진하기가 바로 적용됩니다." size r13_read_size(24,30) color "#efe2c2" xsize 860
    text ("v"+config.version) xpos 54 ypos 594 size 16 color "#796a52"
    textbutton "설정 초기화":
        xpos 44 ypos 630 xsize 184 ysize 56 text_size 21
        action Confirm("읽기·소리·화면 설정을 기본값으로 돌릴까요? 게임 진행과 저장은 유지됩니다.",Function(r13_reset_options))
    # 0.19.2: 단축키 안내는 「더보기」에서 설정 안으로 옮겼다.
    textbutton "단축키 (PC)":
        xpos 532 ypos 630 xsize 200 ysize 56 text_size 21 action Show("r13_shortcut_help")
    if not main_menu:
        textbutton "메인화면":
            xpos 292 ypos 630 xsize 220 ysize 56 text_size 22
            action Confirm("메인화면으로 돌아가시겠습니까?\n저장하지 않은 게임 진행은 사라집니다.",MainMenu(confirm=False))
    textbutton "닫기":
        xpos 976 ypos 630 xsize 230 ysize 56 text_size 24 action Return()
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
