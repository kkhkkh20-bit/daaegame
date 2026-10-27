# 임시 캡처 시험 (2026-10-27 UX 인계서 D01~D03·D06 자료 대조 통합 화면). 공개 전에 지운다.
#   세 시범 장면(1일 입구 · 1일 두 편지 · 7일 화재 첫 추궁)을 PC·휴대폰·큰 글씨로 찍고,
#   체크 → 상세 → 탭 → 선택 유지 → 조사 계속 → 재진입 → 선택·기회 유지를 단언한다.
init 999 python:
    qa_pw_touch_real=r13_touch_ui
    def qa_pw_args(key):
        return list(room13["arguments"].get("v111:"+key,[]))

testcase zz_pw_gate:
    pause 1.0
    $ preferences.text_cps=0
    $ persistent.room13_large_text=False
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_grant,["V111:E01","V111:E02","V111:E03"],"qa")
    run Jump("r13_v111_gate_proof")
    pause 1.5
    assert screen "r13_proof_workspace"
    # T01: 미획득 자료(E04)는 목록에 없다.
    assert eval ("V111:E04" not in r13_pw_entries() and "V111:E02" in r13_pw_entries() and "V111:E01" in r13_pw_entries())
    screenshot "pw-gate-01-pc-empty.png"
    click id "r13_pw_check_E02"
    pause .4
    click id "r13_pw_check_E03"
    pause .4
    assert eval (qa_pw_args("함께 들어갈 근거를 고른다")==["V111:E02","V111:E03"])
    click id "r13_pw_open_E02"
    pause .4
    screenshot "pw-gate-02-pc-detail.png"
    click id "r13_pw_origin"
    pause .4
    screenshot "pw-gate-03-pc-origin.png"
    click id "r13_pw_tab_now"
    pause .4
    assert eval (qa_pw_args("함께 들어갈 근거를 고른다")==["V111:E02","V111:E03"])
    screenshot "pw-gate-04-pc-tab-now.png"
    click id "r13_pw_tab_person"
    pause .4
    screenshot "pw-gate-05-pc-tab-person.png"
    click id "r13_pw_tab_all"
    pause .3
    # T09: 읽기용 나란히 놓기 — 제출 묶음은 그대로다.
    click id "r13_pw_pair"
    pause .4
    click id "r13_pw_open_E01"
    pause .5
    screenshot "pw-gate-06-pc-pair.png"
    assert eval (qa_pw_args("함께 들어갈 근거를 고른다")==["V111:E02","V111:E03"])
    click id "r13_pw_back_list"
    pause .4
    # 칩 × 로 해제
    click id "r13_pw_chip_E03"
    pause .4
    assert eval (qa_pw_args("함께 들어갈 근거를 고른다")==["V111:E02"] and (r13_v111_value("tries:gate") or 0)==0)
    # T04·T05: 조사 계속 → 재진입. 선택·기회 그대로.
    click id "r13_pw_investigate"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval ((r13_v111_value("tries:gate") or 0)==0 and r13_v111_value("meeting:gate") is None)
    run Jump("r13_v111_gate_proof")
    pause 1.5
    assert screen "r13_proof_workspace"
    assert eval (qa_pw_args("함께 들어갈 근거를 고른다")==["V111:E02"])
    screenshot "pw-gate-07-pc-reenter.png"
    $ persistent.room13_large_text=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "pw-gate-08-pc-large.png"
    $ persistent.room13_large_text=False
    run Function(renpy.restart_interaction)
    pause .3
    # T02: 오답 제출은 기존 규칙대로 기회 1회.
    click id "r13_pw_check_E01"
    pause .3
    click id "r13_pw_submit"
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval ((r13_v111_value("tries:gate") or 0)==1 and r13_v111_value("meeting:gate") is None)
    # 휴대폰 배치(D06).
    run Jump("r13_v111_gate_proof")
    pause 1.5
    run Function(renpy.set_screen_variable,"detail",None,screen="r13_proof_workspace")
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "pw-gate-09-touch.png"
    click id "r13_pw_fold"
    pause .4
    screenshot "pw-gate-10-touch-folded.png"
    click id "r13_pw_open_E02"
    pause .4
    screenshot "pw-gate-11-touch-detail.png"
    click id "r13_pw_back_list"
    pause .3
    $ persistent.room13_large_text=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "pw-gate-12-touch-large.png"
    $ persistent.room13_large_text=False
    $ r13_touch_ui=qa_pw_touch_real
    run Function(renpy.restart_interaction)
    pause .3
    assert eval (qa_pw_args("함께 들어갈 근거를 고른다")==["V111:E02"] and (r13_v111_value("tries:gate") or 0)==1)

