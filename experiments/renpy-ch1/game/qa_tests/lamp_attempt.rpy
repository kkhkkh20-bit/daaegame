init python:
    def qa_la_setup():
        r13_edit(day=3,period=0,location='square')
        r13_v111_set('day',3)
        r13_flag('v111:applied:option:sleep2:0')
        r13_v111_set('lamp_bound2',True)
        r13_v111_set('meeting:lamp',None)
        r13_v111_set('tries:lamp',0)
        r13_v111_set('piko_sheltered',False)
        for key in ('lamp_field_done3','lamp_knife_done3','lamp_store_done3'):
            r13_v111_set(key,None)
        store.r13_v111_talk_person=None
    def qa_la_submit(keys):
        store.room13['arguments'][store.v111_claim]=['V111:'+k for k in keys]
        store.r13_v111_talk_person=None

init python:
    def qa_la_meeting_setup():
        qa_la_setup()
        for key in ('NW_LA_CHECK','NW_LA_FIELD','NW_LA_KNIFE','NW_LA_OFFER'):
            r13_nw_acquire(key)
        store.r13_meeting_checkpoint_state=None

testcase lamp_attempt_field_and_win:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_la_setup)
    run Jump('r13_lamp_attempt3')
    click pos (900,600) until eval (room13['v111'].get('gate')=='lamp_attempt_field3') timeout 60
    pause 0.8
    assert eval (r13_v111_value('piko_alive') and not r13_v111_value('piko_sheltered') and r13_v111_owned('E09') and not r13_v111_owned('E15') and not r13_v111_owned('E16'))
    run Show('qa_hidden_base_return',value=('object','lamp'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('lamp_field_done3') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('person','resident_siluk'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '칼과 조각의 대조를 부탁한다'
    click pos (900,600) until eval r13_v111_value('lamp_knife_done3') timeout 30
    pause 0.8
    run Function(r13_edit,location='store')
    run Show('qa_hidden_base_return',value=('person','resident_madam'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '매입 장부와 약속한 값을 확인한다'
    click pos (900,600) until eval r13_v111_value('lamp_store_done3') timeout 30
    pause 0.8
    run Function(r13_edit,location='square')
    run Show('qa_hidden_base_return',value=('person','resident_tok'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '공방에서 함께 확인한다'
    click pos (900,600) until screen 'r13_crisis_proof' timeout 60
    run Function(qa_la_submit,['NW_LA_CHECK','NW_LA_FIELD'])
    run Show('qa_hidden_base_return',value='argue')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval (key=='남아 있는 돌과 칼의 사용을 연결한다') timeout 30
    pause 0.8
    run Function(qa_la_submit,['NW_LA_CHECK','NW_LA_FIELD','NW_LA_KNIFE'])
    run Show('qa_hidden_base_return',value='argue')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval (r13_v111_value('meeting:lamp')=='win') timeout 30
    assert eval (not r13_v111_owned('E15') and not r13_v111_owned('E16') and r13_v111_owned('NW_LA_OFFER'))

testcase lamp_attempt_lose:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_la_meeting_setup)
    run Jump('r13_lamp_attempt_open3')
    click pos (900,600) until screen 'r13_crisis_proof' timeout 60
    run Function(r13_v111_set,'tries:lamp',r13_nw_tries_max('lamp')-1)
    run Function(qa_la_submit,['NW_LA_OFFER'])
    run Show('qa_hidden_base_return',value='argue')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until '회의를 처음부터 다시' timeout 30
    click '회의를 처음부터 다시'
    click pos (900,600) until screen 'r13_crisis_proof' timeout 30
    assert eval (key=='수리 뒤 새로 생긴 파손을 가린다' and r13_v111_value('tries:lamp') in (None,0) and not r13_v111_owned('E15'))
    run Function(r13_v111_set,'tries:lamp',r13_nw_tries_max('lamp')-1)
    run Function(qa_la_submit,['NW_LA_OFFER'])
    run Show('qa_hidden_base_return',value='argue')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until '결과를 받아들인다' timeout 30
    click '결과를 받아들인다'
    click pos (900,600) until eval (r13_v111_value('meeting:lamp')=='lose') timeout 30
    assert eval (bool(r13_v111_value('listed:resident_tok'))==True)

testcase lamp_attempt_partial:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_la_meeting_setup)
    run Jump('r13_lamp_attempt_open3')
    click pos (900,600) until screen 'r13_crisis_proof' timeout 60
    run Function(qa_la_submit,['NW_LA_CHECK','NW_LA_FIELD'])
    run Show('qa_hidden_base_return',value='argue')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval (key=='남아 있는 돌과 칼의 사용을 연결한다') timeout 30
    pause 0.8
    run Function(r13_v111_set,'tries:lamp',r13_nw_tries_max('lamp')-1)
    run Function(qa_la_submit,['NW_LA_OFFER'])
    run Show('qa_hidden_base_return',value='argue')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until '결과를 받아들인다' timeout 30
    click '결과를 받아들인다'
    click pos (900,600) until eval (r13_v111_value('meeting:lamp')=='partial') timeout 30
    assert eval (bool(r13_v111_value('listed:resident_tok'))==False)
