testcase acorn_preview:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Jump("r13_v111_gate_proven")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("r13_v111_registered_depart")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_room_empty")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 90
    run Jump("r13_v111_room_note")
    pause 3.0
    screenshot "acorn-01-memo-line.png"
    click pos (900,600)
    pause 2.5
    screenshot "acorn-02-memo-card.png"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Show("r13_records")
    pause 1.2
    screenshot "acorn-03-records.png"
init python:
    def qa_acorn_seen():
        return any("room13-acorn-ink-crooked" in (getattr(h,"what","") or "") for h in _history_list[-3:])
