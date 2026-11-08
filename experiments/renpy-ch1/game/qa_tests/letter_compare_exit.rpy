# 실제 호출의 review_return이 없는 구 저장과 같은 상태에서 취소·재개·명시 비교를 확인한다.
init python:
    def qa_letter_exit_prepare(single=True):
        r13_edit(day=1,period=1,location="room13")
        r13_v111_set("day",1)
        r13_v111_set("elapsed_minutes",45)
        r13_v111_set("gate_registered",True)
        r13_v111_scene("MS14_D01_S05")
        r13_v111_arrive(["daram"])
        r13_grant(["V111:E01","V111:E06","V111:E03"],"qa-letter-exit")
        claim="v111:두 편지를 나란히 본다"
        r13_pw_set_arguments(claim,[])
        store.r13_pw_views={claim:dict(view="single" if single else "list",detail="V111:E01",quote_open=True,origin_open=False)}

    def qa_letter_exit_domain():
        return winter_copy.deepcopy((room13["day"],room13["period"],room13["evidence"],room13["v111"]["values"]))

label qa_letter_exit_legacy_call:
    # 이미 저장된 None 매개변수도 화면과 반환 분기의 기본 복귀 대상으로 복구한다.
    call r13_v111_proof('두 편지를 나란히 본다',['E01','E06'],'r13_v111_room_compare','r13_v111_letter_retry',None)
    jump expression _return

testcase letter_compare_zero_selection_cancel_and_resume:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_letter_exit_prepare)
    run Call('qa_rr_scene','qa_letter_exit_legacy_call')
    pause until screen 'r13_proof_workspace' timeout 30
    pause .5
    assert eval (qa_pw_read_scope()['view']=='single' and qa_pw_read_scope()['quote_open'])
    assert eval (qa_pw_read_selection([]) and not r13_pw_submit_ok([],"compare"))
    $ qa_letter_before=qa_letter_exit_domain()
    screenshot 'letter-compare-zero-selection-detail.png'
    click id 'r13_ev_close'
    pause until screen 'r13_hub' timeout 30
    assert eval (room13['location']=='room13' and room13['v111']['gate']=='letter_compare_review')
    assert eval (qa_letter_exit_domain()==qa_letter_before and qa_pw_read_selection([]))
    screenshot 'letter-compare-cancel-room.png'
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    click '책상 위 접힌 종이'
    pause until screen 'r13_proof_workspace' timeout 30
    pause .4
    # 옛 한 장 읽기 저장의 첫 재진입은 두 글 읽기로 맞춘다. 제출 선택은 바꾸지 않는다.
    assert eval (qa_pw_read_scope()['view']=='pair' and qa_pw_read_scope()['live_pair']==('V111:E01','V111:E06') and not qa_pw_read_scope()['quote_open'])
    assert eval (qa_letter_exit_domain()==qa_letter_before and qa_pw_read_selection([]))
    click id 'r13_pw_back_list'
    if eval (not qa_pw_read_has('r13_pw_check_E03')):
        click id 'r13_pw_next' until eval qa_pw_read_has('r13_pw_check_E03') timeout 20
    click id 'r13_pw_check_E03'
    click id 'r13_pw_investigate'
    pause until screen 'r13_hub' timeout 30
    assert eval (qa_letter_exit_domain()==qa_letter_before and qa_pw_read_selection(['V111:E03']))
    click '책상 위 접힌 종이'
    pause until screen 'r13_proof_workspace' timeout 30
    pause until eval (qa_pw_read_scope().get('ready')) timeout 10
    click id 'r13_pw_pair'
    pause until eval (qa_pw_read_scope().get('view')=='pair') timeout 10
    if eval (qa_pw_read_has('r13_pw_pick_0')):
        click id 'r13_pw_pick_0'
    else:
        click id 'r13_pw_change_0'
    if eval (not qa_pw_read_has('r13_pw_open_E01')):
        click id 'r13_pw_prev' until eval qa_pw_read_has('r13_pw_open_E01') timeout 20
    click id 'r13_pw_open_E01'
    if eval (qa_pw_read_has('r13_pw_pick_1')):
        click id 'r13_pw_pick_1'
    else:
        click id 'r13_pw_change_1'
    if eval (not qa_pw_read_has('r13_pw_open_E06')):
        click id 'r13_pw_next' until eval qa_pw_read_has('r13_pw_open_E06') timeout 20
    click id 'r13_pw_open_E06'
    pause .4
    assert eval (qa_pw_read_scope()['live_pair']==('V111:E01','V111:E06') and qa_pw_read_selection(['V111:E03']))
    assert eval (qa_pw_read_has('r13_pw_investigate') and qa_pw_read_has('r13_pw_observe'))
    keysym 'K_ESCAPE'
    pause until screen 'r13_hub' timeout 30
    assert eval (qa_letter_exit_domain()==qa_letter_before and qa_pw_read_selection(['V111:E03']))
    click '책상 위 접힌 종이'
    pause until screen 'r13_proof_workspace' timeout 30
    pause .4
    assert eval (qa_pw_read_scope()['view']=='pair' and qa_pw_read_scope()['live_pair']==('V111:E01','V111:E06'))
    screenshot 'letter-compare-explicit-pair-submit.png'
    click id 'r13_pw_submit'
    click pos (900,600) until screen 'choice' timeout 45
    assert eval (r13_v111_value('proof_given:두 편지를 나란히 본다')==['V111:E01','V111:E06'] and room13['period']==2)

testcase letter_compare_wrong_read_pair_uses_original_verdict:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_letter_exit_prepare,False)
    run Call('qa_rr_scene','qa_letter_exit_legacy_call')
    pause until screen 'r13_proof_workspace' timeout 30
    pause .4
    $ qa_letter_before=qa_letter_exit_domain()
    pause until eval (qa_pw_read_scope().get('ready')) timeout 10
    click id 'r13_pw_pair'
    pause until eval (qa_pw_read_scope().get('view')=='pair') timeout 10
    if eval (qa_pw_read_has('r13_pw_pick_0')):
        click id 'r13_pw_pick_0'
    else:
        click id 'r13_pw_change_0'
    if eval (not qa_pw_read_has('r13_pw_open_E01')):
        click id 'r13_pw_prev' until eval qa_pw_read_has('r13_pw_open_E01') timeout 20
    click id 'r13_pw_open_E01'
    click id 'r13_pw_pick_1'
    if eval (not qa_pw_read_has('r13_pw_open_E03')):
        click id 'r13_pw_next' until eval qa_pw_read_has('r13_pw_open_E03') timeout 20
    click id 'r13_pw_open_E03'
    assert eval (qa_pw_read_selection([]))
    click id 'r13_pw_submit'
    pause until screen 'say' timeout 30
    click pos (900,600) until screen 'r13_proof_workspace' timeout 30
    assert eval (v111_wrong_target=='r13_v111_letter_retry' and not r13_v111_value('proof_given:두 편지를 나란히 본다'))
    assert eval (qa_letter_exit_domain()==qa_letter_before)
    pause until eval (qa_pw_read_scope().get('ready')) timeout 10
    click id 'r13_pw_change_1'
    pause until eval (qa_pw_read_scope().get('view')=='list') timeout 10
    if eval (not qa_pw_read_has('r13_pw_open_E06')):
        click id 'r13_pw_next' until eval qa_pw_read_has('r13_pw_open_E06') timeout 20
    click id 'r13_pw_open_E06'
    click id 'r13_pw_submit'
    click pos (900,600) until screen 'choice' timeout 45
    assert eval (r13_v111_value('proof_given:두 편지를 나란히 본다')==['V111:E01','V111:E06'])
