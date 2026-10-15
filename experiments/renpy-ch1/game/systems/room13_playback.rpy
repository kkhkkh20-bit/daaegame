# Playback UI reads real history and never rewinds game state.
init 97 python:
    _r13_previous_afm_callback=config.afm_callback
    def r13_auto_can_advance():
        if getattr(store,"room13_mode",False):
            blocked=("choice","r13_topics","r13_backlog","r13_records","r13_book",
                "r13_map","r13_confirm","r13_work_board","pause_menu","save","load",
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

screen r13_playback_footer():
    $ footer_width=r13_footer_width(3)
    add Solid("#14272be8") xpos (1280-footer_width) ypos 676 xsize footer_width ysize 40
    frame:
        area (1280-footer_width,664,footer_width,56) padding (8,0) background None
        hbox:
            spacing 8
            textbutton "백로그" style "r13_footer_button" action Show("r13_backlog")
            textbutton ("자동 ●" if _preferences.afm_enable else "자동"):
                style "r13_footer_button" action Preference("auto-forward","toggle")
            textbutton "옵션" style "r13_footer_button" action ShowMenu("pause_menu")
