# 문맥 회귀: 세 자료로 오답·재제출, 완료 후 개별 제시, 메모 사전 정보와 관찰.

testcase v2_logic_gate:
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    # 예전 판에서 차이를 이미 말하고 세 자료만 모은 저장 위치와 같다.
    run Function(qa_jump, "gate_investigate", ev=["E01", "E02", "E03"], vals={"purpose_difference_known": True}, place="gate")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    click "근거를 대겠습니다"
    pause until screen "v2_proof" timeout 10
    click "방문 신청 원본"
    click "근거 제시"
    click pos (600, 600) until eval ("MS14_D01_S03_L0024" in v2_trace) timeout 60
    assert eval ("말한 차이는 알겠소" in v2_current()[1]["t"])
    pause 1.5
    screenshot "gate_acknowledged_retry.png"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (set(v2_ev) == {"E01", "E02", "E03"} and v2_kept["gate"] == ["E03"])
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    click "근거를 대겠습니다"
    pause until screen "v2_proof" timeout 10
    click "초소 처리 명단"
    click "근거 제시"
    click pos (600, 600) until screen "v2_field" timeout 120
    assert eval (v2_gate == "registered_menu" and v2_vals.get("gate_registered") is True and not v2_has("E04"))
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    assert eval (not any(r["key"] == ("follow", "F002") for r in v2_topics("guard")))
    click "자료 제시"
    pause until screen "v2_present" timeout 10
    click "정정된 입장 기록"
    click "보여 준다"
    pause until screen "say" timeout 10
    assert eval ("내가 확인한 기록" in v2_current()[1]["t"])
    pause 1.5
    screenshot "gate_registered_record.png"
    click pos (600, 600) until screen "v2_topics" timeout 60
    pause 0.7
    click "자료 제시"
    pause until screen "v2_present" timeout 10
    click "초소 처리 명단"
    click "보여 준다"
    click pos (600, 600) until screen "v2_topics" timeout 60
    assert eval (v2_vals.get("reacted:guard:E02") is True and v2_vals.get("gate_registered") is True)

testcase v2_logic_letters:
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    run Function(qa_jump, "note_pick", ev=["E01", "E02", "E03", "E05"], vals={"gate_registered": True}, place="room13")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "책상 위 접힌 종이"
    click pos (600, 600) until eval ("MS14_D01_S05_L0020" in v2_trace) timeout 60
    assert eval ("맨날 도토리" in v2_current()[1]["t"])
    pause 1.5
    screenshot "note_habit_before_compare.png"
    click pos (600, 600) until screen "v2_field" timeout 60
    pause 0.7
    click "책상 아래 보따리"
    click pos (600, 600) until screen "v2_choice" timeout 60
    pause 0.7
    click "보따리를 연다"
    click pos (600, 600) until screen "v2_proof" timeout 60
    click "방의 메모"
    click "›"
    click "초대 편지"
    click "나란히 놓기"
    click "머리글"
    pause until screen "say" timeout 10
    assert eval ("겨울 날짜" not in v2_current()[1]["t"] and "받는 사람 이름" not in v2_current()[1]["t"])
    pause 1.5
    screenshot "compare_visible_information.png"
    click pos (600, 600) until screen "v2_proof" timeout 60
    click "돌아가기"
    click "견주어 본다"
    click pos (600, 600) until screen "v2_choice" timeout 60
    assert eval (not v2_vals.get("letter_tail_observed") and "NW_D01_SR01" in v2_trace)
    click "방을 더 둘러본다"
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "지도"
    pause until screen "v2_map" timeout 10
    click "이곳으로 이동"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_gate == "to_room13_night" and "MS14_D01_S05_L0037" in v2_trace)
    pause 0.7
    click "할머니"
    pause until screen "v2_topics" timeout 10
    click "자료 제시"
    pause until screen "v2_present" timeout 10
    click "방의 메모"
    click "보여 준다"
    pause until screen "say" timeout 10
    assert eval ("아까 말씀하신" in v2_current()[1]["t"])
    pause 1.5
    screenshot "granny_remembers_chorong.png"
