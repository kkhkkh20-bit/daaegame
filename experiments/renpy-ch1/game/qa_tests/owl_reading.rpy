init python:
    def qa_owl_reading_setup(alive=True):
        r13_edit(day=8,period=0,location='room13')
        r13_v111_set('day',8)
        r13_v111_set('OWL_ALIVE',alive)
        r13_v111_set('owl_reading8_done',None)
        r13_v111_set('location:resident_owlgp',None)
        r13_v111_set('busy:resident_owlgp',None)
        r13_v111_arrive(['resident_owlgp','daram'])
label qa_owl_reading_episode:
    call r13_scene(R13_PLACES['room13'][1],'13호','calm')
    call r13_v111_owl_reading8
    call r13_v111_owl_reading8
    call screen r13_confirm('기록 읽기 시험 완료',yes='끝',no='끝')
    return

testcase owl_reading_alive:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_owl_reading_setup)
    run Jump('qa_owl_reading_episode')
    click pos (900,600) until screen 'r13_confirm' timeout 60
    assert eval (r13_v111_value('owl_reading8_done') and qa_nw_seen('남의 빈칸이지') and qa_nw_seen('내 빈칸은 장수가'))

testcase owl_reading_absent:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_owl_reading_setup,False)
    run Jump('qa_owl_reading_episode')
    click pos (900,600) until screen 'r13_confirm' timeout 60
    assert eval (not r13_v111_value('owl_reading8_done') and not qa_nw_seen('남의 빈칸이지'))
