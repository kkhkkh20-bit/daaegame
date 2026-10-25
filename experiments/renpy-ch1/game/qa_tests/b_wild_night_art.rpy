screen r13_qa_wild_night_art(scene):
    modal True
    zorder 200
    add r13_background(scene)
    frame:
        area (30,20,1220,52) padding (16,8) background Solid("#071522d9")
        text ("배경 검수 · 이야기 미연결 / "+scene) font R13_UI_BOLD_FONT size 24 color "#fff5e5"

testcase b_wild_night_art:
    $ _test.timeout=30
    pause 2.0
    run Show("r13_qa_wild_night_art",scene="wild_school_classroom")
    pause .3
    screenshot "wild-school-classroom.png"
    run Show("r13_qa_wild_night_art",scene="wild_school_hall")
    pause .3
    screenshot "wild-school-hall.png"
    run Show("r13_qa_wild_night_art",scene="wild_square_burning")
    pause .3
    screenshot "wild-square-burning.png"
    run Show("r13_qa_wild_night_art",scene="wild_road_mouth")
    pause .3
    screenshot "wild-road-mouth.png"
    run Show("r13_qa_wild_night_art",scene="wild_greenhouse")
    pause .3
    screenshot "wild-greenhouse.png"
    run Show("r13_qa_wild_night_art",scene="wild_village_dawn")
    pause .3
    screenshot "wild-village-dawn.png"
    run Hide("r13_qa_wild_night_art")
