# 실제 사망 직후 문맥을 준비해 현장 클릭·후속 질문을 실행한다. 생사 경로의 자연 주행은 별도 검사한다.
init python:
    def qa_piko_mourning_setup(with_record=False):
        r13_v111_set("day",3)
        r13_v111_set("piko_alive",False)
        r13_edit(day=3,period=0,location="square")
        store.place=R13_PLACES["square"][0]
        # 실제 사망 확인 대화가 남기는 E09가 다음 장면의 진입 조건이다.
        r13_grant(["V111:E09"],"qa")
        r13_v111_scene("MS14_D03_S02")
        r13_v111_arrive(["resident_lamplighter","neoul","resident_tok","daram"])
        if with_record:r13_grant(["V111:E11"],"qa")

testcase v111_piko_mourning_idle_and_child:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko_mourning_setup)
    run Jump("r13_v111_lamp_inspect3")
    pause until screen "r13_hub" timeout 30
    run SetVariable("qa_piko_elapsed",r13_v111_value("elapsed_minutes") or 0)
    run SetVariable("qa_piko_evidence",list(room13["evidence"]))
    pause until eval (renpy.get_screen("r13_hub").scope["world_ready"]) timeout 30
    run Function(qa_early_person_point,"resident_lamplighter")
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause .7
        run Function(qa_early_person_point,"resident_lamplighter")
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    pause until screen "say" timeout 30
    assert eval (r13_packet[0]=="dad" and r13_packet[2].get("expression")=="anxious")
    click pos (900,600) until eval (r13_packet and r13_packet[0]=="resident_lamplighter") timeout 30
    assert eval (r13_packet[2].get("expression")=="anxious" and "안녕하세요" not in r13_packet[1])
    screenshot "piko-mourning-idle.png"
    click pos (900,600) until screen "r13_hub" timeout 30
    assert eval (r13_v111_value("piko_alive") is False and room13["evidence"]==qa_piko_evidence and r13_v111_value("elapsed_minutes")==qa_piko_elapsed)
    assert eval (r13_v111_daram_hello()[0][2].get("expression")=="anxious")

testcase v111_piko_mourning_followup_keeps_record_and_read:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko_mourning_setup,True)
    run Jump("r13_v111_lamp_inspect3")
    pause until screen "r13_hub" timeout 30
    run SetVariable("qa_piko_elapsed",r13_v111_value("elapsed_minutes") or 0)
    run SetVariable("qa_piko_evidence",list(room13["evidence"]))
    pause until eval (renpy.get_screen("r13_hub").scope["world_ready"]) timeout 30
    run Function(qa_early_person_point,"resident_lamplighter")
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause .7
        run Function(qa_early_person_point,"resident_lamplighter")
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    pause until screen "r13_topics" timeout 30
    pause .7
    assert eval (len(r13_v111_questions("resident_lamplighter"))==1 and "초롱 씨" in r13_v111_questions("resident_lamplighter")[0][0])
    screenshot "piko-mourning-question.png"
    keysym "K_1"
    pause until screen "say" timeout 30
    assert eval ("기록을 다시 확인" in r13_packet[1].replace("\n"," ") and r13_packet[2].get("expression")=="anxious")
    click pos (900,600) until screen "r13_topics" timeout 45
    assert eval (r13_v111_value("followup_read:NW_RX_F008") is True and r13_v111_questions("resident_lamplighter")[0][2])
    assert eval (qa_nw_seen("3번, 돌 3") and qa_nw_seen("새벽 종 직전 점검 완료"))
    assert eval (r13_v111_value("piko_alive") is False and room13["evidence"]==qa_piko_evidence and r13_v111_value("elapsed_minutes")==qa_piko_elapsed)
