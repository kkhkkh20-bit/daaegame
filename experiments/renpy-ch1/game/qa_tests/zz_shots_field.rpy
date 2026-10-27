# 임시: 타이포 V2 적용 뒤 현장 장면 캡처(커밋하지 않음)
testcase zz_shots_field:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    screenshot "f01_hub.png"
    click "지도" until screen "r13_map" timeout 30
    pause 0.8
    screenshot "f02_map.png"
    click id "r13_map_close"
    pause 0.8
    click "돌목"
    pause 1.5
    screenshot "f03_topics.png"
    click "돌아가기"
    pause 1.0
    run ShowMenu("pause_menu")
    pause 1.0
    screenshot "f04_settings.png"
    click id "r13_text_size_large"
    pause 0.8
    screenshot "f05_settings_large.png"
    run Return()
    pause 1.0
    screenshot "f06_hub_large.png"
    click "지도" until screen "r13_map" timeout 30
    pause 0.8
    screenshot "f07_map_large.png"
    click id "r13_map_close"
    pause 0.8
    click "돌목"
    pause 1.5
    screenshot "f08_topics_large.png"
    click "돌아가기"
    pause 0.5
    run Function(r13_set_text_size,"normal")
