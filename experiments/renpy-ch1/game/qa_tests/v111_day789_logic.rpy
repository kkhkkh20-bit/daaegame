# 8일 학교 인계와 구금 유지, 9일 예방 경로의 실제 서류 대조 인물 위치를 검사한다.
# 장면 직전 상태만 기존 설정 함수로 준비하고, 이동과 조사 선택은 실제 화면으로 진행한다.

testcase v111_d789_day8_school_handoff:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",8)
    run Function(r13_v111_set,"route7","prevented")
    run Function(r13_v111_set,"prevention","stone")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_set,"location:daram","room13")
    run Function(r13_v111_set,"location:nabi","school")
    run Function(r13_v111_set,"busy:nabi",None)
    run Function(r13_edit,location="room13",period=0)
    run Jump("r13_v111_mother_letter8")
    pause until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="school") timeout 45
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    # 13호에서 열면 여관 지도이므로 마을 지도를 고른 뒤 학교 이름표를 누른다.
    click id "r13_map_region_village"
    keysym "shift_K_UP"
    keysym "shift_K_UP"
    keysym "shift_K_UP"
    pause .5
    click id "map_name_school"
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="school")
    click id "r13_map_travel"
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="square") timeout 60
    # 지문만 말하고 지나가지 않고, 학교에 두 인물이 실제로 도착한 뒤 인계한다.
    assert eval (room13["location"]=="school")
    assert eval (set(room13["v111"]["people"])==set(["daram","nabi"]))
    assert eval (all(r13_v111_value("location:"+p)=="school" and r13_v111_actor_ready(p) for p in ["daram","nabi"]))
    assert eval (r13_v111_value("DARAM_location")=="school" and r13_v111_value("busy:nabi")=="daram_guard")
    assert eval (qa_nw_seen("다람은 학교에 데려다주고 나비에게 맡긴다"))
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="square")
    click id "r13_map_travel"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D08_S04_L0002") timeout 60
    assert eval (room13["location"]=="square" and "daram" not in room13["v111"]["people"])
    assert eval (r13_v111_value("location:daram")=="school" and not r13_v111_actor_ready("daram"))
    assert eval (r13_v111_value("location:nabi")=="school" and r13_v111_value("busy:nabi")=="daram_guard")
    assert eval (r13_v111_value("DARAM_DETAINED") is False and r13_v111_value("OWL_ALIVE") is True)

testcase v111_d789_day8_custody_stays:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",8)
    run Function(r13_v111_set,"route7","murder")
    run Function(r13_v111_set,"OWL_ALIVE",False)
    run Function(r13_v111_set,"DARAM_DETAINED",True)
    run Function(r13_v111_set,"DARAM_location","custody_room")
    run Function(r13_v111_set,"location:daram","v111_custody")
    run Function(r13_v111_set,"location:nabi","school")
    run Function(r13_v111_set,"busy:nabi",None)
    run Function(r13_edit,location="clinic",period=0)
    run Jump("r13_v111_mother_letter8")
    pause until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel") timeout 45
    # 구금된 다람을 학교에 옮기거나 나비를 보호 담당으로 바꾸지 않는다.
    assert eval (room13["v111"].get("travel_to")=="square")
    assert eval (r13_v111_value("DARAM_DETAINED") is True and r13_v111_value("DARAM_location")=="custody_room")
    assert eval (r13_v111_value("location:daram")=="v111_custody" and r13_v111_value("busy:nabi") is None)
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="square")
    click id "r13_map_travel"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D08_S04_L0002") timeout 60
    assert eval (room13["location"]=="square" and "daram" not in room13["v111"]["people"])
    assert eval (r13_v111_value("DARAM_DETAINED") is True and r13_v111_value("DARAM_location")=="custody_room")
    assert eval (r13_v111_value("location:daram")=="v111_custody" and r13_v111_value("OWL_ALIVE") is False)
    assert eval (not qa_nw_seen("다람은 학교에 데려다주고 나비에게 맡긴다"))

testcase v111_d789_day9_returned_papers_people:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",9)
    run Function(r13_v111_set,"route7","prevented")
    run Function(r13_v111_set,"prevention","stone")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_set,"location:daram","school")
    run Function(r13_v111_set,"location:resident_owlgp","room13")
    run Function(r13_v111_set,"DARAM_location","school")
    run Function(r13_v111_set,"location:nabi","school")
    run Function(r13_v111_set,"busy:nabi","daram_guard")
    run Function(r13_edit,location="school",period=0)
    run Jump("r13_v111_prevent_passage9")
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="kitchen") timeout 45
    # 주방으로 가는 나비는 학교 선생님에게 먼저 인계하고 보호 중 상태를 해제한다.
    assert eval (qa_nw_seen("나비가 선생님에게 다람을 맡긴다"))
    assert eval (room13["location"]=="school" and r13_v111_value("location:daram")=="school")
    assert eval (r13_v111_value("location:resident_teacher")=="school" and r13_v111_value("busy:nabi") is None)
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    click id "r13_map_region_inn"
    click id "map_room_kitchen"
    click id "r13_map_travel"
    pause until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="safe_prevent9") timeout 45
    assert eval (r13_v111_value("location:nabi")=="kitchen" and r13_v111_value("busy:nabi") is None)
    assert eval (r13_v111_value("location:daram")=="school" and r13_v111_value("location:resident_teacher")=="school")
    click pos (48,276) until eval (r13_world_offset()<5) timeout 20
    pause .8
    $ qa_d789_rear=r13_object_target_rect("rear",ROOM13["objects"]["kitchen"]["rear"])
    click pos (qa_d789_rear[0]+qa_d789_rear[2]//2-r13_world_offset(),qa_d789_rear[1]+qa_d789_rear[3]//2)
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="room13") timeout 90
    assert eval (r13_v111_owned("E09_PASSAGE") and r13_v111_value("TTADAK_ALIVE") is True)
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="room13")
    click id "r13_map_travel"
    pause until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="papers_check9") timeout 45
    assert eval (room13["location"]=="room13")
    assert eval (set(room13["v111"]["people"])==set(["resident_owlgp","granny"]))
    assert eval (all(r13_v111_value("location:"+p)=="room13" and r13_v111_actor_ready(p) for p in ["resident_owlgp","granny"]))
    click pos (1232,276) until eval (r13_world_offset()>=r13_world_width()-1280-5) timeout 20
    pause .8
    $ qa_d789_books=r13_object_target_rect("books",ROOM13["objects"]["room13"]["books"])
    click pos (qa_d789_books[0]+qa_d789_books[2]//2-r13_world_offset(),qa_d789_books[1]+qa_d789_books[3]//2)
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D09_P01_L0013") timeout 60
    assert eval (r13_packet[0]=="resident_owlgp" and r13_v111_actor_ready("resident_owlgp"))
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D09_P01_L0020") timeout 45
    assert eval (r13_packet[0]=="granny" and r13_v111_actor_ready("granny"))
    assert eval (r13_v111_value("location:daram")=="school" and r13_v111_value("DARAM_DETAINED") is False)
