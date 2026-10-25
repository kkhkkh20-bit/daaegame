# 2026-10-24 대승리 두 곳(docs/design/GRAND_WIN_DESIGN.md 추천안, 결정 4·7). 보고서 docs/reviews/grand-win-20261024/적용보고.md
# 두 길로 배급표 얻기, 그릇 얻기, 대체 정답으로 대승리, 기본 정답으로 보통 이김, 13일 보상, 국을 미리 막은 판의 대체, 진엔딩 조건.
# 설정 점프는 처음부터 이어 하는 플레이가 아니다.
init python:
    def qa_gw_options(gate):
        r13_v111_context(gate)
        return [o["title"] for o in r13_v111_binding().get("options",[])]
    def qa_gw_true_ready(**values):
        for k,v in values.items():r13_v111_set(k,v)
        return r13_nw_true_ending_ready()

# 사람을 눌러 고른 질문과 같은 길(대기 화면이 돌려준 번호로 부르는 레이블)을 그대로 부른다.
label qa_gw_snack7:
    call r13_v111_nubi_snack7
    jump r13_v111_nubi_children_receipt7
label qa_gw_guard12:
    call r13_v111_early_guard_bowl12
    jump r13_v111_early_bowl12_wait

testcase v111_gw_laundry_overhear5:
    # 5일 저녁: 여관 가는 길 이동 대기에 빨래터가 한 자리 더 열린다(표시 없음). 빨래 줄에 장갑을 걸면 엿듣는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",5)
    run Function(r13_edit,day=5,location="dining",period=2)
    $ room13["v111"]["travel_to"]="inn"
    $ room13["v111"]["travel_detour"]="laundry"
    assert eval (qa_gw_options("travel")==["여관 접수대","마을 빨래터"])
    $ room13["v111"]["travel_detour"]=None
    assert eval (qa_gw_options("travel")==["여관 접수대"])
    run Function(r13_edit,location="laundry")
    run Jump("r13_v111_laundry5")
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval ("빨래 줄에 젖은 장갑을 건다" in qa_gw_options("laundry5"))
    pause 1.0
    click "빨래 줄"
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_owned("NW_LAUNDRY_TALK") and r13_v111_value("grand_ticket_spot_known") is True)
    assert eval (qa_nw_seen("빨래 줄에 잠깐 걸어 말리고 가자") and qa_nw_seen("그 창고가 비면, 그 몫은 당신 집으로 가오") and qa_nw_seen("밑의 홈에 종이를 밀어 넣는다"))
    assert eval (qa_gw_options("laundry5")==["여관 접수대"])

testcase v111_gw_ticket_from_drum7:
    # 7일 빨래터: 숨긴 자리를 모르는 판은 기름통에 손댈 수 없고, 아는 판만 통 밑 홈을 들춘다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",7)
    run Function(r13_edit,day=7,location="laundry",period=0)
    assert eval (qa_gw_options("bori_witness7")==["창고 문 앞에서 무엇을 보셨습니까?"])
    run Function(r13_v111_set,"grand_laundry_seen5",True)
    run Function(r13_v111_set,"grand_ticket_spot_known",True)
    assert eval (qa_gw_options("bori_witness7")==["창고 문 앞에서 무엇을 보셨습니까?","기름통을 살핀다","통 밑 홈을 들춘다"])
    run Jump("r13_v111_bori_witness7")
    click pos (900,600) until screen "r13_hub" timeout 60
    pause 1.0
    click "등유 통"
    pause 1.0
    click "통 밑 홈을 들춘다"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_owned("NW_NUBI_TICKET") and qa_nw_seen("젖은 종이 한 장이 눌려 있다") and qa_nw_seen("어디서 본 글씨다"))
    assert eval (qa_gw_options("bori_witness7")==["창고 문 앞에서 무엇을 보셨습니까?"])

