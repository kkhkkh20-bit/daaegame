# 기존 7일 학교 인수 operations를 준비하고 실제 종료 경계·저장·복원을 검사한다.
init python:
    def qa_part1_finish_state(outcome='win',evacuated=False,grand=False,touch=False):
        qa_resident789(7)
        r13_edit(period=1,location='school')
        store.room13['v111']['scene']='MS14_D07_S02'
        if touch:
            renpy.set_physical_size((844,475))
        r13_v111_arrive(['nabi','resident_teacher','daram'])
        r13_v111_set('meeting:fire',outcome)
        r13_v111_set('FIRE_EVACUATED',evacuated)
        r13_v111_set('KKOMI_ALIVE',evacuated)
        r13_v111_set('NUBI_admitted_setting_fire',outcome!='lose')
        r13_v111_set('neoul_promise_proven',grand)
        r13_v111_set('listed:resident_bori',outcome in ('partial','lose'))
        r13_v111_commit('MS14_D07_S02_L0029')
        r13_v111_commit('MS14_D07_S02_L0046')
        r13_grant(['V111:E27'],'qa-part1-warning')
        r13_v111_set('mother_first_contact_read5',True)
        r13_v111_commit('MS14_D05_S04_L0014')
        store.r13_conv_skip_run=False
        renpy.hide_screen("r13_hub")

    def qa_part1_domain():
        return winter_copy.deepcopy(dict((k,v) for k,v in store.room13['v111']['values'].items() if not k.startswith('part1_')))

    def qa_part1_unlock():
        store.R13_PART1_PUBLIC=False
        renpy.restart_interaction()


testcase part1_win_checkpoint_restore:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state)
    $ qa_part1_before=qa_part1_domain()
    run Jump('r13_v111_free_evening7')
    click pos (900,600) until screen 'r13_part1_end' timeout 60
    pause 1.0
    assert eval (r13_v111_value('part1_completed') and r13_v111_value('part1_checkpoint_written'))
    assert eval (room13['day']==7 and qa_part1_domain()==qa_part1_before and not r13_has('v111:entered:MS14_D07_S03'))
    assert eval (renpy.can_load('part1-clear') and renpy.slot_json('part1-clear')['r13_part1_complete'])
    assert eval (qa_nw_seen('꼬미 자리도 여기 있었으면') and not qa_nw_seen('꼬미가 자기 자리라고'))
    assert eval (qa_nw_seen('엄마가 우리를 부르지 않았다는 건') and qa_nw_seen('마음 놓고 만날 방법'))
    screenshot 'part1-win.png'
    click id 'r13_part1_records'
    pause .3
    screenshot 'part1-win-records.png'
    $ persistent.qa_part1_saved_at=renpy.slot_json('part1-clear')['_ctime']
    run Function(renpy.load,'part1-clear')
    pause until screen 'r13_part1_end' timeout 30
    pause 1.0
    assert eval (r13_v111_value('part1_checkpoint_written') and renpy.slot_json('part1-clear')['_ctime']==persistent.qa_part1_saved_at)
    assert eval (room13['day']==7 and r13_v111_value('route7')=='uncommitted' and not r13_v111_value('DARAM_DETAINED'))
    assert eval (r13_v111_value('meeting:fire')=='win' and not r13_has('v111:entered:MS14_D07_S03'))
    screenshot 'part1-checkpoint-restored.png'
    click id 'r13_part1_main'
    pause until screen 'main_menu' timeout 30
    assert eval (r13_continue_slot()=='part1-clear')
    click '이어하기'
    pause until screen 'r13_part1_end' timeout 30
    assert eval (room13['day']==7 and r13_v111_value('part1_completed'))


testcase part1_partial_keeps_result:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state,'partial')
    $ qa_part1_before=qa_part1_domain()
    run Jump('r13_v111_free_evening7')
    click pos (900,600) until screen 'r13_part1_end' timeout 60
    pause .8
    assert eval (qa_part1_domain()==qa_part1_before and r13_v111_value('listed:resident_bori'))
    assert eval ('감춘 죄' in ' '.join(r13_part1_records(room13['v111']['values'])))
    click id 'r13_part1_records'
    pause .3
    assert eval (qa_nw_seen('보리 씨 이름은 빼내지 못했어') and not qa_nw_seen('불을 낸 사람을 끝내 밝히지 못했어'))
    screenshot 'part1-partial-records.png'


testcase part1_lose_keeps_result:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state,'lose')
    $ qa_part1_before=qa_part1_domain()
    run Jump('r13_v111_free_evening7')
    click pos (900,600) until screen 'r13_part1_end' timeout 60
    pause .8
    assert eval (qa_part1_domain()==qa_part1_before and r13_v111_value('listed:resident_bori'))
    assert eval (not r13_v111_value('NUBI_admitted_setting_fire') and '자백을 얻지 못했다' in ' '.join(r13_part1_records(room13['v111']['values'])))
    click id 'r13_part1_records'
    pause .3
    assert eval (qa_nw_seen('불을 낸 사람을 끝내 밝히지 못했어') and not qa_nw_seen('보리 씨 이름은 빼내지 못했어'))
    screenshot 'part1-lose-records.png'


testcase part1_grand_evacuated_touch:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state,'win',True,True,True)
    $ qa_part1_before=qa_part1_domain()
    run Jump('r13_v111_free_evening7')
    click pos (900,600) until screen 'r13_part1_end' timeout 60
    pause .8
    assert eval (qa_part1_domain()==qa_part1_before and r13_v111_value('KKOMI_ALIVE'))
    assert eval ('배급표' in ' '.join(r13_part1_records(room13['v111']['values'])))
    click id 'r13_part1_records'
    pause .3
    assert eval (qa_nw_seen('꼬미가 자기 자리라고') and not qa_nw_seen('꼬미 자리도 여기 있었으면'))
    screenshot 'part1-grand-touch-records.png'


