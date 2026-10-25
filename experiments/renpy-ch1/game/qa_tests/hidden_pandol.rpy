init python:
    def qa_hp_setup():
        qa_nw_day14('prevented')
        r13_v111_set('day',11)
        r13_edit(day=11,location='school',period=3)
        r13_v111_set('meeting:hypothesis','win')
        for key in ('visit_allowed','family_seen','wood_reserved'):
            r13_hp_set(key)
        for key in ('stove_seen','consent','wood_delivered','tongs','heat_replaced','care_handed'):
            r13_hp_set(key,None)

label qa_hp_episode:
    call r13_hp_visit11
    $ r13_v111_set('departed:nabi',True)
    call r13_hp_handoff13
    $ qa_hp_missing = not r13_hp_value('care_handed')
    $ r13_v111_set('departed:nabi',False)
    $ r13_v111_set('listed:nabi',False)
    $ r13_v111_set('alive:nabi',True)
    call r13_hp_handoff13
    call screen r13_confirm('가족 시험 완료',yes='끝',no='끝')
    return

testcase hidden_pandol_heat_and_care:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_hp_setup)
    run Jump('qa_hp_episode')
    click pos (900,600) until eval (room13['v111'].get('gate')=='hp_house11') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hp_stove'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click pos (900,600) until eval r13_hp_value('stove_seen') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('person','npc_pandol'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '장작으로 바꿔도 되겠습니까?'
    click pos (900,600) until eval r13_hp_value('consent') timeout 90
    pause 0.7
    click '돌아가기'
    pause 0.5
    run Show('qa_hidden_base_return',value=('object','hp_wood'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click pos (900,600) until eval r13_hp_value('wood_delivered') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hp_tongs'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click pos (900,600) until eval r13_hp_value('tongs') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('object','hp_stove'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click pos (900,600) until eval r13_hp_value('heat_replaced') timeout 90
    pause 0.7
    run Show('qa_hidden_base_return',value=('person','npc_pandol'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '학교로 돌아가겠습니다.'
    click pos (900,600) until screen 'r13_confirm' timeout 90
    assert eval (qa_hp_missing and r13_hp_value('care_handed') and r13_hp_value('care_person')=='nabi' and room13['location']=='school')
