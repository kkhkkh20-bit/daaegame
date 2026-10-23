testcase reaction_followup:
    # Owner plan item 3: a new question appears once the evidence is in hand.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    click "돌목"
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_owned("E02"))
    click "돌목"
    pause 1.5
    click pos (900,600) until screen "r13_topics" timeout 30
    pause .8
    screenshot "followup-01-topics.png"
    assert eval (any("왜 제 신청이 일꾼으로" in t[0] for t in r13_v111_questions("guard")))
    click "왜 제 신청이 일꾼으로 됐습니까?"
    pause 1.5
    screenshot "followup-02-line.png"
    # 0.20.6: after the answer the same person's questions open again; 「돌아가기」 leaves.
    click pos (200,400) until screen "r13_topics" timeout 60
    assert eval (r13_followup_read("NW_RX_F002"))
    click "돌아가기"
    pause 1.0
    assert screen "r13_hub"
