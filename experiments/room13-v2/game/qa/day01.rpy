# 1일 화면 시험. 처음부터 끝까지 실제 화면을 눌러 가며 상태를 확인한다.
# 대사를 넘길 때는 대사판 가운데(600,600)를 누른다(건너뛰기·더보기 단추를 피한다).

testcase v2_boot:
    pause until screen "main_menu" timeout 60
    run Function(qa_boot_mark)
    screenshot "boot_main.png"

testcase v2_skip:
    # 건너뛰기: 확인창 없이 읽지 않은 줄까지 넘기고, 다음 고르는 화면(입구 조사)에서 멈춘다.
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.5
    click "건너뛰기"
    pause until screen "v2_field" timeout 60
    pause 1.0
    assert eval (v2_gate == "gate_request" and not renpy.config.skipping and v2_has("E01"))

testcase v2_day01_right:
    # 정답 길: 마차 → 명단 → 선반(금요일) → 신청 원본 → 다르다고 말하기 → 근거 제시(명단+원본) → 여관 → 13호 → 대조 → 잠.
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    screenshot "a00_card.png"
    click pos (600, 600) until eval ("MS14_D01_S01_L0011" in v2_trace) timeout 60
    pause 2.0
    screenshot "a01_carriage.png"
    click pos (600, 600) until eval ("MS14_D01_S02_L0013" in v2_trace) timeout 120
    pause 3.0
    screenshot "a01b_gate_talk.png"
    click pos (600, 600) until screen "v2_field" timeout 180
    assert eval (v2_gate == "gate_request" and v2_has("E01") and v2_vals.get("carriage_stopped") is True and v2_loc == "gate")
    screenshot "a02_gate_request.png"
    pause 0.7
    click "돌목"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_gate == "gate_choice" and v2_has("E02") and v2_scene == "S02")
    pause 0.7
    click "초소 선반"
    click pos (600, 600) until screen "v2_choice" timeout 60
    screenshot "a03_shelf_menu.png"
    pause 0.7
    click "금요일 칸"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_gate == "gate_investigate")
    pause 0.7
    click "초소 서류"
    click pos (600, 600) until eval ("MS14_D01_S03_L0005" in v2_trace) timeout 60
    pause 2.5
    screenshot "a03b_stage.png"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_has("E03") and "MS14_D01_S03_L0003" in v2_trace and v2_scene == "S03")
    run Function(qa_measure)
    screenshot "a04_gate_investigate.png"
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    screenshot "a05_topics.png"
    pause 0.7
    click "명단과 신청서"
    click pos (600, 600) until screen "v2_topics" timeout 60
    assert eval (v2_vals.get("purpose_difference_known") is True)
    pause 0.7
    click "근거를 대겠습니다"
    pause until screen "v2_proof" timeout 10
    pause 0.7
    click "초소 처리 명단"
    pause 0.7
    click "방문 신청 원본"
    screenshot "a06_proof.png"
    pause 0.7
    click "근거 제시"
    click pos (600, 600) until screen "v2_field" timeout 120
    assert eval (v2_gate == "registered_menu" and v2_vals.get("gate_basis_proven") is True and v2_vals.get("meeting:gate") == "win")
    assert eval (v2_has("E05") and "MS14_D01_S03_L0014" in v2_trace and "NW_D01_S03_X01" not in v2_trace)
    pause 0.7
    click "지도"
    pause until screen "v2_map" timeout 10
    screenshot "a07_map.png"
    pause 0.7
    click "이곳으로 이동"
    click pos (600, 600) until screen "v2_field" timeout 120
    assert eval (v2_gate == "to_room13" and v2_loc == "inn" and v2_scene == "S05" and v2_vals.get("heard_inn_order1") is True)
    screenshot "a08_inn.png"
    pause 0.7
    click "지도"
    pause until screen "v2_map" timeout 10
    pause 0.7
    click "이곳으로 이동"
    click pos (600, 600) until screen "v2_field" timeout 120
    assert eval (v2_gate == "note_pick" and v2_loc == "room13" and v2_vals.get("ui_room_arrival_seen") is True)
    screenshot "a09_room13.png"
    pause 0.7
    click "책상 위 접힌 종이"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_gate == "bundle_open" and v2_has("E06"))
    pause 0.7
    click "책상 아래 보따리"
    click pos (600, 600) until screen "v2_choice" timeout 60
    pause 0.7
    click "보따리를 연다"
    click pos (600, 600) until screen "v2_proof" timeout 60
    assert eval (v2_has("E30") and v2_vals.get("under_desk_checked") is True)
    pause 0.7
    click "방의 메모"
    pause 0.7
    click "›"
    pause 0.7
    click "초대 편지"
    pause 0.7
    click "나란히 놓기"
    screenshot "a10_compare_pair.png"
    pause 0.7
    click "끝부분"
    click pos (600, 600) until screen "v2_proof" timeout 60
    assert eval (v2_vals.get("letter_tail_observed") is True and "NW_D01_OB04" in v2_trace)
    pause 0.7
    click "돌아가기"
    pause 0.7
    click "견주어 본다"
    click pos (600, 600) until screen "v2_choice" timeout 60
    assert eval (v2_period == 2 and "NW_D01_SR01" not in v2_trace)
    pause 0.7
    click "할머니에게"
    click pos (600, 600) until screen "v2_field" timeout 120
    assert eval (v2_gate == "sleep1" and v2_loc == "room13" and v2_vals.get("cookie.location") == "room13_plate")
    screenshot "a11_sleep.png"
    pause 0.7
    click "과자를 두고 잠든다"
    click pos (600, 600) until screen "main_menu" timeout 60
    assert eval (persistent.v2_last_end["vals"].get("day") == 2 and "E30" in persistent.v2_last_end["ev"])

