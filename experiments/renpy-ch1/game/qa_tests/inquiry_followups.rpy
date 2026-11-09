# 변경 장면만 실제 화면 입력으로 확인한다. 2일차는 자료 확인을 마친 상태를 준비한다.
init python:
    def qa_inquiry139_domain():
        return winter_copy.deepcopy((room13['evidence'],room13['arguments'],
            r13_v111_value('tries:gate'),r13_v111_value('meeting:gate'),r13_v111_value('gate_registered')))

    def qa_chorong139_prepare():
        qa_chorong_inquiry_prepare()
        # 준비용 자료 지급 알림은 실제 신규 획득 장면이 아니므로 캡처 전에 닫는다.
        renpy.hide_screen('r13_evidence_found')
        r13_v111_set('chorong_memo_checked2',True)
        r13_v111_set('chorong_invitation_checked2',True)

    def qa_inquiry139_indices():
        return [o['index'] for o in r13_v111_binding()['options']]

testcase inquiry139_gate_original_changes_statement:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(renpy.display.screen.screens.__setitem__,('r13_book',None),R13_QA_INQUIRY_REAL_BOOK)
    pause .6
    $ qa_inquiry139_shelf=qa_gate_ledger_pointer('gate_documents')
    click pos (qa_inquiry139_shelf[0],qa_inquiry139_shelf[1])
    click pos (900,600) until eval (renpy.get_screen('r13_hub') and room13['v111']['gate']=='gate_investigate') timeout 60
    assert eval (r13_v111_owned('E02') and r13_v111_owned('E03') and not r13_v111_value('gate_application_acknowledged'))
    $ qa_inquiry139_before=qa_inquiry139_domain()
    click '돌목'
    pause until screen 'r13_topics' timeout 20
    click '자료 제시'
    pause until screen 'r13_book' timeout 20
    pause .5
    click '초대 편지'
    pause .2
    click id 'r13_ev_present'
    pause until screen 'say' timeout 20
    assert eval (r13_packet[0]=='guard' and '초대 편지군요' in r13_packet[1] and not r13_v111_value('gate_application_acknowledged'))
    screenshot 'gate-invitation-response.png'
    click pos (900,600) until screen 'r13_topics' timeout 30
    assert eval (qa_inquiry139_domain()==qa_inquiry139_before)
    click '자료 제시'
    pause until screen 'r13_book' timeout 20
    pause .5
    click '방문 신청 원본'
    pause .2
    click id 'r13_ev_present'
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='guard' and r13_packet[1]==R13_GATE_APPLICATION_QUOTE) timeout 30
    assert eval (not r13_v111_value('gate_application_acknowledged'))
    screenshot 'gate-application-acknowledgment.png'
    click pos (900,600) until screen 'r13_topics' timeout 40
    assert eval (r13_v111_value('gate_application_acknowledged') and 3 not in qa_inquiry139_indices() and qa_inquiry139_domain()==qa_inquiry139_before)
    click '근거를 대겠습니다. 둘 다 들여보내 주십시오.'
    pause until screen 'r13_proof_workspace' timeout 20
    pause until eval (qa_pw_read_scope().get('ready')) timeout 10
    assert eval (qa_pw_read_scope()['ctx']['quote']==R13_GATE_APPLICATION_QUOTE and qa_pw_read_scope()['quote_open'] and qa_pw_read_selection([]))
    assert eval (qa_pw_read_scope()['hearing_row']['target']=='MS14_D01_S03_L0010' and qa_pw_read_scope()['hearing_row']['text']==R13_GATE_APPLICATION_QUOTE)
    assert eval (qa_pw_read_scope()['view']=='list')
    screenshot 'gate-updated-statement-proof.png'
    if eval (qa_pw_read_scope()['view']=='statements'):
        click id 'r13_pw_submit'
    pause .3
    click id 'r13_pw_check_E02'
    pause .3
    click id 'r13_pw_check_E03'
    pause .3
    assert eval (qa_pw_read_selection(['V111:E02','V111:E03']))
    click id 'r13_pw_submit'
    click pos (900,600) until eval (room13['v111']['gate']=='registered_menu') timeout 60
    assert eval (r13_v111_value('meeting:gate')=='win' and r13_v111_value('gate_registered') and r13_v111_value('proof_given:함께 들어갈 근거를 고른다')==['V111:E02','V111:E03'])

testcase inquiry139_chorong_questions_and_repeat:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_chorong139_prepare)
    run Call('qa_rr_scene','r13_v111_go_box')
    pause until eval (room13['v111']['gate']=='go_box') timeout 20
    pause .6
    $ qa_inquiry139_before=qa_inquiry139_domain()
    click '초롱'
    pause until screen 'r13_topics' timeout 20
    pause .5
    screenshot 'chorong-followup-questions.png'
    click '자료 제시'
    pause until screen 'r13_book' timeout 20
    pause .5
    click '초대 편지'
    pause .2
    click id 'r13_ev_present'
    pause until screen 'say' timeout 20
    assert eval (r13_packet[0]=='resident_lamplighter' and '우체국 장부' in r13_packet[1])
    screenshot 'chorong-repeat-response.png'
    click pos (900,600) until screen 'r13_topics' timeout 30
    assert eval (qa_inquiry139_domain()==qa_inquiry139_before and qa_inquiry139_indices()==[0,1,2])
    click '두 글 모두 아내 글씨입니까?'
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='resident_lamplighter' and '방의 메모예요' in r13_packet[1]) timeout 30
    assert eval (not r13_v111_value('chorong_scope_asked2'))
    screenshot 'chorong-handwriting-scope.png'
    click pos (900,600) until screen 'r13_topics' timeout 30
    assert eval (r13_v111_value('chorong_scope_asked2') and qa_inquiry139_indices()==[0,1])
    click '왜 여기서 펴면 안 되죠?'
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='resident_lamplighter' and '우체국에서 물어보세요' in r13_packet[1]) timeout 30
    assert eval (not r13_v111_value('chorong_secrecy_asked2'))
    screenshot 'chorong-evades-reason.png'
    click pos (900,600) until eval (r13_v111_value('chorong_secrecy_asked2')) timeout 30
    assert eval (r13_v111_value('chorong_secrecy_asked2') and qa_inquiry139_indices()==[0] and qa_inquiry139_domain()==qa_inquiry139_before)
