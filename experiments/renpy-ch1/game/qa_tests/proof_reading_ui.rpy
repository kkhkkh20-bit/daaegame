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

init python:
    def qa_pw_part1_fire(empty=False):
        # 분기별 후속 논증 직전 자료만 갖춘 UI fixture. 자백·결말·생사 판정은 실행하지 않는다.
        r13_v111_set("day",7)
        r13_v111_set("FIRE_EVACUATED",bool(empty))
        r13_edit(location="school")
        r13_grant(["V111:E06_FIRE","V111:E07_NUBI","V111:"+("E06_EMPTY" if empty else "E06_RESCUE")],"qa-part1-proof")
        store.r13_pw_views={}

testcase proof_reading_day5_bami_shared:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day5,[])
    run Jump("r13_v111_proof5")
    pause until screen "r13_proof_workspace" timeout 40
    pause .5
    $ qa_pw_read_before=qa_pw_read_domain()
    assert eval (v111_claim=="v111:밤이 혐의의 근거를 확인한다" and qa_pw_read_scope()["view"]=="list")
    assert eval (qa_pw_read_scope()["L"]["quote_h"]==0 and not qa_pw_read_has("r13_pw_fold"))
    assert eval (qa_pw_read_selection([]))
    screenshot "part1-day5-bami-list.png"
    if eval (not qa_pw_read_has("r13_pw_open_E20")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E20") timeout 20
    click id "r13_pw_open_E20"
    pause .3
    assert eval (qa_pw_read_scope()["view"]=="single" and qa_pw_read_selection([]))
    assert eval (qa_pw_read_domain()==qa_pw_read_before)
    screenshot "part1-day5-bami-read.png"

testcase proof_reading_day5_letters_shared:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    # 실제 5일 두 번째 편지 확보 뒤에 해당하는 보유 자료 fixture.
    run Function(r13_v111_set,"day",5)
    run Function(r13_grant,["V111:E27"],"qa-part1-letters")
    run Jump("r13_v111_warning_compare5")
    pause until screen "r13_proof_workspace" timeout 40
    pause .5
    $ qa_pw_read_before=qa_pw_read_domain()
    assert eval (qa_pw_read_scope()["mode"]=="compare" and not qa_pw_read_has("r13_pw_fold"))
    click id "r13_pw_pair"
    click id "r13_pw_pick_0"
    if eval (not qa_pw_read_has("r13_pw_open_E01")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_open_E01") timeout 20
    click id "r13_pw_open_E01"
    click id "r13_pw_pick_1"
    if eval (not qa_pw_read_has("r13_pw_open_E27")):
        click id "r13_pw_prev" until eval qa_pw_read_has("r13_pw_open_E27") timeout 20
    click id "r13_pw_open_E27"
    pause .5
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E01","V111:E27") and qa_pw_read_selection([]))
    assert eval (not r13_pw_submit_ok(qa_pw_read_scope()["chosen"],"compare"))
    assert eval (qa_pw_read_domain()==qa_pw_read_before)
    screenshot "part1-day5-letters-read-without-select.png"

testcase proof_reading_fire_empty_shared:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_part1_fire,True)
    run Jump("r13_v111_empty_fire_basis7")
    pause until screen "r13_fire_links" timeout 40
    pause .5
    $ qa_pw_read_before=qa_pw_read_domain()
    assert eval (v111_claim=="v111:불의 원인과 빈 창고 진압을 구분한다" and qa_fire_link_row()["view"]=="board")
    click id "r13_fire_slot_0"
    click id "r13_fire_tab_all"
    click id "r13_fire_pick_E06_FIRE"
    assert eval (qa_pw_read_selection(["V111:E06_FIRE"]) and qa_fire_link_row()["roles"][0]=="V111:E06_FIRE")
    click id "r13_fire_slot_0"
    click id "r13_fire_read_E06_FIRE"
    click id "r13_fire_origin"
    pause .3
    assert eval (qa_pw_read_selection(["V111:E06_FIRE"]) and qa_fire_link_row()["origin"])
    assert eval (qa_pw_read_domain()==qa_pw_read_before and r13_v111_value("meeting:fire") is None)
    screenshot "part1-fire-empty-read-keeps-selection.png"

testcase proof_reading_fire_rescue_shared:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_part1_fire,False)
    run Jump("r13_v111_rescue_fire_basis7")
    pause until screen "r13_fire_links" timeout 40
    pause .5
    $ qa_pw_read_before=qa_pw_read_domain()
    assert eval (v111_claim=="v111:불의 원인과 아이 구조를 구분한다" and qa_fire_link_row()["view"]=="board")
    click id "r13_fire_slot_0"
    click id "r13_fire_tab_all"
    click id "r13_fire_pick_E06_FIRE"
    assert eval (qa_pw_read_selection(["V111:E06_FIRE"]) and qa_fire_link_row()["roles"][0]=="V111:E06_FIRE")
    click id "r13_fire_slot_0"
    click id "r13_fire_read_E06_FIRE"
    click id "r13_fire_origin"
    pause .3
    assert eval (qa_pw_read_selection(["V111:E06_FIRE"]) and qa_fire_link_row()["origin"])
    assert eval (qa_pw_read_domain()==qa_pw_read_before and r13_v111_value("meeting:fire") is None)
    screenshot "part1-fire-rescue-read-keeps-selection.png"

