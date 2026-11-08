# 준비한 조사 상태에서 실제 가설·제출·처리 라벨과 현장 인물을 검사한다.
init python:
    def qa_piko112_meeting():
        qa_nw_day3_meeting_ready()
        r13_edit(day=3,period=1,location='workshop')
        r13_v111_set('piko_alive',False)
        r13_v111_set('public_stones','store')
        r13_v111_set('location:buri','workshop')
        r13_v111_scene('MS14_D03_S05')
        r13_v111_arrive(['neoul','resident_tok','resident_siluk','daram'])

    def qa_piko112_outcome():
        # 실제 완승 뒤 돌 반환을 택한 지점의 진입 상태다.
        qa_piko112_meeting()
        r13_v111_set('lamp_theft_supported',True)
        r13_v111_set('stone_choice_completed',True)
        r13_v111_set('public_stones','returned_uninstalled')
        r13_v111_set('meeting:lamp','win')


testcase piko112_latch_hypothesis_and_retry:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_piko112_meeting)
    run Call('qa_rr_scene','r13_v111_knife_fit')
    click pos (900,600) until screen 'r13_proof_workspace' timeout 60
    assert eval (r13_v111_owned('E33') and r13_v111_owned('E17') and not r13_v111_value('lamp_theft_supported'))
    pause 1.0
    screenshot 'piko112-direct-evidence.png'
    pause .5
    click id 'r13_pw_next' until eval (renpy.get_widget('r13_proof_workspace','r13_pw_check_E17') is not None) timeout 20
    click id 'r13_pw_check_E17'
    pause .4
    click id 'r13_pw_submit'
    click pos (900,600) until screen 'r13_proof_workspace' timeout 60
    assert eval (r13_v111_value('tries:lamp')==1 and not r13_v111_value('lamp_latch_question3') and not r13_v111_value('lamp_theft_supported'))
    pause .5
    click id 'r13_pw_next' until eval (renpy.get_widget('r13_proof_workspace','r13_pw_check_E32') is not None) timeout 20
    click id 'r13_pw_check_E32'
    click id 'r13_pw_next' until eval (renpy.get_widget('r13_proof_workspace','r13_pw_check_E33') is not None) timeout 20
    click id 'r13_pw_check_E33'
    pause .4
    screenshot 'piko112-evidence.png'
    click id 'r13_pw_submit'
    click pos (900,600) until eval (r13_packet and '그 수리는 고쳐야겠죠' in r13_packet[1].replace('\n',' ')) timeout 60
    screenshot 'piko112-repair-responsibility.png'
    click pos (900,600) until eval (v111_claim=='v111:마지막 점검과 인수한 돌을 연결한다' and renpy.get_screen('r13_proof_workspace')) timeout 60
    assert eval (r13_v111_value('tries:lamp')==1 and not r13_v111_value('lamp_theft_supported'))
    assert eval (r13_v111_value('proof_given:바깥 걸쇠 주장과 발견 위치를 대조한다')==['V111:E17','V111:E32','V111:E33'])


testcase piko112_children_transfer:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_piko112_outcome)
    run Function(r13_v111_set,'meeting:lamp','win')
    run Call('qa_rr_scene','r13_v111_silluk_transfer')
    click pos (900,600) until eval (r13_packet and '아이들한테 금방 온다고 하지 말고' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (not r13_v111_value('listed:resident_siluk') and not r13_v111_value('piko_custody_heard3:buri') and r13_v111_value('silluk.children.location')=='workshop_with_buri')
    screenshot 'piko112-children-transfer.png'
    click pos (900,600) until screen 'r13_hub' timeout 90
    assert eval (r13_v111_value('listed:resident_siluk') is True and r13_v111_value('silluk_status')=='detained_work_waiting_station' and r13_v111_value('piko_custody_heard3:buri')=='transfer')
    assert eval (r13_v111_value('silluk.children.location')=='workshop_with_buri')


testcase piko112_children_report:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_piko112_outcome)
    run Function(r13_v111_set,'meeting:lamp','win')
    run Call('qa_rr_scene','r13_v111_silluk_report')
    click pos (900,600) until eval (r13_packet and '아이들은 아직 안에 있어요' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('silluk.children.location')=='workshop_with_buri')
    screenshot 'piko112-children-report.png'
    click pos (900,600) until screen 'r13_hub' timeout 90
    assert eval (r13_v111_value('silluk_status')=='reporting_obligation' and not r13_v111_value('listed:resident_siluk') and r13_v111_value('piko_custody_heard3:buri')=='report')
    assert eval (r13_v111_value('silluk.children.location')=='workshop_with_buri')


testcase piko112_absent_caregiver:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_piko112_meeting)
    run Function(r13_v111_set,'meeting:lamp','win')
    run Function(r13_v111_set,'alive:buri',False)
    run Call('r13_v111_piko_children_response3','transfer')
    pause .5
    assert screen 'r13_hub'
    assert eval (not r13_v111_value('piko_custody_heard3:buri') and r13_v111_value('alive:buri') is False)


testcase piko112_daram_at_body:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_piko_scene_start)
    run Jump('r13_v111_day3')
    click pos (900,600) until screen 'r13_piko_scene' timeout 90
    pause .4
    click id 'r13_piko_daram'
    click pos (900,600) until eval (r13_packet and '아빠는 여기서 자지 마' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (r13_ep_cut_current=='piko-death3' and not r13_v111_value('piko_scene_read:daram'))
    screenshot 'piko112-daram-body.png'
    click pos (900,600) until screen 'r13_piko_scene' timeout 45
    assert eval (r13_v111_value('piko_scene_read:daram') is True and r13_v111_value('piko_alive') is False and r13_v111_value('portrait')=='unfinished')
