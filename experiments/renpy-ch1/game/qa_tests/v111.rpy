testcase v111_opening_native:
    pause 1.0
    click "처음부터"
    pause 1.0
    assert eval (ms14 is None and room13.get("v111") is not None)
    click pos (900,600) until "편지를 접는다" timeout 60
    assert eval (r13_v111_owned("E01"))
    screenshot "v111_letter_input.png"
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (place=="눈에 막힌 입구" and ms14 is None)
    assert eval (room13["v111"]["gate"]=="gate_request")
    click "돌목"
    click pos (900,600) until screen "r13_hub" timeout 30
    assert eval (r13_v111_owned("E02"))
    click "다람"
    pause .4
    assert screen "r13_topics"
    screenshot "v111_gate_field.png"
    click "돌아가기"
    pause .4
    assert screen "r13_hub"
