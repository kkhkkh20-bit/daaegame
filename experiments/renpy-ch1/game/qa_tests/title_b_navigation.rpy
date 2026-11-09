# 승인된 세로 메뉴: 비활성 항목을 건너뛰고 키보드로 설정을 연다.
testcase title_b_navigation:
    pause 3.0
    move pos (360,360)
    pause 0.3
    keysym "K_DOWN"
    pause 0.3
    # 저장이 있는 SDK 환경에서도 실제 활성 항목만 따라 내려간다.
    assert eval (renpy.get_screen("main_menu").scope["title_focus"]==("continue" if r13_continue_slot() else "load" if r13_save_slots() else "settings"))
    if eval (r13_continue_slot()):
        keysym "K_DOWN"
        pause 0.3
    if eval (r13_save_slots()):
        keysym "K_DOWN"
        pause 0.3
    assert eval (renpy.get_screen("main_menu").scope["title_focus"]=="settings")
    keysym "K_RETURN"
    pause 0.3
    assert screen "pause_menu"
    click "닫기"
    pause 0.3
    assert screen "main_menu"
