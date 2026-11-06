# 소설 개정안의 실제 표시·정보 시점·기존 저장과 결말 경로를 검사한다.
# 시작 상태만 준비하고 대사·이동·완료는 실제 본편 라벨을 실행한다.

testcase novel_d05_letter_read_commit:
    # 봉투를 소지한 것과 새 전문을 들은 것은 다르다. 읽기 전에는 새 지식값이 없고, 읽은 뒤에도 초대장 대조는 플레이어 몫이다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",5)
    run Function(r13_edit,day=5,location="gate",period=1)
    run Function(r13_v111_arrive,["daram","resident_lamplighter"])
    run Function(r13_v111_commit,"MS14_D05_S04_L0005")
    assert eval (r13_v111_owned("E27") and not r13_v111_value("mother_first_contact_read5"))
    run Jump("r13_v111_warning_read5")
    click pos (900,600) until eval (r13_packet and "그날 밤 초롱 씨 오는 길목" in r13_packet[1].replace("\n"," ")) timeout 60
    assert eval (not r13_v111_value("mother_first_contact_read5"))
    assert eval (room13["v111"]["people"]==["daram"])
    screenshot "novel_d05_letter.png"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("mother_first_contact_read5") is True)
    assert eval (r13_v111_owned("E27") and not r13_v111_value("mother_denies_invitation"))
    assert eval (qa_nw_seen("첫날 숲 끝에서 너희 마차를 봤어") and qa_nw_seen("교환함 쪽에서도 너울이 내 발자국을 찾고"))

testcase novel_d11_known_contact:
    # 새 첫답장과 구두전언을 실제로 들은 저장은 첫날 경위를 재설명하지 않고 아이의 기다림에 답한다. 질문 완료값은 보존한다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_edit,location="greenhouse")
    run Function(r13_v111_arrive,["mom","daram"])
    run Function(r13_v111_set,"mother_first_contact_read5",True)
    run Function(r13_v111_set,"mother_contact_relay10",True)
    run Jump("r13_v111_mother_life11")
    click pos (900,600) until eval (r13_packet and "초롱 아저씨가 그저께" in r13_packet[1].replace("\n"," ")) timeout 60
    assert eval (room13["location"]=="greenhouse" and r13_packet[0]=="daram")
    screenshot "novel_d11_waiting.png"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("mother_q_life") is True and room13["v111"].get("gate")=="mother_questions11")
    assert eval (not r13_v111_value("mother_q_invitation") and not r13_v111_value("mother_q_return"))
    assert eval (qa_nw_seen("우리는 벌써 그 여관에 있었잖아") and qa_nw_seen("초롱 아저씨가 그저께"))
    assert eval (all(r13_v111_actor_ready(p) for p in ["mom","daram"]))

testcase novel_d11_legacy_contact:
    # 예전 저장의 E27·봉투값만으로 새 첫날 목격담을 이미 들었다고 소급하지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_edit,location="greenhouse")
    run Function(r13_v111_arrive,["mom","daram"])
    run Function(r13_grant,["V111:E27"],"qa")
    run Function(r13_v111_set,"mother_warning_received",True)
    assert eval (not r13_v111_value("mother_first_contact_read5"))
    run Jump("r13_v111_mother_life11")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D11_S02B_L0023") timeout 60
    assert eval (not qa_nw_seen("마차를 보고도 돌아섰다는 편지는 읽었어"))
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("mother_q_life") is True and room13["v111"].get("gate")=="mother_questions11")
    assert eval (not r13_v111_value("mother_first_contact_read5"))

testcase novel_d14_finish_waiting_portrait:
    # 일반 학교 결말에서만 엄마 앞에서 빈 코를 완성하고 대사 뒤에 상태를 바꾼다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"portrait","unfinished")
    run Function(r13_v111_set,"portrait_waiting_for_mom",True)
    run Jump("r13_v111_cookie14")
    click pos (900,600) until eval (r13_packet and "아이가 조그만 코를 그려 넣는다" in r13_packet[1].replace("\n"," ")) timeout 60
    assert eval (room13["location"]=="school" and r13_v111_value("portrait")=="unfinished")
    assert eval (r13_v111_value("portrait_waiting_for_mom") is True and all(r13_v111_actor_ready(p) for p in ["mom","daram"]))
    screenshot "novel_d14_portrait.png"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D14_S05_L0002") timeout 60
    assert eval (r13_v111_value("portrait")=="child_completed" and r13_v111_value("portrait_waiting_for_mom") is False)
    assert eval (r13_v111_value("ending14")=="morning" and r13_v111_value("night14_lodging")=="school")

testcase novel_d14_legacy_completed_portrait:
    # 이전 저장에서 이미 그린 코는 다시 그리지 않고 엄마와 함께 본다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"portrait","child_completed")
    run Jump("r13_v111_cookie14")
    click pos (900,600) until eval (r13_packet and "엄마 보여 주려고 안 구겨지게" in r13_packet[1].replace("\n"," ")) timeout 60
    assert eval (r13_v111_value("portrait")=="child_completed" and not r13_v111_value("portrait_waiting_for_mom"))
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D14_S05_L0002") timeout 60
    assert eval (not qa_nw_seen("아이가 조그만 코를 그려 넣는다"))
    assert eval (r13_v111_value("ending14")=="morning")

