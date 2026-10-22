# 0.20.7: the proof keeps the book open between picks; a record can be taken back.
testcase proof_pick:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Function(r13_grant,["V111:E01","V111:E02","V111:E03","V111:E04"],"qa")
    run Jump("r13_v111_gate_proof")
    pause 1.5
    click "근거를 내놓는다"
    pause 0.5
    click "QA V111:E02"
    pause 0.6
    click "QA V111:E03"
    pause 0.6
    click "QA V111:E01"
    pause 0.6
    click "QA 닫기"
    pause 0.8
    screenshot "pick-01-three.png"
    assert eval (room13["arguments"]["v111:함께 들어갈 근거를 고른다"]==["V111:E02","V111:E03","V111:E01"])
    click "빼기" pos (0.5,0.5)
    pause 0.8
    screenshot "pick-02-removed.png"
    assert eval (len(room13["arguments"]["v111:함께 들어갈 근거를 고른다"])==2 and not r13_v111_value("tries:gate"))
