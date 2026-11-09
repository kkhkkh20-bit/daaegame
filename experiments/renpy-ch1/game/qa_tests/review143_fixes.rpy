# 상태 준비 뒤 실제 표시 줄과 기존 선택 화면으로 수정 영역을 검사한다.
init python:
    def qa_review143_prepare(day):
        r13_v111_set('day',day)
        r13_edit(day=day,location='gate' if day==5 else 'room13',period=1)
        store.r13_pw_views={}
        store.qa_review143_variants=tuple(config.variants)
        renpy.hide_screen('r13_evidence_found')

    def qa_review143_enter(scene):
        day=R13_V111['scene_days'][scene]
        r13_v111_set('day',day)
        r13_edit(day=day)
        items,values=R13_V111_ENTRY.get(scene,([],{}))
        r13_grant(['V111:'+k for k in items],'검수 진입 조건')
        for key,value in values.items():r13_v111_set(key,value)
        if scene=='MS14_D02_S05':r13_v111_set('D02_afternoon','nero')
        if scene=='MS14_D03_S01':
            r13_flag('v111:applied:option:sleep2:0')
            r13_v111_set('portrait','unfinished')
            r13_grant(['V111:E09'],'검수 초상 수령')
        if scene=='MS14_D05_S04':r13_v111_set('bami_status','cleared')
        r13_v111_scene(scene)

    def qa_review143_remember_domain():
        renpy.test.review143_domain=qa_pw_read_domain()

    def qa_review143_rows():
        return renpy.get_screen('r13_proof_workspace').scope['hearing_rows']

label qa_review143_hearing:
    $ r13_v111_set('bami_cold4',True)
    $ r13_grant(['V111:E20','V111:E22','V111:E23','V111:E24'],'검수 준비')
    $ qa_review143_enter('MS14_D05_S03')
    call r13_lines(qa_hearing141_packet('MS14_D05_S03_L0009'),'qa143:height')
    call r13_lines(qa_hearing141_packet('NW_D05_S03_SL01'),'qa143:fence')
    $ v111_claim='v111:밤이 혐의의 근거를 확인한다'
    call screen r13_proof_workspace(v111_claim,'밤이 혐의의 근거를 확인한다')
    jump r13_v111_letter_compare_review

label qa_review143_dialogue:
    $ r13_v111_set('day',2)
    $ r13_edit(day=2,location='room13',period=2)
    $ qa_review143_enter('MS14_D02_S05')
    call r13_scene(R13_PLACES['room13'][1],R13_PLACES['room13'][0],'calm')
    call r13_lines(r13_v111_lines(['MS14_D02_S05_L0007','MS14_D02_S05_L0008','MS14_D02_S05_L0009']),'qa143:portrait_goal')
    $ r13_v111_set('day',3)
    $ r13_edit(day=3,location='square',period=0)
    $ qa_review143_enter('MS14_D03_S01')
    call r13_scene(R13_PLACES['square'][1],R13_PLACES['square'][0],'calm')
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L9101']),'qa143:portrait_receipt')
    $ r13_v111_set('day',5)
    $ r13_edit(day=5,location='gate',period=1)
    $ qa_review143_enter('MS14_D05_S04')
    call r13_scene(R13_PLACES['gate'][1],R13_PLACES['gate'][0],'calm')
    call r13_lines(r13_v111_lines(['MS14_D05_S04_L0022','MS14_D05_S04_L0023','MS14_D05_S04_L0024']),'qa143:chorong_return')
    jump r13_v111_reply_handoff5

testcase review143_hearing_titles:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_review143_prepare,5)
    run Call('qa_rr_scene','qa_review143_hearing')
    click pos (900,600) until screen 'r13_proof_workspace' timeout 45
    pause until eval (qa_pw_read_scope().get('ready')) timeout 10
    assert eval (len(qa_review143_rows())==2 and len(set(r['title'] for r in qa_review143_rows()))==2)
    screenshot '143-two-distinct-titles-pc.png'
    click id 'r13_hearing_target_NW_D05_S03_SL01'
    pause .3
    assert eval (qa_pw_read_scope()['hearing_row']['target']=='NW_D05_S03_SL01' and '울타리' in qa_pw_read_scope()['hearing_row']['text'])
    run Function(qa_review143_remember_domain)
    run Function(renpy.save,'review143-titles')
    run Function(renpy.load,'review143-titles')
    pause .5
    assert eval (qa_pw_read_domain()==renpy.test.review143_domain and qa_pw_read_scope()['hearing_row']['target']=='NW_D05_S03_SL01')
    $ config.variants=['touch','pc',None]
    pause .5
    screenshot '143-two-distinct-titles-touch.png'
    click id 'r13_hearing_target_MS14_D05_S03_L0009'
    pause .3
    assert eval (qa_pw_read_scope()['hearing_row']['target']=='MS14_D05_S03_L0009' and '키가 맞으면' in qa_pw_read_scope()['hearing_row']['text'])
    $ config.variants=list(qa_review143_variants)

testcase review143_dialogue_connections:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_review143_prepare,5)
    run Call('qa_rr_scene','qa_review143_dialogue')
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D02_S05_L0007') timeout 30
    screenshot '143-portrait-search-first.png'
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('source_id')=='NW_RU_D03_E09_03') timeout 45
    screenshot '143-portrait-receipt.png'
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D05_S04_L0022' and renpy.get_screen('say') and '초롱을부르자' in ''.join(renpy.get_screen('say').scope.get('what','').split())) timeout 45
    screenshot '143-chorong-return.png'
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D05_S04_L0024') timeout 45
    screenshot '143-chorong-answer.png'
