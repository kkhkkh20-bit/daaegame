init 999 python:
    def r13_qa_settings_offset(end=False):
        widget=renpy.get_displayable("pause_menu","r13_settings_body")
        widget.yadjustment.change(widget.yadjustment.range if end else 0)

    def r13_qa_mixer_matches(widget_id, mixer, expected):
        widget=renpy.get_displayable("pause_menu",widget_id)
        adj=widget.adjustment
        fill=100.0*adj.value/float(adj.range)
        label=renpy.get_displayable("pause_menu",widget_id+"_percent")
        visible="".join(str(part) for part in label.text)
        return (abs(fill-expected)<0.001 if expected==100 else abs(fill-expected)<=0.5) and r13_mixer_percent(mixer)==int(round(fill)) and visible=="%d%%"%r13_mixer_percent(mixer)

testcase settings_typography:
    pause 2.0
    $ r13_qa_saved_mixers=(_preferences.get_volume("music"),_preferences.get_volume("sfx"))
    $ persistent.room13_option_tab="reading"
    run Function(r13_set_text_size,"normal")
    run Show("pause_menu")
    pause 0.5
    assert eval (r13_opt_size()==22 and r13_opt_title_size()==30)
    screenshot "settings-type-01-normal-reading.png"
    click "소리"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-02-normal-sound.png"
    # Actual pointer input, relative to the rendered bars rather than the screen.
    click id "music_volume" pos (0.5,0.5)
    click id "fx_volume" pos (0.5,0.5)
    pause 0.3
    assert eval (r13_qa_mixer_matches("music_volume","music",50))
    assert eval (r13_qa_mixer_matches("fx_volume","sfx",50))
    screenshot "settings-volume-50-percent.png"
    drag id "music_volume" pos (0.5,0.5) to id "music_volume" pos (1.1,0.5) steps 20
    drag id "fx_volume" pos (0.5,0.5) to id "fx_volume" pos (1.1,0.5) steps 20
    pause 0.3
    assert eval (r13_qa_mixer_matches("music_volume","music",100))
    assert eval (r13_qa_mixer_matches("fx_volume","sfx",100))
    screenshot "settings-volume-100-percent.png"
    $ _preferences.set_volume("music",r13_qa_saved_mixers[0])
    $ _preferences.set_volume("sfx",r13_qa_saved_mixers[1])
    click "화면"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-03-normal-screen.png"
    click "읽기"
    click id "r13_text_size_large"
    run Function(r13_qa_settings_offset)
    pause 0.3
    assert eval (r13_opt_size()==26 and r13_opt_title_size()==34)
    screenshot "settings-type-04-large-reading-top.png"
    run Function(r13_qa_settings_offset,True)
    pause 0.3
    assert eval (renpy.get_screen("pause_menu").scope["typing_preview"].signature[1]==_r13_say_size())
    screenshot "settings-type-05-large-preview-footer.png"
    click "소리"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-06-large-sound.png"
    click "화면"
    run Function(r13_qa_settings_offset)
    pause 0.3
    screenshot "settings-type-07-large-screen.png"
    click "읽기"
    run Function(r13_qa_settings_offset)
    click id "r13_text_size_small"
    pause 0.3
    assert eval (r13_opt_size()==20 and r13_opt_title_size()==27)
    screenshot "settings-type-08-small-reading.png"
    click id "r13_text_size_normal"
    run Hide("pause_menu")
