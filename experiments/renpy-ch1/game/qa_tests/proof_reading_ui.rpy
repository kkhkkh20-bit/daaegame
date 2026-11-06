# 읽기 UI 회귀. 중간 조사 상태는 기존 fixture로 준비하고 실제 화면 입력을 검사한다.
# SDK 실행은 메인 작업자가 직렬로 맡는다. 이 파일은 정답·자료·생사를 변경하는 제품 코드를 추가하지 않는다.
init python:
    def qa_pw_read_prepare(touch=False,large=False):
        # 실제 1~3일 완주가 아니라 회의 직전의 보유 자료·동의 상태 fixture다.
        store.qa_pw_read_ui_before=(store.r13_touch_ui,persistent.room13_large_text,persistent.room13_text_small)
        store.r13_touch_ui=lambda: bool(touch)
        persistent.room13_large_text=bool(large)
        persistent.room13_text_small=False
        store.r13_pw_views={}
        qa_nw_day3_meeting_ready()

    def qa_pw_read_restore():
        original,large,small=store.qa_pw_read_ui_before
        store.r13_touch_ui=original
        persistent.room13_large_text=large
        persistent.room13_text_small=small
        renpy.restart_interaction()

    def qa_pw_read_scope():
        screen=renpy.get_screen("r13_proof_workspace")
        return screen.scope if screen else {}

    def qa_pw_read_has(control_id):
        return renpy.get_widget("r13_proof_workspace",control_id) is not None

    def qa_pw_read_domain():
        # 읽음 표시 records.seen과 UI 기억은 허용한다. 보유 자료와 모든 분기 값은 고정한다.
        return winter_copy.deepcopy((store.room13["evidence"],store.room13.get("v111",{}).get("values",{})))

    def qa_pw_read_selection(expected):
        return list(store.room13["arguments"].get(store.v111_claim,[]))==list(expected)

    def qa_pw_read_ranges():
        result=[]
        for control_id in ("r13_pw_read_0","r13_pw_read_1"):
            viewport=renpy.get_widget("r13_proof_workspace",control_id)
            if viewport is None:return None
            result.append((viewport.yadjustment.range,viewport.yadjustment.value))
        return tuple(result)

    def qa_pw_read_log_ranges():
        renpy.log("자료 읽기 뷰포트 범위·현재위치: %r"%(qa_pw_read_ranges(),))

    def qa_pw_read_bottom():
        for control_id in ("r13_pw_read_0","r13_pw_read_1"):
            viewport=renpy.get_widget("r13_proof_workspace",control_id)
            if viewport is not None:viewport.yadjustment.change(viewport.yadjustment.range)
        renpy.restart_interaction()


