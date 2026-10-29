testcase map_review_locked:
    pause 1.0
    click "처음부터"
    click pos (640,300) until "편지를 외투 안에" timeout 60
    click pos (640,300) until screen "r13_hub" timeout 90
    assert eval (r13_v111_active())
    $ r13_qa_map_before=winter_copy.deepcopy(room13)
    run Show("r13_map")
    pause until eval renpy.get_screen("r13_map").scope["ready"] timeout 10
    assert eval ("workshop" in dict(r13_map_locked_nodes("village")))
    $ r13_qa_map_selected=renpy.get_screen("r13_map").scope["selected"]
    $ r13_qa_map_focus=r13_cart_focus("village","workshop")
    $ renpy.get_widget("r13_map","r13_map_view").xadjustment.change(r13_qa_map_focus[0])
    $ renpy.get_widget("r13_map","r13_map_view").yadjustment.change(r13_qa_map_focus[1])
    pause .3
    click id "map_locked_name_workshop"
    pause .3
    assert eval (renpy.get_screen("r13_map").scope["map_notice"]==r13_map_locked_notice("수리점"))
    assert eval (renpy.get_screen("r13_map").scope["selected"]==r13_qa_map_selected and room13==r13_qa_map_before)
    screenshot "map-review-locked.png"
    run Hide("r13_map")
    assert screen "r13_hub"
    assert eval (room13==r13_qa_map_before)
