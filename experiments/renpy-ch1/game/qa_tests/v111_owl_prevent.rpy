# 2026-10-25 부엉이 예방 1단계(docs/design/OWL_PREVENTION_DESIGN.md 9장, 7장 1단계)와 결정 10·11.
# 보고서 docs/reviews/owl-prevention-20261024/적용보고.md
# 첫 판 기본 흐름(살인 → 13호 회의), 난로 돌 바꾸기·숨기기, 도토 다짐, 예방판 8~10일 변형 줄, 제단 1번 대체 정답, 과자 길 조건.
# 설정 점프는 처음부터 이어 하는 플레이가 아니다.
init python:
    def qa_op_day7(**values):
        r13_v111_set("day",7)
        r13_edit(day=7,location="school",period=1)
        r13_v111_set("D07_S02_handover_completed",True)
        for k,v in values.items():r13_v111_set(k,v)
    def qa_op_options(gate):
        r13_v111_context(gate)
        return [o["title"] for o in r13_v111_binding().get("options",[]) if o.get("location")==room13["location"]]
    def qa_op_at(place):
        r13_edit(location=place)
        return qa_op_options("free_day7")

label qa_op_pick(n):
    call r13_v111_free_day7_pick(n)
    jump r13_v111_free_day7_wait

testcase v111_op_free_day7_places:
    # 학교 → 13호 사이에 낮 자유 시간이 열린다. 아무 표시 없이, 그 자리에 가야 그 자리의 행동이 보인다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_op_day7)
    run Jump("r13_v111_free_day7")
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (qa_nw_seen("해 지려면 아직 멀었다") and room13["v111"]["gate"]=="free_day7")
    assert eval (qa_op_at("school")==["다람아, 이제 13호에 가 보자."])
    assert eval (qa_op_at("hall")==["돌 바구니가 무거워 보입니다.","아래서 누가 부르면 어떻게 하십니까?"])
    # 0.20.4x 빗장 받이 수리(owl_repair)가 13호에 선택 하나를 더했다. 그 뒤로 이 기대값이 낡아 있었다.
    assert eval (qa_op_at("room13")==["난로를 살핀다","재받이를 들여다본다","13호 빗장 받이를 살핀다"])
    assert eval (qa_op_at("workshop")==["집게 하나만 빌릴 수 있을까?","버리는 문고리 부품을 살핀다"])  # 숨은 장소(hidden_base) 시작점이 뒤에 더해졌다
    assert eval (set(r13_places())>={"school","hall","room13","workshop"})

testcase v111_op_first_run_murder:
    # 아무것도 하지 않은 첫 판: 메뉴 없이 다람을 도토에게 맡기고(걷지 못함·서리는 직접 불러야 함) 살인으로 간다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_op_day7)
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_room_visit7")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 150
    assert eval (r13_v111_value("route7")=="murder" and r13_v111_value("fate:fate_owl")=="lost" and r13_v111_value("choice:MS14_D07_S03")=="C")
    assert eval (qa_nw_seen("머리가 띵해") and qa_nw_seen("가슴팍을 누른다") and qa_nw_seen("내 말만 듣고는 안 나와요") and qa_nw_seen("다리가 이상해") and qa_nw_seen("업고는 못 지나가요") and qa_nw_seen("아이는 제가 보죠"))
    assert eval (not qa_nw_seen("다람과 남고") and not qa_nw_seen("제가 다녀오면 되니까"))

