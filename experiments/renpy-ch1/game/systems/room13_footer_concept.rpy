# 더보기 판(r13_concept_more). 옛 대사 하단 띠 r13_concept_dock·건너뛰기 확인창 r13_concept_skip_confirm 은
# 2026-10-27 정리에서 지웠다 — 대사는 B 대사판(이름 리본)으로 바뀌었고 건너뛰기 확인창은 없애기로 결정했다.
init 80 python:
    R13_CONCEPT_RIGHT=1232

screen r13_concept_more():
    modal True
    zorder 105
    on "show" action Function(r13_end_skip_modes)
    $ active=renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    # 2026-10-27 소유자 "대화 도구에 불필요한 건 다 삭제해": 자료 기록(허브의 기록), 저장·불러오기·메인화면(설정),
    # 다시 시작할 아침은 뺐다. 대화를 읽는 데 필요한 것만 남긴다.
    $ items=[("대화 기록","backlog",[Hide("r13_more_tools"),Show("r13_backlog")],True),
        ("자동 읽기","auto",[Hide("r13_more_tools"),Preference("auto-forward","toggle")],active),
        ("읽은 대사 빠르게","skip",[Hide("r13_more_tools"),Function(r13_toggle_read_skip)],active),
        ("대화창 숨기기","dialogue",[Hide("r13_more_tools"),HideInterface()],active),
        ("설정","settings",[Hide("r13_more_tools"),ShowMenu("pause_menu")],True)]
    # 2026-10-27 검수: 뒤를 어둡게 해 현장 인물이 판 밑으로 삐져나와 보이지 않게.
    add Solid("#05070f80")
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
            text "대화 도구" size (r13_type("subtitle")) color (r13_type_color("ink")) font r13_ui_font()
            # 항목이 홀수면 마지막 것은 두 칸 폭으로 두어 빈칸이 남지 않게 한다(2026-10-27 검수).
            $ paired=items[:len(items)-(len(items)%2)]
            $ paired_rows=len(paired)//2
            grid 2 paired_rows:
                spacing 16
                for title,icon,command,enabled in paired:
                    use r13_concept_more_item(title,icon,command,enabled,288,row_height)
            if len(items)%2:
                use r13_concept_more_item(items[-1][0],items[-1][1],items[-1][2],items[-1][3],592,row_height)
    key "game_menu" action Hide("r13_more_tools")

screen r13_concept_more_item(title,icon,command,enabled,width,row_height):
    button:
        style "r13opt_button" xsize width ysize row_height
        action command sensitive enabled alt title
        hbox:
            align (.5,.5) spacing 10
            add R13AntiqueIcon(icon,size=(26 if r13_touch_ui() else 20)) yalign .5 alpha (1.0 if enabled else .5)
            text title size (r13_type("body")) font r13_ui_font() yalign .5 color ((r13_type_color("ink")) if enabled else (r13_type_color("disabled")))
