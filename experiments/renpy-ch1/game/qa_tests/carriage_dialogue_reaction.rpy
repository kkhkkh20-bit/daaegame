# Owner-requested cause -> reaction -> family exchange, using the actual opening.
testcase carriage_dialogue_reaction:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    pause .5
    click "건너뛰기"
    pause until eval (renpy.get_screen("say") is not None) timeout 20
    pause 1.0
    assert screen "say"
    assert eval (r13_packet[0] is None and r13_packet[1].startswith("마차가 덜컹 기울었다."))
    assert eval (r13_packet[2].get("carriage_jolt") and "r13_visitor" in renpy.get_showing_tags())
    screenshot "carriage79_action.png"
    click pos (900,600)
    pause .5
    assert eval (r13_packet[1]=="과자는 꼭 잡고, 아빠는?" and not r13_packet[2].get("carriage_jolt"))
    screenshot "carriage79_dad.png"
    click pos (900,600)
    pause .5
    assert eval (r13_packet[1]=="아빠는 안 부서지잖아.")
    click pos (900,600)
    pause .5
    assert eval (r13_packet[1]=="넘어지면 아프거든.")
    click pos (900,600)
    pause .5
    assert eval (r13_packet[1].startswith("다람이 한 손으로 내 소매를 잡았다."))
    screenshot "carriage79_sleeve.png"
    click pos (900,600) until "과자는 몇 개 남았어?" timeout 10
    click pos (900,600)
    pause .5
    assert eval (r13_packet[1]=="하나. 엄마 거.")
    screenshot "carriage79_mom.png"
