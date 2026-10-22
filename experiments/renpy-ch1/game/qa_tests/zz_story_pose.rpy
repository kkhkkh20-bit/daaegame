# 0.20.7: Daram's field pose in room 13 on day 1 follows the story step.
testcase story_pose:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_note_pick")
    pause 2.0
    click pos (900,600) until screen "r13_hub" timeout 30
    pause 1.0
    screenshot "pose-01-before.png"
    assert eval (r13_daram_home_activity()[0]=="inspect_floor")
    $ r13_grant(["V111:E06","V111:E30"],"qa")
    run Function(renpy.restart_interaction)
    pause 1.0
    screenshot "pose-02-after-drawing.png"
    assert eval (r13_daram_home_activity()[0]=="action_2")
