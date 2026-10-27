# 더보기 판(r13_concept_more). 옛 대사 하단 띠 r13_concept_dock·건너뛰기 확인창 r13_concept_skip_confirm 은
# 2026-10-27 정리에서 지웠다 — 대사는 B 대사판(이름 리본)으로 바뀌었고 건너뛰기 확인창은 없애기로 결정했다.
init 80 python:
    R13_CONCEPT_RIGHT=1232

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
    # Same paper and navy notebook material as the approved settings screen.
    frame:
        xpos 584 ypos (min(r13_control_y(),R13_NIGHT_CONTROL_Y-28)-panel_height-16) xysize (648,panel_height) padding (28,22) background Frame(Crop((35,25,550,245),r13_asset_path("file:assets/ui-b-main/b_main_panel.png")),48,40)
        vbox:
            spacing 16
            # 2026-10-27 타이포 시안: 더보기 판 제목 subtitle, 항목 body(종이 위 ink, 비활성 disabled).
            text "대화 도구" size (r13_type("subtitle") if R13_TYPE_V2 else (28 if r13_touch_ui() else 24)) color (r13_type_color("ink") if R13_TYPE_V2 else "#493323") font r13_ui_font()
            grid 2 menu_rows:
                spacing 16
                for title,icon,command,enabled in items:
                    button:
                        style "r13opt_button" xsize 288 ysize row_height
                        action command sensitive enabled alt title
                        hbox:
                            align (.5,.5) spacing 10
                            add R13AntiqueIcon(icon,size=(26 if r13_touch_ui() else 20)) yalign .5 alpha (1.0 if enabled else .5)
                            text title size (r13_type("body") if R13_TYPE_V2 else (26 if r13_touch_ui() else 20)) font r13_ui_font() yalign .5 color ((r13_type_color("ink") if R13_TYPE_V2 else "#4b3420") if enabled else (r13_type_color("disabled") if R13_TYPE_V2 else "#8f8778"))
                if len(items)%2:
                    null width 288 height row_height
    key "game_menu" action Hide("r13_more_tools")
