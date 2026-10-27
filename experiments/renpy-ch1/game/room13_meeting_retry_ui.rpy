# 10번 승인 시안의 표시·선택 계약. 회의 초기화나 실패 분기 연결은 이야기 담당이 맡는다.
init 323 python:
    R13_MEETING_RETRY_ACCEPT="accept"
    R13_MEETING_RETRY_RETRY="retry"

screen r13_meeting_retry_choice():
    modal True
    zorder 95
    default ready=False
    timer .2 action SetScreenVariable("ready",True)
    add Solid("#0f1a287d")
    # 원본 비율 유지. 시안 설명 머리글·검토 문구는 게임에 넣지 않는다.
    add Transform(r13_asset_path("file:assets/ui-b-options/b_opt_panel.png"),zoom=1000.0/1288) xpos 138 ypos 86
    add r13_asset_path("file:assets/ui-b-options/b_opt_title_tape.png") xpos 240 ypos 120
    # 타이포 V2: 남색(#263b52)은 이 판의 잉크 역할색이라 토큰(갈색)으로 바꾸지 않는다. 크기만 단계표를 따른다.
    text "회의를 마치며" xpos 331 ypos 156 xanchor .5 yanchor .5 size (r13_type("body") if R13_TYPE_V2 else 23) color "#263b52" font R13_UI_BOLD_FONT
    add Transform(r13_asset_path("file:assets/ui-b-options/b_opt_sticker_corner.png"),zoom=120.0/152) xpos 953 ypos 117
    text "다 있었다." xpos 640 ypos 265 xanchor .5 yanchor .5 size (r13_type("display") if R13_TYPE_V2 else 36) color "#263b52" font R13_UI_BOLD_FONT
    text "그런데 이어 붙이지 못했다." xpos 640 ypos 315 xanchor .5 yanchor .5 size (r13_type("display") if R13_TYPE_V2 else 36) color "#263b52" font R13_UI_BOLD_FONT
    # 작은 160px 납품 버튼을 확대하지 않는다. 승인된 고해상 공통 확인 부품을 사용한다.
    button:
        id "r13_meeting_retry_accept"
        area (218,380,410,133) padding (20,20)
        background r13_sticker_button(primary=True)
        hover_background r13_sticker_button(primary=True,focused=True)
        action Return(R13_MEETING_RETRY_ACCEPT) sensitive ready default_focus True
        alt "결과를 받아들인다"
        text "결과를 받아들인다" align (.5,.5) size (r13_type("emphasis") if R13_TYPE_V2 else (28 if r13_touch_ui() else 26)) color (r13_type_color("inverse") if R13_TYPE_V2 else "#fff8e9") font R13_UI_BOLD_FONT
    button:
        id "r13_meeting_retry_again"
        area (652,380,410,133) padding (20,20)
        background r13_sticker_button()
        hover_background r13_sticker_button(focused=True)
        action Return(R13_MEETING_RETRY_RETRY) sensitive ready
        alt "회의를 처음부터 다시"
        text "회의를 처음부터 다시" align (.5,.5) size (r13_type("emphasis") if R13_TYPE_V2 else (28 if r13_touch_ui() else 26)) color "#263b52" font R13_UI_BOLD_FONT
    text "이 결과로 이야기를 이어갑니다." xpos 423 ypos 539 xanchor .5 yanchor .5 size (r13_type("small") if R13_TYPE_V2 else 22) color (r13_type_color("muted") if R13_TYPE_V2 else "#756f66") font R13_UI_BOLD_FONT
    text "같은 회의의 첫머리로 돌아갑니다." xpos 857 ypos 539 xanchor .5 yanchor .5 size (r13_type("small") if R13_TYPE_V2 else 22) color (r13_type_color("muted") if R13_TYPE_V2 else "#756f66") font R13_UI_BOLD_FONT
    # 2026-10-27 외부 리뷰: 첫 패배 때만 되돌아갈 수 있는 범위를 한 줄로 알린다(실제로 있는 기능만).
    $ recovery_note=r13_recovery_retry_note()
    if recovery_note:
        text recovery_note id "r13_recovery_retry_note" xpos 640 ypos 590 xanchor .5 yanchor .5 xmaximum 900 text_align .5 size (r13_type("small") if R13_TYPE_V2 else (22 if r13_touch_ui() else 20)) color "#263b52" font R13_UI_BOLD_FONT
    # 닫기·타이머는 결정을 대신하지 않는다. 받아들임은 기존 패배 분기로 전달한다.
    key "game_menu" action NullAction()

label r13_meeting_retry_prompt:
    call screen r13_meeting_retry_choice
    return _return
