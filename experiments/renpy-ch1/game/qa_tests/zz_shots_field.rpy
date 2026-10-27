testcase zz_hub_only:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    screenshot "h01_hub.png"
    click "돌목"
    pause 1.5
    screenshot "h02_dialogue.png"
