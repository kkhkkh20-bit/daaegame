# 2026-10-24 행동 검수 반영(docs/reviews/action-review-20261024/적용보고.md): 넣은 줄이 그 경로에서 실제로 나오는지,
# 「생각」 칸이 이동 중에 도착할 장면의 문구를 미리 보이지 않는지 본다.
init python:
    def qa_ar_scene(day,scene,location,period=1,*later):
        """그 날 그 장면을 이미 보인 상태(대기에 닿아 「생각」을 보인 뒤)로 세운다. later 장면은 진입 검사를 건너뛴다."""
        r13_v111_set("day",day)
        r13_edit(day=day,location=location,period=period)
        r13_flag(*["v111:entered:"+s for s in (scene,)+later])
        store.room13["v111"]["scene"]=scene
        r13_v111_context("qa_seen")

testcase v111_ar_thought_travel:
    # 4일 저녁: 처마 장면(D04_S02)에서 초소로 가는 동안 「생각」은 처마 문구를 유지한다(비명 장면 문구
    # 「초소 뒤에서 누가 다친 걸까?」를 미리 보이지 않는다). 도착 뒤 바뀌는 것은 v111_ar_d03_clinic_to_square 가 본다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_ar_scene,4,"MS14_D04_S02","square",1,"MS14_D04_S03")
    assert eval (r13_v111_goal()==R13_V111_QUESTIONS["MS14_D04_S02"])
    run Jump("r13_v111_cry4")
    pause until screen "r13_hub" timeout 30
    assert eval (room13["v111"]["gate"]=="travel" and room13["v111"]["scene"]=="MS14_D04_S03")
    assert eval (r13_v111_goal()==R13_V111_QUESTIONS["MS14_D04_S02"] and "초소 뒤" not in r13_v111_goal())
    screenshot "v111_ar_thought_travel.png"

testcase v111_ar_d03_clinic_to_square:
    # 3일 진료소 끝: 집게를 공방에 돌려주러 나서는 까닭(3-2)이 나오고, 광장으로 가는 동안 「생각」은 진료소 문구다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_ar_scene,3,"MS14_D03_S03","clinic",1,"MS14_D03_S04")
    run Jump("r13_v111_measurement_after")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 90
    assert eval (qa_nw_seen("집게는 공방에 갖다줘요") and qa_nw_seen("가는 길에 톡 씨한테도 알리고요"))
    assert eval (r13_v111_goal()==R13_V111_QUESTIONS["MS14_D03_S03"] and "돌려주기 전에" not in r13_v111_goal())
    # 광장에 도착해 첫 대기에 닿으면 「생각」이 광장 장면 문구로 바뀐다.
    click "지도" until screen "r13_map" timeout 30
    pause 0.6
    click id "map_name_square"
    pause 0.4
    click id "r13_map_travel"
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (room13["location"]=="square" and room13["v111"].get("gate")!="travel" and not room13["v111"].get("thought_pending"))
    assert eval (r13_v111_goal()==R13_V111_QUESTIONS["MS14_D03_S04"])

