testcase v111_opening_native:
    pause 1.0
    click "처음부터"
    pause 1.0
    assert eval (ms14 is None and room13.get("v111") is not None)
    click pos (900,600) until screen "r13_confirm" timeout 50
    assert eval (not r13_v111_owned("E01"))
    screenshot "v111_letter_input.png"
    click "편지를 펼친다"
    click pos (900,600) until "편지를 접는다" timeout 50
    assert eval (r13_v111_owned("E01"))
    click "마지막 줄을 본다"
    click pos (900,600) until "편지를 접는다" timeout 30
    assert eval r13_v111_value("K01a")
    click "편지를 접는다"
    click pos (900,600) until screen "r13_confirm" timeout 40
    click "마차에서 내린다"
    click pos (900,600) until screen "r13_hub" timeout 50
    assert eval (place=="눈에 막힌 입구" and ms14 is None)
    assert eval (room13["v111"]["gate"]=="gate_request")
    screenshot "v111_gate_field.png"
