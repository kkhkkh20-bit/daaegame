# 실제 최종 source_fx 래퍼와 jolt 경로를 엔진에서 확인한다.
testcase retired_hit_audio:
    pause 1.0
    $ renpy.music.stop(channel="scene_fx")
    $ source_effect_log=[]
    $ source_fx("impact")
    $ source_fx("cut9")
    $ source_fx("present")
    assert eval (not source_effect_log and renpy.music.get_playing(channel="scene_fx") is None)
    $ r13_impact("jolt")
    assert eval (r13_impact_log[-1]=="jolt" and renpy.music.get_playing(channel="scene_fx") is None)
    $ source_fx("right")
    assert eval (renpy.music.get_playing(channel="scene_fx")=="assets/sfx-right.wav")
    $ renpy.music.stop(channel="scene_fx")
    $ source_fx("wrong")
    assert eval (renpy.music.get_playing(channel="scene_fx")=="assets/sfx-wrong.wav")
    $ renpy.music.stop(channel="scene_fx")
    screenshot "효과음_전체제거.png"
