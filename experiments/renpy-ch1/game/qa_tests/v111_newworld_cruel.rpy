testcase v111_nw_d12_fever_no_blankets:
    # 0.20.18 CRUEL_CHOICES.md C2·C4: 담요 두 장이 다 남지 않은 판은 12일 아침 다람이 열이 나고,
    # 하나뿐인 난로 옆자리를 다람이 쓴다. 배식 때 쓸 자리는 마련되지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_v111_set,"carried_dry_blankets",1)
    run Function(r13_v111_set,"lower_road_handover",3)
    run Jump("r13_v111_morning_notice12")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("daram_fever12") is True and qa_nw_seen("외투 하나로는 모자랐나 봐"))
    run Jump("r13_v111_warm_place12")
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("warm_seat_taken12") is True and not r13_v111_value("warm_seat_ready"))
    assert eval (qa_nw_seen("열나는 아이부터 눕혀야죠"))
    run Function(r13_v111_context,"morning_prep12")
    assert eval ("불 땔 자리를 부탁드립니다." not in [o["title"] for o in r13_v111_binding()["options"]])
    screenshot "v111_nw_d12_fever.png"

testcase v111_nw_d12_two_blankets_no_fever:
    # 담요 두 장을 지킨 판은 열이 나지 않고 자리를 부탁할 수 있다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_v111_set,"carried_dry_blankets",2)
    run Function(r13_v111_set,"lower_road_handover",3)
    run Jump("r13_v111_morning_notice12")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (not r13_v111_value("daram_fever12") and not qa_nw_seen("외투 하나로는 모자랐나 봐"))
    run Jump("r13_v111_warm_place12")
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("warm_seat_ready") is True)

testcase v111_nw_d13_crowd_block_fails:
    # 0.20.18 CRUEL_CHOICES.md C1: 너울 앞을 몸으로 막으면 군중이 아빠 쪽으로 쏠리고 다람이 다친다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"family_location","square")
    run Function(r13_v111_set,"location:daram","square")
    run Jump("r13_v111_crowd_block13")
    pause 1.0
    click pos (900,600) until eval (r13_v111_value("crowd_injury") is True) timeout 60
    assert eval (r13_v111_value("outcome13")=="crowd_violence" and r13_v111_value("crowd_intervention")=="failed")
    assert eval (qa_nw_seen("애가 있어요") and qa_nw_seen("아무도 그쪽을 보지 않는다"))
    screenshot "v111_nw_d13_crowd_block.png"

testcase v111_nw_d04_silluk_mercy:
    # 0.20.18 CRUEL_CHOICES.md C3 A안: 3일 실룩을 풀어 주면 4일 5번 등이 비고, 밤이가 울타리 옆으로 내려온다.
    # 5일 초소 회의 기회가 하나 준다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",4)
    run Function(r13_v111_set,"silluk_status","reporting_obligation")
    run Function(r13_grant,["V111:E18"],"qa")
    run Function(r13_edit,location="square",period=1)
    run Jump("r13_v111_eaves4")
    pause 1.0
    click pos (900,600) until eval (r13_v111_value("bami_cold4") is True and qa_nw_seen("입술이 파랗다")) timeout 60
    assert eval (qa_nw_seen("5번 등이요. 어젯밤에 또 비었어요"))
    screenshot "v111_nw_d04_silluk_mercy.png"
    run Function(qa_nw_day5,[])
    run Jump("r13_v111_proof5")
    pause 1.5
    assert screen "r13_crisis_proof"
    assert eval (r13_v111_value("tries:gate_post")==1 and r13_v111_value("gate_post_cold_cost") is True)
