# 2026-10-27 자료 대조 패널 정리 캡처 초안. game/qa_tests/ 에 복사해서 돌린다. 커밋하지 않는다.
#   dev/run_renpy_tests.sh zz_proof_v2
# 파일 이름: proof-v2-<상태>-<normal|large>-<pc|touch>.png
#   empty  빈 상태(단계 1 칩, 가운데 한 줄 안내)
#   two    자료 2개(단계 2, 카드 둘 + 빼기)                      — v111_nw_d10_owner_contact_pin 과 같은 진입
#   five   자료 5개(휴대폰 큰 글씨에서도 스크롤 없이 두 열)
#   notice 자료 획득 알림이 패널 아래 오른쪽 한 줄로 내려가는지
# qa_nw_day 는 v111_newworld_d10.rpy 의 init python 에 있다(같은 폴더에 있으면 쓸 수 있다).
# 휴대폰은 zz_type_shots.rpy 와 같이 r13_touch_ui 를 바꿔치기하고 restart_interaction 으로 다시 그린다.

init python:
    def qa_proof_v2_reset():
        # 단계 칩은 첫 제출 성공 전까지만 나오므로 캡처 전에 되돌린다.
        persistent.r13_proof_guide_done=False

    def qa_proof_v2_fill(keys):
        # 자료 고르기 서랍을 거치지 않고 고른 목록을 바로 채운다 — 서랍 조작은 v111_newworld_d10 이 따로 본다.
        copy=winter_copy.deepcopy(room13)
        copy["arguments"][v111_claim]=list(keys)
        store.room13=copy
        renpy.restart_interaction()

    def qa_proof_v2_notice():
        # 패널이 떠 있는 동안 자료 획득 알림이 어디에 뜨는지 본다.
        r13_evidence_acquired(["V111:E14_SUPPLY"])

testcase zz_proof_v2:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(qa_proof_v2_reset)
    run Function(r13_grant,["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER","V111:E08_WOUND_WIRE","V111:E08_TOOL","V111:E09_SCARF"],"qa")
    run Jump("r13_v111_owner_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    # --- 빈 상태 ---
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "proof-v2-empty-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "proof-v2-empty-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "proof-v2-empty-large-touch.png"
    # --- 자료 2개 ---
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    run Function(qa_proof_v2_fill,["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER"])
    pause .6
    screenshot "proof-v2-two-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "proof-v2-two-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "proof-v2-two-large-touch.png"
    run Function(r13_set_text_size,"normal")
    pause .6
    screenshot "proof-v2-two-normal-touch.png"
    # --- 자료 5개 ---
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    run Function(qa_proof_v2_fill,["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER","V111:E08_WOUND_WIRE","V111:E08_TOOL","V111:E09_SCARF"])
    pause .6
    screenshot "proof-v2-five-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "proof-v2-five-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "proof-v2-five-large-touch.png"
    # --- 자료 획득 알림: 패널 아래 오른쪽 한 줄 ---
    run Function(qa_proof_v2_notice)
    pause .5
    screenshot "proof-v2-notice-large-touch.png"
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    run Function(renpy.restart_interaction)
    pause .3
    screenshot "proof-v2-notice-normal-pc.png"
    pause 2.5
    # 빼기 → 네 장, 제출 버튼은 그대로 살아 있다.
    click id "r13_control_빼기"
    pause .6
    screenshot "proof-v2-four-normal-pc.png"
    assert screen "r13_crisis_proof"