testcase v111_op_stone_swap:
    # 난로 돌 바꾸기: 공방 집게 → 13호 재받이의 배급 돌 → 난로에서 바꿔 넣기. 저녁에 부엉이가 무너지지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_op_day7)
    run Function(r13_edit,location="workshop")
    run Call("qa_op_pick",6)
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("tongs7") is True and qa_nw_seen("할아버지 집게예요"))
    run Function(r13_edit,location="room13")
    run Call("qa_op_pick",3)
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (qa_nw_seen("낮인데도 불빛이 푸르스름하다"))
    # 난로와 재받이는 13호 오른쪽 벽(책장 너머)에 있다. 화면을 오른쪽 끝까지 민다.
    click "오른쪽 구역" until "재받이" timeout 20
    pause 1.0
    screenshot "op_room13_right.png"
    click "재받이"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("pocket_ration7") is True and qa_nw_seen("표시가 또렷하고"))
    assert eval (qa_op_options("free_day7")==["난로를 살핀다","집게로 돌을 꺼내고, 주머니의 배급 돌을 넣는다","13호 빗장 받이를 살핀다"])
    pause 0.5
    click "난로"
    pause 0.8
    click "집게로 돌을 꺼내고, 주머니의 배급 돌을 넣는다"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("stove13_7")=="ration" and r13_v111_owned("NW_STONE") and r13_v111_value("NW_STONE.variant")=="swapped")
    assert eval (qa_op_options("free_day7")==["난로를 살핀다","13호 빗장 받이를 살핀다"])
    run Jump("r13_v111_room_visit7")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 150
    assert eval (r13_v111_value("route7")=="prevented" and r13_v111_value("prevention")=="stone" and r13_v111_value("OWL_ALIVE") is True and r13_v111_value("fate:fate_owl")=="stone")
    assert eval (qa_nw_seen("훈훈하다") and qa_nw_seen("목도리 끝을 여민다") and qa_nw_seen("본 건 왼쪽, 들은 건 오른쪽") and qa_nw_seen("난로를 보고 있다"))
    assert eval (not qa_nw_seen("아빠, 머리가 띵해") and not qa_nw_seen("가슴팍을 누른다") and not qa_nw_seen("서리를 좀 데려와"))

testcase v111_op_stone_hide:
    # 숨기기: 배급 돌 없이 집게로 꺼내 눈에 묻는다. 저녁에 도토가 식은 난로에 배급 돌을 새로 넣는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_op_day7,tongs7=True)
    run Function(r13_edit,location="room13")
    assert eval (qa_op_options("free_day7")==["난로를 살핀다","재받이를 들여다본다","집게로 돌을 꺼낸다","13호 빗장 받이를 살핀다"])
    run Call("qa_op_pick",7)
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("stove13_7")=="empty" and qa_nw_seen("검푸르게 타는 돌을 꺼낸다") and qa_nw_seen("머리가 맑아진다"))
    run Jump("r13_v111_room_visit7")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 150
    assert eval (r13_v111_value("prevention")=="stone" and qa_nw_seen("고개를 갸웃한다") and qa_nw_seen("훈훈하다") and not qa_nw_seen("가슴팍을 누른다"))

