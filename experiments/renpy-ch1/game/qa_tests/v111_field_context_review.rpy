# 일반 유저 검토: 담당자 접근과 물건 클릭이 같은 원래 행동을 시작하는지 본다.
label qa_field_review_guard4:
    $ qa_ar_scene(4,"MS14_D04_S03","gate",2)
    $ r13_v111_arrive(['daram','guard','neoul','resident_badook'])
    call r13_scene(R13_PLACES['gate'][1],R13_PLACES['gate'][0],'calm')
    jump r13_v111_look_gate4

label qa_field_review_can6:
    $ qa_ar_scene(6,"MS14_D06_S02","v111_woodshed",1)
    $ r13_v111_arrive(['daram','kid_kkomi','resident_bori'])
    $ r13_v111_set('kkomi_seat6',True)
    $ r13_v111_set('kkomi_can_wait6',True)
    call r13_scene(R13_PLACES['v111_woodshed'][1],R13_PLACES['v111_woodshed'][0],'calm')
    jump r13_v111_afternoon6

testcase v111_field_review_guard_approach:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump('qa_field_review_guard4')
    pause until screen 'r13_hub' timeout 30
    click "오른쪽 구역" until "돌목" timeout 20
    screenshot 'v111_field_review_guard_before.png'
    click "돌목"
    click pos (900,600) until eval (r13_v111_owned('E20')) timeout 30
    assert eval (qa_nw_seen('돌목 씨, 어디를 다치셨습니까?'))
    click pos (900,600) until eval (qa_nw_seen('물었소. 팔을')) timeout 30
    screenshot 'v111_field_review_guard_after.png'

testcase v111_field_review_can_once:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump('qa_field_review_can6')
    pause until screen 'r13_hub' timeout 30
    click "오른쪽 구역" until "깡통 줄 · 살피기" timeout 20
    screenshot 'v111_field_review_can_before.png'
    click "깡통 줄 · 살피기"
    click pos (900,600) until eval (renpy.get_screen('r13_hub') and r13_v111_value('acorn_recovered') is True) timeout 45
    assert eval (r13_v111_value('kkomi_can_seen6') is True)
    assert eval (r13_v111_value('choice:MS14_D06_S02') is None)
    assert eval (r13_v111_value('FIRE_EVACUATED') is not True)
    screenshot 'v111_field_review_can_after.png'
