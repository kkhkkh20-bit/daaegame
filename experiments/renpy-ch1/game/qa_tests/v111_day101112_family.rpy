# 11일 재회 전 동행자와 재회 후 가족의 실제 학교 이동을 검사한다.
# 장면 직전 상태만 기존 설정 함수로 준비하고 실제 라벨과 지도 화면을 진행한다.

testcase v111_d101112_reunion_companions:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",11)
    run Function(r13_v111_set,"tosil_safe_handoff_confirmed",True)
    run Function(r13_v111_set,"greenhouse_address_known",True)
    run Function(r13_v111_set,"family_reunited",False)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_set,"location:daram","school")
    run Function(r13_v111_set,"location:mom","greenhouse")
    run Function(r13_edit,location="school",period=0)
    run Jump("r13_v111_reunion11")
    pause until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="greenhouse") timeout 45
    # 아직 만나지 못한 엄마는 학교 출발 동행자로 들어가지 않는다.
    assert eval (companions==["daram"])
    assert eval (room13["location"]=="school" and r13_v111_value("family_reunited") is False)
    assert eval (r13_v111_value("location:mom")=="greenhouse" and r13_v111_value("location:daram")=="school")
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    click id "r13_map_region_mountain"
    click id "map_building_greenhouse"
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="greenhouse")
    click id "r13_map_travel"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D11_S02_L0002") timeout 60
    # 폐온실에 도착한 뒤 엄마가 실제 장면에 합류해 첫 재회 대사를 한다.
    assert eval (room13["location"]=="greenhouse" and r13_packet[0]=="mom")
    assert eval (set(room13["v111"]["people"])==set(["daram","mom"]))
    assert eval (all(r13_v111_value("location:"+p)=="greenhouse" and r13_v111_actor_ready(p) for p in ["daram","mom"]))
    assert eval (r13_v111_value("DARAM_DETAINED") is False)

testcase v111_d101112_family_school_move:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",11)
    run Function(r13_v111_set,"family_reunited",True)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_set,"DARAM_location","with_dad")
    run Function(r13_v111_set,"busy:nabi",None)
    run Function(r13_v111_set,"busy:mom",None)
    run Function(r13_v111_set,"location:daram","facility")
    run Function(r13_v111_set,"location:mom","facility")
    run Function(r13_edit,location="facility",period=1)
    run Function(r13_v111_scene,"MS14_D11_S03")
    run Function(r13_v111_arrive,["daram","mom"])
    run Jump("r13_v111_family_place11")
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="school") timeout 45
    # 대사에서 함께 가기로 한 두 사람이 실제 이동 동행자로도 잡힌다.
    assert eval (qa_nw_seen("학교에 같이 가서 확인하고 올게요") and qa_nw_seen("다람아, 우리도 같이 가자"))
    assert eval (not qa_nw_seen("다람이하고 여기 있을게"))
    assert eval (set(companions)==set(["daram","mom"]))
    assert eval (room13["location"]=="facility")
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    click id "r13_map_region_village"
    keysym "shift_K_UP"
    keysym "shift_K_UP"
    keysym "shift_K_UP"
    pause .5
    click id "map_name_school"
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="school")
    click id "r13_map_travel"
    pause until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="family_place_check11") timeout 60
    assert eval (room13["location"]=="school")
    assert eval (all(r13_v111_value("location:"+p)=="school" and r13_v111_actor_ready(p) for p in ["daram","mom"]))
    assert eval (r13_v111_value("family_reunited") is True and r13_v111_value("DARAM_DETAINED") is False)

    # 같은 자료를 여러 운반 경로에서 쓰므로 원문 보기의 동적 설명도 경로 공통 사실만 남긴다.
    run Function(r13_grant,["V111:E14_SUPPLY"],"qa")
    run Function(r13_v111_set,"school_heat_connected",False)
    assert eval ("학교로 실제 운반한 장작 묶음을 인계했다" in r13_catalog_record("V111:E14_SUPPLY")["establishes"])
    assert eval ("까로" not in r13_catalog_record("V111:E14_SUPPLY")["establishes"] and "선생님" not in r13_catalog_record("V111:E14_SUPPLY")["establishes"])
    run Function(r13_v111_set,"school_heat_connected",True)
    assert eval ("학교에서 실제로 때고 있다" in r13_catalog_record("V111:E14_SUPPLY")["establishes"] and "쓴 양과 남은 양을 확인했다" in r13_catalog_record("V111:E14_SUPPLY")["establishes"])
