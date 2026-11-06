# 중간 상태 fixture에서 실제 3일 분기와 현장 버튼을 실행한다. 1일부터의 자연 주행 검사는 아니다.
# 주민 소식의 전달 완료 시점은 별도 단위 검사로 확인하고, 여기서는 현장 선택·저장 복원·분기 격리에 집중한다.
init python:
    def qa_piko_resident_scene_invariants():
        return dict(day=store.room13["day"],location=store.room13["location"],
            evidence=list(store.room13["evidence"]),minutes=r13_v111_value("elapsed_minutes"),
            tries=r13_v111_value("tries:lamp"),meeting=r13_v111_value("meeting:lamp"),
            alive=r13_v111_value("piko_alive"),portrait=r13_v111_value("portrait"),
            variant=r13_v111_value("E09.variant"))

    def qa_piko_resident_scene_view():
        return dict(near=store.r13_piko_scene_near,
            read={key:bool(r13_v111_value("piko_scene_read:"+key)) for key in ("posture","portrait","daram")},
            progress=qa_piko_resident_scene_invariants())

    def qa_piko_resident_queries_are_pure():
        before=winter_copy.deepcopy(store.room13)
        for person in ("nabi","buri","resident_tok"):
            r13_piko_news_available(person)
            r13_piko_report_due(person)
            r13_piko_report_lines(person)
            r13_piko_echo_lines(person)
        return store.room13==before

testcase piko_scene_actions_order_restore_and_leave:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko_scene_start)
    run Jump("r13_v111_day3")
    click pos (900,600) until screen "r13_piko_scene" timeout 90
    assert eval (r13_v111_value("piko_alive") is False and r13_v111_owned("E09"))
    assert eval (r13_v111_value("portrait")=="unfinished" and r13_v111_value("E09.variant")=="unfinished")
    assert eval (all(not r13_v111_value("piko_scene_read:"+key) for key in ("posture","portrait","daram")))
    assert eval (qa_piko_resident_queries_are_pure() and not r13_v111_value("piko_news3:nabi") and not r13_v111_value("piko_news3:buri"))
    run SetField(persistent,"qa_piko_resident_before",qa_piko_resident_scene_invariants())

    # 표시 순서와 다르게 초상을 먼저 읽는다. 대화가 끝나기 전에는 읽음 표시가 생기지 않는다.
    pause .4
    click id "r13_piko_portrait"
    pause until screen "r13_pw_picture" timeout 30
    click "닫기"
    pause until screen "say" timeout 30
    assert eval (not r13_v111_value("piko_scene_read:portrait"))
    click pos (900,600) until screen "r13_piko_scene" timeout 45
    assert eval (r13_v111_value("piko_scene_read:portrait") is True)
    assert eval (qa_piko_resident_scene_invariants()==persistent.qa_piko_resident_before)

    pause .4
    click id "r13_piko_distance"
    pause until eval (renpy.get_screen("r13_piko_scene") and not r13_piko_scene_near) timeout 30
    pause .4
    click id "r13_piko_daram"
    pause until screen "say" timeout 30
    assert eval (not r13_v111_value("piko_scene_read:daram"))
    click pos (900,600) until screen "r13_piko_scene" timeout 45
    assert eval (r13_v111_value("piko_scene_read:daram") is True and not r13_piko_scene_near)
    assert eval (not r13_v111_value("piko_scene_read:posture") and qa_piko_resident_scene_invariants()==persistent.qa_piko_resident_before)
    screenshot "piko-scene-two-read-picture-folded.png"

    # 그림을 접고 두 질문만 읽은 화면을 저장한다. 실제 버튼으로 상태를 바꾼 뒤 같은 저장을 불러온다.
    run SetField(persistent,"qa_piko_resident_saved_view",qa_piko_resident_scene_view())
    $ renpy.save("qa-piko-resident-scene")
    pause .4
    click id "r13_piko_distance"
    pause until eval (renpy.get_screen("r13_piko_scene") and r13_piko_scene_near) timeout 30
    pause .4
    click id "r13_piko_posture"
    click pos (900,600) until screen "r13_piko_scene" timeout 45
    assert eval (r13_v111_value("piko_scene_read:posture") is True and r13_piko_scene_near)
    run Function(renpy.load,"qa-piko-resident-scene")
    pause 1.0
    assert screen "r13_piko_scene"
    assert eval (qa_piko_resident_scene_view()==persistent.qa_piko_resident_saved_view)
    screenshot "piko-scene-read-and-picture-restored.png"

    pause .4
    click id "r13_piko_posture"
    pause until screen "say" timeout 30
    assert eval (not r13_v111_value("piko_scene_read:posture"))
    click pos (900,600) until screen "r13_piko_scene" timeout 45
    assert eval (all(r13_v111_value("piko_scene_read:"+key) is True for key in ("posture","portrait","daram")))
    # 이미 읽은 초상을 다시 살펴도 자료·시간·기회가 늘어나지 않는다.
    pause .4
    click id "r13_piko_portrait"
    pause until screen "r13_pw_picture" timeout 30
    click "닫기"
    click pos (900,600) until screen "r13_piko_scene" timeout 45
    assert eval (qa_piko_resident_scene_invariants()==persistent.qa_piko_resident_before)
    assert eval (room13["evidence"].count("V111:E09")==1 and not r13_piko_scene_near)
    screenshot "piko-scene-all-read-revisit.png"
    pause .4
    click id "r13_piko_leave"
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (room13["v111"].get("gate")=="lamp_inspect3" and r13_v111_value("piko_alive") is False)
    assert eval (not renpy.get_screen("r13_piko_scene") and not r13_ep_cut_current and "r13_ep_cut" not in renpy.get_showing_tags())
    assert eval (r13_v111_value("E09.variant")=="unfinished" and room13["evidence"].count("V111:E09")==1)

