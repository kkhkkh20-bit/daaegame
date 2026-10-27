# 임시(공개 전 삭제): 근접 대화 붓 원본 시안 캡처
testcase closeup_smooth:
    pause 1.0
    $ _preferences.text_cps=0
    click "처음부터"
    click pos (900,600) until "안아 주진 마" timeout 90
    pause 0.8
    screenshot "closeup-daram.png"
    click pos (900,600) until screen "r13_hub" timeout 90
    click pos (525,480)
    pause until "여기 있소" timeout 30
    pause 0.8
    screenshot "closeup-dolmok.png"
