# 지도 반환 계약 검증용 버튼. 게임 상태를 바꾸지 않고 현재 화면의 선택만 돌려준다.
screen qa_wild_pick(value):
    zorder 10000
    textbutton "QA 이동":
        pos (20,640)
        action [Hide("qa_wild_pick"),Return(value)]


testcase v111_wild_three:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"ending14","wild_night")
    run Function(r13_v111_set,"daram_fever12",False)
    run Function(r13_v111_set,"wild_late",1)
    run Jump("r13_v111_wild_climb14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("wild_family")=="three" and qa_nw_seen("우리 셋은"))
    assert eval ("wild_night" in persistent.r13_fork_endings)

testcase v111_wild_no_mom_late:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"ending14","wild_night")
    run Function(r13_v111_set,"daram_fever12",False)
    run Function(r13_v111_set,"wild_late",2)
    run Jump("r13_v111_wild_climb14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("wild_family")=="no_mom" and qa_nw_seen("장갑 한 짝"))
    assert eval ("wild_night" in persistent.r13_fork_endings)

testcase v111_wild_no_mom_fever:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"ending14","wild_night")
    run Function(r13_v111_set,"daram_fever12",True)
    run Function(r13_v111_set,"wild_late",0)
    run Jump("r13_v111_wild_climb14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("wild_family")=="no_mom" and qa_nw_seen("장갑 한 짝"))
    assert eval ("wild_night" in persistent.r13_fork_endings)

testcase v111_wild_alone:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"ending14","wild_night")
    run Function(r13_v111_set,"daram_fever12",True)
    run Function(r13_v111_set,"wild_late",2)
    run Jump("r13_v111_wild_climb14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("wild_family")=="alone" and qa_nw_seen("도토리 두 알"))
    assert eval ("wild_night" in persistent.r13_fork_endings)

testcase v111_wild_entry:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Jump("r13_v111_cookie14")
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_room14") timeout 120
    assert eval (r13_v111_value("ending14")=="wild_night" and qa_nw_seen("밖이 왜 아침 같아") and qa_nw_seen("폐온실"))

testcase v111_wild_partial_hypothesis:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"meeting:hypothesis","partial")
    run Jump("r13_v111_cookie14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("ending14")=="morning" and not qa_nw_seen("밖이 왜 아침 같아"))

testcase v111_wild_partial_altar:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"meeting:altar","partial")
    run Jump("r13_v111_cookie14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("ending14")=="morning" and not qa_nw_seen("밖이 왜 아침 같아"))

testcase v111_wild_route_help:
    pause 1.0
    click "처음부터"
    pause 0.7
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"daram_fever12",True)
    run Jump("r13_v111_wild_night14")
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_room14") timeout 90
    pause 1.0
    click pos (100,550)
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_hall14") timeout 90
    pause 1.0
    assert eval (room13["v111"].get("gate")=="wild_hall14")
    click "도토"
    pause 0.7
    click "도토 씨, 바구니 내려놓으세요."
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_square14") timeout 90
    pause 1.0
    click "바둑이"
    pause 0.7
    click "바둑이 씨, 같이 문을 밉시다."
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_road14") timeout 90
    pause 1.0
    click pos (1230,280) until "돌목" timeout 20
    screenshot "wild-guard.png"
    click "돌목"
    pause 0.7
    click "돌목 씨, 같이 가요. 여기 있으면 안 돼요."
    pause 0.7
    click pos (900,600) until screen "r13_end_card" timeout 90
    assert eval (r13_v111_value("wild_late")==3 and r13_v111_value("wild_family")=="alone")


testcase v111_wild_route_pass:
    pause 1.0
    click "처음부터"
    pause 0.7
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 0.7
    screenshot "wild-field-1.png"
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_v111_set,"meeting:hypothesis","lose")
    run Function(r13_v111_set,"meeting:altar","lose")
    run Function(r13_v111_set,"daram_fever12",False)
    run Jump("r13_v111_wild_night14")
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_room14") timeout 90
    pause 1.0
    pause 0.7
    screenshot "wild-field-2.png"
    click pos (100,550)
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_hall14") timeout 90
    pause 1.0
    pause 0.7
    screenshot "wild-field-3.png"
    assert eval (room13["v111"].get("gate")=="wild_hall14")
    click "지도"
    pause 0.7
    run Show("qa_wild_pick",value="square")
    pause 0.3
    click "QA 이동"
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_square14") timeout 90
    pause 1.0
    pause 0.7
    screenshot "wild-field-4.png"
    click "지도"
    pause 0.7
    run Show("qa_wild_pick",value="forest")
    pause 0.3
    click "QA 이동"
    pause 0.7
    click pos (900,600) until eval (room13["v111"].get("gate")=="wild_road14") timeout 90
    pause 1.0
    pause 0.7
    screenshot "wild-field-5.png"
    run Show("qa_wild_pick",value=("object","forest_roots"))
    pause 0.3
    click "QA 이동"
    pause 0.7
    click pos (900,600) until screen "r13_end_card" timeout 90
    assert eval (r13_v111_value("wild_late")==0 and r13_v111_value("wild_family")=="three")
