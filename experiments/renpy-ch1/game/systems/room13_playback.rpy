# Playback UI reads real history and never rewinds game state.
init 97 python:
    _r13_previous_afm_callback=config.afm_callback
    def r13_auto_can_advance():
        if getattr(store,"room13_mode",False):
            blocked=("choice","r13_topics","r13_backlog","r13_records","r13_book",
                "r13_map","r13_learning_notes","r13_more_tools","r13_confirm","r13_work_board","pause_menu","save","load",
                "r13_record_compare","r13_mystery_notebook","r13_item_bag",
                "r13_tool_notebook","r13_cinematic_view","r13_debate_board","r13_meeting_agenda","r13_meeting_ballot")
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

# 0.18.99: 큰 글씨(휴대폰 기본값)에서는 칸 112×56 → 132×70, 글씨 20 → 24.
screen r13_strip_button(caption,icon,command,enabled=True,chosen=False,last=False):
    $ big=persistent.room13_large_text
    $ cw,ch=(132,70) if big else (112,56)
    button:
        xsize cw ysize ch padding (2,0)
        background (R13StripCell(True) if chosen else None)
        hover_background R13StripCell(True)
        action command sensitive enabled alt caption
        fixed:
            xsize (cw-4) ysize ch
            hbox:
                xalign .5 yalign .5 spacing 4
                add R13AntiqueIcon(icon,size=22) yalign .5 alpha (1.0 if enabled else .4)
                text caption size (24 if big else 20) font r13_ui_font() color ("#efe2c2" if enabled else "#a59a86") yalign .5
            if not last:
                add Solid("#756b5980") xpos (cw-5) ypos 13 xsize 1 ysize (ch-26)

screen r13_playback_footer(show_record=False,ready=True):
    $ big=persistent.room13_large_text
    $ footer_width=(5 if show_record else 4)*(132 if big else 112)
    $ footer_height=70 if big else 56
    $ skip_ready=ready and renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    fixed:
        xpos (1280-footer_width) ypos (720-footer_height) xsize footer_width ysize footer_height
        add R13InkPanel() xsize footer_width ysize footer_height
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
    # 0.19.2 빼기 정리 (소유자 승인 시안): 9개 → 저장·불러오기 / 다시 시작할 아침 / 설정 / 메인화면.
    # 대사 중에만 「빠르게」(읽은 것만·전부)와 「대화창 숨기기」. 생활 장부는 일거리와 함께 없앴다. 바깥을 누르면 닫힌다.
    modal True
    zorder 105
    $ line_active=renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    $ meeting_line=line_active and r13_meeting_active
    $ live_listening=meeting_line and r13_meeting_live_active and not r13_meeting_interrupting
    button:
        area (0,0,1280,720) background None action Hide("r13_more_tools") alt "닫기"
    frame:
        xpos 932 yanchor 1.0 ypos (642 if persistent.room13_large_text else 656) xsize 324 padding (12,12) background R13InkPanel()
        vbox:
            spacing 6
            if meeting_line:
                textbutton "자동":
                    style "r13_action_button" xsize 300 ysize 48 text_size 20
                    selected _preferences.afm_enable
                    action [Hide("r13_more_tools"),Preference("auto-forward","toggle")]
                textbutton ("토론 멈추기" if live_listening else "건너뛰기"):
                    style "r13_action_button" xsize 300 ysize 48 text_size 20
                    action ([Hide("r13_more_tools"),Function(r13_meeting_request_live_action,"review")] if live_listening else [Hide("r13_more_tools"),SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)])
            if line_active:
                frame:
                    xsize 300 ysize 52 padding (10,6) background R13InkPanel(focused=True)
                    hbox:
                        spacing 6 yalign .5
                        text "빠르게" size 18 color "#efe2c2" yalign .5 min_width 62
                        textbutton "읽은 것만":
                            style "r13_paper_tab_button" xsize 104 ysize 38 text_size 16
                            selected r13_fast_read sensitive not live_listening
                            action [Hide("r13_more_tools"),Function(r13_toggle_read_skip)]
                        textbutton "전부":
                            style "r13_paper_tab_button" xsize 104 ysize 38 text_size 16
                            selected r13_fast_all sensitive not live_listening
                            action [Hide("r13_more_tools"),Function(r13_toggle_fast_all)]
                textbutton "대화창 숨기기":
                    style "r13_action_button" xsize 300 ysize 48 text_size 20
                    action [Hide("r13_more_tools"),HideInterface()]
            textbutton "저장 · 불러오기":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                action [Hide("r13_more_tools"),ShowMenu("save")]
            textbutton "다시 시작할 아침":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                sensitive bool(r13_morning_days())
                action [Hide("r13_more_tools"),Show("r13_morning_pick")]
            textbutton "설정":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                action [Hide("r13_more_tools"),ShowMenu("pause_menu")]
            textbutton "메인화면":
                style "r13_action_button" xsize 300 ysize 48 text_size 20
                action [Hide("r13_more_tools"),Confirm("메인화면으로 돌아가시겠습니까?\n저장하지 않은 게임 진행은 사라집니다.",MainMenu(confirm=False))]
    key "game_menu" action Hide("r13_more_tools")
