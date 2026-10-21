init python:
    def qa_nw_day5(presented):
        r13_v111_set("day",5)
        r13_grant(["V111:"+k for k in ("E20","E22","E23","E24")],"qa")
        r13_edit(location="gate")
        store.v111_last_presented=list(presented)

testcase v111_nw_d05_half_then_lost:
    # Part of the right set once: one more try. A wrong answer after that is final.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day5,["V111:E20"])
    run Jump("r13_v111_wrong5")
    pause 1.0
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("gate_post_hardened") is True and r13_v111_value("meeting:gate_post") is None)
    assert eval (qa_nw_seen("키로는 못 가리오") and not qa_nw_seen("명단에 올리시오"))
    run Function(qa_nw_day5,["V111:E20"])
    run Jump("r13_v111_wrong5")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("meeting:gate_post")=="lose" and r13_v111_value("listed:bami") is True and r13_v111_value("bami_status")=="listed")
    assert eval (qa_nw_seen("밤이는 보호시설 명단에 올리시오") and qa_nw_seen("탐정단 둘밖에"))
    screenshot "v111_nw_d05_lost.png"
