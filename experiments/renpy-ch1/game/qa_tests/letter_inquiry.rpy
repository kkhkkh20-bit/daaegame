# 첫 방의 관찰 선택과 초롱의 두 자료 제시 순서를 실제 본편에서 확인한다.
init 998 python:
    R13_QA_INQUIRY_REAL_BOOK=renpy.display.screen.screens[("r13_book",None)]

init python:
    def qa_chorong_inquiry_prepare():
        renpy.display.screen.screens[('r13_book',None)]=R13_QA_INQUIRY_REAL_BOOK
        r13_flag('v111:applied:option:sleep1:0')
        r13_v111_set('day',2)
        r13_edit(location='square',period=0)
        r13_v111_scene('MS14_D02_S01')
        r13_v111_arrive(['daram','resident_lamplighter'])
        r13_grant(['V111:E01','V111:E06','V111:E03'],'qa-chorong-inquiry')
        store.r13_book_views={}
        r13_v111_set('gate_registered',True)
        r13_v111_set('location:daram','square')

testcase room_letter_reading_without_spot_quiz:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_letter_exit_prepare,False)
    run Call('qa_rr_scene','r13_v111_letter_compare')
    pause until screen 'r13_proof_workspace' timeout 30
    pause until eval (qa_pw_read_scope().get('ready')) timeout 10
    assert eval (r13_v111_value('letter_inquiry_mode138') and not r13_v111_value('letter_tail_observed'))
    screenshot 'letters-free-reading.png'
    click id 'r13_pw_submit'
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D01_S05_L0033') timeout 45
    assert eval ('엄마 이름도' in r13_packet[1] and not r13_v111_value('letter_tail_observed'))
    click pos (900,600) until screen 'r13_hub' timeout 45
    assert eval (room13['v111']['gate']=='chorong_inquiry1' and room13['period']==0 and r13_v111_value('proof_given:두 편지를 나란히 본다')==['V111:E01','V111:E06'])

testcase chorong_memo_first_cancel_and_other_record:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_chorong_inquiry_prepare)
    run Call('qa_rr_scene','r13_v111_chorong')
    click pos (900,600) until eval (renpy.get_screen('r13_hub') and room13['v111']['gate']=='chorong_documents2') timeout 50
    click '초롱'
    pause until screen 'r13_book' timeout 30
    pause .5
    screenshot 'debug-chorong-cancel-book.png'
    click id 'r13_ev_stop'
    pause until screen 'r13_hub' timeout 30
    assert eval (not r13_v111_value('chorong_memo_checked2') and not r13_v111_value('chorong_invitation_checked2'))
    click '초롱'
    pause until screen 'r13_book' timeout 30
    pause .5
    click '방문 신청 원본'
    click id 'r13_ev_present'
    pause until screen 'say' timeout 20
    click pos (900,600) until screen 'r13_book' timeout 30
    assert eval (not r13_v111_value('chorong_memo_checked2') and not r13_v111_value('chorong_invitation_checked2'))
    pause .4
    click '방의 메모'
    pause .2
    click id 'r13_ev_present'
    pause until screen 'say' timeout 20
    click pos (900,600) until screen 'r13_book' timeout 60
    assert eval (r13_v111_value('chorong_memo_checked2') and not r13_v111_value('chorong_invitation_checked2'))
    screenshot 'chorong-memo-first.png'
    pause .4
    screenshot 'debug-chorong-invitation-book.png'
    click '초대 편지'
    pause .2
    click id 'r13_ev_present'
    pause until screen 'say' timeout 20
    click pos (900,600) until eval (renpy.get_screen('r13_hub') and room13['v111']['gate']=='go_box') timeout 60
    assert eval (r13_v111_value('chorong_memo_checked2') and r13_v111_value('chorong_invitation_checked2'))

testcase chorong_invitation_first:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_chorong_inquiry_prepare)
    run Call('qa_rr_scene','r13_v111_chorong')
    click pos (900,600) until eval (renpy.get_screen('r13_hub') and room13['v111']['gate']=='chorong_documents2') timeout 50
    click '초롱'
    pause until screen 'r13_book' timeout 30
    pause .5
    pause .4
    screenshot 'debug-chorong-invitation-book.png'
    click '초대 편지'
    pause .2
    click id 'r13_ev_present'
    pause until screen 'say' timeout 20
    click pos (900,600) until screen 'r13_book' timeout 45
    assert eval (r13_v111_value('chorong_invitation_checked2') and not r13_v111_value('chorong_memo_checked2'))
    screenshot 'chorong-invitation-first.png'
    pause .4
    click '방의 메모'
    pause .2
    click id 'r13_ev_present'
    pause until screen 'say' timeout 20
    click pos (900,600) until eval (renpy.get_screen('r13_hub') and room13['v111']['gate']=='go_box') timeout 60
    assert eval (r13_v111_value('chorong_memo_checked2') and r13_v111_value('chorong_invitation_checked2'))
