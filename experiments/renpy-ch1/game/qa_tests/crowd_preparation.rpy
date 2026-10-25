init python:
    def qa_cp_setup13(mode='prepare'):
        qa_nw_day13()
        room13['v111']['scene']='MS14_D13_S04'
        r13_v111_set('cart_stopped',True)
        r13_v111_set('family_location','school')
        r13_v111_set('alive:neoul',True)
        r13_v111_set('alive:resident_momo',True)
        r13_v111_set('neoul_promise_proven',mode=='record')
        r13_v111_set('neoul_held',True)
        for key in ('crowd_records_spaced13','crowd_cart_spaced13','crowd_supervisor_placed13','crowd_resolution_done','crowd_injury','fate:fate_crowd'):
            r13_v111_set(key,None)
        for key in ('departed:guard','listed:guard'):
            r13_v111_set(key,False)
        r13_v111_set('busy:guard','silluk_supervision' if mode=='busy' else None)
        r13_v111_set('location:guard','square')
        if mode=='busy':
            r13_v111_set('crowd_records_spaced13',True)
            r13_v111_set('crowd_cart_spaced13',True)
            r13_v111_set('handed:resident_momo',True)

label qa_cp_entry13:
    call r13_scene(R13_PLACES['square'][1],'광장','calm')
    jump r13_v111_crowd_prepare13

testcase crowd_before_publication_guard:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_cp_setup13)
    run Jump('qa_cp_entry13')
    click pos (900,600) until eval (room13['v111'].get('gate')=='crowd_prepare13') timeout 30
    pause 0.8
    assert eval (not r13_crowd_prepared13() and not r13_v111_value('crowd_resolution_done'))
    run Show('qa_hidden_base_return',value=('object','cart'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '기록 읽을 자리를 수레에서 떼어 놓는다'
    click pos (900,600) until eval r13_v111_value('crowd_records_spaced13') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','cart'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '수레 옆 짐을 옮겨 통로를 나눈다'
    click pos (900,600) until eval r13_v111_value('crowd_cart_spaced13') timeout 30
    pause 0.8
    assert eval (not r13_crowd_prepared13())
    run Show('qa_hidden_base_return',value=('person','guard'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '돌목에게 기록 읽는 동안 너울을 맡아 달라고 한다'
    click pos (900,600) until eval r13_v111_value('crowd_supervisor_placed13') timeout 30
    pause 0.8
    assert eval (r13_crowd_prepared13() and not r13_v111_value('crowd_resolution_done'))
    run Show('qa_hidden_base_return',value=('object','cart'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '검증한 기록을 소리 내어 읽는다'
    click pos (900,600) until eval r13_v111_value('crowd_resolution_done') timeout 60
    assert eval (r13_v111_value('fate:fate_crowd')=='supervisor' and r13_v111_value('crowd_injury') is False and r13_v111_value('alive:neoul') is True and not r13_v111_value('busy:guard'))

testcase crowd_busy_guard_and_handover_first:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_cp_setup13,'busy')
    run Jump('qa_cp_entry13')
    click pos (900,600) until eval (room13['v111'].get('gate')=='crowd_prepare13') timeout 30
    pause 0.8
    assert eval (not r13_crowd_guard_available13() and not any(o.get('person')=='guard' for o in r13_v111_binding()['options']) and 'guard' not in r13_visible_people())
    run Show('qa_hidden_base_return',value=('object','cart'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '검증한 기록을 소리 내어 읽는다'
    click pos (900,600) until eval r13_v111_value('crowd_resolution_done') timeout 60
    assert eval (r13_v111_value('crowd_injury') and r13_v111_value('busy:guard')=='silluk_supervision' and r13_v111_value('location:guard')=='square' and r13_v111_value('alive:resident_momo') is True and r13_v111_value('alive:neoul') is False)

testcase crowd_grand_record_still_protects:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_cp_setup13,'record')
    run Jump('qa_cp_entry13')
    click pos (900,600) until eval (room13['v111'].get('gate')=='crowd_prepare13') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','cart'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '다음 →' until '검증한 기록을 소리 내어 읽는다' timeout 10
    click '검증한 기록을 소리 내어 읽는다'
    click pos (900,600) until eval r13_v111_value('crowd_resolution_done') timeout 60
    assert eval (r13_v111_value('crowd_record_read') and r13_v111_owned('NW_NEOUL_LEDGER') and r13_v111_value('crowd_injury') is False and r13_v111_value('alive:neoul') is True)
