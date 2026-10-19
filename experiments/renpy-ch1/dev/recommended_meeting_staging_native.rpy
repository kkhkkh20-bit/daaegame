# Unrun native fixture. Copy to a disposable Ren'Py 8.5.3 QA profile only.
# This seeds presentation state; it is NOT an actual six-episode campaign playthrough.
label r13_qa_recommended_meeting_fixture:
    call r13_recommended_ep23_admin_boot
    $ r13_rec_staging_enabled = True
    $ r13_recommended['mother'] = 'M0'
    $ r13_recommended['piko'] = 'dead'
    $ r13_recommended['episode'] = 1
    $ r13_rec_stage_memory = {}
    call r13_scene('council', '추천 회의 · 분리된 연출 QA', 'calm')
    $ r13_rec_stage_enter(1)
    call r13_lines([('nabi','아이들에게 돌을 가져다준 건 맞아요. 하지만 등에서 꺼낸 건 아니에요.'),('dad','확인한 사실과 직접 보지 못한 일은 나눠서 듣겠습니다.')], 'recommended:hearing:new-defense')
    $ r13_rec_stage_answer('child', True)
    call r13_lines([('dad','돌의 인계를 직접 본 사람의 말을 함께 확인하겠습니다.'),('nabi','그 설명까지 듣겠습니다.')], 'recommended:hearing:answer')
    call screen r13_rec_stage_preview
    $ r13_rec_stage_exit()
    jump r13_recommended_hub

testcase recommended_meeting_adapter_smoke:
    pause 2.0
    click '처음부터'
    pause 3.0
    run Call('r13_qa_recommended_meeting_fixture')
    pause 2.0
    assert screen 'r13_rec_stage_say'
    assert eval (r13_rec_staging_active and not r13_meeting_active and r13_meeting_claim is None)
    assert eval (not {'dad','mom','resident_piko'}.intersection(p for p,_ in r13_meeting_cast('REC_HEARING_1','rec_hearing_1')))
    screenshot 'recommended-stage-01-speaker.png'
    click '수첩 · 확인한 사실'
    assert screen 'r13_recommended_notebook'
    assert eval (renpy.get_screen('r13_book') is None and renpy.get_screen('r13_records') is None)
    screenshot 'recommended-stage-02-own-notebook.png'
    click '현장으로'
    assert screen 'r13_rec_stage_say'
    click '잠깐 멈추기'
    assert screen 'r13_rec_stage_pause'
    screenshot 'recommended-stage-03-pause.png'
    click '이 말부터 계속 듣기'
    $ renpy.save('qa-recommended-stage-line')
    click pos (640,600) until screen 'r13_rec_stage_preview' timeout 60
    screenshot 'recommended-stage-04-cue-map.png'
    click '회의 2'
    assert eval (r13_rec_stage_session['episode']==2)
    screenshot 'recommended-stage-05-ep2.png'
    click '회의 3'
    assert eval (r13_rec_stage_session['episode']==3)
    screenshot 'recommended-stage-06-ep3.png'
    click '회의 4'
    assert eval (r13_rec_stage_session['episode']==4)
    screenshot 'recommended-stage-07-ep4.png'
    $ r13_recommended['neoul']='detained'
    click '회의 5'
    assert eval ('neoul' not in [p for p,_ in r13_meeting_cast('REC_HEARING_5','rec_hearing_5')])
    screenshot 'recommended-stage-08-ep5.png'
    click '회의 6'
    assert eval ('mom' not in [p for p,_ in r13_meeting_cast('REC_HEARING_6','rec_hearing_6')])
    screenshot 'recommended-stage-09-ep6-m0.png'
    $ r13_recommended['mother']='M2'
    run Function(renpy.restart_interaction)
    assert eval ('mom' in [p for p,_ in r13_meeting_cast('REC_HEARING_6','rec_hearing_6')])
    screenshot 'recommended-stage-10-ep6-m2.png'
    click '돌아가기'
    click pos (640,600) until screen 'r13_recommended_field' timeout 60
    assert eval (not r13_rec_staging_active and not r13_meeting_active and r13_meeting_claim is None)
    screenshot 'recommended-stage-11-cleanup.png'
    # Reload is an actual engine operation, with no replay of the saved shock.
    run Function(renpy.load, 'qa-recommended-stage-line')
    pause 1.0
    assert screen 'r13_rec_stage_say'
    assert eval (r13_rec_staging_active and r13_rec_stage_session['episode']==1)
    click '잠깐 멈추기'
    click '현장으로 돌아가 다시 조사하기'
    click pos (640,600) until screen 'r13_recommended_field' timeout 60
    assert eval (not r13_rec_staging_active and not r13_meeting_active and r13_meeting_claim is None)
    screenshot 'recommended-stage-12-interrupted-cleanup.png'