testcase zz_pw_letters:
    pause 1.0
    $ preferences.text_cps=0
    $ persistent.room13_large_text=False
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_grant,["V111:E01","V111:E02","V111:E06"],"qa")
    run Function(r13_v111_set,"gate_registered",True)
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_letter_compare")
    pause 1.5
    assert screen "r13_proof_workspace"
    screenshot "pw-letters-01-pc.png"
    click id "r13_pw_check_E01"
    pause .3
    click id "r13_pw_check_E06"
    pause .3
    # T08: 셋째를 고르면 자동 교체 없이 바꿀 자리를 묻는다.
    click id "r13_pw_check_E02"
    pause .4
    screenshot "pw-letters-02-pc-replace.png"
    assert eval (qa_pw_args("두 편지를 나란히 본다")==["V111:E01","V111:E06"])
    click id "r13_pw_swap_E06"
    pause .4
    assert eval (qa_pw_args("두 편지를 나란히 본다")==["V111:E01","V111:E02"])
    # 잘못 고른 조합: 기존 무벌점 재시도. 맞는 자료는 남는다.
    click id "r13_pw_submit"
    pause 1.0
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .6
    assert eval ("V111:E01" in qa_pw_args("두 편지를 나란히 본다") and "V111:E02" not in qa_pw_args("두 편지를 나란히 본다"))
    screenshot "pw-letters-03-pc-after-wrong.png"
    click id "r13_pw_check_E06"
    pause .3
    click id "r13_pw_side"
    pause .5
    screenshot "pw-letters-04-pc-pair.png"
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "pw-letters-05-touch-pair.png"
    click id "r13_pw_back_list"
    pause .4
    screenshot "pw-letters-06-touch-list.png"
    $ persistent.room13_large_text=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "pw-letters-07-touch-large.png"
    click id "r13_pw_open_E06"
    pause .4
    screenshot "pw-letters-08-touch-large-detail.png"
    click id "r13_pw_back_list"
    pause .3
    $ persistent.room13_large_text=False
    $ r13_touch_ui=qa_pw_touch_real
    run Function(renpy.restart_interaction)
    pause .3
    click id "r13_pw_side"
    pause .4
    # T07: 비교 마치기 → 기존 성공 판정으로 바로.
    click id "r13_pw_submit"
    click pos (900,600) until "할머니에게 초롱의 행방을 묻는다" timeout 120
    assert eval (sorted(r13_v111_value("proof_given:두 편지를 나란히 본다") or [])==["V111:E01","V111:E06"])

testcase zz_pw_fire:
    pause 1.0
    $ preferences.text_cps=0
    $ persistent.room13_large_text=False
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,7,"murder")
    run Function(r13_grant,["V111:E01","V111:E06_FIRE","V111:E06_EMPTY"],"qa")
    run Function(r13_edit,location="laundry")
    run Jump("r13_v111_nubi_proof7")
    pause 1.5
    assert screen "r13_proof_workspace"
    # T10: 아직 못 들은 증언은 보이지 않는다.
    assert eval (not r13_pw_quote_visible_now("불이 시작된 곳과 진술을 대조한다"))
    screenshot "pw-fire-01-pc-no-witness.png"
    click id "r13_pw_investigate"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval ((r13_v111_value("tries:fire") or 0)==0)
    run Function(r13_v111_set,"bori_nubi_door_witness_heard",True)
    run Jump("r13_v111_nubi_proof7")
    pause 1.5
    assert screen "r13_proof_workspace"
    assert eval (r13_pw_quote_visible_now("불이 시작된 곳과 진술을 대조한다"))
    screenshot "pw-fire-02-pc-witness.png"
    click id "r13_pw_press"
    pause 1.0
    click pos (900,600) until screen "r13_proof_workspace" timeout 30
    pause .6
    assert eval ((r13_v111_value("tries:fire") or 0)==0)
    click id "r13_pw_check_E06_FIRE"
    pause .3
    click id "r13_pw_open_E06_FIRE"
    pause .4
    screenshot "pw-fire-03-pc-detail.png"
    click id "r13_pw_tab_past"
    pause .4
    screenshot "pw-fire-04-pc-tab-past.png"
    click id "r13_pw_tab_all"
    pause .3
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "pw-fire-05-touch-detail.png"
    click id "r13_pw_back_list"
    pause .4
    screenshot "pw-fire-06-touch-list.png"
    click id "r13_pw_fold"
    pause .4
    screenshot "pw-fire-07-touch-folded.png"
    $ persistent.room13_large_text=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "pw-fire-08-touch-large-list.png"
    click id "r13_pw_open_E06_FIRE"
    pause .4
    screenshot "pw-fire-09-touch-large-detail.png"
    click id "r13_pw_back_list"
    pause .4
    $ persistent.room13_large_text=False
    $ r13_touch_ui=qa_pw_touch_real
    run Function(renpy.restart_interaction)
    pause .3
    assert eval (qa_pw_args("불이 시작된 곳과 진술을 대조한다")==["V111:E06_FIRE"])
    click id "r13_pw_submit"
    pause 1.0
    assert eval (r13_v111_value("proof_given:불이 시작된 곳과 진술을 대조한다")==["V111:E06_FIRE"])
