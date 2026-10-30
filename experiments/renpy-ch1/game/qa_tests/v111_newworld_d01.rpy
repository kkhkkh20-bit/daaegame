init python:
    def qa_nw_seen(text):
        # The say screen breaks long lines at sentence ends; compare as one line.
        # {w=.4} 같은 글자 태그는 화면에 안 보이므로 빼고 비교한다.
        import re
        return any(text in re.sub(r"\{[^{}]*\}","",(getattr(e,"what","") or "")).replace("\n"," ") for e in (getattr(store,"_history_list",None) or []))

testcase v111_nw_d01_gate_lost:
    # Event 01 plan A: a wrong gate proof is final; Daram enters as '외 한 명'.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("꼭 별 같아") and qa_nw_seen("기계 난로") and qa_nw_seen("등갓에 손을"))
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_set,"tries:gate",r13_nw_tries_max("gate")-1)
    run Jump("r13_v111_gate_wrong")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("gate_daram_unlisted") is True and r13_v111_value("gate_registered") is True)
    assert eval (qa_nw_seen("그걸로는 확인이 안 되오") and qa_nw_seen("외 한 명’으로 붙여") and qa_nw_seen("일꾼 다돌, 외 한 명") and qa_nw_seen("이름 칸이 없소") and qa_nw_seen("정정 없음"))
    assert eval (qa_nw_seen("아르카 곁에.") and qa_nw_seen("불을 주는 돌이오"))
    assert eval (r13_catalog_record("V111:E05")["establishes"].startswith("정정 없음."))
    screenshot "v111_nw_d01_lost_registered.png"
    run Jump("r13_v111_registered_depart")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("돌목이 표를 접으며") and not qa_nw_seen("정정한 표를 접으며") and qa_nw_seen("여관에 먼저 연락하라"))

testcase v111_nw_d01_gate_won:
    # Winning keeps the authored registration and adds the greeting and the aside.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
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
    assert eval (r13_catalog_record("V111:E05")["establishes"].startswith("방문 신청 원본"))
    run Jump("r13_v111_registered_depart")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("정정한 표를 접으며") and qa_nw_seen("여관에 먼저 연락하라"))
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_room_empty")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("돌난로는 뚜껑이 닫힌"))
    screenshot "v111_nw_d01_room.png"

testcase v111_nw_d01_gate_extra_letter:
    # 0.20.4 proof scope: the invitation (E01) on top of the three needed records passes;
    # Dolmok says the letter is not needed. A wrong letter pair asks to choose again.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Function(r13_grant,["V111:E01","V111:E02","V111:E03","V111:E04"],"qa")
    run Jump("r13_v111_gate_proof")
    pause 1.5
    # 2026-10-27 UX 인계서 D01: 입구 논증은 통합 화면(systems/room13_proof_workspace.rpy). 체크로 고르고 「근거 제시」.
    assert screen "r13_proof_workspace"
    click id "r13_pw_check_E01"
    pause 0.4
    click id "r13_pw_check_E02"
    pause 0.4
    click id "r13_pw_check_E03"
    pause 0.4
    click id "r13_pw_check_E04"
    pause 0.4
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("meeting:gate")=="win" and r13_v111_value("gate_daram_unlisted") is not True)
    assert eval (qa_nw_seen("그 편지는 이 확인에 필요 없소") and r13_v111_value("proof_given:함께 들어갈 근거를 고른다")==["V111:E01","V111:E02","V111:E03","V111:E04"])
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_letter_retry")
    pause 1.0
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    assert eval (qa_nw_seen("편지끼리 나란히 놓아야 한다"))  # 2026-10-30 P23 문구

testcase v111_nw_d01_gate_choice_no_actions:
    # 2026-10-29 외부 검토 「행동이 질문 목록 안에 있다」: 입구에서 돌목의 질문 목록에는 「초대 편지를 보여 준다」도
    # 「신청서를 찾으러 선반으로 간다」도 없다. 편지는 「자료 제시」로 보이고, 신청서는 선반(초소)을 눌러 찾는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Show("r13_qa_inject_return",value=("person","guard"))
    pause until screen "say" timeout 30
    click pos (640,300) until eval (room13["v111"]["gate"]=="gate_choice" and renpy.get_screen("r13_hub") is not None) timeout 60
    assert eval (not [q for q in r13_v111_questions("guard") if q[0] in ("초대 편지를 보여 준다","신청서를 찾으러 선반으로 간다")])
    assert eval (r13_v111_has_business("guard"))
    run Show("r13_qa_inject_return",value=("person","guard"))
    pause until screen "r13_topics" timeout 30
    pause 0.8
    screenshot "v111_nw_d01_gate_choice_topics.png"
    # 「자료 제시」로 초대 편지를 내면 편지 쪽 장면(MS14_D01_S02_L0023)으로 간다.
    run Show("r13_qa_inject_return",value="present")
    pause until screen "r13_book" timeout 30
    run Show("r13_qa_inject_return",value="V111:E01")
    # 같은 사람과의 대화가 이어지므로 끝나면 돌목의 질문 목록이 다시 열린다(0.20.6).
    click pos (900,600) until eval (room13["v111"]["gate"]=="gate_investigate" and (renpy.get_screen("r13_hub") or renpy.get_screen("r13_topics")) is not None) timeout 60
    assert eval (r13_has("v111:applied:MS14_D01_S02_L0022_O1") and qa_nw_seen("편지로는 무엇을 신청했는지 모르오"))
