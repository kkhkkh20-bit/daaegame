# 첫 방의 읽기 편의는 유지하고, 실제 관찰 뒤에만 비교를 완료한다.
init python:
    def qa_room_letter_discovery_prepare(touch=False,completed=False):
        store.qa_room_letter_touch_before=store.r13_touch_ui
        store.r13_touch_ui=lambda:bool(touch)
        qa_letter_exit_prepare(False)
        store.r13_pw_views={}
        if completed:
            r13_v111_set("proof_given:두 편지를 나란히 본다",["V111:E01","V111:E06"])

    def qa_room_letter_discovery_domain():
        return winter_copy.deepcopy((room13["day"],room13["period"],room13["evidence"],
                                     room13["arguments"],r13_v111_value("elapsed_minutes"),
                                     r13_v111_value("tries:gate"),r13_v111_value("tries:두 편지를 나란히 본다")))

    def qa_room_letter_discovery_restore():
        store.r13_touch_ui=store.qa_room_letter_touch_before
        renpy.set_physical_size((1280,720))

testcase room_letter_discovery_list_and_legacy_return:
    $ preferences.text_cps=0
    run Function(renpy.set_physical_size,(1280,720))
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_room_letter_discovery_prepare)
    run Call("qa_rr_scene","qa_letter_exit_legacy_call")
    pause until screen "r13_proof_workspace" timeout 30
    pause .5
    assert eval (qa_pw_read_scope()["view"]=="list")
    pause until eval (qa_pw_read_scope().get("ready")) timeout 10
    click id "r13_pw_check_E01"
    click id "r13_pw_check_E06"
    $ qa_discovery_domain=qa_room_letter_discovery_domain()
    click id "r13_pw_submit"
    pause until eval (qa_pw_read_scope().get("observe")) timeout 15
    assert eval (qa_room_letter_discovery_domain()==qa_discovery_domain and not r13_v111_value("proof_given:두 편지를 나란히 본다"))
    screenshot "room-letter-list-needs-discovery.png"
    # 테스트 제어기 밖 UI 타이머에서 반환해, 실제 call screen의 옛 반환을 재현한다.
    run Show("r13_qa_inject_return",value="argue")
    pause .6
    assert screen "r13_proof_workspace"
    assert eval (qa_pw_read_scope()["observe"] and qa_room_letter_discovery_domain()==qa_discovery_domain)
    pause until eval (qa_pw_read_scope().get("ready")) timeout 10
    click id "r13_pw_spot_0_head"
    click pos (900,600) until screen "r13_proof_workspace" timeout 45
    assert eval (not r13_v111_value("letter_tail_observed") and not r13_v111_value("proof_given:두 편지를 나란히 본다"))
    assert eval (qa_room_letter_discovery_domain()==qa_discovery_domain)
    pause until eval (qa_pw_read_scope().get("ready")) timeout 10
    click id "r13_pw_spot_0_tail"
    click pos (900,600) until screen "r13_proof_workspace" timeout 45
    assert eval (r13_v111_value("letter_tail_observed") is True and not qa_pw_read_scope()["observe"])
    assert eval (qa_room_letter_discovery_domain()==qa_discovery_domain)
    pause until eval (qa_pw_read_scope().get("ready")) timeout 10
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_hub" timeout 45
    assert eval (r13_v111_value("proof_given:두 편지를 나란히 본다")==["V111:E01","V111:E06"])
    run Function(qa_room_letter_discovery_restore)

testcase room_letter_discovery_direct_tail_touch:
    $ preferences.text_cps=0
    run Function(renpy.set_physical_size,(1280,720))
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_room_letter_discovery_prepare,True)
    run Function(renpy.set_physical_size,(844,390))
    run Call("qa_rr_scene","r13_v111_letter_compare")
    pause until screen "r13_proof_workspace" timeout 30
    pause .6
    $ qa_discovery_domain=qa_room_letter_discovery_domain()
    assert eval (qa_pw_read_scope()["view"]=="pair" and not qa_pw_read_scope()["observe"])
    screenshot "room-letter-tail-touch-before.png"
    pause until eval (qa_pw_read_scope().get("ready")) timeout 10
    # 메뉴의 정답 문구 대신 실제 메모 원문 끝부분을 누른다.
    click id "r13_pw_document_tail_E06"
    click pos (900,600) until screen "r13_proof_workspace" timeout 45
    assert eval (r13_v111_value("letter_tail_observed") is True and not r13_v111_value("proof_given:두 편지를 나란히 본다"))
    assert eval (qa_room_letter_discovery_domain()==qa_discovery_domain and qa_pw_read_selection([]))
    screenshot "room-letter-tail-touch-observed.png"
    pause until eval (qa_pw_read_scope().get("ready")) timeout 10
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_hub" timeout 45
    assert eval (r13_v111_value("proof_given:두 편지를 나란히 본다")==["V111:E01","V111:E06"])
    run Function(qa_room_letter_discovery_restore)

testcase room_letter_discovery_completed_save_compatibility:
    $ preferences.text_cps=0
    run Function(renpy.set_physical_size,(1280,720))
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_room_letter_discovery_prepare,False,True)
    run Call("qa_rr_scene","r13_v111_letter_compare")
    pause until screen "r13_proof_workspace" timeout 30
    pause .5
    assert eval (not r13_room_letters_discovery_pending("두 편지를 나란히 본다",qa_pw_read_scope()["live_pair"]))
    assert eval (not r13_v111_value("letter_tail_observed"))
    pause until eval (qa_pw_read_scope().get("ready")) timeout 10
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_hub" timeout 45
    assert eval (r13_v111_value("proof_given:두 편지를 나란히 본다")==["V111:E01","V111:E06"] and not r13_v111_value("letter_tail_observed"))
    run Function(qa_room_letter_discovery_restore)
