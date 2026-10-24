# 2026-10-24 지시서 02 감정선 다섯(docs/reviews/codex-02/적용보고.md): 다섯 장면이 그 판에서 나오는지,
# 위기 장면이 그 일을 비추는 줄을 내는지 본다. 설정 점프는 처음부터 이어 하는 플레이가 아니다.

label qa_bd_elder4:
    $ r13_v111_set("day",4)
    $ r13_edit(day=4,location="ms14_somi")
    $ r13_v111_arrive(['daram','resident_nero','resident_somi'])
    call r13_v111_elder_cane4
    jump r13_v111_sleep4

label qa_bd_kkomi4:
    $ r13_v111_set("day",4)
    $ r13_edit(day=4,location="dining")
    $ r13_v111_arrive(['daram'])
    call r13_v111_kkomi_backdoor4
    jump r13_v111_sleep4

label qa_bd_owl5:
    $ r13_v111_set("day",5)
    $ r13_edit(day=5,location="dining")
    $ r13_v111_arrive(['daram'])
    call r13_v111_owl_glove5
    jump r13_v111_lock_check5

label qa_bd_dodam7:
    call r13_v111_dodam_spoon7
    jump r13_v111_sleep10_input

label qa_bd_crisis_lines:
    # 위기 장면의 비추는 줄만 차례로 부른다(그 판의 값을 먼저 세운다).
    $ r13_edit(location="v111_fire")
    $ r13_v111_arrive(['daram','resident_bori','kid_kkomi'])
    call r13_lines(r13_v111_lines(['MS14_D06_S01_L0020','MS14_D06_S03_L0013']),'qa:bonds:d06')
    $ r13_edit(location="room13")
    $ r13_v111_arrive(['daram','resident_seori','resident_owlgp'])
    call r13_lines(r13_v111_lines(['MS14_D07_S04_L0022','MS14_D07_P01_L0005']),'qa:bonds:d07')
    $ r13_v111_set('lower_road_lost',True)
    $ r13_v111_set('nero_alive',False)
    $ r13_v111_set('alive:v111_lowerroad_elder',False)
    $ r13_edit(location="forest")
    $ r13_v111_arrive(['karo'])
    call r13_lines(r13_nw_block('lower_elder11'),'qa:bonds:d11')
    $ r13_edit(location="square")
    $ r13_v111_arrive(['daram','karo'])
    call r13_lines(r13_nw_block('elder_name12'),'qa:bonds:d12')
    $ r13_v111_arrive(['karo','guard','resident_badook','resident_momo'])
    call r13_lines(r13_v111_lines(['MS14_D13_S04_L0066']),'qa:bonds:d13')
    $ r13_v111_set('riot_momo13',True)
    call r13_lines(r13_nw_block('riot13'),'qa:bonds:d13riot')
    jump r13_v111_sleep10_input

testcase v111_bonds_momo2:
    # 2일 우체국: 모모가 피코에게 가는 길을 알려 주고 먼저 나선다(광장에서 피코의 그림을 거절하는 장면으로 이어진다).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",2)
    run Function(r13_v111_set,"mother_box_checked_day2",True)
    run Function(r13_v111_set,"arrival_note_sent",True)
    run Function(r13_grant,["V111:E07"],"qa")
    run Function(r13_edit,day=2,location="post")
    run Jump("r13_v111_post_return")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("모모 관장님?") and qa_nw_seen("값은 깎지 말고요") and qa_nw_seen("정확한 그림은 무서워요") and qa_nw_seen("먼저 우체국을 나선다"))
    assert eval (not qa_nw_seen("광장 3번 등 아래 화가가 있어요"))

testcase v111_bonds_owl3:
    # 3일 진료소 뒤: 집게를 공방에 돌려주고, 이름 없는 노인(부엉이)에게서 수첩 나눠 적기를 듣는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",3)
    run Function(r13_grant,["V111:E10","V111:E11","V111:E32"],"qa")
    run Function(r13_v111_set,"measurement_separated_from_theft",True)
    run Function(r13_edit,day=3,location="clinic")
    run Jump("r13_v111_measurement_after")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("눈이 둥근 노인") and qa_nw_seen("본 건 왼쪽, 들은 건 오른쪽") and qa_nw_seen("종이 묶음이나 세는"))
    assert eval (not qa_nw_seen("등 번호"))

testcase v111_bonds_elder4:
    # 4일 솜이네 처마: 아랫길 노인의 지팡이 헝겊, 네로가 부르는 「영감」.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("qa_bd_elder4")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("‘영감’이라 하면 그게 이름이지") and qa_nw_seen("오늘도 업혀 왔다") and qa_nw_seen("영감, 안에 들어가 있어요"))

testcase v111_bonds_kkomi4:
    # 4일 밤 식당 뒷문: 꼬미가 연필을 주워 주고, 깡통 세는 버릇을 보인다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("qa_bd_kkomi4")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("하나 받으면 하나 넣어") and qa_nw_seen("그건 안 세") and qa_nw_seen("……꼬미."))
    assert eval ("kid_kkomi" not in (room13["v111"].get("people") or []))

