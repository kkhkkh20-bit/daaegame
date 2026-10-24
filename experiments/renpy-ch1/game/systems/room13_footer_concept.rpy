# Shared dialogue dock and playback tools — approved Pretendard Regular design.
init 80 python:
    R13_CONCEPT_RIGHT=1232
screen r13_concept_action(x,w,caption,icon,command,enabled=True,primary=False):
    button:
        area (x,r13_control_y(),w,r13_control_height()) padding (0,0)
        background None hover_background None
        action command sensitive enabled alt caption
        fixed:
            xysize (w,56) align (.5,.5)
            add R13ControlSurface(primary=primary,disabled=not enabled)
            hbox:
                align (.5,.5) spacing 8
                if icon:
                    add R13AntiqueIcon(icon,size=20) yalign .5
                text caption size 22 color ("#fff4df" if enabled else "#a79c8c") font r13_ui_font() yalign .5

screen r13_concept_dock(ready=True,show_record=True,person=None,present_action=None,reserve_return=False):
    $ secondary_width=160
    $ more_x=R13_CONCEPT_RIGHT-secondary_width-(248 if reserve_return else 0)
    $ record_x=more_x-16-secondary_width
    $ line_active=renpy.get_screen("say") is not None and not any(renpy.get_screen(n) for n in ("choice","r13_topics","r13_resident_approach","r13_entry_topics","r13_entry_karo_topics"))
    if line_active:
        use r13_concept_action((record_x if not show_record else record_x-16-secondary_width),secondary_width,"건너뛰기","skip",([SetVariable("r13_carriage_skip",True),Function(renpy.end_interaction,True)] if place=="마차 안" else [SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)]),enabled=ready)
    if present_action is not None:
        use r13_concept_action(record_x-16-256,256,"자료 보여주기","present",present_action,enabled=ready,primary=True)
    if show_record:
        use r13_concept_action(record_x,secondary_width,"기록","record",Show("r13_records",target=person,present_action=present_action),enabled=ready)
    use r13_concept_action(more_x,secondary_width,"더보기","settings",Show("r13_more_tools"),enabled=ready)
    if _preferences.afm_enable and renpy.get_screen("say") is not None and not any(renpy.get_screen(n) for n in ("choice","r13_topics","r13_resident_approach","r13_entry_topics","r13_entry_karo_topics")):
        use r13_concept_action(28,280,"자동 읽기 중 · 정지",None,Preference("auto-forward","disable"),enabled=ready)

screen r13_concept_more():
    modal True
    zorder 105
    on "show" action Function(r13_end_skip_modes)
    $ active=renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    $ items=[("대화 기록","backlog",[Hide("r13_more_tools"),Show("r13_backlog")],True),
        ("자료 기록","record",[Hide("r13_more_tools"),Show("r13_records")],True),
        ("자동 읽기","auto",[Hide("r13_more_tools"),Preference("auto-forward","toggle")],active),
        ("읽은 대사 빠르게","skip",[Hide("r13_more_tools"),Function(r13_toggle_read_skip)],active),
        ("저장 · 불러오기","record",[Hide("r13_more_tools"),ShowMenu("save")],True),
        ("설정","settings",[Hide("r13_more_tools"),ShowMenu("pause_menu")],True),
        ("대화창 숨기기","dialogue",[Hide("r13_more_tools"),HideInterface()],active),
        ("다시 시작할 아침","auto",[Hide("r13_more_tools"),Show("r13_morning_pick")],bool(r13_morning_days())),
        ("메인화면","place_inn",[Hide("r13_more_tools"),Confirm("메인화면으로 돌아가시겠습니까?\n저장하지 않은 게임 진행은 사라집니다.",MainMenu(confirm=False))],True)]
    button:
        area (0,0,1280,720) background None action Hide("r13_more_tools") alt "닫기"
    $ row_height=88 if r13_touch_ui() else 64
    $ menu_rows=(len(items)+1)//2
    $ panel_height=menu_rows*(row_height+16)+74
    # 0.19.98 (owner settings mockup): the same night panel and gold-edged buttons as 설정.
    frame:
        xpos 584 ypos (min(r13_control_y(),R13_NIGHT_CONTROL_Y-28)-panel_height-16) xysize (648,panel_height) padding (28,22) background Frame("assets/ui-night/panel.png",48,48)
        vbox:
            spacing 16
            text "대화 도구" size (28 if r13_touch_ui() else 24) color "#f6ecd8" font r13_ui_font()
            grid 2 menu_rows:
                spacing 16
                for title,icon,command,enabled in items:
                    button:
                        style "r13opt_button" xsize 288 ysize row_height
                        action command sensitive enabled alt title
                        hbox:
                            align (.5,.5) spacing 10
                            add R13AntiqueIcon(icon,size=(26 if r13_touch_ui() else 20)) yalign .5 alpha (1.0 if enabled else .5)
                            text title size (26 if r13_touch_ui() else 20) font r13_ui_font() yalign .5 color ("#4b3420" if enabled else "#8f8778")
                if len(items)%2:
                    null width 288 height row_height
    key "game_menu" action Hide("r13_more_tools")

screen r13_concept_skip_confirm():
    modal True
    zorder 115
    on "show" action [Function(r13_end_skip_modes),Preference("auto-forward","disable")]
    add Solid("#00000066")
    frame:
        area (330,235,620,250) padding (24,22) background R13PaperFrame()
        vbox:
            spacing 20
            text "현재 대화를 건너뛸까요?" size 28 color "#493b30" font r13_ui_font()
            text "처음 보는 대사도 지나가요. 다음 선택지에서 멈춥니다." size 21 color "#65503b" xsize 572 font r13_ui_font()
            hbox:
                spacing 16
                use r13_control("계속 읽기",None,Hide("r13_concept_skip_confirm"),primary=True,width=278,height=64)
                use r13_control("건너뛰기",None,[Hide("r13_concept_skip_confirm"),SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)],width=278,height=64)
    key "game_menu" action Hide("r13_concept_skip_confirm")
