# 0.20.5 (Codex A04/B02): phone + large text evidence view, single and side by side.
testcase evidence_large_touch:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    $ persistent.room13_large_text=True
    $ r13_touch_ui=lambda: True
    $ room13["evidence"]=list(room13["evidence"])+[k for k in ("V111:E06","V111:E27","V111:E35","V111:E14_SUPPLY") if k not in room13["evidence"]]
    $ r13_records_view={"tab":"all","detail":"V111:E06","page":0}
    run Show("r13_records")
    pause 1.2
    screenshot "ev-01-single-large-touch.png"
    click "나란히 놓기"
    pause 1.0
    screenshot "ev-02-pair-pick.png"
    click "초대 편지"
    pause 1.2
    screenshot "ev-03-pair-large-touch.png"
    run Hide("r13_records")
    $ persistent.room13_large_text=False
