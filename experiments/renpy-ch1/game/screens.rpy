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
    add Transform("assets/room13-title-winter020.webp",size=(1280,720))
    add R13TitleSnow()
    add R13TitleVeil()
    text "첫 번째 이야기" xpos 94 ypos 108 font r13_ui_font() size 22 color R13_UI_COLORS["menu_secondary"]
    text "다람탐정" xpos 84 ypos 150 font r13_ui_font() size 110 color R13_UI_COLORS["menu_text"] outlines []
    add Solid(R13_UI_COLORS["menu_accent"],xsize=72,ysize=2) xpos 96 ypos 284
    text "눈 아래의 열세 번째 방" xpos 94 ypos 309 font r13_ui_font() size 22 color R13_UI_COLORS["menu_text"]
    vbox:
        xpos 76 ypos 384 spacing 6
        textbutton "이어하기":
            style ("r13_title_primary" if title_continue else "r13_title_button")
            sensitive title_continue is not None
            default_focus title_continue is not None
            action (r13_load_action(title_continue) if title_continue else NullAction())
        textbutton "처음부터":
            style ("r13_title_button" if title_continue else "r13_title_primary")
            default_focus title_continue is None
            action Start()
        textbutton "불러오기" style "r13_title_button" action ShowMenu("load") sensitive title_has_save
        textbutton "설정" style "r13_title_button" action ShowMenu("pause_menu")
    text ("저장된 여정을 이어갑니다" if title_continue else "이전 저장은 불러오기에서 확인하세요" if title_has_save else "눈에 갇힌 마을에서, 사라진 가족의 흔적을 따라.") xpos 110 ypos 650 font r13_ui_font() size 18 color R13_UI_COLORS["menu_secondary"] xsize 490
    hbox:
        xpos 922 ypos 644 spacing 20
        textbutton "음악 듣기" style "r13_title_aux" action Function(r13_title_music)
        textbutton "그림 수첩" style "r13_title_aux" action OpenURL("https://kkhkkh20-bit.github.io/daaegame/preview/room13-acting/")

screen say(who,what):
    if room13_mode:
        key "K_h" action Show("r13_backlog")
    $ has_portrait = not room13_mode and dialogue_speaker in CAST
    window:
        id "window"
        xalign .5 ypos (454 if room13_mode and persistent.room13_large_text else 506 if room13_mode else 551) xsize (1280 if room13_mode else 1200) ysize (226 if room13_mode and persistent.room13_large_text else 174 if room13_mode else 169)
        background (Solid("#14272b"+(persistent.room13_window_alpha or "d4")) if room13_mode else Solid("#10262de8" if winter_mode else "#211a16f2"))
        padding (0,0)
        fixed:
            if not room13_mode:
                add Solid("#b39060",xsize=1200,ysize=2)
            vbox:
                xpos (220 if room13_mode else 240 if has_portrait else 32) ypos 18
                spacing 10
                if who and not room13_mode:
                    text who id "who" color "#ebcd8a" font (r13_ui_font() if room13_mode else "assets/Galmuri11.ttf")
                if room13_mode:
                    r13_dialogue_text what id "what" style "say_dialogue" size r13_read_size(26,32) line_spacing 7 xsize 930 text_align .0 font r13_ui_font() color ("#9dc9ff" if r13_thought_active else "#fff5df")
                else:
                    text what id "what" xsize (910 if has_portrait else 1120) font "assets/Galmuri11.ttf" color "#fff5df"
    if who and room13_mode:
        frame:
            xpos 108 xanchor 0.0 ypos (424 if persistent.room13_large_text else 476) padding R13_UI_PADDING["name"]
            background R13ActionPanel()
            text who id "who" color "#ffe39a" font r13_ui_font() size r13_read_size(21,26)
    # No speaker profile beside the dialogue (owner's decision); the person is on stage.
    if has_portrait:
        frame:
            id "dialogue_portrait_frame"
            xpos 59 ypos 492 xsize 202 ysize 210
            padding (3,3) background Solid("#b39060")
            fixed:
                add Solid("#30261f")
                add Transform(dialogue_speaker + " avatar_"+dialogue_expression,size=(196,204),fit="contain") id "dialogue_portrait"
    text "▸" xpos (1190 if room13_mode else 1190) ypos (610 if room13_mode else 682) size 30 color "#e8c75c"
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
    if room13_mode:
        on "show" action Function(r13_choice_layout,choice_actor,choice_pose,True)
        on "hide" action Function(r13_choice_layout,choice_actor,choice_pose,False)
        $ choice_entries=[(item.caption,item.action,False) for item in items]
        use r13_question_list(choice_actor,choice_pose,"선택",choice_entries,choice_ready,actor_x=272,list_left=(500 if choice_actor else 190),list_width=(744 if choice_actor else 940),animate=False)
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

