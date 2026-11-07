# 원문과 관찰 버튼을 실제 화면에서 검증한다. 편지 두 장을 보유한 중간 상태 fixture다.
testcase letter_observation_layout:
    $ preferences.text_cps=0
    $ qa_letter_touch_before=r13_touch_ui
    $ qa_letter_large_before=persistent.room13_large_text
    $ r13_touch_ui=lambda:False
    $ persistent.room13_large_text=False
    run Function(renpy.set_physical_size,(1280,720))
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_grant,["V111:E01","V111:E06"],"qa-letter-observation")
    $ r13_pw_views={}
    run Jump("r13_v111_letter_compare")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    run Function(renpy.set_screen_variable,"pair",("V111:E01","V111:E06"),screen="r13_proof_workspace")
    run Function(renpy.set_screen_variable,"view","pair",screen="r13_proof_workspace")
    run Function(renpy.set_screen_variable,"observe",True,screen="r13_proof_workspace")
    run Function(renpy.set_screen_variable,"quote_open",False,screen="r13_proof_workspace")
    pause .7
    assert eval (all(qa_pw_read_has("r13_pw_spot_0_"+spot) and not qa_pw_read_has("r13_pw_spot_1_"+spot) for spot in ("head","body","tail","margin")))
    screenshot "letter-observation-buttons-pc.png"
    $ r13_touch_ui=lambda:True
    $ persistent.room13_large_text=True
    run Function(renpy.set_physical_size,(844,390))
    run Function(renpy.restart_interaction)
    pause .7
    assert eval (all(qa_pw_read_has("r13_pw_spot_0_"+spot) and not qa_pw_read_has("r13_pw_spot_1_"+spot) for spot in ("head","body","tail","margin")))
    screenshot "letter-observation-buttons-mobile.png"
    $ qa_letter_misses_before=r13_v111_value("letter_observe_miss") or 0
    click id "r13_pw_spot_0_head"
    pause until screen "say" timeout 15
    click pos (900,600) until screen "r13_proof_workspace" timeout 45
    assert eval ((r13_v111_value("letter_observe_miss") or 0)==qa_letter_misses_before+1)
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E01","V111:E06"))
    $ r13_touch_ui=qa_letter_touch_before
    $ persistent.room13_large_text=qa_letter_large_before
    run Function(renpy.set_physical_size,(1280,720))
