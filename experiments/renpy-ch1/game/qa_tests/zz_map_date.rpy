# 2026-10-27 지도 이름표 축소·하단 네 조작 통일·현장 날짜판 캡처 초안. game/qa_tests/ 에 복사해 쓴다.
#   소유자 지적 셋 — (1) 마을 지도 글씨 큼 (2) 하단 「선택: …」·「마을」·「이곳으로 이동」·「현장으로」 크기·글자 각각이고 눌림
#   (3) 날짜판 글씨 삐져나옴. 보통/큰 글씨 x PC/휴대폰, 시간대는 「늦은 저녁」(가장 긴 글자)까지 찍는다.
#   시작 순서는 zz_settings_touch 와 같다. 휴대폰은 r13_touch_ui 를 바꿔치기한다.
init 999 python:
    def r13_qa_map_date_touch(on):
        store.r13_touch_ui=(lambda: True) if on else (lambda: False)
        renpy.restart_interaction()

testcase zz_map_date:
    $ _test.timeout=40
    $ preferences.text_cps=0
    $ persistent.room13_large_text=False
    $ persistent.room13_text_small=False
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause .6
    # PC 보통: 현장 날짜판(01 / 일째 / 요일 / 오전) + 장소 이름표
    screenshot "mapdate-01-field-pc-normal.png"
    click "지도" until screen "r13_map" timeout 30
    pause .8
    screenshot "mapdate-02-map-pc-normal.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    # 늦은 저녁: 시간대 글자가 가장 길다(Pretendard Regular 24px 89px < 104px 칸)
    run Function(r13_edit,period=3)
    run Function(renpy.restart_interaction)
    pause .6
    screenshot "mapdate-03-field-pc-normal-late.png"
    # PC 큰 글씨
    run Function(r13_set_text_size,"large")
    pause .6
    screenshot "mapdate-04-field-pc-large-late.png"
    click "지도" until screen "r13_map" timeout 30
    pause .8
    screenshot "mapdate-05-map-pc-large.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    # 휴대폰 큰 글씨 (가장 큰 글자: 날짜판 상한·하단 30px 폭 검증)
    run Function(r13_qa_map_date_touch,True)
    pause .6
    screenshot "mapdate-06-field-touch-large-late.png"
    click "지도" until screen "r13_map" timeout 30
    pause .8
    screenshot "mapdate-07-map-touch-large.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    # 휴대폰 보통
    run Function(r13_set_text_size,"normal")
    pause .6
    screenshot "mapdate-08-field-touch-normal-late.png"
    click "지도" until screen "r13_map" timeout 30
    pause .8
    screenshot "mapdate-09-map-touch-normal.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    # 작게 (지도 이름표 20px 하한 확인)
    run Function(r13_qa_map_date_touch,False)
    run Function(r13_set_text_size,"small")
    pause .6
    click "지도" until screen "r13_map" timeout 30
    pause .8
    screenshot "mapdate-10-map-pc-small.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    run Function(r13_set_text_size,"normal")
    run Function(r13_edit,period=0)
