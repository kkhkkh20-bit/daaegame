# Focused opening test: the new cut must return to the authored interior.
testcase coach_exterior:
    pause 1.0
    click "처음부터"
    pause .5
    assert screen "r13_coach_exterior"
    assert eval (renpy.music.get_playing()=="assets/bgm-travel.mp3")
    assert eval (renpy.music.get_playing(channel="carriage_ride") is not None)
    screenshot "coach80_landscape.png"
    pause until eval (renpy.get_screen("say") is not None) timeout 20
    assert not screen "r13_coach_exterior"
    assert eval (place=="마차 안" and ms14 is None)
    assert eval (renpy.music.get_playing(channel="carriage_ride") is not None)
    assert eval (not renpy.music.get_playing(channel="pulse"))
    screenshot "coach80_inside.png"
