# 임시: 선택지 하나면 창 없이 진행(커밋하지 않음)
testcase zz_single_choice_offer13:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"family_school_place",None)
    run Jump("r13_v111_offer13")
    pause 2.0
    assert eval (not renpy.get_screen("choice"))
    screenshot "single_offer13_after.png"
    click pos (900,600) until screen "choice" timeout 60
    pause 1.0
    screenshot "single_offer13_menu.png"

testcase zz_three_choices_one_page:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"family_offer_terms_seen",True)
    run Function(r13_v111_set,"family_school_place","school")
    run Jump("r13_v111_offer13")
    pause until screen "choice" timeout 30
    pause 1.0
    screenshot "three_offer13.png"