testcase v111_op_promise:
    # 도토 다짐: 낮에 다짐을 받은 판. 부엉이는 무너지고 아빠는 서리를 부르러 가지만, 도토가 거짓 부름에 내려가지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_op_day7)
    run Function(r13_edit,location="hall")
    run Call("qa_op_pick",2)
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("doto_promise7") is True and qa_nw_seen("누가 불러도 내려가지 말아") and qa_nw_seen("그럼 저도 그렇게 하죠"))
    assert eval (qa_op_options("free_day7")==["돌 바구니가 무거워 보입니다."])
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_room_visit7")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 150
    assert eval (qa_nw_seen("가슴팍을 누른다") and qa_nw_seen("다리가 이상해") and r13_v111_value("route7") in (None,"uncommitted"))
    run Function(r13_edit,location="clinic")
    run Jump("r13_v111_promise_night7")
    click pos (900,600) until eval (r13_v111_value("prevention")=="promise" and room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 150
    assert eval (r13_v111_value("route7")=="prevented" and r13_v111_value("prevention")=="promise" and r13_v111_value("OWL_ALIVE") is True and r13_v111_value("DARAM_DETAINED") is False and r13_v111_value("fate:fate_owl")=="promise")
    assert eval (qa_nw_seen("학교 애가 다쳤다고요") and qa_nw_seen("문간에서 대답만 했더니") and qa_nw_seen("난로 불빛만 푸르다") and not qa_nw_seen("안쪽에서 빗장이 걸렸습니다"))

testcase v111_op_promise_day8:
    # 다짐 판의 8일: 예전 B 판처럼 서리가 돌을 꺼내고, 너울은 「혼자 빗장까지 걸려 했다」를 든다(너울·할머니를 세운 뒤).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",8)
    run Function(r13_edit,day=8,location="room13")
    run Function(r13_v111_set,"route7","prevented")
    run Function(r13_v111_set,"prevention","promise")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Jump("r13_v111_prevent_clinic8")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 150
    assert eval (qa_nw_seen("어제보다는 낫네") and qa_nw_seen("부지깽이로 돌 하나를 꺼낸다") and qa_nw_seen("혼자 빗장까지 걸려 했다지") and qa_nw_seen("아프셨다는 이유로"))
    assert eval (not qa_nw_seen("같은 말을 두 번씩 묻는 노인") and r13_v111_value("NW_STONE.variant")=="clinic")

testcase v111_op_stone_day8:
    # 돌을 꺼낸 판의 8일: 서리는 없고, 부엉이가 다람에게 「본 것과 들은 것」을 가르친다. 할머니가 이른 말로 너울이 명단을 꺼낸다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",8)
    run Function(r13_edit,day=8,location="room13")
    run Function(r13_v111_set,"route7","prevented")
    run Function(r13_v111_set,"prevention","stone")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Function(r13_nw_acquire,"NW_STONE","swapped")
    run Jump("r13_v111_prevent_clinic8")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 150
    assert eval (qa_nw_seen("들은 말은 오른쪽에 따로 적거라") and qa_nw_seen("여기가 비었군") and qa_nw_seen("같은 말을 두 번씩 묻는 노인") and qa_nw_seen("저도 그럽니다"))
    assert eval (not qa_nw_seen("어제보다는 낫네") and not qa_nw_seen("무너지시는 건") and not qa_nw_seen("빗장까지"))
    assert eval (r13_v111_value("NW_STONE.variant")=="swapped")

testcase v111_op_stone_days9_11:
    # 돌을 꺼낸 판의 9·10·11일 변형 줄: 「편찮으셨던」「병든」「쓰러진 뒤」를 쓰지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"prevention","stone")
    run Function(r13_v111_set,"OWL_ALIVE",True)
    run Function(r13_v111_set,"meeting:records","lose")
    assert eval (r13_v111_lines(["MS14_D09_P01_L0011"])[0][1].startswith("어르신이 13호에서 기다리시던"))
    assert eval (r13_v111_lines(["MS14_D09_P01_L0015"])[0][1].startswith("다들 그러겠지. 깜빡하는"))
    assert eval ([l[1] for l in r13_v111_lines(["MS14_D10_P01_L0085"]) if "노인이오" in l[1]]==["그리고……{w=.4} 같은 말을 두 번씩 묻는 노인이오.\n혼자 둘 수 없소. 이송 명단에 올리겠소."])
    assert eval (not any("방 때문일" in l[1] for l in r13_v111_lines(["MS14_D10_P01_L0085"])))
    assert eval ([l[1] for l in r13_nw_block("hyp5_won11") if "7일" in l[1]]==["7일 낮 13호 난로에 이 돌이 들어 있었습니다. 그 앞에 잠깐 앉았을 뿐인데, 하려던 일을 잊었습니다."])
    assert eval (not any("반밖에 기억" in l[1] for l in r13_nw_block("hyp5_won11")))
    run Function(r13_v111_set,"prevention","promise")
    assert eval (r13_v111_lines(["MS14_D09_P01_L0011"])[0][1].startswith("어르신이 편찮으셨던"))
    assert eval (any("반밖에 기억" in l[1] for l in r13_nw_block("hyp5_won11")) and any("8일 서리 씨가" in l[1] for l in r13_nw_block("hyp5_won11")))

testcase v111_op_murder_ashbin8:
    # 살인 판 8일: 재받이에서 도토가 넣은 배급 돌이 나온다(다음 판의 단서). 누가 꺼냈는지는 말하지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"route7","murder")
    run Function(r13_v111_set,"OWL_ALIVE",False)
    assert eval (any("재받이를 헤집자" in l[1] for l in r13_v111_lines(["MS14_D08_S02_L0011"])) and any("누가 꺼내서 재에 묻었네요" in l[1] for l in r13_v111_lines(["MS14_D08_S02_L0011"])))

testcase v111_op_altar_alternate:
    # 결정 10: 장부가 없는 판에도 장작 인수·창고 아이들·침상 목록으로 제단 1번을 이긴다. 장작 기록만이면 지금처럼 반쪽.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_proof_accepts("희생의 숫자와 장부를 대조한다",["NW_NEOUL_LEDGER"],["V111:E14_SUPPLY","V111:NW_KKOMI_NOSTONE","V111:NW_SICK_BEDS"]))
    assert eval (not r13_v111_proof_accepts("희생의 숫자와 장부를 대조한다",["NW_NEOUL_LEDGER"],["V111:E14_SUPPLY","V111:NW_SICK_BEDS"]))
    assert eval (r13_v111_proof_accepts("희생의 숫자와 장부를 대조한다",["NW_NEOUL_LEDGER"],["V111:NW_NEOUL_LEDGER"]))
    run Function(qa_nw_day14)
    run Function(r13_edit,location="gate")
    run Function(r13_grant,["V111:E14_SUPPLY","V111:NW_KKOMI_NOSTONE","V111:NW_SICK_BEDS","V111:NW_TABLET_A","V111:NW_TABLET_B"],"qa")
    run Function(r13_v111_set,"proof_given:희생의 숫자와 장부를 대조한다",["V111:E14_SUPPLY","V111:NW_KKOMI_NOSTONE","V111:NW_SICK_BEDS"])
    run Jump("r13_v111_altar1_won14")
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("altar_issue:1")=="won" and qa_nw_seen("보낼 사람이 생기지 않습니다") and not qa_nw_seen("너울 씨 장부입니다"))
    # 대체 정답을 노리다 하나를 빠뜨린 제출은 반쪽으로 끝나지 않고 기회를 쓴다.
    run Function(r13_v111_set,"altar_issue:1",None)
    run SetVariable("v111_last_presented",["V111:E14_SUPPLY","V111:NW_SICK_BEDS"])
    run Jump("r13_v111_altar1_wrong14")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:altar")==1 and not r13_v111_value("altar_half1"))

