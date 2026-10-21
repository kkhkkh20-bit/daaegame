init python:
    def qa_nw_day12(route="late_exposure"):
        r13_v111_set("day",12)
        r13_edit(day=12,location="school",period=2)
        r13_v111_set("route7","murder")
        r13_v111_set("OWL_ALIVE",False)
        r13_v111_set("DARAM_DETAINED",False)
        r13_v111_set("family_reunited",True)
        r13_v111_set("family_school_place",True)
        r13_v111_set("route12",route)
        r13_v111_set("soup_fragment_observed",True)
        r13_v111_set("medical_arrived",True)

testcase v111_nw_d12_morning_list:
    # The transfer column: Daram's name is on it after a lost room-13 meeting.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_nw_list,"daram","room13_lose")
    run Function(r13_nw_list,"resident_bori","fire_lose")
    run Function(r13_v111_set,"lower_road_handover",3)
    run Jump("r13_v111_morning_notice12")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_owned("NW_TRANSFER_LIST") and qa_nw_seen("다람의 이름이 있다") and qa_nw_seen("보리의 이름도 있다") and not qa_nw_seen("나비의 이름도 있다"))

testcase v111_nw_d12_soup_list_partial:
    # Teacher confessed, list point lost: Neoul keeps the list.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_v111_set,"teacher_confessed",True)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_list_wrong12")
    click pos (900,600) until "돌목에게 감독을 맡긴다" timeout 150
    assert eval (r13_v111_value("meeting:soup")=="partial" and not r13_v111_value("transfer_list_secured"))
    assert eval (qa_nw_seen("명단이 무슨 상관이오"))

testcase v111_nw_d12_soup_won:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_v111_set,"teacher_confessed",True)
    run Jump("r13_v111_list_won12")
    click pos (900,600) until "돌목에게 감독을 맡긴다" timeout 150
    assert eval (r13_v111_value("meeting:soup")=="win" and r13_v111_value("transfer_list_secured") is True)
    assert eval (qa_nw_seen("돌아온 아이는 없어요") and qa_nw_seen("우리 애는 명단에 없었소"))

testcase v111_nw_d12_soup_lost_nabi:
    # Handling point lost: Nabi is written on the list, the teacher goes free.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12,"premeal_stopped")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_fragment_wrong12")
    click pos (900,600) until screen "r13_hub" timeout 150
    assert eval (r13_v111_value("meeting:soup")=="lose" and r13_v111_value("listed:nabi") is True and not r13_v111_value("teacher_confessed"))
    assert eval (qa_nw_seen("나비의 이름을 적는다") and qa_nw_seen("찾지 못했어") and not qa_nw_seen("보리가 도담 곁에서"))

testcase v111_nw_d12_portrait:
    # Piko dead: the overpainted portrait shows what was under it.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_v111_set,"piko_alive",False)
    run Jump("r13_v111_sleep12")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (qa_nw_seen("엄마 얼굴 밑에 누가 있어") and qa_nw_seen("붉은 목도리"))
