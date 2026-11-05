# 14일 문밖에서 기다리던 토실과의 재합류, 출발한 수레 뒤 학교 명단 확인 위치를 검사한다.
# 장면 직전 상태만 기존 설정 함수로 준비하고 실제 이야기 선택과 지도 이동을 진행한다.

testcase v111_d1314_tosil_outside_rejoin:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",14)
    run Function(r13_v111_set,"family_reunited",True)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_set,"route7","prevented")
    run Function(r13_v111_set,"prevention","stone")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Function(r13_v111_set,"location:daram","gate")
    run Function(r13_v111_set,"location:mom","gate")
    run Function(r13_edit,location="gate",period=1)
    run Jump("r13_v111_granny_interview14")
    click pos (900,600) until screen "choice" timeout 90
    pause .6
    click id "r13_notebook_choice_2"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D14_S03_L0030") timeout 90
    # 어른 면담 중에는 토실이 문밖에 있으며 현재 면담 발화자로 취급되지 않는다.
    assert eval (r13_v111_value("tosil_listen")=="outside")
    assert eval (r13_v111_value("location:resident_tosil")=="outside_guard")
    assert eval (not r13_v111_actor_ready("resident_tosil"))
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D14_S03_L0038") timeout 90
    # 문밖으로 나온 지문과 실제 합류가 먼저 일어난 뒤 토실의 첫 대답이 나온다.
    assert eval (qa_nw_seen("면담이 끝난 뒤 문밖으로 나와 기다리던 토실 곁에 선다"))
    assert eval (r13_packet[0]=="resident_tosil")
    assert eval (room13["location"]=="gate" and r13_v111_value("location:resident_tosil")=="gate")
    assert eval ("resident_tosil" in room13["v111"]["people"] and r13_v111_actor_ready("resident_tosil"))
    assert eval (r13_v111_value("adult_interview_done") is True and r13_v111_value("bomi_death_confirmed") is True)

testcase v111_d1314_departed_school_records:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",14)
    run Function(r13_v111_set,"family_reunited",True)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_set,"outcome13","partial_rescue")
    run Function(r13_v111_set,"ending14","partial")
    run Function(r13_v111_set,"cart_departed",True)
    run Function(r13_v111_set,"departed:nabi",False)
    run Function(r13_v111_set,"alive:nabi",True)
    run Function(r13_v111_set,"location:nabi","school")
    run Function(r13_v111_set,"location:mom","school")
    run Function(r13_v111_set,"location:daram","square")
    run Function(r13_edit,location="square",period=0)
    run Jump("r13_v111_partial_ending14")
    click pos (900,600) until eval (r13_packet and "수레가 서 있던 자국만 남았다" in r13_packet[1].replace("\n"," ")) timeout 60
    assert eval (room13["location"]=="square")
    click pos (900,600) until eval (r13_packet and "받은 사람 칸이 비어 있다" in r13_packet[1].replace("\n"," ")) timeout 45
    assert eval (room13["location"]=="square" and r13_v111_value("location:nabi")=="school")
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="school") timeout 45
    # 광장 지문 뒤 명단을 확인할 학교까지 실제 지도로 이동한다.
    assert eval (not qa_nw_seen("내리지 못한 이름들은 학교 명단 종이에 그대로 남는다"))
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    keysym "shift_K_UP"
    keysym "shift_K_UP"
    keysym "shift_K_UP"
    pause .5
    click id "map_name_school"
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="school")
    click id "r13_map_travel"
    click pos (900,600) until eval (r13_packet and "학교 명단 종이에 그대로 남는다" in r13_packet[1].replace("\n"," ")) timeout 60
    assert eval (room13["location"]=="school")
    assert eval (all(r13_v111_value("location:"+p)=="school" and r13_v111_actor_ready(p) for p in ["mom","daram","nabi"]))
    click pos (900,600) until eval (r13_packet and "접지 마." in r13_packet[1].replace("\n"," ")) timeout 45
    assert eval (r13_packet[0]=="daram" and r13_v111_actor_ready("daram"))
    assert eval (qa_nw_seen("수레가 서 있던 자국만 남았다") and qa_nw_seen("받은 사람 칸이 비어 있다"))
