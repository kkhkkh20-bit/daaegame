init python:
    def qa_owl_repair_setup():
        r13_edit(day=7,period=1,location='room13')
        r13_v111_set('day',7)
        for key,value in {'meeting:lamp':'win','TOK_ALIVE':True,'listed:resident_tok':False,'departed:resident_tok':False,'busy:resident_tok':None,'location:resident_tok':None,'owl_latch_seen7':None,'owl_tok_agreed7':None,'owl_tok_work7':None,'doto_promise7':None,'stove13_7':None}.items():r13_v111_set(key,value)
        store.r13_v111_talk_person=None
        r13_v111_arrive(['daram'])
label qa_owl_repair_episode:
    call r13_scene(R13_PLACES['room13'][1],'13호','calm')
    jump r13_v111_free_day7_wait

testcase owl_repair_preparation_and_night:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_owl_repair_setup)
    run Jump('qa_owl_repair_episode')
    click pos (900,600) until eval (room13['v111'].get('gate')=='free_day7') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','v111_latch7'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('owl_latch_seen7') timeout 30
    pause 0.8
    run Function(r13_edit,location='workshop')
    run Show('qa_hidden_base_return',value=('person','resident_tok'))
    pause 0.3
    click 'QA 행동'
    pause 0.5
    click '빗장 받이를 봐 주실 수 있습니까?'
    click pos (900,600) until eval r13_v111_value('owl_tok_agreed7') timeout 30
    pause 0.8
    assert eval not r13_v111_value('owl_tok_work7')
    run Function(setattr,renpy.store,'r13_v111_talk_person',None)
    run Function(r13_edit,location='room13')
    run Jump('r13_v111_free_day7_wait')
    pause 0.8
    run Show('qa_hidden_base_return',value=('object','v111_latch7'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('owl_tok_work7') timeout 30
    pause 0.8
    run Jump('r13_v111_tok_night7')
    click pos (900,600) until eval (room13['v111'].get('gate')=='travel') timeout 30
    pause 0.8
    run Show('qa_hidden_base_return',value=('menu','map'))
    pause 0.3
    click 'QA 행동'
    pause 0.8
    run Show('qa_hidden_base_return',value='clinic')
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval (r13_v111_value('prevention')=='repair') timeout 60
    assert eval (r13_v111_value('OWL_ALIVE') and not r13_v111_value('DARAM_DETAINED') and r13_v111_value('busy:resident_tok') is False)
    assert eval (not qa_nw_seen('낮에 말씀하셨잖아요') and qa_nw_seen('제가 곁에 있었어요'))