testcase v111_ar_d05_iron:
    # 5일 저녁(소유자 결정 4·5-1): 3일에 톡이 풀려난 판, 식당에 까로가 있고 쇠 토막을 묻는다. 밤이를 풀어 준 판은
    # 아빠가 솜이에게 할아버지 옷 이야기를 꺼낸 것을 털어놓는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_ar_scene,5,"MS14_D05_S04","ms14_somi_inside",2,"MS14_D05_S05")
    run Function(r13_v111_set,"meeting:lamp","win")
    run Function(r13_v111_set,"meeting:gate_post","win")
    run Jump("r13_v111_night5")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 90
    assert eval (qa_nw_seen("할아버지 옷 이야기는 아저씨가 했어") and qa_nw_seen("옷 이야기를 아저씨가 꺼냈어"))
    click "지도" until screen "r13_map" timeout 30
    click "여관 안"
    pause 0.5
    pause 0.6
    click id "map_room_dining"
    pause 0.4
    click id "r13_map_travel"
    click pos (900,600) until eval (room13["location"]=="dining" and room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 90
    assert eval (qa_nw_seen("쇠 토막은 어디서 구합니까") and qa_nw_seen("고개 소식부터 보죠") and qa_nw_seen("내일 물자 알아보는 동안"))

testcase v111_ar_d10_motive:
    # 10일 13호 회의 고백 갈래(소유자 결정 1): 할머니가 다람이 남은 밤에 움직인 까닭.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Jump("r13_v111_contact_answer10")
    click pos (900,600) until eval (qa_nw_seen("머리 상처까지 아이에게 떠넘길 수는 없습니다")) timeout 180
    assert eval (qa_nw_seen("왜 하필 그 밤이었습니까") and qa_nw_seen("아이 손에 촛대가 있으면, 아무도 늙은이를 안 봐요"))

testcase v111_ar_d13_deal:
    # 13일 입구→광장(13-3), 거래 전 판돌(13-4 가), 조건을 더 물으면 빈칸(13-4 나), 수첩 목표 칸(소유자 결정 2).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(qa_ar_scene,13,"MS14_D13_S01","gate",0,"MS14_D13_S02")
    assert eval (r13_goal_state()[1]==1 and r13_goal_state()[0][1]=="엄마를 지킨다" and r13_goal_state()[2]!="명단에 빈칸이 있는 한, 다음은 누구든 될 수 있다.")
    run Jump("r13_v111_gate_bench13")
    click pos (900,600) until eval (room13["v111"].get("gate")=="travel" and renpy.get_screen("r13_hub")) timeout 90
    assert eval (qa_nw_seen("광장에 이송 수레가 섰소") and qa_nw_seen("나도 서류를 들고 가야 하오"))
    click "지도" until screen "r13_map" timeout 30
    pause 0.6
    click id "map_name_square"
    pause 0.4
    click id "r13_map_travel"
    click pos (900,600) until "조건을 더 묻는다" timeout 90
    assert eval (qa_nw_seen("판돌 아저씨가 수레에 있어") and qa_nw_seen("아침에 학교에서 떨던 그분이"))
    assert eval (r13_goal_state()[2]=="명단에 빈칸이 있는 한, 다음은 누구든 될 수 있다." and r13_goal_state()[1]==1)
    click "조건을 더 묻는다"
    click pos (900,600) until "조건을 더 묻는다" timeout 90
    # 수첩 선택지는 페이지별로 보인다. 실제 다음 버튼으로 수락 항목까지 간다.
    click "다음 →" until "가족 셋이 수락하고 물러난다" timeout 10
    assert eval (qa_nw_seen("그 칸엔 누가 들어갑니까") and qa_nw_seen("빈칸이 있는 한 또 누가 적혀"))

testcase v111_ar_d13_crowd_menu:
    # 13일 군중 메뉴 글(13-11): 갈래는 그대로, 뜻이 하나로 읽히는 글.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_flag,"v111:entered:MS14_D13_C")
    run Jump("r13_v111_crowd13")
    click pos (900,600) until "너울을 몸으로 감싼다" timeout 90
    screenshot "v111_ar_d13_crowd_first.png"
    click "다음 →" until "돌목에게 너울을 맡긴다" timeout 10
    screenshot "v111_ar_d13_crowd_guard.png"
    click "다음 →" until "주민들을 말리지 않는다" timeout 10
    screenshot "v111_ar_d13_crowd_menu.png"

testcase v111_ar_d14_frozen_after_hyp:
    # 얼어붙은 마을(대안 9): 가설 회의를 이긴 판에만 「다 같이 끄기로 하지 않았습니까」 문답이 붙는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"KKOMI_ALIVE",False)
    run Function(r13_v111_set,"nero_alive",False)
    run Function(r13_v111_set,"meeting:hypothesis","win")
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("ending14")=="frozen" and qa_nw_seen("왜 다시 돌을 켭니까") and qa_nw_seen("장작 때문에 죽은 게 아닙니다") and qa_nw_seen("이름을 읽던 나비가"))
