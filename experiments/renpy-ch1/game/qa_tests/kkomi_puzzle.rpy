init python:
    def qa_k2_setup():
        qa_nw_day14('prevented')
        r13_edit(day=6,period=1,location='v111_woodshed')
        r13_v111_set('day',6)
        r13_v111_set('kkomi_seat6',True)
        r13_v111_set('acorn_recovered',None)
        r13_v111_set('kkomi_can_seen6',None)
        r13_v111_talk_person=None
        r13_v111_arrive(['kid_kkomi','daram','resident_bori'])

label qa_k2_episode:
    call r13_scene(R13_PLACES['v111_woodshed'][1],'창고','calm')
    jump r13_v111_afternoon6

testcase kkomi_independent_preparation:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_k2_setup)
    run Jump('qa_k2_episode')
    click pos (900,600) until eval (room13['v111'].get('gate')=='afternoon6') timeout 30
    pause 1.0
    run Show('qa_hidden_base_return',value=('person','kid_kkomi'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '학교에 자리가 났어. 같이 갈래?'
    click pos (900,600) until '먼저 가 버리지는 않을게' timeout 30
    click pos (900,600) until screen 'r13_hub' timeout 30
    assert eval (not r13_v111_value('acorn_recovered') and room13['location']=='v111_woodshed')
    run Show('qa_hidden_base_return',value=('object','v111_wood'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('kkomi_can_seen6') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','v111_wood'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('acorn_recovered') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('person','kid_kkomi'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '학교에 자리가 났어. 같이 갈래?'
    click pos (900,600) until eval (room13['v111'].get('gate')=='travel') timeout 60
    pause 0.8
    run Show('qa_hidden_base_return',value=('menu','map'))
    pause 0.3
    click 'QA 행동'
    pause 0.8
    run Show('qa_hidden_base_return',value='school')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval (room13['v111'].get('gate')=='handoff6') timeout 30
    assert eval (room13['location']=='school' and r13_v111_value('acorn_recovered'))
