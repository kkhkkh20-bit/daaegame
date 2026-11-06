# 준비한 시작 상태에서 본편 라벨과 실제 선택으로 반응·인수·운영 경계를 확인한다.
init python:
    def qa_resident1314(day,location='school'):
        r13_v111_set('day',day)
        r13_edit(day=day,location=location,period=2 if day==14 or location=='square' else 0)
        r13_v111_set('route7','prevented')
        r13_v111_set('OWL_ALIVE',True)
        r13_v111_set('DARAM_DETAINED',False)
        r13_v111_set('family_reunited',True)
        r13_v111_set('family_school_place',True)
        r13_v111_set('location:daram',location)
        r13_v111_set('location:mom',location)
        r13_v111_set('DARAM_location','with_dad')
        r13_v111_set('carried_dry_blankets',2)
        if day==14:
            r13_v111_set('ending14','morning')
            r13_v111_set('all_cart_handed',True)
            r13_v111_set('bomi_death_confirmed',True)


testcase resident13_pandol_blanket:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident1314,13)
    run Function(r13_v111_scene,'MS14_D13_S01')
    run Function(r13_v111_arrive,['mom','daram','npc_pandol','karo'])
    run Call('qa_rr_scene','r13_v111_blanket_mended13')
    click pos (900,600) until eval qa_rr_visible('NW_RR13_P') timeout 90
    assert eval (r13_v111_value('carried_dry_blankets')==2 and not r13_v111_owned('E13_MENDING'))
    assert eval (not r13_v111_value('pandol_blanket_mended') and r13_v111_value('family_deal') is None)
    screenshot 'resident13_pandol.png'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E13_MENDING') and r13_v111_value('pandol_blanket_mended') is True and r13_v111_value('carried_dry_blankets')==2)


testcase resident13_nabi_beds_before_receipt:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident1314,13)
    run Function(r13_v111_set,'false_message_admitted',True)
    run Function(r13_v111_set,'cart_stopped',True)
    run Function(r13_v111_set,'all_cart_handed',False)
    run Function(r13_v111_scene,'MS14_D13_S04')
    run Function(r13_v111_arrive,['nabi','karo'])
    run Call('qa_rr_scene','r13_v111_beds_ready13')
    click pos (900,600) until eval (r13_packet and '데려오기만 하세요' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (not r13_v111_value('handover_prepared13') and not r13_v111_value('all_cart_handed'))
    assert eval (not r13_v111_value('handed:npc_pandol') and not r13_v111_value('handed:resident_momo'))
    screenshot 'resident13_nabi.png'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_value('handover_prepared13') is True and not r13_v111_value('all_cart_handed'))


testcase resident13_karo_return_before_commit:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident1314,13,'square')
    run Function(r13_v111_set,'false_message_admitted',True)
    run Function(r13_v111_set,'cart_stopped',True)
    run Function(r13_v111_set,'all_cart_handed',True)
    run Function(r13_v111_set,'departed:resident_guldol',True)
    run Function(r13_v111_scene,'MS14_D13_S04')
    run Call('qa_rr_scene','r13_v111_cart_return13')
    click pos (900,600) until eval qa_rr_visible('NW_RR13_K') timeout 60
    assert eval (not r13_v111_value('cart_returned') and not r13_v111_value('escort_gear_returned'))
    assert eval (r13_v111_actor_ready('resident_eunho') and not r13_v111_value('current_transport_chain_stopped'))
    screenshot 'resident13_karo.png'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_value('cart_returned') is True and r13_v111_value('escort_gear_returned') is True and r13_v111_value('departed:resident_guldol') is True)


testcase resident14_tosil_name_outside:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident1314,14,'square')
    run Function(r13_v111_set,'tosil_listen','outside')
    run Call('qa_rr_scene','r13_v111_name_board14')
    click pos (900,600) until screen 'choice' timeout 60
    click '토실이 이름을 쓰겠다면 기다린다'
    click pos (900,600) until eval qa_rr_visible('NW_RR14_01') timeout 60
    assert eval (r13_v111_value('tosil_listen')=='outside' and r13_v111_value('bomi_death_confirmed') is True)
    assert eval (not r13_v111_value('current_sacrifice_operation_closed') and r13_v111_actor_ready('resident_tosil'))
    screenshot 'resident14_tosil.png'


testcase resident14_inventory_and_lamps:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident1314,14)
    run Function(r13_v111_set,'current_transport_chain_stopped',False)
    run Function(r13_v111_set,'device_joint_control',False)
    run Function(r13_v111_set,'departed:resident_guldol',True)
    run Function(r13_v111_scene,'MS14_D14_S04')
    run Function(r13_v111_arrive,['mom','daram','nabi','guard','resident_madam','resident_lamplighter'])
    run Call('qa_rr_scene','r13_v111_supply_inventory_done14')
    click pos (900,600) until eval qa_rr_visible('NW_RR14_02') timeout 60
    assert eval (not r13_v111_value('school_inventory_checked') and not r13_v111_value('current_sacrifice_operation_closed'))
    screenshot 'resident14_madam.png'
    click pos (900,600) until eval qa_rr_visible('NW_RR14_03') timeout 60
    assert eval (r13_v111_value('school_inventory_checked') is True and r13_v111_value('school_supply_handed') is True)
    assert eval (not r13_v111_value('current_sacrifice_operation_closed') and not r13_v111_value('lamp_manager'))
    screenshot 'resident14_chorong.png'
    click pos (900,600) until eval (r13_v111_value('lamp_manager')=='resident_lamplighter') timeout 60
    assert eval (not r13_v111_value('current_sacrifice_operation_closed') and r13_v111_value('departed:resident_guldol') is True)
