init python:
    def qa_nw_day6_afternoon():
        # 6일 창고를 살핀 직후(MS14_D06_S02_L0024 확정). 오후 행동은 아직 하나도 하지 않았다.
        r13_v111_set("day",6)
        r13_v111_set("school_day_seat","confirmed")
        r13_edit(location="v111_woodshed",period=1)
        r13_v111_scene("MS14_D06_S02")
    def qa_nw_afternoon6_titles(place):
        r13_v111_context("afternoon6")
        return [o["title"] for o in r13_v111_binding()["options"] if o["location"]==place]

testcase v111_nw_d06_afternoon_today:
    # 0.20.18 열쇠표 K2: 선생님께 자리를 실제로 받아 두어야 창고에서 「지금 같이 가자」가 생기고,
    # 그 길로 네 아이를 학교에 넘기면 꼬미가 산다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day6_afternoon)
    assert eval (qa_nw_afternoon6_titles("v111_woodshed")==["내일 아침에 데리러 올게","장작더미 옆 깡통 줄을 살핀다"])  # 0.20.44 깡통 회수 사전 준비가 더해졌다
    assert eval (qa_nw_afternoon6_titles("school")==["아이들 자리를 여쭌다"])
    run Function(r13_edit,location="school")
    run Jump("r13_v111_afternoon6")
    pause 1.0
    assert screen "r13_hub"
    click "선생님"
    pause 1.0
    click "아이들 자리를 여쭌다"
    click pos (900,600) until eval (r13_v111_value("kkomi_seat6") is True and r13_v111_value("school_permission") is True) timeout 30
    assert eval (qa_nw_seen("창가 쪽 네 자리") and qa_nw_afternoon6_titles("school")==[])
    assert eval (qa_nw_afternoon6_titles("v111_woodshed")==["학교에 자리가 났어. 같이 갈래?","내일 아침에 데리러 올게","장작더미 옆 깡통 줄을 살핀다"])
    # 0.20.44: 깡통 줄을 풀어 도토리를 챙겨야 「같이 가자」가 이어진다(can_wait6). 그 단계는 따로 본다.
    run Function(r13_v111_set,"acorn_recovered",True)
    run Function(r13_edit,location="v111_woodshed")
    run Jump("r13_v111_afternoon6")
    pause 1.0
    # 창고는 너비 2400 이고 꼬미는 x 1454 에 선다. 처음 화면(카메라 0)에는 없으므로 오른쪽으로 민다.
    click "오른쪽 구역" until "꼬미" timeout 20
    pause 0.5
    click "꼬미"
    pause 1.0
    click "학교에 자리가 났어. 같이 갈래?"
    click pos (900,600) until eval (qa_nw_seen("가서 또 쫓겨나는 거 아니지")) timeout 30
    assert eval (r13_v111_value("choice:MS14_D06_S02")=="today" and r13_v111_value("evacuation_requested") is True)
    screenshot "v111_nw_d06_fetch.png"
    # 이동(지도)을 건너뛰고 학교 인계부터 본다.
    run Function(r13_v111_set,"acorn_recovered",True)
    run Function(r13_edit,location="school")
    run Jump("r13_v111_handoff_done6")
    pause 1.0
    click pos (900,600) until eval (r13_v111_value("D06_P01_handover_completed") is True) timeout 60
    assert eval (r13_v111_value("KKOMI_ALIVE") is True)
    assert eval (r13_v111_value("warehouse_children_school_handover")==4)
    assert eval (qa_nw_seen("오늘은 안 내보낸다"))

testcase v111_nw_d06_afternoon_tomorrow:
    # 자리를 받아 두고도 「내일 아침에 데리러 올게」로 떠나면 저녁에 불이 난다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day6_afternoon)
    run Function(r13_v111_set,"kkomi_seat6",True)
    run Jump("r13_v111_afternoon6")
    pause 1.0
    # 창고는 너비 2400 이고 꼬미는 x 1454 에 선다. 처음 화면(카메라 0)에는 없으므로 오른쪽으로 민다.
    click "오른쪽 구역" until "꼬미" timeout 20
    pause 0.5
    click "꼬미"
    pause 1.0
    click "내일 아침에 데리러 올게"
    click pos (900,600) until eval (qa_nw_seen("선생님 허락은 받아 뒀습니다")) timeout 30
    click pos (900,600) until eval (r13_v111_value("FIRE_EVACUATED") is False) timeout 30
    assert eval (r13_v111_value("choice:MS14_D06_S02")=="permission" and not qa_nw_seen("여쭤만 보겠습니다"))
    screenshot "v111_nw_d06_tomorrow.png"
