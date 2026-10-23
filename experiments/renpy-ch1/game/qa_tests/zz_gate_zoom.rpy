testcase gate_zoom:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.5
    screenshot "zoom-01-field.png"
    run Function(lambda:print("QA_ZOOM",r13_field_zoom(),r13_view_width(),r13_world_offset(),[(a["person"],a.get("pose"),a["rect"]) for a in r13_stage_people()]))
    click "돌목"
    pause 2.0
    screenshot "zoom-02-talk.png"

testcase gate_zoom_times:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    run Function(r13_edit,period=1)
    pause 1.5
    screenshot "zoom-03-afternoon.png"
    run Function(r13_edit,period=2)
    pause 1.5
    screenshot "zoom-04-evening.png"
