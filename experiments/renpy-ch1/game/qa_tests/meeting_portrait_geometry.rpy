# 실제 5일차 첫 발언을 멈춰, 작은 증인의 얼굴과 실제 장소 배경을 확인한다.
testcase meeting_child_face_at_gate:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day5,[])
    run Function(r13_v111_set,"musoe.location","clinic")
    run Function(r13_v111_set,"somi.location","clinic")
    run Call("qa_rr_scene","r13_v111_hearing5")
    click pos (900,600) until eval (r13_meeting_active and r13_meeting_focus=="resident_kongi") timeout 60
    pause 1.5
    assert eval (R13_MEETING_SOLO and r13_meeting_claim=="NW:gate_post")
    assert eval (r13_meeting_portrait_y("resident_kongi",840,96,"neutral")<0)
    screenshot "meeting-kongi-face-above-dialogue.png"
