# 실제 새 게임 저장 뒤 메인의 이어하기·불러오기·키보드 상태를 확인한다.
testcase title_book_saved_navigation:
    pause 1.0
    click "처음부터"
    pause until screen "say" timeout 60
    run Function(renpy.save,"1-1")
    run MainMenu(confirm=False)
    pause until screen "main_menu" timeout 40
    assert eval (r13_continue_slot()=="1-1")
    assert eval (renpy.get_screen("main_menu").scope["title_focus"]=="continue")
    screenshot "메인_저장있음.png"
    move pos (360,440)
    pause 0.3
    keysym "K_DOWN"
    pause 0.3
    assert eval (renpy.get_screen("main_menu").scope["title_focus"]=="load")
    keysym "K_RETURN"
    pause until screen "load" timeout 20
    click "돌아가기"
    pause until screen "main_menu" timeout 20
    click "이어하기"
    pause until screen "say" timeout 40
