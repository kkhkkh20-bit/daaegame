# 0.20.7: settings on a phone (larger text and buttons) and the source fold toggle.
testcase settings_touch:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ r13_touch_ui=lambda: True
    run ShowMenu("pause_menu")
    pause 1.2
    screenshot "set-01-reading.png"
    $ persistent.room13_large_text=True
    run Function(renpy.restart_interaction)
    pause 1.0
    screenshot "set-02-reading-large.png"
    $ persistent.room13_large_text=False
    run Return()
    pause 0.8
    $ r13_touch_ui=lambda: False
    $ room13["evidence"]=list(room13["evidence"])+["V111:E06"]
    $ r13_records_view={"tab":"all","detail":"V111:E06","page":0}
    run Show("r13_records")
    pause 1.0
    click "출처 펼치기"
    pause 0.6
    screenshot "set-03-origin-open.png"
    click "출처 접기"
    pause 0.6
    screenshot "set-04-origin-folded.png"