testcase piko_scene_skip_preserves_choice:
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko_scene_start)
    run Jump("r13_v111_day3")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D03_S01_L0002") timeout 60
    click "건너뛰기"
    pause until screen "r13_piko_scene" timeout 45
    pause .5
    assert eval (not r13_conv_skip_run and r13_v111_value("piko_alive") is False and r13_v111_owned("E09"))
    assert eval (all(not r13_v111_value("piko_scene_read:"+key) for key in ("posture","portrait","daram")))
    click id "r13_piko_leave"
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (room13["v111"].get("gate")=="lamp_inspect3")

testcase piko_scene_absent_on_living_routes:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko_scene_start,True)
    run Jump("r13_v111_day3")
    pause .8
    # 잘못 연결된 새 화면이 잠깐 나왔다가 넘어가는 경우도 통과시키지 않는다.
    click pos (900,600) until eval (renpy.get_screen("r13_hub") or renpy.get_screen("r13_piko_scene")) timeout 90
    assert screen "r13_hub"
    assert eval (room13["v111"].get("gate")=="piko_clean" and r13_v111_value("piko_alive") is True)
    assert eval (not renpy.get_screen("r13_piko_scene") and not r13_ep_cut_current)
    assert eval (not r13_piko_report_due("nabi") and not r13_piko_report_due("buri"))

    # 등 절도 미수는 기존 fixture와 실제 day3 분기로 들어가며, 도난판 자료나 사망 화면을 얻지 않는다.
    run Function(qa_la_setup)
    run Jump("r13_v111_day3")
    pause .8
    click pos (900,600) until eval (renpy.get_screen("r13_hub") or renpy.get_screen("r13_piko_scene")) timeout 90
    assert screen "r13_hub"
    assert eval (room13["v111"].get("gate")=="lamp_attempt_field3" and r13_v111_value("piko_alive") is True)
    assert eval (r13_v111_value("lamp_bound2") is True and r13_v111_owned("E09") and r13_v111_value("E09.variant")=="complete")
    assert eval (not renpy.get_screen("r13_piko_scene") and not r13_ep_cut_current and not r13_v111_owned("E15") and not r13_v111_owned("E16"))
    assert eval (all(not r13_v111_value("piko_scene_read:"+key) for key in ("posture","portrait","daram")))
