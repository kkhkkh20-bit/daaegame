# 0.18.99 PC 단축키 (소유자 2026-10-17: "모바일 게임이지만 PC로 하는 사람을 위해서")
# 이미 있던 것: 클릭·스페이스·엔터 = 다음 대사, 숫자 1~9 = 선택지·질문, H = 화면 숨기기, Esc = 메뉴, 회의 ←/→ = 발언 고르기.
# 새로 넣은 것:
#   Ctrl(누르고 있는 동안) = 모든 대사 빠르게 · Tab = 읽은 대사 넘기기(다시 누르면 멈춤)
#   M = 지도 · R = 기록 · 확인창 Enter = 예, Esc = 아니요
init 171 python:
    # Ren'Py's own Ctrl/Tab skipping only skips read text and bypasses the footer modes; ours replace them.
    config.keymap["skip"] = []
    config.keymap["toggle_skip"] = []

    R13_SHORTCUT_HELP = [
        ("클릭 · 스페이스 · 엔터","다음 대사"),
        ("Ctrl (누르고 있기)","모든 대사 빠르게"),
        ("Tab","읽은 대사 넘기기 / 멈추기"),
        ("1 ~ 9","선택지 · 질문 고르기"),
        ("M","지도 · 이동"),
        ("R","기록"),
        ("H","대화창 숨기기"),
        ("← →","회의에서 발언 고르기"),
        ("Enter / Esc","확인창에서 예 / 아니요"),
        ("Esc","메뉴 · 닫기"),
    ]

    def r13_shortcut_line_active():
        return renpy.get_screen("say") is not None and renpy.get_screen("choice") is None

    def r13_shortcut_fast(on):
        if not getattr(store,"room13_mode",False):return
        if on and r13_shortcut_line_active() and not store.r13_fast_all:
            r13_toggle_fast_all()
        elif not on and store.r13_fast_all:
            r13_end_skip_modes()
            renpy.restart_interaction()

    def r13_shortcut_read_skip():
        if getattr(store,"room13_mode",False) and r13_shortcut_line_active():
            r13_toggle_read_skip()

    def r13_shortcut_field():
        """The roaming hub is up and nothing modal sits above it."""
        if not getattr(store,"room13_mode",False) or renpy.get_screen("r13_hub") is None:return False
        return not any(renpy.get_screen(n) for n in ("r13_records","r13_map","r13_more_tools","r13_confirm","say","choice","r13_book"))

    def r13_shortcut_records():
        busy=("r13_records","r13_book","r13_map","r13_more_tools","r13_confirm","r13_shortcut_help","save","load","pause_menu","r13_debate_board","r13_meeting_ballot")
        if getattr(store,"room13_mode",False) and store.room13 and not any(renpy.get_screen(n) for n in busy):
            renpy.show_screen("r13_records")
            renpy.restart_interaction()

    config.overlay_screens.append("r13_shortcuts")

screen r13_shortcuts():
    # Above every modal screen of the game layer, so the keys reach it first.
    zorder 200
    if room13_mode:
        key "K_LCTRL" action Function(r13_shortcut_fast,True)
        key "K_RCTRL" action Function(r13_shortcut_fast,True)
        key "keyup_K_LCTRL" action Function(r13_shortcut_fast,False)
        key "keyup_K_RCTRL" action Function(r13_shortcut_fast,False)
        key "K_TAB" action Function(r13_shortcut_read_skip)
        key "K_r" action Function(r13_shortcut_records)
        if r13_shortcut_field():
            key "K_m" action Return(("menu","map"))

screen r13_shortcut_help():
    modal True
    zorder 110
    key "game_menu" action Hide("r13_shortcut_help")
    add Solid("#0b151bcc")
    frame:
        # 2026-10-27 타이포 시안: 제목 subtitle, 줄 body. 「크게」(28)에서 설명 줄이 620 을 넘어 판을 720 으로 넓힌다.
        xalign .5 yalign .5 xsize (720) padding (30,24) background R13PaperFrame()
        vbox:
            spacing 10
            text "단축키 (PC)" size (r13_type("subtitle")) color (r13_type_color("ink")) font r13_ui_font()
            for keys,what in R13_SHORTCUT_HELP:
                hbox:
                    spacing 16
                    text keys size (r13_type("body")) color (r13_type_color("ink")) min_width 250 font r13_ui_font()
                    text what size (r13_type("body")) color (r13_type_color("muted")) font r13_ui_font()
            null height 6
            textbutton "닫기" style "r13_action_button" xsize 180 ysize 48 text_size (r13_type("body")) xalign .5 action Hide("r13_shortcut_help")