testcase v111_bonds_owl5:
    # 5일 저녁: 같은 노인이 다람의 장갑을 두 땀 꿰매며 이름을 두 번 묻는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("qa_bd_owl5")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("이름이…… 뭐라 했지?") and qa_nw_seen("아까도 말했는데") and qa_nw_seen("두 땀이면 된다"))

testcase v111_bonds_owl7_reunion:
    # 7일 13호: 처음 보는 노인이 아니라 장갑을 꿰매 준 그분으로 다시 만난다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",7)
    run Function(r13_v111_set,"D07_S02_handover_completed",True)
    run Function(r13_edit,day=7,location="room13")
    run Jump("r13_v111_room_visit7")
    click pos (900,600) until "아내 소식을 아십니까" timeout 90
    assert eval (qa_nw_seen("장갑을 꿰매 주던 그분이다") and qa_nw_seen("이번엔 안 잊었지") and qa_nw_seen("부엉이 어르신이셨군요"))
    assert eval (not qa_nw_seen("처음 보는 노인"))

testcase v111_bonds_dodam7:
    # 7일 학교(불 속에서 꼬미를 잃은 판): 도담이 숟가락을 빌려준다. 보리는 손을 데었다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day7)
    run Function(r13_edit,day=7,location="school")
    run Function(r13_v111_arrive,['nabi','resident_bori','resident_teacher'])
    run Jump("qa_bd_dodam7")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("dodam_spoon7") is True and qa_nw_seen("우리 아빠 건 내가 들고 다녀") and qa_nw_seen("손을 데어서"))
    assert eval (not qa_nw_seen("밥 먹을 틈도 없대요"))

testcase v111_bonds_kkomi10:
    # 10일 밤 학교(6일에 꼬미를 살린 판): 새 깡통에 도토리 하나, 다람 주머니에 하나.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"stay")
    run Function(r13_v111_set,"KKOMI_ALIVE",True)
    run Function(r13_v111_arrive,['daram'])
    run Jump("r13_v111_sleep10")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("kkomi_acorn10") is True and qa_nw_seen("내 깡통에 하나, 네 주머니에 하나") and qa_nw_seen("달그락, 한 번"))

testcase v111_bonds_kkomi10_absent:
    # 꼬미를 잃은 판에는 10일 장면이 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"stay")
    run Function(r13_v111_set,"KKOMI_ALIVE",False)
    run Function(r13_v111_arrive,['daram'])
    run Jump("r13_v111_sleep10")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (not r13_v111_value("kkomi_acorn10") and not qa_nw_seen("새 깡통이야"))

testcase v111_bonds_dodam12:
    # 12일 배식 전: 다람이 7일에 빌린 숟가락을 보리 자리에 놓는다. 그 저녁 창가가 그 숟가락을 비춘다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_v111_set,"dodam_spoon7",True)
    run Jump("r13_v111_meal12")
    click pos (900,600) until eval (r13_v111_value("dodam_spoon12") is True) timeout 90
    assert eval (qa_nw_seen("그때 빌린 숟가락 아직 나한테 있어") and qa_nw_seen("우리 아빠 자리에 놔 줘"))
    # 배식 도입이 route12 를 「아직」으로 돌려 두므로, 늦은 폭로 판으로 다시 세운다.
    run Function(r13_v111_set,"route12","late_exposure")
    run Function(r13_v111_set,"KKOMI_ALIVE",True)
    run Function(r13_v111_set,"kkomi_acorn10",True)
    run Jump("r13_v111_late_meal12")
    click pos (900,600) until "네 깡통에 하나랬잖아" timeout 90
    run Function(r13_v111_set,"route12","late_exposure")
    run Function(r13_v111_set,"teacher_confessed",True)
    run Function(r13_v111_set,"school_heat_connected",False)
    run Jump("r13_v111_aftermath_late12")
    click pos (900,600) until "숟가락 두 개가 놓여 있다" timeout 120
    assert eval (qa_nw_seen("불 꺼진 창가"))

testcase v111_bonds_crisis_lines:
    # 6일 불·7일 죽음과 살린 판·11일 지팡이·12일 이름 없는 표·13일 모모의 비추는 줄.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("qa_bd_crisis_lines")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (qa_nw_seen("깡통을 흔들던 아이다") and qa_nw_seen("하나 받으면 하나 넣는다던 깡통이다"))
    assert eval (qa_nw_seen("두 땀이면 된다고 했는데") and qa_nw_seen("장갑을 꿰매 주던 손이다"))
    assert eval (qa_nw_seen("헝겊을 감아 주던 그 지팡이다") and qa_nw_seen("지팡이 짚던 분") and qa_nw_seen("……아무도 몰랐어.") and qa_nw_seen("부르던 거, 나 들었어"))
    assert eval (qa_nw_seen("그 화가한테…… 가 봤어요?") and qa_nw_seen("박물관 열쇠 꾸러미"))