testcase novel_d14_family_route_keeps_portrait:
    # 가족 우선 결말의 입구 숙소는 일반 학교의 코 완성과 연구 약속 장면을 받지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"ending14","family")
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"portrait","unfinished")
    run Function(r13_v111_set,"portrait_waiting_for_mom",True)
    run Function(r13_edit,location="gate")
    run Jump("r13_v111_cookie_gate14")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D14_S05_L0017") timeout 60
    assert eval (r13_v111_value("ending14")=="family" and r13_v111_value("night14_lodging")=="gate")
    assert eval (room13["location"]=="gate" and r13_v111_value("portrait")=="unfinished" and r13_v111_value("portrait_waiting_for_mom") is True)
    assert eval (not qa_nw_seen("남은 돌의 양을 한데 모을 수 있을지") and not qa_nw_seen("아이가 조그만 코를 그려 넣는다"))

testcase novel_d07_corridor_promise:
    # 복도에 실제로 맡긴 뒤 진료소 왕복을 진행한다. 예방 행동과 생존 결과, 귀환 배우 위치를 함께 확인한다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",7)
    run Function(r13_edit,day=7,location="room13",period=2)
    run Function(r13_v111_set,"D07_S02_handover_completed",True)
    run Function(r13_v111_scene,"MS14_D07_S03")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_arrive,["daram","doto","karo","resident_owlgp"])
    run Function(r13_v111_set,"doto_promise7",True)
    run Jump("r13_v111_handover7")
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="clinic") timeout 90
    assert eval (r13_v111_value("corridor_handover7") is True and room13["location"]=="hall")
    assert eval (all(r13_v111_value("location:"+p)=="hall" for p in ["daram","doto"]))
    assert eval (r13_v111_value("DARAM_location")=="hall" and r13_v111_value("DOTO_location")=="hall" and r13_v111_value("DARAM_guardian")=="DOTO")
    assert eval (r13_v111_value("OWL_ALIVE") is True and not r13_v111_value("DARAM_DETAINED"))
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    # 복도에서 연 지도는 여관 구역이다. 마을 탭에서 진료소를 고른다.
    click id "r13_map_region_village"
    pause .3
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="clinic")
    click id "r13_map_travel"
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="school") timeout 90
    assert eval (r13_v111_value("route7")=="prevented" and r13_v111_value("prevention")=="promise")
    assert eval (r13_v111_value("OWL_ALIVE") is True and r13_v111_value("DARAM_DETAINED") is False and r13_v111_value("D07_medical_care")=="complete")
    assert eval (room13["location"]=="hall" and all(r13_v111_value("location:"+p)=="hall" for p in ["daram","doto"]))
    assert eval (r13_v111_value("location:resident_seori")=="room13" and r13_v111_value("location:resident_owlgp")=="room13")
    assert eval (r13_v111_actor_ready("daram") and r13_v111_actor_ready("doto") and not r13_v111_actor_ready("resident_seori"))
    screenshot "novel_d07_corridor_promise.png"

testcase novel_d07_corridor_repair:
    # 복도에 실제로 맡긴 뒤 진료소 왕복을 진행한다. 예방 행동과 생존 결과, 귀환 배우 위치를 함께 확인한다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",7)
    run Function(r13_edit,day=7,location="room13",period=2)
    run Function(r13_v111_set,"D07_S02_handover_completed",True)
    run Function(r13_v111_scene,"MS14_D07_S03")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Function(r13_v111_set,"DARAM_DETAINED",False)
    run Function(r13_v111_arrive,["daram","doto","karo","resident_owlgp"])
    run Function(r13_v111_set,"meeting:lamp","win")
    run Function(r13_v111_set,"TOK_ALIVE",True)
    run Function(r13_v111_set,"owl_tok_work7",True)
    run Function(r13_v111_set,"busy:resident_tok","owl_repair7")
    run Jump("r13_v111_handover7")
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="clinic") timeout 90
    assert eval (r13_v111_value("corridor_handover7") is True and room13["location"]=="hall")
    assert eval (all(r13_v111_value("location:"+p)=="hall" for p in ["daram","doto"]))
    assert eval (r13_v111_value("DARAM_location")=="hall" and r13_v111_value("DOTO_location")=="hall" and r13_v111_value("DARAM_guardian")=="DOTO")
    assert eval (r13_v111_value("OWL_ALIVE") is True and not r13_v111_value("DARAM_DETAINED"))
    click "지도" until screen "r13_map" timeout 30
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 30
    # 복도에서 연 지도는 여관 구역이다. 마을 탭에서 진료소를 고른다.
    click id "r13_map_region_village"
    pause .3
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="clinic")
    click id "r13_map_travel"
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="travel" and room13["v111"].get("travel_to")=="school") timeout 90
    assert eval (r13_v111_value("route7")=="prevented" and r13_v111_value("prevention")=="repair")
    assert eval (r13_v111_value("OWL_ALIVE") is True and r13_v111_value("DARAM_DETAINED") is False and r13_v111_value("D07_medical_care")=="complete")
    assert eval (room13["location"]=="hall" and all(r13_v111_value("location:"+p)=="hall" for p in ["daram","doto"]))
    assert eval (r13_v111_value("location:resident_seori")=="room13" and r13_v111_value("location:resident_owlgp")=="room13")
    assert eval (r13_v111_actor_ready("daram") and r13_v111_actor_ready("doto") and not r13_v111_actor_ready("resident_seori"))
    screenshot "novel_d07_corridor_repair.png"

