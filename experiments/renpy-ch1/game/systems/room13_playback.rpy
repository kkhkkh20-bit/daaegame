# Playback UI reads real history and never rewinds game state.
init 97 python:
    _r13_previous_afm_callback=config.afm_callback
    def r13_auto_can_advance():
        if getattr(store,"room13_mode",False):
            blocked=("choice","r13_topics","r13_backlog","r13_records","r13_book",
                "r13_map","r13_learning_notes","r13_more_tools","r13_confirm","r13_work_board","pause_menu","save","load",
                "r13_record_compare","r13_mystery_notebook","r13_item_bag",
                "r13_tool_notebook","r13_cinematic_view","r13_debate_board")
            if any(renpy.get_screen(name) for name in blocked):return False
        return _r13_previous_afm_callback() if _r13_previous_afm_callback else True
    config.afm_callback=r13_auto_can_advance

screen r13_backlog():
    modal True
    zorder 110
    # Opaque: the current line behind must not show through the history.
    add Solid("#10212aff")
    text "백로그" xpos 90 ypos 36 size 32 color "#fff2cf"
    text "실제로 읽은 대화 · 최근 기록부터" xpos 245 ypos 46 size 20 color "#b7ccd0"
    viewport:
        area (90,108,1100,500) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 20
            for row in r13_history_rows():
                frame:
                    xsize 1060 padding (18,14) background Solid("#253d465e")
                    vbox:
                        spacing 8
                        text (row["who"]+" · "+row["stamp"]):
                            size 20 color "#9fcbd9" xsize 1020
                        text row["what"]:
                            size r13_read_size(25,31) color (r13_role_color("thought") if row["kind"]=="독백" else r13_role_color("narration") if row["kind"]=="서술" else r13_role_color("speech")) xsize 1020
    textbutton "대화로 돌아가기":
        style "r13_action_button" area (935,646,255,48) text_size 22 action Hide("r13_backlog")
    key "game_menu" action Hide("r13_backlog")
    key "K_h" action Hide("r13_backlog")

screen r13_strip_button(caption,icon,command,enabled=True,chosen=False,last=False):
    button:
        xsize 112 ysize 56 padding (2,0)
        background (R13StripCell(True) if chosen else None)
        hover_background R13StripCell(True)
        action command sensitive enabled alt caption
        fixed:
            xsize 108 ysize 56
            hbox:
                xalign .5 yalign .5 spacing 4
                add R13AntiqueIcon(icon,size=22) yalign .5 alpha (1.0 if enabled else .4)
                text caption size 20 font r13_ui_font() color ("#efe2c2" if enabled else "#a59a86") yalign .5
            if not last:
                add Solid("#756b5980") xpos 107 ypos 13 xsize 1 ysize 30

screen r13_playback_footer(show_record=False,ready=True):
    $ footer_width=560 if show_record else 448
    $ skip_ready=ready and renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    fixed:
        xpos (1280-footer_width) ypos 664 xsize footer_width ysize 56
        add R13InkPanel() xsize footer_width ysize 56
        hbox:
            spacing 0
            use r13_strip_button("백로그","backlog",Show("r13_backlog"),enabled=ready)
            use r13_strip_button("자동","auto",Preference("auto-forward","toggle"),enabled=ready,chosen=_preferences.afm_enable)
            use r13_strip_button("건너뛰기","skip",[SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)],enabled=skip_ready)
            if show_record:
                use r13_strip_button("더보기","settings",Show("r13_more_tools"),enabled=ready)
                use r13_strip_button("기록","record",Show("r13_records"),enabled=ready,last=True)
            else:
                use r13_strip_button("설정","settings",ShowMenu("pause_menu"),enabled=ready,last=True)

screen r13_more_tools():
    modal True
    zorder 105
    $ line_active=renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    frame:
        area (932,204 if line_active else 366,324,456 if line_active else 294) padding (12,12) background R13InkPanel()
        vbox:
            spacing 6
            if line_active:
                textbutton "읽은 대사 넘기기":
                    style "r13_action_button" xsize 300 ysize 48 text_size 20
                    selected r13_fast_read sensitive line_active
                    action [Hide("r13_more_tools"),Function(r13_toggle_read_skip)]
                textbutton "모든 대사 빠르게":
                    style "r13_action_button" xsize 300 ysize 48 text_size 20
                    selected r13_fast_all sensitive line_active
                    action [Hide("r13_more_tools"),Function(r13_toggle_fast_all)]
                textbutton "대화창 숨기기":
                    style "r13_action_button" xsize 300 ysize 48 text_size 20 sensitive line_active
                    action [Hide("r13_more_tools"),HideInterface()]
            textbutton "진행 저장":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                action [Hide("r13_more_tools"),ShowMenu("save")]
            textbutton "진행 불러오기":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                action [Hide("r13_more_tools"),ShowMenu("load")]
            textbutton "설정":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                action [Hide("r13_more_tools"),ShowMenu("pause_menu")]
            textbutton "메인화면":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                action [Hide("r13_more_tools"),Confirm("메인화면으로 돌아가시겠습니까?\n저장하지 않은 게임 진행은 사라집니다.",MainMenu(confirm=False))]
            textbutton "닫기":
                style "r13_action_button" xsize 300 ysize 48 text_size 20 action Hide("r13_more_tools")
    key "game_menu" action Hide("r13_more_tools")
