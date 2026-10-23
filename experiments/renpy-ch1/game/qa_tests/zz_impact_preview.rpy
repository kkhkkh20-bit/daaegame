testcase impact_preview:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Jump("r13_v111_gate_proven")
    pause 2.0
    click pos (900,600) until eval ("slam" in r13_impact_log) timeout 60
    pause .08
    screenshot "impact-01-slam.png"
    pause 1.0
    screenshot "impact-02-after.png"
    click pos (900,600) until eval ("jolt" in r13_impact_log) timeout 60
    pause .05
    screenshot "impact-03-jolt.png"
    assert eval (r13_impact_log[:2]==["slam","jolt"] or "slam" in r13_impact_log)
