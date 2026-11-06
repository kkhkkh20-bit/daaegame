# 시작 상태를 준비한 뒤 새 가설·자료 제출·재조사·기존 자백 경계를 실제 화면으로 확인한다.
init python:
    def qa_fire_deduction7():
        qa_resident789(7)
        r13_edit(location='laundry')
        r13_grant(['V111:E06_FIRE','V111:E06_RESCUE'],'qa')
        r13_v111_scene('MS14_D07_S01')
        r13_v111_arrive(['resident_nubi','resident_bori'])


testcase fire7_hypothesis_rebut_and_submit:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Call('qa_rr_scene','r13_v111_bori_witness_heard7')
    click pos (900,600) until screen 'choice' timeout 60
    assert eval (r13_v111_value('fire_lamp_defense_heard') is True and not r13_v111_value('NUBI_admitted_setting_fire'))
    screenshot 'fire7_hypothesis.png'
    pause .4
    keysym 'K_1'
    click pos (900,600) until screen 'choice' timeout 60
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_owned('E07_NUBI'))
    pause .4
    keysym 'K_3'
    click pos (900,600) until screen 'choice' timeout 60
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_value('fire_origin_hypothesis'))
    pause .4
    keysym 'K_2'
    pause until screen 'r13_proof_workspace' timeout 45
    screenshot 'fire7_evidence.png'
    pause .4
    click id 'r13_pw_check_E06_FIRE'
    pause .4
    click id 'r13_pw_submit'
    click pos (900,600) until eval (r13_packet and '문 앞 흔적을 설명할 수 없습니다' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (not r13_v111_owned('E07_NUBI') and not r13_v111_value('NUBI_admitted_setting_fire'))
    screenshot 'fire7_checked.png'
    click pos (900,600) until eval (r13_packet and '가져간다고 안 했어요' in r13_packet[1].replace('\n',' ')) timeout 90
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E07_NUBI') and r13_v111_value('NUBI_admitted_setting_fire') is True and r13_v111_value('NUBI_intent_to_kill')=='unproven')


testcase fire7_investigate_retry:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    # 이전 판에서 자료 대조 직전에 저장한 경우 새 진술부터 보완한다.
    run Call('qa_rr_scene','r13_v111_nubi_proof7')
    click pos (900,600) until screen 'choice' timeout 60
    pause .4
    keysym 'K_2'
    pause until screen 'r13_proof_workspace' timeout 45
    pause .4
    click id 'r13_pw_check_E06_FIRE'
    click id 'r13_pw_investigate'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_value('NUBI_admitted_setting_fire'))
    click '보리'
    click '창고 문 앞에서 무엇을 보셨습니까?'
    click pos (900,600) until screen 'r13_proof_workspace' timeout 60
    assert eval (room13['arguments'][v111_claim]==['V111:E06_FIRE'])
    pause .4
    click id 'r13_pw_check_E06_FIRE'
    pause .4
    click id 'r13_pw_check_E06_RESCUE'
    pause .4
    click id 'r13_pw_submit'
    click pos (900,600) until screen 'r13_proof_workspace' timeout 60
    assert eval (r13_v111_value('tries:fire')==1 and not r13_v111_owned('E07_NUBI'))
    screenshot 'fire7_retry.png'
    pause .4
    click id 'r13_pw_check_E06_FIRE'
    pause .4
    click id 'r13_pw_submit'
    click pos (900,600) until eval (r13_packet and '문 앞 흔적을 설명할 수 없습니다' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (r13_v111_value('tries:fire')==1 and not r13_v111_owned('E07_NUBI'))


testcase fire7_old_success_entry:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Call('qa_rr_scene','r13_v111_nubi_first_question7')
    click pos (900,600) until eval (r13_packet and '문 앞 흔적을 설명할 수 없습니다' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (r13_v111_value('fire_lamp_defense_heard') is True and not r13_v111_owned('E07_NUBI'))
    click pos (900,600) until eval (r13_packet and '가져간다고 안 했어요' in r13_packet[1].replace('\n',' ')) timeout 90
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E07_NUBI') and r13_v111_value('NUBI_intent_to_kill')=='unproven')
