# 2026-10-30 소유자 B안(논쟁 점검 P28): 11일 가설 5번에서 기회가 다해도 1~4번을 하나라도 이겼으면 반쪽으로 끝난다.
testcase v111_hyp5_lost_after_wins:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_edit,location="school")
    run Function(r13_v111_set,"hyp_issue:1","won")
    run Function(r13_v111_set,"hyp_issue:2","lost")
    run Function(r13_v111_set,"tries:hypothesis",r13_nw_tries_max("hypothesis"))
    run Jump("r13_v111_hyp5_lost11")
    click pos (900,600) until eval (r13_v111_value("meeting:hypothesis") is not None and qa_nw_seen("학교에 온 사람들의 집만 불을 끈다")) timeout 90
    assert eval (r13_v111_value("meeting:hypothesis")=="partial" and qa_nw_seen("몇 사람이 일어선다") and not qa_nw_seen("다시 불을 켠다"))

testcase v111_hyp5_lost_none_won:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_edit,location="school")
    run Function(r13_v111_set,"tries:hypothesis",r13_nw_tries_max("hypothesis"))
    run Jump("r13_v111_hyp5_lost11")
    click pos (900,600) until eval (qa_nw_seen("끝내 마을을 설득하지 못했다")) timeout 90
    assert eval (r13_v111_value("meeting:hypothesis")=="lose")
