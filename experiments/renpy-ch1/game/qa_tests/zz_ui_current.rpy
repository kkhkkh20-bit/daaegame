testcase ui_current:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    screenshot "cur-01-choice.png"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    screenshot "cur-02-field.png"
    click "기록"
    pause 1.2
    screenshot "cur-03-records.png"
    run Hide("r13_records")
    pause .6
    click "지도"
    pause 1.2
    screenshot "cur-04-map.png"
    click "현장으로"
    pause 1.5
    click "보리"
    pause 2.0
    screenshot "cur-05-talk.png"
    click pos (900,600)
    pause 1.5
    screenshot "cur-06-questions.png"
