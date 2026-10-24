# Approved 2x2 title: transparent margins must not block directional focus.
testcase title_b_navigation:
    pause 3.0
    move pos (446,506)
    pause 0.3
    keysym "K_DOWN"
    pause 0.3
    assert eval (renpy.get_screen("main_menu").scope["title_focus"]=="settings")
    keysym "K_RETURN"
    pause 0.3
    assert screen "pause_menu"
    click "닫기"
    pause 0.3
    assert screen "main_menu"