testcase v111_op_snack_condition:
    # 결정 11: 다람의 과자 길은 5일 밤 접시의 과자 봉지를 가방에 넣어 둔 판에서만 열린다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",5)
    run Function(r13_edit,day=5,location="room13",period=2)
    assert eval (qa_op_options("lock_check5")==["문과 창문 잠금을 확인한다","책상 접시를 본다"])
    run Function(r13_v111_set,"day",7)
    run Function(r13_edit,day=7,location="school",period=0)
    run Function(r13_v111_set,"location:daram",None)  # 시험 시작이 1일 입구라 다람 자리를 비운다(7일에는 학교에 있다)
    run Jump("r13_v111_nubi_children_school7")
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("grand_snack_ready7") is False and "막내가 네 가방만 보고 있네." not in qa_op_options("nubi_children_receipt7"))
    run Function(r13_v111_set,"snack_bagged5",True)
    run Function(r13_edit,location="school")
    run Jump("r13_v111_nubi_children_school7")
    pause 1.5
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("grand_snack_ready7") is True and "막내가 네 가방만 보고 있네." in qa_op_options("nubi_children_receipt7"))

testcase v111_op_snack_plate5:
    # 5일 밤 접시를 본 판: 다람이 과자 봉지를 가방에 넣는 장면. 보지 않은 판은 그 장면이 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (not any("가방에 넣는다" in l[1] for l in r13_v111_lines(["MS14_D05_S05_L0060"])) and r13_v111_lines(["MS14_D05_S05_L0063"])[0][1].startswith("나는 종이에"))
    run Function(r13_v111_set,"day",5)
    run Function(r13_edit,day=5,location="room13",period=2)
    run Call("r13_v111_snack_plate5")
    click pos (900,600) until eval (r13_v111_value("snack_bagged5") is True) timeout 60
    assert eval (qa_nw_seen("첫날 마차에서 남긴 과자 봉지"))
    assert eval (any("가방에 넣는다" in l[1] for l in r13_v111_lines(["MS14_D05_S05_L0060"])) and r13_v111_lines(["MS14_D05_S05_L0063"])[0][1].startswith("다람이가 봉지 속"))
