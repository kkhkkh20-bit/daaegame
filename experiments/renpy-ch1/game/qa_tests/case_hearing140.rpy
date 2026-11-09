# 회의 직전 fixture 이후에는 발언·문답·제시·실물 위치를 실제 화면으로 누른다.
init python:
    def qa_hearing140_rows():
        return qa_pw_read_scope().get("hearing_rows",[])
    def qa_hearing140_scope(name):
        screen=renpy.get_screen(name)
        return screen.scope if screen else {}
    def qa_hearing140_prepare(touch=False,large=False,normal=True):
        store.qa_hearing140_before=(tuple(config.variants),persistent.room13_large_text,persistent.room13_text_small)
        config.variants=(["touch"] if touch else [])+["pc",None]
        persistent.room13_large_text=large
        persistent.room13_text_small=False
        store.r13_pw_views={}
        if normal:qa_nw_day3_meeting_ready()
    def qa_hearing140_restore():
        variants,large,small=store.qa_hearing140_before
        config.variants=list(variants)
        persistent.room13_large_text=large
        persistent.room13_text_small=small
    def qa_hearing140_resume():
        renpy.save("hearing140")
        renpy.load("hearing140")

testcase hearing140_lamp_complete:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing140_prepare,False,False)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (qa_pw_read_scope()["view"]=="statements" and len(qa_hearing140_rows())==1)
    assert eval (qa_hearing140_rows()[0]["text"]==r13_v111_line("MS14_D03_S05_L0002")[1])
    assert eval (not r13_case_hearing_quote("MS14_D03_S05_L0017"))
    screenshot "hearing140-01-first-statement.png"
    $ qa140_before=qa_pw_read_domain()
    click id "r13_pw_press"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (qa_pw_read_domain()==qa140_before)
    click id "r13_pw_submit"
    pause .3
    assert eval (qa_pw_read_scope()["view"]=="list" and qa_pw_read_scope()["tab"]=="now")
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E12")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E12") timeout 20
    click id "r13_pw_check_E12"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E13") timeout 20
    click id "r13_pw_check_E13"
    pause .2
    screenshot "hearing140-02-evidence-and-statement.png"
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (len(qa_hearing140_rows())==2 and key=="돌과 매입 기록을 낸다")
    # 이미 확인한 발언에 맞는 자료를 다시 제시해도 현재 쟁점 자동승리·기회차감은 없다.
    click id "r13_hearing_target_MS14_D03_S05_L0002"
    click id "r13_pw_submit"
    pause .3
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E12")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E12") timeout 20
    click id "r13_pw_check_E12"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E13") timeout 20
    click id "r13_pw_check_E13"
    pause .2
    $ qa140_before=qa_pw_read_domain()
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (qa_pw_read_domain()==qa140_before and key=="돌과 매입 기록을 낸다")
    # 현재 발언으로 돌아와 다른 자료 묶음을 고른다. 같은 체크는 선택을 해제한다.
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E12")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E12") timeout 20
    click id "r13_pw_check_E12"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E13")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E13") timeout 20
    click id "r13_pw_check_E13"
    pause .2
    click id "r13_pw_single"
    click id "r13_hearing_target_MS14_D03_S05_L0005"
    click id "r13_pw_submit"
    pause .3
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E15")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E15") timeout 20
    click id "r13_pw_check_E15"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E16")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E16") timeout 20
    click id "r13_pw_check_E16"
    pause .2
    click id "r13_pw_submit"
    click pos (900,600) until "칼끝과 안쪽 조각을 맞춰 본다" timeout 60
    click "칼끝과 안쪽 조각을 맞춰 본다"
    click pos (900,600) until screen "r13_case_inspect" timeout 60
    pause .4
    $ qa140_before=qa_pw_read_domain()
    click id "r13_case_inspect_handle"
    pause .3
    assert eval (qa_pw_read_domain()==qa140_before and not r13_v111_owned("E33"))
    click id "r13_case_inspect_fit"
    pause .3
    screenshot "hearing140-03-knife-fracture.png"
    click id "r13_case_inspect_confirm"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (r13_v111_owned("E33") and r13_v111_owned("E17") and len(qa_hearing140_rows())==3)
    $ qa140_before=qa_pw_read_domain()
    click id "r13_hearing_inspect"
    pause .4
    click id "r13_case_inspect_outer"
    pause .3
    screenshot "hearing140-04-outer-latch.png"
    click id "r13_case_inspect_inner"
    pause .3
    screenshot "hearing140-05-inner-fragment.png"
    click id "r13_case_inspect_close"
    pause .4
    assert eval (qa_pw_read_domain()==qa140_before)
    click id "r13_pw_submit"
    pause .3
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E17")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E17") timeout 20
    click id "r13_pw_check_E17"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E32")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E32") timeout 20
    click id "r13_pw_check_E32"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E33")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E33") timeout 20
    click id "r13_pw_check_E33"
    pause .2
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (len(qa_hearing140_rows())==4 and key=="마지막 점검과 인수한 돌을 연결한다")
    screenshot "hearing140-06-last-explanation.png"
    click id "r13_pw_submit"
    pause .3
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E11")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E11") timeout 20
    click id "r13_pw_check_E11"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E15")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E15") timeout 20
    click id "r13_pw_check_E15"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_E16")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_E16") timeout 20
    click id "r13_pw_check_E16"
    pause .2
    click id "r13_pw_submit"
    click pos (900,600) until "확인된 3번 돌을 돌려 달라고 한다" timeout 90
    assert eval (r13_v111_value("meeting:lamp")=="win")
    screenshot "hearing140-07-meeting-won.png"
    run Function(qa_hearing140_restore)

