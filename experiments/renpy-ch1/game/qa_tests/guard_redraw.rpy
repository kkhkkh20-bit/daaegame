# 실제 새 게임의 첫 돌목 대사에서 대화 그림을 확인한다.
testcase guard_redraw_gate:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until eval (r13_packet and r13_packet[0]=="guard") timeout 90
    screenshot "돌목_기본대화.png"
    assert eval (r13_dialogue_player_profiles("guard") is not None)
    assert eval (all("dialogue-player-facing/" in f["file"] for p in r13_dialogue_player_profiles("guard").values() for f in p["frames"].values()))
    run Function(r13_speaker,"guard","joy","joy")
    pause 0.3
    screenshot "돌목_웃음.png"
    run Function(r13_speaker,"guard","angry","angry")
    pause 0.3
    screenshot "돌목_화남.png"
    run Function(r13_speaker,"guard","anxious","anxious")
    pause 0.3
    screenshot "돌목_걱정.png"
    run Function(r13_speaker,"guard","flustered","flustered")
    pause 0.3
    screenshot "돌목_당황.png"
    run Function(r13_speaker,"guard","surprise","surprise")
    pause 0.3
    screenshot "돌목_놀람.png"
    run Function(renpy.hide,"r13_visitor")
    run Hide("say")
    run Show("r13_question_list",person="guard",pose="neutral",title="질문",entries=[("입구 등록에 관해",NullAction(),False)],ready=True)
    pause 0.5
    screenshot "돌목_질문.png"
    $ guard_surface_560=renpy.render_to_surface(r13_close_art("guard","neutral",560))
    assert eval (guard_surface_560.get_bounding_rect(min_alpha=16).height>guard_surface_560.get_height()*.8)
    $ guard_surface_760=renpy.render_to_surface(r13_close_art("guard","neutral",760))
    assert eval (guard_surface_760.get_bounding_rect(min_alpha=16).height>guard_surface_760.get_height()*.8)
    $ guard_surface_840=renpy.render_to_surface(r13_close_art("guard","neutral",840))
    assert eval (guard_surface_840.get_bounding_rect(min_alpha=16).height>guard_surface_840.get_height()*.8)