testcase v2_day01_partial:
    # 일부 정답 뒤 정답: 원본 하나만 → 원본+규칙(맞는 자료만 남고 반박) → 명단까지 더해 이김(편지 덧붙임).
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    run Function(qa_jump, "gate_investigate", ev=["E01", "E02"], place="gate")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "초소 서류"
    click pos (600, 600) until screen "v2_field" timeout 60
    pause 0.7
    click "입장 규칙"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_has("E03") and v2_has("E04"))
    pause 0.7
    click "기록"
    pause until screen "v2_records" timeout 10
    screenshot "b00_records_ev.png"
    click "사람"
    pause 0.3
    screenshot "b00_records_people.png"
    click "메모"
    pause 0.3
    screenshot "b00_records_memo.png"
    click "닫기"
    pause 0.7
    click "설정"
    pause until screen "v2_settings" timeout 10
    screenshot "b00_settings.png"
    click "저장 · 불러오기"
    pause until screen "v2_files" timeout 10
    click "1쪽 1번"
    pause 1.0
    screenshot "b00_saved.png"
    assert eval (len(renpy.list_saved_games(fast=True)) == 1)
    run Function(qa_poke, "qa_marker", True)
    click "불러오기로"
    pause 0.3
    screenshot "b00_load_mode.png"
    click "1쪽 1번"
    pause 0.5
    screenshot "b00_after_load_click.png"
    pause until screen "v2_field" timeout 30
    pause 1.0
    run Function(qa_write, "after_load.txt", (v2_gate, list(v2_ev), v2_vals.get("qa_marker"), v2_loc))
    assert eval (v2_gate == "gate_investigate")
    assert eval (v2_has("E04"))
    assert eval (v2_vals.get("qa_marker") is None)
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    pause 0.7
    click "자료 제시"
    pause until screen "v2_present" timeout 10
    pause 0.3
    click "초대 편지"
    screenshot "b00_present.png"
    click "보여 준다"
    click pos (600, 600) until screen "v2_topics" timeout 60
    assert eval (v2_vals.get("reacted:guard:E01") is True and v2_gate == "gate_investigate")
    pause 0.7
    click "근거를 대겠습니다"
    pause until screen "v2_proof" timeout 10
    pause 0.7
    click "방문 신청 원본"
    pause 0.7
    click "근거 제시"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_vals.get("tries:gate") == 1 and v2_vals.get("gate_hardened") is True and v2_kept.get("gate") == ["E03"])
    assert eval ("MS14_D01_S03_L0024" in v2_trace)
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    pause 0.7
    click "근거를 대겠습니다"
    pause until screen "v2_proof" timeout 10
    assert eval (v2_pick == ["E03"])
    pause 0.7
    click "겨울철 입장 규칙"
    pause 0.7
    click "근거 제시"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_vals.get("tries:gate") == 2 and v2_kept.get("gate") == ["E03"] and "NW_D01_S03_R04" in v2_trace)
    pause 0.7
    click "돌목"
    pause until screen "v2_topics" timeout 10
    pause 0.7
    click "근거를 대겠습니다"
    pause until screen "v2_proof" timeout 10
    pause 0.7
    click "초소 처리 명단"
    pause 0.7
    click "초대 편지"
    screenshot "b01_proof_kept.png"
    pause 0.7
    click "근거 제시"
    click pos (600, 600) until screen "v2_field" timeout 120
    assert eval (v2_gate == "registered_menu" and v2_vals.get("gate_basis_proven") is True and "NW_D01_S03_X02" in v2_trace and "MS14_D01_S03_L0020" in v2_trace)

