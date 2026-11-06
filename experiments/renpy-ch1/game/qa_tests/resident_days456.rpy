# 사건 결과 직후의 상태만 준비하고, 학교 귀환과 주민 반응은 본편을 실행한다.
init python:
    def qa_resident6_after_fire(evacuated):
        r13_v111_set('day',6)
        r13_edit(day=6,location='v111_fire',period=2)
        if evacuated:
            r13_v111_commit('MS14_D06_P01_L0024')
            r13_v111_commit('MS14_D06_S03P_L0008')
        else:
            r13_v111_set('FIRE_EVACUATED',False)
            r13_v111_commit('MS14_D06_S03_L0022')
        r13_v111_set('location:daram','school')


testcase resident6_safe_hands:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_resident6_after_fire,True)
    run Jump('r13_v111_after_fire6')
    pause 1.0
    click pos (900,600) until screen 'r13_hub' timeout 30
    click "지도" until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    assert eval (renpy.get_screen('r13_map').scope['selected']=='school')
    click id 'r13_map_travel'
    click pos (900,600) until eval (r13_packet and '도담이 소매를 잡고 기다린다' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('KKOMI_ALIVE') is True and r13_v111_value('warehouse_children_school_handover')==4)
    assert eval (r13_v111_value('BORI_hands')!='burned' and not qa_nw_seen('아빠가 들게…… 아니, 조금만 더 들어 주렴.'))
    screenshot "resident6_safe_hands.png"
    click pos (900,600) until eval (room13['v111'].get('gate')=='travel' and room13['v111'].get('travel_to')=='v111_ruin') timeout 90
    assert eval (r13_v111_value('KKOMI_ALIVE') is True)


testcase resident6_burned_hands:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_resident6_after_fire,False)
    run Jump('r13_v111_after_fire6')
    pause 1.0
    click pos (900,600) until screen 'r13_hub' timeout 30
    click "지도" until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    assert eval (renpy.get_screen('r13_map').scope['selected']=='school')
    click id 'r13_map_travel'
    click pos (900,600) until eval (r13_packet and '보리가 고개를 숙여 한 모금 마신다' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('KKOMI_ALIVE') is False and r13_v111_value('warehouse_children_rescued')==3)
    assert eval (r13_v111_value('BORI_hands')=='burned' and not qa_nw_seen('보리가 밥그릇으로 뻗던 손을 멈추고 자기 손바닥을 한 번 뒤집어 본다.'))
    screenshot "resident6_burned_hands.png"
    click pos (900,600) until eval (room13['v111'].get('gate')=='travel' and room13['v111'].get('travel_to')=='v111_ruin') timeout 90
    assert eval (r13_v111_value('KKOMI_ALIVE') is False and r13_v111_value('warehouse_children_rescued')==3)


testcase resident4_chair_and_correction:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,'day',4)
    run Function(r13_edit,day=4,location='gate',period=2)
    run Function(r13_grant,['V111:E19'],'qa')
    run Function(r13_v111_set,'afternoon_visit_declined',True)
    run Function(r13_v111_scene,'MS14_D04_S03')
    run Function(r13_v111_arrive,['daram','guard','neoul','resident_badook'])
    run Jump('r13_v111_bite4')
    click pos (900,600) until eval (r13_packet and '나는 의자를 문 옆으로 돌려 놓는다' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (r13_v111_owned('E20') and not qa_nw_seen('밤이가 문 거 아니야'))
    screenshot "resident4_chair.png"
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(r13_edit,location='ms14_guardroom')
    run Function(r13_v111_scene,'MS14_D04_S04')
    run Function(r13_v111_arrive,['daram','resident_badook','bami'])
    run Jump('r13_v111_bami_night4')
    click pos (900,600) until eval (r13_packet and '나한테만 말하면 뭐 해' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_packet[0]=='bami' and r13_v111_owned('E21'))
    assert eval (qa_nw_seen('그건 못 봤어') and not r13_v111_value('rumor_not_eyewitness'))
    screenshot "resident4_correction.png"
    click pos (900,600) until screen 'r13_hub' timeout 90
    assert eval (r13_v111_value('rumor_not_eyewitness') is True)