testcase v111_gw_snack_kid7:
    # 둘째 길: 7일 학교에서 다람이 막내에게 과자를 나누면, 막내가 숨긴 자리를 말한다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",7)
    run Function(r13_edit,day=7,location="school",period=0)
    run Function(r13_v111_arrive,["nabi","resident_teacher","daram"])
    assert eval ("막내가 네 가방만 보고 있네." not in qa_gw_options("nubi_children_receipt7"))
    # 2026-10-25 결정 11: 5일 밤 과자 봉지를 가방에 넣어 둔 판에서만 열린다.
    run Function(r13_v111_set,"snack_bagged5",True)
    run Function(r13_v111_set,"grand_snack_ready7",True)
    assert eval ("막내가 네 가방만 보고 있네." in qa_gw_options("nubi_children_receipt7"))
    run Jump("qa_gw_snack7")
    click pos (900,600) until eval (r13_v111_value("grand_ticket_spot_kid") is True) timeout 90
    assert eval (qa_nw_seen("큰 건 엄마 거야") and qa_nw_seen("솥 옆 통 밑에 넣었어") and r13_v111_value("grand_ticket_spot_known") is True)
    # 막내에게서 들은 판도 같은 손대기가 열린다(속말은 막내 쪽).
    run Function(r13_edit,location="laundry")
    assert eval ("통 밑 홈을 들춘다" in qa_gw_options("bori_witness7"))
    assert eval (R13_NW_WHEN["ticket_spot_kid7"]() and not R13_NW_WHEN["laundry_overheard5"]())

testcase v111_gw_fire_grand:
    # 7일 불 회의 2번: 배급표가 누비 진술 자리를 대신하면 이기고 대승리가 적힌다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day7)
    run Function(r13_grant,["V111:NW_NUBI_TICKET"],"qa")
    run Function(r13_v111_set,"bori_nubi_door_witness_heard",True)
    run Function(r13_edit,location="school")
    run Function(r13_v111_arrive,["nabi","resident_bori","resident_nubi","neoul"])
    run Jump("r13_v111_rescue_fire_basis7")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E06_FIRE"
    pause 0.8
    click "QA V111:E06_RESCUE"
    pause 0.8
    click "QA V111:NW_NUBI_TICKET"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until eval (qa_nw_seen("너울이 이번에는 그 종이를 본다")) timeout 120
    assert eval (r13_v111_value("meeting:fire")=="win" and r13_v111_value("grand:fire") is True and r13_v111_value("neoul_promise_proven") is True)
    assert eval (qa_nw_seen("기록철 사이에 끼운다") and not qa_nw_seen("끝까지 그 종이를 보지 않는다"))

testcase v111_gw_fire_plain:
    # 기본 정답(누비 진술)으로는 지금처럼 이기고, 대승리는 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day7)
    run Function(r13_v111_set,"bori_nubi_door_witness_heard",True)
    run Function(r13_edit,location="school")
    run Function(r13_v111_arrive,["nabi","resident_bori","resident_nubi","neoul"])
    run Jump("r13_v111_rescue_fire_basis7")
    pause 1.5
    click "자료 고르기"
    pause 0.5
    click "QA V111:E06_FIRE"
    pause 0.8
    click "QA V111:E06_RESCUE"
    pause 0.8
    click "QA V111:E07_NUBI"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until eval (qa_nw_seen("끝까지 그 종이를 보지 않는다")) timeout 120
    assert eval (r13_v111_value("meeting:fire")=="win" and r13_v111_value("grand:fire") is not True and r13_v111_value("neoul_promise_proven") is not True)
    assert eval (not qa_nw_seen("기록철 사이에 끼운다"))

testcase v111_gw_bowl_cart11:
    # 11일 광장: 짐칸을 비우며 그릇 상자를 내리고(첫 클릭), 다시 눌러 고르면 하나를 주머니에 넣는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_edit,location="square")
    run Function(r13_v111_arrive,["daram","karo","resident_nero"])
    run Jump("r13_v111_rescue_cart11")
    click pos (900,600) until screen "r13_hub" timeout 60
    pause 1.0
    click "손수레"
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("grand_bowl_seen11") is True and not r13_v111_value("grand_bowl_pocket") and qa_nw_seen("학교로 돌려보내는 그릇이에요"))
    pause 1.0
    click "손수레"
    pause 1.0
    click "그릇 하나를 집는다"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("grand_bowl_pocket") is True and qa_nw_seen("외투 주머니에 넣는다"))

