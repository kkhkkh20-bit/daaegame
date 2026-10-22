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

# Shared five-column footer, including playback states.
screen r13_strip_button(caption,icon,command,enabled=True,chosen=False,last=False,cell_width=None):
    use r13_control(caption,icon,command,enabled=enabled,chosen=chosen,width=cell_width or 232)

# Playback helpers live behind the rightmost More control.
screen r13_playback_footer(show_record=False,ready=True):
    # 0.19.98 (owner mockup): plain lines use the small text controls; 기록 lives in 더보기.
    use r13_night_controls(ready=ready)

screen r13_more_tools():
    # 0.20.0 (owner QA: "까로 질문 중 더보기 메뉴가 뒤에 떠 저장을 누르지 못하는 문제"): zorder set
    # inside a used screen is ignored, so this screen sat at 0 behind the modal question screen (30).
    zorder 105
    modal True
    # New-world meetings keep the approved dialogue menu (backlog inside, skip outside with confirmation).
    if r13_meeting_active and not r13_nw_meeting_claim(r13_meeting_claim):
        use r13_meeting_more_tools
    else:
        use r13_concept_more

screen r13_meeting_more_tools():
    modal True
    zorder 105
    $ line_active=renpy.get_screen("say") is not None and renpy.get_screen("choice") is None
    $ meeting_line=line_active and r13_meeting_active
    $ live_listening=meeting_line and r13_meeting_live_active and not r13_meeting_interrupting
    $ entries=[]
    if meeting_line:
        $ entries.append(("자동","auto",[Hide("r13_more_tools"),Preference("auto-forward","toggle")],True,_preferences.afm_enable))
        $ entries.append(("토론 멈추기" if live_listening else "건너뛰기","skip",[Hide("r13_more_tools"),Function(r13_meeting_request_live_action,"review")] if live_listening else [Hide("r13_more_tools"),SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)],True,False))
    if line_active:
        $ entries.append(("대화창 숨기기","dialogue",[Hide("r13_more_tools"),HideInterface()],True,False))
    $ entries.extend([
        ("저장 · 불러오기","record",[Hide("r13_more_tools"),ShowMenu("save")],True,False),
        ("다시 시작할 아침","auto",[Hide("r13_more_tools"),Show("r13_morning_pick")],bool(r13_morning_days()),False),
        ("설정","settings",[Hide("r13_more_tools"),ShowMenu("pause_menu")],True,False),
        ("메인화면","place_inn",[Hide("r13_more_tools"),Confirm("메인화면으로 돌아가시겠습니까?\n저장하지 않은 게임 진행은 사라집니다.",MainMenu(confirm=False))],True,False)])
    button:
        area (0,0,1280,720) background None action Hide("r13_more_tools") alt "닫기"
    frame:
        xpos 548 yanchor 1.0 ypos (r13_control_y()-16) xsize 704 padding (16,16) background R13InkPanel(alpha="e6",slim=True)
        vbox:
            spacing 16
            if line_active:
                hbox:
                    spacing 16
                    text "빠르게" size 22 color "#efe2c2" yalign .5 xsize 104
                    use r13_control("읽은 것만",None,[Hide("r13_more_tools"),Function(r13_toggle_read_skip)],enabled=not live_listening,chosen=r13_fast_read,width=268)
                    use r13_control("전부",None,[Hide("r13_more_tools"),Function(r13_toggle_fast_all)],enabled=not live_listening,chosen=r13_fast_all,width=268)
            $ menu_rows=(len(entries)+1)//2
            grid 2 menu_rows:
                spacing 16
                for title,icon,command,enabled,chosen in entries:
                    use r13_control(title,icon,command,enabled=enabled,chosen=chosen,width=328)
                if len(entries)%2:
                    null width 328 height r13_control_height()
    key "game_menu" action Hide("r13_more_tools")
