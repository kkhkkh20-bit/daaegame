# 시작 상태만 준비한 뒤 실제 본편 라벨의 새 반응과 기존 인수·자료 경계를 검사한다.
init python:
    def qa_resident101112(day,route='murder',location='school'):
        r13_v111_set('day',day)
        r13_edit(day=day,location=location,period=2 if day==12 else 1 if location=='facility' else 0)
        r13_v111_set('route7',route)
        r13_v111_set('OWL_ALIVE',route!='murder')
        r13_v111_set('DARAM_DETAINED',False)
        r13_v111_set('DARAM_location','with_dad')
        r13_v111_set('TOK_ALIVE',True)
        r13_v111_set('tok_workshop_present',True)
        r13_v111_set('tok_hearing_present',True)
        r13_v111_set('family_reunited',day>=11)
        r13_v111_set('grandmother_custody','detained' if route=='murder' and day>=11 else 'free')
        r13_v111_set('location:daram',location)
        r13_v111_set('location:mom',location if day>=11 else 'greenhouse')
        r13_v111_set('root_address_known',True)
        r13_v111_set('D10_S02_second_door_completed',True)
        r13_v111_set('soup_fragment_observed',day==12)
        if day==10 and route=='murder':
            r13_grant(['V111:'+k for k in ('E08_CHILD_POSITION','E08_ROOM_REACH','E08_CONTACT_ASSEMBLY','E08_WOUND_WIRE','E09_PIN_HANDOVER_TIME','E09_SCARF')],'qa')

    def qa_rr_visible(prefix):
        import re
        rows=[r for section in ('before','after','blocks') for values in R13_NW_TEXT[section].values() for r in values if r.get('id','').startswith(prefix)]
        if not rows or not r13_packet:return False
        return re.sub(r'\s+','',rows[-1]['text']) in re.sub(r'\s+','',r13_packet[1])


label qa_rr_scene(label_name):
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    jump expression label_name


testcase resident11_school_handoff:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,11)
    run Function(r13_v111_set,'family_reunited',False)
    run Function(r13_v111_set,'tosil_safe_handoff_confirmed',False)
    run Function(r13_v111_set,'greenhouse_address_known',True)
    run Function(r13_v111_set,'carried_dry_blankets',2)
    run Function(r13_v111_scene,'MS14_D11_S01')
    run Function(r13_v111_arrive,['daram','resident_tosil','nabi'])
    run Call('qa_rr_scene','r13_v111_tosil_safe11')
    click pos (900,600) until eval qa_rr_visible('NW_RR11_SEAT') timeout 60
    assert eval (not r13_v111_value('tosil_safe_handoff_confirmed') and not r13_v111_value('family_reunited'))
    assert eval (r13_v111_value('carried_dry_blankets')==2 and set(room13['v111']['people'])==set(['daram','resident_tosil','nabi']))
    screenshot 'resident11_seat.png'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_value('tosil_safe_handoff_confirmed') is True and r13_v111_value('tosil_knows_greenhouse') is False)
    assert eval (r13_v111_value('family_reunited') is False and r13_v111_value('carried_dry_blankets')==2)


testcase resident11_family_sleeve:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,11,'murder','greenhouse')
    run Function(r13_v111_set,'mother_first_contact_read5',False)
    run Function(r13_v111_set,'mother_contact_relay10',False)
    run Call('qa_rr_scene','r13_v111_button11')
    click pos (900,600) until eval qa_rr_visible('NW_RR11_SLEEVE') timeout 90
    assert eval (set(room13['v111']['people'])==set(['mom','daram']) and not r13_v111_value('mother_contact_relay10'))
    assert eval (r13_v111_value('family_reunited') is True and not r13_v111_value('tosil_knows_greenhouse'))
    screenshot 'resident11_sleeve.png'


testcase resident11_guldol_light:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,11,'prevented','facility')
    run Function(r13_v111_set,'alive:resident_guldol',True)
    run Function(r13_v111_set,'carried_dry_blankets',1)
    run Call('qa_rr_scene','r13_v111_facility11')
    click pos (900,600) until eval qa_rr_visible('NW_RR11_LIGHT') timeout 90
    assert eval (r13_v111_value('guldol_facility_seen') is True and r13_v111_actor_ready('resident_guldol'))
    assert eval (not r13_v111_owned('NW_TABLET_A') and not r13_v111_value('heat_inventory_observed') and r13_v111_value('carried_dry_blankets')==1)
    screenshot 'resident11_light.png'


testcase resident10_buri_notebook:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,10)
    run Function(r13_v111_set,'DARAM_DETAINED',True)
    run Function(r13_v111_set,'D10_S02_second_door_completed',False)
    run Call('qa_rr_scene','r13_v111_waiting10')
    click pos (900,600) until eval qa_rr_visible('NW_RR10_B') timeout 90
    assert eval (r13_v111_value('DARAM_DETAINED') is True and r13_v111_value('OWL_ALIVE') is False)
    assert eval (r13_v111_value('meeting:room13') is None and not r13_v111_value('D10_S01_main_completed') and not r13_v111_value('D10_S02_second_door_completed'))
    screenshot 'resident10_buri.png'
    click pos (900,600) until screen 'r13_crisis_proof' timeout 90
    assert eval (r13_v111_value('BURI_notebook')=='returned' and r13_v111_value('DARAM_DETAINED') is True)


