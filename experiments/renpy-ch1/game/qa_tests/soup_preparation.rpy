init python:
    def qa_sp_setup12():
        qa_nw_day14('prevented')
        r13_edit(day=12,period=1,location='school')
        r13_v111_set('day',12)
        room13['v111']['scene']='MS14_D12_S02'
        for key in ('soup_smallpot_seen12','soup_bowls_seen12','soup_bottle_seen12','soup_serving_separated12','soup_fragment_observed','fate:fate_soup'):
            r13_v111_set(key,None)
        r13_v111_set('route12','uncommitted')
        r13_v111_set('bottle_original_seal_seen',True)
        r13_v111_set('daram_fever12',True)
        r13_v111_set('meal12_intro_seen',True)
        r13_v111_arrive(['daram','nabi','resident_teacher','resident_bori','kid_dodam','kid_saemi'])

label qa_sp_stay12:
    call r13_scene(R13_PLACES['school'][1],'학교','calm')
    jump r13_v111_stay_meal12

testcase soup_inspection_then_actual_stop:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_sp_setup12)
    run Jump('qa_sp_stay12')
    click pos (900,600) until eval (room13['v111'].get('gate')=='meal_inspect12') timeout 30
    pause 0.8
    assert eval (r13_v111_value('route12')=='uncommitted' and not r13_v111_value('soup_fragment_observed'))
    run Show('qa_hidden_base_return',value=('object','desks'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '작은 냄비와 국자 자리를 살핀다'
    click pos (900,600) until eval r13_v111_value('soup_smallpot_seen12') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','v111_bowl_table'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('soup_bowls_seen12') timeout 30
    pause 0.8
    assert eval (not r13_soup_inspect_ready12() and r13_v111_value('route12')=='uncommitted')
    run Show('qa_hidden_base_return',value=('object','desks'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '선반에 놓인 병의 봉인을 살핀다'
    click pos (900,600) until eval r13_v111_value('soup_bottle_seen12') timeout 30
    pause 0.8
    assert eval (r13_soup_inspect_ready12() and r13_v111_value('route12')=='uncommitted' and not r13_v111_value('soup_fragment_observed'))
    run Show('qa_hidden_base_return',value=('object','v111_bowl_table'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('soup_fragment_observed') timeout 30
    assert eval (r13_v111_value('route12')=='premeal_stopped' and r13_v111_value('soup_serving_separated12') and r13_v111_value('fate:fate_soup')=='premeal')

testcase soup_leave_inspection_still_late:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_sp_setup12)
    run Jump('qa_sp_stay12')
    click pos (900,600) until eval (room13['v111'].get('gate')=='meal_inspect12') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','desks'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '다음 →' until '장작을 받을 일을 다시 살핀다' timeout 10
    click '장작을 받을 일을 다시 살핀다'
    pause 0.8
    click '다음 →' until '다람과 장작을 받으러 간다' timeout 10
    click '다람과 장작을 받으러 간다'
    click pos (900,600) until eval (r13_v111_value('route12')=='late_exposure') timeout 30
    assert eval (not r13_v111_value('soup_serving_separated12') and not r13_v111_value('soup_fragment_observed') and r13_v111_value('fate:fate_soup')=='lost')
