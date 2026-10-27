# 임시: 설정창 버튼 폭 시안 캡처(커밋하지 않음)
testcase zz_opt_shots:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run SetVariable("R13_OPT_UNIFIED",False)
    run Show("pause_menu")
    pause 1.0
    click "읽기"
    pause 0.8
    screenshot "a_before_reading.png"
    click "소리"
    pause 0.8
    screenshot "a_before_sound.png"
    click "화면"
    pause 0.8
    screenshot "a_before_screen.png"
    run SetVariable("R13_OPT_UNIFIED",True)
    pause 0.5
    click "읽기"
    pause 0.8
    screenshot "b_after_reading.png"
    click "소리"
    pause 0.8
    screenshot "b_after_sound.png"
    click "화면"
    pause 0.8
    screenshot "b_after_screen.png"
    run Function(r13_set_text_size,"large")
    pause 0.8
    click "읽기"
    pause 0.8
    screenshot "c_after_large_reading.png"
    click "소리"
    pause 0.8
    screenshot "c_after_large_sound.png"
    run SetVariable("R13_OPT_UNIFIED",False)
    pause 0.8
    screenshot "c_before_large_sound.png"
    run Function(r13_set_text_size,"normal")
    run SetVariable("R13_OPT_UNIFIED",True)
# 2026-10-27 외부 리뷰 UI 두 가지 — 화면 캡처 확인용 초안.
# game/qa_tests/ 에 복사해 dev/run_renpy_tests.sh 로 돌린다(qa_nw_day13·qa_nw_day11·qa_retry_seed 는
# 기존 v111_newworld_d13.rpy·v111_meeting_retry.rpy 의 것을 그대로 쓴다).
init python:
    def qa_ui_review_reset():
        # 처음 한 번 안내가 다시 보이게 한다.
        persistent.r13_proof_guide_done=False
        persistent.r13_recovery_hint_retry=False
        persistent.r13_recovery_hint_morning=False

label qa_ui_review_offer13:
    $ qa_nw_day13()
    $ r13_v111_set("family_offer_terms_seen",True)
    jump r13_v111_offer13

label qa_ui_review_family13:
    $ qa_nw_day13()
    jump r13_v111_family_position13

label qa_ui_review_retry_room13:
    $ qa_nw_day(10,"murder")
    $ qa_retry_seed("room13")
    jump r13_v111_hearing_wrong10

testcase zz_ui_review_issue_offer13:
    # 13일 가족 우선 선택: 제목이 「가족 셋이 물러날까, 현장에 남을까」, 직전 대사는 그 아래 작은 줄.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("qa_ui_review_offer13")
    pause until screen "choice" timeout 30
    pause 1.0
    assert eval (r13_choice_issue_menu_id()=="r13_v111_offer13")
    assert eval (renpy.get_widget("choice","r13_choice_issue") is not None)
    screenshot "ui-review-issue-offer13.png"

testcase zz_ui_review_issue_family13:
    # 다른 쟁점 선택창: 「엄마와 다람을 곁에 둘까, 학교로 보낼까」.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("qa_ui_review_family13")
    pause until screen "choice" timeout 30
    pause 1.0
    assert eval (r13_choice_issue_menu_id()=="r13_v111_family_position13")
    screenshot "ui-review-issue-family13.png"

testcase zz_ui_review_plain_choice:
    # 회의(가설 회의) 선택지는 건드리지 않는다: 쟁점 제목이 붙지 않고 회의 선택 화면 그대로.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Jump("r13_v111_hyp1_q11")
    pause until screen "choice" timeout 60
    pause 1.0
    assert eval (r13_choice_issue([("두 사람이 아르카 곁에 머문 시간을 비교한다",None,False)]) is None)
    screenshot "ui-review-plain-choice.png"

testcase zz_ui_review_first_proof:
    # 첫 자료 대조: 0개일 때 1단계, 하나 담은 뒤 2단계 강조. 첫 제출 성공 뒤에는 기존 문장으로 준다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_ui_review_reset)
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"meeting:blanket","win")
    run Function(r13_v111_set,"meeting:hypothesis","win")
    run Function(r13_grant,["V111:E16","V111:NW_PIKO_PAINTING"],"qa")
    run Jump("r13_v111_rein13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    assert eval (renpy.get_widget("r13_crisis_proof","r13_proof_steps") is not None)
    screenshot "ui-review-proof-step1.png"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E16"
    pause 0.8
    click "QA 닫기"
    pause 1.0
    screenshot "ui-review-proof-step2.png"
    click "선택한 근거 제출"
    pause 0.5
    assert eval persistent.r13_proof_guide_done
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    screenshot "ui-review-proof-after-first.png"

testcase zz_ui_review_first_defeat:
    # 첫 회의 패배(기회 소진): 아래에 되돌아갈 수 있는 범위 한 줄. 두 번째에는 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 120
    run Function(qa_ui_review_reset)
    run Jump("qa_ui_review_retry_room13")
    click pos (900,600) until screen "r13_meeting_retry_choice" timeout 60
    pause 1.0
    assert eval (renpy.get_widget("r13_meeting_retry_choice","r13_recovery_retry_note") is not None)
    screenshot "ui-review-first-defeat.png"
    click id "r13_meeting_retry_again"
    pause 1.0
    assert eval persistent.r13_recovery_hint_retry

testcase zz_ui_review_morning_note:
    # 날짜가 처음 바뀐 아침의 안내 쪽지(모양 확인용으로 직접 띄운다).
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 120
    run Show("r13_recovery_note",message="2일 아침을 남겼습니다. 「더보기」의 「다시 시작할 아침」에서 이 아침으로 돌아올 수 있습니다.")
    pause 0.8
    screenshot "ui-review-morning-note.png"
testcase zz_reunion11:
    # 11일 폐온실 재회: 「아빠한테만 말하지 말고. 나한테도.」 얼굴이 대사창에 가리는지 확인(외부 리뷰 그림 3).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_v111_set,"tosil_safe_handoff_confirmed",True)
    run Function(r13_v111_set,"greenhouse_address_known",True)
    run Function(r13_edit,location="greenhouse",period=0)
    run Function(r13_v111_scene,"MS14_D11_S02")
    run Function(r13_v111_arrive,["daram","mom"])
    run Jump("r13_v111_mother_invitation11")
    pause 1.5
    screenshot "reunion11_1.png"
    click pos (900,600)
    pause 1.0
    screenshot "reunion11_2.png"
    click pos (900,600)
    pause 1.0
    screenshot "reunion11_3.png"
    click pos (900,600)
    pause 1.0
    screenshot "reunion11_4.png"
    click pos (900,600)
    pause 1.0
    screenshot "reunion11_5.png"
    click pos (900,600)
    pause 1.0
    screenshot "reunion11_6.png"
