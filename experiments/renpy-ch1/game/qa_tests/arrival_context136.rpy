# 실제 첫 인물 클릭에서 공통 인사를 확인한다. 숙박·등록 상태를 준비하지 않는다.
testcase arrival136_first_meeting:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause .8
    assert eval (room13["location"]=="gate" and not r13_v111_value("gate_registered"))
    $ qa_arrival136_evidence=list(room13["evidence"])
    $ qa_arrival136_minutes=r13_v111_value("elapsed_minutes")
    click "실룩"
    pause until screen "say" timeout 20
    assert eval (r13_packet[0]=="dad" and "다돌" in r13_packet[1] and "여관" not in r13_packet[1] and "13호" not in r13_packet[1])
    screenshot "arrival136-first-meeting.png"
    click pos (900,600) until screen "r13_hub" timeout 35
    assert eval (room13["evidence"]==qa_arrival136_evidence and r13_v111_value("elapsed_minutes")==qa_arrival136_minutes and not r13_v111_value("gate_registered"))