testcase proof_reading_pc_selection_independent:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_read_prepare,False,False)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .6
    $ qa_pw_read_before=qa_pw_read_domain()
    assert eval (qa_pw_read_scope()["view"]=="list" and qa_pw_read_scope()["L"]["quote_h"]==0)
    assert eval (qa_pw_read_selection([]) and not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    # 비활성 제출 위치를 실제로 눌러도 화면·기회·선택이 그대로다.
    click pos (1086,600)
    pause .3
    assert screen "r13_proof_workspace"
    assert eval (qa_pw_read_domain()==qa_pw_read_before and qa_pw_read_selection([]))
    click id "r13_pw_pair"
    click id "r13_pw_pick_0"
    if eval (not qa_pw_read_has("r13_pw_open_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E11") timeout 20
    click id "r13_pw_open_E11"
    assert eval (qa_pw_read_scope()["view"]=="pair" and qa_pw_read_scope()["live_pair"]==("V111:E11",None))
    click id "r13_pw_pick_1"
    if eval (not qa_pw_read_has("r13_pw_open_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E13") timeout 20
    click id "r13_pw_open_E13"
    pause .6
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13") and qa_pw_read_selection([]))
    assert eval (qa_pw_read_domain()==qa_pw_read_before and not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    assert eval (r13_pw_read_groups("V111:E11")==[("점검장에 적힌 내용",r13_evidence_facts("V111:E11"))])
    assert eval (r13_pw_read_groups("V111:E13")[-1]==("함께 들은 말",r13_evidence_facts("V111:E13")[-1:]))
    assert eval (qa_pw_read_ranges() is not None and all(value==0 for scroll_range,value in qa_pw_read_ranges()))
    run Function(qa_pw_read_log_ranges)
    assert eval (all(scroll_range<=1 for scroll_range,value in qa_pw_read_ranges()))
    screenshot "proof_reading_pc_selection_independent-pair-zero-selection.png"

    # 발언은 기본 접힘이다. 펼치고 접어도 제출 묶음·기회가 바뀌지 않는다.
    click id "r13_pw_fold"
    pause .3
    assert eval (qa_pw_read_scope()["quote_open"] and qa_pw_read_scope()["L"]["quote_h"]>0)
    click id "r13_pw_fold"
    pause .3
    assert eval (not qa_pw_read_scope()["quote_open"] and qa_pw_read_scope()["L"]["quote_h"]==0)
    click id "r13_pw_back_list"
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_prev" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    assert eval (qa_pw_read_scope()["view"]=="list" and qa_pw_read_selection(["V111:E11"]))
    if eval (not qa_pw_read_has("r13_pw_open_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E13") timeout 20
    click id "r13_pw_open_E13"
    assert eval (qa_pw_read_scope()["view"]=="single" and qa_pw_read_scope()["detail"]=="V111:E13")
    assert eval (qa_pw_read_selection(["V111:E11"]) and r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    click id "r13_pw_origin"
    pause .3
    assert eval (qa_pw_read_scope()["origin_open"] and qa_pw_read_selection(["V111:E11"]))
    click id "r13_pw_pair"
    pause .3
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13") and qa_pw_read_scope()["origin_open"])
    assert eval (qa_pw_read_selection(["V111:E11"]) and qa_pw_read_domain()==qa_pw_read_before)
    click id "r13_pw_origin"
    click id "r13_pw_single"
    pause .3
    assert eval (qa_pw_read_scope()["detail"]=="V111:E13" and not qa_pw_read_scope()["origin_open"])
    screenshot "proof_reading_pc_selection_independent-single-keeps-selection.png"
    click id "r13_pw_back_list"
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_prev" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    assert eval (qa_pw_read_selection([]) and qa_pw_read_domain()==qa_pw_read_before)
    assert eval (not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    run Function(qa_pw_read_restore)

testcase proof_reading_touch_selection_independent:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_read_prepare,True,False)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .6
    $ qa_pw_read_before=qa_pw_read_domain()
    assert eval (qa_pw_read_scope()["view"]=="list" and qa_pw_read_scope()["L"]["quote_h"]==0)
    assert eval (qa_pw_read_selection([]) and not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    # 비활성 제출 위치를 실제로 눌러도 화면·기회·선택이 그대로다.
    click pos (1086,600)
    pause .3
    assert screen "r13_proof_workspace"
    assert eval (qa_pw_read_domain()==qa_pw_read_before and qa_pw_read_selection([]))
    click id "r13_pw_pair"
    click id "r13_pw_pick_0"
    if eval (not qa_pw_read_has("r13_pw_open_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E11") timeout 20
    click id "r13_pw_open_E11"
    assert eval (qa_pw_read_scope()["view"]=="pair" and qa_pw_read_scope()["live_pair"]==("V111:E11",None))
    click id "r13_pw_pick_1"
    if eval (not qa_pw_read_has("r13_pw_open_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E13") timeout 20
    click id "r13_pw_open_E13"
    pause .6
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13") and qa_pw_read_selection([]))
    assert eval (qa_pw_read_domain()==qa_pw_read_before and not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    assert eval (r13_pw_read_groups("V111:E11")==[("점검장에 적힌 내용",r13_evidence_facts("V111:E11"))])
    assert eval (r13_pw_read_groups("V111:E13")[-1]==("함께 들은 말",r13_evidence_facts("V111:E13")[-1:]))
    assert eval (qa_pw_read_ranges() is not None and all(value==0 for scroll_range,value in qa_pw_read_ranges()))
    run Function(qa_pw_read_log_ranges)
    # 터치·큰 글씨는 기존 긴 문장을 유지한다. 필요한 스크롤의 끝까지 접근할 수 있어야 한다.
    screenshot "proof_reading_touch_selection_independent-pair-zero-selection.png"
    run Function(qa_pw_read_bottom)
    pause .3
    assert eval (all(abs(scroll_range-value)<=1 for scroll_range,value in qa_pw_read_ranges()))
    screenshot "proof_reading_touch_selection_independent-pair-scroll-end.png"
    # 발언은 기본 접힘이다. 펼치고 접어도 제출 묶음·기회가 바뀌지 않는다.
    click id "r13_pw_fold"
    pause .3
    assert eval (qa_pw_read_scope()["quote_open"] and qa_pw_read_scope()["L"]["quote_h"]>0)
    click id "r13_pw_fold"
    pause .3
    assert eval (not qa_pw_read_scope()["quote_open"] and qa_pw_read_scope()["L"]["quote_h"]==0)
    click id "r13_pw_back_list"
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_prev" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    assert eval (qa_pw_read_scope()["view"]=="list" and qa_pw_read_selection(["V111:E11"]))
    if eval (not qa_pw_read_has("r13_pw_open_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E13") timeout 20
    click id "r13_pw_open_E13"
    assert eval (qa_pw_read_scope()["view"]=="single" and qa_pw_read_scope()["detail"]=="V111:E13")
    assert eval (qa_pw_read_selection(["V111:E11"]) and r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    click id "r13_pw_origin"
    pause .3
    assert eval (qa_pw_read_scope()["origin_open"] and qa_pw_read_selection(["V111:E11"]))
    click id "r13_pw_pair"
    pause .3
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13") and qa_pw_read_scope()["origin_open"])
    assert eval (qa_pw_read_selection(["V111:E11"]) and qa_pw_read_domain()==qa_pw_read_before)
    click id "r13_pw_origin"
    click id "r13_pw_single"
    pause .3
    assert eval (qa_pw_read_scope()["detail"]=="V111:E13" and not qa_pw_read_scope()["origin_open"])
    screenshot "proof_reading_touch_selection_independent-single-keeps-selection.png"
    click id "r13_pw_back_list"
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_prev" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    assert eval (qa_pw_read_selection([]) and qa_pw_read_domain()==qa_pw_read_before)
    assert eval (not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    run Function(qa_pw_read_restore)

testcase proof_reading_large_selection_independent:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_read_prepare,True,True)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .6
    $ qa_pw_read_before=qa_pw_read_domain()
    assert eval (qa_pw_read_scope()["view"]=="list" and qa_pw_read_scope()["L"]["quote_h"]==0)
    assert eval (qa_pw_read_selection([]) and not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    # 비활성 제출 위치를 실제로 눌러도 화면·기회·선택이 그대로다.
    click pos (1086,600)
    pause .3
    assert screen "r13_proof_workspace"
    assert eval (qa_pw_read_domain()==qa_pw_read_before and qa_pw_read_selection([]))
    click id "r13_pw_pair"
    click id "r13_pw_pick_0"
    if eval (not qa_pw_read_has("r13_pw_open_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E11") timeout 20
    click id "r13_pw_open_E11"
    assert eval (qa_pw_read_scope()["view"]=="pair" and qa_pw_read_scope()["live_pair"]==("V111:E11",None))
    click id "r13_pw_pick_1"
    if eval (not qa_pw_read_has("r13_pw_open_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E13") timeout 20
    click id "r13_pw_open_E13"
    pause .6
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13") and qa_pw_read_selection([]))
    assert eval (qa_pw_read_domain()==qa_pw_read_before and not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    assert eval (r13_pw_read_groups("V111:E11")==[("점검장에 적힌 내용",r13_evidence_facts("V111:E11"))])
    assert eval (r13_pw_read_groups("V111:E13")[-1]==("함께 들은 말",r13_evidence_facts("V111:E13")[-1:]))
    assert eval (qa_pw_read_ranges() is not None and all(value==0 for scroll_range,value in qa_pw_read_ranges()))
    run Function(qa_pw_read_log_ranges)
    # 터치·큰 글씨는 기존 긴 문장을 유지한다. 필요한 스크롤의 끝까지 접근할 수 있어야 한다.
    screenshot "proof_reading_large_selection_independent-pair-zero-selection.png"
    run Function(qa_pw_read_bottom)
    pause .3
    assert eval (all(abs(scroll_range-value)<=1 for scroll_range,value in qa_pw_read_ranges()))
    screenshot "proof_reading_large_selection_independent-pair-scroll-end.png"
    # 발언은 기본 접힘이다. 펼치고 접어도 제출 묶음·기회가 바뀌지 않는다.
    click id "r13_pw_fold"
    pause .3
    assert eval (qa_pw_read_scope()["quote_open"] and qa_pw_read_scope()["L"]["quote_h"]>0)
    click id "r13_pw_fold"
    pause .3
    assert eval (not qa_pw_read_scope()["quote_open"] and qa_pw_read_scope()["L"]["quote_h"]==0)
    click id "r13_pw_back_list"
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_prev" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    assert eval (qa_pw_read_scope()["view"]=="list" and qa_pw_read_selection(["V111:E11"]))
    if eval (not qa_pw_read_has("r13_pw_open_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E13") timeout 20
    click id "r13_pw_open_E13"
    assert eval (qa_pw_read_scope()["view"]=="single" and qa_pw_read_scope()["detail"]=="V111:E13")
    assert eval (qa_pw_read_selection(["V111:E11"]) and r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    click id "r13_pw_origin"
    pause .3
    assert eval (qa_pw_read_scope()["origin_open"] and qa_pw_read_selection(["V111:E11"]))
    click id "r13_pw_pair"
    pause .3
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13") and qa_pw_read_scope()["origin_open"])
    assert eval (qa_pw_read_selection(["V111:E11"]) and qa_pw_read_domain()==qa_pw_read_before)
    click id "r13_pw_origin"
    click id "r13_pw_single"
    pause .3
    assert eval (qa_pw_read_scope()["detail"]=="V111:E13" and not qa_pw_read_scope()["origin_open"])
    screenshot "proof_reading_large_selection_independent-single-keeps-selection.png"
    click id "r13_pw_back_list"
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_prev" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    assert eval (qa_pw_read_selection([]) and qa_pw_read_domain()==qa_pw_read_before)
    assert eval (not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))
    run Function(qa_pw_read_restore)

testcase proof_reading_letter_observation_controls:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    # 두 편지를 확보한 중간 상태 fixture. 비교 정답을 제출하거나 새 사실을 만들지 않는다.
    run Function(r13_grant,["V111:E06","V111:E03"],"qa-proof-reading-letters")
    $ r13_pw_views={}
    run Jump("r13_v111_letter_compare")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    $ qa_pw_read_before=qa_pw_read_domain()
    click id "r13_pw_pair"
    click id "r13_pw_pick_0"
    if eval (not qa_pw_read_has("r13_pw_open_E01")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E01") timeout 20
    click id "r13_pw_open_E01"
    click id "r13_pw_pick_1"
    if eval (not qa_pw_read_has("r13_pw_open_E06")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E06") timeout 20
    click id "r13_pw_open_E06"
    pause .5
    assert eval (qa_pw_read_scope()["mode"]=="compare" and qa_pw_read_selection([]))
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E01","V111:E06") and qa_pw_read_has("r13_pw_observe"))
    click id "r13_pw_observe"
    pause .4
    assert eval (qa_pw_read_scope()["observe"] and all(qa_pw_read_has("r13_pw_spot_%d_%s"%(column,spot)) for column in (0,1) for spot in ("head","body","tail","margin")))
    screenshot "proof-reading-letter-observation.png"
    click id "r13_pw_observe"
    pause .4
    assert eval (not qa_pw_read_scope()["observe"] and qa_pw_read_ranges() is not None)
    assert eval (qa_pw_read_selection([]) and qa_pw_read_domain()==qa_pw_read_before)
    assert eval (not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],qa_pw_read_scope()["mode"]))

    # 실제 세 번째 선택은 기존 두 장을 몰래 바꾸지 않는다. 취소·지정 교체를 각각 확인한다.
    click id "r13_pw_back_list"
    click id "r13_pw_check_E01"
    click id "r13_pw_check_E06"
    click id "r13_pw_check_E03"
    pause .3
    assert eval (qa_pw_read_scope()["replace_pending"]=="V111:E03" and qa_pw_read_selection(["V111:E01","V111:E06"]))
    click id "r13_pw_swap_cancel"
    assert eval (qa_pw_read_scope()["replace_pending"] is None and qa_pw_read_selection(["V111:E01","V111:E06"]))
    click id "r13_pw_check_E03"
    click id "r13_pw_swap_E01"
    assert eval (qa_pw_read_scope()["replace_pending"] is None and qa_pw_read_selection(["V111:E03","V111:E06"]))
    assert eval (qa_pw_read_domain()==qa_pw_read_before)
