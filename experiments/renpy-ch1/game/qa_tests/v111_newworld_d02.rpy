init python:
    def qa_nw_day2_afternoon():
        # 2일 식당 제안(MS14_D02_S04)까지 온 상태. 오후 행동은 아직 하나도 하지 않았다.
        r13_v111_set("day",2)
        r13_grant(["V111:E07","V111:E08"],"qa")
        r13_v111_set("portrait_commissioned",True)
        r13_v111_set("nero_contact_lead",True)
        r13_edit(location="dining",period=1)
        r13_v111_scene("MS14_D02_S04")
    def qa_nw_afternoon_titles(place):
        r13_v111_context("afternoon2")
        return [o["title"] for o in r13_v111_binding()["options"] if o["location"]==place]

testcase v111_nw_d02_afternoon_shelter:
    # 0.20.18 열쇠표 K1: 결과를 적은 메뉴 대신 해 지기 전 실제로 한 일이 피코의 밤을 정한다.
    # 포대와 마른 천을 마쳐야 피코에게 자리를 전할 수 있고, 그 길로 들어가면 피코가 산다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day2_afternoon)
    assert eval (qa_nw_afternoon_titles("dining")==["포대를 옮긴다","네로를 만나러 간다"])
    assert eval (qa_nw_afternoon_titles("square")==[])
    run Jump("r13_v111_afternoon")
    pause 1.0
    assert screen "r13_hub"
    click "나비"
    pause 1.0
    click "포대를 옮긴다"
    click pos (900,600) until eval (r13_v111_value("piko_sacks2") is True and qa_nw_seen("벤치 하나가 빈다")) timeout 30
    assert eval (qa_nw_afternoon_titles("dining")==["네로를 만나러 간다","벤치 표면을 살핀다"] and qa_nw_afternoon_titles("inn")==["마른 천을 빌린다"])
    assert eval (qa_nw_afternoon_titles("square")==[])
    run Function(r13_v111_set,"piko_cloth2",True)
    assert eval (qa_nw_afternoon_titles("square")==[])
    # 벤치 관찰·청소의 실제 조작은 piko_bench_preparation에서 확인한다.
    run Function(r13_v111_set,"piko_bench_seen2",True)
    run Function(r13_v111_set,"piko_bench_clean2",True)
    assert eval (qa_nw_afternoon_titles("square")==["식당에 앉을 자리를 전한다"])
    run Function(r13_v111_apply,"option:afternoon:0",[{'op':'set','field':'D02_afternoon','value':'shelter'}])
    run Jump("r13_v111_shelter_done")
    pause 1.0
    click pos (900,600) until eval (r13_v111_value("piko_sheltered") is True) timeout 60
    assert eval (r13_v111_value("nero_met_day2") is False and qa_nw_seen("네로를 놓쳤다"))
    # 저녁 장면은 이동(지도)을 건너뛰려고 13호에서 판정 지점부터 본다.
    run Function(r13_edit,location="room13",period=2)
    run Jump("r13_v111_evening2_route")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("내일 일찍 가야 돼") and not qa_nw_seen("피코가 깨겠지"))
    assert eval (not qa_nw_seen("해가 지기 전에는 한쪽만") and not qa_nw_seen("오늘 밤도 광장에 남는다"))
    screenshot "v111_nw_d02_shelter.png"

testcase v111_nw_d02_afternoon_half_then_nero:
    # 포대만 옮기고 네로에게 가면 한 일은 남지 않는다. 나비가 그 사실을 한 줄로 말하고, 피코는 밖에 남는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day2_afternoon)
    run Function(r13_v111_set,"piko_sacks2",True)
    run Jump("r13_v111_afternoon")
    pause 1.0
    assert screen "r13_hub"
    click "나비"
    pause 1.0
    click "네로를 만나러 간다"
    click pos (900,600) until eval (qa_nw_seen("포대까지 옮겨 놓고요")) timeout 30
    assert eval (r13_v111_value("D02_afternoon")=="nero")
    screenshot "v111_nw_d02_half_nero.png"
    run Function(r13_v111_set,"piko_sheltered",False)
    run Function(r13_v111_set,"selected_afternoon_work_completed",True)
    run Function(r13_edit,location="room13",period=2)
    run Jump("r13_v111_evening2_route")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("피코가 깨겠지") and not qa_nw_seen("내일 일찍 가야 돼"))

testcase v111_nw_d05_piko_sketch:
    # 0.20.18 연쇄 P1: 2일에 살린 피코가 4일 밤 식당에서 그림을 건네고, 5일 회의에서
    # 그 그림이 겉옷 대조·귀가 진술을 대신한다. 피코가 죽은 판에는 그림이 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_proof_accepts("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["V111:E20","V111:E22","V111:NW_PIKO_SKETCH4"]))
    assert eval (r13_v111_proof_accepts("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["V111:E20","V111:E22","V111:E23","V111:E24","V111:NW_PIKO_SKETCH4"]))
    assert eval (not r13_v111_proof_accepts("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["V111:E20","V111:NW_PIKO_SKETCH4"]))
    run Function(r13_v111_set,"day",4)
    run Function(r13_v111_set,"piko_alive",True)
    run Function(r13_v111_set,"piko.location","clinic")
    run Function(r13_edit,location="dining",period=2)
    run Jump("r13_v111_qa_piko_sketch4")
    pause 1.0
    click pos (900,600) until "숯 선 몇 줄이다" timeout 60
    pause 1.0
    screenshot "v111_nw_d04_piko_sketch.png"
    click pos (900,600) until eval (r13_v111_owned("NW_PIKO_SKETCH4")) timeout 60
    assert eval (qa_nw_seen("애들은 저만큼 안 와요") and r13_v111_value("piko.location")=="clinic")
    run Function(qa_nw_day5,[])
    run Jump("r13_v111_proof5")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E20"
    pause 0.8
    click "QA V111:E22"
    pause 0.8
    click "QA V111:NW_PIKO_SKETCH4"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:gate_post")=="win" and r13_v111_value("listed:bami") is not True)
    assert eval (qa_nw_seen("내가 움켜쥔 데가 딱 여기였소") and qa_nw_seen("그림쟁이 낙서 한 장으로"))
    screenshot "v111_nw_d05_piko_sketch.png"

label r13_v111_qa_piko_sketch4:
    call r13_scene(R13_PLACES["dining"][1],R13_PLACES["dining"][0],"calm")
    call r13_v111_piko_sketch4
label r13_v111_qa_hold:
    pause
    jump r13_v111_qa_hold
