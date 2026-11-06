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
        store.r13_conv_skip_run=False

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