testcase v2_day01_detours:
    # 선반 틀린 칸(목요일·토요일), 대조에서 틀린 짝, 「방을 더 둘러본다」로 지도 이동 두 번.
    pause until screen "main_menu" timeout 60
    click "처음부터"
    pause 1.0
    run Function(qa_jump, "gate_choice", ev=["E01", "E02"], place="gate")
    pause until screen "v2_field" timeout 30
    pause 0.7
    click "초소 선반"
    click pos (600, 600) until screen "v2_choice" timeout 60
    pause 0.7
    click "목요일 칸"
    click pos (600, 600) until screen "v2_choice" timeout 60
    pause 0.7
    click "토요일 칸"
    click pos (600, 600) until screen "v2_choice" timeout 60
    assert eval ("v2_choice" and v2_gate == "gate_choice")
    pause 0.7
    click "금요일 칸"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_gate == "gate_investigate")
    run Function(qa_jump, "letter_compare", ev=["E03", "E04", "E05", "E06", "E30"], vals={"gate_registered": True}, place="room13")
    pause until screen "v2_proof" timeout 30
    pause 0.7
    click "›"
    pause 0.7
    click "초대 편지"
    pause 0.7
    click "방문 신청 원본"
    pause 0.7
    click "견주어 본다"
    click pos (600, 600) until screen "v2_proof" timeout 60
    assert eval ("NW_CMP_RETRY_01" in v2_trace and v2_period == 0 and v2_pick == ["E01"])
    pause 0.7
    click "방의 메모"
    pause 0.7
    click "견주어 본다"
    click pos (600, 600) until screen "v2_choice" timeout 60
    assert eval ("NW_D01_SR01" in v2_trace)
    pause 0.7
    click "방을 더 둘러본다"
    pause until screen "v2_field" timeout 30
    assert eval (v2_gate == "to_inn")
    pause 0.7
    click "지도"
    pause until screen "v2_map" timeout 10
    pause 0.7
    click "이곳으로 이동"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_gate == "to_room13_night" and v2_loc == "inn" and "MS14_D01_S05_L0037" in v2_trace)
    pause 0.7
    click "지도"
    pause until screen "v2_map" timeout 10
    pause 0.7
    click "이곳으로 이동"
    click pos (600, 600) until screen "v2_field" timeout 60
    assert eval (v2_gate == "sleep1" and "MS14_D01_S05_L0050" in v2_trace)