testcase v111_gw_soup_grand:
    # 12일: 배식대 옆에 그릇을 놓아 본 판에서만 자료가 되고, 3번 쟁점을 그 그릇으로 이기면 칸이 무효가 된다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12,"premeal_stopped")
    run Function(r13_v111_set,"bowls_carried12",True)
    assert eval (qa_gw_options("bottle_match12")==["병과 파편의 경계를 대조한다"])
    run Function(r13_v111_set,"grand_bowl_pocket",True)
    run Function(r13_v111_arrive,["daram","nabi","resident_teacher"])
    $ r13_world_cameras={"school":520}
    run Jump("r13_v111_bottle_match12")
    click pos (900,600) until screen "r13_hub" timeout 60
    pause 1.0
    click "작은 배식대"
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_owned("NW_RETURNED_BOWL") and qa_nw_seen("어제 수레에서 내린 그릇이랑 같은 거네"))
    run Function(r13_v111_set,"teacher_confessed",True)
    run Function(r13_grant,["V111:NW_WHITE_BOWLS"],"qa")
    run Function(r13_v111_arrive,["daram","nabi","resident_teacher","resident_seori","resident_bori","guard","neoul"])
    run Jump("r13_v111_list_proof12")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_WHITE_BOWLS"
    pause 0.8
    click "QA V111:NW_RETURNED_BOWL"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until eval (qa_nw_seen("명단 원본을 문 옆에서 떼어")) timeout 120
    assert eval (r13_v111_value("meeting:soup")=="win" and r13_v111_value("grand:soup") is True and r13_v111_value("transfer_list_voided") is True)
    assert eval (qa_nw_seen("실려 간 사람 몫이던 그릇만") and qa_nw_seen("이 칸은 무효로 적겠소"))

testcase v111_gw_soup_plain:
    # 기본 정답(명단+흰 그릇)으로는 지금처럼 이기고 무효는 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12,"premeal_stopped")
    run Function(r13_v111_set,"teacher_confessed",True)
    run Function(r13_grant,["V111:NW_TRANSFER_LIST","V111:NW_WHITE_BOWLS"],"qa")
    run Function(r13_v111_arrive,["daram","nabi","resident_teacher","resident_seori","resident_bori","guard","neoul"])
    run Jump("r13_v111_list_proof12")
    pause 1.5
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_TRANSFER_LIST"
    pause 0.8
    click "QA V111:NW_WHITE_BOWLS"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until eval (qa_nw_seen("명단 원본을 문 옆에서 떼어")) timeout 120
    assert eval (r13_v111_value("meeting:soup")=="win" and r13_v111_value("grand:soup") is not True and r13_v111_value("transfer_list_voided") is not True)
    assert eval (not qa_nw_seen("이 칸은 무효로 적겠소"))

testcase v111_gw_early_guard12:
    # 12일 국을 미리 막은 판: 수프 회의가 없다. 같은 그릇을 돌목에게 보이면 수프 대승리를 대신한다(결정 7).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12,"early_prevented")
    run Function(r13_v111_set,"grand_bowl_pocket",True)
    run Function(r13_grant,["V111:NW_TRANSFER_LIST"],"qa")
    run Function(r13_v111_arrive,["daram","mom","nabi","resident_teacher","karo","kid_dodam","kid_saemi"])
    $ r13_world_cameras={"school":520}
    run Jump("r13_v111_early_bowl12")
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval ("이 그릇 바닥의 표시는 무엇입니까?" not in qa_gw_options("early_bowl12"))
    pause 1.0
    click "작은 배식대"
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_owned("NW_RETURNED_BOWL") and "이 그릇 바닥의 표시는 무엇입니까?" in qa_gw_options("early_bowl12"))
    run Jump("qa_gw_guard12")
    click pos (900,600) until eval (r13_v111_value("grand:soup") is True) timeout 90
    assert eval (r13_v111_value("transfer_list_voided") is True and r13_v111_value("meeting:soup") is None)
    assert eval (qa_nw_seen("실려 간 사람 몫 그릇만 학교로 돌려보내오") and qa_nw_seen("……돌아온 적은 없소"))

