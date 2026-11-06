# 장면 앞 상태만 준비한다. 실제 현장 클릭과 기존 QA 자료 선택기를 통해 반환·수신자·시간을 확인한다.
# 제품 자료함의 배치와 실제 자료 선택 화면 검증은 별도 브라우저 검사 범위다.
init python:
    def qa_early_person_point(person):
        # 현재 엔진이 배치한 이름표 좌표만 읽는다. 인물 선택·장소·이야기 상태는 바꾸지 않는다.
        actors=r13_stage_people()
        actor=next(a for a in actors if a["person"]==person)
        face=r13_actor_face_target(actor) or actor["rect"]
        row=next(r for r in r13_actor_nameplates(actors) if r["person"]==person)
        x,y,w,h=row["rect"]
        offset=r13_world_offset()
        zoom=r13_field_zoom()
        store.qa_early_person_x=int((x+w/2.0-offset)*zoom)
        store.qa_early_person_y=int((y+h/2.0)*zoom)
        store.qa_early_person_visible=(face[0]<offset+r13_view_width() and face[0]+face[2]>offset
            and 0<store.qa_early_person_x<1280 and 0<store.qa_early_person_y<720)
        store.qa_early_pan_x=48 if face[0]+face[2]/2.0<offset else 1232

    def qa_early_post_setup():
        r13_v111_set("day",2)
        r13_v111_set("mother_box_checked_day2",True)
        r13_v111_set("arrival_note_sent",True)
        r13_v111_set("location:seryeon","post")
        r13_v111_set("location:daram","post")
        r13_grant(["V111:E01","V111:E02"],"qa")
        r13_edit(location="post",period=0)

    def qa_early_portrait_setup():
        r13_v111_set("day",2)
        r13_v111_set("piko_alive",True)
        r13_v111_set("location:resident_piko","square")
        r13_v111_set("location:daram","square")
        r13_grant(["V111:E07"],"qa")
        r13_edit(location="square",period=0)

testcase v111_early_post_direct_cancel_wrong_and_receiver:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_early_post_setup)
    run Jump("r13_v111_post")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D02_S02_L0002") timeout 45
    assert eval (r13_packet[0]=="seryeon")
    click pos (900,600) until screen "r13_hub" timeout 45
    assert eval (room13["v111"].get("gate")=="envelope_show" and not r13_v111_owned("E07"))
    run SetVariable("qa_early_minutes",r13_v111_value("elapsed_minutes") or 0)
    pause until eval (renpy.get_screen("r13_hub").scope["world_ready"]) timeout 30
    run Function(qa_early_person_point,"seryeon")
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause .7
        run Function(qa_early_person_point,"seryeon")
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    pause until screen "r13_book" timeout 30
    assert eval (not renpy.get_screen("r13_topics") and renpy.get_screen("r13_book").scope["target"]=="seryeon")
    screenshot "early-post-direct-picker.png"
    click "QA 닫기"
    pause until screen "r13_hub" timeout 30
    assert eval (not r13_v111_owned("E07") and r13_v111_value("elapsed_minutes")==qa_early_minutes)
    pause until eval (renpy.get_screen("r13_hub").scope["world_ready"]) timeout 30
    run Function(qa_early_person_point,"seryeon")
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause .7
        run Function(qa_early_person_point,"seryeon")
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    pause until screen "r13_book" timeout 30
    click "QA V111:E02"
    click pos (900,600) until screen "r13_book" timeout 45
    assert eval (room13["v111"].get("gate")=="envelope_show" and not r13_v111_owned("E07"))
    assert eval (r13_v111_value("elapsed_minutes")==qa_early_minutes)
    click "QA V111:E01"
    click pos (900,600) until screen "r13_topics" timeout 60
    assert eval (room13["v111"].get("gate")=="post_menu" and r13_v111_owned("E07"))
    assert eval (r13_v111_value("talked:MS14_D02_S02:seryeon") is True and r13_v111_value("elapsed_minutes")==qa_early_minutes)

testcase v111_early_portrait_single_question_keeps_conversation_and_time:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_early_portrait_setup)
    run Jump("r13_v111_piko2")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D02_S03_L0003") timeout 45
    assert eval (r13_packet[0]=="resident_piko")
    click pos (900,600) until screen "r13_hub" timeout 45
    assert eval (room13["v111"].get("gate")=="portrait_ask" and len(r13_v111_questions("resident_piko"))==1)
    run SetVariable("qa_early_minutes",r13_v111_value("elapsed_minutes") or 0)
    pause until eval (renpy.get_screen("r13_hub").scope["world_ready"]) timeout 30
    run Function(qa_early_person_point,"resident_piko")
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause .7
        run Function(qa_early_person_point,"resident_piko")
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    pause until screen "say" timeout 30
    assert eval (not renpy.get_screen("r13_topics") and r13_v111_value("ui_topic_read:portrait_ask:0") is True)
    assert eval (r13_v111_value("talked:MS14_D02_S03:resident_piko") is True and r13_v111_value("elapsed_minutes")==qa_early_minutes+10)
    screenshot "early-portrait-single-dialogue.png"
    click pos (900,600) until eval (r13_v111_value("portrait_commissioned") is True) timeout 60
    assert eval (r13_v111_value("elapsed_minutes")==qa_early_minutes+10)


# 시안 승인 뒤 확장한 3일 통합 화면에서 선택·오답·충분한 대체 조합을 실제 체크 버튼으로 검증한다.
testcase v111_early_day3_workspace_retry_and_alternate:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    click id "r13_pw_check_E01"
    pause .3
    assert eval (room13["arguments"][v111_claim]==["V111:E01"] and not r13_v111_value("tries:lamp"))
    click "근거 제시"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    assert eval (r13_v111_value("tries:lamp")==1 and not room13["arguments"][v111_claim])
    click id "r13_pw_open_E13"
    pause .3
    assert eval (r13_v111_value("tries:lamp")==1)
    click id "r13_pw_back_list"
    click id "r13_pw_check_E11"
    click id "r13_pw_check_E13"
    pause .3
    screenshot "early-day3-proof-owned-alternate.png"
    click "근거 제시"
    click pos (900,600) until eval (renpy.get_screen("r13_proof_workspace") and v111_claim=="v111:돌과 매입 기록을 낸다") timeout 60
    assert eval (r13_v111_value("tries:lamp")==1 and r13_pw_active("돌과 매입 기록을 낸다"))


testcase v111_early_day3_phone_quote_fits:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(renpy.store.__dict__.__setitem__,"r13_touch_ui",lambda: True)
    run Jump("r13_v111_trial_open")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .5
    click id "r13_pw_fold"
    pause .5
    assert eval (renpy.get_screen("r13_proof_workspace").scope["quote_open"])
    assert eval (renpy.get_screen("r13_proof_workspace").scope["L"]["quote_h"]>=renpy.render(renpy.get_widget("r13_proof_workspace","r13_pw_quote_text"),renpy.get_screen("r13_proof_workspace").scope["L"]["width"]-32,720,0,0).get_size()[1]+20)
    screenshot "early-day3-phone-quote-fits.png"
