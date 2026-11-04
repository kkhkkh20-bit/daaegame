# 4~6일 수정 중 6일의 인물 위치 회귀를 검사한다.
# 전체 자연 주행과 달리 기존 상태 설정 함수로 각 장면 직전까지 준비한다.
# 검사 구간은 실제 이야기 라벨과 이동 화면을 진행하며, 게임 함수는 바꾸지 않는다.

testcase v111_d456_nabi_supply_location:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",6)
    run Function(r13_v111_set,"mother_warning_received",True)
    run Function(r13_v111_set,"KKOMI_ALIVE",True)
    run Function(r13_edit,location="school",period=0)
    run Function(r13_v111_scene,"MS14_D06_S01")
    run Function(r13_v111_arrive,["daram","kid_kkomi"])
    run Jump("r13_v111_nabi_supply6")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D06_S01_L0036") timeout 60
    # 나비가 그릇을 받고 묻는 첫 대사부터 식당이며, 세 인물이 실제로 함께 있다.
    assert eval (room13["location"]=="dining")
    assert eval (set(room13["v111"]["people"])==set(["daram","kid_kkomi","nabi"]))
    assert eval (all(r13_v111_value("location:"+p)=="dining" and r13_v111_actor_ready(p) for p in ["daram","kid_kkomi","nabi"]))
    assert eval (r13_packet[0]=="nabi")

testcase v111_d456_school_permission_reaction:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day6_afternoon)
    run Function(r13_v111_set,"location:kid_kkomi","v111_woodshed")
    run Function(r13_edit,location="school",period=1)
    run Jump("r13_v111_seat6")
    click pos (900,600) until eval (r13_packet and "다람이 움찔한다." in r13_packet[1]) timeout 40
    # 허락만 묻는 때에는 다람이 반응한다. 아직 데려오지 않은 꼬미는 창고에 남아 있다.
    assert eval (room13["location"]=="school" and r13_packet[0] is None)
    assert eval (set(room13["v111"]["people"])==set(["daram","resident_teacher"]))
    assert eval (r13_v111_value("location:kid_kkomi")=="v111_woodshed" and not r13_v111_actor_ready("kid_kkomi"))
    assert eval (not qa_nw_seen("꼬미가 움찔한다"))
    click pos (900,600) until eval (r13_v111_value("kkomi_seat6") is True) timeout 40
    assert eval (r13_v111_value("school_permission") is True)
    assert eval (r13_v111_value("warehouse_children_school_handover")!=4 and r13_v111_value("FIRE_EVACUATED") is not True)

testcase v111_d456_fire_escort_daram_stays:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",6)
    run Function(r13_v111_set,"FIRE_EVACUATED",False)
    run Function(r13_v111_set,"KKOMI_ALIVE",True)
    run Function(r13_v111_set,"school_day_seat","confirmed")
    run Function(r13_v111_set,"location:daram","v111_fire")
    run Function(r13_edit,location="v111_fire",period=2)
    $ qa_d456_life_before=tuple(r13_v111_value(k) for k in ("KKOMI_ALIVE","BORI_hands","FIRE_EVACUATED"))
    run Jump("r13_v111_fire6")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D06_S03_L0010") timeout 60
    # 보리가 안쪽의 꼬미를 보았다는 진술은 학교 이동 전에 현장에서 듣는다.
    assert eval (room13["location"]=="v111_fire" and r13_packet[0]=="resident_bori")
    assert eval (r13_v111_value("location:resident_bori")=="v111_fire")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="school") timeout 40
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="school")
    click id "r13_map_travel"
    pause until eval (renpy.get_screen("r13_hub") and room13["location"]=="school" and room13["v111"].get("travel_to")=="v111_fire") timeout 45
    assert eval (r13_v111_value("location:daram")=="school")
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="v111_fire")
    click id "r13_map_travel"
    pause until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="wet_cloth6") timeout 45
    # 실제 왕복 뒤 아빠만 구조를 준비한다. 다람과 사건 결과는 임의로 바뀌지 않는다.
    assert eval (room13["location"]=="v111_fire" and r13_v111_value("location:daram")=="school")
    assert eval ("daram" not in room13["v111"]["people"] and not r13_v111_actor_ready("daram"))
    assert eval (tuple(r13_v111_value(k) for k in ("KKOMI_ALIVE","BORI_hands","FIRE_EVACUATED"))==qa_d456_life_before)
