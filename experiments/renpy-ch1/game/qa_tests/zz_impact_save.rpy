testcase impact_save:
    # Owner QA 2026-10-22: saving on the line after a shaken line raised a pickling error
    # (the shake callback sits in the rollback log's scene lists).
    pause 1.0
    run SetField(persistent,"room13_motion",True)
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Jump("r13_v111_gate_proven")
    pause 2.0
    click pos (900,600) until eval ("slam" in r13_impact_log) timeout 60
    pause .6
    click pos (900,600)
    pause 1.0
    click pos (900,600)
    pause 1.0
    run FileSave(1,page=9,confirm=False)
    pause 1.0
    assert eval (renpy.can_load("9-1"))
    run FileLoad(1,page=9,confirm=False)
    pause 3.0
    assert screen "say"
