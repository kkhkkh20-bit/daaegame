# 실제 오답 분기에서 기회 소진 화면과 첫 쟁점 복귀를 확인한다.
init python:
    def qa_retry_seed(meeting):
        r13_meeting_checkpoint(meeting)
        store.qa_retry_before=winter_copy.deepcopy(room13)
        r13_v111_set("tries:"+meeting,r13_nw_tries_max(meeting)-1)
        r13_v111_set("proof_given:qa_retry",["V111:E01"])
        room13["arguments"]["qa_retry"]=["V111:E01"]
        room13["flags"].append("v111:applied:qa_retry")

label qa_retry_lamp:
    $ qa_nw_day3_meeting_ready()
    $ qa_retry_seed("lamp")
    jump r13_v111_knife_wrong

label qa_retry_room13:
    $ qa_nw_day(10,"murder")
    $ qa_retry_seed("room13")
    jump r13_v111_hearing_wrong10

label qa_retry_hypothesis:
    $ qa_nw_day11()
    $ qa_retry_seed("hypothesis")
    jump r13_v111_hyp0_sick11

testcase meeting_retry_lamp:
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 120
    run Jump("qa_retry_lamp")
    click pos (900,600) until screen "r13_meeting_retry_choice" timeout 60
    assert eval (r13_v111_value("meeting:lamp") is None)
    pause 0.5
    click id "r13_meeting_retry_again"
    pause 1.0
    assert eval (r13_nw_tries_left("lamp")==r13_nw_tries_max("lamp") and r13_v111_value("proof_given:qa_retry") is None and "v111:applied:qa_retry" not in room13["flags"] and room13["evidence"]==qa_retry_before["evidence"])
    assert eval (not renpy.get_screen("notify"))
    screenshot "meeting-retry-lamp.png"
    run SetVariable("qa_retry_stack_depth",len(renpy.get_return_stack()))
    run Function(r13_v111_set,"tries:lamp",r13_nw_tries_max("lamp")-1)
    click "자료 고르기"
    pause 0.5
    click "QA V111:E14"
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    pause until screen "r13_meeting_retry_choice" timeout 20
    pause 0.5
    click id "r13_meeting_retry_again"
    pause 1.0
    assert eval (r13_nw_tries_left("lamp")==r13_nw_tries_max("lamp") and len(renpy.get_return_stack())==qa_retry_stack_depth)


testcase meeting_retry_room13:
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 120
    run Jump("qa_retry_room13")
    click pos (900,600) until screen "r13_meeting_retry_choice" timeout 60
    assert eval (r13_v111_value("meeting:room13") is None)
    pause 0.5
    click id "r13_meeting_retry_again"
    pause 1.0
    assert eval (r13_nw_tries_left("room13")==r13_nw_tries_max("room13") and r13_v111_value("proof_given:qa_retry") is None and "v111:applied:qa_retry" not in room13["flags"] and room13["evidence"]==qa_retry_before["evidence"])
    screenshot "meeting-retry-room13.png"

testcase meeting_retry_hypothesis:
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 120
    run Jump("qa_retry_hypothesis")
    click pos (900,600) until screen "r13_meeting_retry_choice" timeout 60
    assert eval (r13_v111_value("meeting:hypothesis") is None)
    pause 0.5
    click id "r13_meeting_retry_again"
    pause 1.0
    assert eval (r13_nw_tries_left("hypothesis")==r13_nw_tries_max("hypothesis") and r13_v111_value("proof_given:qa_retry") is None and "v111:applied:qa_retry" not in room13["flags"] and room13["evidence"]==qa_retry_before["evidence"])
    screenshot "meeting-retry-hypothesis.png"

testcase meeting_retry_accept:
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 120
    run Jump("qa_retry_hypothesis")
    click pos (900,600) until screen "r13_meeting_retry_choice" timeout 60
    pause 0.5
    click id "r13_meeting_retry_accept"
    click pos (900,600) until eval (r13_v111_value("meeting:hypothesis")=="lose") timeout 60
