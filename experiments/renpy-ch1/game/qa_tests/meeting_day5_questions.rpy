# 5일차 첫 증명은 이미 통과한 상태만 준비한다. 추가 질문은 승리·기회·보유 자료를 다시 판정하지 않는다.
init python:
    def qa_hearing_question5(sketch=False):
        r13_v111_set('day',5)
        r13_edit(day=5,location='gate',period=1)
        # 첫 증명 뒤의 상태를 준비한다. 대체 정답 시험은 E23·E24 없는 보유 목록을 그대로 쓴다.
        r13_flag('v111:entered:MS14_D05_S03')
        r13_v111_scene('MS14_D05_S03')
        r13_v111_arrive(['daram','guard','neoul','resident_nero','resident_badook','resident_kongi'])
        materials=['E20','E22','NW_PIKO_SKETCH4'] if sketch else ['E20','E22','E23','E24']
        r13_grant(['V111:'+key for key in materials],'qa-hearing-question')
        r13_v111_set('proof_given:밤이 혐의의 근거를 확인한다',['V111:'+key for key in materials])
        r13_v111_set('tries:gate_post',2)

testcase meeting_day5_face_question_keeps_sketch_win:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_hearing_question5,True)
    run Jump('r13_v111_bami_clear5')
    click pos (900,600) until screen 'choice' timeout 90
    assert eval (v111_menu_owner=='hearing_counter5' and r13_v111_value('meeting:gate_post')=='win')
    assert eval (not r13_v111_owned('E24') and r13_nw_followup_issue)
    screenshot 'meeting-day5-question.png'
    click '돌목 씨, 얼굴을 보셨습니까?'
    click pos (900,600) until screen 'r13_hub' timeout 120
    assert eval (qa_nw_seen('못 봤소. 검은 게 털인지 옷인지도 몰랐소.') and qa_nw_seen('네로 씨가 식당에서 제 물통을'))
    assert eval (r13_v111_value('meeting:gate_post')=='win' and r13_v111_value('tries:gate_post')==2)
    assert eval (not r13_v111_owned('E24') and r13_v111_owned('E26') and r13_nw_followup_issue is None)

testcase meeting_day5_coat_question_gets_direct_witness:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_hearing_question5)
    run Jump('r13_v111_bami_clear5')
    click pos (900,600) until screen 'choice' timeout 90
    assert eval (v111_menu_owner=='hearing_counter5' and r13_nw_followup_issue)
    click '네로 씨, 그 옷을 입었습니까?'
    click pos (900,600) until screen 'r13_hub' timeout 120
    assert eval (qa_nw_seen('아뇨. 그날 저녁 어르신께 걸쳐 드렸어요.') and qa_nw_seen('네로 씨가 식당에서 제 물통을'))
    assert eval (r13_v111_value('meeting:gate_post')=='win' and r13_v111_value('tries:gate_post')==2)
    assert eval (r13_v111_owned('E26') and r13_nw_followup_issue is None)
