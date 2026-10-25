init python:
    def qa_hidden_base_setup(parts=True):
        qa_nw_day14('prevented')
        r13_edit(location='school',period=2)
        r13_v111_set('ending14','true')
        for key in ('paper','plate','marks_copied'):
            r13_v111_set('hidden_base:'+key,parts)
        for key in ('finished','entered','opened','aligned','paper_set','frame_seen','read_section','read_incident','notebook_taken','returned','return_context'):
            r13_v111_set('hidden_base:'+key,None)
        r13_v111_arrive(['mom','daram'])

screen qa_hidden_base_return(value):
    zorder 10000
    textbutton 'QA 행동':
        pos (20,640)
        action [Hide('qa_hidden_base_return'),Return(value)]

label qa_hidden_base_episode:
    call r13_scene(R13_PLACES['school'][1],'학교','calm')
    call r13_hidden_base14
    call screen r13_confirm('기지 조사 시험 완료',yes='끝',no='끝')
    return

testcase hidden_base_missing_parts:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_hidden_base_setup,False)
    run Jump('qa_hidden_base_episode')
    pause 0.5
    click pos (900,600) until screen 'r13_confirm' timeout 90
    assert eval (r13_v111_value('ending14')=='true' and not r13_hidden_base_value('entered') and not qa_nw_seen('정비실 문틀에서 맞춘 종이'))

testcase hidden_base_decline:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_hidden_base_setup)
    run Jump('qa_hidden_base_episode')
    click pos (900,600) until eval (room13['v111'].get('gate')=='hidden_base_offer14') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','blankets'))
    pause 0.3
    click 'QA 행동'
    pause 0.7
    assert screen 'r13_confirm'
    assert eval (r13_hidden_base_value('finished') and not r13_hidden_base_value('entered') and room13['location']=='school' and room13['period']==2 and r13_v111_value('ending14')=='true')

testcase hidden_base_door_and_records:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_hidden_base_setup)
    run Jump('qa_hidden_base_episode')
    click pos (900,600) until eval (room13['v111'].get('gate')=='hidden_base_offer14') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('person','mom'))
    pause 0.3
    click 'QA 행동'
    pause 0.7
    click '수첩을 챙기러 같이 가자.'
    click pos (900,600) until eval (room13['v111'].get('gate')=='hidden_base_door14') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hb_door'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '문틀의 홈을 살핀다'
    click pos (900,600) until eval r13_hidden_base_value('frame_seen') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hb_door'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '홈 위에 종이를 댄다'
    click pos (900,600) until eval r13_hidden_base_value('paper_set') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hb_door'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '표시한 면을 안으로 끼운다'
    click pos (900,600) until eval (r13_hidden_base_value('aligned') is False) timeout 90
    pause 0.7
    assert eval (r13_hidden_base_parts_ready() and not r13_hidden_base_value('opened'))
    run Show('qa_hidden_base_return',value=('object','hb_door'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '표시한 면을 바깥으로 끼운다'
    click pos (900,600) until eval r13_hidden_base_value('aligned') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hb_door'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '다음 →' until '문을 연다' timeout 10
    click '문을 연다'
    click pos (900,600) until eval (room13['v111'].get('gate')=='hidden_base_room14') timeout 90
    pause 0.7
    assert eval qa_nw_seen('대화가 잘 끝났네')
    run Show('qa_hidden_base_return',value=('object','hb_section'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_hidden_base_value('read_section') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hb_incident'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_hidden_base_value('read_incident') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hb_notebook'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_hidden_base_value('notebook_taken') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hb_door'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until screen 'r13_confirm' timeout 90
    assert eval (r13_hidden_base_value('returned') and room13['location']=='school' and room13['period']==2 and r13_v111_value('ending14')=='true')
    assert eval (qa_nw_seen('말을 잊고 어제 일을') and qa_nw_seen('사람을 보내라는 명령이 없었어'))
