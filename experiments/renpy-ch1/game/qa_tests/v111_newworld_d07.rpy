init python:
    def qa_nw_day7():
        r13_v111_set("day",7)
        r13_grant(["V111:"+k for k in ("E06_FIRE","E06_RESCUE","E07_NUBI")],"qa")
        r13_v111_set("FIRE_EVACUATED",False)
        r13_edit(location="v111_wash" if "v111_wash" in R13_PLACES else "school")

testcase v111_nw_d07_fire_lost:
    # Losing Nubi's fire (gate): Bori is blamed and listed; the school scene still opens.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day7)
    run Function(r13_v111_set,"tries:fire",R13_NW_TRIES-1)
    run Jump("r13_v111_nubi_wrong7")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:fire")=="lose" and r13_v111_value("listed:resident_bori") is True)
    assert eval (qa_nw_seen("불을 놓은 사람은 보리로 적으시오") and qa_nw_seen("사정은 들었소") and qa_nw_seen("붙잡는 사람은 없다"))
    assert eval (not r13_v111_value("fire_neoul_promise_recorded"))

testcase v111_nw_d07_fire_partial:
    # Weighing lost: '셋 다 책임' stands, Bori listed for hiding, the promise is not recorded.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day7)
    run Function(r13_v111_set,"NUBI_admitted_setting_fire",True)
    run Function(r13_v111_scene,"MS14_D07_S02")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:fire",R13_NW_TRIES-1)
    run Jump("r13_v111_responsibility_wrong7")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:fire")=="partial" and r13_v111_value("listed:resident_bori") is True)
    assert eval (qa_nw_seen("셋 다 책임이오") and qa_nw_seen("어디에도 적히지 않는다") and not qa_nw_seen("……적으시오"))
