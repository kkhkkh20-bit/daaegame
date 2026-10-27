# 2026-10-27 타이포 V2 회의 쪽 캡처 초안. game/qa_tests/ 에 복사해서 돌린다. 커밋하지 않는다.
#   dev/run_renpy_tests.sh zz_type_meeting
# 파일 이름: type-meeting-<화면>-<off|on>-<normal|large>-<pc|touch>.png
#   room13  10일 13호 회의 근접(머리띠·이름표·발언 중 대사)   — v111_newworld_d10.rpy 의 v111_nw_d10_room13_won 과 같은 진입
#   proof   자료 대조 패널(기록 · 자료 대조, 단계 표시, 안내)   — v111_nw_d10_owner_contact_pin 과 같은 진입
#   retry   첫 패배 판(회의를 마치며)                            — v111_nw_d10_room13_half_then_lost 와 같은 진입
# qa_nw_day 는 v111_newworld_d10.rpy 의 init python 에 있다(같은 폴더에 있으면 쓸 수 있다).
# 휴대폰은 zz_type_shots.rpy 와 같이 r13_touch_ui 를 바꿔치기하고, 켜고 끄는 것은 restart_interaction 으로 다시 그린다.

init python:
    def qa_type_meeting_reset():
        # 단계 표시와 되돌리기 안내는 처음 한 번만 나오므로 캡처 전에 되돌린다.
        persistent.r13_proof_guide_done=False
        persistent.r13_recovery_hint_retry=False

testcase zz_type_meeting_room13:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Jump("r13_v111_contact_answer10")
    pause 1.5
    click pos (900,600)
    pause 1.2
    # --- 회의 근접: 머리띠(학교 회의 · 10일째 / 쟁점), 이름표, 대사 ---
    $ R13_TYPE_V2=False
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-room13-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-room13-on-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "type-meeting-room13-on-large-pc.png"
    $ R13_TYPE_V2=False
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-room13-off-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(r13_set_text_size,"normal")
    pause .6
    screenshot "type-meeting-room13-off-normal-touch.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-room13-on-normal-touch.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "type-meeting-room13-on-large-touch.png"
    $ R13_TYPE_V2=True
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")

testcase zz_type_meeting_proof:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(qa_type_meeting_reset)
    run Function(r13_grant,["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER"],"qa")
    run Jump("r13_v111_owner_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    # --- 자료 대조 패널: 빈 상태(단계 1, 안내) ---
    $ R13_TYPE_V2=False
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-proof-empty-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-proof-empty-on-normal-pc.png"
    # --- 자료를 둘 담은 상태(단계 2, 고른 자료 · 2개, 빼기 버튼) ---
    click "자료 고르기"
    pause 0.5
    click "QA V111:E08_CONTACT_ASSEMBLY"
    pause 0.8
    click "QA V111:E09_PIN_OWNER"
    pause 0.8
    click "QA 닫기"
    pause 0.6
    $ R13_TYPE_V2=False
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-proof-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-proof-on-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "type-meeting-proof-on-large-pc.png"
    $ R13_TYPE_V2=False
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-proof-off-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(r13_set_text_size,"normal")
    pause .6
    screenshot "type-meeting-proof-off-normal-touch.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-proof-on-normal-touch.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "type-meeting-proof-on-large-touch.png"
    $ R13_TYPE_V2=True
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")

testcase zz_type_meeting_retry:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(qa_type_meeting_reset)
    run SetVariable("v111_last_presented",["V111:E08_TOOL"])
    run Function(r13_v111_set,"tries:room13",r13_nw_tries_max("room13")-1)
    run Jump("r13_v111_hearing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_meeting_retry_choice" timeout 120
    pause .8
    # --- 첫 패배 판: 회의를 마치며 / 다 있었다 / 두 버튼 / 되돌리기 안내 ---
    $ R13_TYPE_V2=False
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-retry-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-retry-on-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "type-meeting-retry-on-large-pc.png"
    $ R13_TYPE_V2=False
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-retry-off-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(r13_set_text_size,"normal")
    pause .6
    screenshot "type-meeting-retry-off-normal-touch.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-meeting-retry-on-normal-touch.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "type-meeting-retry-on-large-touch.png"
    $ R13_TYPE_V2=True
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    click id "r13_meeting_retry_accept"
