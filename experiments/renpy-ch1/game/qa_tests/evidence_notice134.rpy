# 획득은 기존 grant를 쓰고, 알림의 표시 시간·순서만 준비한 상태에서 검증한다.
init python:
    def qa_notice134_separate_grants():
        # 같은 callback 안에서 화면이 한 번도 그려지기 전에 자료가 연속 도착한다.
        for key in ['V111:E02','V111:E03','V111:E05']:
            r13_grant([key],'qa:notice134')

    def qa_notice134_screen():
        return renpy.get_screen('r13_evidence_found')
    def qa_notice134_current():
        screen=qa_notice134_screen()
        if not screen:return None
        keys=screen.scope.get('notice_keys',screen.scope.get('keys',[]))
        return keys[screen.scope.get('item_index',0)] if keys else None

testcase evidence134_hidden_queue_and_append:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Hide('r13_evidence_found')
    $ qa_notice134_values=winter_copy.deepcopy(room13['v111']['values'])
    run Function(qa_notice134_separate_grants)
    pause until screen 'r13_evidence_found' timeout 10
    pause .4
    assert eval (qa_notice134_current()=='V111:E02' and r13_evidence_notice_visible())
    screenshot 'notice134-list-acquired.png'
    run Show('pause_menu')
    pause 4.0
    assert eval (qa_notice134_current()=='V111:E02' and not r13_evidence_notice_visible())
    run Hide('pause_menu')
    pause .4
    assert eval (qa_notice134_current()=='V111:E02' and r13_evidence_notice_visible())
    screenshot 'notice134-uncovered-still-list.png'
    pause until eval (qa_notice134_current()=='V111:E03') timeout 6
    run Function(r13_grant,['V111:E04'],'qa:notice134:append')
    pause .4
    assert eval (qa_notice134_current()=='V111:E03' and qa_notice134_screen().scope['item_index']==1)
    assert eval (list(qa_notice134_screen().scope['notice_keys'])==['V111:E02','V111:E03','V111:E05','V111:E04'])
    screenshot 'notice134-original-acquired.png'
    run Function(r13_grant,['V111:E02'],'qa:notice134:already-owned')
    assert eval (qa_notice134_current()=='V111:E03')
    pause until eval (qa_notice134_current()=='V111:E05') timeout 6
    pause .4
    screenshot 'notice134-corrected-list-acquired.png'
    pause until eval (qa_notice134_current()=='V111:E04') timeout 6
    pause until eval (qa_notice134_screen() is None) timeout 6
    assert eval (room13['v111']['values']==qa_notice134_values)
