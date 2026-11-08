# 실제 5일차 첫 발언을 멈춰, 작은 증인의 얼굴과 실제 장소 배경을 확인한다.
init python:
    def qa_meeting_child_edges():
        frame=r13_dialogue_source_profile('resident_kongi','neutral',840)['frames']['neutral']
        bounds=frame['source_alpha_bounds']
        y=r13_meeting_portrait_y('resident_kongi',840,96,'neutral')
        return tuple(y+frame['offset'][1]+bounds[n]*frame.get('scale',1) for n in (1,3))

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
    # 원화 여백이 바뀌어도 실제 머리·발선으로 검사한다. 캔버스 y의 부호는 의미가 없다.
    assert eval (100<qa_meeting_child_edges()[0]*1.06+(1-1.06)*240<300 and abs(qa_meeting_child_edges()[1]-760)<.51)
    screenshot "meeting-kongi-face-above-dialogue.png"
