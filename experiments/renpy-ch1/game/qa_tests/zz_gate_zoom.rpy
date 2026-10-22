testcase gate_zoom:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.5
    screenshot "zoom-01-field.png"
    run Function(lambda:print("QA_ZOOM",r13_field_zoom(),r13_view_width(),r13_world_offset(),[(a["person"],a.get("pose"),a["rect"]) for a in r13_stage_people()]))
    click "돌목"
    pause 2.0
    screenshot "zoom-02-talk.png"