testcase part1_future_continuation_starts_existing_night:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state)
    run Jump('r13_v111_free_evening7')
    click pos (900,600) until screen 'r13_part1_end' timeout 60
    pause .8
    run Function(renpy.load,'part1-clear')
    pause until screen 'r13_part1_end' timeout 30
    # 후속판의 공개 경계 설정만 바꾼다. 완성 저장은 8일을 직행하지 않고 기존 저녁부터 이어져야 한다.
    run Function(qa_part1_unlock)
    click pos (900,600) until eval (room13['v111'].get('scene')=='MS14_D07_S03') timeout 45
    assert eval (room13['day']==7 and r13_v111_value('route7')=='uncommitted' and not r13_v111_value('DARAM_DETAINED'))
    screenshot 'part1-next-part-existing-night.png'


testcase part1_finish_cancel_keeps_afternoon:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state,'win',True)
    $ qa_part1_before=qa_part1_domain()
    $ qa_part1_save_before=(renpy.slot_json('part1-clear') or {}).get('_ctime')
    run Call('r13_scene',R13_PLACES['school'][1],R13_PLACES['school'][0],'calm')
    run Jump('r13_v111_free_day7')
    click pos (900,600) until eval (room13['v111'].get('gate')=='free_day7' and renpy.get_screen('r13_hub') and not renpy.get_screen('say')) timeout 60
    screenshot 'part1-afternoon-before-finish.png'
    if not '다람':
        click '오른쪽 구역' until '다람' timeout 20
    click '다람'
    click '다람아, 오늘 조사는 여기서 마치자.'
    pause until screen 'r13_part1_finish_choice' timeout 30
    $ qa_part1_before=qa_part1_domain()
    screenshot 'part1-finish-choice.png'
    click id 'r13_part1_keep_exploring'
    pause until screen 'r13_hub' timeout 30
    assert eval (not r13_v111_value('part1_completed') and qa_part1_domain()==qa_part1_before)
    assert eval ((renpy.slot_json('part1-clear') or {}).get('_ctime')==qa_part1_save_before)
    assert eval (room13['day']==7 and room13['period']==1 and not r13_has('v111:entered:MS14_D07_S03'))
    screenshot 'part1-cancel-afternoon.png'
    click '다람'
    click '다람아, 오늘 조사는 여기서 마치자.'
    pause until screen 'r13_part1_finish_choice' timeout 30
    $ qa_part1_before=qa_part1_domain()
    click id 'r13_part1_finish_now'
    click pos (900,600) until screen 'r13_part1_end' timeout 90
    pause .8
    assert eval (r13_v111_value('part1_completed') and qa_part1_domain()==qa_part1_before)


testcase part1_return_from_end_refreshes_completion:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state,'win',True,True,True)
    $ qa_part1_before=qa_part1_domain()
    run Jump('r13_v111_free_evening7')
    click pos (900,600) until screen 'r13_part1_end' timeout 90
    pause 1.0
    $ persistent.qa_part1_saved_at=renpy.slot_json('part1-clear')['_ctime']
    screenshot 'part1-end-return-touch.png'
    click id 'r13_part1_explore'
    pause until screen 'r13_hub' timeout 30
    assert eval (qa_part1_domain()==qa_part1_before and not r13_v111_value('part1_completed') and not r13_v111_value('part1_checkpoint_written'))
    assert eval (room13['day']==7 and room13['period']==1)
    pause 1.0
    click '다람'
    click '다람아, 오늘 조사는 여기서 마치자.'
    pause until screen 'r13_part1_finish_choice' timeout 30
    $ qa_part1_before=qa_part1_domain()
    click id 'r13_part1_finish_now'
    click pos (900,600) until screen 'r13_part1_end' timeout 90
    pause .8
    assert eval (renpy.slot_json('part1-clear')['_ctime']>persistent.qa_part1_saved_at and qa_part1_domain()==qa_part1_before)
    $ persistent.qa_part1_saved_at=renpy.slot_json('part1-clear')['_ctime']
    run Function(renpy.load,'part1-clear')
    pause until screen 'r13_part1_end' timeout 30
    pause 1.0
    assert eval (r13_v111_value('part1_completed') and r13_v111_value('part1_checkpoint_written') and qa_part1_domain()==qa_part1_before)
    assert eval (renpy.slot_json('part1-clear')['_ctime']==persistent.qa_part1_saved_at)
    screenshot 'part1-refinished-restored.png'


testcase part1_legacy_warning_is_not_heard_automatically:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_part1_finish_state)
    run Function(r13_v111_set,'mother_first_contact_read5',False)
    run Function(r13_v111_set,'mother_denies_invitation',False)
    run Function(r13_v111_set,'KKOMI_ALIVE',None)
    run Function(r13_v111_set,'location:daram','workshop')
    run Function(r13_v111_context,'free_day7')
    $ qa_part1_before=qa_part1_domain()
    run Jump('r13_v111_free_evening7')
    click pos (900,600) until screen 'r13_part1_end' timeout 90
    pause .8
    assert eval (qa_part1_domain()==qa_part1_before)
    assert eval (qa_nw_seen('초롱 씨 쪽지에 적힌 부엉이 어르신') and not qa_nw_seen('엄마가 우리를 부르지 않았다는 건'))
    assert eval (not qa_nw_seen('꼬미 자리도 여기 있었으면') and not qa_nw_seen('꼬미가 자기 자리라고'))
    screenshot 'part1-legacy-contact.png'
