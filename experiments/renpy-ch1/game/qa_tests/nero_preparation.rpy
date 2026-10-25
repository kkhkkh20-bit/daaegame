init python:
    def qa_nr_setup11():
        qa_nw_day14('prevented')
        r13_edit(day=11,period=1,location='square')
        r13_v111_set('day',11)
        room13['v111']['scene']='MS14_D11_S03'
        for key in ('rescue_cart_ready','rescue_cover_ready','rescue_driver_ready','rescue_lights_ready','rescue_school_ready11','lower_road_arrived11','lower_road_handover','grand_bowl_seen11','grand_bowl_pocket'):
            r13_v111_set(key,None)
        r13_v111_set('rescue_preparation_schema11',True)
        r13_v111_set('meeting:hypothesis','win')
        r13_v111_set('school_supply_handed',True)
        r13_v111_arrive(['mom','daram','karo','resident_nero','resident_lamplighter'])

label qa_nr_prepare11:
    call r13_scene(R13_PLACES['square'][1],'광장','calm')
    jump r13_v111_rescue_cart11

testcase nero_independent_preparation:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_nr_setup11)
    run Jump('qa_nr_prepare11')
    click pos (900,600) until eval (room13['v111'].get('gate')=='rescue_cart11') timeout 30
    pause 0.8
    assert eval (not r13_nero_transport_ready11())
    run Show('qa_hidden_base_return',value=('object','cart'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '다음 →' until '수레 짐을 내려 자리를 비운다' timeout 10
    click '수레 짐을 내려 자리를 비운다'
    click pos (900,600) until eval r13_v111_value('rescue_cart_ready') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','cart'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '다음 →' until '덮개를 접어 빈 짐칸에 싣는다' timeout 10
    click '덮개를 접어 빈 짐칸에 싣는다'
    click pos (900,600) until eval r13_v111_value('rescue_cover_ready') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('person','karo'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '까로에게 운반을 부탁한다'
    click pos (900,600) until eval r13_v111_value('rescue_driver_ready') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','lamp'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click pos (900,600) until eval r13_v111_value('rescue_lights_ready') timeout 30
    pause 0.8
    run Function(r13_edit,location='school')
    run Show('qa_hidden_base_return',value=('object','blankets'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click pos (900,600) until eval r13_v111_value('rescue_school_ready11') timeout 30
    pause 0.8
    run Function(r13_edit,location='square')
    assert eval (r13_nero_transport_ready11() and not r13_v111_value('lower_road_handover'))
    run Function(r13_edit,location='school')
    run Function(r13_v111_set,'lower_road_arrived11',3)
    run Function(r13_v111_set,'rescue_handoff_period11','night')
    run Jump('r13_v111_rescue_handoff11')
    click pos (900,600) until eval (room13['v111'].get('gate')=='rescue_handoff11') timeout 30
    pause 0.8
    assert eval (not r13_v111_value('lower_road_handover'))
    run Show('qa_hidden_base_return',value=('object','blankets'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '세 사람을 맞은 자리와 명단을 확인한다'
    click pos (900,600) until eval (r13_v111_value('lower_road_handover')==3) timeout 30
    assert eval (r13_v111_value('nero_alive') and r13_v111_value('fate:fate_nero')=='rescue')
