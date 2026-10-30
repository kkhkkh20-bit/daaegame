# 이야기를 돌리는 고리 하나. 한 바퀴에 사람이 보는 일은 하나뿐이라(대사 한 쪽, 조사 화면, 고르기, 증명)
# 저장·되감기가 그 문장 처음으로 돌아가도 같은 자리에서 다시 시작한다.

label start:
    $ v2_new_game()
    show screen v2_hud
    call v2_run
    $ renpy.music.stop(channel="amb", fadeout=1.0)
    return

label v2_run:
    while True:
        $ v2_next = v2_advance()
        if v2_next is None:
            return
        elif v2_next == "line":
            $ v2_do_line()
        elif v2_next == "wait":
            $ v2_wait_enter()
            call screen v2_field
            $ v2_field_result(_return)
        elif v2_next == "ui":
            if v2_ui[0] == "topics":
                call screen v2_topics(v2_ui[1])
            else:
                call screen v2_present(v2_ui[1])
            $ v2_ui_result(_return)
        elif v2_next == "menu":
            $ renpy.choice_for_skipping()
            call screen v2_choice
            $ v2_menu_choose(_return)
        elif v2_next == "proof":
            $ renpy.choice_for_skipping()
            $ renpy.hide("v2fig")
            $ v2_fig = None
            $ v2_stage = None
            $ v2_proof_prepare(v2_proof_id())
            call screen v2_proof(v2_proof_id())
            $ v2_proof_result(_return)

label after_load:
    show screen v2_hud
    return
