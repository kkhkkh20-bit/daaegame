init python:
    def qa_idle_pick():
        for p in r13_visible_people():
            if r13_v111_idle_ok(p) and p in R13_GREETINGS:
                store.qa_idle_person=p;return
        store.qa_idle_person=None
default qa_idle_person = None

testcase idle_resident:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    run SetVariable("qa_idle_person","resident_bori")
    assert eval (r13_v111_idle_ok("resident_bori"))
    click "보리"
    pause 0.6
    assert eval (not renpy.get_screen("r13_topics"))
    screenshot "idle-greeting.png"
    click pos (900,600) until screen "r13_hub" timeout 30
    assert eval (r13_v111_value("greeted:1:"+qa_idle_person) is True and r13_v111_value("idle_count") is None)
    pause 0.6
    click "보리"
    pause 0.6
    assert eval (not renpy.get_screen("r13_topics"))
    screenshot "idle-thought.png"
    click pos (900,600) until screen "r13_hub" timeout 30
    assert eval (r13_v111_value("idle_count")==1)
