# 임시: 회의 화면 캡처(커밋하지 않음)
testcase zz_solo_lamp:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run SetVariable("R13_MEETING_SOLO",True)
    run Function(qa_nw_day3_meeting_ready)
    run Jump("r13_v111_trial_open")
    pause 2.0
    screenshot "solo_lamp_1.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_lamp_2.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_lamp_3.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_lamp_4.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_lamp_5.png"

testcase zz_solo_room13:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run SetVariable("R13_MEETING_SOLO",True)
    run Function(qa_nw_day,10,"murder")
    run Jump("r13_v111_contact_answer10")
    pause 2.0
    screenshot "solo_room13_1.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_room13_2.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_room13_3.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_room13_4.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_room13_5.png"

testcase zz_solo_altar:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run SetVariable("R13_MEETING_SOLO",True)
    run Function(qa_nw_day14)
    run Function(r13_edit,location="gate")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_altar1_wrong14")
    pause 2.0
    screenshot "solo_altar_1.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_altar_2.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_altar_3.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_altar_4.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_altar_5.png"

testcase zz_solo_fire:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run SetVariable("R13_MEETING_SOLO",True)
    run Function(qa_nw_day7)
    run Function(r13_v111_set,"NUBI_admitted_setting_fire",True)
    run Function(r13_v111_scene,"MS14_D07_S02")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_responsibility_wrong7")
    pause 2.0
    screenshot "solo_fire_1.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_fire_2.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_fire_3.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_fire_4.png"
    click pos (900,600)
    pause 1.2
    screenshot "solo_fire_5.png"

testcase zz_daram_talk:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_14.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_16.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_18.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_20.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_22.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_24.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_26.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_28.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_30.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_32.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_34.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_36.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_38.png"
    click pos (900,600)
    pause 0.6
    click pos (900,600)
    pause 0.6
    screenshot "d_40.png"
