init python:
    def qa_nw_seen(text):
        # The say screen breaks long lines at sentence ends; compare as one line.
        return any(text in (getattr(e,"what","") or "").replace("\n"," ") for e in (getattr(store,"_history_list",None) or []))

testcase v111_nw_d01_gate_lost:
    # Event 01 plan A: a wrong gate proof is final; Daram enters as '외 한 명'.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("꼭 별 같아") and qa_nw_seen("기계 난로") and qa_nw_seen("등갓에 손을"))
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_set,"tries:gate",2)
    run Jump("r13_v111_gate_wrong")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("gate_daram_unlisted") is True and r13_v111_value("gate_registered") is True)
    assert eval (qa_nw_seen("근거가 맞지 않소") and qa_nw_seen("외 한 명’으로 붙여") and qa_nw_seen("일꾼 다돌, 외 한 명") and qa_nw_seen("이름 칸이 없소") and qa_nw_seen("정정 없음"))
    assert eval (qa_nw_seen("아르카 곁에.") and qa_nw_seen("불을 주는 돌이오"))
    assert eval (r13_catalog_record("V111:E05")["establishes"].startswith("정정 없음."))
    screenshot "v111_nw_d01_lost_registered.png"
    run Jump("r13_v111_registered_depart")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("돌목이 표를 접다가") and not qa_nw_seen("정정한 표를 접다가") and qa_nw_seen("이상하오"))

testcase v111_nw_d01_gate_won:
    # Winning keeps the authored registration and adds the greeting and the aside.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Jump("r13_v111_gate_proven")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("gate_daram_unlisted") is not True and r13_v111_value("gate_registered") is True)
    assert eval (qa_nw_seen("아르카 곁에."))
    assert eval (not qa_nw_seen("이름 칸이 없소"))
    assert eval (qa_nw_seen("다람. 됐소"))
    assert eval (r13_catalog_record("V111:E05")["establishes"].startswith("가족 방문 원본"))
    run Jump("r13_v111_registered_depart")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("정정한 표를 접다가") and qa_nw_seen("이상하오"))
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_room_empty")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("돌난로는 뚜껑이 닫힌"))
    screenshot "v111_nw_d01_room.png"