testcase v111_gw_void_stop13:
    # 13일 수레를 세우면 무효 칸으로 실린 사람이 모두 내린다(실룩·굴돌은 다른 까닭이라 남는다).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"meeting:blanket","win")
    run Function(r13_nw_list,"daram","room13_lose")
    run Function(r13_nw_list,"resident_bori","fire_partial")
    run Function(r13_nw_list,"resident_siluk","lamp_transfer")
    run Function(r13_v111_set,"transfer_list_voided",True)
    run Jump("r13_v111_stop_cart13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 120
    assert eval (r13_v111_value("handed:daram") is True and r13_v111_value("handed:resident_bori") is True and r13_v111_value("void_down:resident_bori") is True)
    assert eval (not r13_v111_value("handed:resident_siluk") and qa_nw_seen("그 칸으로 오른 사람은 내리시오"))
    assert eval (not qa_nw_seen("까로가 다람의 손목 끈을 푼다"))

testcase v111_gw_void_blanket_lost13:
    # 담요 회의를 진 판: 수레는 떠나지만 무효 칸 사람은 싣지 않는다. 다람도 남는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"false_message_admitted",False)
    run Function(r13_nw_list,"daram","room13_lose")
    run Function(r13_nw_list,"resident_tok","lamp_lose")
    run Function(r13_v111_set,"transfer_list_voided",True)
    run Function(r13_v111_set,"tries:blanket",r13_nw_tries_max("blanket")-1)
    run Jump("r13_v111_mending_wrong13")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:blanket")=="lose" and r13_v111_value("departed:npc_pandol") is True)
    assert eval (r13_v111_value("departed:daram") is not True and r13_v111_value("departed:resident_tok") is not True)
    assert eval (qa_nw_seen("떠나기 전에 짐칸에서 내렸다") and not qa_nw_seen("아무도 내리지 못한다") and not qa_nw_seen("바퀴가 더 빠르다"))

testcase v111_gw_crowd_record13:
    # 불 대승리의 보상: 13일 군중 앞에서 7일 회의 기록을 함께 읽으면 너울이 살고 장부를 넘긴다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"neoul_promise_proven",True)
    run Function(r13_v111_set,"grand:fire",True)
    run Function(r13_flag,"v111:entered:MS14_D13_C")
    run Jump("r13_v111_crowd13")
    click pos (900,600) until "7일 회의 기록을 함께 읽는다" timeout 90
    assert eval qa_nw_seen("때리면 저 사람 장부도 같이 묻혀요")
    click "7일 회의 기록을 함께 읽는다"
    click pos (900,600) until "학교 침상과 인수를 먼저 확인한다" timeout 90
    assert eval (r13_v111_value("alive:neoul") is not False and r13_v111_value("crowd_injury") is False and r13_v111_value("outcome13")=="all_rescued")
    assert eval (r13_v111_owned("NW_NEOUL_LEDGER") and r13_v111_value("NW_NEOUL_LEDGER.variant")=="surrendered" and qa_nw_seen("내가 적은 건 다 거기 있소"))

testcase v111_gw_crowd_no_record13:
    # 보통 이김(약속을 말로만 적은 판)에는 그 선택지가 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"fire_neoul_promise_recorded",True)
    run Function(r13_flag,"v111:entered:MS14_D13_C")
    run Jump("r13_v111_crowd13")
    click pos (900,600) until "주민들을 말리지 않는다" timeout 90
    assert eval (not qa_nw_seen("7일 회의 기록을 함께 읽는다") and not qa_nw_seen("때리면 저 사람 장부도"))

testcase v111_gw_true_ending:
    # 진엔딩 조건: 아침 결말·사망 0·장부·네 회의 이김 위에 불·수프 대승리.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_grant,["V111:NW_NEOUL_LEDGER"],"qa")
    assert eval (not qa_gw_true_ready(ending14="morning",**{"meeting:records":"win","meeting:hypothesis":"win","meeting:blanket":"win","meeting:altar":"win"}))
    assert eval (not qa_gw_true_ready(**{"grand:fire":True}))
    assert eval (qa_gw_true_ready(**{"grand:soup":True}))
    assert eval (not qa_gw_true_ready(**{"grand:fire":None}))
