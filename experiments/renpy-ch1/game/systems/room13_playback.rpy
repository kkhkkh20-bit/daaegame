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

screen r13_playback_footer(show_record=False,ready=True):
    # 0.18.46 (owner): "건너뛰기" skips the rest of the current conversation (room13.rpy r13_lines).
    $ footer_width=r13_footer_width(5 if show_record else 4)
    $ skip_ready=ready and renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    add R13InkPanel(alpha="d4") xpos (1280-footer_width) ypos 676 xsize footer_width ysize 44
    frame:
        area (1280-footer_width,664,footer_width,56) padding (8,0) background None
        hbox:
            spacing 8
            if show_record:
                use r13_antique_button("기록","record",Show("r13_records"),enabled=ready,compact=True)
            use r13_antique_button("백로그","backlog",Show("r13_backlog"),enabled=ready,compact=True)
            use r13_antique_button(("자동 ●" if _preferences.afm_enable else "자동"),"auto",Preference("auto-forward","toggle"),enabled=ready,compact=True,chosen=_preferences.afm_enable)
            use r13_antique_button("건너뛰기","skip",[SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)],enabled=skip_ready,compact=True)
            if show_record:
                use r13_antique_button("더보기","settings",Show("r13_more_tools"),enabled=ready,compact=True)
            else:
                use r13_antique_button("옵션","settings",ShowMenu("pause_menu"),enabled=ready,compact=True)

screen r13_more_tools():
    modal True
    zorder 105
    $ line_active=renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    frame:
        area (962,356,294,304) padding (12,12) background R13InkPanel()
        vbox:
            spacing 6
            textbutton "읽은 대사 넘기기":
                style "r13_action_button" xsize 270 ysize 48 text_size 20
                selected r13_fast_read sensitive line_active
                action [Hide("r13_more_tools"),Function(r13_toggle_read_skip)]
            textbutton "모든 대사 빠르게":
                style "r13_action_button" xsize 270 ysize 48 text_size 20
                selected r13_fast_all sensitive line_active
                action [Hide("r13_more_tools"),Function(r13_toggle_fast_all)]
            textbutton "대화창 숨기기":
                style "r13_action_button" xsize 270 ysize 48 text_size 20 sensitive line_active
                action [Hide("r13_more_tools"),HideInterface()]
            textbutton "옵션":
                style "r13_action_button" xsize 270 ysize 48 text_size 20
                action [Hide("r13_more_tools"),ShowMenu("pause_menu")]
            textbutton "닫기":
                style "r13_action_button" xsize 270 ysize 48 text_size 20 action Hide("r13_more_tools")
    key "game_menu" action Hide("r13_more_tools")