testcase hearing140_attempt_and_save_touch:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing140_prepare,True,True,False)
    run Function(qa_la_meeting_setup)
    run Jump("r13_lamp_attempt_open3")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (qa_pw_read_scope()["view"]=="statements" and len(qa_hearing140_rows())==1)
    assert eval (qa_hearing140_rows()[0]["target"]=="NW_LA_LA_OPEN3_2" and not r13_case_hearing_quote("MS14_D03_S05_L0002"))
    screenshot "hearing140-08-attempt-touch.png"
    click id "r13_pw_press"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    click id "r13_pw_submit"
    pause .3
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_NW_LA_CHECK")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_NW_LA_CHECK") timeout 20
    click id "r13_pw_check_NW_LA_CHECK"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_NW_LA_FIELD")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_NW_LA_FIELD") timeout 20
    click id "r13_pw_check_NW_LA_FIELD"
    pause .2
    run Function(qa_hearing140_resume)
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (qa_pw_read_selection(["V111:NW_LA_CHECK","V111:NW_LA_FIELD"]) and len(qa_hearing140_rows())==1 and qa_pw_read_scope()["view"]=="list")
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (len(qa_hearing140_rows())==2 and key=="남아 있는 돌과 칼의 사용을 연결한다")
    screenshot "hearing140-09-attempt-second-touch.png"
    click id "r13_pw_submit"
    pause .3
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_NW_LA_CHECK")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_NW_LA_CHECK") timeout 20
    click id "r13_pw_check_NW_LA_CHECK"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_NW_LA_FIELD")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_NW_LA_FIELD") timeout 20
    click id "r13_pw_check_NW_LA_FIELD"
    pause .2
    click id "r13_pw_tab_now"
    pause .2
    if eval (not qa_pw_read_has("r13_pw_check_NW_LA_KNIFE")):
        click id "r13_pw_next" until eval qa_pw_read_has("r13_pw_check_NW_LA_KNIFE") timeout 20
    click id "r13_pw_check_NW_LA_KNIFE"
    pause .2
    click id "r13_pw_submit"
    click pos (900,600) until eval (r13_v111_value("meeting:lamp")=="win") timeout 60
    assert eval (not r13_v111_owned("E15") and not r13_v111_owned("E16"))
    run Function(qa_hearing140_restore)

testcase hearing140_wrong_and_skipped_statement:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing140_prepare,False,False)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    click id "r13_pw_submit"
    pause .3
    click id "r13_pw_check_E14"
    $ qa140_tries=r13_v111_value("tries:lamp") or 0
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval ((r13_v111_value("tries:lamp") or 0)==qa140_tries+1 and r13_v111_value("meeting:lamp") is None)
    # 다음 발언을 실제 건너뛰기 조작으로 생략한다. 캐시 없는 발언은 보여 주지 않는다.
    run Jump("r13_v111_trial_repair_ok")
    pause .4
    click "건너뛰기"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (key=="돌과 매입 기록을 낸다" and not r13_case_hearing_quote("MS14_D03_S05_L0005"))
    assert eval (qa_pw_read_scope()["view"]=="list" and not qa_pw_read_scope()["hearing_rows"] and qa_pw_read_scope()["quote_text"] is None)
    screenshot "hearing140-10-skipped-statement-fallback.png"
    click id "r13_pw_tab_now"
    click id "r13_pw_check_E15"
    click id "r13_pw_check_E16"
    click id "r13_pw_submit"
    click pos (900,600) until "칼끝과 안쪽 조각을 맞춰 본다" timeout 60
    run Function(qa_hearing140_restore)