testcase proof_reading_regular_records_touch:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_read_prepare,True,False)
    $ r13_records_view={"tab":"all","detail":"V111:E13","drawer":"now"}
    $ qa_pw_read_before=qa_pw_read_domain()
    run Show("r13_records")
    pause .8
    assert eval (renpy.get_widget("r13_records","r13_ev_picture") is not None)
    assert eval (renpy.get_widget("r13_records","r13_ev_single_reading").yadjustment.range<=1)
    screenshot "part1-records-body-first-touch.png"
    click id "r13_ev_picture"
    pause until screen "r13_pw_picture" timeout 5
    assert eval (qa_pw_read_domain()==qa_pw_read_before)
    click "닫기"
    pause .3
    click id "r13_ev_origin"
    pause .3
    screenshot "part1-records-source-touch.png"
    click id "r13_ev_pair"
    pause .3
    click "초롱의 점검장"
    pause .5
    assert eval (set(renpy.get_screen("r13_records").scope["pair"])=={"V111:E11","V111:E13"})
    assert eval (renpy.get_widget("r13_records","r13_ev_pair_reading_0") is not None)
    assert eval (qa_pw_read_domain()==qa_pw_read_before)
    screenshot "part1-records-pair-body-first-touch.png"
    run Hide("r13_records")
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
    # 책상에서 함께 펼친 두 글은 읽는 자리만 미리 열고, 제출 선택은 비워 둔다.
    assert eval (qa_pw_read_scope()["view"]=="pair")
    assert eval (qa_pw_read_scope()["mode"]=="compare" and qa_pw_read_selection([]))
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E01","V111:E06") and qa_pw_read_has("r13_pw_observe"))
    click id "r13_pw_observe"
    pause .4
    assert eval (qa_pw_read_scope()["observe"] and all(qa_pw_read_has("r13_pw_spot_0_"+spot) and not qa_pw_read_has("r13_pw_spot_1_"+spot) for spot in ("head","body","tail","margin")))
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

# 실제 체크 두 장을 다시 고르지 않고 펼치며, 읽기는 제출·획득 상태를 바꾸지 않는다.
testcase proof_reading_checked_pair_pc:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_read_prepare,False,False)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .6
    $ qa_pw_read_before=qa_pw_read_domain()
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    if eval (not qa_pw_read_has("r13_pw_check_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E13") timeout 20
    click id "r13_pw_check_E13"
    assert eval (qa_pw_read_selection(["V111:E11","V111:E13"]))
    click id "r13_pw_pair"
    pause .5
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13"))
    assert eval (qa_pw_read_selection(["V111:E11","V111:E13"]) and qa_pw_read_domain()==qa_pw_read_before)
    screenshot "checked-pair-pc.png"
    click id "r13_pw_back_list"
    assert screen "r13_proof_workspace"
    assert eval (qa_pw_read_selection(["V111:E11","V111:E13"]) and qa_pw_read_domain()==qa_pw_read_before)
    run Function(qa_pw_read_restore)

# 실제 체크 두 장을 다시 고르지 않고 펼치며, 읽기는 제출·획득 상태를 바꾸지 않는다.
testcase proof_reading_checked_pair_touch:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_pw_read_prepare,True,False)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .6
    $ qa_pw_read_before=qa_pw_read_domain()
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    if eval (not qa_pw_read_has("r13_pw_check_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E13") timeout 20
    click id "r13_pw_check_E13"
    assert eval (qa_pw_read_selection(["V111:E11","V111:E13"]))
    click id "r13_pw_pair"
    pause .5
    assert eval (qa_pw_read_scope()["live_pair"]==("V111:E11","V111:E13"))
    assert eval (qa_pw_read_selection(["V111:E11","V111:E13"]) and qa_pw_read_domain()==qa_pw_read_before)
    screenshot "checked-pair-touch.png"
    click id "r13_pw_back_list"
    assert screen "r13_proof_workspace"
    assert eval (qa_pw_read_selection(["V111:E11","V111:E13"]) and qa_pw_read_domain()==qa_pw_read_before)
    run Function(qa_pw_read_restore)
