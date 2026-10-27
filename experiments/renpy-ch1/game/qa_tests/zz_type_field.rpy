# 2026-10-27 타이포그래피 V2 2차(현장·지도·질문·설정) 캡처 초안. game/qa_tests/ 에 복사해 쓴다.
#   1일 입구 현장 → 지도 → 주민 질문(qa 화면) → 설정창 읽기 탭. 보통/큰 글씨 x PC/휴대폰.
#   시작 순서는 current_ui_capture / zz_settings_touch 를 본뜬다. 휴대폰은 r13_touch_ui 를 바꿔 흉내 낸다.
init 999 python:
    def r13_qa_type_field_touch(on):
        store.r13_touch_ui=(lambda: True) if on else (lambda: False)
        renpy.restart_interaction()

testcase zz_type_field:
    $ _test.timeout=40
    $ preferences.text_cps=0
    $ persistent.room13_large_text=False
    $ persistent.room13_text_small=False
    $ persistent.room13_window_alpha="d4"
    $ persistent.room13_option_tab="reading"
    pause 2.0
    click "처음부터"
    pause until screen "say" timeout 30
    # 1일 입구: 입구 교정·여관 숙박 전, 생활 시스템은 켜 두어 「가진 돈」 판도 같이 찍힌다.
    run Call("r13_qa_roam",dict(day=1,period=0,location="gate",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    pause .6
    screenshot "type2-01-field-pc-normal.png"
    click "지도" until screen "r13_map" timeout 30
    click "마을"
    pause .8
    screenshot "type2-02-map-pc-normal.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    run Hide("r13_hub")
    run Show("r13_qa_notebook_topics")
    pause .7
    screenshot "type2-03-questions-pc-normal.png"
    run Hide("r13_qa_notebook_topics")
    run ShowMenu("pause_menu")
    pause until screen "pause_menu" timeout 20
    pause .5
    screenshot "type2-04-settings-pc-normal.png"
    # 큰 글씨 (PC)
    click id "r13_text_size_large"
    pause .5
    screenshot "type2-05-settings-pc-large.png"
    run Return()
    pause .8
    run Show("r13_hub")
    pause .6
    screenshot "type2-06-field-pc-large.png"
    click "지도" until screen "r13_map" timeout 30
    click "마을"
    pause .8
    screenshot "type2-07-map-pc-large.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    run Hide("r13_hub")
    run Show("r13_qa_notebook_topics")
    pause .7
    screenshot "type2-08-questions-pc-large.png"
    run Hide("r13_qa_notebook_topics")
    # 휴대폰 (보통)
    $ persistent.room13_large_text=False
    run Function(r13_qa_type_field_touch,True)
    run Show("r13_hub")
    pause .8
    screenshot "type2-09-field-touch-normal.png"
    click "지도" until screen "r13_map" timeout 30
    click "마을"
    pause .8
    screenshot "type2-10-map-touch-normal.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    run Hide("r13_hub")
    run Show("r13_qa_notebook_topics")
    pause .7
    screenshot "type2-11-questions-touch-normal.png"
    run Hide("r13_qa_notebook_topics")
    run ShowMenu("pause_menu")
    pause until screen "pause_menu" timeout 20
    pause .5
    screenshot "type2-12-settings-touch-normal.png"
    # 휴대폰 (큰 글씨)
    click id "r13_text_size_large"
    pause .5
    screenshot "type2-13-settings-touch-large.png"
    run Return()
    pause .8
    run Show("r13_hub")
    pause .6
    screenshot "type2-14-field-touch-large.png"
    click "지도" until screen "r13_map" timeout 30
    click "마을"
    pause .8
    screenshot "type2-15-map-touch-large.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    run Hide("r13_hub")
    run Show("r13_qa_notebook_topics")
    pause .7
    screenshot "type2-16-questions-touch-large.png"
    run Hide("r13_qa_notebook_topics")
    # 원상복구
    $ persistent.room13_large_text=False
    run Function(r13_qa_type_field_touch,False)
    run Show("r13_hub")
