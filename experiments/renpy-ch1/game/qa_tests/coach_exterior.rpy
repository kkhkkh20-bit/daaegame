# Focused opening test (0.19.97): narration on black replaces the outdoor coach cut,
# then the authored carriage interior follows with the typing sound allowed.
# (No audio device in the QA container, so channels are checked by code review only.)
testcase coach_exterior:
    pause 1.0
    click "처음부터"
    pause until eval (r13_black_card and renpy.get_screen("say") is not None) timeout 20
    assert eval (typing_allowed)
    pause 2.5
    screenshot "black_card_1.png"
    click pos (640,360)
    click pos (640,360)
    pause 2.5
    screenshot "black_card_3.png"
    click pos (640,360) until eval (not r13_black_card and renpy.get_screen("say") is not None) timeout 20
    assert eval (place=="마차 안" and ms14 is None)
    assert eval (typing_allowed)
    # Music/ride channels are not asserted: the QA container has no audio device.
    screenshot "coach82_inside.png"