testcase resident10_tok_no_touch:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,10)
    run Function(r13_v111_set,'DARAM_DETAINED',True)
    run Function(r13_v111_scene,'MS14_D10_S03')
    run Function(r13_grant,['V111:E08_WOUND_WIRE','V111:E09_PIN_OWNER'],'qa')
    run Call('qa_rr_scene','r13_v111_owner_tok10')
    click pos (900,600) until eval qa_rr_visible('NW_RR10_T') timeout 60
    assert eval (r13_v111_tok_attends('hearing') and 'resident_tok' in room13['v111']['people'])
    assert eval (r13_v111_value('grandmother_custody')!='detained' and r13_v111_value('meeting:room13') is None)
    screenshot 'resident10_tok.png'


testcase resident10_owl_receipt:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,10,'prevented')
    run Function(r13_v111_set,'meeting:records','partial')
    run Function(r13_v111_set,'prevention','stone')
    run Function(r13_v111_scene,'MS14_D10_P01')
    run Call('qa_rr_scene','r13_v111_public_paper10')
    click pos (900,600) until eval qa_rr_visible('NW_RR10_O') timeout 60
    assert eval (r13_v111_value('OWL_ALIVE') is True and r13_v111_value('DARAM_DETAINED') is False)
    assert eval (r13_v111_value('meeting:records')=='partial' and r13_v111_value('grandmother_custody')!='detained')
    screenshot 'resident10_owl.png'


testcase resident12_seori_child_first:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,12)
    run Function(r13_v111_set,'route12','premeal_stopped')
    run Function(r13_v111_set,'medical_arrived',False)
    run Function(r13_v111_set,'soup_fragment_observed',True)
    run Function(r13_v111_set,'busy:resident_bori','medical_call')
    run Function(r13_v111_set,'location:resident_bori','clinic')
    run Function(r13_v111_scene,'MS14_D12_S04')
    run Function(r13_v111_arrive,['daram','nabi','resident_teacher','guard','neoul'])
    run Call('qa_rr_scene','r13_v111_medical_arrival12')
    click pos (900,600) until eval qa_rr_visible('NW_RR12_01') timeout 90
    assert eval (r13_v111_actor_ready('resident_seori') and r13_v111_actor_ready('resident_bori') and not r13_v111_value('busy:resident_bori'))
    assert eval (not r13_v111_value('medical_arrived') and not r13_v111_owned('E12_HANDLING'))
    screenshot 'resident12_seori.png'
    click pos (900,600) until screen 'r13_crisis_proof' timeout 60
    assert eval (r13_v111_value('medical_arrived') is True and r13_v111_owned('E12_HANDLING') and not r13_v111_value('teacher_confessed'))


testcase resident12_nabi_pot_boundary:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,12)
    run Function(r13_v111_set,'route12','premeal_stopped')
    run Function(r13_v111_set,'teacher_confessed',True)
    run Function(r13_v111_set,'meeting:soup','partial')
    run Function(r13_v111_set,'transfer_list_voided',False)
    run Function(r13_v111_scene,'MS14_D12_S04')
    run Function(r13_v111_arrive,['daram','nabi','resident_teacher','resident_seori','resident_bori','guard','neoul'])
    run Call('qa_rr_scene','r13_v111_aftermath_pre12')
    click pos (900,600) until eval qa_rr_visible('NW_RR12_02') timeout 90
    assert eval (r13_v111_value('meeting:soup')=='partial' and not r13_v111_value('transfer_list_voided'))
    assert eval (not r13_v111_value('book_promise12') and not r13_v111_value('listed:nabi'))
    screenshot 'resident12_nabi.png'
    click pos (900,600) until screen 'choice' timeout 60
    assert eval (r13_v111_value('book_promise12') is True and not r13_v111_value('transfer_list_voided'))


testcase resident12_guard_voided_column:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident101112,12)
    run Function(r13_v111_set,'route12','premeal_stopped')
    run Function(r13_v111_set,'teacher_confessed',True)
    run Function(r13_v111_set,'departed:resident_guldol',True)
    run Function(r13_v111_scene,'MS14_D12_S04')
    run Function(r13_v111_arrive,['daram','nabi','resident_teacher','resident_seori','resident_bori','guard','neoul'])
    run Function(r13_grant,['V111:NW_WHITE_BOWLS','V111:NW_RETURNED_BOWL'],'qa')
    run Call('qa_rr_scene','r13_v111_list_proof12')
    pause until screen 'r13_crisis_proof' timeout 45
    click '자료 고르기'
    click 'QA V111:NW_WHITE_BOWLS'
    click 'QA V111:NW_RETURNED_BOWL'
    click 'QA 닫기'
    click '선택한 근거 제출'
    click pos (900,600) until eval qa_rr_visible('NW_RR12_03') timeout 120
    assert eval (r13_v111_value('meeting:soup')=='win' and r13_v111_value('grand:soup') is True and r13_v111_value('transfer_list_voided') is True)
    assert eval (r13_v111_value('departed:resident_guldol') is True and not r13_v111_value('listed:nabi'))
    screenshot 'resident12_guard.png'
