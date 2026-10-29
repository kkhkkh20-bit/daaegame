# 2026-10-25 대사 검수에서 고친 분기 대사를 그 판에서 실제로 보이는지 확인한다.

testcase dr25_lamp_attempt_owl:
    # 등 미수판은 진료소·집게 반납을 지나지 않는다. 공방에서 부엉이를 만나야 5·7일 대사의 근거가 선다.
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_la_meeting_setup)
    run Function(r13_v111_set,'meeting:lamp','win')
    run Jump('r13_lamp_attempt_after3')
    click pos (900,600) until eval qa_nw_seen('세로줄을 하나 긋는다') timeout 60
    assert eval (qa_nw_seen('회의 내내 거기 있었던') and qa_nw_seen('본 건 왼쪽, 들은 건 오른쪽'))

testcase dr25_lamp_attempt_store:
    # 등 미수판 창고: 자료로 얻는 안쪽 돌 값·창고지기 날짜가 장면으로도 나온다(11일 가설 회의 근거).
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_la_setup)
    run Jump('r13_lamp_attempt3')
    click pos (900,600) until eval (room13['v111'].get('gate')=='lamp_attempt_field3') timeout 60
    pause 0.8
    run Function(r13_edit,location='store')
    run Show('qa_hidden_base_return',value=('person','resident_madam'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '매입 장부와 약속하신 값을 보여 주시겠습니까?'
    click pos (900,600) until eval r13_v111_value('lamp_store_done3') timeout 30
    assert eval (qa_nw_seen('안쪽 돌은 세 배예요') and qa_nw_seen('같은 것을 또 묻는다') and qa_nw_seen('식당 위층에서 살아요') and r13_v111_owned('NW_KEEPER_DATE'))

testcase dr25_kkomi10_carried:
    # 6일에 깡통을 안고 나온 판: 10일에 「새 깡통」이라 하지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"stay")
    run Function(r13_v111_set,"KKOMI_ALIVE",True)
    run Function(r13_v111_set,"kkomi_can_seen6",True)
    run Function(r13_v111_set,"acorn_recovered",True)
    run Function(r13_v111_arrive,['daram'])
    run Jump("r13_v111_sleep10")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_nw_seen("창고에서 안고 나온 그 깡통") and not qa_nw_seen("새 깡통이야") and qa_nw_seen("달그락, 한 번"))