style r13opt_text is text:
    font r13_ui_font()
    color R13_UI_COLORS["menu_text"]
style r13opt_button is button:
    background R13ActionPanel() hover_background R13ActionPanel(True) selected_background R13ActionPanel(True)
    insensitive_background R13ActionPanel(disabled=True)
    padding (12,8) ysize 56
style r13opt_button_text is text:
    font r13_ui_font() color R13_UI_COLORS["menu_text"] hover_color R13_UI_COLORS["menu_accent"] selected_color R13_UI_COLORS["menu_accent"] insensitive_color R13_UI_COLORS["menu_disabled"]
    xalign .5 yalign .5 text_align .5
style r13opt_bar is bar:
    ysize 40
    left_bar Solid(R13_UI_COLORS["menu_accent"],ysize=40) right_bar Solid("#0d1d1f",ysize=40)
    thumb Solid(R13_UI_COLORS["menu_text"],xsize=22,ysize=40) thumb_offset 11

screen r13_opt_row(label):
    hbox:
        spacing 16
        fixed:
            xsize 300 ysize 56
            text label size r13_read_size(22,26) yalign .5
        hbox:
            spacing 10 yalign .5
            transclude

screen pause_menu():
    tag menu
    modal True
    zorder 50
    style_prefix "r13opt"
    default tab=persistent.room13_option_tab or "sound"
    add Solid("#0b151bf2")
    frame:
        area (80,24,1120,672) background Solid("#0f2123f4") padding (30,18)
        vbox:
            spacing 16
            fixed:
                xsize 1060 ysize 56
                text "옵션" size r13_read_size(32,38) color R13_UI_COLORS["menu_accent"] yalign .5
                hbox:
                    xpos 170 yalign .5 spacing 10
                    for key,name in (("sound","소리"),("screen","화면"),("game","게임")):
                        textbutton name xsize 150 selected tab==key action [SetScreenVariable("tab",key),SetField(persistent,"room13_option_tab",key)] text_size r13_read_size(22,26)
                textbutton "돌아가기" xsize 170 xalign 1.0 action Return() text_size r13_read_size(22,26)
            frame:
                background Solid("#14272b") padding (34,26) xsize 1060 ysize 470
                vbox:
                    spacing (10 if tab=="game" else 18)
                    if tab=="sound":
                        use r13_opt_row("배경음"):
                            bar value Preference("music volume") style "r13opt_bar" xsize 440 ysize 40 yalign .5 id "music_volume"
                            textbutton ("꺼짐" if _preferences.get_mute("music") else "켜짐") xsize 150 selected not _preferences.get_mute("music") action Preference("music mute","toggle") text_size r13_read_size(20,24)
                        use r13_opt_row("효과음"):
                            bar value Preference("sound volume") style "r13opt_bar" xsize 440 ysize 40 yalign .5 id "fx_volume"
                            textbutton ("꺼짐" if _preferences.get_mute("sfx") else "켜짐") xsize 150 selected not _preferences.get_mute("sfx") action Preference("sound mute","toggle") text_size r13_read_size(20,24)
                        use r13_opt_row("대사 타이핑 소리"):
                            textbutton ("켜짐" if persistent.room13_typing_sound else "꺼짐") xsize 150 selected persistent.room13_typing_sound action Function(r13_set_option,"room13_typing_sound",not persistent.room13_typing_sound) text_size r13_read_size(20,24)
                            text "문이 열리는 소리 등 효과음은 유지합니다." size r13_read_size(17,20) color R13_UI_COLORS["menu_secondary"] yalign .5
                        use r13_opt_row("소리 확인"):
                            textbutton "효과음 듣기" xsize 200 action Function(r13_test_option_sound) text_size r13_read_size(20,24)
                        use r13_opt_row("음악 출처"):
                            textbutton "보기" xsize 150 action Show("r13_music_credits") text_size r13_read_size(20,24)
                            text "배경음은 CC BY 4.0, 효과음은 CC0입니다." size r13_read_size(17,20) color R13_UI_COLORS["menu_secondary"] yalign .5
                        text "음량 0 또는 꺼짐이면 소리가 나지 않습니다." size r13_read_size(18,21) color R13_UI_COLORS["menu_secondary"]
                    elif tab=="screen":
                        use r13_opt_row("글자 크기"):
                            for key,name in (("small","작게"),("normal","보통"),("large","크게")):
                                textbutton name xsize 150 selected r13_text_size()==key action Function(r13_set_text_size,key) text_size r13_read_size(20,24)
                        use r13_opt_row("대사창 진하기"):
                            for value,name in (("99","연하게"),("d4","보통"),("f5","진하게")):
                                textbutton name xsize 150 selected persistent.room13_window_alpha==value action [SetField(persistent,"room13_window_alpha",value),Function(renpy.save_persistent)] text_size r13_read_size(20,24)
                        use r13_opt_row("화면 움직임"):
                            textbutton ("켜짐" if persistent.room13_motion else "꺼짐") xsize 150 selected persistent.room13_motion action Function(r13_set_option,"room13_motion",not persistent.room13_motion) text_size r13_read_size(20,24)
                        use r13_opt_row("전체 화면"):
                            textbutton "전환" xsize 150 action Function(r13_toggle_fullscreen) text_size r13_read_size(20,24)
                            text "안드로이드 브라우저에서 동작합니다." size r13_read_size(17,20) color R13_UI_COLORS["menu_secondary"] yalign .5
                        frame:
                            xsize 990 ysize 90 padding (18,12) background Solid("#b9ae93")
                            frame:
                                xfill True yfill True padding (16,8) background Solid("#14272b" + persistent.room13_window_alpha)
                                text "기록과 증언을 천천히 비교해 보자." size r13_read_size(24,30) color R13_UI_COLORS["menu_text"] yalign .5
                    else:
                        use r13_opt_row("대사가 나오는 속도"):
                            for speed_title,speed_value in (("느리게",24),("보통",34),("빠르게",55),("즉시",0)):
                                textbutton speed_title xsize 130 action Preference("text speed",speed_value) selected _preferences.text_cps==speed_value text_size r13_read_size(20,24)
                        use r13_opt_row("자동 진행 속도"):
                            vbox:
                                bar value Preference("auto-forward time") style "r13opt_bar" xsize 560 ysize 40 id "afm_time"
                                fixed:
                                    xsize 560 ysize 22
                                    text "빠르게" size r13_read_size(16,19) color R13_UI_COLORS["menu_secondary"]
                                    text "느리게" size r13_read_size(16,19) color R13_UI_COLORS["menu_secondary"] xalign 1.0
                        use r13_opt_row("저장 정리"):
                            textbutton "이전 저장 정리" xsize 220 action Show("r13_save_cleanup",scope="old") text_size r13_read_size(20,24)
                            textbutton "모든 진행 저장 정리" xsize 260 action Show("r13_save_cleanup",scope="all") text_size r13_read_size(20,24)
            hbox:
                spacing 14
                textbutton "옵션 초기화" xsize 180 action Confirm("소리·화면·읽기 설정을 기본값으로 돌릴까요? 진행 저장과 발견·결말 기록은 유지됩니다.",Function(r13_reset_options)) text_size r13_read_size(20,24)
                text "[config.version] · 자동 저장" size 16 color R13_UI_COLORS["menu_secondary"] xsize 190 yalign .5
                if not main_menu:
                    textbutton "저장" xsize 200 action ShowMenu("save") text_size r13_read_size(22,26)
                    textbutton "불러오기" xsize 200 action ShowMenu("load") text_size r13_read_size(22,26)
                    textbutton "처음 화면" xsize 200 action Confirm("저장하지 않은 진행은 사라진다. 처음 화면으로 갈까?",MainMenu(confirm=False)) text_size r13_read_size(22,26)
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
        except Exception:
            pass
    config.save_json_callbacks.append(r13_save_json)

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
        load=r13_load_action(slot)
        if main_menu or r13_save_status(renpy.slot_json(slot))!="compatible":return load
        return Confirm("저장하지 않은 진행은 사라진다. 불러올까?",load)

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
                if not saving:
                    textbutton "최근 자동저장":
                        action r13_load_action("auto-1")
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
                            vbox:
                                spacing 4 yalign .5
                                text ("%d쪽 %d번"%(page,i+1)) size 20 color ("#765426" if room13_mode or main_menu else "#ffdc91")
                                if renpy.can_load(slot):
                                    text r13_slot_where(slot) size 19 xsize 320
                                    text r13_save_caption(renpy.slot_json(slot)) size 15 color "#7d8c90" xsize 320
                                    text FileTime(i+1,format="%Y-%m-%d %H:%M",page=str(page)) size 15 color "#7d8c90"
                                else:
                                    text "비어 있음" size 20
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
        frame:
            xpos 24 ypos 24 xmaximum 760 padding (18,12)
            background R13ActionPanel()
            text message size 21 color "#fff2d9" xmaximum 716
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
