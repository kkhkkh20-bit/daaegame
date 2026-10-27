# 2026-10-27 타이포 시안(R13_TYPE_V2) 캡처 초안. game/qa_tests/ 에 복사해서 돌린다. 커밋하지 않는다.
#   dev/run_renpy_tests.sh zz_type_shots
# 파일 이름: type-<화면>-<off|on>-<normal|large>-<pc|touch>.png
# 시험용 대사 한 줄은 b_notebook_choices.rpy 와 같은 방식(r13_lines)이며 이야기 상태를 바꾸지 않는다.
default r13_qa_type_pick = 0

label r13_qa_type_say:
    call r13_lines([("daram","아빠, 이 수첩에 적힌 글씨 좀 봐 줘. 어제 쓴 건데 오늘 보니까 크기가 다 달라 보여.",{"expression":"joy"})],"qa:type-say")
    $ r13_last_partner="daram"
    $ r13_qa_type_pick=0
    menu:
        "수첩을 같이 본다":
            $ r13_qa_type_pick=1
        "나중에 보자고 한다":
            $ r13_qa_type_pick=2
        "다람이에게 직접 읽어 달라고 한다":
            $ r13_qa_type_pick=3
    jump r13_roam

# 같은 장면을 스위치 끄고/켜고 찍는다. 켜면 restart_interaction 으로 화면이 다시 계산된다.
# 휴대폰은 zz_settings_touch.rpy 와 같이 r13_touch_ui 를 바꿔치기한다.
testcase zz_type_shots:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ r13_black_card=False
    run Jump("r13_qa_type_say")
    pause .5
    click pos (640,400) until screen "say" timeout 20
    pause .8
    # --- 대사창 ---
    $ R13_TYPE_V2=False
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    pause .5
    screenshot "type-say-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "type-say-on-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .5
    screenshot "type-say-on-large-pc.png"
    $ R13_TYPE_V2=False
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "type-say-off-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(r13_set_text_size,"normal")
    pause .5
    screenshot "type-say-off-normal-touch.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "type-say-on-normal-touch.png"
    # --- 선택지 ---
    $ R13_TYPE_V2=False
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    pause .3
    click pos (640,400) until screen "choice" timeout 20
    pause .8
    screenshot "type-choice-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "type-choice-on-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .5
    screenshot "type-choice-on-large-pc.png"
    $ R13_TYPE_V2=False
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "type-choice-off-large-pc.png"
    $ r13_touch_ui=lambda: True
    run Function(r13_set_text_size,"normal")
    pause .5
    screenshot "type-choice-off-normal-touch.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "type-choice-on-normal-touch.png"
    $ R13_TYPE_V2=False
    $ r13_touch_ui=lambda: False
    run Function(r13_set_text_size,"normal")
    pause .3
    click id "r13_notebook_choice_1"
    pause .5
    assert eval (r13_qa_type_pick==1)
    click pos (640,400) until screen "r13_hub" timeout 40
    # --- 기록 화면 (zz_evidence_large_touch.rpy 와 같은 자료 세팅) ---
    $ room13["evidence"]=list(room13["evidence"])+[k for k in ("V111:E06","V111:E27","V111:E35","V111:E14_SUPPLY") if k not in room13["evidence"]]
    $ r13_records_view={"tab":"all","detail":"V111:E06","page":0}
    run Show("r13_records")
    pause 1.2
    click "출처 펼치기"
    pause .6
    screenshot "type-records-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-records-on-normal-pc.png"
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "type-records-on-large-pc.png"
    $ R13_TYPE_V2=False
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-records-off-large-pc.png"
    run Hide("r13_records")
    $ r13_touch_ui=lambda: True
    run Function(r13_set_text_size,"normal")
    run Show("r13_records")
    pause 1.2
    click "출처 펼치기"
    pause .6
    screenshot "type-records-off-normal-touch.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-records-on-normal-touch.png"
    run Hide("r13_records")
    # --- 대화 기록 탭 ---
    $ r13_touch_ui=lambda: False
    $ R13_TYPE_V2=False
    $ r13_records_view={"tab":"dialogue","detail":None,"page":0}
    run Show("r13_records")
    pause 1.0
    screenshot "type-history-off-normal-pc.png"
    $ R13_TYPE_V2=True
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "type-history-on-normal-pc.png"
    run Hide("r13_records")
    $ R13_TYPE_V2=False
    run Function(r13_set_text_size,"normal")
