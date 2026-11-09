label qa_resident145_start(person):
    $ r13_v111_set('day',2)
    $ r13_edit(day=2,location='inn' if person=='resident_yeoni' else 'square',period=1 if person=='resident_yeoni' else 0)
    $ room13['v111']['scene']='MS14_D02_S04' if person=='resident_yeoni' else 'MS14_D02_S01'
    $ r13_v111_arrive(['daram'])
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    call r13_v111_wait('chorong_documents2')
    return

testcase resident145_seol_dialogue:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_resident145_start','resident_seol')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '설이'
    pause until screen 'r13_topics' timeout 15
    pause .7
    screenshot '145-seol-question.png'
    click '정해진 때에 치는 종입니까?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_v111_value('resident_chat_read:life:resident_seol:work') is True and room13['day']==2 and room13['v111']['gate']=='chorong_documents2')
    assert eval (qa_nw_seen('그래서 종소리 뜻을 말로도 알려야 해요.'))
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 10
    pause .7
    click '설이'
    pause until screen 'r13_topics' timeout 15
    assert eval (r13_v111_questions('resident_seol')[-1][2])

testcase resident145_hyeoni_song:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_resident145_start','resident_hyeoni')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    click '오른쪽 구역' until '현이' timeout 20
    pause .7
    click '현이'
    pause until screen 'r13_topics' timeout 15
    pause .7
    click '한 곡 들려주시겠어요?'
    click pos (900,600) until eval (renpy.get_screen('say') and '눈은' in renpy.get_screen('say').scope.get('what','')) timeout 20
    screenshot '145-hyeoni-song.png'
    click pos (900,600) until screen 'r13_topics' timeout 20
    assert eval (r13_v111_value('resident_chat_read:hyeoni:song') is True and room13['day']==2)
    assert eval (r13_hyeoni_verses()==[R13_V111_RESIDENT_WINTER_VERSE])

testcase resident145_yeoni_sewing:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_resident145_start','resident_yeoni')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '여니'
    pause until screen 'r13_topics' timeout 15
    pause .7
    screenshot '145-yeoni-question.png'
    click '수선을 맡기기 전에 준비할 것이 있습니까?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_v111_value('resident_chat_read:smalltalk:yeoni_seam') is True and room13['day']==2 and room13['v111']['gate']=='chorong_documents2')

testcase resident145_badook_patrol:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_resident145_start','resident_badook')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '바둑이'
    pause until screen 'r13_topics' timeout 15
    pause .7
    click '밤 순찰도 혼자 다닙니까?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_v111_value('resident_chat_read:life:resident_badook:work') is True and room13['day']==2)
    screenshot '145-badook-question-read.png'

testcase resident145_owl_records:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa_resident145_start','resident_owlgp')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    click '부엉이 할아버지'
    pause until screen 'r13_topics' timeout 15
    pause .7
    click '지금도 직접 기록을 하십니까?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_v111_value('resident_chat_read:life:resident_owlgp:work') is True and room13['day']==2)
    screenshot '145-owl-question-read.png'
