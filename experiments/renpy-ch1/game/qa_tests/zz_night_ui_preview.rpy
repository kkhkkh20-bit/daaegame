testcase night_ui_preview:
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "say" timeout 30
    pause 1.5
    screenshot "night-01-black.png"
    click pos (900,600)
    pause .6
    click pos (900,600)
    pause .6
    click pos (900,600)
    pause 2.5
    screenshot "night-02-carriage.png"
    click pos (900,600)
    pause 2.5
    screenshot "night-03-carriage.png"
    click pos (900,600)
    pause 2.5
    screenshot "night-04-carriage.png"
    run ShowMenu("pause_menu")
    pause 1.5
    screenshot "night-05-settings-reading.png"
    click "소리"
    pause .8
    screenshot "night-06-settings-sound.png"
    click "화면"
    pause .8
    screenshot "night-07-settings-screen.png"
    click "읽기"
    pause .8
    screenshot "night-07b-settings-reading.png"
    click "닫기"
    pause 1.0
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Jump("r13_v111_gate_proven")
    pause 3.0
    screenshot "night-08-gate.png"
    click pos (900,600)
    pause 3.0
    screenshot "night-09-gate.png"
    click "더보기"
    pause 1.0
    screenshot "night-10-more.png"
    click "설정"
    pause 1.0
    screenshot "night-11-settings-from-more.png"
