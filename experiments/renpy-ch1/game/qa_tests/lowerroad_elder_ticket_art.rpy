# 기존 인물·자료 ID를 사용하는 그림 검수 장면. 실제 진행 기록을 바꾸지 않는다.
testcase lowerroad_elder_ticket_art:
    $ preferences.text_cps=0
    pause 2.0
    click "처음부터"
    pause until screen "say" timeout 30
    # 새게임 v111 상태를 유지한다. 옛 qa_roam은 해당 상태를 없앤다.
    assert eval (r13_v111_active())
    $ r13_black_card=False
    run Function(r13_v111_set,"day",4)
    run Call("r13_qa_v111_place","inn",0)
    pause until screen "r13_hub" timeout 40
    run Call("r13_qa_v111_lines",[("v111_lowerroad_elder","지팡이를 짚고 천천히 가면 되네.",{"expression":"neutral"})],"qa:lowerroad-elder-art")
    pause until screen "say" timeout 30
    assert eval (R13_FULLBODY["people"]["v111_lowerroad_elder"] is not R13_FULLBODY["people"]["elder"])
    assert eval (r13_fullbody_spec("v111_lowerroad_elder","neutral")["file"]==R13_LOWERROAD_ELDER_BODY)
    assert eval (r13_bdialogue_face("v111_lowerroad_elder","neutral")==R13_LOWERROAD_ELDER_FACE)
    pause 1.0
    assert eval (not r13_black_card and "r13_visitor" in renpy.get_showing_tags())
    screenshot "elder-01-normal.png"
    $ persistent.room13_large_text=True
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause 1.0
    screenshot "elder-02-large-touch.png"
    click pos (640,400) until screen "r13_hub" timeout 30
    run Function(r13_grant,["V111:NW_NUBI_TICKET"],"qa")
    $ r13_records_view={"tab":"all","detail":"V111:NW_NUBI_TICKET","page":0}
    run Show("r13_records")
    pause 1.0
    screenshot "ticket-03-large-touch.png"
    run Hide("r13_records")
    $ persistent.room13_large_text=False
    $ r13_touch_ui=lambda: False
    run Show("r13_records")
    pause 1.0
    screenshot "ticket-04-normal.png"
